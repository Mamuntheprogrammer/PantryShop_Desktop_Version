import sqlite3
from models.database import Database  # Ensure this path matches where your Database class is located

class LoginManager:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def authenticate(self):
        # Connect to the database
        db = Database()  # Initialize your database class to establish a connection

        try:
            # Prepare and execute the query to check if a user exists with the given email and password
            query = "SELECT role_type FROM users WHERE email_address = ? AND password = ?"
            db.cursor.execute(query, (self.email, self.password))
            result = db.cursor.fetchone()

            # If result is found, return the user's role; otherwise, return None
            if result:
                role = result[0]  # Assuming role_type is the first item in the result tuple
                return role
            else:
                return None
        finally:
            # Close the database connection
            db.close()

