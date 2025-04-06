import flet as ft
from pages.dashboard.Menu.Containers.general import Build_Zone_General
from pages.dashboard.Menu.Containers.almacen import Build_Zone_Almacen
from pages.dashboard.Menu.Containers.categorias import Build_Zone_Categorias
from pages.dashboard.Menu.Containers.configuracion import Build_Zone_Configuracion
from pages.dashboard.Menu.Containers.informes import Build_Zone_Informes
from pages.dashboard.Menu.Containers.inventario import Build_Zone_Inventario
from pages.dashboard.Menu.Containers.productos import Build_Zone_Productos
from pages.dashboard.Menu.Containers.turno_caja import Build_Zone_Turno_Caja
from pages.authentication.utils.ccs import *

class Build_Zone_Work(ft.Control):
    def __init__(self, page, dashboard):
        super().__init__()
        self.page = page
        self.dashboard = dashboard  # Referencia a DashboardPage
        self.ccs = Ccs()
        self.menu_general = Build_Zone_General(self)
        self.menu_almacen = Build_Zone_Almacen(self.page)
        self.menu_categorias = Build_Zone_Categorias(self.page)
        self.menu_configuracion = Build_Zone_Configuracion(self.page)
        self.menu_informes = Build_Zone_Informes(self.page)
        self.menu_inventario = Build_Zone_Inventario(self.page)
        self.menu_productos = Build_Zone_Productos(self.page)
        self.menu_turno_caja = Build_Zone_Turno_Caja(self.page)

    ###### GENERAL ###########################
    def Buil_General(self):
        data_general = ft.Container(
            content=self.menu_general.build_zone_general(),
            border_radius=15,
            expand=True,
        )
        return ft.Row(expand=True, controls=[data_general])

    ###### ALMACEN ###########################
    def Buil_Almacen(self):
        data_almacen = ft.Container(
            content=self.menu_almacen.build_zone_almacen(),
            expand=True
        )
        return ft.Row(expand=True, controls=[data_almacen])

    ###### CATEGORIAS ###########################
    def Buil_Categorias(self):
        data_categorias = ft.Container(
            content=self.menu_categorias.build_zone_Categorias(),
            expand=True
        )
        return ft.Row(expand=True, controls=[data_categorias])

    ###### CONFIGURACION ###########################
    def Buil_Configuracion(self):
        data_configuracion = ft.Container(
            content=self.menu_configuracion.build_zone_configuracion(),
            expand=True
        )
        return ft.Row(expand=True, controls=[data_configuracion])

    ###### INFORMES ###########################
    def Buil_Informes(self):
        data_informes = ft.Container(
            content=self.menu_informes.build_zone_informes(),
            expand=True
        )
        return ft.Row(expand=True, controls=[data_informes])

    ###### INVENTARIO ###########################
    def Buil_Inventarios(self):
        # Construir el contenedor
        container = self.menu_inventario.build_zone_inventario()

        # Crear el contenedor para la fila
        data_inventarios = ft.Container(
            content=container,
            expand=True
        )

        # Crear la fila que contendrá el contenedor
        row = ft.Row(expand=True, controls=[data_inventarios])

        # Devolver la fila, sin actualizar inmediatamente para evitar superposición de páginas
        return row

    def on_load_inventarios(self):
        # Llamar al método update_table después de que el contenedor se haya agregado a la página
        self.menu_inventario.update_table(self.menu_inventario.first_entity_id)

    ###### PRODUCTOS ###########################
    def Buil_Productos(self):
        data_productos = ft.Container(
            content=self.menu_productos.build_zone_productos(),
            expand=True
        )
        return ft.Row(expand=True, controls=[data_productos])

    ###### TURNO_CAJA ###########################
    def Buil_Turno_Caja(self):
        data_turno_caja = ft.Container(
            content=self.menu_turno_caja.build_zone_turno_caja(),
            expand=True
        )
        return ft.Row(expand=True, controls=[data_turno_caja])
