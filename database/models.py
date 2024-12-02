from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os

# Asegurarse de que la carpeta database exista
if not os.path.exists('database'):
    os.makedirs('database')

# Configuración de la base de datos
DATABASE_URL = 'sqlite:///database/databasePasskeeper.db'
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email_verified = Column(Boolean, default=False)

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    passwords = relationship("Password", back_populates="category")

class Password(Base):
    __tablename__ = 'passwords'
    id = Column(Integer, primary_key=True)
    service_name = Column(String, nullable=False)
    user_email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_favorite = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    user = relationship("User", back_populates="passwords")
    category = relationship("Category", back_populates="passwords")

User.passwords = relationship("Password", order_by=Password.id, back_populates="user")

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()