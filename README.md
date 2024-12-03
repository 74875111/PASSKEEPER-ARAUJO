
# PassKeeper

**PassKeeper** es una herramienta diseñada para que los usuarios puedan almacenar y gestionar sus contraseñas de forma segura. Este proyecto utiliza una base de datos SQLite para proteger los datos.

## Equipo de desarrollo
| **Apellidos y Nombres**         | **Rol**         |
|----------------------------------|-----------------|
| Araujo Huamani, Leonardo Daniel | Scrum Master    |

## Para iniciar la aplicación

### 1. Activar el entorno virtual (.venv)
.venv\Scripts\activate.bat

### 2. Correr el archivo main.py
python main.py

### 3. Correr las pruebas
python -m unittest discover -s tests

### En caso de que te falte alguna libreria 
pip install -r requirements.txt

## Principales Funciones

- **Registro y inicio de sesión:**
    
    - Crea una cuenta usando tu correo electrónico y una contraseña maestra segura.
    - Inicia sesión en la aplicación con tu correo y contraseña maestra.
- **Gestión de contraseñas:**
    
    - Añade, edita y elimina contraseñas de forma rápida y segura.
    - Organiza tus contraseñas en categorías personalizadas.
    - Marca contraseñas como favoritas para un acceso rápido.
- **Generación de contraseñas seguras:**
    
    - Crea contraseñas seguras automáticamente desde la aplicación.
- **Visualización organizada:**
    
    - Visualiza todas tus contraseñas guardadas y organizadas por categoría.
    - Accede rápidamente a tus contraseñas favoritas o por categoría.
- **Seguridad adicional:**
    
    - Las contraseñas se mantienen ocultas por defecto.
    - Se muestra la robustez de cada contraseña y se sugieren cambios si son débiles.
    - Se eliminan automáticamente las contraseñas copiadas del portapapeles después de usarlas.
- **Cerrar sesión y mantener la seguridad:**
    
    - Cierra sesión en la aplicación para proteger tus datos.
    - Opción de mantener la sesión activa durante un período de tiempo configurable.
- **Interfaz simple y minimalista:**
    
    - Diseño limpio y sencillo para una experiencia de usuario eficiente.

## Mensaje final 
Espero que mi aplicación sea de su agrado y desearle a usted Ing.Daniel Gamarra unas bonitas fiestas y prosperidad.  

# Licencia
Este proyecto está bajo la licencia MIT. Para más información, consulta el archivo LICENSE.