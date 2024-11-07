import tkinter as tk
from tkinter import ttk

class SignupView:
    def __init__(self, root, show_login_screen_callback):
        self.root = root
        self.show_login_screen_callback = show_login_screen_callback
        self.root.title("Sign Up")
        self.root.geometry("900x600")
        self.create_signup_form()

    def create_signup_form(self):
        # Frame for the signup form
        form_frame = ttk.Frame(self.root, padding="20")
        form_frame.pack(padx=20, pady=30)

        # Title Label
        ttk.Label(form_frame, text="Sign Up", font=("Helvetica", 18, "bold"), foreground="#4CAF50").grid(row=0, column=0, columnspan=4, pady=(0, 20))

        # Left Column Fields
        left_fields = [
            ("Username:", tk.Entry(form_frame, width=30)),
            ("Password:", tk.Entry(form_frame, width=30, show="*")),
            ("First Name:", tk.Entry(form_frame, width=30)),
            ("Last Name:", tk.Entry(form_frame, width=30)),
            ("Email Address:", tk.Entry(form_frame, width=30)),
            ("Mobile Number:", tk.Entry(form_frame, width=30))
        ]

        # Right Column Fields
        right_fields = [
            ("Full-time:", tk.Checkbutton(form_frame, variable=tk.BooleanVar())),
            ("Part-time:", tk.Checkbutton(form_frame, variable=tk.BooleanVar())),
            ("Undergraduate:", tk.Checkbutton(form_frame, variable=tk.BooleanVar())),
            ("Graduate:", tk.Checkbutton(form_frame, variable=tk.BooleanVar())),
            ("Already Graduate:", tk.Checkbutton(form_frame, variable=tk.BooleanVar())),
            ("Work per Week:", tk.Entry(form_frame, width=30)),
            ("Age Group:", tk.Entry(form_frame, width=30)),
            ("Is Active:", tk.Checkbutton(form_frame, variable=tk.BooleanVar())),
            ("Role Type:", tk.Entry(form_frame, width=30))
        ]

        # Place fields in grid
        for idx, (label, widget) in enumerate(left_fields):
            ttk.Label(form_frame, text=label, font=("Helvetica", 12)).grid(row=idx+1, column=0, sticky="w", pady=5)
            widget.grid(row=idx+1, column=1, padx=25, pady=5)

        for idx, (label, widget) in enumerate(right_fields):
            ttk.Label(form_frame, text=label, font=("Helvetica", 12)).grid(row=idx+1, column=2, sticky="w", pady=5)
            widget.grid(row=idx+1, column=3, padx=25, pady=5)

        # Create the Submit button
        signup_button = ttk.Button(form_frame, text="Submit", width=20, command=self.handle_signup)
        signup_button.grid(row=max(len(left_fields), len(right_fields)) + 2, column=0, columnspan=4, pady=20)

        # Align the Back button below the Submit button, centered
        back_button = ttk.Button(form_frame, text="Back", width=20, command=self.show_login_screen_callback)
        back_button.grid(row=max(len(left_fields), len(right_fields)) + 3, column=0, columnspan=4, pady=(5, 20))


    def handle_signup(self):
        # Placeholder for signup logic
        pass
