# In admin_view.py

import tkinter as tk
from tkinter import ttk

class AdminView:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard")
        self.root.geometry("900x600")
        self.create_admin_dashboard()

    def create_admin_dashboard(self):
        # Example Admin dashboard UI
        dashboard_frame = ttk.Frame(self.root, padding="20")
        dashboard_frame.pack(padx=20, pady=30)

        # Admin Dashboard Title
        ttk.Label(dashboard_frame, text="Admin Dashboard", font=("Helvetica", 18, "bold"), foreground="#4CAF50").grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Example buttons for the Admin
        ttk.Button(dashboard_frame, text="Manage Users", width=20).grid(row=1, column=0, pady=10)
        ttk.Button(dashboard_frame, text="Manage Orders", width=20).grid(row=2, column=0, pady=10)
        ttk.Button(dashboard_frame, text="View Reports", width=20).grid(row=3, column=0, pady=10)
        ttk.Button(dashboard_frame, text="Logout", width=20, command=self.logout).grid(row=4, column=0, pady=10)

    def logout(self):
        self.root.destroy()  # Close the admin window
        # Optionally, you can go back to the login screen here if needed.
