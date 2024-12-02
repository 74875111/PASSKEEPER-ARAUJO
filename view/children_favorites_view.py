import flet as ft
from authenticated import user_actions
from cryptography.fernet import InvalidToken
from database.models import Session, Category

def children_favorites_view(page: ft.Page, user):
    session = Session()

    def reload_passwords():
        passwords = user_actions.list_favorite_passwords(user.id)
        password_count.value = f"Total Favorite Passwords: {len(passwords)}"
        password_items.controls.clear()
        password_items.controls.extend([
            ft.ListTile(
                title=ft.Text(f"Service: {password.service_name}"),
                subtitle=ft.Text(f"User/Email: {password.user_email}\nCategory: {password.category.name if password.category else 'Sin categoría'}\nFavorite: {'Yes' if password.is_favorite else 'No'}"),
                on_click=lambda e, p=password: open_password(e, p),
                trailing=ft.Icon(ft.icons.ARROW_FORWARD),
            )
            for password in passwords
        ])
        page.update()

    passwords = user_actions.list_favorite_passwords(user.id)

    def open_password(e, password):
        def on_delete_password(ev):
            confirm_dialog.open = True
            page.update()

        def confirm_delete(ev):
            user_actions.delete_password(password.id)
            confirm_dialog.open = False
            password_dialog.open = False
            reload_passwords()

        def on_edit_password(ev):
            service_name_input.read_only = False
            user_email_input.read_only = False
            password_input.read_only = False
            category_dropdown.disabled = False
            favorite_checkbox.disabled = False
            save_button.visible = True
            page.update()

        def on_save_password(ev):
            category_name = category_dropdown.value
            category_id = None
            if category_name and category_name != "No hay categorías":
                category = session.query(Category).filter_by(name=category_name).first()
                if category:
                    category_id = category.id

            user_actions.update_password(password.id, service_name_input.value, user_email_input.value, password_input.value, category_id, favorite_checkbox.value)
            password_dialog.open = False
            reload_passwords()

        def toggle_password_visibility(ev):
            password_input.password = not password_input.password
            page.update()

        def close_dialog(ev):
            password_dialog.open = False
            page.update()

        def close_confirm_dialog(ev):
            confirm_dialog.open = False
            page.update()

        # Desencriptar la contraseña
        try:
            decrypted_password = user_actions.fernet.decrypt(password.password.encode()).decode()
        except InvalidToken:
            decrypted_password = "Invalid token"

        categories = session.query(Category).all()
        category_names = [category.name for category in categories]
        category_dropdown = ft.Dropdown(
            label="Category (Optional)",
            options=[ft.dropdown.Option(name) for name in category_names],
            value=password.category.name if password.category else None,
            width=250,
            disabled=True
        )

        service_name_input = ft.TextField(label="Service Name", value=password.service_name, width=250, read_only=True)
        user_email_input = ft.TextField(label="User/Email", value=password.user_email, width=250, read_only=True)
        password_input = ft.TextField(label="Password", value=decrypted_password, password=True, width=250, read_only=True)
        show_password_checkbox = ft.Checkbox(label="Show Password", on_change=toggle_password_visibility)
        favorite_checkbox = ft.Checkbox(label="Favorite", value=password.is_favorite, disabled=True)
        save_button = ft.ElevatedButton(text="Save", on_click=on_save_password, visible=False)

        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirm Deletion"),
            content=ft.Text("Are you sure you want to delete this password?"),
            actions=[
                ft.TextButton("Cancel", on_click=close_confirm_dialog),
                ft.TextButton("Delete", on_click=confirm_delete),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        password_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Password Details"),
            content=ft.Column(
                [
                    service_name_input,
                    user_email_input,
                    password_input,
                    category_dropdown,
                    show_password_checkbox,
                    favorite_checkbox,
                    ft.Row(
                        [
                            ft.IconButton(icon=ft.icons.DELETE, on_click=on_delete_password, tooltip="Delete Password"),
                            ft.IconButton(icon=ft.icons.EDIT, on_click=on_edit_password, tooltip="Edit Password"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    save_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            actions=[
                ft.TextButton("Close", on_click=close_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.dialog = password_dialog
        password_dialog.open = True
        page.update()

        # Mostrar el cuadro de confirmación de eliminación cuando sea necesario
        page.dialog = confirm_dialog

    password_count = ft.Text(f"Total Favorite Passwords: {len(passwords)}", size=20, weight=ft.FontWeight.BOLD)
    password_items = ft.ListView(
        expand=True,
        spacing=10,
        padding=10,
    )

    reload_passwords()

    return ft.Column(
        [
            password_count,
            password_items,
        ],
        expand=True,
        spacing=10,
    )