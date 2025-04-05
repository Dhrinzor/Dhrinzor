import flet as ft

class PageContent:
    def __init__(self, page, navigate_to, app):
        self.page = page
        self.navigate_to = navigate_to

    def show(self):
        return ft.Column(
            controls=[
                ft.Text("Registrar Usuario", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Por favor, ingrese su información de usuario.", size=16),
                ft.ElevatedButton(
                    text="Continuar",
                    on_click=lambda _: self.navigate_to("unit.installers.Install_tools"),
                ),
            ],
            alignment="center",
            spacing=20,
        )