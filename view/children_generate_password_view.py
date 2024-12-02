import flet as ft
from utils.password_utils import generate_strong_password

def children_generate_password_view(page: ft.Page):
    def generate_password(e):
        new_password = generate_strong_password()
        password_input.value = new_password
        result_text.value = "Password generated successfully!"
        page.update()

    def copy_password(e):
        page.set_clipboard(password_input.value)
        result_text.value = "Password copied to clipboard!"
        page.update()

    password_input = ft.TextField(label="Generated Password", password=False, width=250, read_only=True)
    generate_button = ft.ElevatedButton(text="Generate Password", on_click=generate_password)
    copy_button = ft.ElevatedButton(text="Copy Password", on_click=copy_password)
    result_text = ft.Text()

    return ft.Column(
        [
            password_input,
            generate_button,
            copy_button,
            result_text,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )