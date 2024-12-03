import flet as ft
from sqlalchemy.orm import sessionmaker
from database.models import User, engine
from authenticated.user_actions import delete_account

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

def children_settings_view(page: ft.Page, user, login_view):
    def confirm_delete_account(e):
        password = password_input.value
        if not password:
            result_text.value = "Please enter your password."
            page.update()
            return

        # Llamar a la función para eliminar la cuenta del usuario
        result_text.value = delete_account(user.id, password)
        if result_text.value == "Account and all associated passwords and categories deleted successfully.":
            # Redirigir al login
            page.client_storage.remove("session_token")
            print("Token removed.")
            page.clean()
            login_view(page)

    def cancel_delete_account(e):
        delete_section.visible = False
        page.update()

    def toggle_password_visibility(e):
        password_input.password = not password_input.password
        page.update()

    password_input = ft.TextField(label="Password", password=True, width=250)
    show_password_checkbox = ft.Checkbox(label="Show Password", on_change=toggle_password_visibility)
    result_text = ft.Text()

    delete_section = ft.Column(
        [
            password_input,
            show_password_checkbox,
            ft.ElevatedButton(text="Confirm", on_click=confirm_delete_account),
            ft.ElevatedButton(text="Cancel", on_click=cancel_delete_account),
            result_text,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        visible=True  # Visible inicialmente
    )

    return ft.Column(
        [
            ft.Text("Delete account", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.RED_600),
            delete_section,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )