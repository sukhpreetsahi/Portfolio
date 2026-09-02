import os
import time
from client import *
import maskpass
import ast


def startscreen():
    """
    This function is the start up screen to display company logo.
    """
    print(" __  __       _____ _                              _____             ")
    print("|  \\/  |     |  ___(_)                            |_   _|            ")
    print("| .  . |_   _| |_   _ _ __   __ _ _ __   ___ ___    | | _ __   ___   ")
    print("| |\\/| | | | |  _| | | '_ \\ / _` | '_ \\ / __/ _ \\   | || '_ \\ / __|  ")
    print("| |  | | |_| | |   | | | | | (_| | | | | (_|  __/  _| || | | | (__ _ ")
    print("\\_|  |_/\\__, \\_|   |_|_| |_|\\__,_|_| |_|\\___\\___|  \\___/_| |_|\\___(_)")
    print("         __/ |                               ")
    print("        |___/                                ")
    time.sleep(1.5)
    os.system('cls')  # Clears the screen


def homescreen():
    """
    This functions provides options for a user to Login or Register
    """
    print("Main Menu\n")
    print("Options:")
    print("   1. Login")
    print("   2. Register")
    choice = input("Enter choice: ")
    while True:
        if choice == "1":
            login_screen()
            break
        elif choice == "2":
            register_screen()
            break
        else:
            choice = input("Enter a valid option: ")


def login_screen():
    """
    This function allows a user to login by entering username, password and an OTP if valid password entered.
    """
    os.system('cls')  # Clears
    print("Login:")
    print("\x1B[3m(Enter 0 to go back)\x1B[0m \n")  # Italics

    creds_match = False  # Variable which changes to True if Username and Password match

    while not creds_match:  # Loop

        while True:  # Loop if invalid Username
            username = input("Enter Username: ")
            if username == "0":
                os.system('cls')
                homescreen()
                return
            if username:
                break

        while True:  # Loop if incorrect Password entered
            # Stops password being seen while typing
            password = maskpass.askpass(prompt="Password:", mask="*")
            if password:
                response = attempt_login(username, password)
                # Checks if username password match
                if response.startswith('LOGIN_SUCCESS'):
                    details = response.split("LOGIN_SUCCESS,")[1]
                    details = ast.literal_eval(details)
                    # Create Client object
                    client = Client(
                        details['username'], deserialise_list(details['contact_info']), details['hashed_password'])

                    # Returns OTP that was sent to the client""
                    sent_otp = otp_sender(client)

                    if sent_otp == "OTP_FAIL":  # If no OTP was sent then returned to the Login screen as an issue occured
                        print("Issue with OTP system.")
                        time.sleep(1)
                        login_screen()

                    else:
                        while True:  # Loop until correct OTP entered or 0 entered to exit
                            entered_otp = input(
                                "Enter the 6 digit OTP sent to your email or 0 to exit: ")
                            if entered_otp != "0" and check_otp(entered_otp) == "OTP_SUCCESS":
                                creds_match = True
                                print("Successfully Logged in")
                                time.sleep(1)
                                creds_match = True
                                os.system('cls')
                                dashboard(client)  # Go to dashboard

                            elif entered_otp == "0":
                                login_screen()

                            else:
                                print("OTP didn't match.")

                elif response == "Error communicating with server":
                    print("Error communicating with server")
                else:
                    print("Credentials don't match")
                    break


def register_screen():
    os.system('cls')
    """
    This function lets users create an account with a 
    username, first name, last name, email, number & password
    """
    print("Register:")
    print("\x1B[3m(Enter 0 to go back)\x1B[0m \n")

    while True:  # Loops till valid username entered
        username = input("Create a username: ")

        if username == "0":
            os.system('cls')
            homescreen()
            return

        if username:
            value = check_username(username)
            if value == "USERNAME_EXISTS":
                print("This username already exists")
            elif value == "Error communicating with server":
                print("Error with server")
            else:
                break

    while True:
        fname = input("Enter first name: ")
        if fname == "0":
            os.system('cls')
            homescreen()
            return
        if fname.isalpha():  # Name should only contain letters
            break

    while True:
        lname = input("Enter last name: ")
        if fname == "0":
            os.system('cls')
            homescreen()
            return
        if lname.isalpha():
            break

    while True:  # Email must contain an @ and at least 1 dot
        email = input("Enter your email address: ")
        if email == "0":
            os.system('cls')
            homescreen()
            return
        if email.count("@") == 1 and email.count(".") >= 1:
            break

    while True:
        number = input("Enter your mobile number: ")
        if number == "0":
            os.system('cls')
            homescreen()
            return
        if number.isnumeric():  # Number is numeric
            break

    while True:
        # Hide password whilst typing
        password = maskpass.askpass(prompt="Password:", mask="*")
        if password == "0":
            os.system('cls')
            homescreen()
            return

        if password:
            break

    # Client object created
    new_client = Client(
        username, [fname, lname, email, number])
    if register_client(new_client, password) != "Error communicating with server":
        print("Account Registered! \n")
        time.sleep(1)
        os.system('cls')
        login_screen()
    else:
        print("Error communicating with server")


def dashboard(client):
    """
    Main dashboard once a user successfully logs in
    """
    details = client.get_contact_info()
    print("Welcome", details[0], details[1]+"!\n")  # Displays full name
    print("Dashboard\n")
    print("Options:")
    print("   1. View/TopUp Balance")
    print("   2. Money Transfer")
    print("   3. View/Edit Own Details")
    print("   4. View Communications")
    print("   5. Logout")

    while True:
        choice = input("Enter choice: ")

        if choice == "1":
            print("Balance: £100")

        elif choice == "2":
            print("Transfer System Status: Currently Down")

        elif choice == "3":
            edit_screen(client)
            return

        elif choice == "4":
            communications_screen(client)

        elif choice == "5":
            homescreen()
            return

        else:
            print("Enter a valid option:")


def edit_screen(client):
    """
    The screen that appears when option 3 selected in dashboard.
    This screen allows users to view and edit their personal details except for their username.
    """
    os.system('cls')
    while True:
        print("Personal Details:")
        print("  Username:", client.get_username())
        print("  Editable:")
        print("  1. First Name:", client.get_contact_info()[0])
        print("  2. Last Name:", client.get_contact_info()[1])
        print("  3. Email:", client.get_contact_info()[2])
        print("  4. Mobile Number:", client.get_contact_info()[3])
        print("  5. Change Password")
        print("  6. Back to dashboard")
        choice = input("Enter option number: ")
        try:
            if choice == "1":
                new_first_name = input("Enter new first name: ")
                if new_first_name.isalpha():
                    client.set_fname(new_first_name)
                    if modify(client) == "SAVED":  # Sends server request to modify
                        print("First name updated!\n")
                else:
                    print("Invalid first name entered!\n")

            elif choice == "2":
                new_last_name = input("Enter new last name: ")
                if new_last_name.isalpha():
                    client.set_lname(new_last_name)
                    if modify(client) == "SAVED":
                        print("Last name updated!\n")
                else:
                    print("Invalid last name entered!\n")

            elif choice == "3":
                new_email = input("Enter new email: ")
                if new_email():
                    client.set_email(new_email)
                    if modify(client) == "SAVED":
                        print("Email updated!\n")
                else:
                    print("Invalid email entered!\n")

            elif choice == "4":
                new_number = input("Enter new mobile number: ")
                if new_number.isnumeric():
                    client.set_number(new_number)
                    if modify(client) == "SAVED":
                        print("Mobile number updated!\n")
                else:
                    print("Invalid last name entered!\n")

            elif choice == "5":

                old_password = maskpass.askpass(
                    prompt="Enter current password:", mask="*")
                # Checks if their entered password was their old one or not
                if attempt_login(client.get_username(), old_password).startswith('LOGIN_SUCCESS'):
                    new_password = maskpass.askpass(
                        prompt="Enter new password:", mask="*")
                    confirm_password = maskpass.askpass(
                        prompt="Re-enter new password:", mask="*")
                    if new_password == confirm_password:
                        value = modify(client, new_password) # CSV file is edited to reflect the new hashed password
                        # CSV file is edited to reflect the new hashed password
                        if value == "SAVED":
                            print("Password updated successfully.\n")
                    else:
                        print("Passwords do not match.\n")
                else:
                    print("Incorrect current password.\n")

            elif choice == "6":
                os.system('cls')
                dashboard(client)
            else:
                print("Invalid option. Please try again.\n")
        except:
            print("Error with server.\n")


def communications_screen(client):
    """
    This function allows a user to see communications from the company.
    """
    os.system('cls')
    print("Communications:")
    print(communicate())
    while True:
        choice = input("\nEnter 0 to go back: ")
        if choice == "0":
            os.system('cls')
            dashboard(client)


startscreen()
homescreen()
