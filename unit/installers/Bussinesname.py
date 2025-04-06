import flet as ft
from DB.db_setup import initialize_database  # Importar la función para la base de datos

class PageContent:
    def __init__(self, page, navigate_to, app):
        self.page = page
        self.navigate_to = navigate_to

    def show(self):
        def validate_entry(e):
            business_name = e.control.value.upper()  # Convertir entrada a mayúsculas
            e.control.value = business_name  # Actualizar el texto en el campo
            self.page.update()  # Refrescar la página

            # Habilitar el botón si el campo no está vacío
            if business_name.strip():  # Verificar que el campo tenga texto
                continue_button.disabled = False
                error_message.visible = False  # Ocultar mensaje de error
            else:
                continue_button.disabled = True
                error_message.visible = True  # Mostrar mensaje de error
            self.page.update()

        def on_continue(_):
            business_name = business_name_field.value.upper()  # Nombre del negocio
            initialize_database(business_name)  # Crear la base de datos y tabla inicial
            self.navigate_to("unit.installers.Install_tools")  # Navegar a la siguiente página

        # Campo de entrada del nombre del negocio
        business_name_field = ft.TextField(
            label="Nombre del negocio",
            hint_text="Escriba el nombre aquí",
            width=500,
            border_color=ft.colors.BLACK,
            color=ft.colors.BLACK,
            focused_border_color=ft.colors.BLACK,
            cursor_color=ft.colors.BLACK,
            on_change=validate_entry,  # Validación de entrada
        )

        # Botón Continuar inicial desactivado
        continue_button = ft.ElevatedButton(
            text="Continuar",
            on_click=on_continue,  # Actualizar la base de datos y continuar
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE,
            disabled=True,
        )

        # Mensaje de error inicial oculto
        error_message = ft.Text(
            "El campo no puede estar vacío.",
            color=ft.colors.RED,
            visible=False,
        )

        return ft.Container(
            bgcolor=ft.colors.WHITE,
            expand=True,
            padding=ft.padding.all(20),
            content=ft.Column(
                controls=[
                    ft.Container(
                        bgcolor=ft.colors.WHITE,
                        padding=ft.padding.all(15),
                        border_radius=10,
                        content=ft.Text(
                            "Registrar Negocio",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.BLACK,
                            text_align="center",
                        ),
                    ),
                    ft.Container(margin=ft.margin.only(top=20)),
                    ft.Container(
                        bgcolor=ft.colors.GREY_200,
                        padding=ft.padding.all(15),
                        border_radius=10,
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "Por favor, proporcione el nombre que representará a su negocio.",
                                    size=16,
                                    color=ft.colors.BLACK,
                                    text_align="left",
                                ),
                                ft.Text(
                                    "Este será el identificador principal de su entidad, almacén u organización.",
                                    size=16,
                                    color=ft.colors.BLACK,
                                    text_align="left",
                                ),
                                business_name_field,
                                error_message,
                            ],
                            spacing=10,
                        ),
                    ),
                    ft.Container(margin=ft.margin.only(top=30)),
                    ft.Container(
                        content=continue_button,
                        alignment=ft.alignment.bottom_right,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
        )