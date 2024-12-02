import flet as ft
from database.models import Category, Session

def children_categories_view(page: ft.Page):
    session = Session()

    def reload_categories():
        categories = session.query(Category).all()
        category_items.controls.clear()
        category_items.controls.extend([
            ft.Row(
                [
                    ft.Text(category.name, expand=True),
                    ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, c=category: edit_category(c)),
                    ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, c=category: delete_category(c)),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=10,
            )
            for category in categories
        ])
        page.update()

    def add_category(e):
        category_name = category_name_input.value
        if not category_name:
            result_text.value = "Please enter a category name."
            page.update()
            return

        new_category = Category(name=category_name)
        session.add(new_category)
        session.commit()
        result_text.value = "Category added successfully!"
        category_name_input.value = ""
        reload_categories()

    def delete_category(category):
        session.delete(category)
        session.commit()
        reload_categories()

    def edit_category(category):
        edit_category_name_input.value = category.name
        edit_category_dialog.open = True
        page.update()

        def save_category(e):
            category.name = edit_category_name_input.value
            session.commit()
            edit_category_dialog.open = False
            reload_categories()
            page.update()

        save_button.on_click = save_category

    def close_edit_dialog(e):
        edit_category_dialog.open = False
        page.update()

    category_name_input = ft.TextField(label="Category Name", width=250)
    result_text = ft.Text()
    category_items = ft.Column()

    edit_category_name_input = ft.TextField(label="Edit Category Name", width=250)
    save_button = ft.ElevatedButton(text="Save")
    edit_category_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Edit Category"),
        content=ft.Column(
            [
                edit_category_name_input,
                save_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        actions=[
            ft.TextButton("Cancel", on_click=close_edit_dialog)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    reload_categories()

    return ft.Column(
        [
            ft.Row(
                [
                    category_name_input,
                    ft.ElevatedButton(text="Add Category", on_click=add_category),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            result_text,
            category_items,
            edit_category_dialog,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )