from typing import Any

import jwt
from datetime import datetime, timedelta

from loguru import logger


class JWTService:

    def __new__(cls, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], str):

            if args[0] == "":
                raise ValueError("Secret key cannot be empty!")
            elif len(args[0]) < 32:
                logger.warning("Secret key is shorter than 32 characters, consider using a longer key.")

            return super().__new__(cls)
        else:
            logger.critical("JWTService was not provided with a secret key.")

    def __init__(self, secret_key):
        """
        Initialize the JWTService with a secret key.
        :param secret_key: Secret key for signing JWT tokens.
        """
        self.secret_key = secret_key

    def generate_jwt(self, payload: dict, expiration_minutes=60) -> str:
        """
        Generate a signed JWT token.
        :param payload: Dictionary containing payload data.
        :param expiration_minutes: Expiration time in minutes (default: 60).
        :return: Encoded JWT token.
        """
        expiration_time = datetime.now() + timedelta(minutes=expiration_minutes)
        payload["exp"] = expiration_time
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def verify_jwt(self, token: str) -> tuple[dict[str, str], int]:
        """
        Verify and decode a JWT token.
        :param token: JWT token to verify.
        :return: Tuple containing the decoded payload or JSON with an error message, both with status code.
        """
        try:
            decoded_payload: dict = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return decoded_payload, 200
        except jwt.ExpiredSignatureError:
            return { "error_message": "Token has expired." }, 430
        except jwt.InvalidTokenError:
            return { "error_message": "Invalid token." }, 432
