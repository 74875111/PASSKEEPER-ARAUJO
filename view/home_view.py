import flet as ft
from view.children_password_view import children_password_view
from view.children_add_password_view import children_add_password_view
from view.children_categories_view import children_categories_view
from view.children_favorites_view import children_favorites_view
from view.children_generate_password_view import children_generate_password_view
from view.children_settings_view import children_settings_view
def home_view(page: ft.Page, user, login_view):
    print("Opening home view.")
    page.title = "Home"
    page.window_width = 1200
    page.window_height = 800
    page.window_resizable = False
    page.bgcolor = ft.colors.WHITE

    def show_passwords(e):
        content_container.content = children_password_view(page, user)
        page.update()

    def show_add_password(e):
        content_container.content = children_add_password_view(page, user)
        page.update()

    def show_categories(e):
        content_container.content = children_categories_view(page, user)
        page.update()

    def show_favorites(e):
        content_container.content = children_favorites_view(page, user)
        page.update()

    def show_generate_password(e):
        content_container.content = children_generate_password_view(page)
        page.update()

    def show_settings(e):
        content_container.content = children_settings_view(page, user,login_view)
        page.update()

    def logout(e):
        page.client_storage.remove("session_token")
        print("Token removed.")
        page.clean()
        login_view(page)

    sidebar = ft.Column(
        [
            ft.Text("Navigation", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
            ft.ElevatedButton(text="Add Password", on_click=show_add_password, bgcolor=ft.colors.GREEN_600, color=ft.colors.WHITE, width=150),
            ft.ElevatedButton(text="Passwords", on_click=show_passwords, bgcolor=ft.colors.BLUE_600, color=ft.colors.WHITE, width=150),
            ft.ElevatedButton(text="Favorites", on_click=show_favorites, bgcolor=ft.colors.BLUE_600, color=ft.colors.WHITE, width=150),
            ft.ElevatedButton(text="Categories", on_click=show_categories, bgcolor=ft.colors.BLUE_600, color=ft.colors.WHITE, width=150),
            ft.ElevatedButton(text="Generate Password", on_click=show_generate_password, bgcolor=ft.colors.BLUE_600, color=ft.colors.WHITE, width=150),
            ft.ElevatedButton(text="Delete account", on_click=show_settings, bgcolor=ft.colors.BLUE_600, color=ft.colors.WHITE, width=150),
            ft.ElevatedButton(text="Logout", on_click=logout, bgcolor=ft.colors.RED_600, color=ft.colors.WHITE, width=150),
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        width=200,
    )

    global content_container
    content_container = ft.Container(
        content=ft.Text("Select an option from the sidebar", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
        expand=True,
    )

    page.add(
        ft.Row(
            [
                sidebar,
                content_container,
            ],
            expand=True,
        )
    )