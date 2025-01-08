import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Dynamically construct DATABASE_URL
DATABASE_URL = f"postgresql://{os.getenv('DB_USER', 'db_user')}:{os.getenv('DB_PASSWORD', 'password123')}@{os.getenv('DB_HOST', 'database')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'app_db')}"
# DATABASE_URL = "postgresql://db_user:password123@localhost:5432/app_db"
print(DATABASE_URL)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

class DatabaseContext: 
    def __init__(self, db_url=DATABASE_URL):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self._initialize_database()

    def _initialize_database(self):
        Base.metadata.create_all(self.engine)

    def get_all_users(self):
        session = self.Session()
        try:
            return session.query(User).all()
        except SQLAlchemyError as e:
            print(f"Error getting all users: {e}")
            return []
        finally:
            session.close()

    def get_user_by_email(self, email):
        session = self.Session()
        try:
            return session.query(User).filter_by(email=email).first()
        except SQLAlchemyError as e:
            print(f"Error getting user by email: {e}")
            return None
        finally:
            session.close()

    def create_user(self, user_name, email, password):
        session = self.Session()
        try:
            new_user = User(user_name=user_name, email=email, password=password)
            session.add(new_user)
            session.commit()
        except SQLAlchemyError as e:
            print(f"Error creating user: {e}")
            session.rollback()
        finally:
            session.close()
