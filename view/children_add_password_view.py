import flet as ft
from authenticated import user_actions
from database.models import Session, Category

def children_add_password_view(page: ft.Page, user):
    session = Session()

    def on_add_password(ev):
        service_name = service_name_input.value
        user_email = user_email_input.value
        password = password_input.value
        category_name = category_dropdown.value

        if not service_name or not user_email or not password:
            result_text.value = "Please fill in all required fields."
            page.update()
            return

        category_id = None
        if category_name and category_name != "No hay categorías":
            category = session.query(Category).filter_by(name=category_name).first()
            if category:
                category_id = category.id

        user_actions.create_password(service_name, user_email, password, user.id, category_id)
        result_text.value = "Password added successfully!"
        form_container.visible = False
        add_another_button.visible = True
        page.update()

    def add_another(ev):
        service_name_input.value = ""
        user_email_input.value = ""
        password_input.value = ""
        category_dropdown.value = None
        result_text.value = ""
        form_container.visible = True
        add_another_button.visible = False
        page.update()

    categories = session.query(Category).all()
    if categories:
        category_names = [category.name for category in categories]
    else:
        category_names = ["No hay categorías"]

    service_name_input = ft.TextField(label="Service Name", width=250)
    user_email_input = ft.TextField(label="User/Email", width=250)
    password_input = ft.TextField(label="Password", password=True, width=250)
    category_dropdown = ft.Dropdown(
        label="Category (Optional)",
        options=[ft.dropdown.Option(name) for name in category_names],
        width=250
    )
    result_text = ft.Text()
    add_another_button = ft.ElevatedButton(text="Add Another", on_click=add_another, visible=False)

    form_container = ft.Column(
        [
            service_name_input,
            user_email_input,
            password_input,
            category_dropdown,
            ft.ElevatedButton(text="Add Password", on_click=on_add_password),
            result_text,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )

    return ft.Column(
        [
            form_container,
            add_another_button,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )