import flet as ft
from authenticated import user_actions
from view.register_view import register_view
from view.home_view import home_view
from view.recover_password_view import recover_password_view
from session_manager import verify_token
from database.models import session, User

def login_view(page: ft.Page):
    page.title = "Login"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.WHITE
    page.window_width = 400
    page.window_height = 600
    page.window_resizable = False
    page.window_center()
    page.window_maximizable = False  # Deshabilitar el botón de maximizar

    def on_login(e):
        email = email_input.value
        password = password_input.value
        message, user, token = user_actions.login(email, password)
        result.value = message
        if user:
            page.client_storage.set("session_token", token)
            page.clean()
            home_view(page, user, login_view)
        page.update()

    def on_register(e):
        page.clean()
        register_view(page)

    def on_recover_password(e):
        page.clean()
        recover_password_view(page)

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
                    ft.ElevatedButton(text="Forgot Password?", on_click=on_recover_password),
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

if __name__ == "__main__":
    def main(page: ft.Page):
        token = page.client_storage.get("session_token")
        if token:
            user_id = verify_token(token)
            if user_id:
                user = session.query(User).filter_by(id=user_id).first()
                if user:
                    home_view(page, user, login_view)
                    return
        page.clean()
        login_view(page)

    ft.app(target=main)