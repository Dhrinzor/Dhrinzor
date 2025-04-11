import os
import flet as ft
from unit.globals.recursivo import Utils  # Importar la clase Utils
from DB.db_setup import UserDB  # Importar la clase UserDB
class PageContent:
    def __init__(self, page, navigate_to, app):
        self.page = page
        self.navigate_to = navigate_to
        self.app = app  # Referencia al objeto principal (TheMagicCardApp o InstallPage)
        self.modo = None  # Variable para almacenar el tipo de instalación

    def _finalize(self, event):
        utils = Utils()  # Crear instancia de Utils

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

        # Buscar el tipo de instalación usando Utils.buscar_parametro
        try:
            self.modo = utils.buscar_parametro("key.txt", "Tipo de instalación")
            if not self.modo:
                raise ValueError("El archivo 'key.txt' no contiene un tipo de instalación válido.")
            print(f"Tipo de instalación leído: {self.modo}")
        except Exception as e:
            print(f"Error al obtener el tipo de instalación: {str(e)}")
            self.modo = "Error"

        # Obtener la ruta de la base de datos existente desde `install_tools.py`
        db_dest_path = r"C:\MagicCorp\DB"
        existing_db_path = os.path.join(db_dest_path, f"DB_{utils.buscar_parametro('key.txt', 'Negocio')}.db")  # Usar nombre de la base creada en install_tools.py

        try:
            user_db = UserDB(existing_db_path)  # Reutilizar la base de datos existente
            user_db.create_user_tables(self.modo)  # Crear tablas según el tipo de instalación
            print(f"Tablas de usuario creadas exitosamente en la base de datos: {existing_db_path}")
        except Exception as e:
            print(f"Error al crear las tablas de usuario: {str(e)}")

        # Tomar acción según el tipo de instalación
        if self.modo == "Negocio":
            print("Redirigiendo a la página de inicio de sesión...")
            self.app.navigate("login")  # Navegar al login usando el método principal
        else:
            print(f"No se realizará ninguna acción para el modo: {self.modo}")

        # Mensaje final dinámico
        finalize_button.text = "Completado"
        finalize_button.disabled = True
        final_message.value = "¡Instalación completada con éxito! Gracias por confiar en MagicCorp."
        self.page.update()
    
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
            icon=ft.icons.CHECK,
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