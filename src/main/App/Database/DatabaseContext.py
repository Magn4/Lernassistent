from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

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

class Module(Base):
    __tablename__ = 'modules'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    topics = relationship("Topic", back_populates="module", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Module(name={self.name})>"

class Topic(Base):
    __tablename__ = 'topics'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    module_id = Column(Integer, ForeignKey('modules.id', ondelete="CASCADE"))
    files = relationship("File", back_populates="topic", cascade="all, delete-orphan")
    module = relationship("Module", back_populates="topics")

    def __repr__(self):
        return f"<Topic(name={self.name}, module_id={self.module_id})>"

class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.id', ondelete="CASCADE"))
    content = Column(Text, nullable=True)
    topic = relationship("Topic", back_populates="files")

    def __repr__(self):
        return f"<File(name={self.name}, topic_id={self.topic_id})>"

# ADD: New class for Dashboard uploads (Ni)
class DashboardUpload(Base):
    __tablename__ = 'dashboard_uploads'

    id = Column(Integer, primary_key=True)  # Unique ID for each dashboard upload
    module_name = Column(String(255), nullable=False)  # Module name, cannot be empty
    topic_name = Column(String(255), nullable=False)  # topic name, cannot be empty
    extracted_text = Column(Text, nullable=True)  # Store the extracted text from the PDF

    def __init__(self, module_name, topic_name, extracted_text):
        self.module_name = module_name
        self.topic_name = topic_name
        self.extracted_text = extracted_text

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
    
    def create_module(self, module_name):
        session = self.Session()
        try:
            if session.query(Module).filter_by(name=module_name).first():
                raise ValueError(f"Module '{module_name}' already exists.")
            new_module = Module(name=module_name)
            session.add(new_module)
            session.commit()
        finally:
            session.close()

    def create_topic(self, module_name, topic_name):
        session = self.Session()
        try:
            module = session.query(Module).filter_by(name=module_name).first()
            if not module:
                raise ValueError(f"Module '{module_name}' does not exist.")
            if any(topic.name == topic_name for topic in module.topics):
                raise ValueError(f"Topic '{topic_name}' already exists in module '{module_name}'.")
            new_topic = Topic(name=topic_name, module=module)
            session.add(new_topic)
            session.commit()
        finally:
            session.close()
    
    def upload_file(self, module_name, topic_name, file_name, file_content):
        session = self.Session()
        try:
            module = session.query(Module).filter_by(name=module_name).first()
            if not module:
                raise ValueError(f"Module '{module_name}' does not exist.")
            topic = session.query(Topic).filter_by(name=topic_name, module=module).first()
            if not topic:
                raise ValueError(f"Topic '{topic_name}' does not exist in module '{module_name}'.")
            new_file = File(name=file_name, content=file_content, topic=topic)
            session.add(new_file)
            session.commit()
        finally:
            session.close()
        
    def delete_module(self, module_name):
        session = self.Session()
        try:
            module = session.query(Module).filter_by(name=module_name).first()
            if not module:
                raise ValueError(f"Module '{module_name}' does not exist.")
            session.delete(module)
            session.commit()
        finally:
            session.close()

    def delete_topic(self, module_name, topic_name):
        session = self.Session()
        try:
            module = session.query(Module).filter_by(name=module_name).first()
            if not module:
                raise ValueError(f"Module '{module_name}' does not exist.")
            topic = session.query(Topic).filter_by(name=topic_name, module=module).first()
            if not topic:
                raise ValueError(f"topic '{topic_name}' does not exist in module '{module_name}'.")
            session.delete(topic)
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

    def save_dashboard_upload(self, module_name, topic_name, extracted_text):
        """Save a new dashboard upload into the database."""
        session = self.Session()
        try:
            new_dashboard = DashboardUpload(module_name=module_name, topic_name=topic_name, extracted_text=extracted_text)
            session.add(new_dashboard)  # Add the new dashboard upload to the session
            session.commit()  # Commit the session to save it to the database
        finally:
            session.close()

#