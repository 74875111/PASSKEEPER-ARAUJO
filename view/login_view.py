import flet as ft
from authenticated import user_actions
from session_manager import verify_token
from database.models import session, User
from view.home_view import home_view

def login_view(page: ft.Page):
    print("Opening login view.")
    page.title = "Login"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.WHITE
    page.window_width = 400
    page.window_height = 600
    page.window_resizable = False
    page.window_center()
    page.window_maximizable = False
     # Cerrar cualquier diálogo abierto
    if page.dialog:
        page.dialog.open = False
        page.dialog = None
        page.update()
     # Asegurarse de que la página se actualice
    page.update()
    def check_session():
        # Verificar el token de sesión antes de configurar la vista de login
        token = page.client_storage.get("session_token")
        print(f"Token retrieved: {token}")
        if token:
            user_id = verify_token(token)
            print(f"User ID from token: {user_id}")
            if user_id:
                user = session.query(User).filter_by(id=user_id).first()
                if user:
                    print("User found, navigating to home view.")
                    page.clean()
                    print("Opening home view.")
                    home_view(page, user, login_view)
                    return
                else:
                    print("User not found.")
            else:
                print("Invalid token.")
        else:
            print("No token found.")

    def on_login(e):
        email = email_input.value
        password = password_input.value
        message, user, token = user_actions.login(email, password)
        result.value = message
        if user:
            print(f"Token set: {token}")
            page.client_storage.set("session_token", token)
            stored_token = page.client_storage.get("session_token")
            print(f"Token stored: {stored_token}")
            page.clean()
            home_view(page, user, login_view)
        else:
            print("Login failed.")
        page.update()

    def on_register(e):
        from view.register_view import register_view
        page.clean()
        register_view(page,login_view)



    def toggle_password_visibility(e):
        password_input.password = not password_input.password
        page.update()

    email_input = ft.TextField(label="Email", border_color=ft.colors.RED_600, width=250)
    password_input = ft.TextField(label="Password", password=True, border_color=ft.colors.RED_600, width=250)
    show_password_checkbox = ft.Checkbox(label="Show Password", on_change=toggle_password_visibility)
    result = ft.Text()

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Login", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.RED_600),
                    email_input,
                    password_input,
                    show_password_checkbox,
                    ft.ElevatedButton(text="Login", on_click=on_login),
                    ft.ElevatedButton(text="Register", on_click=on_register),
                    result,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            alignment=ft.alignment.center,
            padding=20,
        )
    )

    # Llamar a la función de verificación de sesión
    check_session()