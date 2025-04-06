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
                            "Bienvenido",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.BLACK,
                            text_align="center",
                        ),
                        ft.Text(
                            "Es un placer tenerte con nosotros.",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.BLACK,
                            text_align="center",
                        ),
            
                    # Mensaje de bienvenida
                    ft.Text(
                                    "Nuestra misión es proporcionarte una experiencia única y herramientas excepcionales que harán que tu día a día sea más eficiente y gratificante.",
                                    size=17,
                                    color=ft.colors.BLACK,
                                ),
                                ft.Text(
                                    "Este es el primer paso hacia un entorno más intuitivo y personalizado, que hemos creado pensando en ti.",
                                    size=17,
                                    color=ft.colors.BLACK,
                                ),
                                ft.Text(
                                    "Estamos aquí para apoyarte en cada etapa del camino y asegurarnos de que disfrutes al máximo de todas las capacidades que nuestra aplicación tiene para ofrecer.",
                                    size=18,
                                    color=ft.colors.BLACK,
                                ),
                                ft.Text(
                                    "Gracias por confiar en nosotros para ser parte de este proyecto.",
                                    size=20,
                                    text_align="center",
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.BLACK,
                                ),
                                
                            #alignment=ft.MainAxisAlignment.CENTER,
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
        self.navigate_to("unit.installers.License")
