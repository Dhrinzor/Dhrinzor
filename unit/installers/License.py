import flet as ft

class PageContent:
    def __init__(self, page, navigate_to, app):
        self.page = page
        self.navigate_to = navigate_to
        self.app = app  # Referencia a la instancia de InstallPage

    def show(self):
        # Contenedor principal que organiza los elementos en la página
        return ft.Container(
            bgcolor=ft.colors.WHITE,
            expand=True,
            padding=ft.padding.all(20),
            border_radius=15,
            content=ft.Column(
                controls=[
                    # Título "Bienvenido" centrado en la parte superior
                    ft.Text(
                        "Licencia", 
                        size=30, 
                        weight=ft.FontWeight.BOLD, 
                        color=ft.colors.BLACK,
                        text_align="center"
                    ),
                    # Divider
                    ft.Divider(height=30, thickness=1, color=ft.colors.GREY),
                    # Mensaje de bienvenida
                    ft.Text(
                        "¡Bienvenido a nuestra aplicación! Estamos emocionados de que estés aquí. En breve comenzaremos con la instalación de las principales caracteristicas de nuestra aplicación.",
                        size=18,
                        text_align="center",
                        color=ft.colors.GREY,
                    ),
                    # Botón "Comenzar" en la esquina inferior derecha
                    ft.Container(
                        content=ft.ElevatedButton(
                            text="Comenzar",
                            on_click=self._handle_start_button,
                        ),
                        alignment=ft.alignment.bottom_right,
                        margin=ft.margin.only(top=20),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,  # Espaciado entre elementos
            ),
        )

    def _handle_start_button(self, e):
        # Llamar al método de actualización de checkboxes en InstallPage
        self.app.actualizar_checkboxes()
        # Navegar a la página Username.py
        self.navigate_to("unit.installers.Username")