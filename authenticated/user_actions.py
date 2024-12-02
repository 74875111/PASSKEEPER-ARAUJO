import os
from sqlalchemy.orm import sessionmaker
from database.models import Category, User, Password, engine
from sqlalchemy.exc import IntegrityError
from session_manager import generate_token
from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv
from services.email_verification import verify_email
from utils.password_utils import is_password_strong

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la clave AES desde la variable de entorno
AES_KEY = os.getenv('AES_KEY')
fernet = Fernet(AES_KEY)

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

def create_user(email, password, email_verified=False):
    is_strong, message = is_password_strong(password)
    if not is_strong:
        return message

    encrypted_password = fernet.encrypt(password.encode()).decode()
    new_user = User(email=email, password=encrypted_password, email_verified=email_verified)
    try:
        session.add(new_user)
        session.commit()
        return "User created successfully."
    except IntegrityError:
        session.rollback()
        return "Error: The email is already registered."

def create_user_with_email_verification(email, password):
    # Verificar el correo electrónico
    is_valid, message = verify_email(email)
    if not is_valid:
        return message

    return create_user(email, password, email_verified=True)

def login(email, password):
    user = session.query(User).filter_by(email=email).first()
    if user:
        try:
            decrypted_password = fernet.decrypt(user.password.encode()).decode()
            if decrypted_password == password:
                token = generate_token(user.id)
                return "Login successful.", user, token
            else:
                return "Incorrect email or password.", None, None
        except InvalidToken:
            return "Incorrect email or password.", None, None
    else:
        return "Incorrect email or password.", None, None

def list_passwords(user_id):
    passwords = session.query(Password).filter_by(user_id=user_id).all()
    return passwords

def create_password(service_name, user_email, password, user_id, category_id=None):
    encrypted_password = fernet.encrypt(password.encode()).decode()
    new_password = Password(
        service_name=service_name,
        user_email=user_email,
        password=encrypted_password,
        user_id=user_id,
        category_id=category_id
    )
    session.add(new_password)
    session.commit()
    return "Password created successfully."

def delete_password(password_id):
    password = session.query(Password).filter_by(id=password_id).first()
    if password:
        session.delete(password)
        session.commit()
        return "Password deleted successfully."
    return "Password not found."

def update_password(password_id, service_name, user_email, password, category_id=None, is_favorite=False):
    password_record = session.query(Password).filter_by(id=password_id).first()
    if password_record:
        encrypted_password = fernet.encrypt(password.encode()).decode()
        password_record.service_name = service_name
        password_record.user_email = user_email
        password_record.password = encrypted_password
        password_record.category_id = category_id
        password_record.is_favorite = is_favorite
        session.commit()
        return "Password updated successfully."
    return "Password not found."

def get_password(password_id):
    password_record = session.query(Password).filter_by(id=password_id).first()
    if password_record:
        try:
            decrypted_password = fernet.decrypt(password_record.password.encode()).decode()
            password_record.password = decrypted_password
        except InvalidToken:
            password_record.password = "Invalid token"
        return password_record
    return None

def list_favorite_passwords(user_id):
    passwords = session.query(Password).filter_by(user_id=user_id, is_favorite=True).all()
    return passwords

def list_passwords_by_category(user_id, category_name):
    category = session.query(Category).filter_by(name=category_name).first()
    if category:
        passwords = session.query(Password).filter_by(user_id=user_id, category_id=category.id).all()
    else:
        passwords = []
    return passwords

def delete_account(user_id, password):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        decrypted_password = fernet.decrypt(user.password.encode()).decode()
        if decrypted_password == password:
            session.query(Password).filter_by(user_id=user_id).delete()
            session.delete(user)
            session.commit()
            return "Account and all associated passwords deleted successfully."
        else:
            return "Incorrect password."
    return "User not found."