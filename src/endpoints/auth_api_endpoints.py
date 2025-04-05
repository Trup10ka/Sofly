from flask import Blueprint, request, jsonify

from src.data import UserDTO
from src.db import UserService
from src.security import JWTService, verify_password, encrypt_password_sha256


def init_auth_endpoints(blueprint: Blueprint, user_service: UserService, jwt_service: JWTService):
    """
    Initialize the login endpoints for the Flask application.

    Args:
        :param user_service: The Flask blueprint to register the login endpoints with.
        :param blueprint: The database client to interact with the database.
        :param jwt_service: JWTService: The JWT service to handle token generation and verification.
    """

    @blueprint.route('/login', methods=['POST'])
    def login():
        data: dict = request.get_json()

        if 'username' not in data or 'password' not in data:
            return { "error_message": "Missing username or password" }, 404

        username = data['username']
        password = data['password']

        if not username or not password:
            return { "error_message": "Username and password cannot be empty" }, 432

        user = user_service.get_user_by_username(username=username)
        if user is None:
            return { "error_message": "User not found" }, 404
        if not verify_password(password, user.password_hash):
            return { "error_message": "Invalid password" }, 401

        payload = {
            "username": username,
        }

        token = jwt_service.generate_jwt(payload)

        response = jsonify({"SOFLY_TOKEN": token})

        response.set_cookie('SOFLY_TOKEN', token, httponly=True, secure=True)

        return response, 200

    @blueprint.route('/register', methods=['POST'])
    def register():
        data: dict = request.get_json()

        if 'username' not in data or 'password' not in data or 'email' not in data:
            return { "error_message": "One of the fields is missing" }, 404

        username = data['username']
        password = data['password']
        email = data['email']

        if not username or not password or not email:
            return { "error_message": "Username, password and email cannot be empty" }, 432

        if user_service.get_user_by_username(username=username) is not None:
            return { "error_message": "User already exists" }, 409

        if user_service.get_user_by_email(email=email) is not None:
            return { "error_message": "Email already exists" }, 409

        hashed_password = encrypt_password_sha256(password)

        is_created = user_service.create_user(UserDTO(username=username, password_hash=hashed_password, email=email))

        if not is_created:
            return { "error_message": "User creation failed" }, 500

        payload = {
            "username": username,
        }

        token = jwt_service.generate_jwt(payload)

        response = jsonify({"SOFLY_TOKEN": token})

        response.set_cookie('SOFLY_TOKEN', token, httponly=True, secure=True)

        return response, 200
