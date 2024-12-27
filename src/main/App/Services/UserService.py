from werkzeug.security import generate_password_hash, check_password_hash
from Database.DatabaseContext import DatabaseContext

class UserService:
    def __init__(self, db_context):
        self.db_context = db_context

    def is_account_already_existing(self, user_name, email):
        user = self.db_context.get_user_by_username_or_email(user_name, email)
        return user is not None

    def create_account(self, user_name, email, password):
        hashed_password = generate_password_hash(password)
        self.db_context.create_user(user_name, email, hashed_password)

    def authenticate_user(self, email, password):
        user = self.db_context.get_user_by_email(email)
        if user and check_password_hash(user.password, password):
            return True
        return False