import flet as ft
from authenticated import user_actions
import time

def register_view(page: ft.Page, login_view):
    print("Opening register view.")
    page.title = "Register"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.WHITE
    page.window_width = 400
    page.window_height = 600
    page.window_resizable = False
    page.window_center()
    page.window_maximizable = False

    def toggle_password_visibility(e):
        password_input.password = not password_input.password
        page.update()

    def on_register(e):
        email = email_input.value
        password = password_input.value
        is_strong, password_message = user_actions.is_password_strong(password)
        if not is_strong:
            result.value = password_message
            result.color = ft.colors.RED
            page.update()
            return

        message = user_actions.create_user(email, password)

        if message == "User created successfully.":
            # Mostrar feedback en verde
            result.value = "Registration successful"
            result.color = ft.colors.GREEN
            # Bloquear todos los inputs, botones y casillas
            email_input.disabled = True
            password_input.disabled = True
            show_password_checkbox.disabled = True
            register_button.disabled = True
            back_button.disabled = True
            page.update()
            # Esperar 2 segundos antes de redirigir al login
            time.sleep(2)
            page.clean()
            login_view(page)
        else:
            # Mostrar feedback en rojo
            result.value = message
            result.color = ft.colors.RED
            page.update()

    def on_back(e):
        page.clean()
        login_view(page)

    email_input = ft.TextField(label="Email", border_color=ft.colors.RED_600, width=250)
    password_input = ft.TextField(label="Password", password=True, border_color=ft.colors.RED_600, width=250)
    show_password_checkbox = ft.Checkbox(label="Show Password", on_change=toggle_password_visibility)
    result = ft.Text()

    register_button = ft.ElevatedButton(text="Register", on_click=on_register)
    back_button = ft.ElevatedButton(text="Back", on_click=on_back)

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Register", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.RED_600),
                    email_input,
                    password_input,
                    show_password_checkbox,
                    register_button,
                    back_button,
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