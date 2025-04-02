
class User:
    """
    User class to represent a user in the system.

    :param user_id: The unique identifier for the user.
    :param username: The username of the user.
    :param password_hash: The hashed password of the user.
    :param email: The email address of the user.
    """

    def __init__(self, user_id: int, username: str, password_hash: str, email: str):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash
        self.email = email

    def __str__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"