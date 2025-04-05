import flet as ft

class PageContent:
    def __init__(self, page, navigate_to, app):
        self.page = page
        self.navigate_to = navigate_to

    def show(self):
        return ft.Column(
            controls=[
                ft.Text("Instalar Herramientas", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("A continuación, procederemos con la instalación de herramientas.", size=16),
                ft.ElevatedButton(
                    text="Continuar",
                    on_click=lambda _: self.navigate_to("unit.installers.Performance"),
                ),
            ],
            alignment="center",
            spacing=20,
        )