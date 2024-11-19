import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk  # Optional: Only if you're using themed Tkinter for the parent window

class Loader:
    def __init__(self, parent):
        """
        Initializes the Loader with the parent frame.
        :param parent: Parent frame or window where the loader will be displayed.
        """
        self.parent = parent
        self.loader_frame = None

    def show(self):
        """Show the loader frame with a progress indicator."""
        if not self.loader_frame:
            self.loader_frame = ttk.Frame(self.parent, padding="20", style="TFrame")
            self.loader_frame.place(relwidth=1, relheight=1)

            # Add a progress label or animated spinner (use ttk widgets for better theme consistency)
            ttk.Label(
                self.loader_frame,
                text="Loading...",
                style="TLabel",
                font=("Arial", 18),
                anchor="center"
            ).pack(expand=True)

            # Optionally, add a spinning wheel or progress bar
            spinner = ttk.Progressbar(self.loader_frame, mode="indeterminate")
            spinner.pack(pady=10)
            spinner.start()  # Start the animation

    def hide(self):
        """Hide and destroy the loader frame."""
        if self.loader_frame:
            self.loader_frame.destroy()
            self.loader_frame = None
