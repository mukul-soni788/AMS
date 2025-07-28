from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import date, time, datetime
from uuid import UUID

# User schemas
class UserBase(BaseModel):
    id: UUID
    email: str
    full_name: str
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    profile_picture: Optional[str] = None
    language_preference: Optional[str] = None
    is_active: Optional[bool] = True
    is_verified: Optional[bool] = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Specialty schemas
class SpecialtyBase(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    category: Optional[str] = None

    class Config:
        from_attributes = True

# Language schemas
class LanguageBase(BaseModel):
    id: UUID
    name: str
    code: str

    class Config:
        from_attributes = True

# Doctor Rating schemas
class DoctorRatingBase(BaseModel):
    id: UUID
    doctor_id: Optional[UUID] = None
    average_rating: Optional[float] = None
    total_reviews: Optional[int] = None
    communication_avg: Optional[float] = None
    punctuality_avg: Optional[float] = None
    expertise_avg: Optional[float] = None
    last_updated: Optional[datetime] = None

    class Config:
        from_attributes = True

# Doctor Profile schemas
class DoctorProfileBase(BaseModel):
    id: UUID
    user_id: Optional[UUID] = None
    medical_license_number: Optional[str] = None
    license_expiry: Optional[date] = None
    years_experience: Optional[int] = None
    bio: Optional[str] = None
    consultation_fee: Optional[float] = None
    telemedicine_enabled: Optional[bool] = False
    is_verified: Optional[bool] = False
    verification_documents: Optional[str] = None
    specialization_primary: Optional[str] = None

    class Config:
        from_attributes = True

class DoctorWithUser(BaseModel):
    id: UUID
    user_id: Optional[UUID] = None
    medical_license_number: Optional[str] = None
    license_expiry: Optional[date] = None
    years_experience: Optional[int] = None
    bio: Optional[str] = None
    consultation_fee: Optional[float] = None
    telemedicine_enabled: Optional[bool] = False
    is_verified: Optional[bool] = False
    verification_documents: Optional[str] = None
    specialization_primary: Optional[str] = None
    user: Optional[UserBase] = None
    doctor_specialties: Optional[List[Dict[str, Any]]] = None
    doctor_languages: Optional[List[Dict[str, Any]]] = None
    doctor_ratings: Optional[List[DoctorRatingBase]] = None

    class Config:
        from_attributes = True

# Clinic Service schemas
class ClinicServiceBase(BaseModel):
    id: UUID
    clinic_id: Optional[UUID] = None
    service_name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    duration_minutes: Optional[int] = None

    class Config:
        from_attributes = True

# Clinic schemas
class ClinicBase(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    license_number: Optional[str] = None
    operating_hours: Optional[Dict[str, Any]] = None
    services_offered: Optional[Dict[str, Any]] = None
    images: Optional[List[str]] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None
    clinic_services: Optional[List[ClinicServiceBase]] = None

    class Config:
        from_attributes = True

# Appointment schemas
class AppointmentBase(BaseModel):
    id: UUID
    appointment_date: date
    patient_id: Optional[UUID] = None
    doctor_id: Optional[UUID] = None
    clinic_id: Optional[UUID] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    consultation_type: Optional[str] = None
    consultation_mode: Optional[str] = None
    status: Optional[str] = "scheduled"
    reason_for_visit: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AppointmentWithDetails(BaseModel):
    id: UUID
    appointment_date: date
    patient_id: Optional[UUID] = None
    doctor_id: Optional[UUID] = None
    clinic_id: Optional[UUID] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    consultation_type: Optional[str] = None
    consultation_mode: Optional[str] = None
    status: Optional[str] = "scheduled"
    reason_for_visit: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    doctor: Optional[DoctorWithUser] = None
    clinic: Optional[ClinicBase] = None

    class Config:
        from_attributes = True

# For backward compatibility
Appointment = AppointmentWithDetails 