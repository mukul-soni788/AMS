# AMS (Appointment Management System)

AMS is a modern, full-stack healthcare appointment and profile management platform built with FastAPI and PostgreSQL. It supports multiple user roles (patients, doctors, clinic admins, system admins) and provides secure authentication, profile management, appointment scheduling, and more, with a responsive web UI.

---

## Features

- **User Registration & Login** (email/phone, password, OTP)
- **Role-based Access**: Patient, Doctor, Clinic Admin, System Admin
- **Profile Management**: Update personal, medical, and professional info
- **Avatar Upload**: Profile picture support
- **Medical History**: Patients can manage their medical records
- **Doctor Specialties**: Doctors can manage their specialties and professional info
- **Secure Authentication**: JWT tokens, password hashing (bcrypt)
- **Email OTP Verification**: For registration and login
- **Responsive UI**: Built with Tailwind CSS, supports desktop and mobile
- **Sample Data**: SQL scripts for roles, users, and profiles
- **Extensible**: Modular codebase for easy feature addition

---

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Frontend/UI**: Jinja2 templates, Tailwind CSS, Vanilla JS
- **Auth**: JWT, passlib, bcrypt
- **Other**: python-dotenv, python-multipart

---

## Project Structure

```
AMS/
  ├── app/
  │   ├── main.py            # FastAPI entrypoint
  │   ├── database.py        # DB connection
  │   ├── models/            # SQLAlchemy models
  │   ├── routes/            # API and view routes
  │   ├── schemas/           # (for Pydantic schemas)
  │   ├── static/            # Static files (logo, avatars, etc.)
  │   └── templates/         # Jinja2 HTML templates
  ├── ams_db.sql             # Sample DB schema & data
  ├── requirements.txt       # Python dependencies
  └── README.md
```

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repo-url>
cd AMS
```

### 2. Install Python Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the `app/` directory with the following:
```
DATABASE_URL=postgresql://<user>:<password>@localhost:5432/<dbname>
SMTP_HOST=<your-smtp-host>
SMTP_PORT=587
SMTP_USER=<your-smtp-user>
SMTP_PASS=<your-smtp-password>
FROM_EMAIL=<from-email-address>
```

### 4. Set Up the Database
- Ensure PostgreSQL is running.
- Create a database (e.g., `ams_db`).
- Run the schema and sample data:
  ```bash
  psql -U <user> -d <dbname> -f ams_db.sql
  ```

### 5. Run the Application
```bash
uvicorn app.main:app --reload
```
- Visit [http://localhost:8000](http://localhost:8000)

---

## Usage Overview

- **Register**: `/register` (choose Patient or Doctor)
- **Login**: `/login` (password or OTP)
- **Profile**: `/profile` (view/update info, upload avatar)
- **API Endpoints**: `/api/auth/*`, `/api/profile/*`

---

## UI Screenshots

- **Login**: Modern, responsive login form (email/phone, password, OTP)
- **Register**: Role selection, password strength, social login placeholders
- **Profile**: Tabbed interface for personal, medical, and professional info; avatar upload; medical history management
- **Sidebar & Navbar**: Dashboard navigation, notifications, user menu

---

## Database Schema

- See `ams_db.sql` for full schema and sample data
- Core tables: `users`, `roles`, `user_roles`, `doctor_profiles`, `patient_profiles`, `appointments`, etc.
- Sample roles: patient, doctor, clinic_admin, sys_admin

---

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `FROM_EMAIL`: For OTP email delivery

---

## Dependencies

- fastapi
- uvicorn
- sqlalchemy
- psycopg2-binary
- python-dotenv
- passlib
- python-multipart
- bcrypt==3.2.2

---

## License

MIT (or specify your license)

---

## Credits

- UI: Tailwind CSS, Jinja2
- Backend: FastAPI, SQLAlchemy
- Sample data: See `impp.txt` and `ams_db.sql`

---

## Contributing

Pull requests and issues are welcome!
