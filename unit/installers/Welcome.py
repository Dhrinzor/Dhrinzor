import flet as ft

class PageContent:
    def __init__(self, page, navigate_to, app):
        self.page = page
        self.navigate_to = navigate_to
        self.app = app  # Referencia a la instancia de InstallPage

    def show(self):
        # Contenedor principal con el diseño requerido
        return ft.Container(
            bgcolor=ft.colors.WHITE,
            expand=True,
            content=ft.Column(
                controls=[
                    # Contenedor azul para el título "Bienvenido", expandido solo horizontalmente
                    ft.Container(
                        bgcolor=ft.colors.BLUE,
                        width=800,  # Ancho definido para expandir hacia los laterales
                        padding=ft.padding.all(30),
                        content=ft.Column(
                            controls=[
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
                            ]
                        ),
                    ),
                    # Contenedor para el texto de bienvenida
                    ft.Container(
                        content=ft.Column(
                            controls=[
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
                                ft.Divider(thickness=1, color=ft.colors.GREY),  # Divider al final del texto
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.all(20),
                    ),
                    # Botón "Comenzar" alineado en la parte inferior derecha
                    ft.Container(
                        content=ft.ElevatedButton(
                            text="Comenzar",
                            on_click=self._handle_start_button,
                        ),
                        alignment=ft.alignment.bottom_right,
                        margin=ft.margin.only(top=10),
                    ),
                ],
            ),
        )

    def _handle_start_button(self, e):
        print("Botón 'Comenzar' presionado.")  # Confirmar que el clic del botón es registrado.

        # Depurar la referencia al checkbox
        try:
            print("Intentando seleccionar el checkbox 'checkbox_instalar'...")
            if hasattr(self.app, "checkbox_instalar"):
                self.app.checkbox_instalar.value = True  # Marca el checkbox como seleccionado
                print("Checkbox seleccionado correctamente.")
            else:
                print("Error: 'checkbox_instalar' no está definido en 'self.app'.")
        except Exception as err:
            print(f"Error al intentar seleccionar el checkbox: {err}")

        # Actualizar la página para reflejar los cambios visuales
        try:
            print("Actualizando la página para reflejar los cambios...")
            self.app.page.update()
            print("Página actualizada correctamente.")
        except Exception as err:
            print(f"Error al actualizar la página: {err}")

        # Depurar la navegación a License.py
        try:
            print("Intentando navegar a 'License.py'...")
            self.navigate_to("unit.installers.License")
            print("Navegación exitosa.")
        except Exception as err:
            print(f"Error al intentar navegar: {err}")