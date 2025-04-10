import os
import shutil
import flet as ft
from DB.db_setup import BusinessDB  # Importar la función para inicializar la base de datos


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

        # Actualizar el archivo key.txt con el nombre del negocio
        def update_key_file(business_name):
            try:
                # Ruta del archivo fuente (local)
                source_key_path = os.path.join(os.getcwd(), "key.txt")
                if not os.path.exists(source_key_path):
                    raise FileNotFoundError("No se encontró el archivo 'key.txt' en la raíz local.")

                # Leer contenido actual del archivo
                with open(source_key_path, "r", encoding="utf-8") as file:
                    content = file.readlines()

                # Actualizar el campo 'Negocio:'
                for i, line in enumerate(content):
                    if "Negocio:" in line:
                        content[i] = f"          Negocio: {business_name}\n"

                # Escribir el contenido actualizado
                with open(source_key_path, "w", encoding="utf-8") as file:
                    file.writelines(content)

                # Copiar el archivo actualizado a C:\MagicCorp
                destination_key_path = os.path.join("C:\\", "MagicCorp", "key.txt")
                magiccorp_path = os.path.join("C:\\", "MagicCorp")
                if not os.path.exists(magiccorp_path):
                    os.mkdir(magiccorp_path)  # Crear carpeta MagicCorp si no existe
                shutil.copy(source_key_path, destination_key_path)
                print(f"Archivo 'key.txt' actualizado y copiado exitosamente a {destination_key_path}")
            except Exception as ex:
                raise Exception(f"Error al actualizar el archivo 'key.txt': {str(ex)}")

        # Acción al presionar "Continuar"
        def on_continue(_):
            business_name = business_name_field.value.upper().strip()  # Obtener el nombre del negocio
            if not business_name:
                show_error_message("Por favor, ingrese un nombre válido para continuar.")  # Mostrar error si está vacío
                return
            try:
                # Actualizar el archivo key.txt con el nombre del negocio
                update_key_file(business_name)

                # Ruta de la carpeta de bases de datos
                db_path = os.path.join("C:\\", "MagicCorp", "DB")

                # Intentar inicializar la base de datos pasando la ruta y el nombre del negocio
                BusinessDB(db_path, business_name)

                # Actualizar el checkbox correspondiente en `InstallPage`
                if hasattr(self.app, "_update_checkboxes"):
                    self.app._update_checkboxes("BusinessName")  # Activar el checkbox correspondiente
                else:
                    print("Error: No se pudo actualizar el checkbox.")

                # Navegar a la siguiente página si no hay errores
                self.navigate_to("unit.installers.Install_tools")
            except Exception as ex:
                # Mostrar el error en un banner si ocurre un problema
                show_error_message(f"Error: {str(ex)}")

        # Campo de entrada del nombre del negocio
        business_name_field = ft.TextField(
            label="Nombre del Negocio:",
            hint_text="Escriba el nombre de su empresa aquí",
            width=500,
            border_color=ft.colors.BLACK,
            color=ft.colors.BLACK,
            focused_border_color=ft.colors.BLUE,
            cursor_color=ft.colors.BLUE,
            on_change=validate_entry,  # Validación de entrada
        )

        # Botón Continuar siempre habilitado
        continue_button = ft.ElevatedButton(
            text="Registrar Negocio",
            on_click=on_continue,  # Intentar actualizar la base de datos y manejar errores
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE,
            icon=ft.icons.CHECK_CIRCLE,  # Icono más profesional
        )

        # Contenedor emergente para mensajes de error
        error_banner = ft.Container(
            visible=False,  # Inicialmente oculto
            bgcolor=ft.colors.RED,  # Fondo rojo para mayor claridad de error
            padding=ft.padding.all(10),
            border_radius=10,
            content=ft.Row(
                controls=[
                    ft.Text(
                        value="",  # El mensaje dinámico se mostrará aquí
                        color=ft.colors.WHITE,  # Texto blanco sobre fondo rojo
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

        # Título y descripción inicial mejorados
        title_container = ft.Container(
            bgcolor=ft.colors.BLUE,
            padding=ft.padding.all(20),
            border_radius=10,
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Registrar Nombre de su Negocio",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.WHITE,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Este nombre será el identificador principal de su negocio y no podrá cambiarse posteriormente.",
                        size=16,
                        color=ft.colors.WHITE,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                spacing=5,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        )

        return ft.Container(
            bgcolor=ft.colors.GREY_100,
            expand=True,
            padding=ft.padding.all(10),
            content=ft.Column(
                controls=[
                    title_container,
                    ft.Container(margin=ft.margin.only(top=5)),
                    ft.Container(
                        bgcolor=ft.colors.WHITE,
                        padding=ft.padding.all(15),
                        border_radius=10,
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "Proporcione el nombre de su empresa, este será el identificador de su organización.",
                                    size=16,
                                    color=ft.colors.BLACK,
                                    text_align=ft.TextAlign.LEFT,
                                ),
                                business_name_field,
                            ],
                            spacing=15,
                        ),
                    ),
                    ft.Container(margin=ft.margin.only(top=5)),
                    ft.Container(
                        content=continue_button,
                        alignment=ft.alignment.bottom_center,
                    ),
                    error_banner,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
        )