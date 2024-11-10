import tkinter as tk
from tkinter import ttk

class UserView:
    def __init__(self, root, return_to_login):
        self.root = root
        self.return_to_login = return_to_login
        self.current_frame = None

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
        ttk.Label(frame, text="View Profile", font=("Helvetica", 16)).pack(pady=20)
        # Add fields for displaying profile information
        self.show_frame(frame)

    def show_update_profile(self):
        frame = ttk.Frame(self.root)
        ttk.Label(frame, text="Update Profile", font=("Helvetica", 16)).pack(pady=20)
        # Add fields for updating profile information
        self.show_frame(frame)

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
