 
class LoginSystem:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        print(self.username)

    def authenticate(self):
        # Example static credentials, this should be replaced with actual database logic
        valid_users = {
            "username": "admin",
            "password": "admin",
        }

        if valid_users["username"]==self.username and valid_users["password"]==self.password:
            return True
        else:
            return False
