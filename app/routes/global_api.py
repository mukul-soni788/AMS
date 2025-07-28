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

router = APIRouter(prefix="/api/global", tags=["global"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def update_appointment_slots(doctor_id: int, db: Session):
    appointment_slots = db.query(models.AppointmentSlots).filter(models.AppointmentSlots.doctor_id == doctor_id).all()
    for appointment_slot in appointment_slots:
        appointment_slot.updated_at = datetime.now()
        appointment_slots.is_available = True
        appointment_slots.is_blocked = False
        appointment_slots.blocked_reason = None
    db.commit()

@router.get("/all_doctors")
def get_all_doctors(
    db: Session = Depends(get_db), 
    user_id: int = Depends(get_current_user_id),
    specialty_id: str = None
):
    query = db.query(models.DoctorProfiles)
    if specialty_id:
        query = query.join(models.DoctorSpecialties).filter(models.DoctorSpecialties.specialty_id == specialty_id)
    doctors = query.all()
    return doctors

@router.get("/all_doctors_details/{doctor_id}")
def get_all_doctors_details(doctor_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    doctor = db.query(models.DoctorProfiles).filter(models.DoctorProfiles.id == doctor_id).first()
    
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found.")
    
    appointment_slots = db.query(models.AppointmentSlots).filter(models.AppointmentSlots.doctor_id == doctor.id).all()
    if appointment_slots.updated_at < datetime.now().date():
        update_appointment_slots(doctor_id, db)

    # Get user information
    doctor.user = db.query(models.Users).filter(models.Users.id == doctor.user_id).first()
    
    # Get doctor specialties
    doctor.doctor_specialties = db.query(models.DoctorSpecialties).filter(models.DoctorSpecialties.doctor_id == doctor.id).all()
    
    # Get doctor languages
    doctor.doctor_languages = db.query(models.DoctorLanguages).filter(models.DoctorLanguages.doctor_id == doctor.id).all()
    
    # Get average rating instead of individual ratings
    from sqlalchemy import func
    avg_rating = db.query(func.avg(models.DoctorRatings.rating)).filter(models.DoctorRatings.doctor_id == doctor.id).scalar()
    doctor.average_rating = round(avg_rating, 1) if avg_rating else 0.0
    
    # Get clinic information
    clinic_doctor = db.query(models.ClinicDoctors).filter(models.ClinicDoctors.doctor_id == doctor.id).first()
    if clinic_doctor:
        doctor.clinic = db.query(models.Clinics).filter(models.Clinics.id == clinic_doctor.clinic_id).first()
    
    # Get education
    doctor.educations = db.query(models.Educations).filter(models.Educations.doctor_id == doctor.id).all()
    
    # Get experiences
    doctor.experiences = db.query(models.Experiences).filter(models.Experiences.doctor_id == doctor.id).all()
    
    # Get awards
    doctor.awards = db.query(models.Awards).filter(models.Awards.doctor_id == doctor.id).all()
    
    # Get publications
    doctor.publications = db.query(models.Publications).filter(models.Publications.doctor_id == doctor.id).all()
    
    # Get research interests
    doctor.research_interests = db.query(models.ResearchInterests).filter(models.ResearchInterests.doctor_id == doctor.id).all()
    
    # Get research projects
    doctor.research_projects = db.query(models.ResearchProjects).filter(models.ResearchProjects.doctor_id == doctor.id).all()
    
    # Get research publications
    doctor.research_publications = db.query(models.ResearchPublications).filter(models.ResearchPublications.doctor_id == doctor.id).all()

    doctor.doctor_schedules = db.query(models.DoctorSchedules).filter(models.DoctorSchedules.doctor_id == doctor.id).all()

    doctor.appointment_slots = db.query(models.AppointmentSlots).filter(models.AppointmentSlots.doctor_id == doctor.id, models.AppointmentSlots.is_available == True, models.AppointmentSlots.is_blocked == False, models.AppointmentSlots.start_time >= datetime.now().time()).all()

    doctor.doctor_schedules = db.query(models.DoctorSchedules).filter(models.DoctorSchedules.doctor_id == doctor.id).all()

    
    return doctor  


@router.get("/all_clinics")
def get_all_clinics(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    clinics = db.query(models.Clinics).all()
    return clinics


@router.get("clinic_details/{clinic_id}")
def get_clinic_details(clinic_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    clinic = db.query(models.Clinics).filter(models.Clinics.id == clinic_id).first()
    clinic.clinic_services = db.query(models.ClinicServices).filter(models.ClinicServices.clinic_id == clinic.id).all()
    clinic.clinic_doctors = db.query(models.ClinicDoctors).filter(models.ClinicDoctors.clinic_id == clinic.id).all()
    clinic.clinic_images = db.query(models.ClinicImages).filter(models.ClinicImages.clinic_id == clinic.id).all()
    return clinic

