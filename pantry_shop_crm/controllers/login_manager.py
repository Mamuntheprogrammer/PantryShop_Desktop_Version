import sqlite3
from models.database import Database  # Ensure this path matches where your Database class is located
from . import session
from tkinter import messagebox

class LoginManager:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def authenticate(self):
        # Connect to the database
        db = Database()  # Initialize your database class to establish a connection

        try:
            # Prepare and execute the query to check if a user exists with the given email and password
            query = "SELECT user_id,first_name, role_type FROM users WHERE email_address = ? AND password = ? AND is_active = 1"
            db.cursor.execute(query, (self.email, self.password))
            result = db.cursor.fetchone()

            # If result is found, return the user's role; otherwise, return None
            if result:
                userid, name,role = result
                # Set the global user_id and role
                session.user_id = userid
                session.user_role = role
                session.user_name = name
                return role
            else:
                messagebox.showerror("Error", "Incorrect Credential")
                return None
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            db.close()


        # finally:
        #     # Close the database connection
        #     db.close()



        #         messagebox.showinfo("Update Error", "No material found with the provided ID.")
        #     else:
        #         messagebox.showinfo("Material Updated", "Material information has been successfully updated.")
        # except sqlite3.Error as e:
        #     messagebox.showerror("Database Error", f"An error occurred: {e}")
        # finally:
        #     conn.close()