import tkinter as tk
from tkinter import ttk, messagebox
from database import execute_query
from utils import validate_date, validate_grade, format_student_data

def clear_window(root):
    for widget in root.winfo_children():
        widget.destroy()

def show_home(root):
    clear_window(root)
    tk.Label(root, text="Welcome to FMTALI", font=("Helvetica", 20, "bold"), bg='#F5F5F5',
             fg="#003366").pack(pady=20)
    tk.Button(root, text="View All Students", command=lambda: view_all_students(root), bg="#0066CC",
              fg="#FFFFFF").pack(pady=10)
    tk.Button(root, text="Add Student", command=lambda: open_add_student_form(root), bg="#0066CC",
              fg="#FFFFFF").pack(pady=10)
    tk.Button(root, text="Look Up Student", command=lambda: open_lookup_student_form(root), bg="#0066CC",
              fg="#FFFFFF").pack(pady=10)
    tk.Button(root, text="Analyze Data", command=lambda: open_analyze_data_form(root), bg="#0066CC",
              fg="#FFFFFF").pack(pady=10)

def view_all_students(root):
    clear_window(root)
    query = """
        SELECT StudentNumber, FirstName, LastName, Gender, Address, DateOfBirth, Qualification,
               Grade_Python, Grade_Azure_Fundamentals, Grade_Azure_AI, Grade_Power_BI, Average_grade
        FROM Students
    """
    rows = execute_query(query, fetch=True)
    if rows is None:
        return

    columns = [
        "StudentNumber", "FirstName", "LastName", "Gender", "Address", "DateOfBirth", "Qualification",
        "Grade_Python", "Grade_Azure_Fundamentals", "Grade_Azure_AI", "Grade_Power_BI", "Average_grade"
    ]

    tree = ttk.Treeview(root, columns=columns, show="headings", style='Treeview')
    style = ttk.Style()
    style.configure('Treeview',
                    background='#FFFFFF',
                    foreground='#333333',
                    fieldbackground='#FFFFFF')
    style.configure('Treeview.Heading',
                    background='#E6F0FF',
                    foreground='#003366')

    column_widths = {
        "StudentNumber": 100,
        "FirstName": 120,
        "LastName": 120,
        "Gender": 60,
        "Address": 150,
        "DateOfBirth": 80,
        "Qualification": 150,
        "Grade_Python": 90,
        "Grade_Azure_Fundamentals": 110,
        "Grade_Azure_AI": 90,
        "Grade_Power_BI": 90,
        "Average_grade": 90
    }

    for col in columns:
        tree.heading(col, text=col.replace("_", " ").title())
        tree.column(col, width=column_widths.get(col, 100))

    tree.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    for row in rows:
        formatted_row = [
            str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]),
            str(row[6]), str(row[7]), str(row[8]), str(row[9]), str(row[10]), f"{row[11]:.2f}"
        ]
        tree.insert('', 'end', values=formatted_row)

    tk.Button(root, text="Back to Home", command=lambda: show_home(root), bg="#0066CC",
              fg="#FFFFFF").pack(pady=10)

def open_add_student_form(root):
    clear_window(root)

    tk.Label(root, text="Add New Student", font=("Helvetica", 16, "bold"), bg="#F5F5F5",
             fg="#003366").grid(row=0, column=0, columnspan=2, pady=10)

    labels = ["Student Number", "First Name", "Last Name", "Gender", "Address", "Date of Birth (YYYY-MM-DD)", "Qualification",
              "Grade Python", "Grade Azure Fundamentals", "Grade Azure AI", "Grade Power BI"]
    entries = []

    for idx, label in enumerate(labels, start=1):
        tk.Label(root, text=label, bg="#F5F5F5", fg="#333333").grid(row=idx, column=0, sticky="e", padx=5, pady=5)
        entry = tk.Entry(root, bg="#FFFFFF", fg="#333333")
        entry.grid(row=idx, column=1, padx=5, pady=5)
        entries.append(entry)

    tk.Button(root, text="Save", command=lambda: add_student(
        root, entries[0].get(), entries[1].get(), entries[2].get(), entries[3].get(),
        entries[4].get(), entries[5].get(), entries[6].get(), entries[7].get(),
        entries[8].get(), entries[9].get(), entries[10].get()
    ), bg="#0066CC", fg="#FFFFFF").grid(row=len(labels)+1, column=0, columnspan=2, pady=10)

    tk.Button(root, text="Back to Home", command=lambda: show_home(root), bg="#0066CC",
              fg="#FFFFFF").grid(row=len(labels)+2, column=0, columnspan=2, pady=10)

def open_lookup_student_form(root):
    clear_window(root)

    tk.Label(root, text="Look Up Student", font=("Helvetica", 16, "bold"), bg="#F5F5F5",
             fg="#003366").grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(root, text="Student Number", bg="#F5F5F5", fg="#333333").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    student_number_entry = tk.Entry(root, bg="#FFFFFF", fg="#333333")
    student_number_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(root, text="First Name", bg="#F5F5F5",
             fg="#333333").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    first_name_entry = tk.Entry(root, bg="#FFFFFF", fg="#333333")
    first_name_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(root, text="Last Name", bg="#F5F5F5",
             fg="#333333").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    last_name_entry = tk.Entry(root, bg="#FFFFFF", fg="#333333")
    last_name_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Button(root, text="Search", command=lambda: lookup_student(
        root, student_number_entry.get(), first_name_entry.get(), last_name_entry.get()
    ), bg="#0066CC", fg="#FFFFFF").grid(row=4, column=0, columnspan=2, pady=10)

    tk.Button(root, text="Back to Home", command=lambda: show_home(root), bg="#0066CC",
              fg="#FFFFFF").grid(row=5, column=0, columnspan=2, pady=10)

def lookup_student(root, student_number, first_name, last_name):
    query = """
        SELECT StudentNumber, FirstName, LastName, Gender, Address, DateOfBirth, Qualification,
               Grade_Python, Grade_Azure_Fundamentals, Grade_Azure_AI, Grade_Power_BI, Average_grade
        FROM Students
        WHERE StudentNumber = ? OR FirstName = ? OR LastName = ?
    """
    students = execute_query(query, (student_number, first_name, last_name), fetch=True)

    if students:
        clear_window(root)
        show_student_details(root, students[0])

    else:
        messagebox.showinfo("Search Result", "No student found.")
        tk.Button(root, text="Search Again", command=lambda: open_lookup_student_form(root), bg="#0066CC",
                  fg="#FFFFFF").pack(pady=10)
        tk.Button(root, text="Back to Home", command=lambda: show_home(root), bg="#0066CC",
                  fg="#FFFFFF").pack(pady=10)

def show_student_details(root, student):
    clear_window(root)
    tk.Label(root, text="Student Details", font=("Helvetica", 16, "bold"), bg="#F5F5F5",
             fg="#003366").grid(row=0, column=0, columnspan=2, pady=10)

    columns = [
        "Student Number", "First Name", "Last Name", "Gender", "Address", "Date of Birth", "Qualification"
        "Grade Python", "Grade Azure Fundamentals", "Grade Azure AI", "Grade Power BI", 
        "Average Grade"
    ]

    tree = ttk.Treeview(root, columns=columns, show="headings", style='Treeview')
    style = ttk.Style()
    style.configure('Treeview',
                    background='#FFFFFF',
                    foreground='#333333',
                    fieldbackground='#FFFFFF')
    style.configure('Treeview.Heading',
                    background='#E6F0FF',
                    foreground='#003366')

    column_widths = {
        "Student Number": 100,
        "First Name": 120,
        "Last Name": 120,
        "Gender": 60,
        "Address": 150,
        "Qualification": 150,
        "Date of Birth": 80,
        "Grade Python": 90,
        "Grade Azure Fundamentals": 110,
        "Grade Azure AI": 90,
        "Grade Power BI": 90,
        "Average Grade": 90
    }

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=column_widths.get(col, 100))

    tree.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

    formatted_row = [
        str(student[0]), str(student[1]), str(student[2]), str(student[3]), str(student[4]),
        str(student[5]), str(student[6]), str(student[7]), str(student[8]), str(student[9]),
        str(student[10]), f"{student[11]:.2f}"
    ]
    tree.insert('', 'end', values=formatted_row)

    tk.Button(root, text="Update Student", command=lambda: open_update_student_form(root, student), bg="#0066CC",
              fg="#FFFFFF").grid(row=2, column=0, pady=10)
    tk.Button(root, text="Delete Student", command=lambda: delete_student(root, student[0]), bg="#FF0000",
              fg="#FFFFFF").grid(row=2, column=1, pady=10)
    tk.Button(root, text="Search Another Student", command=lambda: open_lookup_student_form(root), bg="#0066CC",
              fg="#FFFFFF").grid(row=3, column=0, pady=10)
    tk.Button(root, text="Back to Home", command=lambda: show_home(root), bg="#0066CC",
              fg="#FFFFFF").grid(row=3, column=1, pady=10)

def open_update_student_form(root, student):
    clear_window(root)

    tk.Label(root, text="Update Student Details", font=("Helvetica", 16, "bold"), bg="#F5F5F5",
             fg="#003366").grid(row=0, column=0, columnspan=2, pady=10)

    labels = ["Student Number", "First Name", "Last Name", "Gender", "Address", "Date of Birth (YYYY-MM-DD)", "Qualification",
              "Grade Python", "Grade Azure Fundamentals", "Grade Azure AI", "Grade Power BI"]
    entries = []

    for idx, label in enumerate(labels, start=1):
        tk.Label(root, text=label, bg="#F5F5F5", fg="#333333").grid(row=idx, column=0, sticky="e", padx=5, pady=5)
        entry = tk.Entry(root, bg="#FFFFFF", fg="#333333")
        entry.grid(row=idx, column=1, padx=5, pady=5)
        entries.append(entry)

    # Prefill the entries with the current student data
    for entry, value in zip(entries, student):
        entry.insert(0, value)

    tk.Button(root, text="Save Changes", command=lambda: update_student(
        root, student[0], entries[1].get(), entries[2].get(), entries[3].get(), entries[4].get(),
        entries[5].get(), entries[6].get(), entries[7].get(), entries[8].get(), entries[9].get(),
        entries[10].get()
    ), bg="#0066CC", fg="#FFFFFF").grid(row=len(labels)+1, column=0, columnspan=2, pady=10)

    tk.Button(root, text="Back to Home", command=lambda: show_home(root), bg="#0066CC",
              fg="#FFFFFF").grid(row=len(labels)+2, column=0, columnspan=2, pady=10)

def add_student(root, student_number, first_name, last_name, gender, address, date_of_birth, qualification, grade_python, grade_azure_fundamentals, grade_azure_ai, grade_power_bi):
    if not validate_date(date_of_birth):
        messagebox.showerror("Invalid Input", "Date of Birth must be in YYYY-MM-DD format.")
        return
    if not validate_grade(grade_python) or not validate_grade(grade_azure_fundamentals) or not validate_grade(grade_azure_ai) or not validate_grade(grade_power_bi):
        messagebox.showerror("Invalid Input", "Grades must be numeric and between 0-100.")
        return

    query = """
        INSERT INTO Students (StudentNumber, FirstName, LastName, Gender, Address, DateOfBirth, Qualification, Grade_Python, Grade_Azure_Fundamentals, Grade_Azure_AI, Grade_Power_BI)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    parameters = (student_number, first_name, last_name, gender, address, date_of_birth, qualification, grade_python, grade_azure_fundamentals, grade_azure_ai, grade_power_bi)
    execute_query(query, parameters)

    messagebox.showinfo("Success", "Student added successfully.")
    show_home(root)

def update_student(root, original_student_number, first_name, last_name, gender, address, date_of_birth, qualification, grade_python, grade_azure_fundamentals, grade_azure_ai, grade_power_bi):
    if not validate_date(date_of_birth):
        messagebox.showerror("Invalid Input", "Date of Birth must be in YYYY-MM-DD format.")
        return
    if not validate_grade(grade_python) or not validate_grade(grade_azure_fundamentals) or not validate_grade(grade_azure_ai) or not validate_grade(grade_power_bi):
        messagebox.showerror("Invalid Input", "Grades must be numeric and between 0-100.")
        return

    query = """
        UPDATE Students
        SET FirstName = ?, LastName = ?, Gender = ?, Address = ?, DateOfBirth = ?, Qualification = ?, Grade_Python = ?, Grade_Azure_Fundamentals = ?, Grade_Azure_AI = ?, Grade_Power_BI = ?
        WHERE StudentNumber = ?
    """
    parameters = (first_name, last_name, gender, address, date_of_birth, qualification, grade_python, grade_azure_fundamentals, grade_azure_ai, grade_power_bi, original_student_number)
    execute_query(query, parameters)

    messagebox.showinfo("Success", "Student details updated successfully.")
    query = """
        SELECT StudentNumber, FirstName, LastName, Gender, Address, DateOfBirth, Qualification,
               Grade_Python, Grade_Azure_Fundamentals, Grade_Azure_AI, Grade_Power_BI, Average_grade
        FROM Students
        WHERE StudentNumber = ?
    """
    student = execute_query(query, (original_student_number,), fetch=True)[0]
    show_student_details(root, student)

def delete_student(root, student_number):
    confirmation = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?")
    if confirmation:
        query = "DELETE FROM Students WHERE StudentNumber = ?"
        execute_query(query, (student_number,))
        messagebox.showinfo("Success", "Student deleted successfully.")
        show_delete_confirmation(root)

def show_delete_confirmation(root):
    clear_window(root)
    tk.Label(root, text="Student deleted successfully.", font=("Helvetica", 16, "bold"), bg='#F5F5F5',
             fg="#003366").pack(pady=20)
    tk.Button(root, text="Search Another Student", command=lambda: open_lookup_student_form(root), bg="#0066CC",
              fg="#FFFFFF").pack(pady=10)
    tk.Button(root, text="Back to Home", command=lambda: show_home(root), bg="#0066CC",
              fg="#FFFFFF").pack(pady=10)


def open_analyze_data_form(root):
    clear_window(root)

    tk.Label(root, text="Analyze Data", font=("Helvetica", 16, "bold"), bg="#F5F5F5",
             fg="#003366").grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(root, text="Enter SQL Query:", bg="#F5F5F5", fg="#333333").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    query_entry = tk.Entry(root, bg="#FFFFFF", fg="#333333", width=50)
    query_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Button(root, text="Run Query", command=lambda: analyze_data(root, query_entry.get()), bg="#0066CC",
              fg="#FFFFFF").grid(row=2, column=0, columnspan=2, pady=10)

    tk.Button(root, text="Back to Home", command=lambda: show_home(root), bg="#0066CC",
              fg="#FFFFFF").grid(row=3, column=0, columnspan=2, pady=10)



def analyze_data(root, query):
    def go_back_home():
        clear_window(root)
        show_home(root)  # Use the existing show_home function

    def execute_another_query():
        clear_window(root)
        open_analyze_data_form(root)  # Function to open the analyze data form

    clear_window(root)

    if not query.strip():
        messagebox.showerror("Invalid Input", "Query cannot be empty.")
        open_analyze_data_form(root)
        return

    try:
        # Execute the query and fetch results
        rows, columns = execute_query(query, fetch=True, fetch_columns=True)

        if rows is None or columns is None:
            messagebox.showerror("Query Error", "An error occurred while executing the query.")
            open_analyze_data_form(root)
            return

        # If no results were returned, notify the user and return
        if not rows:
            messagebox.showinfo("No Results", "No results found for the query.")
            open_analyze_data_form(root)
            return

        # Clean up rows to remove any tuple formatting
        formatted_rows = [tuple(map(lambda x: str(x) if x is not None else '', row)) for row in rows]

        # Display results in a Treeview
        tree = ttk.Treeview(root, columns=columns, show="headings", style='Treeview')
        style = ttk.Style()
        style.configure('Treeview',
                    background='#FFFFFF',
                    foreground='#333333',
                    fieldbackground='#FFFFFF')
        style.configure('Treeview.Heading',
                    background='#E6F0FF',
                    foreground='#003366')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        for row in formatted_rows:
            tree.insert('', 'end', values=row)

        tree.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Buttons for additional actions
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        home_button = tk.Button(button_frame, text="Go Back Home", command=go_back_home, bg="#0066CC", fg="#FFFFFF")
        home_button.pack(side=tk.LEFT, padx=10)

        another_query_button = tk.Button(button_frame, text="Execute Another Query", command=execute_another_query, bg="#0066CC", fg="#FFFFFF")
        another_query_button.pack(side=tk.LEFT, padx=10)

    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        open_analyze_data_form(root)






