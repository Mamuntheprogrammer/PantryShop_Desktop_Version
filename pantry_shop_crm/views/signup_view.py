import tkinter as tk
from tkinter import ttk, messagebox
from controllers.signup_manager import SignupManager

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
            "already_graduate": tk.BooleanVar(),
            "work_per_week": tk.Entry(form_frame, width=30),
            "age_group": tk.Entry(form_frame, width=30),
            
            "role_type": tk.StringVar()  # for dropdown
        }
        # "is_active": tk.BooleanVar(),

        

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
            ("Already Graduate:", tk.Checkbutton(form_frame, variable=self.fields["already_graduate"])),
            ("Work per Week:", self.fields["work_per_week"]),
            ("Age Group:", self.fields["age_group"]),
            # ("Is Active:", tk.Checkbutton(form_frame, variable=False)),
            ("Role Type:", ttk.Combobox(form_frame, textvariable=self.fields["role_type"], values=["Admin", "User"], width=27))
        ]
     

        # Place fields in grid
        for idx, (label, widget) in enumerate(left_fields):
            ttk.Label(form_frame, text=label, font=("Helvetica", 12)).grid(row=idx+1, column=0, sticky="w", pady=5)
            widget.grid(row=idx+1, column=1, padx=25, pady=5)

        for idx, (label, widget) in enumerate(right_fields):
            ttk.Label(form_frame, text=label, font=("Helvetica", 12)).grid(row=idx+1, column=2, sticky="w", pady=5)
            widget.grid(row=idx+1, column=3, padx=25, pady=5)

        # Submit and Back buttons
        signup_button = ttk.Button(form_frame, text="Submit", width=20, command=self.handle_signup)
        signup_button.grid(row=max(len(left_fields), len(right_fields)) + 2, column=0, columnspan=4, pady=20)

        back_button = ttk.Button(form_frame, text="Back", width=20, command=self.show_login_screen_callback)
        back_button.grid(row=max(len(left_fields), len(right_fields)) + 3, column=0, columnspan=4, pady=(5, 20))

    def handle_signup(self):
        # Collect form data
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
            "already_graduate": self.fields["already_graduate"].get(),
            "work_per_week": self.fields["work_per_week"].get(),
            "age_group": self.fields["age_group"].get(),
            "is_active": False,
            "role_type": self.fields["role_type"].get()
        }

        print(user_data)

        # Call signup manager to handle signup
        result = self.signup_manager.handle_signup(user_data)
        
        # Display success or error message
        if result["success"]:
            messagebox.showinfo("Signup", result["message"])
            self.show_login_screen_callback()
        else:
            messagebox.showerror("Error", result["message"])


                # Optionally, show a success message after saving


