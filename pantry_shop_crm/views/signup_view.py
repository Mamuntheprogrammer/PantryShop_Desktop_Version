import tkinter as tk
from tkinter import ttk, messagebox
from controllers.signup_manager import SignupManager
import re


class SignupView:
    def __init__(self, root, show_login_screen_callback):
        self.root = root
        self.show_login_screen_callback = show_login_screen_callback
        self.signup_manager = SignupManager()
        self.root.title("Sign Up")
        self.root.geometry("1150x675")
        self.create_signup_form()

    def create_signup_form(self):
        # Frame for the signup form
        form_frame = ttk.Frame(self.root, padding="20")
        form_frame.pack(padx=20, pady=30)

        # Title Label
        ttk.Label(form_frame, text="Sign Up", font=("Helvetica", 18, "bold"), foreground="#4CAF50").grid(row=0, column=0, columnspan=4, pady=(0, 20))

        # Form fields
        self.fields = {
            "first_name": tk.Entry(form_frame, width=30),
            "last_name": tk.Entry(form_frame, width=30),
            "email_address": tk.Entry(form_frame, width=30),
            "password": tk.Entry(form_frame, width=30, show="*"),
            "mobile_number": tk.Entry(form_frame, width=30),
            "fulltime": tk.BooleanVar(),
            "parttime": tk.BooleanVar(),
            "undergraduate": tk.BooleanVar(),
            "graduate": tk.BooleanVar(),
            "work_per_week": tk.Entry(form_frame, width=30),
            "age_group": tk.Entry(form_frame, width=30),
            "role_type": tk.StringVar()  # for dropdown
        }

        # Left column fields
        left_fields = [
            ("First Name:", self.fields["first_name"]),
            ("Last Name:", self.fields["last_name"]),
            ("Email Address:", self.fields["email_address"]),
            ("Password:", self.fields["password"]),
            ("Mobile Number:", self.fields["mobile_number"])
        ]

        # Set default value for Role Type dropdown
        self.fields["role_type"].set("User")

        # Right column fields with checkboxes and dropdown
        right_fields = [
            ("Full-time:", tk.Checkbutton(form_frame, variable=self.fields["fulltime"])),
            ("Part-time:", tk.Checkbutton(form_frame, variable=self.fields["parttime"])),
            ("Undergraduate:", tk.Checkbutton(form_frame, variable=self.fields["undergraduate"])),
            ("Graduate:", tk.Checkbutton(form_frame, variable=self.fields["graduate"])),
            ("Work per Week:", self.fields["work_per_week"]),
            ("Age Group:", self.fields["age_group"]),
            ("Role Type:", ttk.Combobox(form_frame, textvariable=self.fields["role_type"], values=["Admin", "User"], width=27))
        ]

        # Place fields in grid
        for idx, (label, widget) in enumerate(left_fields):
            ttk.Label(form_frame, text=label, font=("Helvetica", 12)).grid(row=idx+1, column=0, sticky="w", pady=5)
            widget.grid(row=idx+1, column=1, padx=25, pady=5)

        for idx, (label, widget) in enumerate(right_fields):
            ttk.Label(form_frame, text=label, font=("Helvetica", 12)).grid(row=idx+1, column=2, sticky="w", pady=5)
            widget.grid(row=idx+1, column=3, padx=25, pady=5)

        # Bind phone number input to the format function and placeholder
        self.set_placeholder(self.fields["mobile_number"], "(xxx) xxx-xxxx")
        self.fields["mobile_number"].bind("<KeyRelease>", self.format_phone_number)
        self.fields["mobile_number"].bind("<FocusIn>", self.clear_placeholder)
        self.fields["mobile_number"].bind("<FocusOut>", self.restore_placeholder)

        # Submit and Back buttons
        signup_button = ttk.Button(form_frame, text="Submit", width=20, command=self.handle_signup)
        signup_button.grid(row=max(len(left_fields), len(right_fields)) + 2, column=0, columnspan=4, pady=20)

        back_button = ttk.Button(form_frame, text="Back", width=20, command=self.show_login_screen_callback)
        back_button.grid(row=max(len(left_fields), len(right_fields)) + 3, column=0, columnspan=4, pady=(5, 20))

    def set_placeholder(self, entry, placeholder_text):
        """Sets a placeholder text for the Entry widget."""
        entry.insert(0, placeholder_text)
        entry.config(fg="gray")

    def clear_placeholder(self, event):
        """Clears the placeholder text when the user clicks on the entry field."""
        current_text = self.fields["mobile_number"].get()
        if current_text == "(xxx) xxx-xxxx":
            self.fields["mobile_number"].delete(0, tk.END)
            self.fields["mobile_number"].config(fg="black")

    def restore_placeholder(self, event):
        """Restores the placeholder text if the field is left empty."""
        current_text = self.fields["mobile_number"].get()
        if current_text == "":
            self.set_placeholder(self.fields["mobile_number"], "(xxx) xxx-xxxx")
        elif current_text != "(xxx) xxx-xxxx":
            self.fields["mobile_number"].config(fg="black")

    def format_phone_number(self, event=None):
        phone_number = self.fields["mobile_number"].get().replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
        
        if len(phone_number) >= 1:
            phone_number = f"({phone_number[:3]}) {phone_number[3:6]}-{phone_number[6:11]}"
        self.fields["mobile_number"].delete(0, tk.END)
        self.fields["mobile_number"].insert(0, phone_number[:14])

    def validate_fields(self):
        # Validate First Name
        first_name = self.fields["first_name"].get().strip()
        if not first_name.isalpha():
            return False, "First Name must contain only letters."

        # Validate Last Name
        last_name = self.fields["last_name"].get().strip()
        if not last_name.isalpha():
            return False, "Last Name must contain only letters."

        # Validate Email Address
        email = self.fields["email_address"].get().strip()
        email_pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(email_pattern, email):
            return False, "Please enter a valid email address."

        # Validate Password (e.g., minimum 8 characters, at least one letter, one number)
        password = self.fields["password"].get().strip()
        if len(password) < 8 or not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
            return False, "Password must be at least 8 characters long and contain both letters and numbers."

        # Validate Mobile Number (USA format: (xxx) xxx-xxxx)
        mobile_number = self.fields["mobile_number"].get().strip()
        phone_pattern = r"^\(\d{3}\) \d{3}-\d{4}$"
        if not re.match(phone_pattern, mobile_number):
            return False, "Please enter a valid U.S. phone number in the format (xxx) xxx-xxxx."

        return True, ""

    def handle_signup(self):
        # Validate fields before proceeding
        valid, message = self.validate_fields()
        if not valid:
            messagebox.showerror("Validation Error", message)
            return

        # Collect form data if validation passes
        user_data = {
            "first_name": self.fields["first_name"].get(),
            "last_name": self.fields["last_name"].get(),
            "email_address": self.fields["email_address"].get(),
            "password": self.fields["password"].get(),
            "mobile_number": self.fields["mobile_number"].get(),
            "fulltime": self.fields["fulltime"].get(),
            "parttime": self.fields["parttime"].get(),
            "undergraduate": self.fields["undergraduate"].get(),
            "graduate": self.fields["graduate"].get(),
            "work_per_week": self.fields["work_per_week"].get(),
            "age_group": self.fields["age_group"].get(),
            "is_active": False,
            "role_type": self.fields["role_type"].get()
        }

        # Call signup manager to handle signup
        result = self.signup_manager.handle_signup(user_data)

                # Display success or error message
        if result["success"]:
            # Include the email address, first name, and last name in the success message
            success_message = f"Signup successful!\n\nWelcome, {self.fields['first_name'].get()} {self.fields['last_name'].get()}.\nYour email: {self.fields['email_address'].get()}"
            messagebox.showinfo("Signup", success_message)
            self.show_login_screen_callback()
        else:
            messagebox.showerror("Error", result["message"])

