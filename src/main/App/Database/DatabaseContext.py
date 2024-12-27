from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection settings
DATABASE_URL = "postgresql://db_admin:password123@localhost:5432/main_db"

# SQLAlchemy setup
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
        """ Create the necessary tables if they do not exist. """
        Base.metadata.create_all(self.engine)

    def get_user_by_username_or_email(self, user_name, email):
        """ querie the database to find a user by either their username or email. """
        session = self.Session()
        try:
            return session.query(User).filter((User.user_name == user_name) | (User.email == email)).first()
        finally:
            session.close()

    def create_user(self, user_name, email, password):
        session = self.Session()
        try:
            new_user = User(user_name=user_name, email=email, password=password)
            session.add(new_user)
            session.commit()
        finally:
            session.close()


