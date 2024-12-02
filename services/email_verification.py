import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la clave de API desde la variable de entorno
API_KEY = os.getenv('ABSTRACT_API_KEY')

def verify_email(email):
    url = f'https://emailvalidation.abstractapi.com/v1/?api_key={API_KEY}&email={email}'
    response = requests.get(url)
    data = response.json()
    
    if data['is_valid_format']['value'] and data['is_smtp_valid']['value']:
        return True, "Email is valid and can receive emails."
    else:
        return False, "Email is invalid or cannot receive emails."