from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Body, Header
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import models
from uuid import UUID
import uuid
import datetime
import shutil
import os
from passlib.context import CryptContext

router = APIRouter(prefix="/api/profile", tags=["profile"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_current_user_id(Authorization: str = Header(None), db: Session = Depends(get_db)):
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    access_token = Authorization.split(" ", 1)[1]
    # Find the token in DB and deactivate it
    token_obj = db.query(models.AuthTokens).filter(models.AuthTokens.token_hash != None).all()
    for t in token_obj:
        try:
            if verify_password(access_token, t.token_hash):
                t.is_active = False
                db.commit()
                return t.user_id
        except Exception:
            continue
    raise HTTPException(status_code=401, detail="Invalid or expired token")

# --- GET PROFILE ---
@router.get("/me")
def get_profile(user_id: UUID = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_role = db.query(models.UserRoles).filter(models.UserRoles.user_id == user.id).first()
    role = db.query(models.Roles).filter(models.Roles.id == user_role.role_id).first() if user_role else None
    role_name = role.name if role else None
    response = {
        "id": str(user.id),
        "email": user.email,
        "full_name": user.full_name,
        "phone": user.phone,
        "date_of_birth": user.date_of_birth,
        "gender": user.gender,
        "profile_picture": user.profile_picture,
        "language_preference": user.language_preference,
        "is_active": user.is_active,
        "is_verified": user.is_verified,
        "role": role_name
    }
    if role_name == "patient":
        patient_profile = db.query(models.PatientProfiles).filter(models.PatientProfiles.user_id == user.id).first()
        if patient_profile:
            response["patient_profile"] = {
                "emergency_contact_name": patient_profile.emergency_contact_name,
                "emergency_contact_phone": patient_profile.emergency_contact_phone,
                "blood_group": patient_profile.blood_group,
                "allergies": patient_profile.allergies,
                "chronic_conditions": patient_profile.chronic_conditions,
                "insurance_provider": patient_profile.insurance_provider,
                "insurance_policy_number": patient_profile.insurance_policy_number,
                "preferred_language": patient_profile.preferred_language,
            }
            history = db.query(models.MedicalHistory).filter(models.MedicalHistory.patient_id == user.id).all()
            response["medical_history"] = [
                {
                    "id": str(item.id),
                    "condition": item.condition,
                    "diagnosed_date": item.diagnosed_date,
                    "status": item.status,
                    "treatment": item.treatment,
                    "notes": item.notes,
                }
                for item in history
            ]
    elif role_name == "doctor":
        doctor_profile = db.query(models.DoctorProfiles).filter(models.DoctorProfiles.user_id == user.id).first()
        if doctor_profile:
            response["doctor_profile"] = {
                "medical_license_number": doctor_profile.medical_license_number,
                "license_expiry": doctor_profile.license_expiry,
                "years_experience": doctor_profile.years_experience,
                "bio": doctor_profile.bio,
                "consultation_fee": doctor_profile.consultation_fee,
                "telemedicine_enabled": doctor_profile.telemedicine_enabled,
                "is_verified": doctor_profile.is_verified,
                "verification_documents": doctor_profile.verification_documents,
                "specialization_primary": doctor_profile.specialization_primary,
            }
            # Specialties (with description/category/is_primary/certification_date)
            specialties = (
                db.query(models.DoctorSpecialties, models.Specialties)
                .join(models.Specialties, models.DoctorSpecialties.specialty_id == models.Specialties.id)
                .filter(models.DoctorSpecialties.doctor_id == user.id)
                .all()
            )
            response["specialties"] = [
                {
                    "specialty_id": str(ds.specialty_id),
                    "name": s.name,
                    "description": s.description,
                    "category": s.category,
                    "is_primary": ds.is_primary,
                    "certification_date": ds.certification_date,
                }
                for ds, s in specialties
            ]
    return response

# --- UPDATE PROFILE ---
@router.put("/update")
def update_profile(data: dict = Body(...), user_id: UUID = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_role = db.query(models.UserRoles).filter(models.UserRoles.user_id == user.id).first()
    role = db.query(models.Roles).filter(models.Roles.id == user_role.role_id).first() if user_role else None
    role_name = role.name if role else None
    # Update user fields
    for field in ["full_name", "phone", "date_of_birth", "gender", "language_preference"]:
        if field in data:
            setattr(user, field, data[field])
    # Patient profile and medical history
    if role_name == "patient":
        patient_profile = db.query(models.PatientProfiles).filter(models.PatientProfiles.user_id == user.id).first()
        if patient_profile and "patient_profile" in data:
            for field in ["emergency_contact_name", "emergency_contact_phone", "blood_group", "allergies", "chronic_conditions", "insurance_provider", "insurance_policy_number", "preferred_language"]:
                if field in data["patient_profile"]:
                    setattr(patient_profile, field, data["patient_profile"][field])
        # Medical history update (bulk)
        if "medical_history" in data:
            for item in data["medical_history"]:
                if "id" in item:
                    mh = db.query(models.MedicalHistory).filter(models.MedicalHistory.id == UUID(item["id"]), models.MedicalHistory.patient_id == user.id).first()
                    if mh:
                        for field in ["condition", "diagnosed_date", "status", "treatment", "notes"]:
                            if field in item:
                                setattr(mh, field, item[field])
                else:
                    mh = models.MedicalHistory(
                        id=uuid.uuid4(),
                        patient_id=user.id,
                        condition=item.get("condition"),
                        diagnosed_date=item.get("diagnosed_date"),
                        status=item.get("status"),
                        treatment=item.get("treatment"),
                        notes=item.get("notes"),
                    )
                    db.add(mh)
    # Doctor profile and specialties
    if role_name == "doctor":
        doctor_profile = db.query(models.DoctorProfiles).filter(models.DoctorProfiles.user_id == user.id).first()
        if doctor_profile and "doctor_profile" in data:
            for field in ["medical_license_number", "license_expiry", "years_experience", "bio", "consultation_fee", "telemedicine_enabled", "verification_documents", "specialization_primary"]:
                if field in data["doctor_profile"]:
                    setattr(doctor_profile, field, data["doctor_profile"][field])
        # Specialties update (bulk, handle custom names)
        if "specialties" in data:
            db.query(models.DoctorSpecialties).filter(models.DoctorSpecialties.doctor_id == user.id).delete()
            for s in data["specialties"]:
                specialty_id = None
                if "specialty_id" in s and s["specialty_id"]:
                    specialty_id = s["specialty_id"]
                elif "name" in s and s["name"]:
                    # Check if specialty exists (case-insensitive)
                    spec = db.query(models.Specialties).filter(models.Specialties.name.ilike(s["name"])).first()
                    if not spec:
                        spec = models.Specialties(
                            name=s["name"],
                            description=s.get("description"),
                            category=s.get("category")
                        )
                        db.add(spec)
                        db.commit()
                        db.refresh(spec)
                    specialty_id = str(spec.id)
                if specialty_id:
                    specialty = models.DoctorSpecialties(
                        doctor_id=user.id,
                        specialty_id=UUID(specialty_id),
                        is_primary=s.get("is_primary", False),
                        certification_date=s.get("certification_date"),
                    )
                    db.add(specialty)
    user.updated_at = datetime.datetime.utcnow()
    db.commit()
    return {"message": "Profile updated successfully"}

# --- UPLOAD AVATAR ---
@router.post("/upload-avatar")
def upload_avatar(file: UploadFile = File(...), user_id: UUID = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Save file
    upload_dir = "app/static/avatars"
    os.makedirs(upload_dir, exist_ok=True)
    file_ext = os.path.splitext(file.filename)[1]
    filename = f"{user.id}{file_ext}"
    file_path = os.path.join(upload_dir, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    user.profile_picture = f"/static/avatars/{filename}"
    db.commit()
    return {"profile_picture": user.profile_picture}

@router.get("/specialties")
def get_specialties(user_id: UUID = Depends(get_current_user_id), db: Session = Depends(get_db)):
    specialties = db.query(models.Specialties).order_by(models.Specialties.name.asc()).all()
    return [{"id": str(s.id), "name": s.name, "description": s.description, "category": s.category} for s in specialties]

