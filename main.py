import tkinter as tk
from ui import show_home

def main():
    root = tk.Tk()
    root.title("Learning Management System")
    root.geometry("800x600")
    show_home(root)
    root.mainloop()

if __name__ == "__main__":
    main()

