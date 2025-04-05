import flet as ft

class PageContent:
    def __init__(self, page, navigate_to, app):
        self.page = page
        self.navigate_to = navigate_to

    def show(self):
        return ft.Column(
            controls=[
                ft.Text("Preferencias de Instalación", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Último paso antes de la instalación.", size=16),
                ft.ElevatedButton(
                    text="Instalar",
                    on_click=self._install,
                ),
            ],
            alignment="center",
            spacing=20,
        )

    def _install(self, event):
        print("Instalación completada.")