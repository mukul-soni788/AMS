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
from datetime import datetime
from typing import List, Dict
from jinja2 import Template
from models.models import *
from datetime import time

router = APIRouter(prefix="/api/doctors", tags=["doctor_appointment"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/add_doctor_availability")
def add_doctor_availability(
    data: dict = Body(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    automatic_slot = data.get("automatic_slot")
    start_time = data.get("start_time")
    end_time = data.get("end_time")
    slot_duration = data.get("slot_duration")
    max_patients_per_slot = data.get("max_patients_per_slot")
    clinic_id = data.get("clinic_id")
    day = data.get("day")

    # Save doctor availability
    doctor_availability = DoctorAvailability(
        doctor_id=user_id,
        day=day,
        start_time=start_time,
        end_time=end_time,
        slot_duration=slot_duration,
        max_patients_per_slot=max_patients_per_slot,
        is_active=data.get("is_active", True),
        clinic_id=clinic_id
    )
    db.add(doctor_availability)

    # Auto slot creation
    if automatic_slot:
        for i in range(start_time, end_time, slot_duration):
            slot = AppointmentSlots(
                doctor_id=user_id,
                clinic_id=clinic_id,
                day=day,
                start_time=i,
                end_time=i + slot_duration,
                slot_duration=slot_duration,
                max_patients_per_slot=max_patients_per_slot
            )
            db.add(slot)
    else:
        manual_slots = data.get("manual_slots", [])
        for slot in manual_slots:
            slot_start = slot.get("start_time")
            slot_end = slot.get("end_time")
            patients_per_slot = slot.get("max_patients_per_slot", max_patients_per_slot)

            if slot_start is None or slot_end is None:
                continue  # Skip invalid slot

            slot_obj = AppointmentSlots(
                doctor_id=user_id,
                clinic_id=clinic_id,
                day=day,
                start_time=slot_start,
                end_time=slot_end,
                slot_duration=slot_duration,
                max_patients_per_slot=patients_per_slot
            )
            db.add(slot_obj)

    db.commit()
    return {"message": "Doctor availability and slots added successfully"}

@router.get("/appointments")
def get_doctor_appointments(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    appointments = db.query(models.Appointments).filter(models.Appointments.doctor_id == user_id).all().order_by(models.Appointments.appointment_date.desc())
    return appointments


@router.get("/appointments/{appointment_id}")
def get_doctor_appointment_details(appointment_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    appointment = db.query(models.Appointments).filter(models.Appointments.id == appointment_id, models.Appointments.doctor_id == user_id).first()
    appointment.patient = db.query(models.Users).filter(models.Users.id == appointment.patient_id).first()
    appointment.slot = db.query(models.AppointmentSlots).filter(models.AppointmentSlots.id == appointment.slot_id).first()
    patient_details = db.query(models.PatientProfiles).filter(models.PatientProfiles.user_id == appointment.patient_id).first()
    medical_history = db.query(models.MedicalHistory).filter(models.MedicalHistory.patient_id == appointment.patient_id).all()
    prescriptions = db.query(models.Prescriptions).filter(models.Prescriptions.patient_id == appointment.patient_id).all()
    appointment.patient_details = patient_details
    appointment.medical_history = medical_history
    appointment.prescriptions = prescriptions
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
                models.AppointmentSlots.patient_id == appointment.patient_id,
                models.AppointmentSlots.doctor_id == appointment.doctor_id,
                models.AppointmentSlots.slot_date == appointment.appointment_date,
                models.AppointmentSlots.start_time == appointment.start_time
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
                models.AppointmentSlots.patient_id == appointment.patient_id,
                models.AppointmentSlots.doctor_id == appointment.doctor_id,
                models.AppointmentSlots.is_available == True
            ).first()
            
            if not new_slot:
                raise HTTPException(status_code=400, detail="New appointment slot is not available or invalid")
            
            # Check for conflicting appointments
            conflicting_appointment = db.query(models.Appointments).filter(
                models.Appointments.patient_id == appointment.patient_id,
                models.Appointments.appointment_date == new_slot.slot_date,
                models.Appointments.start_time == new_slot.start_time,
                models.Appointments.doctor_id == appointment.doctor_id,
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
                models.AppointmentSlots.patient_id == appointment.patient_id,
                models.AppointmentSlots.doctor_id == appointment.doctor_id,
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
            models.AppointmentSlots.patient_id == appointment.patient_id,
            models.AppointmentSlots.doctor_id == appointment.doctor_id,
            models.AppointmentSlots.slot_date == appointment.appointment_date,
            models.AppointmentSlots.start_time == appointment.start_time,
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

