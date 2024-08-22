import re

def validate_date(date_str):
    """Validate the date format YYYY-MM-DD."""
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if re.match(pattern, date_str):
        return True
    return False

def validate_grade(grade_str):
    """Validate that the grade is a number between 0 and 100."""
    try:
        grade = float(grade_str)
        if 0 <= grade <= 100:
            return True
    except ValueError:
        pass
    return False

def format_student_data(student):
    """Format student data for display."""
    formatted_data = {
        "Student Number": student[0],
        "First Name": student[1],
        "Last Name": student[2],
        "Gender": student[3],
        "Address": student[4],
        "Date of Birth": student[5],
        "Grade Python": student[6],
        "Grade Azure Fundamentals": student[7],
        "Grade Azure AI": student[8],
        "Grade Power BI": student[9],
        "Qualification": student[10],
        "Average Grade": f"{student[11]:.2f}"
    }
    return formatted_data
