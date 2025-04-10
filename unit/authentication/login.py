import flet as ft
import threading
import time
#from DB.user import UserDB
#from unit.dashboard.dashboard import DashboardPage  # Importar DashboardPage

# Importación de utilidades de colores y tamaños  
from src.sizes import * 
from src.ccs import *
##############FIN DE LAS DEPENDENCIAS################  


class LoginPage(ft.Control):  
    def __init__(self, main_app):  
        super().__init__()  
        self.main_app = main_app  
        #self.dbuser = UserDB()
        self.list_alerts = {
            "ALpassword": "¡Error! Usuario o contraseña incorrecta.",
            "ALvacios": "¡Error! Existen campos vacíos.",
            "ALexito": "¡Registro exitoso!"
        }

    def build(self):  
        self.Eusuario = ft.TextField(label="Usuario", width=ancho, height=alto, color=ft.colors.CYAN_ACCENT, prefix_icon=ft.icons.EMAIL)  
        self.Econtraseña = ft.TextField(label="Contraseña", width=ancho, height=alto, color=ft.colors.CYAN_ACCENT, prefix_icon=ft.icons.LOCK, password=True) 
        self.mostrar_contraseña = ft.Checkbox(label="Mostrar contraseña", check_color=ft.colors.PURPLE, on_change=self.password_visible_changed)
        self.bcrear_cuenta = ft.TextButton("Registrarse", icon=ft.icons.GROUP_ADD_ROUNDED, on_click=self.signup)
        self.blogin = ft.TextButton("INICIAR SESION", icon=ft.icons.LOGIN, on_click=self.login)
        self.LTitulo = ft.Text('Iniciar Sesion', width=alto_letra, size=size_letra, weight='w900', color=customTextColor, text_align='center')
        self.imagen = ft.Image(src='src/Image/PNG/DC.png', width=foto_size)
        
        return ft.Container(
            ft.Row(
                [
                    ft.Container(
                        ft.Column(
                            [
                                self.LTitulo,
                                ft.Container(self.Eusuario, padding=ft.padding.only(20, 10)),
                                ft.Container(self.Econtraseña, padding=ft.padding.only(20, 10)),
                                ft.Container(self.mostrar_contraseña, padding=ft.padding.only(20)),
                                ft.Container(self.blogin, padding=ft.padding.only(20, 10)),
                                ft.Container(
                                    ft.Row([ft.Text('No tiene una cuenta?'), self.bcrear_cuenta], spacing=8),
                                    padding=ft.padding.only(40)),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor=ft.colors.PURPLE,
                        expand=True,
                    ),
                    ft.Container(
                        ft.Column([
                            ft.Text("Bienvenido", size=40, font_family="Georgia"),
                            ft.Container(self.imagen, padding=ft.padding.only(5)),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor=ft.colors.BLUE_300,
                        expand=True,
                        border_radius=ft.BorderRadius(top_left=tope_izquierdo1, top_right=tope_derecho1, bottom_left=boton_izquierdo1, bottom_right=boton_derecho1)
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            alignment=ft.alignment.center,
            width=700,
            height=400,
            bgcolor=ft.colors.PURPLE,
            animate_opacity=300,
            border_radius=radio_border
        )

    def password_visible_changed(self, e):  
        self.Econtraseña.password = not self.Econtraseña.password
        self.Econtraseña.update()

    def login(self, e):
        if self.main_app.dbuser.login(self.Eusuario.value, self.Econtraseña.value):
            self.name = self.Eusuario.value
            self.show_loading_screen()

            threading.Thread(target=self.main_app.dbuser.insert_login_history, args=(self.name,)).start()
            
            self.check_user_role()  # Verificar el rol del usuario
        else:
            self.Eusuario.value = ""
            self.Econtraseña.value = ""
            self.show_alert_dialog("ALpassword")

    def show_loading_screen(self):
        self.main_app.page.dialog = ft.AlertDialog(
            modal=True,
            bgcolor=None,  # Fondo transparente para el diálogo
            content=ft.Container(
                ft.Column(
                    [
                        ft.ProgressRing(),
                        ft.Text("Actualizando Base de Datos", color=ft.colors.WHITE),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    tight=True,
                ),
                padding=2,
                bgcolor=None,  # Fondo transparente para el contenedor
            ),
        )
        self.main_app.page.dialog.open = True
        self.main_app.page.update()


    def check_user_role(self):
        # Simular un tiempo de espera para asegurarse de que los datos se hayan guardado en la base de datos
        time.sleep(0.01)  # Ajusta el tiempo según sea necesario
        self.main_app.page.dialog.open = False
        self.main_app.page.update()     
        self.main_app.active_user = self.main_app.dbuser.get_last_login_user()
        self.main_app.rol = self.main_app.dbuser.get_user_role(self.main_app.active_user)
        # Inicializa DashboardPage con los valores obtenidos
        #self.main_app.dashboard_page = DashboardPage(self.main_app)

        #self.main_app.navigate("dashboard")

    def show_alert_dialog(self, key):
        message = self.list_alerts[key]
        self.main_app.page.dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[ft.TextButton(text="OK", on_click=self.close_dialog)],
        )
        self.main_app.page.dialog.open = True
        self.main_app.page.update()

    def close_dialog(self, e):
        self.main_app.page.dialog.open = False
        self.main_app.page.update()

    def signup(self, e):
        self.main_app.navigate("signup")






