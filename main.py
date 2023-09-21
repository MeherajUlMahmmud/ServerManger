import tkinter as tk
import sqlite3
import subprocess

# Create the main application window
app = tk.Tk()
app.title("Server Manager")

# Set the initial window size (width x height)
app.geometry("600x400")

# Create a SQLite database (or use file-based storage)
conn = sqlite3.connect("servers.db")
cursor = conn.cursor()

# Create a table to store server information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS servers (
        id INTEGER PRIMARY KEY,
        serverName TEXT NOT NULL,
        serverIp TEXT NOT NULL,
        serverPort INTEGER NOT NULL,
        serverUsername TEXT NOT NULL,
        serverPassword TEXT NOT NULL
    )
''')
conn.commit()

# Function to open PuTTY with pre-filled username and password


def open_putty(server_name):
    cursor.execute(
        "SELECT serverIp, serverUsername, serverPassword FROM servers WHERE serverName=?", (server_name,))
    server_info = cursor.fetchone()
    if server_info:
        ip, username, password = server_info
        # Launch PuTTY with pre-filled values
        # Replace 'putty.exe' with the correct PuTTY executable path
        cmd = f'putty.exe -ssh {ip} -l {username} -pw {password}'
        subprocess.Popen(cmd, shell=True)
    else:
        tk.messagebox.showerror("Error", "Server information not found!")

# Function to open the "Add Server" window


def open_add_server_window():
    add_server_window = tk.Toplevel(app)
    add_server_window.title("Add New Server")

    # Create entry fields for server information
    tk.Label(add_server_window, text="Server Name:").pack()
    server_name_entry = tk.Entry(add_server_window)
    server_name_entry.pack()

    tk.Label(add_server_window, text="Server IP:").pack()
    server_ip_entry = tk.Entry(add_server_window)
    server_ip_entry.pack()

    tk.Label(add_server_window, text="Server Port:").pack()
    server_port_entry = tk.Entry(add_server_window)
    server_port_entry.pack()

    tk.Label(add_server_window, text="Username:").pack()
    server_username_entry = tk.Entry(add_server_window)
    server_username_entry.pack()

    tk.Label(add_server_window, text="Password:").pack()
    server_password_entry = tk.Entry(add_server_window, show="*")
    server_password_entry.pack()

    # Function to add the server to the database
    def add_server():
        name = server_name_entry.get()
        ip = server_ip_entry.get()
        port = int(server_port_entry.get())
        username = server_username_entry.get()
        password = server_password_entry.get()

        cursor.execute("INSERT INTO servers (serverName, serverIp, serverPort, serverUsername, serverPassword) VALUES (?, ?, ?, ?, ?)",
                       (name, ip, port, username, password))
        conn.commit()

        # Close the "Add Server" window
        add_server_window.destroy()

        # Refresh the server list
        refresh_server_list()

    # Create a button to add the server
    tk.Button(add_server_window, text="Add Server", command=add_server).pack()

# Function to refresh the server list with clickable buttons


def refresh_server_list():
    for widget in server_frame.winfo_children():
        widget.destroy()

    cursor.execute("SELECT serverName FROM servers")
    server_names = cursor.fetchall()

    for i, server_name in enumerate(server_names):
        server_name = server_name[0]
        row_num = i // 3  # Place 3 buttons in each row
        col_num = i % 3   # Arrange buttons in 3 columns
        tk.Button(server_frame, text=server_name, command=lambda name=server_name: open_putty(
            name)).grid(row=row_num, column=col_num, pady=5, padx=10)


# Create a "Create" button to open the "Add Server" window
create_button = tk.Button(app, text="Add New Server",
                          command=open_add_server_window)
create_button.pack()

# Create a frame for the server list
server_frame = tk.Frame(app)
server_frame.pack()

# Refresh the server list
refresh_server_list()

# Start the Tkinter main loop
app.mainloop()
