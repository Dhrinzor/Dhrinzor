import flet as ft
from pages.authentication.utils.ccs import *
from pages.authentication.utils.user import UserDB
from datetime import datetime

class Build_Menu_Left(ft.Control):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.ccs = Ccs()
        self.db=UserDB()
        self.theme_switch = ft.Switch(label="Tema Oscuro",label_style=ft.TextStyle(color=ft.colors.BLUE_GREY if self.ccs.mode == "claro" else ft.colors.BLUE_ACCENT_100, font_family=self.ccs.alegrian, size=16), on_change=self.modify_file, value=(self.ccs.mode == "oscuro"))
        self.imagen=ft.Image( src='src/Image/PNG/DC.png',width=200)
    
    def get_last_login_user(self): 
        return self.db.get_last_login_user() or "Usuario"
    
    def modify_file(self, e):
        self.ccs.toggle_mode()
        self.page.theme_mode = 'light' if self.ccs.mode == "claro" else 'oscuro'
        if self.ccs.mode == "claro":
            self.theme_switch.label = "Tema Claro"
            self.theme_switch.label_style = ft.TextStyle(
                color=ft.colors.BLUE_GREY,  # Color del texto para el modo claro
                font_family=self.ccs.alegrian,  # Cambia la fuente según tu preferencia
                size=16  # Tamaño del texto
            )
        else:
            self.theme_switch.label = "Tema Oscuro"
            self.theme_switch.label_style = ft.TextStyle(
                color=ft.colors.BLUE_ACCENT_100,  # Color del texto para el modo claro
                font_family=self.ccs.alegrian,  # Cambia la fuente según tu preferencia
                size=16  # Tamaño del texto
            )
        self.page.update()

    def build(self):      
        self.current_time = ft.Text(value=datetime.now().strftime("%d-%m-%Y"), style="headlineLarge")
        
        self.BGeneral       =   ft.TextButton(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.WIDGETS_OUTLINED ),
                                            ft.Text("General", font_family=self.ccs.diaria, size=self.ccs.diaria_size )
                                        ],
                                    ), 
            on_click=lambda e:  self.page.go("/general")
        )
        self.BTurno_Caja    =   ft.TextButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.BUSINESS_CENTER_OUTLINED, ),
                    ft.Text("Turno Caja", font_family=self.ccs.diaria, size=self.ccs.diaria_size )
                ],
            ), 
            on_click=lambda e: self.page.go("/turno_caja")
        )
        self.BInformes      =   ft.TextButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.ASSIGNMENT_OUTLINED, ),
                    ft.Text("Informes", font_family=self.ccs.diaria, size=self.ccs.diaria_size, )
                ],
            ), 
            on_click=lambda e: self.page.go("/informes")
        )
        self.BCategorias    =   ft.TextButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.CATEGORY_OUTLINED, ),
                    ft.Text("Categorias", font_family=self.ccs.diaria, size=self.ccs.diaria_size, )
                ],
            ), 
            on_click=lambda e: self.page.go("/categorias")
        )
        self.BInventario    =   ft.TextButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.INVENTORY_OUTLINED, ),
                    ft.Text("Transferencias", font_family=self.ccs.diaria, size=self.ccs.diaria_size )
                ],
            ), 
            on_click=lambda e: self.page.go("/inventario")
        )
        self.BConfiguracion =   ft.TextButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.TUNE_OUTLINED, ),
                    ft.Text("Configuración", font_family=self.ccs.diaria, size=self.ccs.diaria_size )
                ],
            ), 
            on_click=lambda e: self.page.go("/configuracion")
        )
        self.BProductos     =   ft.TextButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.LOCAL_OFFER_OUTLINED, ),
                    ft.Text("Productos", font_family=self.ccs.diaria, size=self.ccs.diaria_size )
                ],
            ), 
            on_click=lambda e: self.page.go("/productos")
        )
        self.BAlmacen       =   ft.TextButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.WAREHOUSE_OUTLINED, ),
                    ft.Text("Almacen", font_family=self.ccs.diaria, size=self.ccs.diaria_size )
                ],
            ), 
            on_click=lambda e: self.page.go("/almacen")
        )
        self.name=self.get_last_login_user()

        return ft.Container(
            expand=True,# Ocupar todo el alto de la página
            padding=ft.padding.only(top=10, left=10, right=10),
            # opacity=0.8,
            bgcolor=ft.colors.WHITE10,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(
                                ft.icons.PERSON,
                                size=50,
                                
                            ),
                            ft.Text(value=self.name, font_family=self.ccs.diaria, size=self.ccs.hallowin_size )
                        ],
                        alignment=ft.alignment.center
                    ),
                    ft.Divider(
                        color="black",
                        height=0.5,
                        thickness=0.5
                    ),
                    ft.Container(self.BGeneral),
                    ft.Container(self.BTurno_Caja),
                    ft.Container(self.BInformes),
                    ft.Divider(
                        color="black",
                        height=1,
                        thickness=1
                    ),
                    ft.Container(self.BCategorias),
                    ft.Container(self.BProductos),
                    ft.Container(self.BInventario),
                    ft.Container(self.BAlmacen),
                    ft.Divider(
                        color="black",
                        height=0.5,
                        thickness=0.5
                    ),
                    ft.Container(self.BConfiguracion),
                    ft.Container(self.current_time,expand=False, alignment=ft.alignment.center, padding=ft.padding.only(left=10,top=10,bottom=10,right=10)),  # Añadir el reloj debajo de Configuración
                    ft.Container(self.theme_switch,
                    ),
                    ft.Container( self.imagen),
                ],
            )
        )




