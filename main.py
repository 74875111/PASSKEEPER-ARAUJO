import flet as ft
from view.login_view import login_view

def main(page: ft.Page):
    page.window_width = 400
    page.window_height = 400
    page.window_resizable = False
    login_view(page)

ft.app(target=main)