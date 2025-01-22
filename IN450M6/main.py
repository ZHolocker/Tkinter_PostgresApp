from tkinter import messagebox
import tkinter as tk
import psycopg2 as pg
from getpass import getpass


cx = pg.connect(host="localhost", database="IN450M2", user="postgres", password="Officer4532")

root = tk.Tk()
root.geometry("500x500")
root.title("IN450M2") #IN450M2 is the name of the database in my postgresql, change it to your database you want to use

# Create the cursor
c = cx.cursor()

# List rows function
def list_rows():
    list_rows_query = tk.Toplevel()
    list_rows_query.title("Number of Rows for in450a") #in450a, in450b, and in450c are all table names in my postgresql database
    list_rows_query.geometry("500x500")

    canvas = tk.Canvas(list_rows_query)
    scrollbar = tk.Scrollbar(list_rows_query, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    c.execute("SELECT COUNT(*) FROM in450a")
    result = c.fetchall()
    for x in result:
        rows_label = tk.Label(scrollable_frame, text=x)
        rows_label.pack()

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

# Retrieve first and last names
def retrieve_names():
    retrieve_names_query = tk.Toplevel()
    retrieve_names_query.title("First and last names from in450b")
    retrieve_names_query.geometry("1000x900")

    canvas = tk.Canvas(retrieve_names_query)
    scrollbar = tk.Scrollbar(retrieve_names_query, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    c.execute("SELECT first_name || ' ' || last_name as full_name FROM in450b")
    resultsb = c.fetchall()
    for x in resultsb:
        names_label = tk.Label(scrollable_frame, text=x)
        names_label.pack()

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

button2 = tk.Button(root, text="First and Last names", command=retrieve_names)
button2.pack(pady=10)

# List number of rows button
list_rows_button = tk.Button(root, text="Number of Rows", command=list_rows)
list_rows_button.pack(pady=20)



# Function to display data from a selected table
def display_table_data(table_name):
    table_data_window = tk.Toplevel(root)
    table_data_window.title(f"Data from {table_name}")
    table_data_window.geometry("1000x900")

    canvas = tk.Canvas(table_data_window)
    scrollbar = tk.Scrollbar(table_data_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    try:
        c.execute(f"SELECT * FROM {table_name}")
        columns = [desc[0] for desc in c.description]
        results = c.fetchall()

        # Display column names
        col_label = tk.Label(scrollable_frame, text=" | ".join(columns))
        col_label.pack()

        # Display rows
        for row in results:
            row_label = tk.Label(scrollable_frame, text=" | ".join(map(str, row)))
            row_label.pack()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

# Function to show tables from the database
def show_tables(username):
    table_window = tk.Toplevel(root)
    table_window.title("Tables")

    try:
        # Query to get all tables the user has access to
        c.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        """)
        results = c.fetchall()

        for table_name in results:
            table_button = tk.Button(table_window, text=table_name[0], command=lambda tn=table_name[0]: display_table_data(tn))
            table_button.pack()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Login function
def login():
    global cx, c
    username = username_entry.get()
    password = password_entry.get()
    host = host_entry.get()  # Prompt for database host

    if username in users and users[username] == password:
        try:
            cx = pg.connect(host=host, database="IN450M2", user=username, password=password)
            c = cx.cursor()
            messagebox.showinfo("Login Success", f"Welcome {username}")
            show_tables(username)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    else:
        messagebox.showerror("Login Failed", "Invalid credentials")

# User credentials
users = {
    "usera": "Officer4532",
    "userb": "Officer4532",
    "userc": "Officer4532"
}

# Initial setup for the login window
login_window = tk.Tk()
login_window.title("Login")

tk.Label(login_window, text="Username").pack()
username_entry = tk.Entry(login_window)
username_entry.pack()

tk.Label(login_window, text="Password").pack()
password_entry = tk.Entry(login_window, show="*")
password_entry.pack()

tk.Label(login_window, text="Host").pack()  # Add host prompt to the login window
host_entry = tk.Entry(login_window)
host_entry.pack()

login_button = tk.Button(login_window, text="Login", command=login)
login_button.pack()

login_window.mainloop()