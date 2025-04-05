import flet as ft

class LoginPage:
    def __init__(self, page: ft.Page):
        self.page = page

    def show(self):
        self.page.title = "Login - The Magic Card"
        self.page.horizontal_alignment = "center"
        self.page.vertical_alignment = "center"

        self.page.add(
            ft.Column(
                controls=[
                    ft.Text("Inicio de sesión", size=24, weight="bold"),
                    ft.TextField(label="Usuario", width=300),
                    ft.TextField(label="Contraseña", password=True, width=300),
                    ft.ElevatedButton(
                        text="Iniciar Sesión",
                        bgcolor=ft.Colors.BLUE,
                        color="white",
                        on_click=self._login,
                    ),
                ],
                alignment="center",
                spacing=20,
            )
        )

    def _login(self, event):
        # Lógica de inicio de sesión (simulada)
        print("Iniciando sesión...")
        self.page.update()