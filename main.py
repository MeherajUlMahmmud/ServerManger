import tkinter as tk
import subprocess

# Create the main application window
app = tk.Tk()
app.title("Server Manager")

# Set the initial window size (width x height)
app.geometry("600x400")

# Diiable window resizing
app.resizable(0, 0)

# Function to open PuTTY with pre-filled username and password


def open_putty(ip, username, password):
    # Launch PuTTY with pre-filled values
    # Replace 'putty.exe' with the correct PuTTY executable path
    cmd = f'putty.exe -ssh {ip} -l {username} -pw {password}'
    subprocess.Popen(cmd, shell=True)

# Function to read server information from a text file


def read_server_info():
    server_list = []
    with open('servers.txt', 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 5:
                ip, port, username, password, server_name = parts
                server_list.append((ip, username, password, server_name))
    return server_list

# Function to refresh the server list with clickable buttons


def refresh_server_list():
    servers = read_server_info()

    for i, server in enumerate(servers):
        ip, username, password, server_name = server
        row_num = i // 5  # Place 5 buttons in each row
        col_num = i % 5   # Arrange buttons in 5 columns
        tk.Button(server_frame, text=server_name, command=lambda i=ip, u=username, p=password: open_putty(
            i, u, p)).grid(row=row_num, column=col_num, pady=5, padx=10)


# Create a frame for the server list
server_frame = tk.Frame(app)
server_frame.pack()

# Refresh the server list
refresh_server_list()

# Start the Tkinter main loop
app.mainloop()
