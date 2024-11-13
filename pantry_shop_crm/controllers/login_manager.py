import sqlite3
from models.database import Database  # Ensure this path matches where your Database class is located
from . import session

class LoginManager:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def authenticate(self):
        # Connect to the database
        db = Database()  # Initialize your database class to establish a connection

        try:
            # Prepare and execute the query to check if a user exists with the given email and password
            query = "SELECT user_id, role_type FROM users WHERE email_address = ? AND password = ?"
            db.cursor.execute(query, (self.email, self.password))
            result = db.cursor.fetchone()

            # If result is found, return the user's role; otherwise, return None
            if result:
                userid, role = result
                # Set the global user_id and role
                session.user_id = userid
                session.user_role = role
                return role
            else:
                return None
        finally:
            # Close the database connection
            db.close()

