import flet as ft

class MainApp:
    def main(self, page: ft.Page):
        page.expand = True
        page.padding = 0
        page.vertical_alignment = "center"
        page.horizontal_alignment = "center"
        page.theme_mode = ft.ThemeMode.SYSTEM
        page.window.min_width = 1400
        page.window.min_height = 800
        page.window.maximized = True
        # Puedes añadir más elementos a la página aquí
        page.update()

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





