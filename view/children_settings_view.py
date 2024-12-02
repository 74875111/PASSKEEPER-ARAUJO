import flet as ft
from authenticated import user_actions

def children_settings_view(page: ft.Page, user):
    def on_delete_account(e):
        confirm_dialog.open = True
        page.update()

    def confirm_delete_account(e):
        password = password_input.value
        message = user_actions.delete_account(user.id, password)
        result_text.value = message
        if "successfully" in message:
            confirm_dialog.open = False
            page.update()
            page.clean()
            from view.login_view import login_view  # Importar aquí para evitar la importación circular
            login_view(page)
        else:
            confirm_dialog.open = False
            page.update()

    def close_confirm_dialog(e):
        confirm_dialog.open = False
        page.update()

    password_input = ft.TextField(label="Password", password=True, width=250)
    result_text = ft.Text()

    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirm Deletion"),
        content=ft.Column(
            [
                password_input,
                ft.ElevatedButton(text="Confirm", on_click=confirm_delete_account),
                ft.ElevatedButton(text="Cancel", on_click=close_confirm_dialog),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = confirm_dialog

    return ft.Column(
        [
            ft.Text("Settings", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.RED_600),
            ft.ElevatedButton(text="Delete Account", on_click=on_delete_account, bgcolor=ft.colors.RED_600, color=ft.colors.WHITE),
            result_text,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )