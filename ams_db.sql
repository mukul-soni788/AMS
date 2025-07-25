--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: admin_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admin_logs (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    admin_id uuid,
    action character varying(100),
    target_type character varying(100),
    target_id uuid,
    details jsonb,
    ip_address inet,
    "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.admin_logs OWNER TO postgres;

--
-- Name: ai_chat_sessions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ai_chat_sessions (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    patient_id uuid,
    session_start timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    session_end timestamp with time zone,
    symptom_analysis jsonb,
    recommendations jsonb,
    triage_level character varying(50)
);


ALTER TABLE public.ai_chat_sessions OWNER TO postgres;

--
-- Name: ai_recommendations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ai_recommendations (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    session_id uuid,
    recommendation_type character varying(100),
    specialist_suggested character varying(255),
    urgency_level character varying(50),
    confidence_score numeric(5,4)
);


ALTER TABLE public.ai_recommendations OWNER TO postgres;

--
-- Name: allergies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.allergies (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    patient_id uuid,
    allergen character varying(255),
    reaction text,
    severity character varying(100),
    recorded_date timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    notes text
);


ALTER TABLE public.allergies OWNER TO postgres;

--
-- Name: analytics_events; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.analytics_events (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid,
    event_type character varying(100),
    event_data jsonb,
    "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    session_id character varying(255)
);


ALTER TABLE public.analytics_events OWNER TO postgres;

--
-- Name: appointment_feedback; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.appointment_feedback (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    appointment_id uuid,
    patient_id uuid,
    doctor_id uuid,
    overall_rating integer,
    communication_rating integer,
    punctuality_rating integer,
    expertise_rating integer,
    comments text,
    is_anonymous boolean DEFAULT false,
    submitted_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT appointment_feedback_communication_rating_check CHECK (((communication_rating >= 1) AND (communication_rating <= 5))),
    CONSTRAINT appointment_feedback_expertise_rating_check CHECK (((expertise_rating >= 1) AND (expertise_rating <= 5))),
    CONSTRAINT appointment_feedback_overall_rating_check CHECK (((overall_rating >= 1) AND (overall_rating <= 5))),
    CONSTRAINT appointment_feedback_punctuality_rating_check CHECK (((punctuality_rating >= 1) AND (punctuality_rating <= 5)))
);


ALTER TABLE public.appointment_feedback OWNER TO postgres;

--
-- Name: appointment_reminders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.appointment_reminders (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    appointment_id uuid,
    reminder_type character varying(50),
    send_at timestamp with time zone,
    status character varying(50),
    sent_at timestamp with time zone
);


ALTER TABLE public.appointment_reminders OWNER TO postgres;

--
-- Name: appointment_reschedule_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.appointment_reschedule_history (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    appointment_id uuid,
    old_date date,
    old_time time without time zone,
    new_date date,
    new_time time without time zone,
    reason text,
    rescheduled_by uuid,
    rescheduled_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.appointment_reschedule_history OWNER TO postgres;

--
-- Name: appointment_slots; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.appointment_slots (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    doctor_id uuid,
    clinic_id uuid,
    slot_date date,
    start_time time without time zone,
    end_time time without time zone,
    is_available boolean DEFAULT true,
    is_blocked boolean DEFAULT false,
    blocked_reason text
);


ALTER TABLE public.appointment_slots OWNER TO postgres;

--
-- Name: appointment_statuses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.appointment_statuses (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying(50) NOT NULL,
    description text
);


ALTER TABLE public.appointment_statuses OWNER TO postgres;

--
-- Name: appointments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.appointments (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    patient_id uuid,
    doctor_id uuid,
    clinic_id uuid,
    appointment_date date NOT NULL,
    start_time time without time zone,
    end_time time without time zone,
    consultation_type character varying(100),
    consultation_mode character varying(100),
    status character varying(50) DEFAULT 'scheduled'::character varying,
    reason_for_visit text,
    notes text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.appointments OWNER TO postgres;

--
-- Name: audit_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.audit_logs (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid,
    table_name character varying(100),
    record_id uuid,
    action character varying(50),
    old_values jsonb,
    new_values jsonb,
    "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    ip_address inet
);


ALTER TABLE public.audit_logs OWNER TO postgres;

--
-- Name: auth_tokens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_tokens (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid,
    token_hash text NOT NULL,
    token_type character varying(50),
    expires_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    is_active boolean DEFAULT true
);


ALTER TABLE public.auth_tokens OWNER TO postgres;

--
-- Name: backup_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.backup_logs (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    backup_type character varying(100),
    file_path text,
    size bigint,
    status character varying(50),
    started_at timestamp with time zone,
    completed_at timestamp with time zone,
    error_message text
);


ALTER TABLE public.backup_logs OWNER TO postgres;

--
-- Name: call_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.call_logs (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    session_id uuid,
    participant_id uuid,
    action character varying(100),
    "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    details text
);


ALTER TABLE public.call_logs OWNER TO postgres;

--
-- Name: certifications; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.certifications (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    doctor_id uuid,
    certificate_name character varying(255),
    issuing_body character varying(255),
    issue_date date,
    expiry_date date,
    certificate_url text
);


ALTER TABLE public.certifications OWNER TO postgres;

--
-- Name: chat_conversations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chat_conversations (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    patient_id uuid,
    doctor_id uuid,
    appointment_id uuid,
    started_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    last_message_at timestamp with time zone,
    status character varying(50)
);


ALTER TABLE public.chat_conversations OWNER TO postgres;

--
-- Name: chat_messages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chat_messages (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    conversation_id uuid,
    sender_id uuid,
    message_type character varying(50),
    content text,
    attachment_url text,
    sent_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    read_at timestamp with time zone,
    delivery_status character varying(50)
);


ALTER TABLE public.chat_messages OWNER TO postgres;

--
-- Name: clinic_admin_profiles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clinic_admin_profiles (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid,
    clinic_id uuid,
    admin_level character varying(50),
    permissions jsonb
);


ALTER TABLE public.clinic_admin_profiles OWNER TO postgres;

--
-- Name: clinic_doctors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clinic_doctors (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    clinic_id uuid,
    doctor_id uuid,
    joined_date timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    status character varying(50) DEFAULT 'active'::character varying,
    consultation_fee_override numeric(10,2)
);


ALTER TABLE public.clinic_doctors OWNER TO postgres;

--
-- Name: clinic_images; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clinic_images (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    clinic_id uuid,
    image_url text,
    image_type character varying(100),
    uploaded_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.clinic_images OWNER TO postgres;

--
-- Name: clinic_services; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clinic_services (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    clinic_id uuid,
    service_name character varying(255),
    description text,
    price numeric(10,2),
    duration_minutes integer
);


ALTER TABLE public.clinic_services OWNER TO postgres;

--
-- Name: clinics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clinics (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    address text,
    city character varying(255),
    state character varying(255),
    country character varying(255),
    postal_code character varying(20),
    latitude double precision,
    longitude double precision,
    phone character varying(20),
    email character varying(255),
    website character varying(255),
    license_number character varying(100),
    operating_hours jsonb,
    services_offered jsonb,
    images text[],
    is_active boolean DEFAULT true,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.clinics OWNER TO postgres;

--
-- Name: consultation_notes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.consultation_notes (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    appointment_id uuid,
    doctor_id uuid,
    notes text,
    diagnosis text,
    treatment_plan text,
    follow_up_date date,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.consultation_notes OWNER TO postgres;

--
-- Name: doctor_availability; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.doctor_availability (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    doctor_id uuid,
    clinic_id uuid,
    day_of_week integer,
    start_time time without time zone,
    end_time time without time zone,
    slot_duration integer,
    max_patients_per_slot integer,
    is_active boolean DEFAULT true,
    CONSTRAINT doctor_availability_day_of_week_check CHECK (((day_of_week >= 0) AND (day_of_week <= 6)))
);


ALTER TABLE public.doctor_availability OWNER TO postgres;

--
-- Name: doctor_languages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.doctor_languages (
    doctor_id uuid NOT NULL,
    language_id uuid NOT NULL,
    proficiency_level character varying(50)
);


ALTER TABLE public.doctor_languages OWNER TO postgres;

--
-- Name: doctor_profiles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.doctor_profiles (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid,
    medical_license_number character varying(255),
    license_expiry date,
    years_experience integer,
    bio text,
    consultation_fee numeric(10,2),
    telemedicine_enabled boolean DEFAULT false,
    is_verified boolean DEFAULT false,
    verification_documents text,
    specialization_primary character varying(255)
);


ALTER TABLE public.doctor_profiles OWNER TO postgres;

--
-- Name: doctor_ratings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.doctor_ratings (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    doctor_id uuid,
    average_rating numeric(3,2),
    total_reviews integer,
    communication_avg numeric(3,2),
    punctuality_avg numeric(3,2),
    expertise_avg numeric(3,2),
    last_updated timestamp with time zone
);


ALTER TABLE public.doctor_ratings OWNER TO postgres;

--
-- Name: doctor_schedules; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.doctor_schedules (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    doctor_id uuid,
    clinic_id uuid,
    schedule_date date,
    start_time time without time zone,
    end_time time without time zone,
    break_start time without time zone,
    break_end time without time zone,
    is_available boolean DEFAULT true,
    notes text
);


ALTER TABLE public.doctor_schedules OWNER TO postgres;

--
-- Name: doctor_specialties; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.doctor_specialties (
    doctor_id uuid NOT NULL,
    specialty_id uuid NOT NULL,
    is_primary boolean DEFAULT false,
    certification_date date
);


ALTER TABLE public.doctor_specialties OWNER TO postgres;

--
-- Name: educations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.educations (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    doctor_id uuid,
    degree character varying(255),
    institution character varying(255),
    year_completed integer,
    is_verified boolean DEFAULT false
);


ALTER TABLE public.educations OWNER TO postgres;

--
-- Name: email_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.email_logs (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid,
    email_address character varying(255),
    subject character varying(255),
    status character varying(50),
    sent_at timestamp with time zone,
    opened_at timestamp with time zone,
    clicked_at timestamp with time zone
);


ALTER TABLE public.email_logs OWNER TO postgres;

--
-- Name: emergency_contacts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.emergency_contacts (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    patient_id uuid,
    contact_name character varying(255),
    relationship character varying(100),
    phone character varying(20),
    email character varying(255),
    is_primary boolean DEFAULT false
);


ALTER TABLE public.emergency_contacts OWNER TO postgres;

--
-- Name: feedback_reports; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.feedback_reports (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    feedback_id uuid,
    reported_by uuid,
    reason text,
    status character varying(50),
    reviewed_at timestamp with time zone,
    action_taken text
);


ALTER TABLE public.feedback_reports OWNER TO postgres;

--
-- Name: file_uploads; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.file_uploads (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    uploaded_by uuid,
    file_name character varying(255),
    file_path text,
    file_type character varying(100),
    file_size bigint,
    virus_scan_status character varying(50),
    access_level character varying(50),
    uploaded_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.file_uploads OWNER TO postgres;

--
-- Name: health_tips; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.health_tips (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    title character varying(255),
    content text,
    category character varying(100),
    target_conditions character varying(255)[],
    created_by uuid,
    is_active boolean DEFAULT true,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.health_tips OWNER TO postgres;

--
-- Name: insurance_claims; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.insurance_claims (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    patient_id uuid,
    appointment_id uuid,
    insurance_provider character varying(255),
    policy_number character varying(255),
    claim_amount numeric(12,2),
    claim_status character varying(50),
    submitted_date timestamp with time zone,
    processed_date timestamp with time zone
);


ALTER TABLE public.insurance_claims OWNER TO postgres;

--
-- Name: invoice_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.invoice_items (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    invoice_id uuid,
    description text,
    quantity integer,
    unit_price numeric(12,2),
    total_price numeric(12,2)
);


ALTER TABLE public.invoice_items OWNER TO postgres;

--
-- Name: invoices; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.invoices (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    appointment_id uuid,
    patient_id uuid,
    doctor_id uuid,
    clinic_id uuid,
    invoice_number character varying(50) NOT NULL,
    amount numeric(12,2) NOT NULL,
    tax_amount numeric(12,2),
    total_amount numeric(12,2) NOT NULL,
    status character varying(50) DEFAULT 'unpaid'::character varying,
    due_date date,
    paid_date timestamp with time zone
);


ALTER TABLE public.invoices OWNER TO postgres;

--
-- Name: lab_bookings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lab_bookings (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    patient_id uuid,
    lab_partner_id uuid,
    test_ids uuid[],
    booking_date date,
    appointment_time time without time zone,
    home_collection boolean DEFAULT false,
    status character varying(50),
    total_amount numeric(10,2)
);


ALTER TABLE public.lab_bookings OWNER TO postgres;

--
-- Name: lab_partners; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lab_partners (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying(255) NOT NULL,
    address text,
    phone character varying(20),
    email character varying(255),
    services_offered jsonb,
    rating numeric(3,2),
    is_active boolean DEFAULT true
);


ALTER TABLE public.lab_partners OWNER TO postgres;

--
-- Name: lab_reports; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lab_reports (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    patient_id uuid,
    doctor_id uuid,
    test_name character varying(255),
    test_date date,
    results text,
    reference_values text,
    lab_name character varying(255),
    report_file text,
    status character varying(50)
);


ALTER TABLE public.lab_reports OWNER TO postgres;

--
-- Name: lab_results; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lab_results (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    booking_id uuid,
    patient_id uuid,
    test_id uuid,
    result_value text,
    reference_range text,
    status character varying(50),
    result_date date,
    report_url text
);


ALTER TABLE public.lab_results OWNER TO postgres;

--
-- Name: lab_tests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lab_tests (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    lab_partner_id uuid,
    test_name character varying(255),
    category character varying(100),
    description text,
    price numeric(10,2),
    preparation_instructions text,
    sample_type character varying(100),
    turnaround_time character varying(100)
);


ALTER TABLE public.lab_tests OWNER TO postgres;

--
-- Name: languages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.languages (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying(100) NOT NULL,
    code character varying(10) NOT NULL
);


ALTER TABLE public.languages OWNER TO postgres;

--
-- Name: locales; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.locales (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    code character varying(10) NOT NULL,
    name character varying(100),
    is_active boolean DEFAULT true,
    date_format character varying(50),
    time_format character varying(50),
    currency_code character varying(10),
    is_rtl boolean DEFAULT false
);


ALTER TABLE public.locales OWNER TO postgres;

--
-- Name: medical_documents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.medical_documents (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    patient_id uuid,
    doctor_id uuid,
    visit_id uuid,
    document_type character varying(100),
    file_name character varying(255),
    file_path text,
    file_size bigint,
    upload_date timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    access_permissions jsonb
);


ALTER TABLE public.medical_documents OWNER TO postgres;

--
-- Name: medical_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.medical_history (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    patient_id uuid,
    condition character varying(255),
    diagnosed_date date,
    status character varying(100),
    treatment text,
    notes text
);


ALTER TABLE public.medical_history OWNER TO postgres;

--
-- Name: medical_visits; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.medical_visits (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    patient_id uuid,
    doctor_id uuid,
    clinic_id uuid,
    appointment_id uuid,
    visit_date date,
    chief_complaint text,
    diagnosis text,
    treatment_plan text,
    follow_up_instructions text,
    vital_signs jsonb,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.medical_visits OWNER TO postgres;

--
-- Name: medicine_reminders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.medicine_reminders (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    patient_id uuid,
    medicine_name character varying(255),
    dosage character varying(100),
    frequency character varying(100),
    reminder_times time without time zone[],
    start_date date,
    end_date date,
    is_active boolean DEFAULT true
);


ALTER TABLE public.medicine_reminders OWNER TO postgres;

--
-- Name: medicines; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.medicines (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying(255) NOT NULL,
    generic_name character varying(255),
    brand_names text[],
    category character varying(100),
    description text,
    price numeric(10,2),
    prescription_required boolean DEFAULT true,
    stock_status character varying(50)
);


ALTER TABLE public.medicines OWNER TO postgres;

--
-- Name: message_attachments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.message_attachments (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    message_id uuid,
    file_name character varying(255),
    file_path text,
    file_type character varying(100),
    file_size bigint,
    uploaded_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.message_attachments OWNER TO postgres;

--
-- Name: notification_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notification_logs (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    notification_id uuid,
    channel character varying(50),
    status character varying(50),
    delivery_time timestamp with time zone,
    error_message text,
    retry_count integer DEFAULT 0
);


ALTER TABLE public.notification_logs OWNER TO postgres;

--
-- Name: notification_preferences; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notification_preferences (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid,
    notification_type character varying(100),
    email_enabled boolean DEFAULT true,
    sms_enabled boolean DEFAULT true,
    push_enabled boolean DEFAULT true,
    frequency character varying(50) DEFAULT 'immediate'::character varying
);


ALTER TABLE public.notification_preferences OWNER TO postgres;

--
-- Name: notification_templates; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notification_templates (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying(100) NOT NULL,
    subject character varying(255),
    email_template text,
    sms_template text,
    push_template text,
    variables jsonb
);


ALTER TABLE public.notification_templates OWNER TO postgres;

--
-- Name: notifications; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notifications (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid,
    title character varying(255) NOT NULL,
    message text,
    type character varying(100),
    channel character varying(50),
    status character varying(50) DEFAULT 'pending'::character varying,
    scheduled_at timestamp with time zone,
    sent_at timestamp with time zone,
    read_at timestamp with time zone,
    data jsonb
);


ALTER TABLE public.notifications OWNER TO postgres;

--
-- Name: otp_codes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.otp_codes (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid,
    code_hash text NOT NULL,
    contact_method character varying(50),
    purpose character varying(100),
    expires_at timestamp with time zone,
    attempts integer DEFAULT 0,
    is_used boolean DEFAULT false,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.otp_codes OWNER TO postgres;

--
-- Name: patient_favorites; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.patient_favorites (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    patient_id uuid,
    doctor_id uuid,
    added_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.patient_favorites OWNER TO postgres;

--
-- Name: patient_profiles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.patient_profiles (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid,
    emergency_contact_name character varying(255),
    emergency_contact_phone character varying(20),
    blood_group character varying(10),
    allergies text,
    chronic_conditions text,
    insurance_provider character varying(255),
    insurance_policy_number character varying(255),
    preferred_language character varying(10)
);


ALTER TABLE public.patient_profiles OWNER TO postgres;

--
-- Name: patient_vitals_tracking; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.patient_vitals_tracking (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    patient_id uuid,
    recorded_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    weight numeric(6,2),
    height numeric(6,2),
    blood_pressure_systolic integer,
    blood_pressure_diastolic integer,
    heart_rate integer,
    temperature numeric(5,2),
    blood_sugar numeric(6,2),
    notes text
);


ALTER TABLE public.patient_vitals_tracking OWNER TO postgres;

--
-- Name: payment_methods; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payment_methods (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid,
    method_type character varying(100),
    provider character varying(100),
    token text,
    is_default boolean DEFAULT false,
    is_active boolean DEFAULT true,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.payment_methods OWNER TO postgres;

--
-- Name: payments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payments (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    appointment_id uuid,
    patient_id uuid,
    amount numeric(12,2) NOT NULL,
    currency character varying(10) DEFAULT 'INR'::character varying,
    payment_gateway character varying(100) DEFAULT 'razorpay'::character varying,
    razorpay_order_id character varying(255) NOT NULL,
    razorpay_payment_id character varying(255),
    razorpay_signature character varying(255),
    status character varying(50) NOT NULL,
    payment_date timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    refund_amount numeric(12,2) DEFAULT 0,
    refund_date timestamp with time zone
);


ALTER TABLE public.payments OWNER TO postgres;

--
-- Name: pharmacy_orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pharmacy_orders (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    patient_id uuid,
    pharmacy_partner_id uuid,
    prescription_id uuid,
    order_date timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    status character varying(50),
    total_amount numeric(10,2),
    delivery_address text
);


ALTER TABLE public.pharmacy_orders OWNER TO postgres;

--
-- Name: pharmacy_partners; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pharmacy_partners (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying(255) NOT NULL,
    address text,
    phone character varying(20),
    email character varying(255),
    license_number character varying(100),
    is_active boolean DEFAULT true,
    delivery_available boolean DEFAULT false
);


ALTER TABLE public.pharmacy_partners OWNER TO postgres;

--
-- Name: prescription_medicines; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.prescription_medicines (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    prescription_id uuid,
    medicine_name character varying(255),
    dosage character varying(100),
    frequency character varying(100),
    duration character varying(100),
    instructions text,
    generic_alternative character varying(255)
);


ALTER TABLE public.prescription_medicines OWNER TO postgres;

--
-- Name: prescriptions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.prescriptions (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    visit_id uuid,
    doctor_id uuid,
    patient_id uuid,
    prescription_date date,
    status character varying(50),
    notes text
);


ALTER TABLE public.prescriptions OWNER TO postgres;

--
-- Name: refunds; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.refunds (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    payment_id uuid,
    amount numeric(12,2),
    reason text,
    status character varying(50),
    requested_date timestamp with time zone,
    processed_date timestamp with time zone,
    refund_method character varying(100)
);


ALTER TABLE public.refunds OWNER TO postgres;

--
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    permissions jsonb
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- Name: security_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.security_logs (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid,
    event_type character varying(100),
    details text,
    risk_level character varying(50),
    ip_address inet,
    user_agent text,
    "timestamp" timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.security_logs OWNER TO postgres;

--
-- Name: sessions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sessions (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid,
    session_token text NOT NULL,
    device_info text,
    ip_address inet,
    last_activity timestamp with time zone,
    expires_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.sessions OWNER TO postgres;

--
-- Name: sms_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sms_logs (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid,
    phone_number character varying(20),
    message text,
    status character varying(50),
    sent_at timestamp with time zone,
    delivery_status character varying(50),
    provider_response text
);


ALTER TABLE public.sms_logs OWNER TO postgres;

--
-- Name: specialties; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.specialties (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    category character varying(255)
);


ALTER TABLE public.specialties OWNER TO postgres;

--
-- Name: symptom_reports; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.symptom_reports (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    patient_id uuid,
    symptoms jsonb,
    severity integer,
    duration character varying(100),
    body_parts character varying(255)[],
    additional_info text,
    ai_assessment jsonb,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT symptom_reports_severity_check CHECK (((severity >= 1) AND (severity <= 10)))
);


ALTER TABLE public.symptom_reports OWNER TO postgres;

--
-- Name: system_announcements; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.system_announcements (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    title character varying(255),
    message text,
    type character varying(100),
    target_roles character varying(100)[],
    start_date timestamp with time zone,
    end_date timestamp with time zone,
    is_active boolean DEFAULT true,
    created_by uuid
);


ALTER TABLE public.system_announcements OWNER TO postgres;

--
-- Name: system_metrics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.system_metrics (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    metric_name character varying(100),
    value numeric(15,4),
    recorded_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    category character varying(100)
);


ALTER TABLE public.system_metrics OWNER TO postgres;

--
-- Name: telemedicine_sessions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.telemedicine_sessions (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    appointment_id uuid,
    room_id character varying(255),
    session_token text,
    start_time timestamp with time zone,
    end_time timestamp with time zone,
    status character varying(50),
    recording_url text,
    connection_quality character varying(50),
    participants_info jsonb
);


ALTER TABLE public.telemedicine_sessions OWNER TO postgres;

--
-- Name: translations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.translations (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    locale character varying(10),
    translation_key character varying(255),
    translation_value text,
    context character varying(255),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.translations OWNER TO postgres;

--
-- Name: user_devices; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_devices (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid,
    device_id character varying(255),
    device_type character varying(100),
    push_token text,
    is_active boolean DEFAULT true,
    last_seen timestamp with time zone
);


ALTER TABLE public.user_devices OWNER TO postgres;

--
-- Name: user_locale_preferences; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_locale_preferences (
    user_id uuid NOT NULL,
    locale_id uuid NOT NULL,
    date_format character varying(50),
    time_format character varying(50),
    currency_display character varying(50)
);


ALTER TABLE public.user_locale_preferences OWNER TO postgres;

--
-- Name: user_roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_roles (
    user_id uuid NOT NULL,
    role_id uuid NOT NULL,
    assigned_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    assigned_by uuid
);


ALTER TABLE public.user_roles OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    email character varying(255) NOT NULL,
    phone character varying(20),
    password_hash character varying(255) NOT NULL,
    full_name character varying(255) NOT NULL,
    date_of_birth date,
    gender character varying(50),
    profile_picture text,
    language_preference character varying(10),
    is_active boolean DEFAULT true,
    is_verified boolean DEFAULT false,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: vital_signs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vital_signs (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    patient_id uuid,
    visit_id uuid,
    recorded_date timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    blood_pressure_systolic integer,
    blood_pressure_diastolic integer,
    heart_rate integer,
    temperature numeric(5,2),
    weight numeric(6,2),
    height numeric(6,2),
    bmi numeric(5,2),
    oxygen_saturation integer
);


ALTER TABLE public.vital_signs OWNER TO postgres;

--
-- Name: wallet_transactions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wallet_transactions (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid,
    transaction_type character varying(50),
    amount numeric(12,2),
    balance_before numeric(12,2),
    balance_after numeric(12,2),
    reference_id uuid,
    description text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.wallet_transactions OWNER TO postgres;

--
-- Data for Name: admin_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.admin_logs (id, admin_id, action, target_type, target_id, details, ip_address, "timestamp") FROM stdin;
\.


--
-- Data for Name: ai_chat_sessions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ai_chat_sessions (id, patient_id, session_start, session_end, symptom_analysis, recommendations, triage_level) FROM stdin;
\.


--
-- Data for Name: ai_recommendations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ai_recommendations (id, session_id, recommendation_type, specialist_suggested, urgency_level, confidence_score) FROM stdin;
\.


--
-- Data for Name: allergies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.allergies (id, patient_id, allergen, reaction, severity, recorded_date, notes) FROM stdin;
\.


--
-- Data for Name: analytics_events; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.analytics_events (id, user_id, event_type, event_data, "timestamp", session_id) FROM stdin;
\.


--
-- Data for Name: appointment_feedback; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.appointment_feedback (id, appointment_id, patient_id, doctor_id, overall_rating, communication_rating, punctuality_rating, expertise_rating, comments, is_anonymous, submitted_at) FROM stdin;
\.


--
-- Data for Name: appointment_reminders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.appointment_reminders (id, appointment_id, reminder_type, send_at, status, sent_at) FROM stdin;
\.


--
-- Data for Name: appointment_reschedule_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.appointment_reschedule_history (id, appointment_id, old_date, old_time, new_date, new_time, reason, rescheduled_by, rescheduled_at) FROM stdin;
\.


--
-- Data for Name: appointment_slots; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.appointment_slots (id, doctor_id, clinic_id, slot_date, start_time, end_time, is_available, is_blocked, blocked_reason) FROM stdin;
\.


--
-- Data for Name: appointment_statuses; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.appointment_statuses (id, name, description) FROM stdin;
85395929-d4af-48ce-b307-39189f6a36a7	scheduled	Appointment has been scheduled
d2128128-0268-41d9-a780-bd99a27d9f30	confirmed	Appointment confirmed by doctor
74a18bfb-cc90-499d-9fe7-f2db6bf90f96	in_progress	Consultation is currently ongoing
5d7d4fef-92bf-4d4c-8340-6def62c9d6e8	completed	Consultation has been completed
44275e3c-218c-4a76-bff8-83078757ca70	cancelled	Appointment was cancelled
589983e6-90a6-4ece-8f05-fa3b86185e5d	no_show	Patient did not show up
939a8278-f589-4b19-b4ae-e226aa5626a0	rescheduled	Appointment has been rescheduled
f4356e22-9ed7-4307-aa81-6eae177af959	pending_payment	Waiting for payment confirmation
5599c5fc-dd50-421b-aabe-0337d51c9a73	refunded	Payment has been refunded
\.


--
-- Data for Name: appointments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.appointments (id, patient_id, doctor_id, clinic_id, appointment_date, start_time, end_time, consultation_type, consultation_mode, status, reason_for_visit, notes, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: audit_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.audit_logs (id, user_id, table_name, record_id, action, old_values, new_values, "timestamp", ip_address) FROM stdin;
\.


--
-- Data for Name: auth_tokens; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_tokens (id, user_id, token_hash, token_type, expires_at, created_at, is_active) FROM stdin;
\.


--
-- Data for Name: backup_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.backup_logs (id, backup_type, file_path, size, status, started_at, completed_at, error_message) FROM stdin;
\.


--
-- Data for Name: call_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.call_logs (id, session_id, participant_id, action, "timestamp", details) FROM stdin;
\.


--
-- Data for Name: certifications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.certifications (id, doctor_id, certificate_name, issuing_body, issue_date, expiry_date, certificate_url) FROM stdin;
\.


--
-- Data for Name: chat_conversations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.chat_conversations (id, patient_id, doctor_id, appointment_id, started_at, last_message_at, status) FROM stdin;
\.


--
-- Data for Name: chat_messages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.chat_messages (id, conversation_id, sender_id, message_type, content, attachment_url, sent_at, read_at, delivery_status) FROM stdin;
\.


--
-- Data for Name: clinic_admin_profiles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clinic_admin_profiles (id, user_id, clinic_id, admin_level, permissions) FROM stdin;
\.


--
-- Data for Name: clinic_doctors; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clinic_doctors (id, clinic_id, doctor_id, joined_date, status, consultation_fee_override) FROM stdin;
\.


--
-- Data for Name: clinic_images; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clinic_images (id, clinic_id, image_url, image_type, uploaded_at) FROM stdin;
\.


--
-- Data for Name: clinic_services; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clinic_services (id, clinic_id, service_name, description, price, duration_minutes) FROM stdin;
\.


--
-- Data for Name: clinics; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clinics (id, name, description, address, city, state, country, postal_code, latitude, longitude, phone, email, website, license_number, operating_hours, services_offered, images, is_active, created_at) FROM stdin;
\.


--
-- Data for Name: consultation_notes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.consultation_notes (id, appointment_id, doctor_id, notes, diagnosis, treatment_plan, follow_up_date, created_at) FROM stdin;
\.


--
-- Data for Name: doctor_availability; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.doctor_availability (id, doctor_id, clinic_id, day_of_week, start_time, end_time, slot_duration, max_patients_per_slot, is_active) FROM stdin;
\.


--
-- Data for Name: doctor_languages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.doctor_languages (doctor_id, language_id, proficiency_level) FROM stdin;
\.


--
-- Data for Name: doctor_profiles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.doctor_profiles (id, user_id, medical_license_number, license_expiry, years_experience, bio, consultation_fee, telemedicine_enabled, is_verified, verification_documents, specialization_primary) FROM stdin;
d31a4e02-20cf-47b9-b73c-521e0a71eaf4	550e8400-e29b-41d4-a716-446655440002	MD123456789	\N	15	Experienced cardiologist with expertise in preventive cardiology and heart disease management.	150.00	t	t	\N	Cardiology
6ff6a262-5edf-4994-82cc-8e5a977cfa36	550e8400-e29b-41d4-a716-446655440005	MD987654321	\N	20	Senior physician and clinic administrator with expertise in internal medicine.	200.00	t	t	\N	Internal Medicine
\.


--
-- Data for Name: doctor_ratings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.doctor_ratings (id, doctor_id, average_rating, total_reviews, communication_avg, punctuality_avg, expertise_avg, last_updated) FROM stdin;
\.


--
-- Data for Name: doctor_schedules; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.doctor_schedules (id, doctor_id, clinic_id, schedule_date, start_time, end_time, break_start, break_end, is_available, notes) FROM stdin;
\.


--
-- Data for Name: doctor_specialties; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.doctor_specialties (doctor_id, specialty_id, is_primary, certification_date) FROM stdin;
\.


--
-- Data for Name: educations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.educations (id, doctor_id, degree, institution, year_completed, is_verified) FROM stdin;
\.


--
-- Data for Name: email_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.email_logs (id, user_id, email_address, subject, status, sent_at, opened_at, clicked_at) FROM stdin;
\.


--
-- Data for Name: emergency_contacts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.emergency_contacts (id, patient_id, contact_name, relationship, phone, email, is_primary) FROM stdin;
\.


--
-- Data for Name: feedback_reports; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.feedback_reports (id, feedback_id, reported_by, reason, status, reviewed_at, action_taken) FROM stdin;
\.


--
-- Data for Name: file_uploads; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.file_uploads (id, uploaded_by, file_name, file_path, file_type, file_size, virus_scan_status, access_level, uploaded_at) FROM stdin;
\.


--
-- Data for Name: health_tips; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.health_tips (id, title, content, category, target_conditions, created_by, is_active, created_at) FROM stdin;
ff91ba48-339e-462e-9d00-f17f4f5ce93f	Stay Hydrated	Drink at least 8 glasses of water daily to maintain proper body function and prevent dehydration.	General Wellness	{}	\N	t	2025-07-23 17:22:57.689814+05:30
14da1ba3-fafb-4b70-accc-8e6079ba1269	Regular Exercise	Engage in at least 30 minutes of moderate physical activity most days of the week.	Fitness	{obesity,diabetes,hypertension}	\N	t	2025-07-23 17:22:57.689814+05:30
116d0b24-5b20-4d27-909b-a7b7c797ef03	Heart-Healthy Diet	Include fruits, vegetables, whole grains, and lean proteins while limiting saturated fats and sodium.	Nutrition	{heart_disease,hypertension,cholesterol}	\N	t	2025-07-23 17:22:57.689814+05:30
46ade7c4-14a6-4178-8a34-bce07f2a7483	Blood Sugar Management	Monitor blood glucose regularly and follow prescribed medication schedules.	Diabetes Care	{diabetes,prediabetes}	\N	t	2025-07-23 17:22:57.689814+05:30
6db6d70d-3a65-42d8-a890-e25020c89fe7	Stress Management	Practice relaxation techniques like deep breathing, meditation, or yoga to manage stress.	Mental Health	{anxiety,stress,hypertension}	\N	t	2025-07-23 17:22:57.689814+05:30
\.


--
-- Data for Name: insurance_claims; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.insurance_claims (id, patient_id, appointment_id, insurance_provider, policy_number, claim_amount, claim_status, submitted_date, processed_date) FROM stdin;
\.


--
-- Data for Name: invoice_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.invoice_items (id, invoice_id, description, quantity, unit_price, total_price) FROM stdin;
\.


--
-- Data for Name: invoices; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.invoices (id, appointment_id, patient_id, doctor_id, clinic_id, invoice_number, amount, tax_amount, total_amount, status, due_date, paid_date) FROM stdin;
\.


--
-- Data for Name: lab_bookings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.lab_bookings (id, patient_id, lab_partner_id, test_ids, booking_date, appointment_time, home_collection, status, total_amount) FROM stdin;
\.


--
-- Data for Name: lab_partners; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.lab_partners (id, name, address, phone, email, services_offered, rating, is_active) FROM stdin;
\.


--
-- Data for Name: lab_reports; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.lab_reports (id, patient_id, doctor_id, test_name, test_date, results, reference_values, lab_name, report_file, status) FROM stdin;
\.


--
-- Data for Name: lab_results; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.lab_results (id, booking_id, patient_id, test_id, result_value, reference_range, status, result_date, report_url) FROM stdin;
\.


--
-- Data for Name: lab_tests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.lab_tests (id, lab_partner_id, test_name, category, description, price, preparation_instructions, sample_type, turnaround_time) FROM stdin;
0c654479-5473-40b6-9aa2-8d588bb994f7	\N	Complete Blood Count (CBC)	Hematology	Comprehensive blood analysis	\N	No special preparation required	Blood	24 hours
75b19425-a3b6-428b-ac5e-ce3bf7a47927	\N	Lipid Profile	Biochemistry	Cholesterol and triglyceride levels	\N	12-hour fasting required	Blood	24 hours
119405ac-0448-484d-a650-4d2e81c6516d	\N	Blood Glucose (Fasting)	Biochemistry	Blood sugar levels	\N	12-hour fasting required	Blood	2 hours
dbedab42-1431-4d80-8c00-ae831ba6074f	\N	Thyroid Function Test	Endocrinology	TSH, T3, T4 levels	\N	No special preparation	Blood	48 hours
11b5951b-1cf5-44ff-b3cf-edb6d26f6b6a	\N	Liver Function Test	Biochemistry	Liver enzyme levels	\N	No special preparation	Blood	24 hours
71e6746e-4c09-45b0-86c8-8102685714b5	\N	Kidney Function Test	Biochemistry	Creatinine and BUN levels	\N	No special preparation	Blood	24 hours
4978b69d-e921-4da4-87d3-d52ede79f9bd	\N	Urine Analysis	Clinical Pathology	Complete urine examination	\N	Clean catch midstream sample	Urine	4 hours
4e8f297f-d128-4e4f-a417-c14873c8e514	\N	HbA1c	Biochemistry	Long-term blood sugar control	\N	No fasting required	Blood	24 hours
\.


--
-- Data for Name: languages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.languages (id, name, code) FROM stdin;
b8424374-dd9d-4654-8b30-014567078244	English	en
f97169bc-bc6c-490b-81a4-e402a19c8bf5	Hindi	hi
cc599f6e-c3ec-4603-92dc-eed9a29f27e5	Spanish	es
9f9ad501-5409-44b1-a805-e12a28505366	French	fr
973eb503-f244-4309-87f4-3241b3c5ed5c	German	de
5d981a32-5680-4977-a199-b4dbd14f9c00	Chinese	zh
b777f619-28ca-4997-a759-739a8808e021	Arabic	ar
085b1494-3b96-48df-bde9-28f06cd6c414	Portuguese	pt
ecad163b-4e69-44aa-925a-fd92cf07d96e	Russian	ru
871c1a3c-a389-4bc2-86d9-87c458e880e2	Japanese	ja
3d3af876-436c-4ca1-b247-254b9549bd6a	Korean	ko
f8840e26-9744-4704-bcba-a600e781d1f0	Italian	it
80fb6eb2-9535-4046-9d21-dd4af98512ac	Dutch	nl
67cf238f-22c9-43ca-859d-7bd6b7f69e46	Swedish	sv
dc344a6b-1478-42b9-86b8-ba8e99243f4c	Bengali	bn
05b55537-dbea-4250-982b-e08514b06682	Tamil	ta
c915ca89-797f-4b49-9e81-feb27ae4bf30	Telugu	te
12802ce2-cd0a-48d8-a266-42fb2a454e5f	Marathi	mr
33b5fa1d-ee92-429e-b674-ce8c5c991a43	Gujarati	gu
2c6233ce-d12e-4839-a448-43cf6493695e	Punjabi	pa
\.


--
-- Data for Name: locales; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.locales (id, code, name, is_active, date_format, time_format, currency_code, is_rtl) FROM stdin;
8804b33d-72f3-401b-ac6a-16fc89ae2b10	en-US	English (United States)	t	MM/DD/YYYY	12-hour	USD	f
382d5b89-2a59-4072-9239-53f9264732d9	en-IN	English (India)	t	DD/MM/YYYY	12-hour	INR	f
d45bf956-8935-468b-8a86-77b8d282d5ad	hi-IN	Hindi (India)	t	DD/MM/YYYY	12-hour	INR	f
65a05b7c-f674-4fce-9681-b2174d203e33	es-ES	Spanish (Spain)	t	DD/MM/YYYY	24-hour	EUR	f
1b0403a7-2899-4e55-96ef-18b680fc50d0	fr-FR	French (France)	t	DD/MM/YYYY	24-hour	EUR	f
a565cfab-3f7f-4cef-bb12-e662e09ab2d8	de-DE	German (Germany)	t	DD.MM.YYYY	24-hour	EUR	f
27cab2ad-8c12-4855-b841-c8acab54ace2	ar-SA	Arabic (Saudi Arabia)	t	DD/MM/YYYY	12-hour	SAR	t
aa64663e-55af-4421-b33e-8935cccca229	zh-CN	Chinese (China)	t	YYYY/MM/DD	24-hour	CNY	f
dd96ba6f-c5b3-4601-8961-1fb84864aab9	ja-JP	Japanese (Japan)	t	YYYY/MM/DD	24-hour	JPY	f
034fb0fa-e532-4ab6-9296-87392e9a8430	pt-BR	Portuguese (Brazil)	t	DD/MM/YYYY	24-hour	BRL	f
\.


--
-- Data for Name: medical_documents; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.medical_documents (id, patient_id, doctor_id, visit_id, document_type, file_name, file_path, file_size, upload_date, access_permissions) FROM stdin;
\.


--
-- Data for Name: medical_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.medical_history (id, patient_id, condition, diagnosed_date, status, treatment, notes) FROM stdin;
\.


--
-- Data for Name: medical_visits; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.medical_visits (id, patient_id, doctor_id, clinic_id, appointment_id, visit_date, chief_complaint, diagnosis, treatment_plan, follow_up_instructions, vital_signs, created_at) FROM stdin;
\.


--
-- Data for Name: medicine_reminders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.medicine_reminders (id, patient_id, medicine_name, dosage, frequency, reminder_times, start_date, end_date, is_active) FROM stdin;
\.


--
-- Data for Name: medicines; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.medicines (id, name, generic_name, brand_names, category, description, price, prescription_required, stock_status) FROM stdin;
7eaf79cd-d81e-4979-aac0-a8553c15ec12	Paracetamol	Acetaminophen	{Tylenol,Panadol,Crocin}	Analgesic	Pain reliever and fever reducer	\N	f	in_stock
b942b842-b8bb-42a6-9d08-57729abc6d89	Ibuprofen	Ibuprofen	{Advil,Motrin,Brufen}	NSAID	Anti-inflammatory pain reliever	\N	f	in_stock
03b78f5c-3690-4edb-a068-cb78d920ebb8	Aspirin	Acetylsalicylic Acid	{Bayer,Ecosprin}	NSAID	Pain reliever and blood thinner	\N	f	in_stock
06bd49bf-fab4-4646-af67-cd869f155be2	Amoxicillin	Amoxicillin	{Amoxil,Trimox}	Antibiotic	Penicillin antibiotic	\N	t	in_stock
8188b878-fc53-4d82-981a-e78aeb9bd661	Metformin	Metformin	{Glucophage,Glycomet}	Antidiabetic	Diabetes medication	\N	t	in_stock
8b406851-b588-4d0f-84e1-b2a3f9a62c79	Atorvastatin	Atorvastatin	{Lipitor,Atorlip}	Statin	Cholesterol medication	\N	t	in_stock
d8efae48-fce9-4fce-865c-4d915b894c3f	Omeprazole	Omeprazole	{Prilosec,Omez}	PPI	Acid reflux medication	\N	t	in_stock
\.


--
-- Data for Name: message_attachments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.message_attachments (id, message_id, file_name, file_path, file_type, file_size, uploaded_at) FROM stdin;
\.


--
-- Data for Name: notification_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notification_logs (id, notification_id, channel, status, delivery_time, error_message, retry_count) FROM stdin;
\.


--
-- Data for Name: notification_preferences; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notification_preferences (id, user_id, notification_type, email_enabled, sms_enabled, push_enabled, frequency) FROM stdin;
\.


--
-- Data for Name: notification_templates; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notification_templates (id, name, subject, email_template, sms_template, push_template, variables) FROM stdin;
8b1b9f93-344a-45ad-a78d-13481ed1112a	appointment_confirmation	Appointment Confirmed	Dear {{patient_name}}, your appointment with Dr. {{doctor_name}} on {{appointment_date}} at {{appointment_time}} has been confirmed.	Hi {{patient_name}}! Your appointment with Dr. {{doctor_name}} on {{appointment_date}} at {{appointment_time}} is confirmed.	Appointment confirmed with Dr. {{doctor_name}}	["patient_name", "doctor_name", "appointment_date", "appointment_time"]
41131c07-aba0-465c-838d-d8f0692d0be0	appointment_reminder	Appointment Reminder	Dear {{patient_name}}, this is a reminder for your appointment with Dr. {{doctor_name}} tomorrow at {{appointment_time}}.	Reminder: Tomorrow {{appointment_time}} - Dr. {{doctor_name}}. Reply CANCEL to cancel.	Appointment reminder: Tomorrow at {{appointment_time}}	["patient_name", "doctor_name", "appointment_time"]
615b6275-dc4b-481f-b813-172e3eb7c178	payment_success	Payment Successful	Dear {{patient_name}}, your payment of {{amount}} for appointment #{{appointment_id}} has been processed successfully.	Payment of {{amount}} received for appointment #{{appointment_id}}. Thank you!	Payment successful: {{amount}}	["patient_name", "amount", "appointment_id"]
9b0242be-ab46-4b7e-bf8e-ffe6ce98c51e	prescription_ready	Prescription Ready	Dear {{patient_name}}, your prescription from Dr. {{doctor_name}} is ready for download.	Your prescription from Dr. {{doctor_name}} is ready. Check your app.	Prescription ready for download	["patient_name", "doctor_name"]
\.


--
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notifications (id, user_id, title, message, type, channel, status, scheduled_at, sent_at, read_at, data) FROM stdin;
\.


--
-- Data for Name: otp_codes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.otp_codes (id, user_id, code_hash, contact_method, purpose, expires_at, attempts, is_used, created_at) FROM stdin;
\.


--
-- Data for Name: patient_favorites; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.patient_favorites (id, patient_id, doctor_id, added_at) FROM stdin;
\.


--
-- Data for Name: patient_profiles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.patient_profiles (id, user_id, emergency_contact_name, emergency_contact_phone, blood_group, allergies, chronic_conditions, insurance_provider, insurance_policy_number, preferred_language) FROM stdin;
365a035d-12fa-45f4-8395-ca40c02f6cb4	550e8400-e29b-41d4-a716-446655440004	Emergency Contact	+1234567894	O+	\N	\N	\N	\N	en
\.


--
-- Data for Name: patient_vitals_tracking; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.patient_vitals_tracking (id, patient_id, recorded_at, weight, height, blood_pressure_systolic, blood_pressure_diastolic, heart_rate, temperature, blood_sugar, notes) FROM stdin;
\.


--
-- Data for Name: payment_methods; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.payment_methods (id, user_id, method_type, provider, token, is_default, is_active, created_at) FROM stdin;
\.


--
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.payments (id, appointment_id, patient_id, amount, currency, payment_gateway, razorpay_order_id, razorpay_payment_id, razorpay_signature, status, payment_date, refund_amount, refund_date) FROM stdin;
\.


--
-- Data for Name: pharmacy_orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pharmacy_orders (id, patient_id, pharmacy_partner_id, prescription_id, order_date, status, total_amount, delivery_address) FROM stdin;
\.


--
-- Data for Name: pharmacy_partners; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pharmacy_partners (id, name, address, phone, email, license_number, is_active, delivery_available) FROM stdin;
\.


--
-- Data for Name: prescription_medicines; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.prescription_medicines (id, prescription_id, medicine_name, dosage, frequency, duration, instructions, generic_alternative) FROM stdin;
\.


--
-- Data for Name: prescriptions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.prescriptions (id, visit_id, doctor_id, patient_id, prescription_date, status, notes) FROM stdin;
\.


--
-- Data for Name: refunds; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.refunds (id, payment_id, amount, reason, status, requested_date, processed_date, refund_method) FROM stdin;
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles (id, name, description, permissions) FROM stdin;
22d83a0b-e41c-4c8e-b02a-2d483715eb4a	patient	Patients who can book appointments, consult with doctors, and manage their health records	{"chat": ["create", "read"], "profile": ["read", "update"], "feedback": ["create", "read"], "payments": ["create", "read"], "pharmacy": ["order", "track"], "ai_assistant": ["use"], "appointments": ["create", "read", "update", "cancel"], "lab_bookings": ["create", "read", "track"], "telemedicine": ["join", "participate"], "medical_records": ["read", "upload", "share"]}
59bf1d3a-3a2e-4576-b609-b4ea897dcfe7	doctor	Medical practitioners who provide consultations and manage patient care	{"chat": ["create", "read"], "profile": ["read", "update"], "feedback": ["read"], "patients": ["read", "search"], "schedule": ["read", "update"], "lab_reports": ["read", "create"], "appointments": ["read", "update", "confirm", "complete"], "telemedicine": ["create", "join", "manage"], "prescriptions": ["create", "read", "update"], "medical_records": ["read", "create", "update"], "consultation_notes": ["create", "read", "update"]}
d4cee4f3-c338-4af6-a3eb-da516697da58	clinic_admin	Administrators who manage clinic operations, doctors, and appointments	{"staff": ["manage"], "clinic": ["read", "update", "manage"], "doctors": ["read", "assign", "manage"], "profile": ["read", "update"], "reports": ["generate", "read"], "patients": ["read", "search"], "schedule": ["read", "update", "manage"], "services": ["manage"], "analytics": ["read"], "appointments": ["read", "manage", "reschedule"]}
1fe269ab-7703-4cfc-ab35-83e4cee3a4ea	sys_admin	System administrators with full access to manage the entire platform	{"audit": ["read", "manage"], "users": ["create", "read", "update", "delete", "suspend"], "backup": ["create", "restore"], "system": ["configure", "maintain"], "clinics": ["approve", "manage", "verify"], "content": ["manage", "moderate"], "doctors": ["verify", "manage", "approve"], "reports": ["generate", "read", "export"], "feedback": ["moderate", "manage"], "payments": ["read", "manage", "refund"], "analytics": ["read", "export"], "appointments": ["read", "manage", "override"], "notifications": ["manage", "broadcast"]}
\.


--
-- Data for Name: security_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.security_logs (id, user_id, event_type, details, risk_level, ip_address, user_agent, "timestamp") FROM stdin;
\.


--
-- Data for Name: sessions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sessions (id, user_id, session_token, device_info, ip_address, last_activity, expires_at, created_at) FROM stdin;
\.


--
-- Data for Name: sms_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sms_logs (id, user_id, phone_number, message, status, sent_at, delivery_status, provider_response) FROM stdin;
\.


--
-- Data for Name: specialties; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.specialties (id, name, description, category) FROM stdin;
d027f7a2-8461-47ce-9051-a46b73a4807c	Cardiology	Heart and cardiovascular system specialists	Medical
98789c49-42ac-48b8-91c0-43e131de7d48	Dermatology	Skin, hair, and nail specialists	Medical
f61c3e2c-2155-4dab-8106-8f5282fba70b	Endocrinology	Hormone and metabolic disorder specialists	Medical
06ba9b17-5d4c-404c-9894-25fb2e678890	Gastroenterology	Digestive system specialists	Medical
89b8e956-21a6-4b95-9dd5-482088707f12	Neurology	Nervous system specialists	Medical
756382b4-a431-4ea3-979d-2622607a0498	Oncology	Cancer treatment specialists	Medical
4c52daca-72e8-4c93-bcad-732753967383	Orthopedics	Bone and joint specialists	Surgical
57257df7-1d13-4322-a776-0ae354b1b2f5	Pediatrics	Children healthcare specialists	Medical
dae4322a-a967-4a24-a5a5-15ce2d7b4cca	Psychiatry	Mental health specialists	Mental Health
b6447af6-0984-441d-8514-04f940b0e8b6	Gynecology	Women reproductive health specialists	Medical
8a314cbd-d316-42c4-9411-939bfe02420f	Urology	Urinary system specialists	Surgical
a8b52927-22ae-4dc5-bdda-e14ea4292977	Ophthalmology	Eye care specialists	Medical
0369d3ef-d035-4146-a347-e3826db4f4ba	ENT	Ear, Nose, and Throat specialists	Medical
75aea244-b28c-4707-84a0-eb77a1d791b9	General Medicine	Primary care physicians	Medical
357475ee-5e65-4b1b-bd3a-4b93dc44941a	Emergency Medicine	Emergency and critical care	Critical Care
\.


--
-- Data for Name: symptom_reports; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.symptom_reports (id, patient_id, symptoms, severity, duration, body_parts, additional_info, ai_assessment, created_at) FROM stdin;
\.


--
-- Data for Name: system_announcements; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.system_announcements (id, title, message, type, target_roles, start_date, end_date, is_active, created_by) FROM stdin;
9d783be9-13aa-40ac-9688-a9b9e4d9a673	Welcome to HealthPlatform	Welcome to our comprehensive healthcare platform. Book appointments, consult with doctors, and manage your health records all in one place.	welcome	{patient,doctor,clinic_admin}	2025-07-23 17:22:23.224188+05:30	2025-08-22 17:22:23.224188+05:30	t	\N
\.


--
-- Data for Name: system_metrics; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.system_metrics (id, metric_name, value, recorded_at, category) FROM stdin;
\.


--
-- Data for Name: telemedicine_sessions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.telemedicine_sessions (id, appointment_id, room_id, session_token, start_time, end_time, status, recording_url, connection_quality, participants_info) FROM stdin;
\.


--
-- Data for Name: translations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.translations (id, locale, translation_key, translation_value, context, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: user_devices; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_devices (id, user_id, device_id, device_type, push_token, is_active, last_seen) FROM stdin;
\.


--
-- Data for Name: user_locale_preferences; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_locale_preferences (user_id, locale_id, date_format, time_format, currency_display) FROM stdin;
\.


--
-- Data for Name: user_roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_roles (user_id, role_id, assigned_at, assigned_by) FROM stdin;
550e8400-e29b-41d4-a716-446655440001	1fe269ab-7703-4cfc-ab35-83e4cee3a4ea	2025-07-23 17:12:13.092195+05:30	\N
550e8400-e29b-41d4-a716-446655440002	59bf1d3a-3a2e-4576-b609-b4ea897dcfe7	2025-07-23 17:12:13.092195+05:30	550e8400-e29b-41d4-a716-446655440001
550e8400-e29b-41d4-a716-446655440003	d4cee4f3-c338-4af6-a3eb-da516697da58	2025-07-23 17:12:13.092195+05:30	550e8400-e29b-41d4-a716-446655440001
550e8400-e29b-41d4-a716-446655440004	22d83a0b-e41c-4c8e-b02a-2d483715eb4a	2025-07-23 17:12:13.092195+05:30	\N
550e8400-e29b-41d4-a716-446655440005	59bf1d3a-3a2e-4576-b609-b4ea897dcfe7	2025-07-23 17:12:13.092195+05:30	550e8400-e29b-41d4-a716-446655440001
550e8400-e29b-41d4-a716-446655440005	d4cee4f3-c338-4af6-a3eb-da516697da58	2025-07-23 17:12:13.092195+05:30	550e8400-e29b-41d4-a716-446655440001
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, email, phone, password_hash, full_name, date_of_birth, gender, profile_picture, language_preference, is_active, is_verified, created_at, updated_at) FROM stdin;
550e8400-e29b-41d4-a716-446655440001	admin@healthplatform.com	+1234567890	$2b$12$LQv3c1yqBTLhL5n7HdnTGuj/4aw7TW2zF8ql3KGq8QHwFU7D9cjIK	System Administrator	\N	\N	\N	\N	t	t	2025-07-23 17:12:13.092195+05:30	2025-07-23 17:12:13.092195+05:30
550e8400-e29b-41d4-a716-446655440002	dr.smith@healthplatform.com	+1234567891	$2b$12$LQv3c1yqBTLhL5n7HdnTGuj/4aw7TW2zF8ql3KGq8QHwFU7D9cjIK	Dr. John Smith	1980-05-15	Male	\N	\N	t	t	2025-07-23 17:12:13.092195+05:30	2025-07-23 17:12:13.092195+05:30
550e8400-e29b-41d4-a716-446655440003	clinic.admin@healthcenter.com	+1234567892	$2b$12$LQv3c1yqBTLhL5n7HdnTGuj/4aw7TW2zF8ql3KGq8QHwFU7D9cjIK	Jane Clinic Admin	1985-08-20	Female	\N	\N	t	t	2025-07-23 17:12:13.092195+05:30	2025-07-23 17:12:13.092195+05:30
550e8400-e29b-41d4-a716-446655440004	patient@email.com	+1234567893	$2b$12$LQv3c1yqBTLhL5n7HdnTGuj/4aw7TW2zF8ql3KGq8QHwFU7D9cjIK	John Patient	1990-03-10	Male	\N	\N	t	t	2025-07-23 17:12:13.092195+05:30	2025-07-23 17:12:13.092195+05:30
550e8400-e29b-41d4-a716-446655440005	dr.admin@clinic.com	+1234567895	$2b$12$LQv3c1yqBTLhL5n7HdnTGuj/4aw7TW2zF8ql3KGq8QHwFU7D9cjIK	Dr. Admin Multi Role	1975-12-01	Female	\N	\N	t	t	2025-07-23 17:12:13.092195+05:30	2025-07-23 17:12:13.092195+05:30
\.


--
-- Data for Name: vital_signs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vital_signs (id, patient_id, visit_id, recorded_date, blood_pressure_systolic, blood_pressure_diastolic, heart_rate, temperature, weight, height, bmi, oxygen_saturation) FROM stdin;
\.


--
-- Data for Name: wallet_transactions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.wallet_transactions (id, user_id, transaction_type, amount, balance_before, balance_after, reference_id, description, created_at) FROM stdin;
\.


--
-- Name: admin_logs admin_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admin_logs
    ADD CONSTRAINT admin_logs_pkey PRIMARY KEY (id);


--
-- Name: ai_chat_sessions ai_chat_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_chat_sessions
    ADD CONSTRAINT ai_chat_sessions_pkey PRIMARY KEY (id);


--
-- Name: ai_recommendations ai_recommendations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_recommendations
    ADD CONSTRAINT ai_recommendations_pkey PRIMARY KEY (id);


--
-- Name: allergies allergies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.allergies
    ADD CONSTRAINT allergies_pkey PRIMARY KEY (id);


--
-- Name: analytics_events analytics_events_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.analytics_events
    ADD CONSTRAINT analytics_events_pkey PRIMARY KEY (id);


--
-- Name: appointment_feedback appointment_feedback_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appointment_feedback
    ADD CONSTRAINT appointment_feedback_pkey PRIMARY KEY (id);


--
-- Name: appointment_reminders appointment_reminders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appointment_reminders
    ADD CONSTRAINT appointment_reminders_pkey PRIMARY KEY (id);


--
-- Name: appointment_reschedule_history appointment_reschedule_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appointment_reschedule_history
    ADD CONSTRAINT appointment_reschedule_history_pkey PRIMARY KEY (id);


--
-- Name: appointment_slots appointment_slots_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appointment_slots
    ADD CONSTRAINT appointment_slots_pkey PRIMARY KEY (id);


--
-- Name: appointment_statuses appointment_statuses_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appointment_statuses
    ADD CONSTRAINT appointment_statuses_name_key UNIQUE (name);


--
-- Name: appointment_statuses appointment_statuses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appointment_statuses
    ADD CONSTRAINT appointment_statuses_pkey PRIMARY KEY (id);


--
-- Name: appointments appointments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appointments
    ADD CONSTRAINT appointments_pkey PRIMARY KEY (id);


--
-- Name: audit_logs audit_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (id);


--
-- Name: auth_tokens auth_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_tokens
    ADD CONSTRAINT auth_tokens_pkey PRIMARY KEY (id);


--
-- Name: backup_logs backup_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.backup_logs
    ADD CONSTRAINT backup_logs_pkey PRIMARY KEY (id);


--
-- Name: call_logs call_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.call_logs
    ADD CONSTRAINT call_logs_pkey PRIMARY KEY (id);


--
-- Name: certifications certifications_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.certifications
    ADD CONSTRAINT certifications_pkey PRIMARY KEY (id);


--
-- Name: chat_conversations chat_conversations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_conversations
    ADD CONSTRAINT chat_conversations_pkey PRIMARY KEY (id);


--
-- Name: chat_messages chat_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_messages
    ADD CONSTRAINT chat_messages_pkey PRIMARY KEY (id);


--
-- Name: clinic_admin_profiles clinic_admin_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clinic_admin_profiles
    ADD CONSTRAINT clinic_admin_profiles_pkey PRIMARY KEY (id);


--
-- Name: clinic_admin_profiles clinic_admin_profiles_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clinic_admin_profiles
    ADD CONSTRAINT clinic_admin_profiles_user_id_key UNIQUE (user_id);


--
-- Name: clinic_doctors clinic_doctors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clinic_doctors
    ADD CONSTRAINT clinic_doctors_pkey PRIMARY KEY (id);


--
-- Name: clinic_images clinic_images_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clinic_images
    ADD CONSTRAINT clinic_images_pkey PRIMARY KEY (id);


--
-- Name: clinic_services clinic_services_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clinic_services
    ADD CONSTRAINT clinic_services_pkey PRIMARY KEY (id);


--
-- Name: clinics clinics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clinics
    ADD CONSTRAINT clinics_pkey PRIMARY KEY (id);


--
-- Name: consultation_notes consultation_notes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.consultation_notes
    ADD CONSTRAINT consultation_notes_pkey PRIMARY KEY (id);


--
-- Name: doctor_availability doctor_availability_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctor_availability
    ADD CONSTRAINT doctor_availability_pkey PRIMARY KEY (id);


--
-- Name: doctor_languages doctor_languages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctor_languages
    ADD CONSTRAINT doctor_languages_pkey PRIMARY KEY (doctor_id, language_id);


--
-- Name: doctor_profiles doctor_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctor_profiles
    ADD CONSTRAINT doctor_profiles_pkey PRIMARY KEY (id);


--
-- Name: doctor_profiles doctor_profiles_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctor_profiles
    ADD CONSTRAINT doctor_profiles_user_id_key UNIQUE (user_id);


--
-- Name: doctor_ratings doctor_ratings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctor_ratings
    ADD CONSTRAINT doctor_ratings_pkey PRIMARY KEY (id);


--
-- Name: doctor_schedules doctor_schedules_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctor_schedules
    ADD CONSTRAINT doctor_schedules_pkey PRIMARY KEY (id);


--
-- Name: doctor_specialties doctor_specialties_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctor_specialties
    ADD CONSTRAINT doctor_specialties_pkey PRIMARY KEY (doctor_id, specialty_id);


--
-- Name: educations educations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.educations
    ADD CONSTRAINT educations_pkey PRIMARY KEY (id);


--
-- Name: email_logs email_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.email_logs
    ADD CONSTRAINT email_logs_pkey PRIMARY KEY (id);


--
-- Name: emergency_contacts emergency_contacts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.emergency_contacts
    ADD CONSTRAINT emergency_contacts_pkey PRIMARY KEY (id);


--
-- Name: feedback_reports feedback_reports_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.feedback_reports
    ADD CONSTRAINT feedback_reports_pkey PRIMARY KEY (id);


--
-- Name: file_uploads file_uploads_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.file_uploads
    ADD CONSTRAINT file_uploads_pkey PRIMARY KEY (id);


--
-- Name: health_tips health_tips_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.health_tips
    ADD CONSTRAINT health_tips_pkey PRIMARY KEY (id);


--
-- Name: insurance_claims insurance_claims_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.insurance_claims
    ADD CONSTRAINT insurance_claims_pkey PRIMARY KEY (id);


--
-- Name: invoice_items invoice_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoice_items
    ADD CONSTRAINT invoice_items_pkey PRIMARY KEY (id);


--
-- Name: invoices invoices_invoice_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT invoices_invoice_number_key UNIQUE (invoice_number);


--
-- Name: invoices invoices_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT invoices_pkey PRIMARY KEY (id);


--
-- Name: lab_bookings lab_bookings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lab_bookings
    ADD CONSTRAINT lab_bookings_pkey PRIMARY KEY (id);


--
-- Name: lab_partners lab_partners_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lab_partners
    ADD CONSTRAINT lab_partners_pkey PRIMARY KEY (id);


--
-- Name: lab_reports lab_reports_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lab_reports
    ADD CONSTRAINT lab_reports_pkey PRIMARY KEY (id);


--
-- Name: lab_results lab_results_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lab_results
    ADD CONSTRAINT lab_results_pkey PRIMARY KEY (id);


--
-- Name: lab_tests lab_tests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lab_tests
    ADD CONSTRAINT lab_tests_pkey PRIMARY KEY (id);


--
-- Name: languages languages_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.languages
    ADD CONSTRAINT languages_code_key UNIQUE (code);


--
-- Name: languages languages_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.languages
    ADD CONSTRAINT languages_name_key UNIQUE (name);


--
-- Name: languages languages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.languages
    ADD CONSTRAINT languages_pkey PRIMARY KEY (id);


--
-- Name: locales locales_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locales
    ADD CONSTRAINT locales_code_key UNIQUE (code);


--
-- Name: locales locales_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locales
    ADD CONSTRAINT locales_pkey PRIMARY KEY (id);


--
-- Name: medical_documents medical_documents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medical_documents
    ADD CONSTRAINT medical_documents_pkey PRIMARY KEY (id);


--
-- Name: medical_history medical_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medical_history
    ADD CONSTRAINT medical_history_pkey PRIMARY KEY (id);


--
-- Name: medical_visits medical_visits_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medical_visits
    ADD CONSTRAINT medical_visits_pkey PRIMARY KEY (id);


--
-- Name: medicine_reminders medicine_reminders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medicine_reminders
    ADD CONSTRAINT medicine_reminders_pkey PRIMARY KEY (id);


--
-- Name: medicines medicines_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medicines
    ADD CONSTRAINT medicines_pkey PRIMARY KEY (id);


--
-- Name: message_attachments message_attachments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message_attachments
    ADD CONSTRAINT message_attachments_pkey PRIMARY KEY (id);


--
-- Name: notification_logs notification_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification_logs
    ADD CONSTRAINT notification_logs_pkey PRIMARY KEY (id);


--
-- Name: notification_preferences notification_preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification_preferences
    ADD CONSTRAINT notification_preferences_pkey PRIMARY KEY (id);


--
-- Name: notification_templates notification_templates_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification_templates
    ADD CONSTRAINT notification_templates_name_key UNIQUE (name);


--
-- Name: notification_templates notification_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification_templates
    ADD CONSTRAINT notification_templates_pkey PRIMARY KEY (id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- Name: otp_codes otp_codes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.otp_codes
    ADD CONSTRAINT otp_codes_pkey PRIMARY KEY (id);


--
-- Name: patient_favorites patient_favorites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patient_favorites
    ADD CONSTRAINT patient_favorites_pkey PRIMARY KEY (id);


--
-- Name: patient_profiles patient_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patient_profiles
    ADD CONSTRAINT patient_profiles_pkey PRIMARY KEY (id);


--
-- Name: patient_profiles patient_profiles_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patient_profiles
    ADD CONSTRAINT patient_profiles_user_id_key UNIQUE (user_id);


--
-- Name: patient_vitals_tracking patient_vitals_tracking_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patient_vitals_tracking
    ADD CONSTRAINT patient_vitals_tracking_pkey PRIMARY KEY (id);


--
-- Name: payment_methods payment_methods_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payment_methods
    ADD CONSTRAINT payment_methods_pkey PRIMARY KEY (id);


--
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (id);


--
-- Name: payments payments_razorpay_order_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_razorpay_order_id_key UNIQUE (razorpay_order_id);


--
-- Name: payments payments_razorpay_payment_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_razorpay_payment_id_key UNIQUE (razorpay_payment_id);


--
-- Name: pharmacy_orders pharmacy_orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pharmacy_orders
    ADD CONSTRAINT pharmacy_orders_pkey PRIMARY KEY (id);


--
-- Name: pharmacy_partners pharmacy_partners_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pharmacy_partners
    ADD CONSTRAINT pharmacy_partners_pkey PRIMARY KEY (id);


--
-- Name: prescription_medicines prescription_medicines_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prescription_medicines
    ADD CONSTRAINT prescription_medicines_pkey PRIMARY KEY (id);


--
-- Name: prescriptions prescriptions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prescriptions
    ADD CONSTRAINT prescriptions_pkey PRIMARY KEY (id);


--
-- Name: refunds refunds_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.refunds
    ADD CONSTRAINT refunds_pkey PRIMARY KEY (id);


--
-- Name: roles roles_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: security_logs security_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.security_logs
    ADD CONSTRAINT security_logs_pkey PRIMARY KEY (id);


--
-- Name: sessions sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (id);


--
-- Name: sms_logs sms_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sms_logs
    ADD CONSTRAINT sms_logs_pkey PRIMARY KEY (id);


--
-- Name: specialties specialties_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.specialties
    ADD CONSTRAINT specialties_name_key UNIQUE (name);


--
-- Name: specialties specialties_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.specialties
    ADD CONSTRAINT specialties_pkey PRIMARY KEY (id);


--
-- Name: symptom_reports symptom_reports_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.symptom_reports
    ADD CONSTRAINT symptom_reports_pkey PRIMARY KEY (id);


--
-- Name: system_announcements system_announcements_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.system_announcements
    ADD CONSTRAINT system_announcements_pkey PRIMARY KEY (id);


--
-- Name: system_metrics system_metrics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.system_metrics
    ADD CONSTRAINT system_metrics_pkey PRIMARY KEY (id);


--
-- Name: telemedicine_sessions telemedicine_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.telemedicine_sessions
    ADD CONSTRAINT telemedicine_sessions_pkey PRIMARY KEY (id);


--
-- Name: translations translations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.translations
    ADD CONSTRAINT translations_pkey PRIMARY KEY (id);


--
-- Name: user_devices user_devices_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_devices
    ADD CONSTRAINT user_devices_pkey PRIMARY KEY (id);


--
-- Name: user_locale_preferences user_locale_preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_locale_preferences
    ADD CONSTRAINT user_locale_preferences_pkey PRIMARY KEY (user_id, locale_id);


--
-- Name: user_roles user_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_pkey PRIMARY KEY (user_id, role_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_phone_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_phone_key UNIQUE (phone);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: vital_signs vital_signs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vital_signs
    ADD CONSTRAINT vital_signs_pkey PRIMARY KEY (id);


--
-- Name: wallet_transactions wallet_transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wallet_transactions
    ADD CONSTRAINT wallet_transactions_pkey PRIMARY KEY (id);


--
-- Name: idx_analytics_events_user; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_analytics_events_user ON public.analytics_events USING btree (user_id, "timestamp");


--
-- Name: idx_appointments_doctor_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_appointments_doctor_date ON public.appointments USING btree (doctor_id, appointment_date);


--
-- Name: idx_appointments_patient_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_appointments_patient_date ON public.appointments USING btree (patient_id, appointment_date);


--
-- Name: idx_audit_logs_user; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_audit_logs_user ON public.audit_logs USING btree (user_id, "timestamp");


--
-- Name: idx_chat_messages_conversation; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_chat_messages_conversation ON public.chat_messages USING btree (conversation_id, sent_at);


--
-- Name: idx_clinics_location; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_clinics_location ON public.clinics USING btree (city, state);


--
-- Name: idx_doctors_specialty; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_doctors_specialty ON public.doctor_specialties USING btree (specialty_id);


--
-- Name: idx_feedback_doctor; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_feedback_doctor ON public.appointment_feedback USING btree (doctor_id, submitted_at);


--
-- Name: idx_medical_documents_patient; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_medical_documents_patient ON public.medical_documents USING btree (patient_id, document_type);


--
-- Name: idx_notifications_user_unread; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_notifications_user_unread ON public.notifications USING btree (user_id, read_at);


--
-- Name: idx_payments_razorpay_order; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_payments_razorpay_order ON public.payments USING btree (razorpay_order_id);


--
-- Name: idx_payments_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_payments_status ON public.payments USING btree (status, payment_date);


--
-- Name: idx_system_metrics_category; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_system_metrics_category ON public.system_metrics USING btree (category, recorded_at);


--
-- Name: idx_telemedicine_sessions_appointment; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_telemedicine_sessions_appointment ON public.telemedicine_sessions USING btree (appointment_id);


--
-- Name: idx_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_users_email ON public.users USING btree (email);


--
-- Name: idx_users_phone; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_users_phone ON public.users USING btree (phone);


--
-- Name: admin_logs admin_logs_admin_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admin_logs
    ADD CONSTRAINT admin_logs_admin_id_fkey FOREIGN KEY (admin_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: ai_chat_sessions ai_chat_sessions_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_chat_sessions
    ADD CONSTRAINT ai_chat_sessions_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient_profiles(user_id) ON DELETE CASCADE;


--
-- Name: ai_recommendations ai_recommendations_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_recommendations
    ADD CONSTRAINT ai_recommendations_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.ai_chat_sessions(id) ON DELETE CASCADE;


--
-- Name: allergies allergies_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.allergies
    ADD CONSTRAINT allergies_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient_profiles(user_id) ON DELETE CASCADE;


--
-- Name: analytics_events analytics_events_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.analytics_events
    ADD CONSTRAINT analytics_events_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: appointment_feedback appointment_feedback_appointment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appointment_feedback
    ADD CONSTRAINT appointment_feedback_appointment_id_fkey FOREIGN KEY (appointment_id) REFERENCES public.appointments(id) ON DELETE CASCADE;


--
-- Name: appointment_feedback appointment_feedback_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appointment_feedback
    ADD CONSTRAINT appointment_feedback_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor_profiles(user_id) ON DELETE CASCADE;


--
-- Name: appointment_feedback appointment_feedback_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appointment_feedback
    ADD CONSTRAINT appointment_feedback_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient_profiles(user_id) ON DELETE CASCADE;


--
-- Name: appointment_reminders appointment_reminders_appointment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appointment_reminders
    ADD CONSTRAINT appointment_reminders_appointment_id_fkey FOREIGN KEY (appointment_id) REFERENCES public.appointments(id) ON DELETE CASCADE;


--
-- Name: appointment_reschedule_history appointment_reschedule_history_appointment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appointment_reschedule_history
    ADD CONSTRAINT appointment_reschedule_history_appointment_id_fkey FOREIGN KEY (appointment_id) REFERENCES public.appointments(id) ON DELETE CASCADE;


--
-- Name: appointment_reschedule_history appointment_reschedule_history_rescheduled_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appointment_reschedule_history
    ADD CONSTRAINT appointment_reschedule_history_rescheduled_by_fkey FOREIGN KEY (rescheduled_by) REFERENCES public.users(id);


--
-- Name: appointment_slots appointment_slots_clinic_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appointment_slots
    ADD CONSTRAINT appointment_slots_clinic_id_fkey FOREIGN KEY (clinic_id) REFERENCES public.clinics(id) ON DELETE SET NULL;


--
-- Name: appointment_slots appointment_slots_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appointment_slots
    ADD CONSTRAINT appointment_slots_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor_profiles(user_id) ON DELETE CASCADE;


--
-- Name: appointments appointments_clinic_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appointments
    ADD CONSTRAINT appointments_clinic_id_fkey FOREIGN KEY (clinic_id) REFERENCES public.clinics(id) ON DELETE SET NULL;


--
-- Name: appointments appointments_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appointments
    ADD CONSTRAINT appointments_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor_profiles(user_id) ON DELETE CASCADE;


--
-- Name: appointments appointments_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appointments
    ADD CONSTRAINT appointments_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient_profiles(user_id) ON DELETE CASCADE;


--
-- Name: audit_logs audit_logs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: auth_tokens auth_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_tokens
    ADD CONSTRAINT auth_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: call_logs call_logs_participant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.call_logs
    ADD CONSTRAINT call_logs_participant_id_fkey FOREIGN KEY (participant_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: call_logs call_logs_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.call_logs
    ADD CONSTRAINT call_logs_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.telemedicine_sessions(id) ON DELETE CASCADE;


--
-- Name: certifications certifications_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.certifications
    ADD CONSTRAINT certifications_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor_profiles(user_id) ON DELETE CASCADE;


--
-- Name: chat_conversations chat_conversations_appointment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_conversations
    ADD CONSTRAINT chat_conversations_appointment_id_fkey FOREIGN KEY (appointment_id) REFERENCES public.appointments(id) ON DELETE CASCADE;


--
-- Name: chat_conversations chat_conversations_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_conversations
    ADD CONSTRAINT chat_conversations_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor_profiles(user_id) ON DELETE CASCADE;


--
-- Name: chat_conversations chat_conversations_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_conversations
    ADD CONSTRAINT chat_conversations_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient_profiles(user_id) ON DELETE CASCADE;


--
-- Name: chat_messages chat_messages_conversation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_messages
    ADD CONSTRAINT chat_messages_conversation_id_fkey FOREIGN KEY (conversation_id) REFERENCES public.chat_conversations(id) ON DELETE CASCADE;


--
-- Name: chat_messages chat_messages_sender_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chat_messages
    ADD CONSTRAINT chat_messages_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: clinic_admin_profiles clinic_admin_profiles_clinic_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clinic_admin_profiles
    ADD CONSTRAINT clinic_admin_profiles_clinic_id_fkey FOREIGN KEY (clinic_id) REFERENCES public.clinics(id) ON DELETE SET NULL;


--
-- Name: clinic_admin_profiles clinic_admin_profiles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clinic_admin_profiles
    ADD CONSTRAINT clinic_admin_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: clinic_doctors clinic_doctors_clinic_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clinic_doctors
    ADD CONSTRAINT clinic_doctors_clinic_id_fkey FOREIGN KEY (clinic_id) REFERENCES public.clinics(id) ON DELETE CASCADE;


--
-- Name: clinic_doctors clinic_doctors_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clinic_doctors
    ADD CONSTRAINT clinic_doctors_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor_profiles(user_id) ON DELETE CASCADE;


--
-- Name: clinic_images clinic_images_clinic_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clinic_images
    ADD CONSTRAINT clinic_images_clinic_id_fkey FOREIGN KEY (clinic_id) REFERENCES public.clinics(id) ON DELETE CASCADE;


--
-- Name: clinic_services clinic_services_clinic_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clinic_services
    ADD CONSTRAINT clinic_services_clinic_id_fkey FOREIGN KEY (clinic_id) REFERENCES public.clinics(id) ON DELETE CASCADE;


--
-- Name: consultation_notes consultation_notes_appointment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.consultation_notes
    ADD CONSTRAINT consultation_notes_appointment_id_fkey FOREIGN KEY (appointment_id) REFERENCES public.appointments(id) ON DELETE CASCADE;


--
-- Name: consultation_notes consultation_notes_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.consultation_notes
    ADD CONSTRAINT consultation_notes_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor_profiles(user_id) ON DELETE CASCADE;


--
-- Name: doctor_availability doctor_availability_clinic_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctor_availability
    ADD CONSTRAINT doctor_availability_clinic_id_fkey FOREIGN KEY (clinic_id) REFERENCES public.clinics(id) ON DELETE SET NULL;


--
-- Name: doctor_availability doctor_availability_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctor_availability
    ADD CONSTRAINT doctor_availability_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor_profiles(user_id) ON DELETE CASCADE;


--
-- Name: doctor_languages doctor_languages_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctor_languages
    ADD CONSTRAINT doctor_languages_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor_profiles(user_id) ON DELETE CASCADE;


--
-- Name: doctor_languages doctor_languages_language_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctor_languages
    ADD CONSTRAINT doctor_languages_language_id_fkey FOREIGN KEY (language_id) REFERENCES public.languages(id) ON DELETE CASCADE;


--
-- Name: doctor_profiles doctor_profiles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctor_profiles
    ADD CONSTRAINT doctor_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: doctor_ratings doctor_ratings_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctor_ratings
    ADD CONSTRAINT doctor_ratings_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor_profiles(user_id) ON DELETE CASCADE;


--
-- Name: doctor_schedules doctor_schedules_clinic_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctor_schedules
    ADD CONSTRAINT doctor_schedules_clinic_id_fkey FOREIGN KEY (clinic_id) REFERENCES public.clinics(id) ON DELETE CASCADE;


--
-- Name: doctor_schedules doctor_schedules_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctor_schedules
    ADD CONSTRAINT doctor_schedules_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor_profiles(user_id) ON DELETE CASCADE;


--
-- Name: doctor_specialties doctor_specialties_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctor_specialties
    ADD CONSTRAINT doctor_specialties_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor_profiles(user_id) ON DELETE CASCADE;


--
-- Name: doctor_specialties doctor_specialties_specialty_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctor_specialties
    ADD CONSTRAINT doctor_specialties_specialty_id_fkey FOREIGN KEY (specialty_id) REFERENCES public.specialties(id) ON DELETE CASCADE;


--
-- Name: educations educations_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.educations
    ADD CONSTRAINT educations_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor_profiles(user_id) ON DELETE CASCADE;


--
-- Name: email_logs email_logs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.email_logs
    ADD CONSTRAINT email_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: emergency_contacts emergency_contacts_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.emergency_contacts
    ADD CONSTRAINT emergency_contacts_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient_profiles(user_id) ON DELETE CASCADE;


--
-- Name: feedback_reports feedback_reports_feedback_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.feedback_reports
    ADD CONSTRAINT feedback_reports_feedback_id_fkey FOREIGN KEY (feedback_id) REFERENCES public.appointment_feedback(id) ON DELETE CASCADE;


--
-- Name: feedback_reports feedback_reports_reported_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.feedback_reports
    ADD CONSTRAINT feedback_reports_reported_by_fkey FOREIGN KEY (reported_by) REFERENCES public.users(id);


--
-- Name: file_uploads file_uploads_uploaded_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.file_uploads
    ADD CONSTRAINT file_uploads_uploaded_by_fkey FOREIGN KEY (uploaded_by) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: health_tips health_tips_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.health_tips
    ADD CONSTRAINT health_tips_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: insurance_claims insurance_claims_appointment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.insurance_claims
    ADD CONSTRAINT insurance_claims_appointment_id_fkey FOREIGN KEY (appointment_id) REFERENCES public.appointments(id) ON DELETE SET NULL;


--
-- Name: insurance_claims insurance_claims_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.insurance_claims
    ADD CONSTRAINT insurance_claims_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient_profiles(user_id) ON DELETE SET NULL;


--
-- Name: invoice_items invoice_items_invoice_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoice_items
    ADD CONSTRAINT invoice_items_invoice_id_fkey FOREIGN KEY (invoice_id) REFERENCES public.invoices(id) ON DELETE CASCADE;


--
-- Name: invoices invoices_appointment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT invoices_appointment_id_fkey FOREIGN KEY (appointment_id) REFERENCES public.appointments(id) ON DELETE SET NULL;


--
-- Name: invoices invoices_clinic_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT invoices_clinic_id_fkey FOREIGN KEY (clinic_id) REFERENCES public.clinics(id) ON DELETE SET NULL;


--
-- Name: invoices invoices_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT invoices_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor_profiles(user_id) ON DELETE SET NULL;


--
-- Name: invoices invoices_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoices
    ADD CONSTRAINT invoices_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient_profiles(user_id) ON DELETE SET NULL;


--
-- Name: lab_bookings lab_bookings_lab_partner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lab_bookings
    ADD CONSTRAINT lab_bookings_lab_partner_id_fkey FOREIGN KEY (lab_partner_id) REFERENCES public.lab_partners(id) ON DELETE CASCADE;


--
-- Name: lab_bookings lab_bookings_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lab_bookings
    ADD CONSTRAINT lab_bookings_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient_profiles(user_id) ON DELETE CASCADE;


--
-- Name: lab_reports lab_reports_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lab_reports
    ADD CONSTRAINT lab_reports_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor_profiles(user_id) ON DELETE SET NULL;


--
-- Name: lab_reports lab_reports_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lab_reports
    ADD CONSTRAINT lab_reports_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient_profiles(user_id) ON DELETE CASCADE;


--
-- Name: lab_results lab_results_booking_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lab_results
    ADD CONSTRAINT lab_results_booking_id_fkey FOREIGN KEY (booking_id) REFERENCES public.lab_bookings(id) ON DELETE CASCADE;


--
-- Name: lab_results lab_results_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lab_results
    ADD CONSTRAINT lab_results_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient_profiles(user_id) ON DELETE CASCADE;


--
-- Name: lab_results lab_results_test_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lab_results
    ADD CONSTRAINT lab_results_test_id_fkey FOREIGN KEY (test_id) REFERENCES public.lab_tests(id);


--
-- Name: lab_tests lab_tests_lab_partner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lab_tests
    ADD CONSTRAINT lab_tests_lab_partner_id_fkey FOREIGN KEY (lab_partner_id) REFERENCES public.lab_partners(id) ON DELETE CASCADE;


--
-- Name: medical_documents medical_documents_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medical_documents
    ADD CONSTRAINT medical_documents_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor_profiles(user_id) ON DELETE SET NULL;


--
-- Name: medical_documents medical_documents_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medical_documents
    ADD CONSTRAINT medical_documents_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient_profiles(user_id) ON DELETE CASCADE;


--
-- Name: medical_documents medical_documents_visit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medical_documents
    ADD CONSTRAINT medical_documents_visit_id_fkey FOREIGN KEY (visit_id) REFERENCES public.medical_visits(id) ON DELETE SET NULL;


--
-- Name: medical_history medical_history_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medical_history
    ADD CONSTRAINT medical_history_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient_profiles(user_id) ON DELETE CASCADE;


--
-- Name: medical_visits medical_visits_appointment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medical_visits
    ADD CONSTRAINT medical_visits_appointment_id_fkey FOREIGN KEY (appointment_id) REFERENCES public.appointments(id);


--
-- Name: medical_visits medical_visits_clinic_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medical_visits
    ADD CONSTRAINT medical_visits_clinic_id_fkey FOREIGN KEY (clinic_id) REFERENCES public.clinics(id) ON DELETE SET NULL;


--
-- Name: medical_visits medical_visits_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medical_visits
    ADD CONSTRAINT medical_visits_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor_profiles(user_id) ON DELETE CASCADE;


--
-- Name: medical_visits medical_visits_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medical_visits
    ADD CONSTRAINT medical_visits_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient_profiles(user_id) ON DELETE CASCADE;


--
-- Name: medicine_reminders medicine_reminders_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medicine_reminders
    ADD CONSTRAINT medicine_reminders_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient_profiles(user_id) ON DELETE CASCADE;


--
-- Name: message_attachments message_attachments_message_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message_attachments
    ADD CONSTRAINT message_attachments_message_id_fkey FOREIGN KEY (message_id) REFERENCES public.chat_messages(id) ON DELETE CASCADE;


--
-- Name: notification_logs notification_logs_notification_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification_logs
    ADD CONSTRAINT notification_logs_notification_id_fkey FOREIGN KEY (notification_id) REFERENCES public.notifications(id) ON DELETE CASCADE;


--
-- Name: notification_preferences notification_preferences_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification_preferences
    ADD CONSTRAINT notification_preferences_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: notifications notifications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: otp_codes otp_codes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.otp_codes
    ADD CONSTRAINT otp_codes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: patient_favorites patient_favorites_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patient_favorites
    ADD CONSTRAINT patient_favorites_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor_profiles(user_id) ON DELETE CASCADE;


--
-- Name: patient_favorites patient_favorites_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patient_favorites
    ADD CONSTRAINT patient_favorites_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient_profiles(user_id) ON DELETE CASCADE;


--
-- Name: patient_profiles patient_profiles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patient_profiles
    ADD CONSTRAINT patient_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: patient_vitals_tracking patient_vitals_tracking_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patient_vitals_tracking
    ADD CONSTRAINT patient_vitals_tracking_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient_profiles(user_id) ON DELETE CASCADE;


--
-- Name: payment_methods payment_methods_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payment_methods
    ADD CONSTRAINT payment_methods_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: payments payments_appointment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_appointment_id_fkey FOREIGN KEY (appointment_id) REFERENCES public.appointments(id) ON DELETE SET NULL;


--
-- Name: payments payments_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient_profiles(user_id) ON DELETE SET NULL;


--
-- Name: pharmacy_orders pharmacy_orders_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pharmacy_orders
    ADD CONSTRAINT pharmacy_orders_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient_profiles(user_id) ON DELETE CASCADE;


--
-- Name: pharmacy_orders pharmacy_orders_pharmacy_partner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pharmacy_orders
    ADD CONSTRAINT pharmacy_orders_pharmacy_partner_id_fkey FOREIGN KEY (pharmacy_partner_id) REFERENCES public.pharmacy_partners(id) ON DELETE CASCADE;


--
-- Name: pharmacy_orders pharmacy_orders_prescription_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pharmacy_orders
    ADD CONSTRAINT pharmacy_orders_prescription_id_fkey FOREIGN KEY (prescription_id) REFERENCES public.prescriptions(id);


--
-- Name: prescription_medicines prescription_medicines_prescription_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prescription_medicines
    ADD CONSTRAINT prescription_medicines_prescription_id_fkey FOREIGN KEY (prescription_id) REFERENCES public.prescriptions(id) ON DELETE CASCADE;


--
-- Name: prescriptions prescriptions_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prescriptions
    ADD CONSTRAINT prescriptions_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctor_profiles(user_id) ON DELETE CASCADE;


--
-- Name: prescriptions prescriptions_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prescriptions
    ADD CONSTRAINT prescriptions_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient_profiles(user_id) ON DELETE CASCADE;


--
-- Name: prescriptions prescriptions_visit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prescriptions
    ADD CONSTRAINT prescriptions_visit_id_fkey FOREIGN KEY (visit_id) REFERENCES public.medical_visits(id) ON DELETE CASCADE;


--
-- Name: refunds refunds_payment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.refunds
    ADD CONSTRAINT refunds_payment_id_fkey FOREIGN KEY (payment_id) REFERENCES public.payments(id) ON DELETE CASCADE;


--
-- Name: security_logs security_logs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.security_logs
    ADD CONSTRAINT security_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: sessions sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: sms_logs sms_logs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sms_logs
    ADD CONSTRAINT sms_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: symptom_reports symptom_reports_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.symptom_reports
    ADD CONSTRAINT symptom_reports_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient_profiles(user_id) ON DELETE CASCADE;


--
-- Name: system_announcements system_announcements_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.system_announcements
    ADD CONSTRAINT system_announcements_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: telemedicine_sessions telemedicine_sessions_appointment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.telemedicine_sessions
    ADD CONSTRAINT telemedicine_sessions_appointment_id_fkey FOREIGN KEY (appointment_id) REFERENCES public.appointments(id) ON DELETE CASCADE;


--
-- Name: user_devices user_devices_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_devices
    ADD CONSTRAINT user_devices_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: user_locale_preferences user_locale_preferences_locale_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_locale_preferences
    ADD CONSTRAINT user_locale_preferences_locale_id_fkey FOREIGN KEY (locale_id) REFERENCES public.locales(id) ON DELETE CASCADE;


--
-- Name: user_locale_preferences user_locale_preferences_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_locale_preferences
    ADD CONSTRAINT user_locale_preferences_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: user_roles user_roles_assigned_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_assigned_by_fkey FOREIGN KEY (assigned_by) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: user_roles user_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id) ON DELETE CASCADE;


--
-- Name: user_roles user_roles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: vital_signs vital_signs_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vital_signs
    ADD CONSTRAINT vital_signs_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patient_profiles(user_id) ON DELETE CASCADE;


--
-- Name: vital_signs vital_signs_visit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vital_signs
    ADD CONSTRAINT vital_signs_visit_id_fkey FOREIGN KEY (visit_id) REFERENCES public.medical_visits(id) ON DELETE CASCADE;


--
-- Name: wallet_transactions wallet_transactions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wallet_transactions
    ADD CONSTRAINT wallet_transactions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

