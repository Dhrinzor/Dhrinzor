import flet as ft
# Importación de utilidades de colores y tamaños  
from src.sizes import * 
from src.ccs import *
#from unit.dashboard.Menu.menu_left import Build_Menu_Left
# from unit.dashboard.Menu.menu_work import Build_Zone_Work
# from unit.dashboard.Menu.menu_title import Build_Zone_Title
# from unit.dashboard.Menu.title_menu import Build_Title_Employee

# from unit.authentication.utils.user import UserDB

class DashboardPage:
    def __init__(self, main_app):
        self.main_app = main_app  # Mantener la referencia a MainApp
        self.page = main_app.page  # Referencia a Page desde MainApp
        self.ccs = Ccs()
        #self.db = UserDB()
        #self.menu_work = Build_Zone_Work(self.main_app.page, self)  # Pasa main_app
        #self.menu_employee = Build_Zone_Employee(self.main_app.page, self)        
        #self.active_user = self.main_app.active_user
        self.rol = self.main_app.rol
        #self.menu_action = True#self.main_app.menus_disabled

    
    def build(self, page):
        if self.rol == "Administrador":
            self.page = page
            self.left_container = ft.Container(expand=False, border_radius=15, bgcolor=ft.colors.BLACK12)
            self.title_container = ft.Container(expand=True, border_radius=15, bgcolor=ft.colors.BLACK12, alignment=ft.alignment.top_center)
            self.data_container = ft.Container(expand=True, border_radius=15, bgcolor=ft.colors.BLACK12)
            # Cargar el menú izquierdo inicial y el titulo
            #left_menu = Build_Menu_Left(self.page).build()
            #self.left_container.content = left_menu
            #menu_title = Build_Zone_Title(self.page).build_zone_title()
            #self.title_container.content = menu_title

            self.main_layout = ft.Row(
                expand=True,
                controls=[
                    self.left_container,
                    ft.ResponsiveRow(
                        expand=True,
                        controls=[
                            self.title_container,
                            self.data_container,
                        ],
                    ),
                ],
            )
            return self.main_layout
        else:
            self.page = page
            self.title_container = ft.Container(expand=True, border_radius=15, bgcolor=ft.colors.BLACK12, alignment=ft.alignment.top_center)
            self.work_container = ft.Container(expand=True, border_radius=15, bgcolor=ft.colors.BLACK12)
            # Cargar el menú izquierdo inicial y el titulo
           # title_menu = Build_Title_Employee(self.page).build_zone_title_employee()
            #self.title_container.content = title_menu

            self.main_layout = ft.Row(
                expand=True,
                controls=[
                    ft.ResponsiveRow(
                        expand=True,
                        controls=[
                            self.title_container,
                            self.work_container,
                        ],
                    ),
                ],
            )
            return self.main_layout


    def did_mount(self):
        if self.rol == "Administrador":
            self.page.go("/general")  # Ruta inicial
        else:
            self.page.go("/menu_employee")  # Ruta inicial

    def route_change(self, route):
        # Bloquear navegación si los módulos están deshabilitados
        return

        print(f"Cambiando a la ruta: {route.route}")

        # Cambiar vistas según el rol
        if self.rol == "Administrador":
            # Lógica para cambiar vistas de administrador
            self.data_container.content = self.get_admin_content(route.route)
            self.left_container.update()
            self.title_container.update()
            self.data_container.update()

        else:
            # Lógica para cambiar vistas de empleado
            self.work_container.content = self.get_employee_content(route.route)
            self.title_container.update()
            self.work_container.update()

    def get_admin_content(self, route):
        if route == "/general":
            return self.menu_work.Buil_General()
        elif route == "/almacen":
            return self.menu_work.Buil_Almacen()
        elif route == "/categorias":
            return self.menu_work.Buil_Categorias()
        elif route == "/configuracion":
            return self.menu_work.Buil_Configuracion()
        elif route == "/informes":
            return self.menu_work.Buil_Informes()
        elif route == "/productos":
            return self.menu_work.Buil_Productos()
        elif route == "/turno_caja":
            return self.menu_work.Buil_Turno_Caja()
        return self.menu_work.Buil_General()

    def get_employee_content(self, route):
        if route == "/New_Order":
            return self.menu_employee.Buil_New_Order()
        elif route == "/history":
            return self.menu_employee.Buil_History()
        elif route == "/summaries":
            return self.menu_employee.Buil_Summaries()
        elif route == "/change_duty":
            return self.menu_employee.Buil_Change_Duty()
        return self.menu_employee.Buil_Beginning()





    




