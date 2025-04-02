
class UserDTO:

    def __init__(self, user_id: int, username: str, email: str, password_hash: str):
        self.id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def __str__(self):
        return f"UserDTO(id={self.id}, username={self.username}, email={self.email})"