from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import datetime
import re
from users import *
from screens import *
import os

patients_record = []
treated_patients = []


def main():
    screen = Tk()
    screen.title('Medical Centre Management System')
    screen.eval('tk::PlaceWindow . center')
    screen.iconbitmap("medical-kit.ico")
    screen.configure(bg="lemon chiffon")

    # Load admin data from admin file and initiate admin object
    admindata = []
    with open("admin/admin1.txt") as adminfile:
        for line in adminfile:
            admindata.append(line.strip("\n"))
    admin1 = Admin(admindata[0], admindata[1], admindata[2], admindata[3], admindata[4])

    doc_list = []

    # Load all doctor files from the doctors directory and then initiate the doctor objects
    doctorfiles = []
    for path in os.listdir("doctors"):
        # check if current path is a file
        if os.path.isfile(os.path.join("doctors", path)):
            doctorfiles.append(path)
    for doctorfile in doctorfiles:
        docdata = []
        with open(f"doctors/{doctorfile}") as docfile:
            for line in docfile:
                docdata.append(line.strip("\n"))
        doctor = Doctor(docdata[0], docdata[1], docdata[2])
        doc_list.append(doctor)

    pat_list = []

    # Load all doctor files from the doctors directory and then initiate the doctor objects
    patfiles = []
    for path in os.listdir("patients"):
        # check if current path is a file
        if os.path.isfile(os.path.join("patients", path)):
            patfiles.append(path)
    for patfile in patfiles:
        patdata = []
        with open(f"patients/{patfile}") as patientfile:
            for line in patientfile:
                patdata.append(line.strip("\n"))
        patient = Patient(patdata[0], patdata[1], patdata[2], patdata[3], patdata[4], patdata[5])
        pat_list.append(patient)

    # Open appointments, create objects add to admins appointment list
    # Load all doctor files from the doctors directory and then initiate the doctor objects
    appointment_list = []
    appointfiles = []
    for path in os.listdir("appointments"):
        # check if current path is a file
        if os.path.isfile(os.path.join("appointments", path)):
            appointfiles.append(path)

    for appointfile in appointfiles:
        appointdata = []
        with open(f"appointments/{appointfile}") as appointmentfile:
            for line in appointmentfile:
                appointdata.append(line.strip("\n"))
        if appointdata[3] == "Treated":
            appointment = Appointment(appointdata[0], appointdata[1], appointdata[2], appointdata[3])
            admin1.add_to_treated(appointment)
        else:
            selected_patient = None
            selected_doc = None
            for patient in pat_list:
                if appointdata[0] == patient.get_name():
                    match = re.match(r"([a-z]+)([0-9]+)", appointfile, re.I)
                    items = match.groups()
                    if items[1] == patient.get_dob().replace("/", ""):
                        appointdata[0] = patient
                        selected_patient = patient
                        break
            if appointdata[2] != "None":
                for doctor in doc_list:
                    if appointdata[2] == doctor.get_name():
                        appointdata[2] = doctor
                        selected_doc = doctor
                        break
            else:
                appointdata[2] = None
            appointment = Appointment(appointdata[0], appointdata[1], appointdata[2], appointdata[3])
            if selected_patient:
                selected_patient.set_appointment(appointment)
            if selected_doc:
                selected_doc.add_appointment(appointment)
            admin1.add_appointment(appointment)

    app = StartScreen(screen, admin1, doc_list, pat_list)
    screen.mainloop()


if __name__ == "__main__":
    main()
