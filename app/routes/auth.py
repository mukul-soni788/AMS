from fastapi import APIRouter, Depends, HTTPException, status, Request, Body, Header
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import models
from passlib.context import CryptContext
from uuid import UUID
import uuid
import datetime
import secrets
import smtplib
from email.mime.text import MIMEText
import os

router = APIRouter(prefix="/api/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def send_otp_email(to_email: str, otp_code: str):
    smtp_host = os.getenv('SMTP_HOST')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_user = os.getenv('SMTP_USER')
    smtp_pass = os.getenv('SMTP_PASS')
    from_email = os.getenv('FROM_EMAIL', smtp_user)
    subject = 'Your AMS OTP Code'
    body = f'Your OTP code for AMS registration is: {otp_code}\n\nThis code is valid for 10 minutes.'
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    try:
        if smtp_port == 465:
            # SSL connection
            with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=10) as server:
                server.login(smtp_user, smtp_pass)
                server.sendmail(from_email, [to_email], msg.as_string())
        else:
            # StartTLS connection
            with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(smtp_user, smtp_pass)
                server.sendmail(from_email, [to_email], msg.as_string())
    except smtplib.SMTPAuthenticationError:
        print('SMTP Authentication Error: Check your SMTP_USER and SMTP_PASS.')
    except smtplib.SMTPConnectError:
        print('SMTP Connection Error: Could not connect to the SMTP server.')
    except Exception as e:
        print(f'Error sending OTP email: {e}')

# --- REGISTER ---
@router.post("/register")
def register_user(data: dict = Body(...), db: Session = Depends(get_db)):
    required = ["role", "full_name", "email", "phone", "password", "terms_accepted"]
    for field in required:
        if field not in data:
            raise HTTPException(status_code=400, detail=f"Missing field: {field}")
    try:
        # Check for existing email/phone
        if db.query(models.Users).filter(models.Users.email == data["email"]).first():
            raise HTTPException(status_code=409, detail="Email already registered")
        if db.query(models.Users).filter(models.Users.phone == data["phone"]).first():
            raise HTTPException(status_code=409, detail="Phone already registered")
        # Create user
        role = data["role"].lower()
        user = models.Users(
            id=uuid.uuid4(),
            email=data["email"],
            password_hash=hash_password(data["password"]),
            full_name=data["full_name"],
            phone=data["phone"],
            is_active=True,
            is_verified=False,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        # Assign role
        role_obj = db.query(models.Roles).filter(models.Roles.name == role).first()
        if not role_obj:
            db.delete(user)
            db.commit()
            raise HTTPException(status_code=400, detail="Invalid role")
        user_role = models.UserRoles(user_id=user.id, role_id=role_obj.id, assigned_at=datetime.datetime.utcnow())
        db.add(user_role)
        db.commit()
        # Create blank profile row for patient/doctor
        if role == "patient":
            patient_profile = models.PatientProfiles(user_id=user.id)
            db.add(patient_profile)
            db.commit()
        elif role == "doctor":
            doctor_profile = models.DoctorProfiles(user_id=user.id)
            db.add(doctor_profile)
            db.commit()
        elif role == "clinic_admin":
            add_clinic = models.Clinics(
                id=uuid.uuid4(),
                name=data["clinic_name"],
                address=data["clinic_address"],
                phone=data["phone"],
                email=data["email"],
                created_at=datetime.datetime.utcnow(),
                updated_at=datetime.datetime.utcnow(),
            )
            db.add(add_clinic)
            update_clinic_id = models.ClinicAdminProfiles(clinic_id=add_clinic.id, user_id=user.id)
            db.add(update_clinic_id)
            db.commit()
        # Generate OTP for verification
        otp_code = str(secrets.randbelow(1000000)).zfill(6)
        print(otp_code)
        otp = models.OtpCodes(
            id=uuid.uuid4(),
            code_hash=hash_password(otp_code),
            user_id=user.id,
            contact_method="email",
            purpose="register",
            expires_at=datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
            attempts=0,
            is_used=False,
            created_at=datetime.datetime.utcnow(),
        )
        db.add(otp)
        db.commit()
        # Send OTP via email
        send_otp_email(user.email, otp_code)
        return {"user_id": str(user.id), "verification_required": True}
    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        print(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail="Registration failed. Please try again.")

# --- VERIFY OTP ---
@router.post("/verify-otp")
def verify_otp(data: dict = Body(...), db: Session = Depends(get_db)):
    required = ["user_id", "otp_code", "verification_type"]
    for field in required:
        if field not in data:
            raise HTTPException(status_code=400, detail=f"Missing field: {field}")
    user = db.query(models.Users).filter(models.Users.id == UUID(data["user_id"])).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    otp = db.query(models.OtpCodes).filter(
        models.OtpCodes.user_id == user.id,
        models.OtpCodes.purpose == data["verification_type"],
        models.OtpCodes.is_used == False,
        models.OtpCodes.expires_at > datetime.datetime.utcnow()
    ).order_by(models.OtpCodes.created_at.desc()).first()
    if not otp or not verify_password(data["otp_code"], otp.code_hash):
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    otp.is_used = True
    user.is_verified = True
    db.commit()
    # Generate tokens (dummy for now)
    access_token = secrets.token_urlsafe(32)
    refresh_token = secrets.token_urlsafe(32)
    # Save tokens
    token = models.AuthTokens(
        id=uuid.uuid4(),
        token_hash=hash_password(access_token),
        user_id=user.id,
        token_type="access",
        expires_at=datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        is_active=True,
        created_at=datetime.datetime.utcnow(),
    )
    db.add(token)
    db.commit()
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user_profile": {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "phone": user.phone,
            "is_verified": user.is_verified,
            "is_active": user.is_active,
        }
    }

# --- LOGIN ---
@router.post("/login")
def login(data: dict = Body(...), db: Session = Depends(get_db)):
    required = ["email_or_phone", "password"]
    for field in required:
        if field not in data:
            raise HTTPException(status_code=400, detail=f"Missing field: {field}")
    user = db.query(models.Users).filter(
        (models.Users.email == data["email_or_phone"]) | (models.Users.phone == data["email_or_phone"])
    ).first()
    if not user or not verify_password(data["password"], user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is inactive")
    # Generate tokens
    access_token = secrets.token_urlsafe(32)
    refresh_token = secrets.token_urlsafe(32)
    token = models.AuthTokens(
        id=uuid.uuid4(),
        token_hash=hash_password(access_token),
        user_id=user.id,
        token_type="access",
        expires_at=datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        is_active=True,
        created_at=datetime.datetime.utcnow(),
    )
    db.add(token)
    db.commit()
    # Get role
    user_role = db.query(models.UserRoles).filter(models.UserRoles.user_id == user.id).first()
    role = db.query(models.Roles).filter(models.Roles.id == user_role.role_id).first() if user_role else None
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user_profile": {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "phone": user.phone,
            "is_verified": user.is_verified,
            "is_active": user.is_active,
        },
        "role": role.name if role else None
    }

# --- LOGIN OTP ---
@router.post("/login-otp")
def login_otp(data: dict = Body(...), db: Session = Depends(get_db)):
    required = ["contact"]
    for field in required:
        if field not in data:
            raise HTTPException(status_code=400, detail=f"Missing field: {field}")
    user = db.query(models.Users).filter(
        (models.Users.email == data["contact"]) | (models.Users.phone == data["contact"])
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    otp_code = str(secrets.randbelow(1000000)).zfill(6)
    print(otp_code)
    otp = models.OtpCodes(
        id=uuid.uuid4(),
        code_hash=hash_password(otp_code),
        user_id=user.id,
        contact_method="email" if "@" in data["contact"] else "phone",
        purpose="login",
        expires_at=datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
        attempts=0,
        is_used=False,
        created_at=datetime.datetime.utcnow(),
    )
    db.add(otp)
    db.commit()
    # TODO: Send OTP via email/SMS
    return {"otp_sent": True, "expires_in": 600}

# --- SOCIAL LOGIN ---
@router.post("/social-login")
def social_login(data: dict = Body(...)):
    # Placeholder for Google/Apple OAuth
    return {"message": "Social login not implemented in this demo."}

# --- LOGOUT ---
@router.post("/logout")
def logout(Authorization: str = Header(None), db: Session = Depends(get_db)):
    # Expecting 'Bearer <access_token>'
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
                return {"message": "Logged out"}
        except Exception:
            continue
    raise HTTPException(status_code=401, detail="Invalid token")

# --- REFRESH TOKEN ---
@router.post("/refresh-token")
def refresh_token(data: dict = Body(...), db: Session = Depends(get_db)):
    refresh_token = data.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Missing refresh_token")
    # Find the refresh token in DB (simulate, as only access tokens are stored in this demo)
    # In production, you would store refresh tokens and check expiry, etc.
    # Here, just return a new access token for demo
    user_id = data.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id")
    # Generate new access token
    access_token = secrets.token_urlsafe(32)
    token = models.AuthTokens(
        id=uuid.uuid4(),
        token_hash=hash_password(access_token),
        user_id=user_id,
        token_type="access",
        expires_at=datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        is_active=True,
        created_at=datetime.datetime.utcnow(),
    )
    db.add(token)
    db.commit()
    return {"access_token": access_token}

# --- FORGOT PASSWORD ---
@router.post("/forgot-password")
def forgot_password(data: dict = Body(...), db: Session = Depends(get_db)):
    required = ["email_or_phone"]
    for field in required:
        if field not in data:
            raise HTTPException(status_code=400, detail=f"Missing field: {field}")
    user = db.query(models.Users).filter(
        (models.Users.email == data["email_or_phone"]) | (models.Users.phone == data["email_or_phone"])
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    otp_code = str(secrets.randbelow(1000000)).zfill(6)
    otp = models.OtpCodes(
        id=uuid.uuid4(),
        code_hash=hash_password(otp_code),
        user_id=user.id,
        contact_method="email" if "@" in data["email_or_phone"] else "phone",
        purpose="reset_password",
        expires_at=datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
        attempts=0,
        is_used=False,
        created_at=datetime.datetime.utcnow(),
    )
    db.add(otp)
    db.commit()
    # TODO: Send OTP via email/SMS
    return {"reset_link_sent": True, "expires_in": 600}

# --- RESET PASSWORD ---
@router.post("/reset-password")
def reset_password(data: dict = Body(...), db: Session = Depends(get_db)):
    required = ["reset_token", "new_password"]
    for field in required:
        if field not in data:
            raise HTTPException(status_code=400, detail=f"Missing field: {field}")
    otp = db.query(models.OtpCodes).filter(
        models.OtpCodes.code_hash == hash_password(data["reset_token"]),
        models.OtpCodes.purpose == "reset_password",
        models.OtpCodes.is_used == False,
        models.OtpCodes.expires_at > datetime.datetime.utcnow()
    ).first()
    if not otp:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    user = db.query(models.Users).filter(models.Users.id == otp.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.password_hash = hash_password(data["new_password"])
    otp.is_used = True
    db.commit()
    return {"message": "Password reset successful"} 