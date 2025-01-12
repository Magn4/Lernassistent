from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Text  # Add this import to use the Text type

# Database connection settings
DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/Lernassistent"

# SQLAlchemy setup
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)


# ADD: New class for Dashboard uploads (Ni)
class DashboardUpload(Base):
    __tablename__ = 'dashboard_uploads'

    id = Column(Integer, primary_key=True)  # Unique ID for each dashboard upload
    module_name = Column(String(255), nullable=False)  # Module name, cannot be empty
    directory_name = Column(String(255), nullable=False)  # Directory name, cannot be empty
    extracted_text = Column(Text, nullable=True)  # Store the extracted text from the PDF

    def __init__(self, module_name, directory_name, extracted_text):
        self.module_name = module_name
        self.directory_name = directory_name
        self.extracted_text = extracted_text

#




class DatabaseContext:
    def __init__(self, db_url=DATABASE_URL):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self._initialize_database()

    def _initialize_database(self):
        """ Create the necessary tables if they do not exist. """
        Base.metadata.create_all(self.engine)

    def get_all_users(self):
        session = self.Session()
        try:
            return session.query(User).all()  # Fetch all users from the database
        finally:
            session.close()

    def get_user_by_email(self, email):
        """ Query the database to find a user by their email. """
        session = self.Session()
        try:
            return session.query(User).filter_by(email=email).first()
        finally:
            session.close()

    def get_user_by_username_or_email(self, user_name, email):
        """ Query the database to find a user by either their username or email. """
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

    # ADD: New methods for DashboardUploads (Ni)
    def get_all_dashboards(self):
        """Fetch all dashboard uploads from the database."""
        session = self.Session()
        try:
            return session.query(DashboardUpload).all()  # Fetch all dashboards uploaded
        finally:
            session.close()

    def get_dashboard_by_id(self, dashboard_id):
        """Fetch a dashboard upload by its ID."""
        session = self.Session()
        try:
            return session.query(DashboardUpload).filter_by(id=dashboard_id).first()  # Find by ID
        finally:
            session.close()

    def save_dashboard_upload(self, module_name, directory_name, extracted_text):
        """Save a new dashboard upload into the database."""
        session = self.Session()
        try:
            new_dashboard = DashboardUpload(module_name=module_name, directory_name=directory_name, extracted_text=extracted_text)
            session.add(new_dashboard)  # Add the new dashboard upload to the session
            session.commit()  # Commit the session to save it to the database
        finally:
            session.close()

#