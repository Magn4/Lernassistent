from flask import request, jsonify
from Services.UserService import UserService

class UserController:
    def __init__(self, user_service):
        self.user_service = user_service

    def register(self):
        data = request.get_json()
        user_name = data.get('userName')
        email = data.get('eMail')
        password = data.get('password')

        if self.user_service.is_account_already_existing(user_name, email):
            return jsonify({"error": "Account already exists"}), 400

        self.user_service.create_account(user_name, email, password)
        return jsonify({"message": "Account created successfully"}), 201

    def login(self):
        data = request.get_json()
        email = data.get('eMail')
        password = data.get('password')

        if self.user_service.authenticate_user(email, password):
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    
    def get_all_users(self):
        users = self.user_service.get_all_users()  # Call service to get all users
        user_list = [{"user_id": user.user_id, "user_name": user.user_name, "email": user.email} for user in users]
        return jsonify({"users": user_list}), 200