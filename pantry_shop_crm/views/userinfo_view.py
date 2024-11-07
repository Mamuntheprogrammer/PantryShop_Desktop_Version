import tkinter as tk
from tkinter import ttk, messagebox

class UserInfoView:
    def __init__(self, root, user_data, refresh_callback, submit_callback, back_callback, logout_callback):
        self.root = root
        self.user_data = user_data  # Dictionary with user data
        self.refresh_callback = refresh_callback
        self.submit_callback = submit_callback
        self.back_callback = back_callback
        self.logout_callback = logout_callback

        self.root.title("User Information")
        self.root.geometry("800x450")
        self.root.config(bg="#f4f4f4")

        # Main frame container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Frame for displaying user information in a modern table style
        info_frame = ttk.Frame(main_frame, padding="10", style="Card.TFrame")
        info_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Title for User Information Section (centered)
        ttk.Label(info_frame, text="User Information", font=("Helvetica", 14, "bold"), foreground="#4CAF50").grid(row=0, column=0, columnspan=2, pady=10, sticky="n", padx=(0, 0))

        # Treeview for displaying user data in a structured format
        self.user_tree = ttk.Treeview(info_frame, columns=("field", "value"), show="headings", height=10)
        self.user_tree.heading("field", text="Field")
        self.user_tree.heading("value", text="Value")
        self.user_tree.column("field", width=150, anchor="w")
        self.user_tree.column("value", width=250, anchor="w")
        self.user_tree.grid(row=1, column=0, padx=5, pady=5)

        # Refresh Button (positioned below the treeview)
        ttk.Button(info_frame, text="Refresh", command=self.refresh_data).grid(row=2, column=0, pady=10, sticky="e")

        # Frame for updating user information
        form_frame = ttk.Frame(main_frame, padding="10", style="Card.TFrame")
        form_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Title for form
        ttk.Label(form_frame, text="Update Information", font=("Helvetica", 14, "bold"), foreground="#4CAF50").grid(row=0, column=0, columnspan=2, pady=10)

        # Initialize fields dictionary
        self.fields = {}

        # User Information Form with aligned fields
        for idx, field in enumerate(["first_name", "last_name", "email", "departname", "phone", "age", "max_hour", "reference", "student_status"]):
            label = ttk.Label(form_frame, text=field.replace("_", " ").title(), anchor="e", width=15)
            label.grid(row=idx+1, column=0, sticky="e", pady=2, padx=(5, 10))
            
            entry = ttk.Entry(form_frame, width=25)
            entry.grid(row=idx+1, column=1, pady=2, padx=(10, 5))
            self.fields[field] = entry

        # Submit Button
        ttk.Button(form_frame, text="Submit", command=self.handle_submit).grid(row=len(self.fields)+1, column=0, columnspan=2, pady=10)

        # Bottom navigation buttons
        nav_frame = ttk.Frame(main_frame, padding="10")
        nav_frame.grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Button(nav_frame, text="Back", width=15, command=self.back_callback).grid(row=0, column=0, padx=5)
        ttk.Button(nav_frame, text="Logout", width=15, command=self.logout_callback).grid(row=0, column=1, padx=5)

        # Apply styles
        style = ttk.Style()
        style.configure("Card.TFrame", background="#ffffff", borderwidth=2, relief="groove")

        # Load initial data into the display
        self.load_user_data()

    def load_user_data(self):
        """Load user data into the display table and form fields."""
        # Clear the treeview first
        for row in self.user_tree.get_children():
            self.user_tree.delete(row)
        
        # Display user data in the treeview
        for field, value in self.user_data.items():
            self.user_tree.insert("", "end", values=(field.replace("_", " ").title(), value))

        # Pre-fill form fields with existing data
        for field, entry in self.fields.items():
            entry.delete(0, "end")
            if field in self.user_data:
                entry.insert(0, self.user_data[field])

    def refresh_data(self):
        """Refreshes data from the refresh callback."""
        self.refresh_callback()
        self.load_user_data()

    def handle_submit(self):
        """Handles the form submission."""
        updated_data = {field: entry.get() for field, entry in self.fields.items()}
        if messagebox.askyesno("Confirm Update", "Are you sure you want to update your information?"):
            self.submit_callback(updated_data)

# Example usage
if __name__ == "__main__":
    root = tk.Tk()

    # Mock user data for testing
    user_data = {
        "id": 1,
        "username": "john_doe",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "user_type": "student",
        "departname": "Computer Science",
        "phone": "1234567890",
        "age": 22,
        "max_hour": 40,
        "reference": "Prof. Smith",
        "student_status": "Active",
        "auth_otp": None
    }

    def refresh():
        print("Refreshing data...")  # Add real refresh logic here

    def submit(updated_data):
        print("Submitted data:", updated_data)  # Add real submission logic here

    def go_back():
        print("Back button clicked")

    def logout():
        print("Logout button clicked")

    UserInfoView(root, user_data, refresh, submit, go_back, logout)
    root.mainloop()
