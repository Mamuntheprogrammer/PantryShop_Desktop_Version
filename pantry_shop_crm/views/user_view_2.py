import tkinter as tk
from tkinter import ttk

class UserView:
    def __init__(self, root, return_to_login):
        self.root = root
        self.return_to_login = return_to_login
        self.current_frame = None

        # Sample user data (these variables should be initialized with actual data in your code)
        self.username_var = tk.StringVar(value="john_doe")
        self.first_name_var = tk.StringVar(value="John")
        self.last_name_var = tk.StringVar(value="Doe")
        self.email_var = tk.StringVar(value="john.doe@example.com")
        self.user_type_var = tk.StringVar(value="Admin")
        self.departname_var = tk.StringVar(value="Sales")
        self.phone_var = tk.StringVar(value="123-456-7890")
        self.age_var = tk.StringVar(value="30")
        self.max_hour_var = tk.StringVar(value="40")
        self.reference_var = tk.StringVar(value="HR")
        self.student_status_var = tk.StringVar(value="Graduate")

        # Show the initial user home with a welcome message
        self.show_user_home()

        # Create the user menu bar
        self.create_user_menu()

    def create_user_menu(self):
        # Create the menu bar
        menu_bar = tk.Menu(self.root, bg="#333", fg="#FFF", font=("Helvetica", 10))

        # Profile menu
        profile_menu = tk.Menu(menu_bar, tearoff=0, bg="#333", fg="#FFF", activebackground="#002bb2")
        profile_menu.add_command(label="View Profile", command=self.show_view_profile)
        profile_menu.add_command(label="Update Profile", command=self.show_update_profile)
        menu_bar.add_cascade(label="Profile", menu=profile_menu)

        # Manage Order menu
        manage_order_menu = tk.Menu(menu_bar, tearoff=0, bg="#333", fg="#FFF", activebackground="#002bb2")
        manage_order_menu.add_command(label="Create Order", command=self.show_create_order)
        manage_order_menu.add_command(label="View and Edit Order", command=self.show_view_edit_order)
        manage_order_menu.add_command(label="Order Report", command=self.show_order_report)
        menu_bar.add_cascade(label="Manage Order", menu=manage_order_menu)

        # Logout option in the menu
        logout_menu = tk.Menu(menu_bar, tearoff=0, bg="#333", fg="#FFF", activebackground="#002bb2")
        logout_menu.add_command(label="Logout", command=self.logout)
        menu_bar.add_cascade(label="Logout", menu=logout_menu)

        # Configure the root window to display this menu
        self.root.config(menu=menu_bar)

    def show_frame(self, frame):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame
        self.current_frame.pack(fill="both", expand=True)

    def show_user_home(self):
        # Create the main frame with a welcome message
        frame = ttk.Frame(self.root)
        welcome_message = "Welcome, User!"  # Replace "User" with the actual user's name if available
        ttk.Label(frame, text=welcome_message, font=("Helvetica", 18, "bold")).pack(pady=20)
        ttk.Label(frame, text="Please use the menu to navigate.", font=("Helvetica", 12)).pack(pady=10)
        self.show_frame(frame)

    def show_view_profile(self):
        frame = ttk.Frame(self.root)
        
        # Title label
        ttk.Label(frame, text="View Profile", font=("Helvetica", 16, "bold")).pack(pady=20)

        # Create a frame to contain the profile fields
        profile_frame = ttk.Frame(frame)
        profile_frame.pack(pady=10)

        # Define the fields to be displayed (assuming these variables are already defined somewhere in your code)
        fields = [
            ("Username", self.username_var),
            ("First Name", self.first_name_var),
            ("Last Name", self.last_name_var),
            ("Email", self.email_var),
            ("User Type", self.user_type_var),
            ("Department", self.departname_var),
            ("Phone", self.phone_var),
            ("Age", self.age_var),
            ("Max Hour", self.max_hour_var),
            ("Reference", self.reference_var),
            ("Student Status", self.student_status_var),
        ]
        
        # Loop through the fields and display them in a vertical list
        for label_text, var in fields:
            field_frame = ttk.Frame(profile_frame)
            field_frame.pack(fill="x", pady=5)
            
            ttk.Label(field_frame, text=f"{label_text}:", font=("Helvetica", 12), anchor="w", width=15).pack(side="left", padx=10)
            ttk.Label(field_frame, text=var.get(), font=("Helvetica", 12), relief="sunken", width=30).pack(side="left", padx=10)
        
        # Add a back button to return to home screen
        back_button = ttk.Button(frame, text="Back", command=self.show_user_home)
        back_button.pack(pady=20)

        self.show_frame(frame)



    def show_update_profile(self):
        frame = ttk.Frame(self.root)
        
        # Title label
        ttk.Label(frame, text="Update Profile", font=("Helvetica", 16, "bold")).pack(pady=20)
        
        # Create a frame to hold the update profile fields
        update_frame = ttk.Frame(frame)
        update_frame.pack(pady=10)

        # Define the fields to be updated (use the existing Tkinter variables that hold the current data)
        fields = [
            ("Username", self.username_var),
            ("First Name", self.first_name_var),
            ("Last Name", self.last_name_var),
            ("Email", self.email_var),
            ("User Type", self.user_type_var),
            ("Department", self.departname_var),
            ("Phone", self.phone_var),
            ("Age", self.age_var),
            ("Max Hour", self.max_hour_var),
            ("Reference", self.reference_var),
            ("Student Status", self.student_status_var),
        ]

        # Loop through the fields and create entry widgets for each field
        for label_text, var in fields:
            field_frame = ttk.Frame(update_frame)
            field_frame.pack(fill="x", pady=5)
            
            ttk.Label(field_frame, text=f"{label_text}:", font=("Helvetica", 12), anchor="w", width=15).pack(side="left", padx=10)
            entry = ttk.Entry(field_frame, textvariable=var, font=("Helvetica", 12), width=30)
            entry.pack(side="left", padx=10)

        # Button to save the updated profile information
        save_button = ttk.Button(frame, text="Save Changes", command=self.save_profile_changes)
        save_button.pack(pady=20)

        # Button to cancel and go back to the profile view
        cancel_button = ttk.Button(frame, text="Cancel", command=self.show_view_profile)
        cancel_button.pack(pady=10)

        self.show_frame(frame)

    def save_profile_changes(self):
        # Here you can add code to save the updated data to the database or wherever needed.
        # For now, let's just print the updated values as an example.
        print("Updated Profile Information:")
        print(f"Username: {self.username_var.get()}")
        print(f"First Name: {self.first_name_var.get()}")
        print(f"Last Name: {self.last_name_var.get()}")
        print(f"Email: {self.email_var.get()}")
        print(f"User Type: {self.user_type_var.get()}")
        print(f"Department: {self.departname_var.get()}")
        print(f"Phone: {self.phone_var.get()}")
        print(f"Age: {self.age_var.get()}")
        print(f"Max Hour: {self.max_hour_var.get()}")
        print(f"Reference: {self.reference_var.get()}")
        print(f"Student Status: {self.student_status_var.get()}")

        # You can also include additional logic to handle saving the updated profile information
        # into a database or API.
        
        # Optionally, show a success message after saving
        success_message = "Profile updated successfully!"
        success_label = ttk.Label(self.root, text=success_message, font=("Helvetica", 12), foreground="green")
        success_label.pack(pady=10)
        
        # Remove the success message after 2 seconds
        self.root.after(2000, success_label.destroy)  # 2000 milliseconds = 2 seconds
        
        self.show_view_profile()  # Redirect back to view profile after saving changes


    def show_create_order(self):
        frame = ttk.Frame(self.root)
        ttk.Label(frame, text="Create Order", font=("Helvetica", 16)).pack(pady=20)
        # Add fields for creating an order
        self.show_frame(frame)

    def show_view_edit_order(self):
        frame = ttk.Frame(self.root)
        ttk.Label(frame, text="View and Edit Order", font=("Helvetica", 16)).pack(pady=20)
        # Add fields for viewing and editing orders
        self.show_frame(frame)

    def show_order_report(self):
        frame = ttk.Frame(self.root)
        ttk.Label(frame, text="Order Report", font=("Helvetica", 16)).pack(pady=20)
        # Add order report functionality
        self.show_frame(frame)

    def logout(self):
        # Destroy any current frame and reset the window to the login view
        if self.current_frame:
            self.current_frame.destroy()

        # Call the return_to_login method to display the login form
        self.return_to_login()

