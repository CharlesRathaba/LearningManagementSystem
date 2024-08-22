# Learning Management System

This project is a simple Learning Management System (LMS) built using Python with a graphical user interface (GUI) powered by Tkinter. The system allows users to manage student data, including viewing, adding, updating, and deleting student records. Additionally, the system provides a feature to analyze student data using custom SQL queries.

## Features

- **View All Students**: Display all student records stored in the database.
- **Add Student**: Add new students to the database.
- **Look Up Student**: Search for a student by student number, first name, or last name.
- **Update Student**: Modify the details of an existing student.
- **Delete Student**: Remove a student from the database.
- **Analyze Data**: Run custom SQL queries on the database to analyze student data.

## Project Structure

The project is organized into the following files:

- **`database.py`**: Handles database connection and query execution using `pyodbc`.
- **`ui.py`**: Contains the GUI implementation for the LMS using Tkinter.
- **`utils.py`**: Provides utility functions for data validation and formatting.
- **`main.py`**: The main entry point for the application.

## Requirements

- Python 3.x
- `pyodbc` library
- Microsoft SQL Server

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/CharlesRathaba/learning-management-system.git
    cd learning-management-system
    ```

2. **Install the required Python packages:**

    ```bash
    pip install pyodbc
    ```

3. **Configure the database connection:**

    In the `database.py` file, update the `DB_CONFIG` dictionary with your database settings:

    ```python
    DB_CONFIG = {
        'DRIVER': 'SQL Server',
        'SERVER': 'your_server_name',
        'DATABASE': 'LearningManagementSystem',
        'Trusted_Connection': 'yes'
    }
    ```

4. **Run the application:**

    ```bash
    python main.py
    ```

## Usage

- **Home Screen**: Navigate through the options to view, add, look up, update, or delete student records, or to analyze data.
- **View All Students**: Displays a list of all students with their details.
- **Add Student**: Provides a form to input and save a new student's details.
- **Look Up Student**: Search for a student by entering their student number, first name, or last name.
- **Update Student**: After looking up a student, modify their details and save the changes.
- **Delete Student**: Permanently remove a student from the database.
- **Analyze Data**: Enter a custom SQL query to analyze the data in the `Students` table.


## Contributing

Feel free to contribute to this project by creating a pull request.

