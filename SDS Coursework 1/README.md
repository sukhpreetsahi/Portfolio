# Medical Centre Management System (MCMS)
## Project Overview

This project is a Medical Centre Management System (MCMS) developed in Python as part of coursework. The system is designed to manage medical records, patient appointments, and doctor assignments, focusing on an Administrator's role. It provides GUI (Tkinter) interfaces for user interaction.

The MCMS supports three types of users: Administrator, Doctor, and Patient. Below are the main features available for each user:

### Administrator
   - Login: Admin can securely log into the system.
   - Doctor Management: Register, view, update, and delete doctor profiles.
   - Patient Management: View patient records and assign patients to doctors.
   - Appointment Management: Approve patient appointment requests and manage doctor assignments.
   - Reports: Generate management reports on doctor availability, patient appointments, and illness types.
    
### Doctor
   - Login: Doctors can log in to view their patients' records and appointments.
   - Patient Records: View patient details and upcoming appointments.
    
### Patient
   - Registration: Patients can apply to be enrolled in the medical centre.
   - Appointment Booking: Book appointments with available doctors.
   - Appointment Status: Check their appointment status (e.g., pending, approved, treated).

## System Structure

The project follows a modular approach, dividing the functionality into different components:
    admin/: Folder holding admins data.
    appointments/: Folder holding appointments data.
    doctors/: Folder holding doctors data.
    patients/: Folder holding patient data.
    screens.py: Implements the Tkinter GUI for user interaction.
    users.py: Defines user classes (Admin, Doctor, Patient).
    main.py: The main entry point of the system.

## Demonstration Video:
Link: https://youtu.be/Hl0qjwkZOtU

