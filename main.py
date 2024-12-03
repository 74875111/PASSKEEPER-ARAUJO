import flet as ft
from view.login_view import login_view

def main(page: ft.Page):
    page.window_width = 400
    page.window_height = 400
    page.window_resizable = False

    def on_close(e):
        print("Application is closing.")
        page.client_storage.remove("session_token")
        print("Token removed on close.")

    page.on_close = on_close
    login_view(page)

ft.app(target=main)