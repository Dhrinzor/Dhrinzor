import subprocess
import os
import flet as ft
import importlib
from unit.authentication.login import LoginPage  # Asegúrate de que el path sea correcto

class TheMagicCardApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.installation_path = r"C:\Program Files (x86)\The Magic Card"  # Ruta de instalación
        self.magiccorp_path = r"C:\MagicCorp"  # Ruta de la carpeta MagicCorp
        self.login_page = LoginPage(self)  # Instanciamos LoginPage al inicializar el programa

        # Configuración de la ventana
        self.page.expand = True
        self.page.padding = 0
        self.page.vertical_alignment = "center"
        self.page.horizontal_alignment = "center"
        self.page.theme_mode = ft.ThemeMode.SYSTEM
        self.page.window.maximized = True  # Maximiza la ventana al iniciarse
        self.page.update()  # Aplica los cambios de la configuración

    def run(self):
        # Ejecutar la sincronización en segundo plano
        self._sync_repository()

        # Verificar si la carpeta MagicCorp existe
        if os.path.exists(self.magiccorp_path):
            print(f"La carpeta '{self.magiccorp_path}' ya existe. Cargando la ventana de login...")
            self.navigate("login")
        else:
            print(f"La carpeta '{self.magiccorp_path}' no existe. Cargando la página de instalación...")
            self._load_installation_page()

    def _sync_repository(self):
        # Ruta del archivo .bat
        bat_file_path = os.path.join(os.getcwd(), "sync_version.bat")
        if os.path.exists(bat_file_path):
            try:
                # Ejecutar el archivo .bat en segundo plano
                subprocess.Popen(bat_file_path, shell=True)
                print("Sincronización con GitHub iniciada en segundo plano.")
            except Exception as e:
                print(f"Error al ejecutar el archivo .bat: {e}")
        else:
            print(f"El archivo {bat_file_path} no existe.")

    def _load_installation_page(self):
        # Método privado para cargar el módulo de instalación
        install_module = importlib.import_module("unit.install")
        install_module.InstallPage(self.page, self).show()  # Pasamos `self` como referencia al objeto principal

    def navigate(self, page_name):
        # Limpiar los controles actuales de la página
        self.page.controls.clear()

        # Navegación según el nombre de la página
        if page_name == "login":
            self.page.add(self.login_page.build())  # Agrega la estructura de LoginPage
        elif page_name == "signup":
            print("Navegando a la página de registro (signup)")
        elif page_name == "dashboard":
            print("Navegando al dashboard")
        else:
            print(f"Página desconocida: {page_name}")
        
        # Actualizar la página con los nuevos controles
        self.page.update()

    def close_application(self):
        print("Cerrando la aplicación...")
        os._exit(0)  # Salida inmediata del programa


def main(page: ft.Page):
    app = TheMagicCardApp(page)
    app.run()  # Ejecuta la aplicación principal


if __name__ == "__main__":
    ft.app(target=main)
    
# import flet as ft
# import shutil
# import os
# from pages.authentication.utils.ccs import Ccs
# from pages.dashboard.dashboard import DashboardPage
# from pages.authentication.login import LoginPage
# from pages.authentication.signup import SignupPage
# from pages.authentication.utils.user import UserDB

# class MainApp:
#     def __init__(self):
        
#         # self.dbuser = UserDB()
#         # self.signup_page = SignupPage(self)
#         # self.login_page = LoginPage(self)
#         # self.dashboard_page = None  # Inicializar después de que page esté disponible
#         # #self.ccs = Ccs()
#         # self.active_user = None
#         self.rol = None
#         # # Estado global para controlar el bloqueo de módulos
#         # self.menus_disabled  = False
#     # def bloquear_modulos(self):
#     #     self.menus_disabled = True
#     #     print("Módulos bloqueados globalmente.")

#     # def desbloquear_modulos(self):
#     #     self.menus_disabled = False
#     #     print("Módulos desbloqueados globalmente.")
        
              
#     def main(self, page: ft.Page):
#         self.page = page
#         #version = self.leer_version_desde_archivo()
#         self.page.expand = True
#         #self.page.title = f"The Magic Card {version}"
#         self.page.padding = 0
#         self.page.vertical_alignment = "center"
#         self.page.horizontal_alignment = "center"
#         self.page.theme_mode = ft.ThemeMode.SYSTEM
#         self.page.window.min_width = 1400
#         self.page.window.min_height = 800
#         self.page.window.maximized = True
#     #     with open("output.txt", "w") as file:
#     #         file.write("oscuro")
#     #     self.page.add(self.login_page.build())
#     #     self.page.update()

#     #     # Inicializar después de que page esté disponible
#     #     #self.dashboard_page = DashboardPage(self)

#     # def leer_version_desde_archivo(self):
#     #     try:
#     #         with open("key.txt", "r") as file:
#     #             for line in file:
#     #                 if "Version:" in line:
#     #                     return line.split(":")[1].strip()
#     #     except FileNotFoundError:
#     #         return "Unknown"  # Devolver una versión por defecto si el archivo no se encuentra
        
#     # def navigate(self, page_name):
#     #     # Bloquear navegación si los menús están deshabilitados
#     #     if self.menus_disabled:
#     #         print(f"No se puede navegar a {page_name}. Los módulos están bloqueados.")
#     #         return

#     #     # Continuar con la navegación
#     #     self.page.controls.clear()
#     #     if page_name == "login":
#     #         self.page.add(self.login_page.build())
#     #     elif page_name == "signup":
#     #         self.page.add(self.signup_page.build())
#     #     elif page_name == "dashboard":
#     #         self.page.on_route_change = self.dashboard_page.route_change
#     #         self.page.add(self.dashboard_page.build(self.page))
#     #         self.dashboard_page.did_mount()
#     #     self.page.update()


# if __name__ == "__main__":
#     app = MainApp()
#     ft.app(target=app.main)





