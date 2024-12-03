import unittest
from authenticated import user_actions
from database.models import Session, User, Password, Category
from sqlalchemy.exc import IntegrityError
from cryptography.fernet import Fernet
import os

# Cargar la clave de cifrado desde las variables de entorno
AES_KEY = os.getenv('AES_KEY')
fernet = Fernet(AES_KEY)

class TestUserActions(unittest.TestCase):

    def setUp(self):
        """Configura el entorno de prueba creando un usuario de prueba."""
        self.session = Session()
        self.user_email = "test@example.com"
        self.user_password = "TestPassword123!"
        encrypted_password = fernet.encrypt(self.user_password.encode()).decode()
        self.user = User(email=self.user_email, password=encrypted_password)
        self.session.add(self.user)
        self.session.commit()

    def tearDown(self):
        """Limpia el entorno de prueba eliminando todos los registros de la base de datos."""
        self.session.query(Password).delete()
        self.session.query(User).delete()
        self.session.query(Category).delete()
        self.session.commit()
        self.session.close()

    def test_create_user(self):
        """Prueba la creación de un nuevo usuario."""
        message = user_actions.create_user("newuser@example.com", "NewPassword123!")
        self.assertEqual(message, "User created successfully.")

    def test_create_user_with_existing_email(self):
        """Prueba la creación de un usuario con un email ya registrado."""
        message = user_actions.create_user(self.user_email, self.user_password)
        self.assertEqual(message, "Error: The email is already registered.")

    def test_login(self):
        """Prueba el inicio de sesión con credenciales correctas."""
        message, user, token = user_actions.login(self.user_email, self.user_password)
        self.assertEqual(message, "Login successful.")
        self.assertIsNotNone(user)
        self.assertIsNotNone(token)

    def test_login_with_incorrect_password(self):
        """Prueba el inicio de sesión con una contraseña incorrecta."""
        message, user, token = user_actions.login(self.user_email, "WrongPassword")
        self.assertEqual(message, "Incorrect email or password.")
        self.assertIsNone(user)
        self.assertIsNone(token)

    def test_delete_account(self):
        """Prueba la eliminación de una cuenta y todas las contraseñas asociadas."""
        message = user_actions.delete_account(self.user.id, self.user_password)
        self.assertEqual(message, "Account and all associated passwords and categories deleted successfully.")
        user = self.session.query(User).filter_by(id=self.user.id).first()
        self.assertIsNone(user)

if __name__ == "__main__":
    unittest.main()