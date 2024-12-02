import unittest
from utils.password_utils import is_password_strong, generate_strong_password

class TestPasswordUtils(unittest.TestCase):

    def test_is_password_strong(self):
        """Prueba si una contraseña es fuerte."""
        strong_password = "StrongPassword123!"
        weak_password = "weak"
        self.assertTrue(is_password_strong(strong_password)[0])
        self.assertFalse(is_password_strong(weak_password)[0])

    def test_generate_strong_password(self):
        """Prueba la generación de una contraseña fuerte."""
        password = generate_strong_password()
        self.assertTrue(is_password_strong(password)[0])

if __name__ == "__main__":
    unittest.main()