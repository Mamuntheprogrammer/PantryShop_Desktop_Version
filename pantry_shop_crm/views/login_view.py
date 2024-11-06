import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from controllers.login_system import LoginSystem

class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x350")
        self.root.config(bg="#f4f4f4")  # Set a background color

        self.create_login_form()

    def create_login_form(self):
        # Create a frame for the login form
        form_frame = ttk.Frame(self.root, padding="20")
        form_frame.pack(padx=20, pady=30)

        # Title Label
        ttk.Label(form_frame, text="Login", font=("Helvetica", 18, "bold"), foreground="#4CAF50").grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Username label and input
        ttk.Label(form_frame, text="Username:", font=("Helvetica", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.username_entry = ttk.Entry(form_frame, width=30, font=("Helvetica", 12))
        self.username_entry.grid(row=1, column=1, columnspan=2, pady=5)

        # Password label and input
        ttk.Label(form_frame, text="Password:", font=("Helvetica", 12)).grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(form_frame, width=30, font=("Helvetica", 12), show="*")
        self.password_entry.grid(row=2, column=1, columnspan=2, pady=5)

        # Login and Sign Up Buttons in the same row as password_entry
        login_button = ttk.Button(form_frame, text="Login", width=10, command=self.handle_login)
        login_button.grid(row=4, column=1, sticky="e", padx=(0, 5),pady=(20,0))  # Positioned next to password_entry

        signup_button = ttk.Button(form_frame, text="Sign Up", width=10, command=self.handle_signup)
        signup_button.grid(row=4, column=2, sticky="w", padx=(5, 0),pady=(20,0))  # Positioned next to Login button





        # # Option for forgot password (styling)
        # forgot_password_label = ttk.Label(form_frame, text="Forgot Password?", foreground="#007BFF", cursor="hand2")
        # forgot_password_label.grid(row=4, column=0, columnspan=2, pady=5)
        # forgot_password_label.bind("<Button-1>", self.forgot_password)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        login_system = LoginSystem(username, password)
        if login_system.authenticate():
            messagebox.showinfo("Login", "Login successful!")
            self.root.destroy()  # Close login window
            # Open the main dashboard window here (not implemented in this snippet)
        else:
            messagebox.showerror("Login", "Invalid username or password.")

            
    def handle_signup(self):
        messagebox.showinfo("Sign Up", "Sign Up form will appear here.")
        # Placeholder for opening the Sign Up form

    # def forgot_password(self, event):
    #     # Placeholder function for handling forgotten password
    #     messagebox.showinfo("Forgot Password", "Password reset functionality not implemented yet.")

# # Main entry point for the application
# if __name__ == "__main__":
#     root = tk.Tk()
#     login_view = LoginView(root)
#     root.mainloop()
