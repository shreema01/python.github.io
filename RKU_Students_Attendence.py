# --------------------------------------------Admin log in and registration----------------------

import tkinter as tk
import mysql.connector
from tkinter import messagebox

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="rku_attendence_admin"
)

# Create the main window
root = tk.Tk()

# Set the window title and size
root.title("RKU Student Attendance System")
root.geometry("500x400")

# Add a label with the university name
label = tk.Label(root, text="Welcome to RKU Attendance System",
                 font=("Arial", 20))
label.pack(pady=20)

# Add a label and entry for username
username_label = tk.Label(root, text="Username", font=("Arial", 14))
username_label.pack()
username_entry = tk.Entry(root, font=("Arial", 14))
username_entry.pack()

# Add a label and entry for password
password_label = tk.Label(root, text="Password", font=("Arial", 14))
password_label.pack()
password_entry = tk.Entry(root, show="*", font=("Arial", 14))
password_entry.pack()

# Add a button to log in as admin


def login():
    # Retrieve the values entered in the username and password entry fields
    username = username_entry.get()
    password = password_entry.get()

    # Query the MySQL database to check if the username and password match an admin account
    cursor = db.cursor()
    query = "SELECT * FROM admin WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        status_label.config(text="Login successful", fg="green")
    else:
        status_label.config(text="Login failed", fg="red")


def login_as_admin():
    class Student:
        def __init__(self, name, roll, major):
            self.name = name
            self.roll = roll
            self.major = major

    class StudentRegistrationApp:
        def __init__(self, master):
            self.master = master
            master.title("RKU Attendance System")
            master.geometry("500x530")

            # Connect to the MySQL database
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="rku_attendence_admin"
            )
            self.cursor = self.db.cursor()

            # Create IT and CE student lists
            self.it_students = []
            self.ce_students = []

            # Create header frame and welcome label
            header_frame = tk.Frame(master)
            header_frame.pack(side=tk.TOP, pady=10)
            tk.Label(header_frame, text="Welcome to RKU Server",
                     font=("Arial", 16)).pack()

            # Create labels and entry fields for name, roll, and major
            tk.Label(master, text="Name").pack()
            self.name_entry = tk.Entry(master)
            self.name_entry.pack()

            tk.Label(master, text="Roll").pack()
            self.roll_entry = tk.Entry(master)
            self.roll_entry.pack()

            tk.Label(master, text="Major").pack()
            self.major_var = tk.StringVar(value="IT")
            self.major_dropdown = tk.OptionMenu(
                master, self.major_var, "IT", "CE")
            self.major_dropdown.pack()

            # Create button for registering student
            self.register_button = tk.Button(
                master, text="Register", command=self.register_student)
            self.register_button.pack(pady=10)

            # -------------------Start-----------------------------------------------------------------#

            def take_attendance_callback_function():
                import tkinter as tk
                import mysql.connector
                from tkinter import messagebox

                # Establishing connection with the database
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="rku_attendence_admin"
                )

                # Creating a cursor object
                mycursor = mydb.cursor()
                student_data = None
                division_name_table = None
                attendance_status_boolean = []

                # Defining the function to display the student data with tick marks for attendance

                def display_attendance(table_name):
                    global attendance_status_boolean, student_data
                    attendance_status_boolean = []
                    # Fetching the student data from the table
                    mycursor.execute("SELECT * FROM " + table_name)
                    student_data = mycursor.fetchall()

                    # Defining the function to update attendance status
                    def update_attendance_status(i, value):
                        attendance_status_boolean[i] = value

                    # Clearing the previous data from the frame
                    for widget in frame.winfo_children():
                        widget.destroy()

                    # Creating the table headers
                    headers = ["Roll No.", "Name", "Attendance"]
                    for j, header in enumerate(headers):
                        label = tk.Label(frame, text=header)
                        label.grid(row=0, column=j)

                    # Creating a table to display the student data with tick marks for attendance
                    for i in range(len(student_data)):
                        # Displaying the roll number
                        label = tk.Label(frame, text=str(student_data[i][0]))
                        label.grid(row=i+1, column=0)

                        # Displaying the name
                        label = tk.Label(frame, text=str(student_data[i][1]))
                        label.grid(row=i+1, column=1)

                        # Creating a checkbox to mark attendance
                        attendance_var = tk.BooleanVar()
                        attendance_var.set(False)
                        attendance_checkbox = tk.Checkbutton(
                            frame, variable=attendance_var, command=lambda i=i, v=attendance_var.get(): update_attendance_status(i, v))
                        attendance_checkbox.grid(row=i+1, column=2)
                        attendance_status_boolean.append(
                            False)  # set initial value to False

                # Defining the function to handle the submission of attendance data

                def submit_attendance():
                    # Getting the faculty, division, and date
                    global attendance_status_boolean, student_data, division_name_table
                    faculty = faculty_entry.get()
                    division = dropdown_var.get()
                    date = date_entry.get()

                    # Creating a list of tuples containing student data and attendance status
                    final_status = list(
                        zip(student_data, attendance_status_boolean))

                    # Inserting attendance data into the database
                    for query in final_status:
                        try:
                            id = query[0][0]
                            name = query[0][1]
                            if False in query:
                                query = f"INSERT INTO attendance VALUES ('{faculty}', '{division}', '{date}', '{name}','{id}', 'Absent');"
                                mycursor.execute(query)
                                mydb.commit()
                            elif True in query:
                                query = f"INSERT INTO attendance VALUES ('{faculty}', '{division}', '{date}', '{name}','{id}', 'Present');"
                                mycursor.execute(query)
                                mydb.commit()
                        except Exception:
                            messagebox.showerror("Error", "Error Occured")
                            return
                    messagebox.showinfo(
                        "Success", "Attendance Updated Successfully")

                # Defining the function to handle the selection from the dropdown menu

                def handle_dropdown(selection):
                    global division_name_table
                    if selection == "IT":
                        display_attendance("it_students")
                        division_name_table = "it_students"
                    elif selection == "CE":
                        display_attendance("ce_students")
                        division_name_table = "ce_students"

                    # Creating the Tkinter window
                root = tk.Tk()
                root.title("RKU Attendance")
                root.geometry("500x400")

                # Adding the RKU server label
                rku_server_label = tk.Label(
                    root, text="Welcome to RKU Server", font=("Arial", 20))
                rku_server_label.pack()

                faculty_frame = tk.Frame(root)
                faculty_frame.pack()
                faculty_label = tk.Label(faculty_frame, text="Faculty:")
                faculty_label.pack(side="left", anchor="w")
                faculty_entry = tk.Entry(faculty_frame)
                faculty_entry.pack(side="left")

                # Creating the Date label and entry
                date_frame = tk.Frame(root)
                date_frame.pack()
                date_label = tk.Label(date_frame, text="Date:")
                date_label.pack(side="left", anchor="w")
                date_entry = tk.Entry(date_frame)
                date_entry.pack(side="left")

                # Creating a frame for the label and dropdown menu
                dropdown_frame = tk.Frame(root)
                dropdown_frame.pack()

                # Creating the label for the dropdown menu
                division_label = tk.Label(dropdown_frame, text="Division:")
                division_label.pack(side="left", anchor="w")

                # Creating the dropdown menu for IT and CE
                options = ["IT", "CE"]
                dropdown_var = tk.StringVar(root)
                dropdown_var.set(options[0])
                dropdown_menu = tk.OptionMenu(
                    dropdown_frame, dropdown_var, *options, command=handle_dropdown)
                dropdown_menu.pack(side="left")

                # Creating a frame to display the data
                frame = tk.Frame(root)
                frame.pack()

                # Creating the submit button
                submit_button = tk.Button(
                    root, text="Submit Attendance", command=submit_attendance)
                submit_button.pack()

                # Starting the Tkinter main loop
                root.mainloop()

            take_attendance_button = tk.Button(
                master, text="Take Attendance", command=take_attendance_callback_function)

            take_attendance_button.pack(pady=10)

            # Create reset button
            self.reset_button = tk.Button(
                master, text="Reset", command=self.reset_fields)
            self.reset_button.pack(pady=10)

            # Create label for displaying registered students
            tk.Label(master, text="Registered Students").pack()
            self.student_listbox = tk.Listbox(master)
            self.student_listbox.pack()

        def register_student(self):
            name = self.name_entry.get()
            roll = self.roll_entry.get()
            major = self.major_var.get()
            if major == "IT":
                student = Student(name, roll, "IT")
                self.it_students.append(student)
                # Store IT student data to the database
                query = "INSERT INTO it_students (name, roll) VALUES (%s, %s)"
                values = (name, roll)
                self.cursor.execute(query, values)
                self.db.commit()
            else:
                student = Student(name, roll, "CE")
                self.ce_students.append(student)
                # Store CE student data to the database
                query = "INSERT INTO ce_students (name, roll) VALUES (%s, %s)"
                values = (name, roll)
                self.cursor.execute(query, values)
                self.db.commit()
            self.student_listbox.delete(0, tk.END)
            for student in self.it_students + self.ce_students:
                self.student_listbox.insert(
                    tk.END, f"{student.name} ({student.major}) - Roll No. {student.roll}")
            # Show success message
            messagebox.showinfo("Success", "Student registered successfully!")

        def reset_fields(self):
            self.name_entry.delete(0, tk.END)
            self.roll_entry.delete(0, tk.END)
            self.major_var.set("IT")
            self.student_listbox.delete

    root = tk.Tk()
    app = StudentRegistrationApp(root)
    root.mainloop()


login_button = tk.Button(root, text="Login as Admin", font=(
    "Arial", 16), width=20, height=2, command=login_as_admin)
login_button.pack(pady=10)

# Add a button to register as admin


def register():
    # Retrieve the values entered in the username and password entry fields
    username = username_entry.get()
    password = password_entry.get()

    # Insert a new admin account into the MySQL database
    cursor = db.cursor()
    query = "INSERT INTO admin (username, password) VALUES (%s, %s)"
    cursor.execute(query, (username, password))
    db.commit()

    status_label.config(text="Registration successful", fg="green")


register_button = tk.Button(root, text="Register as Admin", font=(
    "Arial", 16), width=20, height=2, command=register)
register_button.pack(pady=10)

# Add a label to display the login/registration status
status_label = tk.Label(root, text="", font=("Arial", 14))
status_label.pack(pady=10)

# Add a button to reset the username and password entry fields


def reset():
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)


reset_button = tk.Button(root, text="Reset", font=(
    "Arial", 12), width=10, command=reset)
reset_button.pack(pady=10)

# Run the main event loop
root.mainloop()

# Close the database connection
db.close()
