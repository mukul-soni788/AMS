#!/usr/bin/env python3
"""
Test script for appointment endpoints with doctor and clinic information
"""

import requests
import json
from datetime import datetime, date, time

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_appointments_endpoints():
    """Test the appointment endpoints"""
    
    print("Testing Appointment Endpoints with Doctor and Clinic Information")
    print("=" * 60)
    
    # Test data for creating an appointment
    appointment_data = {
        "appointment_date": "2024-12-25",
        "start_time": "10:00:00",
        "end_time": "11:00:00",
        "doctor_id": "550e8400-e29b-41d4-a716-446655440000",  # Example UUID
        "clinic_id": "550e8400-e29b-41d4-a716-446655440001",  # Example UUID
        "consultation_type": "general",
        "consultation_mode": "in-person",
        "reason_for_visit": "Regular checkup",
        "notes": "Patient requested morning appointment"
    }
    
    # Headers for authentication (you'll need to get a valid token)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 96BVSNctnD-adNn1cPLZVOIc9m5PIW_dOb9pfpVSR9o"  # Replace with actual token
    }
    
    try:
        # Initialize appointments variable
        appointments = None
        
        # Test 1: Get all appointments
        print("\n1. Testing GET /api/patients/appointments")
        response = requests.get(f"{BASE_URL}/api/patients/appointments", headers=headers)
        
        if response.status_code == 200:
            appointments = response.json()
            print("✅ Successfully retrieved appointments")
            print(f"   Past appointments: {len(appointments.get('past', []))}")
            print(f"   Upcoming appointments: {len(appointments.get('upcoming', []))}")
            
            # Check if appointments have doctor and clinic info
            if appointments.get('upcoming'):
                first_appointment = appointments['upcoming'][0]
                if 'doctor' in first_appointment and 'clinic' in first_appointment:
                    print("✅ Appointments include doctor and clinic information")
                    print(f"   Doctor: {first_appointment['doctor'].get('user', {}).get('full_name', 'N/A')}")
                    print(f"   Clinic: {first_appointment['clinic'].get('name', 'N/A')}")
                else:
                    print("❌ Appointments missing doctor or clinic information")
        else:
            print(f"❌ Failed to get appointments: {response.status_code}")
            print(f"   Response: {response.text}")
        
        # Test 2: Get specific appointment
        if appointments and appointments.get('upcoming'):
            appointment_id = appointments['upcoming'][0]['id']
            print(f"\n2. Testing GET /api/patients/appointments/{appointment_id}")
            
            response = requests.get(f"{BASE_URL}/api/patients/appointments/{appointment_id}", headers=headers)
            
            if response.status_code == 200:
                appointment = response.json()
                print("✅ Successfully retrieved specific appointment")
                if 'doctor' in appointment and 'clinic' in appointment:
                    print("✅ Appointment includes doctor and clinic information")
                else:
                    print("❌ Appointment missing doctor or clinic information")
            else:
                print(f"❌ Failed to get specific appointment: {response.status_code}")
        else:
            print("\n2. Skipping specific appointment test - no upcoming appointments available")
        
        # Test 3: Get appointment with full details
        if appointments and appointments.get('upcoming'):
            appointment_id = appointments['upcoming'][0]['id']
            print(f"\n3. Testing GET /api/patients/appointments/{appointment_id}/details")
            
            response = requests.get(f"{BASE_URL}/api/patients/appointments/{appointment_id}/details", headers=headers)
            
            if response.status_code == 200:
                appointment = response.json()
                print("✅ Successfully retrieved appointment with full details")
                
                # Check for additional details
                doctor = appointment.get('doctor', {})
                clinic = appointment.get('clinic', {})
                
                if doctor.get('doctor_specialties'):
                    print("✅ Doctor specialties included")
                if doctor.get('doctor_languages'):
                    print("✅ Doctor languages included")
                if doctor.get('doctor_ratings'):
                    print("✅ Doctor ratings included")
                if clinic.get('clinic_services'):
                    print("✅ Clinic services included")
            else:
                print(f"❌ Failed to get appointment details: {response.status_code}")
        else:
            print("\n3. Skipping appointment details test - no upcoming appointments available")
        
        # Test 4: Create new appointment
        print("\n4. Testing POST /api/patients/appointments")
        response = requests.post(f"{BASE_URL}/api/patients/appointments", 
                               json=appointment_data, headers=headers)
        
        if response.status_code == 200:
            new_appointment = response.json()
            print("✅ Successfully created new appointment")
            print(f"   Appointment ID: {new_appointment.get('id')}")
            print(f"   Date: {new_appointment.get('appointment_date')}")
            print(f"   Doctor ID: {new_appointment.get('doctor_id')}")
        else:
            print(f"❌ Failed to create appointment: {response.status_code}")
            print(f"   Response: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def print_expected_response_format():
    """Print the expected response format"""
    print("\nExpected Response Format:")
    print("=" * 40)
    
    expected_format = {
        "past": [
            {
                "id": "uuid",
                "appointment_date": "2024-01-15",
                "start_time": "10:00:00",
                "end_time": "11:00:00",
                "consultation_type": "general",
                "consultation_mode": "in-person",
                "status": "completed",
                "reason_for_visit": "Regular checkup",
                "notes": "Patient was healthy",
                "doctor": {
                    "id": "uuid",
                    "medical_license_number": "MD123456",
                    "years_experience": 10,
                    "consultation_fee": 100.0,
                    "specialization_primary": "Cardiology",
                    "user": {
                        "id": "uuid",
                        "full_name": "Dr. John Smith",
                        "email": "john.smith@example.com",
                        "phone": "+1234567890"
                    },
                    "doctor_specialties": [
                        {
                            "specialty": {
                                "id": "uuid",
                                "name": "Cardiology",
                                "description": "Heart and cardiovascular system"
                            }
                        }
                    ],
                    "doctor_languages": [
                        {
                            "language": {
                                "id": "uuid",
                                "name": "English",
                                "code": "en"
                            },
                            "proficiency_level": "Native"
                        }
                    ],
                    "doctor_ratings": [
                        {
                            "average_rating": 4.8,
                            "total_reviews": 150,
                            "communication_avg": 4.9,
                            "punctuality_avg": 4.7,
                            "expertise_avg": 4.8
                        }
                    ]
                },
                "clinic": {
                    "id": "uuid",
                    "name": "City Medical Center",
                    "address": "123 Main St",
                    "city": "New York",
                    "state": "NY",
                    "phone": "+1234567890",
                    "email": "info@citymedical.com",
                    "clinic_services": [
                        {
                            "id": "uuid",
                            "service_name": "General Consultation",
                            "description": "Basic health checkup",
                            "price": 100.0,
                            "duration_minutes": 60
                        }
                    ]
                }
            }
        ],
        "upcoming": []
    }
    
    print(json.dumps(expected_format, indent=2))

if __name__ == "__main__":
    print_expected_response_format()
    test_appointments_endpoints() 