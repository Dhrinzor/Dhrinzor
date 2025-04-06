import os
import flet as ft

class PageContent:
    def __init__(self, page, navigate_to, app):
        self.page = page
        self.navigate_to = navigate_to
        self.app = app  # Referencia a `InstallPage`

    def show(self):
        # Ruta del archivo de licencia
        license_path = r"D:\APP\the magic card program\license.txt"

        # Leer el contenido del archivo de licencia
        try:
            with open(license_path, "r", encoding="utf-8") as file:  # Asegurarse de leer con UTF-8
                license_text = file.read().splitlines()  # Dividir el texto en líneas
        except FileNotFoundError:
            license_text = ["No se encontró el archivo de licencia. Verifique la instalación."]
            print("Error: El archivo de licencia no existe en la ruta especificada.")
        except UnicodeDecodeError as e:
            license_text = ["Error al leer el archivo de licencia. Codificación incompatible."]
            print(f"Error de decodificación: {e}")

        # Crear elementos para el ListView con el texto de la licencia
        license_items = [
            ft.Text(line, size=16, color=ft.colors.BLACK) for line in license_text
        ]

        # Crear la estructura de la página
        return ft.Container(
            bgcolor=ft.colors.WHITE,
            expand=True,
            padding=ft.padding.all(10),
            content=ft.Column(
                controls=[
                    # Contenedor superior con el título "Acuerdo de Licencia"
                    ft.Container(
                        bgcolor=ft.colors.WHITE,
                        padding=ft.padding.all(5),
                        border_radius=10,
                        content=ft.Text(
                            "Acuerdo de Licencia",
                            size=25,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.BLACK,
                            text_align="center",
                        ),
                    ),
                    # Espaciador visual
                    ft.Container(margin=ft.margin.only(top=2)),
                    # Contenedor con el texto desplazable de la licencia
                    ft.Container(
                        bgcolor=ft.colors.GREY_200,
                        padding=ft.padding.all(5),
                        border_radius=10,
                        content=ft.ListView(
                            controls=license_items,  # Agrega las líneas de texto al ListView
                        ),
                        height=355,  # Altura del contenedor
                        width=550,  # Ancho del contenedor
                    ),
                    # Espaciador visual para separar de los botones
                    ft.Container(margin=ft.margin.only(top=5)),
                    # Botones "Aceptar" y "Rechazar"
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                text="Aceptar",
                                on_click=self._handle_accept_license,
                                bgcolor=ft.colors.GREEN,
                                color=ft.colors.WHITE,
                            ),
                            ft.ElevatedButton(
                                text="Rechazar",
                                on_click=self._handle_reject_license,
                                bgcolor=ft.colors.RED,
                                color=ft.colors.WHITE,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,  # Espaciado entre los botones
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,  # Espaciado entre los elementos principales
            ),
        )

    def _handle_accept_license(self, e):
        print("Licencia aceptada.")  # Confirmar aceptación
        if hasattr(self.app, "_update_checkboxes"):
            self.app._update_checkboxes("License")  # Actualizar el checkbox desde `InstallPage`
        else:
            print("Error: No se pudo actualizar el checkbox.")
        self.navigate_to("unit.installers.Bussinesname")  # Navegar a la página siguiente

    def _handle_reject_license(self, e):
        print("Licencia rechazada.")  # Confirmar rechazo
        self.navigate_to("unit.installers.Welcome")  # Redirigir a la página inicial