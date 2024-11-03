#Login System By Kavyashreni#

import tkinter as tk
from tkinter import messagebox
import json
import random
import string

# Constants for colors and styling
PRIMARY_COLOR = "#4CAF50"  # Green for buttons
SECONDARY_COLOR = "#F0F0F0"  # Light background for frame
TEXT_COLOR = "#000000"  # Black text
CAPTCHA_COLOR = "#333333"  # Dark CAPTCHA text
DATA_FILE = "user_data.json"

def load_users():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f)

def toggle_password(entry):
    """Toggle the visibility of the password in the entry widget."""
    if entry.cget('show') == '*':
        entry.config(show="")
    else:
        entry.config(show="*")

def refresh_captcha():
    global captcha_code
    captcha_code = ''.join(random.choices(string.digits, k=4))
    captcha_label.config(text=f"CAPTCHA: {captcha_code}")

def login():
    username = username_entry.get().strip()
    password = password_entry.get()
    entered_captcha = captcha_entry.get().strip()
    users = load_users()

    if users.get(username) == password and entered_captcha == captcha_code:
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        open_dashboard(username)
    elif entered_captcha != captcha_code:
        messagebox.showerror("Error", "Invalid CAPTCHA.")
    else:
        messagebox.showerror("Error", "Invalid username or password.")

def register():
    username = username_entry.get().strip()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Username and password cannot be empty.")
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match.")
        return

    users = load_users()
    if username in users:
        messagebox.showerror("Error", "Username already exists.")
    else:
        users[username] = password
        save_users(users)
        messagebox.showinfo("Success", "Registration successful!")

def change_password(username):
    new_password = new_password_entry.get()
    confirm_password = confirm_password_entry.get()
    if new_password and new_password == confirm_password:
        users = load_users()
        users[username] = new_password
        save_users(users)
        messagebox.showinfo("Success", "Password changed successfully!")
    else:
        messagebox.showerror("Error", "Passwords do not match.")

def delete_account(username):
    users = load_users()
    if username in users:
        del users[username]
        save_users(users)
        messagebox.showinfo("Account Deleted", "Your account has been deleted.")
        window.quit()

def open_dashboard(username):
    dashboard = tk.Toplevel(window)
    dashboard.title("User Dashboard")
    dashboard.geometry("300x400")
    tk.Label(dashboard, text=f"Welcome, {username}!", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Button(dashboard, text="Change Password", bg=PRIMARY_COLOR, fg="white", 
              command=lambda: show_change_password(dashboard, username)).pack(pady=5)

    tk.Button(dashboard, text="Delete Account", bg="red", fg="white", 
              command=lambda: delete_account(username)).pack(pady=5)

def show_change_password(dashboard, username):
    global new_password_entry, confirm_password_entry
    
    tk.Label(dashboard, text="New Password:", font=("Arial", 12), bg=SECONDARY_COLOR).pack(pady=5)
    new_password_entry = tk.Entry(dashboard, show="*", width=25)
    new_password_entry.pack(pady=5)

    tk.Label(dashboard, text="Confirm Password:", font=("Arial", 12), bg=SECONDARY_COLOR).pack(pady=5)
    confirm_password_entry = tk.Entry(dashboard, show="*", width=25)
    confirm_password_entry.pack(pady=5)

    # Single Show Password Checkbox
    show_password_checkbox = tk.Checkbutton(dashboard, text="Show Password", bg=SECONDARY_COLOR,
                                             command=lambda: [toggle_password(new_password_entry), toggle_password(confirm_password_entry)])
    show_password_checkbox.pack(pady=5)

    change_button = tk.Button(dashboard, text="Confirm Change", bg=PRIMARY_COLOR, fg="white",
                               command=lambda: change_password(username))
    change_button.pack(pady=5)


# Root Window Configuration
window = tk.Tk()
window.title("Login Dashboard")
window.geometry("400x550")  # Adjusted height for registration fields
window.config(bg="white")

# Login Frame
login_frame = tk.Frame(window, bg=SECONDARY_COLOR, bd=1, relief="solid", padx=20, pady=20)
login_frame.place(relx=0.5, rely=0.5, anchor="center")

# Buttons for Login and Register
button_frame = tk.Frame(login_frame, bg=SECONDARY_COLOR)
button_frame.grid(row=0, column=0, columnspan=2, pady=10)

login_button = tk.Button(button_frame, text="Login", bg=PRIMARY_COLOR, fg="white", width=10, command=login)
login_button.grid(row=0, column=0, padx=5)

register_button = tk.Button(button_frame, text="Register", bg=PRIMARY_COLOR, fg="white", width=10, command=register)
register_button.grid(row=0, column=1, padx=5)

# Username Field
tk.Label(login_frame, text="Username:", font=("Arial", 12, "bold"), bg=SECONDARY_COLOR).grid(row=1, column=0, sticky="e", pady=5, padx=5)
username_entry = tk.Entry(login_frame, width=25)
username_entry.grid(row=1, column=1, pady=5)

# Password Field
tk.Label(login_frame, text="Password:", font=("Arial", 12, "bold"), bg=SECONDARY_COLOR).grid(row=2, column=0, sticky="e", pady=5, padx=5)
password_entry = tk.Entry(login_frame, show="*", width=25)
password_entry.grid(row=2, column=1, pady=5)

# Confirm Password Field
tk.Label(login_frame, text="Confirm Password:", font=("Arial", 12, "bold"), bg=SECONDARY_COLOR).grid(row=3, column=0, sticky="e", pady=5, padx=5)
confirm_password_entry = tk.Entry(login_frame, show="*", width=25)
confirm_password_entry.grid(row=3, column=1, pady=5)

# Show Password Checkbox
show_password = tk.Checkbutton(login_frame, text="Show Password", bg=SECONDARY_COLOR, command=lambda: [toggle_password(password_entry), toggle_password(confirm_password_entry)])
show_password.grid(row=4, column=0, columnspan=2, pady=5)

# CAPTCHA Field
captcha_code = ''.join(random.choices(string.digits, k=4))
captcha_label = tk.Label(login_frame, text=f"CAPTCHA: {captcha_code}", font=("Arial", 12, "bold"), bg=SECONDARY_COLOR, fg=CAPTCHA_COLOR)
captcha_label.grid(row=5, column=0, sticky="e", padx=5, pady=5)

captcha_entry = tk.Entry(login_frame, width=25)
captcha_entry.grid(row=5, column=1, pady=5)

# Refresh CAPTCHA Button
refresh_button = tk.Button(login_frame, text="Refresh CAPTCHA", bg=PRIMARY_COLOR, fg="white", command=refresh_captcha)
refresh_button.grid(row=6, column=0, columnspan=2, pady=10)

# Start the GUI loop
window.mainloop()

#Login System By Kavyashreni#
