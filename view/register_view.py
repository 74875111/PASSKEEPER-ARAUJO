import flet as ft
from authenticated import user_actions
import time


def register_view(page: ft.Page):
    page.title = "Register"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.WHITE

    def on_register(e):
        email = email_input.value
        password = password_input.value
        use_email_verification = email_verification_checkbox.value

        # Verificar la robustez de la contraseña
        is_strong, password_message = user_actions.is_password_strong(password)
        if not is_strong:
            result.value = password_message
            page.update()
            return

        if use_email_verification:
            message = user_actions.create_user_with_email_verification(email, password)
        else:
            message = user_actions.create_user(email, password)

        result.value = message
        page.update()

        if "successfully" in message:
            time.sleep(
                2
            )  # Esperar 2 segundos antes de cambiar a la pantalla de inicio de sesión
            page.clean()
            from view.login_view import (
                login_view,
            )  # Importar aquí para evitar la importación circular

            login_view(page)
        else:
            page.update()

    def on_back(e):
        page.clean()
        from view.login_view import (
            login_view,
        )  # Importar aquí para evitar la importación circular

        login_view(page)

    def toggle_password_visibility(e):
        password_input.password = not password_input.password
        page.update()

    email_input = ft.TextField(label="Email", border_color=ft.colors.RED_600, width=250)
    password_input = ft.TextField(
        label="Password", password=True, border_color=ft.colors.RED_600, width=250
    )
    show_password_checkbox = ft.Checkbox(
        label="Show Password", on_change=toggle_password_visibility
    )
    email_verification_checkbox = ft.Checkbox(
        label="Crear con verificación de email", value=True
    )
    result = ft.Text()

    page.add(
        ft.Column(
            [
                ft.Text(
                    "Register", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.RED_600
                ),
                email_input,
                password_input,
                show_password_checkbox,
                email_verification_checkbox,
                ft.ElevatedButton(text="Register", on_click=on_register),
                ft.ElevatedButton(text="Back", on_click=on_back),
                result,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
    )


if __name__ == "__main__":
    ft.app(target=register_view)
