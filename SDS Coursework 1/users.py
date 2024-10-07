import datetime
import os
import re


class Admin:
    def __init__(self, name, username, password, dob="", address=""):
        self.__name = name
        self.__username = username
        self.__password = password
        self.__dob = dob
        self.__address = address
        self.__appointments = []
        self.__treated_appointments = []

    def check_credentials(self, username, password):
        if self.__username == username and self.__password == password:
            return True
        else:
            return False

    def get_own_data(self):
        return self.__username, self.__name, self.__address

    def get_name(self):
        return self.__name

    def get_username(self):
        return self.__username

    def get_dob(self):
        return self.__dob

    def check_password(self, password):
        if self.__password == password:
            return True
        else:
            return False

    def get_address(self):
        return self.__address

    def set_name(self, name):
        self.__name = name
        with open("admin/admin1.txt", "r") as adminfile:  # Open the file in read mode
            lines = adminfile.readlines()  # Assign the file as a list to a variable
            lines[0] = name + "\n"  # Replace the proper line with the provided content
        with open("admin/admin1.txt", "w") as adminfile:  # Open the file in write mode
            adminfile.write("".join(lines))  # Write the modified content to the file

    def set_dob(self, dob):
        self.__dob = dob
        with open("admin/admin1.txt", "r") as adminfile:  # Open the file in read mode
            lines = adminfile.readlines()  # Assign the file as a list to a variable
            lines[3] = dob + "\n"  # Replace the proper line with the provided content
        with open("admin/admin1.txt", "w") as adminfile:  # Open the file in write mode
            adminfile.write("".join(lines))  # Write the modified content to the file

    def set_address(self, address):
        self.__address = address
        with open("admin/admin1.txt", "r") as adminfile:  # Open the file in read mode
            lines = adminfile.readlines()  # Assign the file as a list to a variable
            lines[4] = address + "\n"  # Replace the proper line with the provided content
        with open("admin/admin1.txt", "w") as adminfile:  # Open the file in write mode
            adminfile.write("".join(lines))  # Write the modified content to the file

    def add_to_treated(self, appointment):
        appointment.treated()
        self.__treated_appointments.append(appointment)
        if type(appointment.get_patient()) != str:
            appointment.get_doctor().remove_appointment(appointment)

    def get_treated_appointments(self):
        return self.__treated_appointments

    def add_appointment(self, appointment):
        self.__appointments.append(appointment)


class Patient:
    def __init__(self, name, dob, mobile, address, postcode, family_head=None, doctor=None):
        self.__name = name
        self.__dob = dob
        self.__mobile = mobile
        self.__address = address
        self.__postcode = postcode
        self.__doctor = doctor
        self.__family_head = family_head
        self.__appointment = None

    def get_name(self):
        return self.__name

    def get_dob(self):
        return self.__dob

    def get_age(self):
        # import datetime
        today = datetime.date.today()
        born = datetime.datetime.strptime(self.__dob, "%d/%m/%Y")
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def get_mobile(self):
        return self.__mobile

    def get_address(self):
        return self.__address

    def get_postcode(self):
        return self.__postcode

    def get_family_head(self):
        return self.__family_head

    def get_appointment(self):
        return self.__appointment

    def set_appointment(self, appointment):
        self.__appointment = appointment

    def assign_doctor(self, doctor):
        self.__doctor = doctor

    def view_appointment_status(self):
        return self.appointment.__status()

    def __file_name(self):
        return self.__name.replace(" ", "").lower() + self.__dob.replace("/", "") + ".txt"

    def create_file(self):
        filename = self.__file_name()
        lines = [self.__name + "\n", self.__dob + "\n", self.__mobile + "\n", self.__address + "\n", self.__postcode + "\n", self.__family_head]
        with open(f"patients/{filename}", "w") as patientfile:  # Open the file in write mode
            patientfile.write("".join(lines))  # Write the modified content to the file

    def delete_file(self):
        os.remove("patients/"+self.__file_name())
        appointfiles = []
        delete_file = False
        for path in os.listdir("appointments"):
            # check if current path is a file
            if os.path.isfile(os.path.join("appointments", path)):
                appointfiles.append(path)
        for file in appointfiles:
            match = re.match(r"([a-z]+)([0-9]+)", file, re.I)
            items = match.groups()
            if items[0] == self.__name.replace(" ", "").lower():
                if items[1] == self.__dob.replace("/", ""):
                    with open(f"appointments/{file}", "r") as appointmentfile:  # Open the file in read mode
                        lines = appointmentfile.readlines()  # Assign the file as a list to a variable
                        if lines[3] != "Treated":  # Replace the proper line with the provided content
                            delete_file = True
                    if delete_file:
                        os.remove("appointments/"+file)


class Doctor:
    def __init__(self, name, dob, password):
        self.__name = name
        self.__dob = dob
        self.__patients = []
        self.__appointments = []
        self.__split_dob = self.__dob.split("/")
        self.__username = str(self.__name.split(" ")[0]) + "@" + str(
            self.__split_dob[0] + self.__split_dob[1] + self.__split_dob[2])
        self.__password = password

    def get_name(self):
        return self.__name

    def get_dob(self):
        return self.__dob

    def get_patients(self):
        return self.__patients

    def get_num_patients(self):
        return len(self.__patients)

    def check_password(self, password):
        if password == self.__password:
            return True
        else:
            return False

    def create_file(self):
        filename = self.__file_name()
        lines = [self.__name+"\n", self.__dob+"\n", self.__password]
        with open(f"doctors/{filename}", "w") as doctorfile:  # Open the file in write mode
            doctorfile.write("".join(lines))  # Write the modified content to the file

    def __file_name(self):
        return self.__name.replace(" ", "").lower()+self.__dob.replace("/", "")+".txt"

    def set_name(self, name):
        filename = self.__file_name()
        self.__name = name
        with open(f"doctors/{filename}", "r") as doctorfile:  # Open the file in read mode
            lines = doctorfile.readlines()  # Assign the file as a list to a variable
            lines[0] = name + "\n"  # Replace the proper line with the provided content
        with open(f"doctors/{filename}", "w") as doctorfile:  # Open the file in write mode
            doctorfile.write("".join(lines))  # Write the modified content to the file
        os.rename("doctors/"+filename, "doctors/"+self.__file_name())

    def set_dob(self, dob):
        filename = self.__file_name()
        self.__dob = dob
        with open(f"doctors/{filename}", "r") as doctorfile:  # Open the file in read mode
            lines = doctorfile.readlines()  # Assign the file as a list to a variable
            lines[1] = dob + "\n"  # Replace the proper line with the provided content
        with open(f"doctors/{filename}", "w") as doctorfile:  # Open the file in write mode
            doctorfile.write("".join(lines))  # Write the modified content to the file
        os.rename("doctors/"+filename, "doctors/"+self.__file_name())

    def add_patient(self, patient):
        self.__patients.append(patient)

    def remove_patient(self, patient):
        self.__patients.remove(patient)

    def add_appointment(self, appointment):
        self.__appointments.append(appointment)

    def get_appointments(self):
        return self.__appointments

    def remove_appointment(self, appointment):
        self.__appointments.remove(appointment)

    def delete_file(self):
        os.remove("doctors/"+self.__file_name())


class Appointment:
    def __init__(self, patient, symptom, doctor=None, status="Pending"):
        self.__patient = patient
        self.__symptom = symptom
        self.__doctor = doctor
        self.__status = status
        self.appointment_date = None

    def approve(self):
        filename = self.__file_name()
        self.__status = "Approved"
        with open(f"appointments/{filename}", "r") as appointmentfile:  # Open the file in read mode
            lines = appointmentfile.readlines()  # Assign the file as a list to a variable
            lines[3] = "Approved"  # Replace the proper line with the provided content
        with open(f"appointments/{filename}", "w") as appointmentfile:  # Open the file in write mode
            appointmentfile.write("".join(lines))  # Write the modified content to the file

    def treated(self):
        filename = self.__file_name()
        self.__status = "Treated"
        if type(self.__patient) != str:
            with open(f"appointments/{filename}", "r") as appointmentfile:  # Open the file in read mode
                lines = appointmentfile.readlines()  # Assign the file as a list to a variable
                lines[3] = "Treated"  # Replace the proper line with the provided content
            with open(f"appointments/{filename}", "w") as appointmentfile:  # Open the file in write mode
                appointmentfile.write("".join(lines))  # Write the modified content to the file

    def assign_doc(self, doctor):
        filename = self.__file_name()
        self.__doctor = doctor
        self.approve()
        with open(f"appointments/{filename}", "r") as appointmentfile:  # Open the file in read mode
            lines = appointmentfile.readlines()  # Assign the file as a list to a variable
            lines[2] = doctor.get_name() + "\n"  # Replace the proper line with the provided content
        with open(f"appointments/{filename}", "w") as appointmentfile:  # Open the file in write mode
            appointmentfile.write("".join(lines))  # Write the modified content to the file

    def get_patient(self):
        return self.__patient

    def get_symptom(self):
        return self.__symptom

    def get_status(self):
        return self.__status

    def get_doctor(self):
        return self.__doctor

    def get_date(self):
        return self.appointment_date

    def create_file(self):
        filename = self.__file_name()
        if self.__doctor:
            doctor = doctor.get_name()
        else:
            doctor = "None"
        lines = [self.__patient.get_name() + "\n", self.__symptom + "\n", doctor+"\n", self.__status]
        with open(f"appointments/{filename}", "w") as appointmentfile:  # Open the file in write mode
            appointmentfile.write("".join(lines))  # Write the modified content to the file

    def __file_name(self):
        if type(self.__patient) != str:
            return self.__patient.get_name().replace(" ", "").lower() + self.__patient.get_dob().replace("/", "") + self.__symptom.replace(" ", "").lower() + ".txt"
