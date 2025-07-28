import sys
from app.database import SessionLocal
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, joinedload
from app.routes.profile import get_current_user_id
from fastapi import APIRouter, Depends, HTTPException, Body
from app.models import models
from passlib.context import CryptContext
from app.schemas import *
from datetime import datetime, date, time
from typing import List, Dict
from jinja2 import Template


router = APIRouter(prefix="/api/patients", tags=["profile"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/appointments")
def create_appointment(data: dict = Body(...), db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)): 
    try:
        # Validate required fields
        required_fields = ["slot_id", "doctor_id", "clinic_id"]
        for field in required_fields:
            if field not in data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        slot_id = data.get("slot_id")
        doctor_id = data.get("doctor_id")
        clinic_id = data.get("clinic_id")
        
        # Get the appointment slot by ID
        appointment_slot = db.query(models.AppointmentSlots).filter(
            models.AppointmentSlots.id == slot_id,
            models.AppointmentSlots.doctor_id == doctor_id,
            models.AppointmentSlots.clinic_id == clinic_id,
            models.AppointmentSlots.is_available == True
        ).first()
        
        if not appointment_slot:
            raise HTTPException(status_code=400, detail="Appointment slot is not available or invalid")
        
        # Check for conflicting appointments
        conflicting_appointment = db.query(models.Appointments).filter(
            models.Appointments.doctor_id == doctor_id,
            models.Appointments.appointment_date == appointment_slot.slot_date,
            models.Appointments.start_time == appointment_slot.start_time,
            models.Appointments.status.in_(["scheduled", "confirmed"])
        ).first()
        
        if conflicting_appointment:
            raise HTTPException(status_code=400, detail="Doctor has a conflicting appointment at this time")
        
        # Create appointment using slot data
        appointment = models.Appointments(
            patient_id=user_id,
            appointment_date=appointment_slot.slot_date,
            start_time=appointment_slot.start_time,
            end_time=appointment_slot.end_time,
            doctor_id=doctor_id,
            clinic_id=clinic_id,
            status="scheduled",
            consultation_type=data.get("consultation_type"),
            consultation_mode=data.get("consultation_mode"),
            reason_for_visit=data.get("reason_for_visit", ""),
            notes=data.get("notes", "")
        )
        db.add(appointment)
        db.flush()  # Get the appointment ID
        
        # Update appointment slot availability
        appointment_slot.is_available = False
        appointment_slot.created_at = datetime.now()
        appointment_slot.updated_at = datetime.now()
        appointment_slot.blocked_reason = f"Booked by appointment {appointment.id}"
        
        db.commit()
        db.refresh(appointment)
        
        return {
            "id": appointment.id, 
            "appointment_date": appointment.appointment_date, 
            "start_time": appointment.start_time, 
            "end_time": appointment.end_time,
            "doctor_id": appointment.doctor_id,
            "clinic_id": appointment.clinic_id,
            "status": appointment.status,
            "slot_id": slot_id,
            "message": "Appointment created successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating appointment: {str(e)}")

@router.get("/appointments", response_model=Dict[str, List[AppointmentWithDetails]])
def get_appointments(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    # Fetch all appointments for the user with doctor and clinic information
    all_appointments = db.query(models.Appointments).options(
        joinedload(models.Appointments.doctor).joinedload(models.DoctorProfiles.user),
        joinedload(models.Appointments.clinic),
        joinedload(models.Appointments.appointment_feedback),
        joinedload(models.Appointments.payments),
        joinedload(models.Appointments.invoices),
        joinedload(models.Appointments.medical_visits),
        joinedload(models.Appointments.telemedicine_sessions),
        joinedload(models.Appointments.appointment_reschedule_history)
    ).filter(
        models.Appointments.patient_id == user_id
    ).order_by(models.Appointments.appointment_date.desc()).all()

    if not all_appointments:
        raise HTTPException(status_code=404, detail="No appointments found for this patient.")

    now = datetime.now()

    # Split into past and upcoming
    past_appointments = [appt for appt in all_appointments if appt.appointment_date < now.date()]
    upcoming_appointments = [appt for appt in all_appointments if appt.appointment_date >= now.date()]

    return {
        "past": past_appointments,
        "upcoming": upcoming_appointments
    }


@router.get("/appointments/{appointment_id}/details", response_model=AppointmentWithDetails)
def get_appointment_with_full_details(appointment_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    """
    Get appointment with full details including doctor specialties, languages, and clinic services
    """
    appointment = db.query(models.Appointments).options(
        joinedload(models.Appointments.doctor).joinedload(models.DoctorProfiles.user),
        joinedload(models.Appointments.doctor).joinedload(models.DoctorProfiles.doctor_specialties).joinedload(models.DoctorSpecialties.specialty),
        joinedload(models.Appointments.doctor).joinedload(models.DoctorProfiles.doctor_languages).joinedload(models.DoctorLanguages.language),
        joinedload(models.Appointments.doctor).joinedload(models.DoctorProfiles.doctor_ratings),
        joinedload(models.Appointments.clinic),
        joinedload(models.Appointments.clinic).joinedload(models.Clinics.clinic_services),
        joinedload(models.Appointments.appointment_feedback),
        joinedload(models.Appointments.payments),
        joinedload(models.Appointments.invoices),
        joinedload(models.Appointments.medical_visits),
        joinedload(models.Appointments.telemedicine_sessions),
        joinedload(models.Appointments.appointment_reschedule_history),
        joinedload(models.Appointments.consultation_notes),
    ).filter(
        models.Appointments.id == appointment_id,
        models.Appointments.patient_id == user_id
    ).first()
    
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found.")
    
    return appointment

@router.put("/update_appointment/{appointment_id}")
def update_appointment(appointment_id: int, data: dict = Body(...), db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    try:
        appointment = db.query(models.Appointments).filter(
            models.Appointments.id == appointment_id,
            models.Appointments.patient_id == user_id
        ).first()
        
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found.")
        
        # Store old values for reschedule history
        old_date = appointment.appointment_date
        old_start_time = appointment.start_time
        old_end_time = appointment.end_time
        
        # Check if this is a status update to "completed"
        new_status = data.get("status")
        if new_status == "completed":
            # Update appointment status
            appointment.status = new_status
            appointment.updated_at = datetime.now()
            
            # Free up the appointment slot
            slot = db.query(models.AppointmentSlots).filter(
                models.AppointmentSlots.doctor_id == appointment.doctor_id,
                models.AppointmentSlots.clinic_id == appointment.clinic_id,
                models.AppointmentSlots.slot_date == appointment.appointment_date,
                models.AppointmentSlots.start_time == appointment.start_time,
                models.AppointmentSlots.end_time == appointment.end_time
            ).first()
            
            if slot:
                slot.is_available = True
                slot.blocked_reason = None
            
            db.commit()
            return {"message": "Appointment marked as completed", "appointment": appointment}
        
        # Check if this is a reschedule (slot_id change)
        is_reschedule = False
        new_slot_id = data.get("slot_id")
        
        if new_slot_id and new_slot_id != getattr(appointment, 'slot_id', None):
            is_reschedule = True
            
            # Get the new appointment slot by ID
            new_slot = db.query(models.AppointmentSlots).filter(
                models.AppointmentSlots.id == new_slot_id,
                models.AppointmentSlots.doctor_id == appointment.doctor_id,
                models.AppointmentSlots.clinic_id == appointment.clinic_id,
                models.AppointmentSlots.is_available == True
            ).first()
            
            if not new_slot:
                raise HTTPException(status_code=400, detail="New appointment slot is not available or invalid")
            
            # Check for conflicting appointments
            conflicting_appointment = db.query(models.Appointments).filter(
                models.Appointments.doctor_id == appointment.doctor_id,
                models.Appointments.appointment_date == new_slot.slot_date,
                models.Appointments.start_time == new_slot.start_time,
                models.Appointments.status.in_(["scheduled", "confirmed"]),
                models.Appointments.id != appointment_id
            ).first()
            
            if conflicting_appointment:
                raise HTTPException(status_code=400, detail="Doctor has a conflicting appointment at the new time")
        
        # Update appointment fields
        for key, value in data.items():
            if hasattr(appointment, key):
                setattr(appointment, key, value)
        
        appointment.updated_at = datetime.now()
        
        # Handle reschedule logic
        if is_reschedule:
            # Update appointment with new slot data
            appointment.appointment_date = new_slot.slot_date
            appointment.start_time = new_slot.start_time
            appointment.end_time = new_slot.end_time
            
            # Free up old slot
            old_slot = db.query(models.AppointmentSlots).filter(
                models.AppointmentSlots.doctor_id == appointment.doctor_id,
                models.AppointmentSlots.clinic_id == appointment.clinic_id,
                models.AppointmentSlots.slot_date == old_date,
                models.AppointmentSlots.start_time == old_start_time,
                models.AppointmentSlots.end_time == old_end_time
            ).first()
            
            if old_slot:
                old_slot.is_available = True
                old_slot.blocked_reason = None
            
            # Block new slot
            new_slot.is_available = False
            new_slot.blocked_reason = f"Booked by appointment {appointment.id}"
            
            # Create reschedule history entry
            reschedule_history = models.AppointmentRescheduleHistory(
                appointment_id=appointment.id,
                old_date=old_date,
                old_time=old_start_time,
                new_date=new_slot.slot_date,
                new_time=new_slot.start_time,
                reason=data.get("reschedule_reason", "Patient requested reschedule"),
                rescheduled_by=user_id
            )
            db.add(reschedule_history)
        
        db.commit()
        db.refresh(appointment)
        
        response_message = "Appointment rescheduled successfully" if is_reschedule else "Appointment updated successfully"
        return {"message": response_message, "appointment": appointment}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating appointment: {str(e)}")

@router.delete("/appointments/{appointment_id}")
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    try:
        appointment = db.query(models.Appointments).filter(
            models.Appointments.id == appointment_id,
            models.Appointments.patient_id == user_id
        ).first()
        
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found.")
        
        if appointment.status in ["completed", "cancelled"]:
            raise HTTPException(status_code=400, detail=f"Cannot cancel appointment with status: {appointment.status}")
        
        # Free up the appointment slot
        slot = db.query(models.AppointmentSlots).filter(
            models.AppointmentSlots.doctor_id == appointment.doctor_id,
            models.AppointmentSlots.clinic_id == appointment.clinic_id,
            models.AppointmentSlots.slot_date == appointment.appointment_date,
            models.AppointmentSlots.start_time == appointment.start_time,
            models.AppointmentSlots.end_time == appointment.end_time
        ).first()
        
        if slot:
            slot.is_available = True
            slot.blocked_reason = None
        
        # Update appointment status
        appointment.status = "cancelled"
        appointment.updated_at = datetime.now()
        
        db.commit()
        
        return {"message": "Appointment cancelled successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error cancelling appointment: {str(e)}")

