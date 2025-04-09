import flet as ft
from DB.db_setup import initialize_database  # Importar la función para la base de datos

class PageContent:
    def __init__(self, page, navigate_to, app):
        self.page = page
        self.navigate_to = navigate_to
        self.app = app  # Referencia a la instancia principal (`InstallPage`)

    def show(self):
        # Mostrar mensaje de error en un contenedor emergente
        def show_error_message(message):
            error_banner.content.controls[0].value = message  # Establecer el mensaje de error
            error_banner.visible = True  # Hacer visible el banner de error
            self.page.update()  # Actualizar la página

        # Ocultar el mensaje de error
        def hide_error_message(_):
            error_banner.visible = False  # Ocultar el banner de error
            self.page.update()  # Actualizar la página

        # Validar el campo de entrada
        def validate_entry(e):
            business_name = e.control.value.upper()  # Convertir entrada a mayúsculas
            e.control.value = business_name  # Actualizar el texto en el campo
            self.page.update()  # Refrescar la página

        # Acción al presionar "Continuar"
        def on_continue(_):
            business_name = business_name_field.value.upper().strip()  # Obtener el nombre del negocio
            if not business_name:
                show_error_message("El campo no puede estar vacío.")  # Mostrar error si está vacío
                return
            try:
                # Intentar inicializar la base de datos
                initialize_database(business_name)

                # Actualizar el checkbox correspondiente en `InstallPage`
                if hasattr(self.app, "_update_checkboxes"):
                    self.app._update_checkboxes("Bussinesname")  # Activar el checkbox correspondiente
                else:
                    print("Error: No se pudo actualizar el checkbox.")

                # Navegar a la siguiente página si no hay errores
                self.navigate_to("unit.installers.Install_tools")  
            except Exception as ex:
                # Mostrar el error en un banner si ocurre un problema
                show_error_message(f"Error: {str(ex)}")

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

        # Botón Continuar siempre habilitado
        continue_button = ft.ElevatedButton(
            text="Continuar",
            on_click=on_continue,  # Intentar actualizar la base de datos y manejar errores
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE,
        )

        # Contenedor emergente para mensajes de error
        error_banner = ft.Container(
            visible=False,  # Inicialmente oculto
            bgcolor=ft.colors.GREY_300,  # Fondo gris claro para mayor elegancia
            padding=ft.padding.all(10),
            border_radius=10,
            content=ft.Row(
                controls=[
                    ft.Text(
                        value="",  # El mensaje dinámico se mostrará aquí
                        color=ft.colors.BLACK,  # Texto negro para mayor claridad
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.ElevatedButton(
                        text="Cerrar",
                        bgcolor=ft.colors.GREY_800,
                        color=ft.colors.WHITE,
                        on_click=hide_error_message,  # Cerrar el mensaje al presionar el botón
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
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
                                ft.Text(
                                    "Este nombre no podrá modificarse en el futuro.",
                                    size=18,
                                    color=ft.colors.BLACK,
                                    text_align="left",
                                ),
                                business_name_field,
                            ],
                            spacing=10,
                        ),
                    ),
                    ft.Container(margin=ft.margin.only(top=30)),
                    ft.Container(
                        content=continue_button,
                        alignment=ft.alignment.bottom_right,
                    ),
                    # Contenedor de error ubicado debajo del botón
                    error_banner,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
        )