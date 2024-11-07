 
import tkinter as tk
from tkinter import ttk

class UserView:
    def __init__(self, root, back_callback, logout_callback):
        self.root = root
        self.back_callback = back_callback
        self.logout_callback = logout_callback
        self.root.title("User Dashboard")
        self.root.geometry("800x500")
        self.root.config(bg="#f4f4f4")

        # Main frame container for side-by-side frames and the bottom buttons
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(pady=20)

        # Side-by-side frames container
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=0, column=0, padx=10, pady=10)

        # First frame for user information
        user_info_frame = ttk.Frame(action_frame, padding="10", style="Card.TFrame")
        user_info_frame.grid(row=0, column=0, padx=10, pady=10)

        # User Information buttons
        ttk.Label(user_info_frame, text="User Information", font=("Helvetica", 14, "bold"), foreground="#4CAF50").pack(pady=10)
        ttk.Button(user_info_frame, text="Update User Information", width=20).pack(pady=5)
        ttk.Button(user_info_frame, text="View User Information", width=20).pack(pady=5)

        # Second frame for order options
        order_frame = ttk.Frame(action_frame, padding="10", style="Card.TFrame")
        order_frame.grid(row=0, column=1, padx=10, pady=10)

        # Order buttons
        ttk.Label(order_frame, text="Order Management", font=("Helvetica", 14, "bold"), foreground="#4CAF50").pack(pady=10)
        ttk.Button(order_frame, text="Create Order", width=20).pack(pady=5)
        ttk.Button(order_frame, text="View Orders", width=20).pack(pady=5)
        ttk.Button(order_frame, text="Order Report", width=20).pack(pady=5)

        # Bottom frame for navigation buttons
        navigation_frame = ttk.Frame(main_frame, padding="10")
        navigation_frame.grid(row=1, column=0, pady=10)

        # Back and Logout buttons
        ttk.Button(navigation_frame, text="Back", width=15, command=self.back_callback).grid(row=0, column=0, padx=5)
        ttk.Button(navigation_frame, text="Logout", width=15, command=self.logout_callback).grid(row=0, column=1, padx=5)

        # Style for the modern card look
        style = ttk.Style()
        style.configure("Card.TFrame", background="#ffffff", borderwidth=2, relief="groove")
        style.configure("TButton", font=("Helvetica", 10), padding=5)
        style.configure("TLabel", font=("Helvetica", 12), foreground="#333333")

# Example usage
if __name__ == "__main__":
    root = tk.Tk()

    def go_back():
        print("Back button clicked")

    def logout():
        print("Logout button clicked")

    UserView(root, go_back, logout)
    root.mainloop()
