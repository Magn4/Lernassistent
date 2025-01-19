import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
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
    module_id = Column(Integer, ForeignKey('modules.id', ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    files = relationship("File", back_populates="topic", cascade="all, delete-orphan")
    module = relationship("Module", back_populates="topics")

    def __repr__(self):
        return f"<Topic(name={self.name}, module_id={self.module_id})>"

class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.id', ondelete="CASCADE"))
    path = Column(String(255), nullable=True)
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
    def _handle_session(self, operation):
        """Helper to manage database sessions."""
        session = self.Session()
        try:
            result = operation(session)
            session.commit()
            return result
        except SQLAlchemyError as e:
            logger.error(f"Database operation failed: {e}")
            session.rollback()
            raise
        finally:
            session.close()
    
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
        """ Query the database to find a user by their email. """
        session = self.Session()
        try:
            return session.query(User).filter_by(email=email).first()
        except SQLAlchemyError as e:
            print(f"Error getting user by email: {e}")
            return None
        finally:
            session.close()
   # User Operations
    def get_user_by_username_or_email(self, username=None, email=None):
        def operation(session):
            if username:
                user = session.query(User).filter_by(user_name=username).first()
                if user:
                    return user
            if email:
                user = session.query(User).filter_by(email=email).first()
                return user
            return None
        return self._handle_session(operation)

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

    def list_modules(self):
        session = self.Session()
        try:
            modules = session.query(Module).all()
            return [module.name for module in modules]
        finally:
            session.close()
    
    def list_topics(self, module_name):
        session = self.Session()
        try:
            module = session.query(Module).filter_by(name=module_name).first()
            if not module:
                raise ValueError(f"Module '{module_name}' does not exist.")
            topics = session.query(Topic).filter_by(module=module).all()
            return [topic.name for topic in topics]
        finally:
            session.close()
    
    def list_files(self, module_name, topic_name):
        session = self.Session()
        try:
            module = session.query(Module).filter_by(name=module_name).first()
            if not module:
                raise ValueError(f"Module '{module_name}' does not exist.")
            topic = session.query(Topic).filter_by(name=topic_name, module=module).first()
            if not topic:
                raise ValueError(f"Topic '{topic_name}' does not exist in module '{module_name}'.")
            files = session.query(File).filter_by(topic=topic).all()
            return [file.name for file in files]
        finally:
            session.close()
        
    def upload_file(self, module_name, topic_name, file_name, file_path):
        session = self.Session()
        try:
            module = session.query(Module).filter_by(name=module_name).first()
            if not module:
                raise ValueError(f"Module '{module_name}' does not exist.")
            topic = session.query(Topic).filter_by(name=topic_name, module=module).first()
            if not topic:
                raise ValueError(f"Topic '{topic_name}' does not exist in module '{module_name}'.")
            new_file = File(name=file_name, path=file_path, topic=topic)
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
    
    def delete_file(self, module_name, topic_name, file_name):
        session = self.Session()
        try:
            module = session.query(Module).filter_by(name=module_name).first()
            if not module:
                raise ValueError(f"Module '{module_name}' does not exist.")
            topic = session.query(Topic).filter_by(name=topic_name, module=module).first()
            if not topic:
                raise ValueError(f"Topic '{topic_name}' does not exist in module '{module_name}'.")
            file = session.query(File).filter_by(name=file_name, topic=topic).first()
            if not file:
                raise ValueError(f"File '{file_name}' does not exist in topic '{topic_name}' of module '{module_name}'.")
            session.delete(file)
            session.commit()
        finally:
            session.close()
    
    def get_file_path(self, module_name, topic_name, file_name):
        session = self.Session()
        try:
            module = session.query(Module).filter_by(name=module_name).first()
            if not module:
                raise ValueError(f"Module '{module_name}' does not exist.")
            topic = session.query(Topic).filter_by(name=topic_name, module=module).first()
            if not topic:
                raise ValueError(f"Topic '{topic_name}' does not exist in module '{module_name}'.")
            file = session.query(File).filter_by(name=file_name, topic=topic).first()
            if not file:
                raise ValueError(f"File '{file_name}' does not exist in topic '{topic_name}' of module '{module_name}'.")
            return file.path
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