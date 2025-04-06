import flet as ft

class PageContent:
    def __init__(self, page, navigate_to, app):
        self.page = page
        self.navigate_to = navigate_to
        self.app = app  # Referencia a la instancia de InstallPage

        # Leer la versión desde version.txt
        try:
            with open("version.txt", "r") as file:
                self.version = file.read().strip()  # Leer y eliminar espacios adicionales
        except FileNotFoundError:
            self.version = "Versión desconocida"  # Manejar error si no se encuentra el archivo

    def show(self):
        return ft.Container(
            bgcolor=ft.colors.WHITE10,
            expand=True,
            padding=ft.padding.only(left=30, top=80, bottom=72, right=30),
            border_radius=15,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Bienvenido", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text("Acerca de la Aplicación", size=20, weight=ft.FontWeight.BOLD),
                                        ft.Row(
                                            controls=[
                                                ft.Text(f"Versión: {self.version}", size=15, weight=ft.FontWeight.BOLD),
                                                ft.PopupMenuButton(
                                                    content=ft.Text("Opciones", size=15, weight=ft.FontWeight.BOLD),
                                                    items=[
                                                        ft.PopupMenuItem(text="Soporte Técnico", icon=ft.icons.HELP),
                                                        ft.PopupMenuItem(text="Política de Privacidad", icon=ft.icons.PRIVACY_TIP),
                                                        ft.PopupMenuItem(text="Términos de Servicio", icon=ft.icons.DESCRIPTION),
                                                    ]
                                                ),
                                            ],
                                            spacing=10
                                        )
                                    ]
                                ),
                                margin=ft.margin.only(left=100)
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Divider(height=20, thickness=1),
                    ft.Text("Gestión de Usuarios", size=20, weight=ft.FontWeight.BOLD),
                    ft.TextButton("Añadir Usuario", icon=ft.icons.PERSON_ADD),
                    ft.TextButton("Editar Usuario", icon=ft.icons.EDIT),
                    ft.Divider(height=20, thickness=1),
                ]
            )
        )

    def actualizar_checkboxes(self, e):
        # Llamar al método de actualización de la página principal
        self.app.actualizar_checkboxes()
        # Navegar a la página username.py
        self.navigate_to("unit.installers.Username")