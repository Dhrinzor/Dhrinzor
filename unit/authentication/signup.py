import flet as ft
import string
import os
from src.sizes import *
from src.ccs import *
from DB.db_setup import UserDB  # Importar la gestión de la base de datos

# Importación de utilidades de colores y tamaños  
from src.sizes import * 
from src.ccs import *
##############FIN DE LAS DEPENDENCIAS################  

class SignupPage(ft.Control):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
         # Define la ruta del archivo de base de datos
        self.business_db_path = os.path.join("C:\\", "MagicCorp", "DB", "DB_{business_name}.db")
        self.dbuser = UserDB(self.business_db_path)  # Pasa la ruta de la base de datos como argumento
        # Define UI elements
        self.LTitulo = ft.Text('Registrarse', width=alto_letra, size=size_letra, weight='w900', color="white", text_align='center')
        self.imagen = ft.Image(src='src/Image/PNG/signup.png', width=foto_size)
        self.Enombre = ft.TextField(label="Nombre", width=ancho, height=alto, color=ft.colors.DEEP_PURPLE_ACCENT_200, prefix_icon=ft.icons.SUPERVISED_USER_CIRCLE_OUTLINED)
        self.Eusuario = ft.TextField(label="Usuario",  width=ancho, height=alto, color=ft.colors.DEEP_PURPLE_ACCENT_200, prefix_icon=ft.icons.SUPERVISOR_ACCOUNT_OUTLINED,on_focus=self.cambiar_color_rojo,error_style=ft.TextStyle(color=ft.colors.RED) ) # Asegúrate de que el `error_text` sea rojo)
        self.Econtraseña = ft.TextField(
            label="Contraseña", width=ancho, height=alto, color=ft.colors.DEEP_PURPLE_ACCENT_200, prefix_icon=ft.icons.LOCK, 
            can_reveal_password=True, password=True, on_focus=self.cambiar_color_rojo, on_blur=self.validar_contraseña, error_style=ft.TextStyle(color=ft.colors.RED)
        )
        self.Econfirm_password = ft.TextField(
            label="Confirmar contraseña", width=ancho, height=alto, color=ft.colors.DEEP_PURPLE_ACCENT_200, prefix_icon=ft.icons.LOCK, 
            can_reveal_password=True, password=True, on_focus=self.cambiar_color_rojo, on_blur=self.validar_confirmacion_contraseña, error_style=ft.TextStyle(color=ft.colors.RED)
        )
        self.EVpassword = ft.TextField(
            label="Contraseña autorizada", hover_color='#64B5F6', fill_color='#294382', focused_border_color="#9C27B0", 
            width=ancho, height=alto, color=ft.colors.DEEP_PURPLE_ACCENT_200, prefix_icon=ft.icons.LOCK_CLOCK_ROUNDED, 
            can_reveal_password=True, password=True, on_blur=self.validar_contraseña_autorizada, error_style=ft.TextStyle(color=ft.colors.RED)
        ) 
        # Buttons
        self.BRegistrar = ft.TextButton(
            content=ft.Row(controls=[ft.Icon(ft.icons.PERSON_ADD, color=ft.colors.PURPLE),
                    ft.Text("Registrar", font_family=diaria, size=diaria_size, color=ft.colors.PURPLE)]),  on_click=self.register
        )
        self.BInicio = ft.TextButton( content=ft.Row(
                    controls=[ft.Icon(ft.icons.LOGOUT, color=ft.colors.PURPLE),
                        ft.Text("Volver a inicio", font_family=diaria, size=diaria_size, color=ft.colors.PURPLE)]),on_click=self.login 
        )
    def cambiar_color_rojo(self, e):
        e.control.border_color = ft.colors.RED
        if self.page:
            self.main_app.page.update()

    def validar_contraseña(self, e):
        contraseña = self.Econtraseña.value
        if len(contraseña) <= 6:
            self.Econtraseña.error_text = "Contraseña debil: menor a 6 caracteres."
            self.Econtraseña.border_color = ft.colors.RED
        elif not any(char.isupper() for char in contraseña):
            self.Econtraseña.error_text = "Debe contener al menos una mayúscula."
            self.Econtraseña.border_color = ft.colors.RED
        elif not any(char in string.punctuation.replace("'", "").replace('"', '') for char in contraseña):
            self.Econtraseña.error_text = "Debe contener caracteres especiales."
            self.Econtraseña.border_color = ft.colors.RED
        else:
            self.Econtraseña.error_text = None
            self.Econtraseña.border_color = ft.colors.GREEN
        if self.page:
            self.main_app.page.update()

    def validar_confirmacion_contraseña(self, e):
        if self.Econtraseña.value != self.Econfirm_password.value:
            self.Econfirm_password.error_text = "¡Error! Contraseñas no coinciden."
            self.Econfirm_password.border_color = ft.colors.RED
        else:
            self.Econfirm_password.error_text = None
            self.Econfirm_password.border_color = ft.colors.GREEN
        if self.page:
            self.main_app.page.update()

    def validar_contraseña_autorizada(self, e):
        if not self.dbuser.password_exists(self.EVpassword.value):
            self.EVpassword.error_text = "¡Error! Contraseña autorizada no registrada."
            self.EVpassword.border_color = ft.colors.RED
        else:
            self.EVpassword.error_text = None
            self.EVpassword.border_color = ft.colors.GREEN
        if self.page:
            self.main_app.page.update()
               
    def build(self):
        return ft.Container(   
            ft.Row(
                [ft.Container( ft.Column([
                                self.LTitulo, 
                                ft.Container(self.imagen, padding=ft.padding.only(1, 5))],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor=ft.colors.PURPLE,
                        expand=True,
                        border_radius=ft.BorderRadius(top_left=tope_izquierdo, top_right=tope_derecho, bottom_left=boton_izquierdo, bottom_right=boton_derecho)
                    ),
                    ft.Container(
                        ft.Column(
                            [self.LTitulo,
                                ft.Container(self.Enombre, padding=ft.padding.only(5, 2)),
                                ft.Container(self.Eusuario, padding=ft.padding.only(5, 2)),
                                ft.Container(self.Econtraseña, padding=ft.padding.only(5, 2)),
                                ft.Container(self.Econfirm_password, padding=ft.padding.only(5, 2)),
                                ft.Container(self.EVpassword, padding=ft.padding.only(5)),
                                ft.Container(
                                    ft.Row([ft.Text('                    ', color=ft.colors.PURPLE),
                                            self.BRegistrar,], 
                                        spacing=8
                                    ), 
                                    padding=ft.padding.only(10)
                                ),
                                ft.Container(ft.Row([ft.Text('Ya tiene cuenta?', color=ft.colors.PURPLE, size=15),
                                            self.BInicio,], 
                                        spacing=8
                                    ), 
                                    padding=ft.padding.only(10)
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        bgcolor=ft.colors.BLUE_300,
                        expand=True
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            alignment=ft.alignment.center,
            width=700,
            height=400,
            bgcolor=ft.colors.BLUE_300,
            animate_opacity=300,
            border_radius=radio_border
        )

    def register(self, e):
        if self.dbuser.user_exists(self.Eusuario.value):
            self.Eusuario.error_text = "¡Error! El usuario ya existe."
            self.Eusuario.border_color = ft.colors.RED  # Cambia el color del borde a rojo
            self.main_app.page.update()
            return

        self.validar_contraseña(None)

        if self.Econtraseña.error_text:
            self.main_app.page.update()
            return

        self.validar_confirmacion_contraseña(None)

        if self.Econfirm_password.error_text:
            self.main_app.page.update()
            return

        if not self.dbuser.password_exists(self.EVpassword.value):
            self.EVpassword.error_text = "¡Error! Contraseña autorizada no registrada."
            self.EVpassword.border_color = ft.colors.RED
            self.main_app.page.update()
            return

        rol = "Administrador"
        self.dbuser.signup(self.Enombre.value, self.Eusuario.value, self.Econtraseña.value, rol)
        self.Enombre.value = ""
        self.Eusuario.value = ""
        self.Econtraseña.value = ""
        self.Econfirm_password.value = ""
        self.EVpassword.value = ""
        self.show_error_dialog("¡Registro exitoso!")
        self.main_app.navigate("login")

    def close_dialog(self, e):
        self.main_app.page.dialog.open = False
        self.main_app.page.update()

    def show_error_dialog(self, message):
        self.main_app.page.dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[
                ft.TextButton(text="OK", on_click=self.close_dialog),
            ],
        )
        self.main_app.page.dialog.open = True
        self.main_app.page.update()

    def login(self, e):
        self.Enombre.value = ""
        self.Eusuario.value = ""
        self.Econtraseña.value = ""
        self.Econfirm_password.value = ""
        self.EVpassword.value = ""
        self.Econtraseña.error_text = None
        self.Econfirm_password.error_text = None
        self.EVpassword.error_text = None
        self.Econtraseña.border_color = ft.colors.DEEP_PURPLE_ACCENT_200
        self.Econfirm_password.border_color = ft.colors.DEEP_PURPLE_ACCENT_200
        self.EVpassword.border_color = ft.colors.DEEP_PURPLE_ACCENT_200
        if self.page:
            self.main_app.page.update()
        self.main_app.navigate("login")

