import os
import time
import flet as ft

class PageContent:
    def __init__(self, page, navigate_to, app):
        self.page = page
        self.navigate_to = navigate_to
        self.app = app  # Referencia al objeto principal (TheMagicCardApp o InstallPage)

    def _finalize(self, event):
        # Revisar si se seleccionó "Crear acceso directo"
        if create_shortcut_checkbox.value:
            print("Creando acceso directo en el escritorio...")
            desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            shortcut_path = os.path.join(desktop_path, "MagicCorp.lnk")
            try:
                if not os.path.exists(desktop_path):
                    raise FileNotFoundError("El escritorio no está disponible. Usando la carpeta raíz como alternativa.")
                with open(shortcut_path, "w") as shortcut:
                    shortcut.write("[Acceso directo a MagicCorp]\n")
                    shortcut.write("Este acceso directo está simulado en el escritorio.")
                print(f"Acceso directo creado en: {shortcut_path}")
            except Exception as e:
                print(f"Error al crear el acceso directo: {str(e)}")
        else:
            print("El usuario decidió no crear el acceso directo.")

        # Mensaje final dinámico
        finalize_button.text = "Completado"
        finalize_button.disabled = True
        final_message.value = "¡Instalación completada con éxito! Gracias por confiar en MagicCorp."
        self.page.update()

        # Cargar la página de inicio de sesión
        print("Redirigiendo a la página de inicio de sesión...")
        self.app.navigate("login")  # Navegar al login usando el método principal

    def show(self):
        global finalize_button, create_shortcut_checkbox, final_message

        # Checkbox para crear acceso directo
        create_shortcut_checkbox = ft.Checkbox(
            label="Crear un acceso directo en el escritorio",
            value=False,
            fill_color=ft.colors.BLUE,
        )

        # Mensaje final dinámico
        final_message = ft.Text(value="", size=16, color=ft.colors.GREEN)

        # Botón para finalizar
        finalize_button = ft.ElevatedButton(
            text="Finalizar",
            on_click=self._finalize,
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE,
            icon=ft.icons.CHECK,  # Icono profesional
        )

        # Estructura de la página
        return ft.Container(
            bgcolor=ft.colors.WHITE,
            expand=True,
            padding=ft.padding.all(20),
            content=ft.Column(
                controls=[
                    ft.Text("Preferencias de Instalación", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE),
                    ft.Text("Último paso antes de completar la instalación.", size=16, text_align=ft.TextAlign.CENTER),
                    create_shortcut_checkbox,  # Checkbox para acceso directo
                    finalize_button,  # Botón para finalizar
                    final_message,  # Mensaje final dinámico
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
        )