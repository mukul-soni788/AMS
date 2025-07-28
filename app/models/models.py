from typing import Any, List, Optional

from sqlalchemy import ARRAY, BigInteger, Boolean, CheckConstraint, Date, DateTime, Double, ForeignKeyConstraint, Index, Integer, Numeric, PrimaryKeyConstraint, String, Text, Time, UniqueConstraint, Uuid, text
from sqlalchemy.dialects.postgresql import INET, JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import decimal
import uuid

class Base(DeclarativeBase):
    pass


class AppointmentStatuses(Base):
    __tablename__ = 'appointment_statuses'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='appointment_statuses_pkey'),
        UniqueConstraint('name', name='appointment_statuses_name_key')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(Text)


class BackupLogs(Base):
    __tablename__ = 'backup_logs'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='backup_logs_pkey'),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    backup_type: Mapped[Optional[str]] = mapped_column(String(100))
    file_path: Mapped[Optional[str]] = mapped_column(Text)
    size: Mapped[Optional[int]] = mapped_column(BigInteger)
    status: Mapped[Optional[str]] = mapped_column(String(50))
    started_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    completed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    error_message: Mapped[Optional[str]] = mapped_column(Text)


class Clinics(Base):
    __tablename__ = 'clinics'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='clinics_pkey'),
        Index('idx_clinics_location', 'city', 'state')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    address: Mapped[Optional[str]] = mapped_column(Text)
    city: Mapped[Optional[str]] = mapped_column(String(255))
    state: Mapped[Optional[str]] = mapped_column(String(255))
    country: Mapped[Optional[str]] = mapped_column(String(255))
    postal_code: Mapped[Optional[str]] = mapped_column(String(20))
    latitude: Mapped[Optional[float]] = mapped_column(Double(53))
    longitude: Mapped[Optional[float]] = mapped_column(Double(53))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    website: Mapped[Optional[str]] = mapped_column(String(255))
    license_number: Mapped[Optional[str]] = mapped_column(String(100))
    operating_hours: Mapped[Optional[dict]] = mapped_column(JSONB)
    services_offered: Mapped[Optional[dict]] = mapped_column(JSONB)
    images: Mapped[Optional[list]] = mapped_column(ARRAY(Text()))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    clinic_admin_profiles: Mapped[List['ClinicAdminProfiles']] = relationship('ClinicAdminProfiles', back_populates='clinic')
    clinic_images: Mapped[List['ClinicImages']] = relationship('ClinicImages', back_populates='clinic')
    clinic_services: Mapped[List['ClinicServices']] = relationship('ClinicServices', back_populates='clinic')
    appointment_slots: Mapped[List['AppointmentSlots']] = relationship('AppointmentSlots', back_populates='clinic')
    appointments: Mapped[List['Appointments']] = relationship('Appointments', back_populates='clinic')
    clinic_doctors: Mapped[List['ClinicDoctors']] = relationship('ClinicDoctors', back_populates='clinic')
    doctor_availability: Mapped[List['DoctorAvailability']] = relationship('DoctorAvailability', back_populates='clinic')
    doctor_schedules: Mapped[List['DoctorSchedules']] = relationship('DoctorSchedules', back_populates='clinic')
    invoices: Mapped[List['Invoices']] = relationship('Invoices', back_populates='clinic')
    medical_visits: Mapped[List['MedicalVisits']] = relationship('MedicalVisits', back_populates='clinic')


class LabPartners(Base):
    __tablename__ = 'lab_partners'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='lab_partners_pkey'),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    name: Mapped[str] = mapped_column(String(255))
    address: Mapped[Optional[str]] = mapped_column(Text)
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    services_offered: Mapped[Optional[dict]] = mapped_column(JSONB)
    rating: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(3, 2))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    lab_tests: Mapped[List['LabTests']] = relationship('LabTests', back_populates='lab_partner')
    lab_bookings: Mapped[List['LabBookings']] = relationship('LabBookings', back_populates='lab_partner')


class Languages(Base):
    __tablename__ = 'languages'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='languages_pkey'),
        UniqueConstraint('code', name='languages_code_key'),
        UniqueConstraint('name', name='languages_name_key')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    name: Mapped[str] = mapped_column(String(100))
    code: Mapped[str] = mapped_column(String(10))

    doctor_languages: Mapped[List['DoctorLanguages']] = relationship('DoctorLanguages', back_populates='language')


class Locales(Base):
    __tablename__ = 'locales'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='locales_pkey'),
        UniqueConstraint('code', name='locales_code_key')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    code: Mapped[str] = mapped_column(String(10))
    name: Mapped[Optional[str]] = mapped_column(String(100))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    date_format: Mapped[Optional[str]] = mapped_column(String(50))
    time_format: Mapped[Optional[str]] = mapped_column(String(50))
    currency_code: Mapped[Optional[str]] = mapped_column(String(10))
    is_rtl: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    user_locale_preferences: Mapped[List['UserLocalePreferences']] = relationship('UserLocalePreferences', back_populates='locale')


class Medicines(Base):
    __tablename__ = 'medicines'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='medicines_pkey'),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    name: Mapped[str] = mapped_column(String(255))
    generic_name: Mapped[Optional[str]] = mapped_column(String(255))
    brand_names: Mapped[Optional[list]] = mapped_column(ARRAY(Text()))
    category: Mapped[Optional[str]] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text)
    price: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    prescription_required: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    stock_status: Mapped[Optional[str]] = mapped_column(String(50))


class NotificationTemplates(Base):
    __tablename__ = 'notification_templates'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='notification_templates_pkey'),
        UniqueConstraint('name', name='notification_templates_name_key')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    name: Mapped[str] = mapped_column(String(100))
    subject: Mapped[Optional[str]] = mapped_column(String(255))
    email_template: Mapped[Optional[str]] = mapped_column(Text)
    sms_template: Mapped[Optional[str]] = mapped_column(Text)
    push_template: Mapped[Optional[str]] = mapped_column(Text)
    variables: Mapped[Optional[dict]] = mapped_column(JSONB)


class PharmacyPartners(Base):
    __tablename__ = 'pharmacy_partners'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pharmacy_partners_pkey'),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    name: Mapped[str] = mapped_column(String(255))
    address: Mapped[Optional[str]] = mapped_column(Text)
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    license_number: Mapped[Optional[str]] = mapped_column(String(100))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    delivery_available: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    pharmacy_orders: Mapped[List['PharmacyOrders']] = relationship('PharmacyOrders', back_populates='pharmacy_partner')


class Roles(Base):
    __tablename__ = 'roles'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='roles_pkey'),
        UniqueConstraint('name', name='roles_name_key')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text)
    permissions: Mapped[Optional[dict]] = mapped_column(JSONB)

    user_roles: Mapped[List['UserRoles']] = relationship('UserRoles', back_populates='role')


class Specialties(Base):
    __tablename__ = 'specialties'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='specialties_pkey'),
        UniqueConstraint('name', name='specialties_name_key')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    category: Mapped[Optional[str]] = mapped_column(String(255))

    doctor_specialties: Mapped[List['DoctorSpecialties']] = relationship('DoctorSpecialties', back_populates='specialty')


class SystemMetrics(Base):
    __tablename__ = 'system_metrics'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='system_metrics_pkey'),
        Index('idx_system_metrics_category', 'category', 'recorded_at')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    metric_name: Mapped[Optional[str]] = mapped_column(String(100))
    value: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(15, 4))
    recorded_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    category: Mapped[Optional[str]] = mapped_column(String(100))


class Translations(Base):
    __tablename__ = 'translations'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='translations_pkey'),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    locale: Mapped[Optional[str]] = mapped_column(String(10))
    translation_key: Mapped[Optional[str]] = mapped_column(String(255))
    translation_value: Mapped[Optional[str]] = mapped_column(Text)
    context: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('email', name='users_email_key'),
        UniqueConstraint('phone', name='users_phone_key'),
        Index('idx_users_email', 'email'),
        Index('idx_users_phone', 'phone')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    email: Mapped[str] = mapped_column(String(255))
    password_hash: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    date_of_birth: Mapped[Optional[datetime.date]] = mapped_column(Date)
    gender: Mapped[Optional[str]] = mapped_column(String(50))
    profile_picture: Mapped[Optional[str]] = mapped_column(Text)
    language_preference: Mapped[Optional[str]] = mapped_column(String(10))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    is_verified: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    admin_logs: Mapped[List['AdminLogs']] = relationship('AdminLogs', back_populates='admin')
    analytics_events: Mapped[List['AnalyticsEvents']] = relationship('AnalyticsEvents', back_populates='user')
    audit_logs: Mapped[List['AuditLogs']] = relationship('AuditLogs', back_populates='user')
    auth_tokens: Mapped[List['AuthTokens']] = relationship('AuthTokens', back_populates='user')
    clinic_admin_profiles: Mapped[Optional['ClinicAdminProfiles']] = relationship('ClinicAdminProfiles', uselist=False, back_populates='user')
    doctor_profiles: Mapped[Optional['DoctorProfiles']] = relationship('DoctorProfiles', uselist=False, back_populates='user')
    email_logs: Mapped[List['EmailLogs']] = relationship('EmailLogs', back_populates='user')
    file_uploads: Mapped[List['FileUploads']] = relationship('FileUploads', back_populates='users')
    health_tips: Mapped[List['HealthTips']] = relationship('HealthTips', back_populates='users')
    notification_preferences: Mapped[List['NotificationPreferences']] = relationship('NotificationPreferences', back_populates='user')
    notifications: Mapped[List['Notifications']] = relationship('Notifications', back_populates='user')
    otp_codes: Mapped[List['OtpCodes']] = relationship('OtpCodes', back_populates='user')
    patient_profiles: Mapped[Optional['PatientProfiles']] = relationship('PatientProfiles', uselist=False, back_populates='user')
    payment_methods: Mapped[List['PaymentMethods']] = relationship('PaymentMethods', back_populates='user')
    security_logs: Mapped[List['SecurityLogs']] = relationship('SecurityLogs', back_populates='user')
    sessions: Mapped[List['Sessions']] = relationship('Sessions', back_populates='user')
    sms_logs: Mapped[List['SmsLogs']] = relationship('SmsLogs', back_populates='user')
    system_announcements: Mapped[List['SystemAnnouncements']] = relationship('SystemAnnouncements', back_populates='users')
    user_devices: Mapped[List['UserDevices']] = relationship('UserDevices', back_populates='user')
    user_locale_preferences: Mapped[List['UserLocalePreferences']] = relationship('UserLocalePreferences', back_populates='user')
    user_roles: Mapped[List['UserRoles']] = relationship('UserRoles', foreign_keys='[UserRoles.assigned_by]', back_populates='users')
    user_roles_: Mapped[List['UserRoles']] = relationship('UserRoles', foreign_keys='[UserRoles.user_id]', back_populates='user')
    wallet_transactions: Mapped[List['WalletTransactions']] = relationship('WalletTransactions', back_populates='user')
    appointment_reschedule_history: Mapped[List['AppointmentRescheduleHistory']] = relationship('AppointmentRescheduleHistory', back_populates='users')
    call_logs: Mapped[List['CallLogs']] = relationship('CallLogs', back_populates='participant')
    chat_messages: Mapped[List['ChatMessages']] = relationship('ChatMessages', back_populates='sender')
    feedback_reports: Mapped[List['FeedbackReports']] = relationship('FeedbackReports', back_populates='users')


class AdminLogs(Base):
    __tablename__ = 'admin_logs'
    __table_args__ = (
        ForeignKeyConstraint(['admin_id'], ['users.id'], ondelete='SET NULL', name='admin_logs_admin_id_fkey'),
        PrimaryKeyConstraint('id', name='admin_logs_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    admin_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    action: Mapped[Optional[str]] = mapped_column(String(100))
    target_type: Mapped[Optional[str]] = mapped_column(String(100))
    target_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    details: Mapped[Optional[dict]] = mapped_column(JSONB)
    ip_address: Mapped[Optional[Any]] = mapped_column(INET)
    timestamp: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    admin: Mapped[Optional['Users']] = relationship('Users', back_populates='admin_logs')


class AnalyticsEvents(Base):
    __tablename__ = 'analytics_events'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL', name='analytics_events_user_id_fkey'),
        PrimaryKeyConstraint('id', name='analytics_events_pkey'),
        Index('idx_analytics_events_user', 'user_id', 'timestamp')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    event_type: Mapped[Optional[str]] = mapped_column(String(100))
    event_data: Mapped[Optional[dict]] = mapped_column(JSONB)
    timestamp: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    session_id: Mapped[Optional[str]] = mapped_column(String(255))

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='analytics_events')


class AuditLogs(Base):
    __tablename__ = 'audit_logs'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL', name='audit_logs_user_id_fkey'),
        PrimaryKeyConstraint('id', name='audit_logs_pkey'),
        Index('idx_audit_logs_user', 'user_id', 'timestamp')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    table_name: Mapped[Optional[str]] = mapped_column(String(100))
    record_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    action: Mapped[Optional[str]] = mapped_column(String(50))
    old_values: Mapped[Optional[dict]] = mapped_column(JSONB)
    new_values: Mapped[Optional[dict]] = mapped_column(JSONB)
    timestamp: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    ip_address: Mapped[Optional[Any]] = mapped_column(INET)

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='audit_logs')


class AuthTokens(Base):
    __tablename__ = 'auth_tokens'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='auth_tokens_user_id_fkey'),
        PrimaryKeyConstraint('id', name='auth_tokens_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    token_hash: Mapped[str] = mapped_column(Text)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    token_type: Mapped[Optional[str]] = mapped_column(String(50))
    expires_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='auth_tokens')


class ClinicAdminProfiles(Base):
    __tablename__ = 'clinic_admin_profiles'
    __table_args__ = (
        ForeignKeyConstraint(['clinic_id'], ['clinics.id'], ondelete='SET NULL', name='clinic_admin_profiles_clinic_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='clinic_admin_profiles_user_id_fkey'),
        PrimaryKeyConstraint('id', name='clinic_admin_profiles_pkey'),
        UniqueConstraint('user_id', name='clinic_admin_profiles_user_id_key')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    clinic_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    admin_level: Mapped[Optional[str]] = mapped_column(String(50))
    permissions: Mapped[Optional[dict]] = mapped_column(JSONB)

    clinic: Mapped[Optional['Clinics']] = relationship('Clinics', back_populates='clinic_admin_profiles')
    user: Mapped[Optional['Users']] = relationship('Users', back_populates='clinic_admin_profiles')


class ClinicImages(Base):
    __tablename__ = 'clinic_images'
    __table_args__ = (
        ForeignKeyConstraint(['clinic_id'], ['clinics.id'], ondelete='CASCADE', name='clinic_images_clinic_id_fkey'),
        PrimaryKeyConstraint('id', name='clinic_images_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    clinic_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    image_url: Mapped[Optional[str]] = mapped_column(Text)
    image_type: Mapped[Optional[str]] = mapped_column(String(100))
    uploaded_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    clinic: Mapped[Optional['Clinics']] = relationship('Clinics', back_populates='clinic_images')


class ClinicServices(Base):
    __tablename__ = 'clinic_services'
    __table_args__ = (
        ForeignKeyConstraint(['clinic_id'], ['clinics.id'], ondelete='CASCADE', name='clinic_services_clinic_id_fkey'),
        PrimaryKeyConstraint('id', name='clinic_services_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    clinic_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    service_name: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    price: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer)

    clinic: Mapped[Optional['Clinics']] = relationship('Clinics', back_populates='clinic_services')


class DoctorProfiles(Base):
    __tablename__ = 'doctor_profiles'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='doctor_profiles_user_id_fkey'),
        PrimaryKeyConstraint('id', name='doctor_profiles_pkey'),
        UniqueConstraint('user_id', name='doctor_profiles_user_id_key')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    medical_license_number: Mapped[Optional[str]] = mapped_column(String(255))
    license_expiry: Mapped[Optional[datetime.date]] = mapped_column(Date)
    years_experience: Mapped[Optional[int]] = mapped_column(Integer)
    bio: Mapped[Optional[str]] = mapped_column(Text)
    consultation_fee: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    telemedicine_enabled: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    is_verified: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    verification_documents: Mapped[Optional[str]] = mapped_column(Text)
    specialization_primary: Mapped[Optional[str]] = mapped_column(String(255))

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='doctor_profiles')
    appointment_slots: Mapped[List['AppointmentSlots']] = relationship('AppointmentSlots', back_populates='doctor')
    appointments: Mapped[List['Appointments']] = relationship('Appointments', back_populates='doctor')
    certifications: Mapped[List['Certifications']] = relationship('Certifications', back_populates='doctor')
    clinic_doctors: Mapped[List['ClinicDoctors']] = relationship('ClinicDoctors', back_populates='doctor')
    doctor_availability: Mapped[List['DoctorAvailability']] = relationship('DoctorAvailability', back_populates='doctor')
    doctor_languages: Mapped[List['DoctorLanguages']] = relationship('DoctorLanguages', back_populates='doctor')
    doctor_ratings: Mapped[List['DoctorRatings']] = relationship('DoctorRatings', back_populates='doctor')
    doctor_schedules: Mapped[List['DoctorSchedules']] = relationship('DoctorSchedules', back_populates='doctor')
    doctor_specialties: Mapped[List['DoctorSpecialties']] = relationship('DoctorSpecialties', back_populates='doctor')
    educations: Mapped[List['Educations']] = relationship('Educations', back_populates='doctor')
    lab_reports: Mapped[List['LabReports']] = relationship('LabReports', back_populates='doctor')
    patient_favorites: Mapped[List['PatientFavorites']] = relationship('PatientFavorites', back_populates='doctor')
    appointment_feedback: Mapped[List['AppointmentFeedback']] = relationship('AppointmentFeedback', back_populates='doctor')
    chat_conversations: Mapped[List['ChatConversations']] = relationship('ChatConversations', back_populates='doctor')
    consultation_notes: Mapped[List['ConsultationNotes']] = relationship('ConsultationNotes', back_populates='doctor')
    invoices: Mapped[List['Invoices']] = relationship('Invoices', back_populates='doctor')
    medical_visits: Mapped[List['MedicalVisits']] = relationship('MedicalVisits', back_populates='doctor')
    medical_documents: Mapped[List['MedicalDocuments']] = relationship('MedicalDocuments', back_populates='doctor')
    prescriptions: Mapped[List['Prescriptions']] = relationship('Prescriptions', back_populates='doctor')


class EmailLogs(Base):
    __tablename__ = 'email_logs'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL', name='email_logs_user_id_fkey'),
        PrimaryKeyConstraint('id', name='email_logs_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    email_address: Mapped[Optional[str]] = mapped_column(String(255))
    subject: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[Optional[str]] = mapped_column(String(50))
    sent_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    opened_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    clicked_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='email_logs')


class FileUploads(Base):
    __tablename__ = 'file_uploads'
    __table_args__ = (
        ForeignKeyConstraint(['uploaded_by'], ['users.id'], ondelete='SET NULL', name='file_uploads_uploaded_by_fkey'),
        PrimaryKeyConstraint('id', name='file_uploads_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    uploaded_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    file_name: Mapped[Optional[str]] = mapped_column(String(255))
    file_path: Mapped[Optional[str]] = mapped_column(Text)
    file_type: Mapped[Optional[str]] = mapped_column(String(100))
    file_size: Mapped[Optional[int]] = mapped_column(BigInteger)
    virus_scan_status: Mapped[Optional[str]] = mapped_column(String(50))
    access_level: Mapped[Optional[str]] = mapped_column(String(50))
    uploaded_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    users: Mapped[Optional['Users']] = relationship('Users', back_populates='file_uploads')


class HealthTips(Base):
    __tablename__ = 'health_tips'
    __table_args__ = (
        ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL', name='health_tips_created_by_fkey'),
        PrimaryKeyConstraint('id', name='health_tips_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    title: Mapped[Optional[str]] = mapped_column(String(255))
    content: Mapped[Optional[str]] = mapped_column(Text)
    category: Mapped[Optional[str]] = mapped_column(String(100))
    target_conditions: Mapped[Optional[list]] = mapped_column(ARRAY(String(length=255)))
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    users: Mapped[Optional['Users']] = relationship('Users', back_populates='health_tips')


class LabTests(Base):
    __tablename__ = 'lab_tests'
    __table_args__ = (
        ForeignKeyConstraint(['lab_partner_id'], ['lab_partners.id'], ondelete='CASCADE', name='lab_tests_lab_partner_id_fkey'),
        PrimaryKeyConstraint('id', name='lab_tests_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    lab_partner_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    test_name: Mapped[Optional[str]] = mapped_column(String(255))
    category: Mapped[Optional[str]] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text)
    price: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    preparation_instructions: Mapped[Optional[str]] = mapped_column(Text)
    sample_type: Mapped[Optional[str]] = mapped_column(String(100))
    turnaround_time: Mapped[Optional[str]] = mapped_column(String(100))

    lab_partner: Mapped[Optional['LabPartners']] = relationship('LabPartners', back_populates='lab_tests')
    lab_results: Mapped[List['LabResults']] = relationship('LabResults', back_populates='test')


class NotificationPreferences(Base):
    __tablename__ = 'notification_preferences'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='notification_preferences_user_id_fkey'),
        PrimaryKeyConstraint('id', name='notification_preferences_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    notification_type: Mapped[Optional[str]] = mapped_column(String(100))
    email_enabled: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    sms_enabled: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    push_enabled: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    frequency: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("'immediate'::character varying"))

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='notification_preferences')


class Notifications(Base):
    __tablename__ = 'notifications'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='notifications_user_id_fkey'),
        PrimaryKeyConstraint('id', name='notifications_pkey'),
        Index('idx_notifications_user_unread', 'user_id', 'read_at')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    title: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    message: Mapped[Optional[str]] = mapped_column(Text)
    type: Mapped[Optional[str]] = mapped_column(String(100))
    channel: Mapped[Optional[str]] = mapped_column(String(50))
    status: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("'pending'::character varying"))
    scheduled_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    sent_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    read_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    data: Mapped[Optional[dict]] = mapped_column(JSONB)

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='notifications')
    notification_logs: Mapped[List['NotificationLogs']] = relationship('NotificationLogs', back_populates='notification')


class OtpCodes(Base):
    __tablename__ = 'otp_codes'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='otp_codes_user_id_fkey'),
        PrimaryKeyConstraint('id', name='otp_codes_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    code_hash: Mapped[str] = mapped_column(Text)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    contact_method: Mapped[Optional[str]] = mapped_column(String(50))
    purpose: Mapped[Optional[str]] = mapped_column(String(100))
    expires_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    attempts: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))
    is_used: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='otp_codes')


class PatientProfiles(Base):
    __tablename__ = 'patient_profiles'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='patient_profiles_user_id_fkey'),
        PrimaryKeyConstraint('id', name='patient_profiles_pkey'),
        UniqueConstraint('user_id', name='patient_profiles_user_id_key')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    emergency_contact_name: Mapped[Optional[str]] = mapped_column(String(255))
    emergency_contact_phone: Mapped[Optional[str]] = mapped_column(String(20))
    blood_group: Mapped[Optional[str]] = mapped_column(String(10))
    allergies: Mapped[Optional[str]] = mapped_column(Text)
    chronic_conditions: Mapped[Optional[str]] = mapped_column(Text)
    insurance_provider: Mapped[Optional[str]] = mapped_column(String(255))
    insurance_policy_number: Mapped[Optional[str]] = mapped_column(String(255))
    preferred_language: Mapped[Optional[str]] = mapped_column(String(10))

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='patient_profiles')
    ai_chat_sessions: Mapped[List['AiChatSessions']] = relationship('AiChatSessions', back_populates='patient')
    allergies_: Mapped[List['Allergies']] = relationship('Allergies', back_populates='patient')
    appointments: Mapped[List['Appointments']] = relationship('Appointments', back_populates='patient')
    emergency_contacts: Mapped[List['EmergencyContacts']] = relationship('EmergencyContacts', back_populates='patient')
    lab_bookings: Mapped[List['LabBookings']] = relationship('LabBookings', back_populates='patient')
    lab_reports: Mapped[List['LabReports']] = relationship('LabReports', back_populates='patient')
    medical_history: Mapped[List['MedicalHistory']] = relationship('MedicalHistory', back_populates='patient')
    medicine_reminders: Mapped[List['MedicineReminders']] = relationship('MedicineReminders', back_populates='patient')
    patient_favorites: Mapped[List['PatientFavorites']] = relationship('PatientFavorites', back_populates='patient')
    patient_vitals_tracking: Mapped[List['PatientVitalsTracking']] = relationship('PatientVitalsTracking', back_populates='patient')
    symptom_reports: Mapped[List['SymptomReports']] = relationship('SymptomReports', back_populates='patient')
    appointment_feedback: Mapped[List['AppointmentFeedback']] = relationship('AppointmentFeedback', back_populates='patient')
    chat_conversations: Mapped[List['ChatConversations']] = relationship('ChatConversations', back_populates='patient')
    insurance_claims: Mapped[List['InsuranceClaims']] = relationship('InsuranceClaims', back_populates='patient')
    invoices: Mapped[List['Invoices']] = relationship('Invoices', back_populates='patient')
    lab_results: Mapped[List['LabResults']] = relationship('LabResults', back_populates='patient')
    medical_visits: Mapped[List['MedicalVisits']] = relationship('MedicalVisits', back_populates='patient')
    payments: Mapped[List['Payments']] = relationship('Payments', back_populates='patient')
    medical_documents: Mapped[List['MedicalDocuments']] = relationship('MedicalDocuments', back_populates='patient')
    prescriptions: Mapped[List['Prescriptions']] = relationship('Prescriptions', back_populates='patient')
    vital_signs: Mapped[List['VitalSigns']] = relationship('VitalSigns', back_populates='patient')
    pharmacy_orders: Mapped[List['PharmacyOrders']] = relationship('PharmacyOrders', back_populates='patient')


class PaymentMethods(Base):
    __tablename__ = 'payment_methods'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='payment_methods_user_id_fkey'),
        PrimaryKeyConstraint('id', name='payment_methods_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    method_type: Mapped[Optional[str]] = mapped_column(String(100))
    provider: Mapped[Optional[str]] = mapped_column(String(100))
    token: Mapped[Optional[str]] = mapped_column(Text)
    is_default: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='payment_methods')


class SecurityLogs(Base):
    __tablename__ = 'security_logs'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL', name='security_logs_user_id_fkey'),
        PrimaryKeyConstraint('id', name='security_logs_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    event_type: Mapped[Optional[str]] = mapped_column(String(100))
    details: Mapped[Optional[str]] = mapped_column(Text)
    risk_level: Mapped[Optional[str]] = mapped_column(String(50))
    ip_address: Mapped[Optional[Any]] = mapped_column(INET)
    user_agent: Mapped[Optional[str]] = mapped_column(Text)
    timestamp: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='security_logs')


class Sessions(Base):
    __tablename__ = 'sessions'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='sessions_user_id_fkey'),
        PrimaryKeyConstraint('id', name='sessions_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    session_token: Mapped[str] = mapped_column(Text)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    device_info: Mapped[Optional[str]] = mapped_column(Text)
    ip_address: Mapped[Optional[Any]] = mapped_column(INET)
    last_activity: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    expires_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='sessions')


class SmsLogs(Base):
    __tablename__ = 'sms_logs'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL', name='sms_logs_user_id_fkey'),
        PrimaryKeyConstraint('id', name='sms_logs_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20))
    message: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[Optional[str]] = mapped_column(String(50))
    sent_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    delivery_status: Mapped[Optional[str]] = mapped_column(String(50))
    provider_response: Mapped[Optional[str]] = mapped_column(Text)

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='sms_logs')


class SystemAnnouncements(Base):
    __tablename__ = 'system_announcements'
    __table_args__ = (
        ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL', name='system_announcements_created_by_fkey'),
        PrimaryKeyConstraint('id', name='system_announcements_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    title: Mapped[Optional[str]] = mapped_column(String(255))
    message: Mapped[Optional[str]] = mapped_column(Text)
    type: Mapped[Optional[str]] = mapped_column(String(100))
    target_roles: Mapped[Optional[list]] = mapped_column(ARRAY(String(length=100)))
    start_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    end_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)

    users: Mapped[Optional['Users']] = relationship('Users', back_populates='system_announcements')


class UserDevices(Base):
    __tablename__ = 'user_devices'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='user_devices_user_id_fkey'),
        PrimaryKeyConstraint('id', name='user_devices_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    device_id: Mapped[Optional[str]] = mapped_column(String(255))
    device_type: Mapped[Optional[str]] = mapped_column(String(100))
    push_token: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    last_seen: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='user_devices')


class UserLocalePreferences(Base):
    __tablename__ = 'user_locale_preferences'
    __table_args__ = (
        ForeignKeyConstraint(['locale_id'], ['locales.id'], ondelete='CASCADE', name='user_locale_preferences_locale_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='user_locale_preferences_user_id_fkey'),
        PrimaryKeyConstraint('user_id', 'locale_id', name='user_locale_preferences_pkey')
    )

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    locale_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    date_format: Mapped[Optional[str]] = mapped_column(String(50))
    time_format: Mapped[Optional[str]] = mapped_column(String(50))
    currency_display: Mapped[Optional[str]] = mapped_column(String(50))

    locale: Mapped['Locales'] = relationship('Locales', back_populates='user_locale_preferences')
    user: Mapped['Users'] = relationship('Users', back_populates='user_locale_preferences')


class UserRoles(Base):
    __tablename__ = 'user_roles'
    __table_args__ = (
        ForeignKeyConstraint(['assigned_by'], ['users.id'], ondelete='SET NULL', name='user_roles_assigned_by_fkey'),
        ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE', name='user_roles_role_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='user_roles_user_id_fkey'),
        PrimaryKeyConstraint('user_id', 'role_id', name='user_roles_pkey')
    )

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    role_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    assigned_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    assigned_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)

    users: Mapped[Optional['Users']] = relationship('Users', foreign_keys=[assigned_by], back_populates='user_roles')
    role: Mapped['Roles'] = relationship('Roles', back_populates='user_roles')
    user: Mapped['Users'] = relationship('Users', foreign_keys=[user_id], back_populates='user_roles_')


class WalletTransactions(Base):
    __tablename__ = 'wallet_transactions'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='wallet_transactions_user_id_fkey'),
        PrimaryKeyConstraint('id', name='wallet_transactions_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    transaction_type: Mapped[Optional[str]] = mapped_column(String(50))
    amount: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(12, 2))
    balance_before: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(12, 2))
    balance_after: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(12, 2))
    reference_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='wallet_transactions')


class AiChatSessions(Base):
    __tablename__ = 'ai_chat_sessions'
    __table_args__ = (
        ForeignKeyConstraint(['patient_id'], ['patient_profiles.user_id'], ondelete='CASCADE', name='ai_chat_sessions_patient_id_fkey'),
        PrimaryKeyConstraint('id', name='ai_chat_sessions_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    patient_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    session_start: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    session_end: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    symptom_analysis: Mapped[Optional[dict]] = mapped_column(JSONB)
    recommendations: Mapped[Optional[dict]] = mapped_column(JSONB)
    triage_level: Mapped[Optional[str]] = mapped_column(String(50))

    patient: Mapped[Optional['PatientProfiles']] = relationship('PatientProfiles', back_populates='ai_chat_sessions')
    ai_recommendations: Mapped[List['AiRecommendations']] = relationship('AiRecommendations', back_populates='session')


class Allergies(Base):
    __tablename__ = 'allergies'
    __table_args__ = (
        ForeignKeyConstraint(['patient_id'], ['patient_profiles.user_id'], ondelete='CASCADE', name='allergies_patient_id_fkey'),
        PrimaryKeyConstraint('id', name='allergies_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    patient_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    allergen: Mapped[Optional[str]] = mapped_column(String(255))
    reaction: Mapped[Optional[str]] = mapped_column(Text)
    severity: Mapped[Optional[str]] = mapped_column(String(100))
    recorded_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    notes: Mapped[Optional[str]] = mapped_column(Text)

    patient: Mapped[Optional['PatientProfiles']] = relationship('PatientProfiles', back_populates='allergies_')


class AppointmentSlots(Base):
    __tablename__ = 'appointment_slots'
    __table_args__ = (
        ForeignKeyConstraint(['clinic_id'], ['clinics.id'], ondelete='SET NULL', name='appointment_slots_clinic_id_fkey'),
        ForeignKeyConstraint(['doctor_id'], ['doctor_profiles.user_id'], ondelete='CASCADE', name='appointment_slots_doctor_id_fkey'),
        PrimaryKeyConstraint('id', name='appointment_slots_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    doctor_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    clinic_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    slot_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    start_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    end_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    is_available: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    is_blocked: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    blocked_reason: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    clinic: Mapped[Optional['Clinics']] = relationship('Clinics', back_populates='appointment_slots')
    doctor: Mapped[Optional['DoctorProfiles']] = relationship('DoctorProfiles', back_populates='appointment_slots')


class Appointments(Base):
    __tablename__ = 'appointments'
    __table_args__ = (
        ForeignKeyConstraint(['clinic_id'], ['clinics.id'], ondelete='SET NULL', name='appointments_clinic_id_fkey'),
        ForeignKeyConstraint(['doctor_id'], ['doctor_profiles.user_id'], ondelete='CASCADE', name='appointments_doctor_id_fkey'),
        ForeignKeyConstraint(['patient_id'], ['patient_profiles.user_id'], ondelete='CASCADE', name='appointments_patient_id_fkey'),
        PrimaryKeyConstraint('id', name='appointments_pkey'),
        Index('idx_appointments_doctor_date', 'doctor_id', 'appointment_date'),
        Index('idx_appointments_patient_date', 'patient_id', 'appointment_date')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    appointment_date: Mapped[datetime.date] = mapped_column(Date)
    patient_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    doctor_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    clinic_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    start_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    end_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    consultation_type: Mapped[Optional[str]] = mapped_column(String(100))
    consultation_mode: Mapped[Optional[str]] = mapped_column(String(100))
    status: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("'scheduled'::character varying"))
    reason_for_visit: Mapped[Optional[str]] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    clinic: Mapped[Optional['Clinics']] = relationship('Clinics', back_populates='appointments')
    doctor: Mapped[Optional['DoctorProfiles']] = relationship('DoctorProfiles', back_populates='appointments')
    patient: Mapped[Optional['PatientProfiles']] = relationship('PatientProfiles', back_populates='appointments')
    appointment_feedback: Mapped[List['AppointmentFeedback']] = relationship('AppointmentFeedback', back_populates='appointment')
    appointment_reminders: Mapped[List['AppointmentReminders']] = relationship('AppointmentReminders', back_populates='appointment')
    appointment_reschedule_history: Mapped[List['AppointmentRescheduleHistory']] = relationship('AppointmentRescheduleHistory', back_populates='appointment')
    chat_conversations: Mapped[List['ChatConversations']] = relationship('ChatConversations', back_populates='appointment')
    consultation_notes: Mapped[List['ConsultationNotes']] = relationship('ConsultationNotes', back_populates='appointment')
    insurance_claims: Mapped[List['InsuranceClaims']] = relationship('InsuranceClaims', back_populates='appointment')
    invoices: Mapped[List['Invoices']] = relationship('Invoices', back_populates='appointment')
    medical_visits: Mapped[List['MedicalVisits']] = relationship('MedicalVisits', back_populates='appointment')
    payments: Mapped[List['Payments']] = relationship('Payments', back_populates='appointment')
    telemedicine_sessions: Mapped[List['TelemedicineSessions']] = relationship('TelemedicineSessions', back_populates='appointment')


class Certifications(Base):
    __tablename__ = 'certifications'
    __table_args__ = (
        ForeignKeyConstraint(['doctor_id'], ['doctor_profiles.user_id'], ondelete='CASCADE', name='certifications_doctor_id_fkey'),
        PrimaryKeyConstraint('id', name='certifications_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    doctor_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    certificate_name: Mapped[Optional[str]] = mapped_column(String(255))
    issuing_body: Mapped[Optional[str]] = mapped_column(String(255))
    issue_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    expiry_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    certificate_url: Mapped[Optional[str]] = mapped_column(Text)

    doctor: Mapped[Optional['DoctorProfiles']] = relationship('DoctorProfiles', back_populates='certifications')


class ClinicDoctors(Base):
    __tablename__ = 'clinic_doctors'
    __table_args__ = (
        ForeignKeyConstraint(['clinic_id'], ['clinics.id'], ondelete='CASCADE', name='clinic_doctors_clinic_id_fkey'),
        ForeignKeyConstraint(['doctor_id'], ['doctor_profiles.user_id'], ondelete='CASCADE', name='clinic_doctors_doctor_id_fkey'),
        PrimaryKeyConstraint('id', name='clinic_doctors_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    clinic_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    doctor_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    joined_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    status: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("'active'::character varying"))
    consultation_fee_override: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))

    clinic: Mapped[Optional['Clinics']] = relationship('Clinics', back_populates='clinic_doctors')
    doctor: Mapped[Optional['DoctorProfiles']] = relationship('DoctorProfiles', back_populates='clinic_doctors')


class DoctorAvailability(Base):
    __tablename__ = 'doctor_availability'
    __table_args__ = (
        CheckConstraint('day_of_week >= 0 AND day_of_week <= 6', name='doctor_availability_day_of_week_check'),
        ForeignKeyConstraint(['clinic_id'], ['clinics.id'], ondelete='SET NULL', name='doctor_availability_clinic_id_fkey'),
        ForeignKeyConstraint(['doctor_id'], ['doctor_profiles.user_id'], ondelete='CASCADE', name='doctor_availability_doctor_id_fkey'),
        PrimaryKeyConstraint('id', name='doctor_availability_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    doctor_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    clinic_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    day_of_week: Mapped[Optional[int]] = mapped_column(Integer)
    start_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    end_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    slot_duration: Mapped[Optional[int]] = mapped_column(Integer)
    max_patients_per_slot: Mapped[Optional[int]] = mapped_column(Integer)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    clinic: Mapped[Optional['Clinics']] = relationship('Clinics', back_populates='doctor_availability')
    doctor: Mapped[Optional['DoctorProfiles']] = relationship('DoctorProfiles', back_populates='doctor_availability')


class DoctorLanguages(Base):
    __tablename__ = 'doctor_languages'
    __table_args__ = (
        ForeignKeyConstraint(['doctor_id'], ['doctor_profiles.user_id'], ondelete='CASCADE', name='doctor_languages_doctor_id_fkey'),
        ForeignKeyConstraint(['language_id'], ['languages.id'], ondelete='CASCADE', name='doctor_languages_language_id_fkey'),
        PrimaryKeyConstraint('doctor_id', 'language_id', name='doctor_languages_pkey')
    )

    doctor_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    language_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    proficiency_level: Mapped[Optional[str]] = mapped_column(String(50))

    doctor: Mapped['DoctorProfiles'] = relationship('DoctorProfiles', back_populates='doctor_languages')
    language: Mapped['Languages'] = relationship('Languages', back_populates='doctor_languages')


class DoctorRatings(Base):
    __tablename__ = 'doctor_ratings'
    __table_args__ = (
        ForeignKeyConstraint(['doctor_id'], ['doctor_profiles.user_id'], ondelete='CASCADE', name='doctor_ratings_doctor_id_fkey'),
        PrimaryKeyConstraint('id', name='doctor_ratings_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    doctor_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    average_rating: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(3, 2))
    total_reviews: Mapped[Optional[int]] = mapped_column(Integer)
    communication_avg: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(3, 2))
    punctuality_avg: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(3, 2))
    expertise_avg: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(3, 2))
    last_updated: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    doctor: Mapped[Optional['DoctorProfiles']] = relationship('DoctorProfiles', back_populates='doctor_ratings')


class DoctorSchedules(Base):
    __tablename__ = 'doctor_schedules'
    __table_args__ = (
        ForeignKeyConstraint(['clinic_id'], ['clinics.id'], ondelete='CASCADE', name='doctor_schedules_clinic_id_fkey'),
        ForeignKeyConstraint(['doctor_id'], ['doctor_profiles.user_id'], ondelete='CASCADE', name='doctor_schedules_doctor_id_fkey'),
        PrimaryKeyConstraint('id', name='doctor_schedules_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    doctor_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    clinic_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    schedule_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    start_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    end_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    break_start: Mapped[Optional[datetime.time]] = mapped_column(Time)
    break_end: Mapped[Optional[datetime.time]] = mapped_column(Time)
    is_available: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    notes: Mapped[Optional[str]] = mapped_column(Text)

    clinic: Mapped[Optional['Clinics']] = relationship('Clinics', back_populates='doctor_schedules')
    doctor: Mapped[Optional['DoctorProfiles']] = relationship('DoctorProfiles', back_populates='doctor_schedules')


class DoctorSpecialties(Base):
    __tablename__ = 'doctor_specialties'
    __table_args__ = (
        ForeignKeyConstraint(['doctor_id'], ['doctor_profiles.user_id'], ondelete='CASCADE', name='doctor_specialties_doctor_id_fkey'),
        ForeignKeyConstraint(['specialty_id'], ['specialties.id'], ondelete='CASCADE', name='doctor_specialties_specialty_id_fkey'),
        PrimaryKeyConstraint('doctor_id', 'specialty_id', name='doctor_specialties_pkey'),
        Index('idx_doctors_specialty', 'specialty_id')
    )

    doctor_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    specialty_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    is_primary: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    certification_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    doctor: Mapped['DoctorProfiles'] = relationship('DoctorProfiles', back_populates='doctor_specialties')
    specialty: Mapped['Specialties'] = relationship('Specialties', back_populates='doctor_specialties')


class Educations(Base):
    __tablename__ = 'educations'
    __table_args__ = (
        ForeignKeyConstraint(['doctor_id'], ['doctor_profiles.user_id'], ondelete='CASCADE', name='educations_doctor_id_fkey'),
        PrimaryKeyConstraint('id', name='educations_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    doctor_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    degree: Mapped[Optional[str]] = mapped_column(String(255))
    institution: Mapped[Optional[str]] = mapped_column(String(255))
    year_completed: Mapped[Optional[int]] = mapped_column(Integer)
    is_verified: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    doctor: Mapped[Optional['DoctorProfiles']] = relationship('DoctorProfiles', back_populates='educations')


class EmergencyContacts(Base):
    __tablename__ = 'emergency_contacts'
    __table_args__ = (
        ForeignKeyConstraint(['patient_id'], ['patient_profiles.user_id'], ondelete='CASCADE', name='emergency_contacts_patient_id_fkey'),
        PrimaryKeyConstraint('id', name='emergency_contacts_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    patient_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    contact_name: Mapped[Optional[str]] = mapped_column(String(255))
    relationship_: Mapped[Optional[str]] = mapped_column('relationship', String(100))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    is_primary: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    patient: Mapped[Optional['PatientProfiles']] = relationship('PatientProfiles', back_populates='emergency_contacts')


class LabBookings(Base):
    __tablename__ = 'lab_bookings'
    __table_args__ = (
        ForeignKeyConstraint(['lab_partner_id'], ['lab_partners.id'], ondelete='CASCADE', name='lab_bookings_lab_partner_id_fkey'),
        ForeignKeyConstraint(['patient_id'], ['patient_profiles.user_id'], ondelete='CASCADE', name='lab_bookings_patient_id_fkey'),
        PrimaryKeyConstraint('id', name='lab_bookings_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    patient_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    lab_partner_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    test_ids: Mapped[Optional[list]] = mapped_column(ARRAY(Uuid()))
    booking_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    appointment_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    home_collection: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    status: Mapped[Optional[str]] = mapped_column(String(50))
    total_amount: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))

    lab_partner: Mapped[Optional['LabPartners']] = relationship('LabPartners', back_populates='lab_bookings')
    patient: Mapped[Optional['PatientProfiles']] = relationship('PatientProfiles', back_populates='lab_bookings')
    lab_results: Mapped[List['LabResults']] = relationship('LabResults', back_populates='booking')


class LabReports(Base):
    __tablename__ = 'lab_reports'
    __table_args__ = (
        ForeignKeyConstraint(['doctor_id'], ['doctor_profiles.user_id'], ondelete='SET NULL', name='lab_reports_doctor_id_fkey'),
        ForeignKeyConstraint(['patient_id'], ['patient_profiles.user_id'], ondelete='CASCADE', name='lab_reports_patient_id_fkey'),
        PrimaryKeyConstraint('id', name='lab_reports_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    patient_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    doctor_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    test_name: Mapped[Optional[str]] = mapped_column(String(255))
    test_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    results: Mapped[Optional[str]] = mapped_column(Text)
    reference_values: Mapped[Optional[str]] = mapped_column(Text)
    lab_name: Mapped[Optional[str]] = mapped_column(String(255))
    report_file: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[Optional[str]] = mapped_column(String(50))

    doctor: Mapped[Optional['DoctorProfiles']] = relationship('DoctorProfiles', back_populates='lab_reports')
    patient: Mapped[Optional['PatientProfiles']] = relationship('PatientProfiles', back_populates='lab_reports')


class MedicalHistory(Base):
    __tablename__ = 'medical_history'
    __table_args__ = (
        ForeignKeyConstraint(['patient_id'], ['patient_profiles.user_id'], ondelete='CASCADE', name='medical_history_patient_id_fkey'),
        PrimaryKeyConstraint('id', name='medical_history_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    patient_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    condition: Mapped[Optional[str]] = mapped_column(String(255))
    diagnosed_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    status: Mapped[Optional[str]] = mapped_column(String(100))
    treatment: Mapped[Optional[str]] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text)

    patient: Mapped[Optional['PatientProfiles']] = relationship('PatientProfiles', back_populates='medical_history')


class MedicineReminders(Base):
    __tablename__ = 'medicine_reminders'
    __table_args__ = (
        ForeignKeyConstraint(['patient_id'], ['patient_profiles.user_id'], ondelete='CASCADE', name='medicine_reminders_patient_id_fkey'),
        PrimaryKeyConstraint('id', name='medicine_reminders_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    patient_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    medicine_name: Mapped[Optional[str]] = mapped_column(String(255))
    dosage: Mapped[Optional[str]] = mapped_column(String(100))
    frequency: Mapped[Optional[str]] = mapped_column(String(100))
    reminder_times: Mapped[Optional[list]] = mapped_column(ARRAY(Time()))
    start_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    end_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    patient: Mapped[Optional['PatientProfiles']] = relationship('PatientProfiles', back_populates='medicine_reminders')


class NotificationLogs(Base):
    __tablename__ = 'notification_logs'
    __table_args__ = (
        ForeignKeyConstraint(['notification_id'], ['notifications.id'], ondelete='CASCADE', name='notification_logs_notification_id_fkey'),
        PrimaryKeyConstraint('id', name='notification_logs_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    notification_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    channel: Mapped[Optional[str]] = mapped_column(String(50))
    status: Mapped[Optional[str]] = mapped_column(String(50))
    delivery_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    retry_count: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))

    notification: Mapped[Optional['Notifications']] = relationship('Notifications', back_populates='notification_logs')


class PatientFavorites(Base):
    __tablename__ = 'patient_favorites'
    __table_args__ = (
        ForeignKeyConstraint(['doctor_id'], ['doctor_profiles.user_id'], ondelete='CASCADE', name='patient_favorites_doctor_id_fkey'),
        ForeignKeyConstraint(['patient_id'], ['patient_profiles.user_id'], ondelete='CASCADE', name='patient_favorites_patient_id_fkey'),
        PrimaryKeyConstraint('id', name='patient_favorites_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    patient_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    doctor_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    added_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    doctor: Mapped[Optional['DoctorProfiles']] = relationship('DoctorProfiles', back_populates='patient_favorites')
    patient: Mapped[Optional['PatientProfiles']] = relationship('PatientProfiles', back_populates='patient_favorites')


class PatientVitalsTracking(Base):
    __tablename__ = 'patient_vitals_tracking'
    __table_args__ = (
        ForeignKeyConstraint(['patient_id'], ['patient_profiles.user_id'], ondelete='CASCADE', name='patient_vitals_tracking_patient_id_fkey'),
        PrimaryKeyConstraint('id', name='patient_vitals_tracking_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    patient_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    recorded_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    weight: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(6, 2))
    height: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(6, 2))
    blood_pressure_systolic: Mapped[Optional[int]] = mapped_column(Integer)
    blood_pressure_diastolic: Mapped[Optional[int]] = mapped_column(Integer)
    heart_rate: Mapped[Optional[int]] = mapped_column(Integer)
    temperature: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))
    blood_sugar: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(6, 2))
    notes: Mapped[Optional[str]] = mapped_column(Text)

    patient: Mapped[Optional['PatientProfiles']] = relationship('PatientProfiles', back_populates='patient_vitals_tracking')


class SymptomReports(Base):
    __tablename__ = 'symptom_reports'
    __table_args__ = (
        CheckConstraint('severity >= 1 AND severity <= 10', name='symptom_reports_severity_check'),
        ForeignKeyConstraint(['patient_id'], ['patient_profiles.user_id'], ondelete='CASCADE', name='symptom_reports_patient_id_fkey'),
        PrimaryKeyConstraint('id', name='symptom_reports_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    patient_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    symptoms: Mapped[Optional[dict]] = mapped_column(JSONB)
    severity: Mapped[Optional[int]] = mapped_column(Integer)
    duration: Mapped[Optional[str]] = mapped_column(String(100))
    body_parts: Mapped[Optional[list]] = mapped_column(ARRAY(String(length=255)))
    additional_info: Mapped[Optional[str]] = mapped_column(Text)
    ai_assessment: Mapped[Optional[dict]] = mapped_column(JSONB)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    patient: Mapped[Optional['PatientProfiles']] = relationship('PatientProfiles', back_populates='symptom_reports')


class AiRecommendations(Base):
    __tablename__ = 'ai_recommendations'
    __table_args__ = (
        ForeignKeyConstraint(['session_id'], ['ai_chat_sessions.id'], ondelete='CASCADE', name='ai_recommendations_session_id_fkey'),
        PrimaryKeyConstraint('id', name='ai_recommendations_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    session_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    recommendation_type: Mapped[Optional[str]] = mapped_column(String(100))
    specialist_suggested: Mapped[Optional[str]] = mapped_column(String(255))
    urgency_level: Mapped[Optional[str]] = mapped_column(String(50))
    confidence_score: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 4))

    session: Mapped[Optional['AiChatSessions']] = relationship('AiChatSessions', back_populates='ai_recommendations')


class AppointmentFeedback(Base):
    __tablename__ = 'appointment_feedback'
    __table_args__ = (
        CheckConstraint('communication_rating >= 1 AND communication_rating <= 5', name='appointment_feedback_communication_rating_check'),
        CheckConstraint('expertise_rating >= 1 AND expertise_rating <= 5', name='appointment_feedback_expertise_rating_check'),
        CheckConstraint('overall_rating >= 1 AND overall_rating <= 5', name='appointment_feedback_overall_rating_check'),
        CheckConstraint('punctuality_rating >= 1 AND punctuality_rating <= 5', name='appointment_feedback_punctuality_rating_check'),
        ForeignKeyConstraint(['appointment_id'], ['appointments.id'], ondelete='CASCADE', name='appointment_feedback_appointment_id_fkey'),
        ForeignKeyConstraint(['doctor_id'], ['doctor_profiles.user_id'], ondelete='CASCADE', name='appointment_feedback_doctor_id_fkey'),
        ForeignKeyConstraint(['patient_id'], ['patient_profiles.user_id'], ondelete='CASCADE', name='appointment_feedback_patient_id_fkey'),
        PrimaryKeyConstraint('id', name='appointment_feedback_pkey'),
        Index('idx_feedback_doctor', 'doctor_id', 'submitted_at')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    appointment_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    patient_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    doctor_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    overall_rating: Mapped[Optional[int]] = mapped_column(Integer)
    communication_rating: Mapped[Optional[int]] = mapped_column(Integer)
    punctuality_rating: Mapped[Optional[int]] = mapped_column(Integer)
    expertise_rating: Mapped[Optional[int]] = mapped_column(Integer)
    comments: Mapped[Optional[str]] = mapped_column(Text)
    is_anonymous: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    submitted_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    appointment: Mapped[Optional['Appointments']] = relationship('Appointments', back_populates='appointment_feedback')
    doctor: Mapped[Optional['DoctorProfiles']] = relationship('DoctorProfiles', back_populates='appointment_feedback')
    patient: Mapped[Optional['PatientProfiles']] = relationship('PatientProfiles', back_populates='appointment_feedback')
    feedback_reports: Mapped[List['FeedbackReports']] = relationship('FeedbackReports', back_populates='feedback')


class AppointmentReminders(Base):
    __tablename__ = 'appointment_reminders'
    __table_args__ = (
        ForeignKeyConstraint(['appointment_id'], ['appointments.id'], ondelete='CASCADE', name='appointment_reminders_appointment_id_fkey'),
        PrimaryKeyConstraint('id', name='appointment_reminders_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    appointment_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    reminder_type: Mapped[Optional[str]] = mapped_column(String(50))
    send_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    status: Mapped[Optional[str]] = mapped_column(String(50))
    sent_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    appointment: Mapped[Optional['Appointments']] = relationship('Appointments', back_populates='appointment_reminders')


class AppointmentRescheduleHistory(Base):
    __tablename__ = 'appointment_reschedule_history'
    __table_args__ = (
        ForeignKeyConstraint(['appointment_id'], ['appointments.id'], ondelete='CASCADE', name='appointment_reschedule_history_appointment_id_fkey'),
        ForeignKeyConstraint(['rescheduled_by'], ['users.id'], name='appointment_reschedule_history_rescheduled_by_fkey'),
        PrimaryKeyConstraint('id', name='appointment_reschedule_history_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    appointment_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    old_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    old_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    new_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    new_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    reason: Mapped[Optional[str]] = mapped_column(Text)
    rescheduled_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    rescheduled_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    appointment: Mapped[Optional['Appointments']] = relationship('Appointments', back_populates='appointment_reschedule_history')
    users: Mapped[Optional['Users']] = relationship('Users', back_populates='appointment_reschedule_history')


class ChatConversations(Base):
    __tablename__ = 'chat_conversations'
    __table_args__ = (
        ForeignKeyConstraint(['appointment_id'], ['appointments.id'], ondelete='CASCADE', name='chat_conversations_appointment_id_fkey'),
        ForeignKeyConstraint(['doctor_id'], ['doctor_profiles.user_id'], ondelete='CASCADE', name='chat_conversations_doctor_id_fkey'),
        ForeignKeyConstraint(['patient_id'], ['patient_profiles.user_id'], ondelete='CASCADE', name='chat_conversations_patient_id_fkey'),
        PrimaryKeyConstraint('id', name='chat_conversations_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    patient_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    doctor_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    appointment_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    started_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    last_message_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    status: Mapped[Optional[str]] = mapped_column(String(50))

    appointment: Mapped[Optional['Appointments']] = relationship('Appointments', back_populates='chat_conversations')
    doctor: Mapped[Optional['DoctorProfiles']] = relationship('DoctorProfiles', back_populates='chat_conversations')
    patient: Mapped[Optional['PatientProfiles']] = relationship('PatientProfiles', back_populates='chat_conversations')
    chat_messages: Mapped[List['ChatMessages']] = relationship('ChatMessages', back_populates='conversation')


class ConsultationNotes(Base):
    __tablename__ = 'consultation_notes'
    __table_args__ = (
        ForeignKeyConstraint(['appointment_id'], ['appointments.id'], ondelete='CASCADE', name='consultation_notes_appointment_id_fkey'),
        ForeignKeyConstraint(['doctor_id'], ['doctor_profiles.user_id'], ondelete='CASCADE', name='consultation_notes_doctor_id_fkey'),
        PrimaryKeyConstraint('id', name='consultation_notes_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    appointment_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    doctor_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    diagnosis: Mapped[Optional[str]] = mapped_column(Text)
    treatment_plan: Mapped[Optional[str]] = mapped_column(Text)
    follow_up_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    appointment: Mapped[Optional['Appointments']] = relationship('Appointments', back_populates='consultation_notes')
    doctor: Mapped[Optional['DoctorProfiles']] = relationship('DoctorProfiles', back_populates='consultation_notes')


class InsuranceClaims(Base):
    __tablename__ = 'insurance_claims'
    __table_args__ = (
        ForeignKeyConstraint(['appointment_id'], ['appointments.id'], ondelete='SET NULL', name='insurance_claims_appointment_id_fkey'),
        ForeignKeyConstraint(['patient_id'], ['patient_profiles.user_id'], ondelete='SET NULL', name='insurance_claims_patient_id_fkey'),
        PrimaryKeyConstraint('id', name='insurance_claims_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    patient_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    appointment_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    insurance_provider: Mapped[Optional[str]] = mapped_column(String(255))
    policy_number: Mapped[Optional[str]] = mapped_column(String(255))
    claim_amount: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(12, 2))
    claim_status: Mapped[Optional[str]] = mapped_column(String(50))
    submitted_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    processed_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    appointment: Mapped[Optional['Appointments']] = relationship('Appointments', back_populates='insurance_claims')
    patient: Mapped[Optional['PatientProfiles']] = relationship('PatientProfiles', back_populates='insurance_claims')


class Invoices(Base):
    __tablename__ = 'invoices'
    __table_args__ = (
        ForeignKeyConstraint(['appointment_id'], ['appointments.id'], ondelete='SET NULL', name='invoices_appointment_id_fkey'),
        ForeignKeyConstraint(['clinic_id'], ['clinics.id'], ondelete='SET NULL', name='invoices_clinic_id_fkey'),
        ForeignKeyConstraint(['doctor_id'], ['doctor_profiles.user_id'], ondelete='SET NULL', name='invoices_doctor_id_fkey'),
        ForeignKeyConstraint(['patient_id'], ['patient_profiles.user_id'], ondelete='SET NULL', name='invoices_patient_id_fkey'),
        PrimaryKeyConstraint('id', name='invoices_pkey'),
        UniqueConstraint('invoice_number', name='invoices_invoice_number_key')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    invoice_number: Mapped[str] = mapped_column(String(50))
    amount: Mapped[decimal.Decimal] = mapped_column(Numeric(12, 2))
    total_amount: Mapped[decimal.Decimal] = mapped_column(Numeric(12, 2))
    appointment_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    patient_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    doctor_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    clinic_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    tax_amount: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(12, 2))
    status: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("'unpaid'::character varying"))
    due_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    paid_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    appointment: Mapped[Optional['Appointments']] = relationship('Appointments', back_populates='invoices')
    clinic: Mapped[Optional['Clinics']] = relationship('Clinics', back_populates='invoices')
    doctor: Mapped[Optional['DoctorProfiles']] = relationship('DoctorProfiles', back_populates='invoices')
    patient: Mapped[Optional['PatientProfiles']] = relationship('PatientProfiles', back_populates='invoices')
    invoice_items: Mapped[List['InvoiceItems']] = relationship('InvoiceItems', back_populates='invoice')


class LabResults(Base):
    __tablename__ = 'lab_results'
    __table_args__ = (
        ForeignKeyConstraint(['booking_id'], ['lab_bookings.id'], ondelete='CASCADE', name='lab_results_booking_id_fkey'),
        ForeignKeyConstraint(['patient_id'], ['patient_profiles.user_id'], ondelete='CASCADE', name='lab_results_patient_id_fkey'),
        ForeignKeyConstraint(['test_id'], ['lab_tests.id'], name='lab_results_test_id_fkey'),
        PrimaryKeyConstraint('id', name='lab_results_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    booking_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    patient_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    test_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    result_value: Mapped[Optional[str]] = mapped_column(Text)
    reference_range: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[Optional[str]] = mapped_column(String(50))
    result_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    report_url: Mapped[Optional[str]] = mapped_column(Text)

    booking: Mapped[Optional['LabBookings']] = relationship('LabBookings', back_populates='lab_results')
    patient: Mapped[Optional['PatientProfiles']] = relationship('PatientProfiles', back_populates='lab_results')
    test: Mapped[Optional['LabTests']] = relationship('LabTests', back_populates='lab_results')


class MedicalVisits(Base):
    __tablename__ = 'medical_visits'
    __table_args__ = (
        ForeignKeyConstraint(['appointment_id'], ['appointments.id'], name='medical_visits_appointment_id_fkey'),
        ForeignKeyConstraint(['clinic_id'], ['clinics.id'], ondelete='SET NULL', name='medical_visits_clinic_id_fkey'),
        ForeignKeyConstraint(['doctor_id'], ['doctor_profiles.user_id'], ondelete='CASCADE', name='medical_visits_doctor_id_fkey'),
        ForeignKeyConstraint(['patient_id'], ['patient_profiles.user_id'], ondelete='CASCADE', name='medical_visits_patient_id_fkey'),
        PrimaryKeyConstraint('id', name='medical_visits_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    patient_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    doctor_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    clinic_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    appointment_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    visit_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    chief_complaint: Mapped[Optional[str]] = mapped_column(Text)
    diagnosis: Mapped[Optional[str]] = mapped_column(Text)
    treatment_plan: Mapped[Optional[str]] = mapped_column(Text)
    follow_up_instructions: Mapped[Optional[str]] = mapped_column(Text)
    vital_signs: Mapped[Optional[dict]] = mapped_column(JSONB)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    appointment: Mapped[Optional['Appointments']] = relationship('Appointments', back_populates='medical_visits')
    clinic: Mapped[Optional['Clinics']] = relationship('Clinics', back_populates='medical_visits')
    doctor: Mapped[Optional['DoctorProfiles']] = relationship('DoctorProfiles', back_populates='medical_visits')
    patient: Mapped[Optional['PatientProfiles']] = relationship('PatientProfiles', back_populates='medical_visits')
    medical_documents: Mapped[List['MedicalDocuments']] = relationship('MedicalDocuments', back_populates='visit')
    prescriptions: Mapped[List['Prescriptions']] = relationship('Prescriptions', back_populates='visit')
    vital_signs_: Mapped[List['VitalSigns']] = relationship('VitalSigns', back_populates='visit')


class Payments(Base):
    __tablename__ = 'payments'
    __table_args__ = (
        ForeignKeyConstraint(['appointment_id'], ['appointments.id'], ondelete='SET NULL', name='payments_appointment_id_fkey'),
        ForeignKeyConstraint(['patient_id'], ['patient_profiles.user_id'], ondelete='SET NULL', name='payments_patient_id_fkey'),
        PrimaryKeyConstraint('id', name='payments_pkey'),
        UniqueConstraint('razorpay_order_id', name='payments_razorpay_order_id_key'),
        UniqueConstraint('razorpay_payment_id', name='payments_razorpay_payment_id_key'),
        Index('idx_payments_razorpay_order', 'razorpay_order_id'),
        Index('idx_payments_status', 'status', 'payment_date')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    amount: Mapped[decimal.Decimal] = mapped_column(Numeric(12, 2))
    razorpay_order_id: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50))
    appointment_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    patient_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    currency: Mapped[Optional[str]] = mapped_column(String(10), server_default=text("'INR'::character varying"))
    payment_gateway: Mapped[Optional[str]] = mapped_column(String(100), server_default=text("'razorpay'::character varying"))
    razorpay_payment_id: Mapped[Optional[str]] = mapped_column(String(255))
    razorpay_signature: Mapped[Optional[str]] = mapped_column(String(255))
    payment_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    refund_amount: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(12, 2), server_default=text('0'))
    refund_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    appointment: Mapped[Optional['Appointments']] = relationship('Appointments', back_populates='payments')
    patient: Mapped[Optional['PatientProfiles']] = relationship('PatientProfiles', back_populates='payments')
    refunds: Mapped[List['Refunds']] = relationship('Refunds', back_populates='payment')


class TelemedicineSessions(Base):
    __tablename__ = 'telemedicine_sessions'
    __table_args__ = (
        ForeignKeyConstraint(['appointment_id'], ['appointments.id'], ondelete='CASCADE', name='telemedicine_sessions_appointment_id_fkey'),
        PrimaryKeyConstraint('id', name='telemedicine_sessions_pkey'),
        Index('idx_telemedicine_sessions_appointment', 'appointment_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    appointment_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    room_id: Mapped[Optional[str]] = mapped_column(String(255))
    session_token: Mapped[Optional[str]] = mapped_column(Text)
    start_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    end_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    status: Mapped[Optional[str]] = mapped_column(String(50))
    recording_url: Mapped[Optional[str]] = mapped_column(Text)
    connection_quality: Mapped[Optional[str]] = mapped_column(String(50))
    participants_info: Mapped[Optional[dict]] = mapped_column(JSONB)

    appointment: Mapped[Optional['Appointments']] = relationship('Appointments', back_populates='telemedicine_sessions')
    call_logs: Mapped[List['CallLogs']] = relationship('CallLogs', back_populates='session')


class CallLogs(Base):
    __tablename__ = 'call_logs'
    __table_args__ = (
        ForeignKeyConstraint(['participant_id'], ['users.id'], ondelete='CASCADE', name='call_logs_participant_id_fkey'),
        ForeignKeyConstraint(['session_id'], ['telemedicine_sessions.id'], ondelete='CASCADE', name='call_logs_session_id_fkey'),
        PrimaryKeyConstraint('id', name='call_logs_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    session_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    participant_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    action: Mapped[Optional[str]] = mapped_column(String(100))
    timestamp: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    details: Mapped[Optional[str]] = mapped_column(Text)

    participant: Mapped[Optional['Users']] = relationship('Users', back_populates='call_logs')
    session: Mapped[Optional['TelemedicineSessions']] = relationship('TelemedicineSessions', back_populates='call_logs')


class ChatMessages(Base):
    __tablename__ = 'chat_messages'
    __table_args__ = (
        ForeignKeyConstraint(['conversation_id'], ['chat_conversations.id'], ondelete='CASCADE', name='chat_messages_conversation_id_fkey'),
        ForeignKeyConstraint(['sender_id'], ['users.id'], ondelete='CASCADE', name='chat_messages_sender_id_fkey'),
        PrimaryKeyConstraint('id', name='chat_messages_pkey'),
        Index('idx_chat_messages_conversation', 'conversation_id', 'sent_at')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    conversation_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    sender_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    message_type: Mapped[Optional[str]] = mapped_column(String(50))
    content: Mapped[Optional[str]] = mapped_column(Text)
    attachment_url: Mapped[Optional[str]] = mapped_column(Text)
    sent_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    read_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    delivery_status: Mapped[Optional[str]] = mapped_column(String(50))

    conversation: Mapped[Optional['ChatConversations']] = relationship('ChatConversations', back_populates='chat_messages')
    sender: Mapped[Optional['Users']] = relationship('Users', back_populates='chat_messages')
    message_attachments: Mapped[List['MessageAttachments']] = relationship('MessageAttachments', back_populates='message')


class FeedbackReports(Base):
    __tablename__ = 'feedback_reports'
    __table_args__ = (
        ForeignKeyConstraint(['feedback_id'], ['appointment_feedback.id'], ondelete='CASCADE', name='feedback_reports_feedback_id_fkey'),
        ForeignKeyConstraint(['reported_by'], ['users.id'], name='feedback_reports_reported_by_fkey'),
        PrimaryKeyConstraint('id', name='feedback_reports_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    feedback_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    reported_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    reason: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[Optional[str]] = mapped_column(String(50))
    reviewed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    action_taken: Mapped[Optional[str]] = mapped_column(Text)

    feedback: Mapped[Optional['AppointmentFeedback']] = relationship('AppointmentFeedback', back_populates='feedback_reports')
    users: Mapped[Optional['Users']] = relationship('Users', back_populates='feedback_reports')


class InvoiceItems(Base):
    __tablename__ = 'invoice_items'
    __table_args__ = (
        ForeignKeyConstraint(['invoice_id'], ['invoices.id'], ondelete='CASCADE', name='invoice_items_invoice_id_fkey'),
        PrimaryKeyConstraint('id', name='invoice_items_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    invoice_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    description: Mapped[Optional[str]] = mapped_column(Text)
    quantity: Mapped[Optional[int]] = mapped_column(Integer)
    unit_price: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(12, 2))
    total_price: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(12, 2))

    invoice: Mapped[Optional['Invoices']] = relationship('Invoices', back_populates='invoice_items')


class MedicalDocuments(Base):
    __tablename__ = 'medical_documents'
    __table_args__ = (
        ForeignKeyConstraint(['doctor_id'], ['doctor_profiles.user_id'], ondelete='SET NULL', name='medical_documents_doctor_id_fkey'),
        ForeignKeyConstraint(['patient_id'], ['patient_profiles.user_id'], ondelete='CASCADE', name='medical_documents_patient_id_fkey'),
        ForeignKeyConstraint(['visit_id'], ['medical_visits.id'], ondelete='SET NULL', name='medical_documents_visit_id_fkey'),
        PrimaryKeyConstraint('id', name='medical_documents_pkey'),
        Index('idx_medical_documents_patient', 'patient_id', 'document_type')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    patient_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    doctor_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    visit_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    document_type: Mapped[Optional[str]] = mapped_column(String(100))
    file_name: Mapped[Optional[str]] = mapped_column(String(255))
    file_path: Mapped[Optional[str]] = mapped_column(Text)
    file_size: Mapped[Optional[int]] = mapped_column(BigInteger)
    upload_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    access_permissions: Mapped[Optional[dict]] = mapped_column(JSONB)

    doctor: Mapped[Optional['DoctorProfiles']] = relationship('DoctorProfiles', back_populates='medical_documents')
    patient: Mapped[Optional['PatientProfiles']] = relationship('PatientProfiles', back_populates='medical_documents')
    visit: Mapped[Optional['MedicalVisits']] = relationship('MedicalVisits', back_populates='medical_documents')


class Prescriptions(Base):
    __tablename__ = 'prescriptions'
    __table_args__ = (
        ForeignKeyConstraint(['doctor_id'], ['doctor_profiles.user_id'], ondelete='CASCADE', name='prescriptions_doctor_id_fkey'),
        ForeignKeyConstraint(['patient_id'], ['patient_profiles.user_id'], ondelete='CASCADE', name='prescriptions_patient_id_fkey'),
        ForeignKeyConstraint(['visit_id'], ['medical_visits.id'], ondelete='CASCADE', name='prescriptions_visit_id_fkey'),
        PrimaryKeyConstraint('id', name='prescriptions_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    visit_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    doctor_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    patient_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    prescription_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    status: Mapped[Optional[str]] = mapped_column(String(50))
    notes: Mapped[Optional[str]] = mapped_column(Text)

    doctor: Mapped[Optional['DoctorProfiles']] = relationship('DoctorProfiles', back_populates='prescriptions')
    patient: Mapped[Optional['PatientProfiles']] = relationship('PatientProfiles', back_populates='prescriptions')
    visit: Mapped[Optional['MedicalVisits']] = relationship('MedicalVisits', back_populates='prescriptions')
    pharmacy_orders: Mapped[List['PharmacyOrders']] = relationship('PharmacyOrders', back_populates='prescription')
    prescription_medicines: Mapped[List['PrescriptionMedicines']] = relationship('PrescriptionMedicines', back_populates='prescription')


class Refunds(Base):
    __tablename__ = 'refunds'
    __table_args__ = (
        ForeignKeyConstraint(['payment_id'], ['payments.id'], ondelete='CASCADE', name='refunds_payment_id_fkey'),
        PrimaryKeyConstraint('id', name='refunds_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    payment_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    amount: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(12, 2))
    reason: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[Optional[str]] = mapped_column(String(50))
    requested_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    processed_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    refund_method: Mapped[Optional[str]] = mapped_column(String(100))

    payment: Mapped[Optional['Payments']] = relationship('Payments', back_populates='refunds')


class VitalSigns(Base):
    __tablename__ = 'vital_signs'
    __table_args__ = (
        ForeignKeyConstraint(['patient_id'], ['patient_profiles.user_id'], ondelete='CASCADE', name='vital_signs_patient_id_fkey'),
        ForeignKeyConstraint(['visit_id'], ['medical_visits.id'], ondelete='CASCADE', name='vital_signs_visit_id_fkey'),
        PrimaryKeyConstraint('id', name='vital_signs_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    patient_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    visit_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    recorded_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    blood_pressure_systolic: Mapped[Optional[int]] = mapped_column(Integer)
    blood_pressure_diastolic: Mapped[Optional[int]] = mapped_column(Integer)
    heart_rate: Mapped[Optional[int]] = mapped_column(Integer)
    temperature: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))
    weight: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(6, 2))
    height: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(6, 2))
    bmi: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))
    oxygen_saturation: Mapped[Optional[int]] = mapped_column(Integer)

    patient: Mapped[Optional['PatientProfiles']] = relationship('PatientProfiles', back_populates='vital_signs')
    visit: Mapped[Optional['MedicalVisits']] = relationship('MedicalVisits', back_populates='vital_signs_')


class MessageAttachments(Base):
    __tablename__ = 'message_attachments'
    __table_args__ = (
        ForeignKeyConstraint(['message_id'], ['chat_messages.id'], ondelete='CASCADE', name='message_attachments_message_id_fkey'),
        PrimaryKeyConstraint('id', name='message_attachments_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    message_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    file_name: Mapped[Optional[str]] = mapped_column(String(255))
    file_path: Mapped[Optional[str]] = mapped_column(Text)
    file_type: Mapped[Optional[str]] = mapped_column(String(100))
    file_size: Mapped[Optional[int]] = mapped_column(BigInteger)
    uploaded_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    message: Mapped[Optional['ChatMessages']] = relationship('ChatMessages', back_populates='message_attachments')


class PharmacyOrders(Base):
    __tablename__ = 'pharmacy_orders'
    __table_args__ = (
        ForeignKeyConstraint(['patient_id'], ['patient_profiles.user_id'], ondelete='CASCADE', name='pharmacy_orders_patient_id_fkey'),
        ForeignKeyConstraint(['pharmacy_partner_id'], ['pharmacy_partners.id'], ondelete='CASCADE', name='pharmacy_orders_pharmacy_partner_id_fkey'),
        ForeignKeyConstraint(['prescription_id'], ['prescriptions.id'], name='pharmacy_orders_prescription_id_fkey'),
        PrimaryKeyConstraint('id', name='pharmacy_orders_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    patient_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    pharmacy_partner_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    prescription_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    order_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    status: Mapped[Optional[str]] = mapped_column(String(50))
    total_amount: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    delivery_address: Mapped[Optional[str]] = mapped_column(Text)

    patient: Mapped[Optional['PatientProfiles']] = relationship('PatientProfiles', back_populates='pharmacy_orders')
    pharmacy_partner: Mapped[Optional['PharmacyPartners']] = relationship('PharmacyPartners', back_populates='pharmacy_orders')
    prescription: Mapped[Optional['Prescriptions']] = relationship('Prescriptions', back_populates='pharmacy_orders')


class PrescriptionMedicines(Base):
    __tablename__ = 'prescription_medicines'
    __table_args__ = (
        ForeignKeyConstraint(['prescription_id'], ['prescriptions.id'], ondelete='CASCADE', name='prescription_medicines_prescription_id_fkey'),
        PrimaryKeyConstraint('id', name='prescription_medicines_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    prescription_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    medicine_name: Mapped[Optional[str]] = mapped_column(String(255))
    dosage: Mapped[Optional[str]] = mapped_column(String(100))
    frequency: Mapped[Optional[str]] = mapped_column(String(100))
    duration: Mapped[Optional[str]] = mapped_column(String(100))
    instructions: Mapped[Optional[str]] = mapped_column(Text)
    generic_alternative: Mapped[Optional[str]] = mapped_column(String(255))

    prescription: Mapped[Optional['Prescriptions']] = relationship('Prescriptions', back_populates='prescription_medicines')
