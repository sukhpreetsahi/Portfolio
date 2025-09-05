from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import datetime
import re
from users import *


class StartScreen:
    def __init__(self, screen, admin, doc_list, pat_list):
        self.__screen = screen
        self.__admin = admin
        self.__doc_list = doc_list
        self.__pat_list = pat_list

        self.__title = Label(self.__screen, text='User Selection:', font=50, background='lemon chiffon')

        self.__title.pack(side=TOP, padx=70)

        self.__gridframe = Frame(self.__screen, background='lemon chiffon')
        self.__gridframe.pack()

        self.__admin_button = Button(self.__gridframe, text='Admin', command=self.admin_login)
        self.__admin_button.grid(row=0, column=0, pady=10)

        self.__doctor_button = Button(self.__gridframe, text='Doctor', command=self.doctor_login)
        self.__doctor_button.grid(row=1, column=0, pady=10)

        self.__patient_button = Button(self.__gridframe, text='Patient', command=self.patient_options)
        self.__patient_button.grid(row=2, column=0, pady=10)

    def admin_login(self):
        self.__screen.destroy()
        admin_login_screen = Tk()
        admin_login_screen.title('Medical Centre Management System')
        admin_login_screen.iconbitmap("medical-kit.ico")
        admin_login_screen.configure(bg="lemon chiffon")
        admin_login_screen.eval('tk::PlaceWindow . center')
        menu = AdminLoginScreen(admin_login_screen, self.__admin, self.__doc_list, self.__pat_list)
        admin_login_screen.mainloop()

    def patient_options(self):
        self.__screen.destroy()
        patient_login_screen = Tk()
        patient_login_screen.title('Medical Centre Management System')
        patient_login_screen.iconbitmap("medical-kit.ico")
        patient_login_screen.configure(bg="lemon chiffon")
        patient_login_screen.eval('tk::PlaceWindow . center')
        menu = PatientOptionsScreen(patient_login_screen, self.__admin, self.__doc_list, self.__pat_list)
        patient_login_screen.mainloop()

    def doctor_login(self):
        self.__screen.destroy()
        doctor_login_screen = Tk()
        doctor_login_screen.title('Medical Centre Management System')
        doctor_login_screen.iconbitmap("medical-kit.ico")
        doctor_login_screen.configure(bg="lemon chiffon")
        doctor_login_screen.eval('tk::PlaceWindow . center')
        menu = DoctorLoginScreen(doctor_login_screen, self.__admin, self.__doc_list, self.__pat_list)
        doctor_login_screen.mainloop()


class AdminLoginScreen:
    def __init__(self, screen, admin, doc_list, pat_list):
        self.__admin = admin
        self.__screen = screen
        self.__doc_list = doc_list
        self.__pat_list = pat_list

        self.__back_button = Button(self.__screen, text='Back', command=self.__back)
        self.__back_button.pack(side=TOP, anchor="nw", padx=8, pady=5)
        self.__title = Label(self.__screen, text="Admin Login", padx=20, pady=20, bg="lemon chiffon", font="50")
        self.__title.pack()

        self.__username_label = Label(self.__screen, text="Username:", bg="lemon chiffon")
        self.__username_label.pack()

        self.__username_entry = Entry(self.__screen)
        self.__username_entry.pack()

        self.__password_label = Label(self.__screen, text="Password:", bg="lemon chiffon")
        self.__password_label.pack()

        self.__password_entry = Entry(self.__screen, show="*")
        self.__password_entry.pack()

        self.__login_button = Button(self.__screen, text="Login", command=self.__check_credentials)
        self.__login_button.pack()
        self.__screen.bind('<Return>', self.__check_credentials)

    def __back(self):
        self.__screen.destroy()
        screen = Tk()
        screen.title('Medical Centre Management System')
        screen.iconbitmap("medical-kit.ico")
        screen.configure(bg="lemon chiffon")
        screen.eval('tk::PlaceWindow . center')
        app = StartScreen(screen, self.__admin, self.__doc_list, self.__pat_list)
        screen.mainloop()

    def __check_credentials(self, e=None):
        username = self.__username_entry.get()
        password = self.__password_entry.get()

        if self.__admin.check_credentials(username, password):
            messagebox.showinfo("Login Successful", "Welcome, Admin!")
            self.__screen.destroy()
            self.__admin_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def __admin_menu(self):
        admin_screen = Tk()
        menu = AdminScreen(admin_screen, self.__admin, self.__doc_list, self.__pat_list)
        admin_screen.title('Medical Centre Management System')
        admin_screen.iconbitmap("medical-kit.ico")
        admin_screen.configure(bg="lemon chiffon")
        admin_screen.mainloop()


class AdminScreen:
    def __init__(self, screen, admin, doctors, patients):
        self.__screen = screen
        self.__admin = admin
        self.__doctors = doctors
        self.__patients = patients
        self.__treated_appointments = self.__admin.get_treated_appointments()
        self.__title = Label(self.__screen, bd=20, relief=RIDGE, text='Admin Menu', font=50, fg='green', bg='white',
                             pady=20, padx=100)

        # Creating Frames
        self.__frame = Frame(self.__screen, bd=10, relief=RIDGE)
        self.__left_frame = Frame(self.__frame, padx=50)
        self.__left_upper_frame = LabelFrame(self.__left_frame, padx=50, text='Admin Options')
        self.__left_lower_frame = LabelFrame(self.__left_frame, padx=50, text='Doctor Options: ')
        self.__right_frame = Frame(self.__frame, padx=50)
        self.__right_upper_frame = LabelFrame(self.__right_frame, text='Patient Options: ')
        self.__right_lower_frame = LabelFrame(self.__right_frame, text='Management Report: ')

        # Displaying Title & Frames
        self.__back_button = Button(self.__screen, text='Back', command=self.__back)
        self.__back_button.pack(side=TOP, anchor="nw", padx=8, pady=5)
        self.__title.pack(side=TOP, pady=10)
        self.__frame.pack(side=TOP, pady=10)
        self.__left_frame.pack(side=LEFT, padx=20)
        self.__left_upper_frame.pack(pady=10)
        self.__left_lower_frame.pack(pady=10)
        self.__right_frame.pack(side=RIGHT, padx=20)
        self.__right_upper_frame.pack(pady=10)
        self.__right_lower_frame.pack(pady=10)

        # Creating Admin Option Buttons
        self.__admin_details_button = Button(self.__left_upper_frame, text='View Own Details', command=self.__update_admin)

        # Creating Doctor Option Buttons
        self.__register_doc_button = Button(self.__left_lower_frame, text='Register Doctor', command=self.__register_doc)
        self.__view_docs_button = Button(self.__left_lower_frame, text='View/Edit Doctors', command=self.__view_docs)

        # Creating Patient Option Buttons
        self.__view_patients_button = Button(self.__right_upper_frame, text='View Patients',
                                             command=self.__view_patients)
        self.__view_appointments_button = Button(self.__right_upper_frame, text='View Appointments', command=self.__view_appointments)

        # Creating Management Report Option Buttons
        self.__request_report_button = Button(self.__right_lower_frame, text='Request Report',
                                              command=self.__show_report)

        # Displaying Buttons
        self.__admin_details_button.pack(padx=50, pady=10)
        self.__register_doc_button.pack(padx=50, pady=10)
        self.__view_docs_button.pack(padx=50, pady=10)
        self.__view_patients_button.pack(padx=50, pady=10)
        self.__view_appointments_button.pack(padx=50, pady=10)
        self.__request_report_button.pack(padx=60, pady=10)

    def __back(self):
        self.__screen.destroy()
        screen = Tk()
        screen.title('Medical Centre Management System')
        screen.iconbitmap("medical-kit.ico")
        screen.configure(bg="lemon chiffon")
        screen.eval('tk::PlaceWindow . center')
        app = StartScreen(screen, self.__admin, self.__doctors, self.__patients)
        screen.mainloop()

    def __check_valid_name(self, name):
        split_name = name.split(" ")
        if len(name) > 1 and len(name.split(" ")) > 1 and len(split_name[0]) > 1:
            if all(x.isalpha() for x in split_name):
                return True
            else:
                return False
        else:
            return False

    def __check_valid_dob(self, dob):
        try:
            dateObject = datetime.datetime.strptime(dob, '%d/%m/%Y')
            return True
        except:
            return False

    def __check_valid_password(self, password):
        if len(password) >= 8 and bool(re.search(r'\d', password)):
            if bool(re.search('@|$|_', password)):
                return True
            else:
                return False
        else:
            return False

    def __check_valid_postcode(self, postcode):
        split_postcode = postcode.split(" ")
        first_half_valid = False
        second_half_valid = False
        if len(split_postcode) == 2 and all(x.isalnum() for x in split_postcode):
            if 2 <= len(split_postcode[0]) <= 4:
                if split_postcode[0].isalnum():
                    if split_postcode[0][0].isalpha():
                        first_half_valid = True
            if len(split_postcode[1]) == 3:
                if split_postcode[1][0].isnumeric():
                    if all(x.isalpha() for x in split_postcode[1][1:-1]):
                        second_half_valid = True
        if first_half_valid and second_half_valid:
            return True
        else:
            return False

    def __check_valid_address(self, address):
        split_address = address.split(", ")
        if len(split_address) > 1:
            split_address[0] = split_address[0].split(" ")
            if all(x.isalnum() for x in split_address[0]) and self.__check_valid_postcode(split_address[1]):
                return True
            else:
                return False
        else:
            return False

    def __update_admin(self):
        def check_updated_details(name, dob, address):
            if self.__check_valid_name(name):
                if self.__check_valid_dob(dob):
                    if self.__check_valid_address(address):
                        return True
                    else:
                        return 'Please enter a valid address'
                else:
                    return 'Please enter a valid DOB'
            else:
                return 'Please enter a valid full name'

        def detail_submitter(e=None):
            status = check_updated_details(self.__admin_update_name_entry.get(), self.__admin_update_dob_entry.get(), self.__admin_update_address_entry.get())
            if status == True:
                if self.__admin.get_name() != self.__admin_update_name_entry.get().title() or self.__admin.get_dob() != self.__admin_update_dob_entry.get() or self.__admin.get_address() != self.__admin_update_address_entry.get():
                    self.__admin.set_name(self.__admin_update_name_entry.get().title())
                    self.__admin.set_dob(self.__admin_update_dob_entry.get())
                    self.__admin.set_address(self.__admin_update_address_entry.get())
                    messagebox.showinfo("Success", "Successfully Updated Your Details", parent=self.__admin_updater_screen)
                    selected = self.__admin_table.get_children()[0]
                    self.__admin_table.item(selected, values=(self.__admin_update_name_entry.get().title(), self.__admin_update_dob_entry.get(), self.__admin_update_address_entry.get()))
                self.__admin_updater_screen.destroy()
                self.__admin_update_button['state'] = 'normal'
            else:
                messagebox.showerror("Error", status, parent=self.__admin_updater_screen)

        def update_view():  # Opens a screen to update the details of the admin
            self.__admin_updater_screen = Toplevel(self.__update_admin_screen)
            self.__admin_updater_screen.title(f"{self.__admin.get_name()}")
            self.__admin_updater_screen.configure(bg="lemon chiffon")
            self.__admin_updater_screen_frame = Frame(self.__admin_updater_screen, bd=2, relief=RIDGE)
            self.__admin_updater_screen_frame.pack(padx=10, pady=10)
            self.__admin_update_button['state'] = 'disabled'
            self.__admin_updater_screen.protocol("WM_DELETE_WINDOW", lambda: self.__admin_update_button.configure(
                state='normal') or self.__admin_updater_screen.destroy())

            self.__admin_update_name = Label(self.__admin_updater_screen_frame, text='Name')
            self.__admin_update_name_entry = Entry(self.__admin_updater_screen_frame)
            self.__admin_update_name_entry.insert(END, f"{self.__admin.get_name()}")

            self.__admin_update_dob = Label(self.__admin_updater_screen_frame, text='DOB')
            self.__admin_update_dob_entry = Entry(self.__admin_updater_screen_frame)
            self.__admin_update_dob_entry.insert(END, f"{self.__admin.get_dob()}")

            self.__admin_update_address = Label(self.__admin_updater_screen_frame, text='Address')
            self.__admin_update_address_entry = Entry(self.__admin_updater_screen_frame)
            self.__admin_update_address_entry.insert(END, f"{self.__admin.get_address()}")

            self.__admin_update_name.grid(row=0, column=0, padx=5, pady=5)
            self.__admin_update_name_entry.grid(row=0, column=1, padx=5, pady=5)
            self.__admin_update_dob.grid(row=1, column=0, padx=5, pady=5)
            self.__admin_update_dob_entry.grid(row=1, column=1, padx=5, pady=5)
            self.__admin_update_address.grid(row=2, column=0, padx=5, pady=5)
            self.__admin_update_address_entry.grid(row=2, column=1, padx=5, pady=5)
            self.__admin_update_submit = Button(self.__admin_updater_screen, text='Submit', background='blue', command=detail_submitter)
            self.__admin_update_submit.pack()
            self.__admin_updater_screen.bind('<Return>', detail_submitter)

        self.__admin_details_button['state'] = 'disabled'
        self.__update_admin_screen = Toplevel(self.__screen)
        self.__update_admin_screen.protocol("WM_DELETE_WINDOW", lambda: self.__admin_details_button.configure(
            state='normal') or self.__update_admin_screen.destroy())
        self.__update_admin_screen.title('View Own Details')
        self.__update_admin_screen.configure(bg="lemon chiffon")
        self.__admin_table = ttk.Treeview(self.__update_admin_screen, columns=('name', "dob", "address"), show="headings", selectmode="browse")
        self.__admin_table.heading('name', text='Full Name')
        self.__admin_table.heading('dob', text='Date Of Birth')
        self.__admin_table.heading('address', text='Address')
        self.__admin_table.pack(padx=5, pady=5)

        name = self.__admin.get_name()
        dob = self.__admin.get_dob()
        address = self.__admin.get_address()
        data = (name, dob, address)
        self.__admin_table.insert(parent='', index=0, values=data)

        self.__admin_update_button = Button(self.__update_admin_screen, text='Update', background='light blue', command=update_view)
        self.__admin_update_button.pack(padx=10, pady=10)

    def __register_doc(self):  # Opens another screen to register a new doctor
        def temp_text(e):
            self.__doc_dob_entry.delete(0, END)

        def clear_text():
            self.__doc_name_entry.delete(0, END)
            self.__doc_dob_entry.delete(0, END)
            self.__doc_password_entry.delete(0, END)
            self.__doc_dob_entry.insert(END, 'DD/MM/YYYY')

        def check_doc_details():
            if self.__check_valid_name(self.__doc_name_entry.get()):
                if self.__check_valid_dob(self.__doc_dob_entry.get()):
                    if self.__check_valid_password(self.__doc_password_entry.get()):
                        return True
                    else:
                        return 'Please enter a valid password'
                else:
                    return 'Please enter a valid DOB'
            else:
                return 'Please enter a valid full name'

        def save_new_doc(e=None):
            status = check_doc_details()
            doctor_exists = False
            if status == True:
                for doctor in self.__doctors:
                    if doctor.get_name() == self.__doc_name_entry.get() and doctor.get_dob() == self.__doc_dob_entry.get():
                        doctor_exists = True
                        break
                if doctor_exists:
                    messagebox.showerror("Error", 'This Doctor is already on the system',
                                         parent=self.__register_doc_screen)
                else:
                    doctor = Doctor(self.__doc_name_entry.get().title(), self.__doc_dob_entry.get(),
                                    self.__doc_password_entry.get())
                    self.__doctors.append(doctor)
                    doctor.create_file()
                    messagebox.showinfo("Success", 'Successfully saved Dr.' + self.__doc_name_entry.get().title(),
                                        parent=self.__register_doc_screen)
                    self.__register_doc_screen.destroy()
                    self.__register_doc_button.configure(state='normal')
            else:
                messagebox.showerror("Error", str(status), parent=self.__register_doc_screen)

        self.__register_doc_button['state'] = 'disabled'
        self.__register_doc_screen = Toplevel(self.__screen)
        self.__register_doc_screen.protocol("WM_DELETE_WINDOW", lambda: self.__register_doc_button.configure(
            state='normal') or self.__register_doc_screen.destroy())
        self.__register_doc_screen.title('Register Doctor')
        self.__register_doc_screen.configure(bg="lemon chiffon")
        self.__register_doc_frame = LabelFrame(self.__register_doc_screen, text='Doctor Registration Form', bd='10',
                                               relief=RIDGE)
        self.__register_doc_frame.pack(padx=10, pady=10)
        self.__doc_name = Label(self.__register_doc_frame, text='Name:')
        self.__doc_name_entry = Entry(self.__register_doc_frame)
        self.__doc_dob = Label(self.__register_doc_frame, text='DOB:')
        self.__doc_dob_entry = Entry(self.__register_doc_frame)
        self.__doc_dob_entry.insert(END, 'DD/MM/YYYY')
        self.__doc_dob_entry.bind("<FocusIn>", temp_text)
        self.__doc_name.grid(row=0, column=0, pady=10)
        self.__doc_name_entry.grid(row=0, column=1)
        self.__doc_dob.grid(row=1, column=0)
        self.__doc_dob_entry.grid(row=1, column=1, pady=10)
        self.__doc_password = Label(self.__register_doc_frame, text='Create Password:')
        self.__doc_password_entry = Entry(self.__register_doc_frame)
        self.__doc_password.grid(row=2, column=0)
        self.__doc_password_entry.grid(row=2, column=1)
        self.__password_requirement = Label(self.__register_doc_frame,
                                            text='Tip: \n- Minimum 8 Characters\n- Minimum 1 Capital Letter\n- Minimum 1 Symbol',
                                            justify=LEFT)
        self.__password_requirement.grid(row=3, column=0, columnspan=2, pady=10)
        self.__doc_buttons_frame = Frame(self.__register_doc_screen, background='lemon chiffon')
        self.__doc_buttons_frame.pack()
        self.__doc_form_submit_button = Button(self.__doc_buttons_frame, text='Submit', background='green',
                                               command=save_new_doc)
        self.__doc_form_clear_button = Button(self.__doc_buttons_frame, text='Clear', background='blue',
                                              command=clear_text)
        self.__doc_form_submit_button.grid(row=0, column=1, padx=5)
        self.__doc_form_clear_button.grid(row=0, column=0, padx=5)
        self.__register_doc_screen.bind('<Return>', save_new_doc)

    def __view_docs(self):

        def check_updated_details(name, dob):
            if self.__check_valid_name(name):
                if self.__check_valid_dob(dob):
                    return True
                else:
                    return 'Please enter a valid DOB'
            else:
                return 'Please enter a valid full name'

        def detail_submitter(e=None):
            status = check_updated_details(self.__update_name_entry.get(), self.__update_dob_entry.get())
            if status == True:
                if self.__selected_doc.get_name() != self.__update_name_entry.get().title() or self.__selected_doc.get_dob() != self.__update_dob_entry.get():
                    self.__selected_doc.set_name(self.__update_name_entry.get().title())
                    self.__selected_doc.set_dob(self.__update_dob_entry.get())
                    messagebox.showinfo("Success", "Successfully Updated Doctor Details", parent=self.__updater_screen)
                    selected = self.__docs_table.focus()
                    self.__docs_table.item(selected,
                                           values=(self.__update_name_entry.get().title(), self.__update_dob_entry.get()))
                self.__updater_screen.destroy()
                self.__update_button['state'] = 'normal'
            else:
                messagebox.showerror("Error", status, parent=self.__updater_screen)

        def update_view():  # Opens a screen to update the details of selected doc
            item = self.__docs_table.focus()
            if item:
                self.__updater_screen = Toplevel(self.__view_docs_screen)
                self.__updater_screen.title(f"{self.__docs_table.item(item, 'values')[0]}")
                self.__updater_screen.configure(bg="lemon chiffon")
                self.__updater_screen_frame = Frame(self.__updater_screen, bd=2, relief=RIDGE)
                self.__updater_screen_frame.pack(padx=10, pady=10)
                self.__update_button['state'] = 'disabled'
                self.__updater_screen.protocol("WM_DELETE_WINDOW", lambda: self.__update_button.configure(
                    state='normal') or self.__updater_screen.destroy())
                self.__update_name = Label(self.__updater_screen_frame, text='Name')
                self.__update_name_entry = Entry(self.__updater_screen_frame)
                self.__selected_doc = None
                selected_doc_name = self.__docs_table.item(item, 'values')[0]
                selected_doc_dob = self.__docs_table.item(item, 'values')[1]
                for doctor in self.__doctors:
                    if selected_doc_name == doctor.get_name() and selected_doc_dob == doctor.get_dob():
                        self.__selected_doc = doctor
                        break
                self.__update_name_entry.insert(END, f"{self.__selected_doc.get_name()}")
                self.__update_dob = Label(self.__updater_screen_frame, text='DOB')
                self.__update_dob_entry = Entry(self.__updater_screen_frame)
                self.__update_dob_entry.insert(END, f"{self.__selected_doc.get_dob()}")
                self.__update_name.grid(row=0, column=0, padx=5, pady=5)
                self.__update_name_entry.grid(row=0, column=1, padx=5, pady=5)
                self.__update_dob.grid(row=1, column=0, padx=5, pady=5)
                self.__update_dob_entry.grid(row=1, column=1, padx=5, pady=5)
                self.__update_doc_submit = Button(self.__updater_screen, text='Submit', background='blue',
                                                  command=detail_submitter)
                self.__update_doc_submit.pack()
                self.__updater_screen.bind('<Return>', detail_submitter)
            else:
                messagebox.showerror("Error", "Select a Doctor to update the details of",
                                     parent=self.__view_docs_screen)

        def doc_deleter():  # Removes a doctor from the record
            item = self.__docs_table.focus()
            if item:
                selected_doc_name = self.__docs_table.item(item, 'values')[0]
                selected_doc_dob = self.__docs_table.item(item, 'values')[1]
                for doctor in self.__doctors:
                    if selected_doc_name == doctor.get_name() and selected_doc_dob == doctor.get_dob():
                        self.__doctors.remove(doctor)
                        doctor.delete_file()
                        break
                self.__docs_table.delete(item)
                messagebox.showinfo("Success", "The Doctor has been removed from the system",
                                    parent=self.__view_docs_screen)
            else:
                messagebox.showerror("Error", "Select a Doctor to remove from the system",
                                     parent=self.__view_docs_screen)

        self.__view_docs_button['state'] = 'disabled'
        self.__view_docs_screen = Toplevel(self.__screen)
        self.__view_docs_screen.protocol("WM_DELETE_WINDOW", lambda: self.__view_docs_button.configure(
            state='normal') or self.__view_docs_screen.destroy())
        self.__view_docs_screen.title('View Doctors')
        self.__view_docs_screen.configure(bg="lemon chiffon")
        self.__docs_table = ttk.Treeview(self.__view_docs_screen, columns=('name', "dob"), show="headings",
                                         selectmode="browse")
        self.__docs_table.heading('name', text='Full Name')
        self.__docs_table.heading('dob', text='Date Of Birth')
        self.__docs_table.pack(padx=5, pady=5)
        doc_num = 0

        for doctor in self.__doctors:
            name = doctor.get_name()
            dob = doctor.get_dob()
            data = (name, dob)
            self.__docs_table.insert(parent='', index=doc_num, values=data)
            doc_num += 1

        self.__doctor_updater_button_frame = Frame(self.__view_docs_screen, background='lemon chiffon')
        self.__doctor_updater_button_frame.pack()
        self.__update_button = Button(self.__doctor_updater_button_frame, text='Update', background='light blue',
                                      command=update_view)
        self.__update_button.pack(side=LEFT, padx=10, pady=10)
        self.__delete_button = Button(self.__doctor_updater_button_frame, text='Delete', background='red',
                                      command=doc_deleter)
        self.__delete_button.pack(side=RIGHT, padx=10, pady=10)

    def __view_patients(self):
        def sort_by_family():
            tree = self.__pats_table
            col = 6
            descending = False
            data = [(tree.set(item, col), item) for item in tree.get_children('')]
            data.sort(reverse=descending)
            for index, (val, item) in enumerate(data):
                tree.move(item, '', index)
            tree.heading(col, command=lambda: sort_treeview(tree, col, not descending))

        self.__view_patients_button['state'] = 'disabled'
        self.__view_patients_screen = Toplevel(self.__screen)
        self.__view_patients_screen.protocol("WM_DELETE_WINDOW", lambda: self.__view_patients_button.configure(
            state='normal') or self.__view_patients_screen.destroy())
        self.__view_patients_screen.title('View Patients')
        self.__view_patients_screen.configure(bg="lemon chiffon")

        self.__pats_table = ttk.Treeview(self.__view_patients_screen,
                                         columns=('name', "dob", "age", "mobile", "address", "postcode", "family_head"),
                                         show="headings",
                                         selectmode="browse")
        self.__pats_table.heading('name', text='Full Name')
        self.__pats_table.heading('dob', text='Date Of Birth')
        self.__pats_table.heading('age', text='Age')
        self.__pats_table.heading('mobile', text='Mobile')
        self.__pats_table.heading('address', text='Address')
        self.__pats_table.heading('postcode', text='Postcode')
        self.__pats_table.heading('family_head', text='Family Head')
        self.__pats_table.column("age", width=50)
        self.__pats_table.column("postcode", width=70)
        self.__pats_table.column("dob", width=90)
        self.__pats_table.pack(padx=5, pady=5)
        pat_num = 0
        for patient in self.__patients:
            name = patient.get_name()
            dob = patient.get_dob()
            age = patient.get_age()
            mobile = patient.get_mobile()
            address = patient.get_address()
            postcode = patient.get_postcode()
            head = patient.get_family_head()
            data = (name, dob, age, mobile, address, postcode, head)
            self.__pats_table.insert(parent='', index=pat_num, values=data)
            pat_num += 1
        self.__discharge_button = Button(self.__view_patients_screen, text='Discharge', bg='red', command=self.__discharge_patient)
        self.__discharge_button.pack(pady=10)
        self.__sort_button = Button(self.__view_patients_screen, text='Sort By Family', bg='green', command=sort_by_family)
        self.__sort_button.pack(pady=10)

    def __discharge_patient(self):
        item = self.__pats_table.focus()
        selected_patient = None

        if item:
            for patient in self.__patients:
                if patient.get_name() == self.__pats_table.item(item, 'values')[0] and patient.get_dob() == self.__pats_table.item(item, 'values')[1]:
                    selected_patient = patient
                    self.__patients.remove(patient)
                    patient.delete_file()
                    self.__pats_table.delete(item)
                    break
            if selected_patient:
                for doctor in self.__doctors:
                    for appointment in doctor.get_appointments():
                        if appointment.get_patient() == selected_patient:
                            doctor.remove_appointment(appointment)
                            break
                messagebox.showinfo("Success", "Discharged "+selected_patient.get_name(), parent=self.__view_patients_screen)
        else:
            messagebox.showerror("Error", "Select a patient to discharge!", parent=self.__view_patients_screen)

    def __view_appointments(self):
        def treated():
            item = self.__appointment_table.focus()
            if item:
                selected_patient_name = self.__appointment_table.item(item, 'values')[0]
                selected_patient_symptom = self.__appointment_table.item(item, 'values')[1]
                selected_status = self.__appointment_table.item(item, 'values')[2]
                selected_doctor_name = self.__appointment_table.item(item, 'values')[3]
                if selected_doctor_name == "Not Yet Assigned":
                    messagebox.showerror("Error", "This appointment hasn't even been approved yet",
                                         parent=self.__view_appointments_screen)
                    return
                for patient in self.__patients:
                    if selected_patient_name == patient.get_name() and selected_patient_symptom == patient.get_appointment().get_symptom():
                        self.__admin.add_to_treated(patient.get_appointment())
                        self.__appointment_table.item(item, values=(selected_patient_name, selected_patient_symptom, "Treated", selected_doctor_name))
                        self.__treated_appointment_table.insert("", END, values=self.__appointment_table.item(item)['values'])
                        self.__appointment_table.delete(item)
                        break
                messagebox.showinfo("Success", "This Appointment has now been set to treated",
                                    parent=self.__view_appointments_screen)
            else:
                messagebox.showerror("Error", "Select an appointment to set to treated",
                                     parent=self.__view_appointments_screen)

        self.__view_appointments_button['state'] = 'disabled'
        self.__view_appointments_screen = Toplevel(self.__screen)
        self.__view_appointments_screen.protocol("WM_DELETE_WINDOW", lambda: self.__view_appointments_button.configure(
            state='normal') or self.__view_appointments_screen.destroy())
        self.__view_appointments_screen.title('View Appointments')
        self.__view_appointments_screen.configure(bg="lemon chiffon")
        appointments = []

        for patient in self.__patients:
            if patient.get_appointment():
                if patient.get_appointment().get_status() != "Treated":
                    appointments.append(patient.get_appointment())

        self.__appointments_label = LabelFrame(self.__view_appointments_screen, padx=10, pady=10, text='Current Appointments: ', background='white', relief=RIDGE, bd=10)
        self.__appointments_label.pack(pady=5, padx=5)

        if len(appointments) != 0:
            self.__appointment_table = ttk.Treeview(self.__appointments_label, columns=('name', 'symptoms', 'status', 'doctor'), show="headings", selectmode="browse")
            self.__appointment_table.heading('name', text="Name")
            self.__appointment_table.heading('symptoms', text='Symptoms')
            self.__appointment_table.heading('status', text="Status")
            self.__appointment_table.heading('doctor', text="Doctor")

            self.__appointment_table.pack(padx=5, pady=5)
            appoint_num = 0
            for appointment in appointments:
                name = appointment.get_patient().get_name()
                symptom = appointment.get_symptom()
                status = appointment.get_status()
                doctor = appointment.get_doctor()
                if doctor:
                    doctor = doctor.get_name()
                if not doctor:
                    doctor = "Not Yet Assigned"
                data = (name, symptom, status, doctor)
                self.__appointment_table.insert(parent='', index=appoint_num, values=data)
                appoint_num += 1
            self.__appointment_buttons_frame = Frame(self.__appointments_label, bg="white")
            self.__appointment_buttons_frame.pack()
            self.__assign_doc_button = Button(self.__appointment_buttons_frame, text='Assign Doctor', command=self.__select_doc)
            self.__assign_doc_button.pack(side=LEFT, padx=5, pady=5)
            self.__treated_button = Button(self.__appointment_buttons_frame, text='Treated', bg='green', command=treated)
            self.__treated_button.pack(side=RIGHT, padx=5, pady=5)
        else:
            self.__no_appointments = Label(self.__view_appointments_screen,
                                           text="There are no new appointment requests")
            self.__no_appointments.pack(padx=10, pady=10)

        self.__treated_label = LabelFrame(self.__view_appointments_screen, padx=10, pady=10, text='Treated Appointments: ', background='white', relief=RIDGE, bd=10)
        self.__treated_label.pack(pady=5, padx=5)
        self.__treated_appointment_table = ttk.Treeview(self.__treated_label, columns=('name', 'symptoms', 'status', 'doctor'), show="headings", selectmode="browse")
        self.__treated_appointment_table.heading('name', text="Name")
        self.__treated_appointment_table.heading('symptoms', text='Symptoms')
        self.__treated_appointment_table.heading('status', text="Status")
        self.__treated_appointment_table.heading('doctor', text="Doctor")
        self.__treated_appointment_table.pack(padx=5, pady=5)
        self.__treated_appointment_table.pack(padx=5, pady=5)
        treated_appoint_num = 0
        for appointment in self.__admin.get_treated_appointments():
            if type(appointment.get_patient()) != str:
                name = appointment.get_patient().get_name()
            else:
                name = appointment.get_patient()
            doctor = appointment.get_doctor()
            symptom = appointment.get_symptom()
            status = appointment.get_status()

            if type(doctor) != str and type(doctor) is not None:
                doctor = doctor.get_name()
            elif type(doctor) is None:
                doctor = "Not Yet Assigned"
            data = (name, symptom, status, doctor)
            self.__treated_appointment_table.insert(parent='', index=treated_appoint_num, values=data)
            treated_appoint_num += 1

    def __show_report(self):
        def on_mousewheel(event):
            self.__canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.__request_report_button['state'] = 'disabled'
        self.__report_screen = Toplevel(self.__screen)
        self.__report_screen.protocol("WM_DELETE_WINDOW", lambda: self.__request_report_button.configure(
            state='normal') or self.__report_screen.destroy())
        self.__report_screen.title('Management Report')
        self.__report_screen.configure(bg="lemon chiffon")
        self.__report_frame = Frame(self.__report_screen, padx=10, pady=10, background='white', relief=RIDGE, bd=10)
        self.__report_frame.pack()

        self.__scrollbar = Scrollbar(self.__report_screen, orient=VERTICAL)
        self.__scrollbar.pack(side=RIGHT, fill=Y)

        self.__canvas = Canvas(self.__report_screen, yscrollcommand=self.__scrollbar.set)
        self.__canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.__inner_report_frame = Frame(self.__canvas, bg="white")
        self.__inner_report_frame.pack(fill=BOTH, expand=True)

        # Configure the Scrollbar to control the Canvas's yview
        self.__scrollbar.config(command=self.__canvas.yview)

        # Create a window into the Canvas to display the Frame
        self.__canvas.create_window((0, 0), window=self.__inner_report_frame, anchor="nw")

        # Bind the MouseWheel event to the Canvas
        self.__canvas.bind_all("<MouseWheel>", on_mousewheel)

        # Configure the Canvas to resize with the Frame
        self.__inner_report_frame.bind("<Configure>", lambda event, canvas=self.__canvas: self.__canvas.configure(scrollregion=self.__canvas.bbox("all")))

        self.__total_docs_label = Label(self.__inner_report_frame, text='Total No. of Doctors:', background="white")
        self.__total_docs = Label(self.__inner_report_frame, text=str(len(self.__doctors)), background='white')
        self.__patientsperdoc_label = Label(self.__inner_report_frame, text='Patients Per Doctor:', background="white",
                                            font="Verdana 9 underline")
        self.__total_docs_label.grid(row=0, column=0, padx=5)
        self.__total_docs.grid(row=0, column=1, padx=5)
        self.__patientsperdoc_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        row = 2
        loop = 1
        self.__total_unassigned_patients = 0
        self.__total_patients = len(self.__patients)
        for doctor in self.__doctors:
            self.__doc_name_label = Label(self.__inner_report_frame, text="Dr." + doctor.get_name(), background="white")
            self.__doc_name_label.grid(row=row, column=0, padx=5, pady=5)
            self.__doc_patients = Label(self.__inner_report_frame, text=doctor.get_num_patients(), background="white")
            self.__doc_patients.grid(row=row, column=1, padx=5, pady=5)
            row += 1
        for patient in self.__patients:
            if patient.get_appointment():
                if patient.get_appointment().get_status() == "Pending":
                    self.__total_unassigned_patients += 1
        self.__unassigned_patients_label = Label(self.__inner_report_frame, text='Unassigned Patients', background='white')
        self.__unassigned_patients = Label(self.__inner_report_frame, text=self.__total_unassigned_patients,
                                           background='white')
        self.__unassigned_patients_label.grid(row=row, column=0, padx=5, pady=5)
        self.__unassigned_patients.grid(row=row, column=1, padx=5, pady=5)
        row += 1
        self.__patientsperillness_label = Label(self.__inner_report_frame, text="No, of Patients Per Illness Type:",
                                                background="white", font="Verdana 9 underline")
        self.__patientsperillness_label.grid(row=row, column=0, columnspan=2, padx=5, pady=10)

        symptoms = ["Headache Issue",
                    "Eye Related Condition",
                    "Ear Related Condition",
                    "Nose Related Condition",
                    "Oral Condition",
                    "Muscular Related Condition",
                    "Allergies",
                    "Asthma",
                    "Bowel and Gastrointestinal Conditions",
                    "Cancer",
                    "Colds and Flu",
                    "COPD",
                    "Diabetes",
                    "Down Syndrome, Autism and Developmental Delays",
                    "Epilepsy",
                    "Fatigue and Sleep",
                    "Heart Health and Stroke",
                    "Hepatitis",
                    "HIV",
                    "Infectious Diseases",
                    "Joints and Spinal Conditions",
                    "Kidneys",
                    "Lungs and Respiratory Conditions",
                    "Multiple Sclerosis",
                    "Obesity",
                    "Skin, Nails and Rashes",
                    "Thyroid",
                    "Other"]
        row += 1
        for symptom in symptoms:
            self.__symptom_name_label = Label(self.__inner_report_frame, text=symptom, background="white")
            self.__symptom_name_label.grid(row=row, column=0, padx=5, pady=5)
            count = 0
            for patient in self.__patients:
                if patient.get_appointment():
                    if patient.get_appointment().get_symptom() == symptom:
                        count += 1
            self.__symptom_count = Label(self.__inner_report_frame, text=count, background="white")
            self.__symptom_count.grid(row=row, column=1, padx=5, pady=5)
            row += 1

    def __select_doc(self):  # Opens a screen to update the details of selected doc
        item = self.__appointment_table.focus()
        if item:
            if self.__appointment_table.item(item, 'values')[-1] == "Not Yet Assigned":
                self.__select_doc_screen = Toplevel(self.__view_appointments_screen)
                self.__select_doc_screen.title("Assign Doctor")
                self.__select_doc_screen.configure(bg="lemon chiffon")
                self.__assign_doc_button['state'] = 'disabled'
                self.__select_doc_screen.protocol("WM_DELETE_WINDOW", lambda: self.__assign_doc_button.configure(
                    state='normal') or self.__select_doc_screen.destroy())
                doctor_names = []
                for doctor in self.__doctors:
                    doctor_names.append("Dr." + doctor.get_name())
                self.__select_doc_label = Label(self.__select_doc_screen,
                                                text='Select a Doctor from the drop down menu below:',
                                                bg="lemon chiffon")
                self.__select_doc_label.pack(side=TOP, pady=10)
                self.__variable = StringVar(self.__select_doc_screen)
                self.__variable.set('Select')  # default value
                self.__doctor_option_menu = OptionMenu(self.__select_doc_screen, self.__variable, *doctor_names)
                self.__doctor_option_menu.configure(background='white')
                self.__selection_submit_button = Button(self.__select_doc_screen, text='Submit', background='green',
                                                        command=self.__doc_select_submit)
                self.__doctor_option_menu.pack()
                self.__selection_submit_button.pack(pady=10)

            else:
                messagebox.showerror("Error", "This appointment already has a Doctor assigned!", parent=self.__view_appointments_screen)
        else:
            messagebox.showerror("Error", "Select an appointment to assign a Doctor to", parent=self.__view_appointments_screen)

    def __doc_select_submit(self):
        self.__selection_submit_button['state'] = 'disabled'
        self.__select_doc_screen.protocol("WM_DELETE_WINDOW", lambda: self.__selection_submit_button.configure(
            state='normal') or self.__select_doc_screen.destroy())

        if self.__variable.get() != "Select":
            item = self.__appointment_table.focus()
            selected_doc = None
            selected_patient = None
            for doctor in self.__doctors:
                if doctor.get_name() == self.__variable.get().strip("Dr."):
                    selected_doc = doctor
                    break
            for patient in self.__patients:
                if patient.get_name() == self.__appointment_table.item(item, 'values')[0]:
                    selected_patient = patient
                    break
            selected_patient.get_appointment().assign_doc(selected_doc)
            selected_doc.add_appointment(selected_patient.get_appointment())
            messagebox.showinfo("Success", "Assigned Doctor", parent=self.__select_doc_screen)
            self.__appointment_table.set(item, '#3', 'Approved')
            self.__appointment_table.set(item, '#4', selected_doc.get_name())
            self.__assign_doc_button['state'] = 'normal'
            self.__select_doc_screen.destroy()
        else:
            messagebox.showerror("Error", "Select a Doctor to assign to patient", parent=self.__select_doc_screen)
            self.__selection_submit_button['state'] = 'normal'


class DoctorLoginScreen:
    def __init__(self, screen, admin, doctors, patients):
        self.__admin = admin
        self.__screen = screen
        self.__doctors = doctors
        self.__patients = patients
        self.__this_doctor = None

        self.__back_button = Button(self.__screen, text='Back', command=self.__back)
        self.__back_button.pack(side=TOP, anchor="nw", padx=8, pady=5)
        self.__title = Label(self.__screen, text="Doctor Login", padx=20, pady=20, bg="lemon chiffon", font="50")
        self.__title.pack()

        self.__name_label = Label(self.__screen, text="Name:", bg="lemon chiffon")
        self.__name_label.pack()

        self.__name_entry = Entry(self.__screen)
        self.__name_entry.pack()

        self.__password_label = Label(self.__screen, text="Password:", bg="lemon chiffon")
        self.__password_label.pack()

        self.__password_entry = Entry(self.__screen, show="*")
        self.__password_entry.pack()

        self.__login_button = Button(self.__screen, text="Login", command=self.__check_credentials)
        self.__login_button.pack(pady=5)

        self.__screen.bind('<Return>', self.__check_credentials)

    def __back(self):
        self.__screen.destroy()
        screen = Tk()
        screen.title('Medical Centre Management System')
        screen.iconbitmap("medical-kit.ico")
        screen.configure(bg="lemon chiffon")
        screen.eval('tk::PlaceWindow . center')
        app = StartScreen(screen, self.__admin, self.__doctors, self.__patients)
        screen.mainloop()

    def __check_credentials(self, e=None):
        name = self.__name_entry.get().title()
        password = self.__password_entry.get()
        doctor_found = False

        for doctor in self.__doctors:
            if doctor.get_name() == name and doctor.check_password(password):
                doctor_found = True
                self.__this_doctor = doctor
                break
        if doctor_found:
            messagebox.showinfo("Login Successful", "Welcome, Dr." + name)
            self.__screen.destroy()
            self.__doctor_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid Name or password")

    def __doctor_menu(self):
        doctor_screen = Tk()
        menu = DoctorScreen(doctor_screen, self.__admin, self.__doctors, self.__patients, self.__this_doctor)
        doctor_screen.title('Medical Centre Management System')
        doctor_screen.iconbitmap("medical-kit.ico")
        doctor_screen.configure(bg="lemon chiffon")
        doctor_screen.eval('tk::PlaceWindow . center')
        doctor_screen.mainloop()


class DoctorScreen:
    def __init__(self, screen, admin, doctors, patients, this_doctor):
        self.__screen = screen
        self.__admin = admin
        self.__doctors = doctors
        self.__patients = patients
        self.__this_doctor = this_doctor
        self.__title = Label(self.__screen, bd=20, relief=RIDGE, text='Doctor Menu', font=50, fg='green', bg='white',
                             pady=20, padx=100)
        # Displaying Title & Frames
        self.__back_button = Button(self.__screen, text='Back', command=self.__back)
        self.__back_button.pack(side=TOP, anchor="nw", padx=8, pady=5)
        self.__title.pack(side=TOP, pady=10)

        # Creating Frame
        self.__frame = Frame(self.__screen, bd=10, relief=RIDGE)
        self.__frame.pack(pady=10)

        self.__left_frame = LabelFrame(self.__frame, text='Patient Options: ')
        self.__right_frame = LabelFrame(self.__frame, text='Appointment Options: ')

        self.__left_frame.pack(side=LEFT, padx=5, pady=10)
        self.__right_frame.pack(side=RIGHT)

        # View Patient Button
        self.__view_patients_button = Button(self.__left_frame, text='View Patients',
                                             command=self.__view_patients)
        self.__view_patients_button.pack(padx=10, pady=10)

        # View Appointments Button

        self.__view_appointments_button = Button(self.__right_frame, text='View Appointments', command=self.__view_appointments)
        self.__view_appointments_button.pack(padx=10, pady=10)

    def __back(self):
        self.__screen.destroy()
        screen = Tk()
        StartScreen(screen, self.__admin, self.__doctors, self.__patients)
        screen.title('Medical Centre Management System')
        screen.iconbitmap("medical-kit.ico")
        screen.configure(bg="lemon chiffon")
        screen.eval('tk::PlaceWindow . center')
        screen.mainloop()

    def __view_patients(self):
        self.__view_patients_button['state'] = 'disabled'
        self.__view_appointments_screen = Toplevel(self.__screen)
        self.__view_appointments_screen.protocol("WM_DELETE_WINDOW", lambda: self.__view_patients_button.configure(
            state='normal') or self.__view_appointments_screen.destroy())
        self.__view_appointments_screen.title('View Patients')
        self.__view_appointments_screen.configure(bg="lemon chiffon")
        self.__pats_table = ttk.Treeview(self.__view_appointments_screen, columns=('name', "dob", "age", "mobile", "address", "postcode", "family_head"), show="headings",
                                         selectmode="browse")
        self.__pats_table.heading('name', text='Full Name')
        self.__pats_table.heading('dob', text='Date Of Birth')
        self.__pats_table.heading('age', text='Age')
        self.__pats_table.heading('mobile', text='Mobile')
        self.__pats_table.heading('address', text='Address')
        self.__pats_table.heading('postcode', text='Postcode')
        self.__pats_table.heading('family_head', text='Family Head')
        self.__pats_table.column("age", width=50)
        self.__pats_table.column("postcode", width=70)
        self.__pats_table.column("dob", width=90)
        self.__pats_table.pack(padx=5, pady=5)
        pat_num = 0
        for patient in self.__patients:
            name = patient.get_name()
            dob = patient.get_dob()
            age = patient.get_age()
            mobile = patient.get_mobile()
            address = patient.get_address()
            postcode = patient.get_postcode()
            head = patient.get_family_head()
            data = (name, dob, age, mobile, address, postcode, head)
            self.__pats_table.insert(parent='', index=pat_num, values=data)
            pat_num += 1

    def __view_appointments(self):
        self.__view_appointments_button['state'] = 'disabled'
        self.__view_appointments_screen = Toplevel(self.__screen)
        self.__view_appointments_screen.protocol("WM_DELETE_WINDOW", lambda: self.__view_appointments_button.configure(
            state='normal') or self.__view_appointments_screen.destroy())
        self.__view_appointments_screen.title('View Appointments')
        self.__view_appointments_screen.configure(bg="lemon chiffon")
        appointments = []
        for appointment in self.__this_doctor.get_appointments():
            appointments.append(appointment)

        if len(appointments) != 0:
            self.__appointment_table = ttk.Treeview(self.__view_appointments_screen, columns=('name', 'symptoms'), show="headings", selectmode="browse")
            self.__appointment_table.heading('name', text="Name")
            self.__appointment_table.heading('symptoms', text='Symptoms')
            self.__appointment_table.pack(padx=5, pady=5)
            appoint_num = 0
            for appointment in appointments:
                if type(appointment.get_patient) != str:
                    name = appointment.get_patient().get_name()
                else:
                    name = appointment.get_patient()
                symptom = appointment.get_symptom()
                data = (name, symptom)
                self.__appointment_table.insert(parent='', index=appoint_num, values=data)
                appoint_num += 1
        else:
            self.__no_appointments = Label(self.__view_appointments_screen,
                                           text="You have no current appointments")
            self.__no_appointments.pack(padx=10, pady=10)


class PatientOptionsScreen:
    def __init__(self, screen, admin, doc_list, pat_list):
        self.__admin = admin
        self.__screen = screen
        self.__doctors = doc_list
        self.__patients = pat_list

        self.__back_button = Button(self.__screen, text='Back', command=self.__back)
        self.__back_button.pack(side=TOP, anchor="nw", padx=8, pady=5)
        self.__title = Label(self.__screen, text="Patient Options", padx=20, pady=20, bg="lemon chiffon", font="50")
        self.__title.pack()

        self.__login_button = Button(self.__screen, text="Appointments", command=self.__login_patient)
        self.__login_button.pack(pady=10)
        self.__register_button = Button(self.__screen, text="Register", command=self.__register_patient)
        self.__register_button.pack(pady=5)

    def __back(self):
        self.__screen.destroy()
        screen = Tk()
        screen.title('Medical Centre Management System')
        screen.iconbitmap("medical-kit.ico")
        screen.configure(bg="lemon chiffon")
        screen.eval('tk::PlaceWindow . center')
        app = StartScreen(screen, self.__admin, self.__doctors, self.__patients)
        screen.mainloop()

    def __login_patient(self):
        self.__screen.destroy()
        login_screen = Tk()
        PatientLoginScreen(login_screen, self.__admin, self.__doctors, self.__patients)
        login_screen.title('Medical Centre Management System')
        login_screen.iconbitmap("medical-kit.ico")
        login_screen.configure(bg="lemon chiffon")
        login_screen.eval('tk::PlaceWindow . center')
        login_screen.mainloop()

    def __register_patient(self):  # Opens another screen to register a new patient
        self.__screen.destroy()
        registration_screen = Tk()
        PatientRegisterScreen(registration_screen, self.__admin, self.__doctors, self.__patients)
        registration_screen.title('Medical Centre Management System')
        registration_screen.iconbitmap("medical-kit.ico")
        registration_screen.configure(bg="lemon chiffon")
        registration_screen.eval('tk::PlaceWindow . center')
        registration_screen.mainloop()


class PatientLoginScreen:
    def __init__(self, screen, admin, doctors, patients):
        def temp_text(e):
            if self.__dob_entry.get() == 'DD/MM/YYYY':
                self.__dob_entry.delete(0, END)

        self.__screen = screen
        self.__admin = admin
        self.__doctors = doctors
        self.__patients = patients
        self.__my_patient = None
        self.__back_button = Button(self.__screen, text='Back', command=self.__back)
        self.__back_button.pack(side=TOP, anchor="nw", padx=8, pady=5)
        self.__title = Label(self.__screen, text="Patient Details", padx=20, pady=20, bg="lemon chiffon", font="50")
        self.__title.pack()

        self.__login_input_frame = Frame(self.__screen, bg="lemon chiffon")
        self.__login_input_frame.pack()
        self.__name_label = Label(self.__login_input_frame, text="Name:", bg="lemon chiffon")
        self.__name_label.grid(row=0, column=0, padx=5)

        self.__name_entry = Entry(self.__login_input_frame)
        self.__name_entry.grid(row=0, column=1, padx=5)

        self.__dob_label = Label(self.__login_input_frame, text="DOB:", bg="lemon chiffon")
        self.__dob_label.grid(row=1, column=0, padx=5, pady=5)

        self.__dob_entry = Entry(self.__login_input_frame)
        self.__dob_entry.grid(row=1, column=1, padx=5, pady=5)

        self.__dob_entry.insert(END, 'DD/MM/YYYY')
        self.__dob_entry.bind("<FocusIn>", temp_text)

        self.__submit_button = Button(self.__screen, text='Submit', background="green",
                                      command=self.__check_credentials)
        self.__submit_button.pack(pady=5)
        self.__screen.bind('<Return>', self.__check_credentials)

    def __back(self):
        self.__screen.destroy()
        screen = Tk()
        screen.title('Medical Centre Management System')
        screen.iconbitmap("medical-kit.ico")
        screen.configure(bg="lemon chiffon")
        screen.eval('tk::PlaceWindow . center')
        PatientOptionsScreen(screen, self.__admin, self.__doctors, self.__patients)
        screen.mainloop()

    def __check_valid_name(self, name):
        split_name = name.split(" ")
        if len(name) > 1 and len(name.split(" ")) > 1 and len(split_name[0]) > 1:
            if all(x.isalpha() for x in split_name):
                return True
            else:
                return False
        else:
            return False

    def __check_valid_dob(self, dob):
        try:
            dateObject = datetime.datetime.strptime(dob, '%d/%m/%Y')
            return True
        except:
            return False

    def __check_credentials(self, e=None):
        name = self.__name_entry.get()
        dob = self.__dob_entry.get()
        patient_match = False

        if self.__check_valid_name(name) and self.__check_valid_dob(dob):
            for patient in self.__patients:
                if patient.get_name() == name.title() and patient.get_dob() == dob:
                    patient_match = True
                    self.__my_patient = patient
                    break
            if patient_match:
                messagebox.showinfo("Patient Found", "Welcome, " + name.title() + " !")
                self.__screen.destroy()
                self.__patient_menu()
            else:
                messagebox.showerror("Patient Not Found",
                                     "Please register if you are not on the system, else enter your details correctly!")
        else:
            messagebox.showerror("Input Error", "Please Input your Name & DOB in the correct format")

    def __patient_menu(self):
        patient_screen = Tk()
        PatientScreen(patient_screen, self.__admin, self.__doctors, self.__patients, self.__my_patient)
        patient_screen.title('Medical Centre Management System')
        patient_screen.iconbitmap("medical-kit.ico")
        patient_screen.configure(bg="lemon chiffon")
        patient_screen.mainloop()


class PatientRegisterScreen:
    def __init__(self, screen, admin, doctors, patients):
        def temp_text(e):
            if self.__dob_entry.get() == "DD/MM/YYYY":
                self.__dob_entry.delete(0, END)

        def temp_mobile_text(e):
            if self.__mobile_entry.get() == "E.g  07411223341":
                self.__mobile_entry.delete(0, END)

        self.__screen = screen
        self.__admin = admin
        self.__doctors = doctors
        self.__patients = patients
        self.__back_button = Button(self.__screen, text='Back', command=self.__back)
        self.__back_button.pack(side=TOP, anchor="nw", padx=8, pady=5)
        self.__title = Label(self.__screen, text="Patient Registration Form", padx=20, pady=20, bg="lemon chiffon",
                             font="50")
        self.__title.pack()

        self.__patient_registration_frame = Frame(self.__screen, bg="lemon chiffon")
        self.__patient_registration_frame.pack()
        self.__name_label = Label(self.__patient_registration_frame, text="Name:", bg="lemon chiffon")
        self.__name_label.grid(row=0, column=0, padx=5)

        self.__name_entry = Entry(self.__patient_registration_frame)
        self.__name_entry.grid(row=0, column=1, padx=5)

        self.__dob_label = Label(self.__patient_registration_frame, text="DOB:", bg="lemon chiffon")
        self.__dob_label.grid(row=1, column=0, padx=5, pady=5)

        self.__dob_entry = Entry(self.__patient_registration_frame)
        self.__dob_entry.grid(row=1, column=1, padx=5, pady=5)

        self.__dob_entry.insert(END, 'DD/MM/YYYY')
        self.__dob_entry.bind("<FocusIn>", temp_text)

        self.__mobile_label = Label(self.__patient_registration_frame, text="Mobile:", bg="lemon chiffon")
        self.__mobile_label.grid(row=2, column=0, padx=5, pady=5)

        self.__mobile_entry = Entry(self.__patient_registration_frame)
        self.__mobile_entry.grid(row=2, column=1, padx=5, pady=5)

        self.__mobile_entry.insert(END, 'E.g  07411223341')
        self.__mobile_entry.bind("<FocusIn>", temp_mobile_text)

        self.__address_label = Label(self.__patient_registration_frame, text="Address:", bg="lemon chiffon")
        self.__address_label.grid(row=3, column=0, padx=5, pady=5)

        self.__address_entry = Entry(self.__patient_registration_frame)
        self.__address_entry.grid(row=3, column=1, padx=5, pady=5)

        self.__postcode_label = Label(self.__patient_registration_frame, text="Postcode:", bg="lemon chiffon")
        self.__postcode_label.grid(row=4, column=0, padx=5, pady=5)

        self.__postcode_entry = Entry(self.__patient_registration_frame)
        self.__postcode_entry.grid(row=4, column=1, padx=5, pady=5)

        self.__family_head_label = Label(self.__patient_registration_frame, text="Family Head:", bg="lemon chiffon")
        self.__family_head_label.grid(row=5, column=0, padx=5, pady=5)

        self.__family_head_entry = Entry(self.__patient_registration_frame)
        self.__family_head_entry.grid(row=5, column=1, padx=5, pady=5)

        self.__submit_button = Button(self.__screen, text='Submit', background="green",
                                      command=self.__check_credentials)
        self.__submit_button.pack(pady=5)
        self.__screen.bind('<Return>', self.__check_credentials)

    def __back(self):
        self.__screen.destroy()
        screen = Tk()
        screen.title('Medical Centre Management System')
        screen.iconbitmap("medical-kit.ico")
        screen.configure(bg="lemon chiffon")
        screen.eval('tk::PlaceWindow . center')
        PatientOptionsScreen(screen, self.__admin, self.__doctors, self.__patients)
        screen.mainloop()

    def __check_valid_name(self, name):
        split_name = name.split(" ")
        if len(name) > 1 and len(name.split(" ")) > 1 and len(split_name[0]) > 1:
            if all(x.isalpha() for x in split_name):
                return True
            else:
                return False
        else:
            return False

    def __check_valid_dob(self, dob):
        try:
            dateObject = datetime.datetime.strptime(dob, '%d/%m/%Y')
            return True
        except:
            return False

    def __check_valid_mobile(self, mobile):
        if mobile.isnumeric() and mobile[0] == "0":
            if len(mobile) == 11:
                return True
            else:
                return False
        else:
            return False

    def __check_valid_address(self, address):
        split_address = address.split(" ")
        if len(split_address) > 1:
            if split_address[0].isalnum() and all(x.isalpha() for x in split_address[1:-1]):
                return True
            else:
                return False
        else:
            return False

    def __check_valid_postcode(self, postcode):
        split_postcode = postcode.split(" ")
        first_half_valid = False
        second_half_valid = False
        if len(split_postcode) == 2 and all(x.isalnum() for x in split_postcode):
            if 2 <= len(split_postcode[0]) <= 4:
                if split_postcode[0].isalnum():
                    if split_postcode[0][0].isalpha():
                        first_half_valid = True
            if len(split_postcode[1]) == 3:
                if split_postcode[1][0].isnumeric():
                    if all(x.isalpha() for x in split_postcode[1][1:-1]):
                        second_half_valid = True
        if first_half_valid and second_half_valid:
            return True
        else:
            return False

    def __check_valid_family_head(self, family_head):
        return self.__check_valid_name(family_head)

    def __check_credentials(self, e=None):
        name = self.__name_entry.get()
        dob = self.__dob_entry.get()
        mobile = self.__mobile_entry.get()
        address = self.__address_entry.get()
        postcode = self.__postcode_entry.get()
        family_head = self.__family_head_entry.get()
        patient_match = False

        if self.__check_valid_name(name):
            if self.__check_valid_dob(dob):
                if self.__check_valid_mobile(mobile):
                    if self.__check_valid_address(address):
                        if self.__check_valid_postcode(postcode):
                            if self.__check_valid_family_head(family_head):
                                for patient in self.__patients:
                                    if patient.get_name() == name.title() and patient.get_dob() == dob:
                                        patient_match = True
                                        break
                                if patient_match:
                                    messagebox.showerror("Registration Failed", "You are already on the system!")
                                    self.__back()
                                else:
                                    messagebox.showinfo("Registration Successful", "You have been added to the system!")
                                    new_patient = Patient(name.title(), dob, mobile, address.title(), postcode.upper(),
                                                          family_head.title())
                                    self.__patients.append(new_patient)
                                    new_patient.create_file()
                                    self.__back()
                            else:
                                messagebox.showerror("Input Error", "Please Input your Family Head correctly")
                        else:
                            messagebox.showerror("Input Error", "Please Input your Postcode correctly")
                    else:
                        messagebox.showerror("Input Error", "Please Input your Address correctly")
                else:
                    messagebox.showerror("Input Error", "Please Input your Mobile correctly")
            else:
                messagebox.showerror("Input Error", "Please Input your DOB correctly")
        else:
            messagebox.showerror("Input Error", "Please Input your Name correctly")


class PatientScreen:
    def __init__(self, screen, admin, doctors, patients, my_patient):
        self.__screen = screen
        self.__admin = admin
        self.__doctors = doctors
        self.__patients = patients
        self.__my_patient = my_patient
        self.__title = Label(self.__screen, bd=20, relief=RIDGE, text='Patient Menu', font=50, fg='green', bg='white',
                             pady=20, padx=100)
        # Displaying Title & Back Button
        self.__back_button = Button(self.__screen, text='Back', command=self.__back)
        self.__back_button.pack(side=TOP, anchor="nw", padx=8, pady=5)
        self.__title.pack(side=TOP, pady=10)

        # Display Frames
        self.__appointments_frame = Frame(self.__screen, relief=SUNKEN, bd=1)
        self.__booking_frame = LabelFrame(self.__screen, text="Book Appointment")
        self.__appointments_frame.pack()
        if self.__my_patient.get_appointment() is None:
            self.__booking_frame.pack(pady=10)
            # Appointments Section
            self.__no_appointments = Label(self.__appointments_frame, text="You have no current appointments requested or booked")
            self.__no_appointments.pack(padx=10, pady=10)
            # Booking Section
            symptoms = ["Headache Issue",
                        "Eye Related Condition",
                        "Ear Related Condition",
                        "Nose Related Condition",
                        "Oral Condition",
                        "Muscular Related Condition",
                        "Allergies",
                        "Asthma",
                        "Bowel and Gastrointestinal Conditions",
                        "Cancer",
                        "Colds and Flu",
                        "COPD",
                        "Diabetes",
                        "Down Syndrome, Autism and Developmental Delays",
                        "Epilepsy",
                        "Fatigue and Sleep",
                        "Heart Health and Stroke",
                        "Hepatitis",
                        "HIV",
                        "Infectious Diseases",
                        "Joints and Spinal Conditions",
                        "Kidneys",
                        "Lungs and Respiratory Conditions",
                        "Multiple Sclerosis",
                        "Obesity",
                        "Skin, Nails and Rashes",
                        "Thyroid",
                        "Other"]

            self.__variable = StringVar(self.__booking_frame)
            self.__variable.set('Select Symptom')  # default value
            self.__symptoms_option_menu = ttk.Combobox(self.__booking_frame, textvariable=self.__variable, values=symptoms, state="readonly", width=45)
            self.__selection_submit_button = Button(self.__screen, text='Submit', background='green', command=self.__request_appointment)

            self.__symptoms_option_menu.pack(padx=10, pady=10)
            self.__selection_submit_button.pack(pady=10)

        else:
            self.__view_appointment_details()

    def __back(self):
        self.__screen.destroy()
        screen = Tk()
        PatientOptionsScreen(screen, self.__admin, self.__doctors, self.__patients)
        screen.title('Medical Centre Management System')
        screen.iconbitmap("medical-kit.ico")
        screen.configure(bg="lemon chiffon")
        screen.eval('tk::PlaceWindow . center')
        screen.mainloop()

    def __view_appointment_details(self):
        appointment = self.__my_patient.get_appointment()
        self.__table = ttk.Treeview(self.__appointments_frame, columns=('name', 'symptoms', "status", "doctor"), show="headings", selectmode="browse")
        self.__table.heading('name', text="Name")
        self.__table.heading('symptoms', text='Symptoms')
        self.__table.heading('status', text='Status')
        self.__table.heading('doctor', text='Doctor')
        self.__table.pack(padx=5, pady=5)

        name = self.__my_patient.get_name()
        symptom = appointment.get_symptom()
        status = appointment.get_status()
        doctor = appointment.get_doctor()
        if doctor:
            doctor = doctor.get_name()
        else:
            doctor = "Not Yet Assigned"
        data = (name, symptom, status, doctor)
        self.__table.insert(parent='', index=0, values=data)

    def __request_appointment(self):
        symptom = self.__symptoms_option_menu.get()
        if symptom == "Select Symptom":
            messagebox.showerror("Error", "Select a symptom!")
        else:
            appointment = Appointment(self.__my_patient, symptom)
            appointment.create_file()
            self.__my_patient.set_appointment(appointment)
            self.__booking_frame.pack_forget()
            self.__no_appointments.pack_forget()
            self.__selection_submit_button.pack_forget()
            self.__view_appointment_details()
