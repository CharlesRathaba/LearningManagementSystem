import pyodbc
from tkinter import messagebox

# Database connection settings
DB_CONFIG = {
    'DRIVER': 'SQL Server',
    'SERVER': 'ICT_RB_LT34',
    'DATABASE': 'LearningManagementSystem',
    'Trusted_Connection': 'yes'
}

def connect_db():
    try:
        conn = pyodbc.connect(
            f'DRIVER={{{DB_CONFIG["DRIVER"]}}};'
            f'SERVER={DB_CONFIG["SERVER"]};'
            f'DATABASE={DB_CONFIG["DATABASE"]};'
            f'Trusted_Connection={DB_CONFIG["Trusted_Connection"]}'
        )
        return conn
    except pyodbc.Error as e:
        messagebox.showerror("Database Connection Error", str(e))
        return None

def execute_query(query, params=None, fetch=False, fetch_columns=False):
    conn = connect_db()
    if not conn:
        return (None, None) if fetch_columns else None
    
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or [])
        
        if fetch:
            if fetch_columns:
                if cursor.description is None:
                    print("Cursor description is None.")
                    return None, None
                
                columns = [column[0] for column in cursor.description]
                rows = cursor.fetchall()
                return rows, columns
            else:
                rows = cursor.fetchall()
                return rows
        else:
            conn.commit()
            return None
    
    except pyodbc.Error as e:
        messagebox.showerror("Database Error", str(e))
        print("Error while executing query:", e)
        return (None, None) if fetch_columns else None
    
    finally:
        conn.close()

