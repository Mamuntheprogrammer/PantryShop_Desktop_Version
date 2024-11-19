import tkinter as tk
from models.database import Database  # Import the database setup class
from views.login_view import LoginView
from ttkthemes import ThemedTk

class PantryShopCRMApp:
    def __init__(self, root):
        self.root = root
        self.root.set_theme("arc")
        self.db = Database()
        self.show_login_screen()

    def show_login_screen(self):
        # Destroy existing widgets and open login screen
        for widget in self.root.winfo_children():
            widget.destroy()

        # Pass the main root to LoginView
        LoginView(self.root, self.show_signup_screen)

    def show_signup_screen(self):
        # Destroy existing widgets and open signup screen
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Pass the main root to SignupView and provide the callback to go back to login screen
        from views.signup_view import SignupView

        SignupView(self.root, self.show_login_screen)
        


# Main execution
if __name__ == "__main__":
    root = ThemedTk()
    app = PantryShopCRMApp(root)
    root.mainloop()
