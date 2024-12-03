import flet as ft
from sqlalchemy.orm import sessionmaker
from database.models import Category, User, engine
from authenticated.user_actions import create_category, list_categories

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

def children_categories_view(page: ft.Page, user):
    def reload_categories():
        print("Reloading categories...")  # Feedback en consola
        categories = list_categories(user.id)
        category_list.controls.clear()
        for category in categories:
            category_list.controls.append(
                ft.Row(
                    [
                        ft.Text(category.name, expand=True),
                        ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, c=category: open_edit_dialog(c)),
                        ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, c=category: confirm_delete_category(c)),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    spacing=10,
                )
            )
        page.update()
        print("Categories reloaded.")  # Feedback en consola

    def add_category(e):
        category_name = category_name_input.value
        if not category_name:
            result_text.value = "Please enter a category name."
            page.update()
            return

        # Verificar si ya existe una categoría con el mismo nombre
        existing_category = session.query(Category).filter_by(name=category_name, user_id=user.id).first()
        if existing_category:
            result_text.value = "Category with the same name already exists."
            page.update()
            return

        try:
            new_category = Category(name=category_name, user_id=user.id)
            session.add(new_category)
            session.commit()
            result_text.value = "Category added successfully!"
        except Exception as e:
            session.rollback()
            result_text.value = f"Error adding category: {str(e)}"
        finally:
            category_name_input.value = ""
            reload_categories()

    def confirm_delete_category(category):
        delete_category_dialog.content = ft.Text(f"Are you sure you want to delete the category '{category.name}'?")
        delete_category_dialog.actions = [
            ft.TextButton("Yes", on_click=lambda e: delete_category(category)),
            ft.TextButton("No", on_click=lambda e: close_delete_dialog())
        ]
        delete_category_dialog.open = True
        page.update()

    def close_delete_dialog():
        delete_category_dialog.open = False
        page.update()

    def delete_category(category):
        # Recargar el objeto Category en la sesión actual antes de eliminarlo
        category_to_delete = session.query(Category).filter_by(id=category.id).first()
        if category_to_delete:
            session.delete(category_to_delete)
            session.commit()
            print(f"Category '{category.name}' deleted.")  # Feedback en consola
            reload_categories()
        close_delete_dialog()

    def open_edit_dialog(category):
        edit_category_name_input.value = category.name
        edit_category_dialog.open = True
        page.update()

        def save_category(e):
            print("Save button clicked")  # Feedback en consola
            new_name = edit_category_name_input.value
            existing_category = session.query(Category).filter_by(name=new_name, user_id=user.id).first()
            if existing_category and existing_category.id != category.id:
                result_text.value = "Category with the same name already exists."
                page.update()
                return

            category_to_edit = session.query(Category).filter_by(id=category.id).first()
            if category_to_edit:
                print(f"Editing category: {category_to_edit.name}")  # Feedback en consola
                category_to_edit.name = new_name
                try:
                    session.commit()
                    print(f"Category name updated to: {category_to_edit.name}")  # Feedback en consola
                    edit_category_dialog.open = False
                    reload_categories()
                except Exception as e:
                    session.rollback()
                    result_text.value = f"Error updating category: {str(e)}"
            else:
                print("Category not found")  # Feedback en consola
            page.update()

        save_button.on_click = save_category

    category_name_input = ft.TextField(label="Category Name", border_color=ft.colors.RED_600, width=250)
    result_text = ft.Text()

    edit_category_name_input = ft.TextField(label="Edit Category Name", border_color=ft.colors.RED_600, width=250)
    save_button = ft.ElevatedButton(text="Save")
    edit_category_dialog = ft.AlertDialog(
        modal=True,
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
            ft.TextButton("Cancel", on_click=lambda e: close_edit_dialog())
        ]
    )

    def close_edit_dialog():
        edit_category_dialog.open = False
        page.update()

    delete_category_dialog = ft.AlertDialog(
        modal=True,
        content=ft.Text(""),
        actions=[]
    )

    page.overlay.append(edit_category_dialog)
    page.overlay.append(delete_category_dialog)

    category_list = ft.ListView(expand=True, spacing=10)

    container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Categories", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.RED_600),
                category_name_input,
                ft.ElevatedButton(text="Add Category", on_click=add_category),
                result_text,
                category_list,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        alignment=ft.alignment.center,
        padding=20,
        expand=True,
    )

    reload_categories()  # Llamar a reload_categories para cargar las categorías existentes

    return container