import subprocess
import os
import flet as ft
import importlib
from unit.authentication.login import LoginPage  # Asegúrate de que el path sea correcto
from unit.authentication.signup import SignupPage  # Asegúrate de que el path sea correcto

class MainApp:
    def __init__(self):
        # Propiedades Globales
        self.page = None
        self.login_page = LoginPage(self)
        self.signup_page = SignupPage(self)
        self.magiccorp_path = r"C:\MagicCorp"  # Ruta principal
        self.required_files = [  # Archivos necesarios
            "key.txt",
            "license.txt",
            "sync_version.bat",
            "version.txt",
            "test.txt",
            "README.md",
            "install.nsi",
            "requirements.txt"
        ]
        self.required_folders = [  # Carpetas necesarias
            "DB",
            "src"
        ]

    def main(self, page: ft.Page):
        # Configuración inicial de la ventana
        self.page = page
        self.page.title = "MagicCorp Software"
        self.page.expand = True
        self.page.padding = 0
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.theme_mode = ft.ThemeMode.SYSTEM

        # Configuración de dimensiones de la ventana
        self.page.window.maximized = True  # Maximizar ventana al inicio

        # Verificar si los archivos y carpetas necesarios existen
        if self._verify_magiccorp_contents():
            print("Todos los archivos y carpetas necesarios existen. Cargando la ventana de inicio...")
            self.page.add(self.login_page.build())  # Carga la página de login
        else:
            print("Archivos o carpetas faltantes. Redirigiendo a la instalación...")
            self._load_installation_page()  # Navegar a la página de instalación

        self.page.update()

    def _verify_magiccorp_contents(self):
        """Verifica que los archivos y carpetas requeridos estén presentes en la ruta."""
        # Verificar carpeta principal
        if not os.path.exists(self.magiccorp_path):
            print(f"No se encontró la carpeta principal en {self.magiccorp_path}.")
            return False

        # Verificar archivos requeridos
        for file in self.required_files:
            file_path = os.path.join(self.magiccorp_path, file)
            if not os.path.exists(file_path):
                print(f"Archivo faltante: {file}")
                return False

        # Verificar carpetas requeridas
        for folder in self.required_folders:
            folder_path = os.path.join(self.magiccorp_path, folder)
            if not os.path.exists(folder_path):
                print(f"Carpeta faltante: {folder}")
                return False

        # Si todo está presente
        print("Todos los archivos y carpetas requeridos existen.")
        return True

    def _load_installation_page(self):
        """Carga la página de instalación si faltan archivos o carpetas."""
        try:
            print("Mostrando la página de instalación...")
            install_module = importlib.import_module("unit.install")  # Cargar módulo de instalación dinámicamente
            install_module.InstallPage(self.page, self).show()  # Mostrar la página de instalación
        except Exception as e:
            print(f"Error al cargar la página de instalación: {e}")

    def navigate(self, page_name):
        """Navegación entre páginas."""
        self.page.controls.clear()

        # Cargar la página correspondiente
        if page_name == "login":
            self.page.add(self.login_page.build())
        elif page_name == "signup":
            self.page.add(self.signup_page.build())
        else:
            print(f"Página desconocida: {page_name}")

        self.page.update()


if __name__ == "__main__":
    app = MainApp()
    ft.app(target=app.main)
    
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





