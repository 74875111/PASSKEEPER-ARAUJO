import flet as ft

def recover_password_view(page: ft.Page):
    page.title = "Recover Password"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.WHITE
    page.window_width = 400
    page.window_height = 450
    page.window_resizable = False
    page.window_center()
    page.window_maximizable = False  # Deshabilitar el botón de maximizar

    def on_back(e):
        page.clean()
        from view.login_view import login_view  # Importar aquí para evitar la importación circular
        login_view(page)

    email_input = ft.TextField(label="Email", border_color=ft.colors.RED_600, width=250)
    result = ft.Text()

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    email_input,
                    ft.ElevatedButton(text="Recover Password", on_click=lambda e: None),  # Lógica de recuperación aún no implementada
                    ft.ElevatedButton(text="Back", on_click=on_back),
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
    ft.app(target=recover_password_view)