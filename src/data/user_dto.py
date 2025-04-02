
class UserDTO:

    def __init__(self, username: str, email: str, password_hash: str):
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def __str__(self):
        return f"UserDTO(username={self.username}, email={self.email})"