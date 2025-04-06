import flet as ft
from pages.authentication.utils.ccs import *
from pages.dashboard.Menu.Containers.data_hub import InventoryDB  # Asegúrate de importar tu clase de base de datos

class Build_Zone_Productos(ft.Control):
    def __init__(self, page):
        super().__init__()
        self.page = page 
        self.db = InventoryDB()  # Crear una instancia de tu clase de base de datos
    
    def build_zone_productos(self):
        # Obtener productos existentes de la base de datos
        products = self.db.get_all_productos_existentes()

        # Crear filas para la tabla
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Container(content=ft.Text(product["producto"]), width=250)),
                    ft.DataCell(ft.Container(content=ft.Text(str(product["precio_costo"])), width=150)),
                    ft.DataCell(ft.Container(content=ft.Text(str(product["cantidad"])), width=100)),
                ],
            ) for product in products
        ]

        # Crear la tabla de productos sin encabezado
        product_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Producto")),
                ft.DataColumn(ft.Text("Precio Costo")),
                ft.DataColumn(ft.Text("Cantidad")),
            ],
            rows=rows,
            heading_row_height=0  # Ocultar la fila de encabezado
        )

        # Crear el encabezado
        table_header = ft.Row(
            controls=[
                ft.Container(ft.Text("      Producto"), width=310),
                ft.Container(ft.Text("   Precio Costo"), width=180),
                ft.Container(ft.Text("   Cantidad"), width=100),
            ],
            spacing=10,
        )

        # Crear un contenedor con scroll solo para los datos de la tabla
        scrollable_table_container = ft.Container(
            content=ft.Column(
                controls=[product_table],
                scroll=ft.ScrollMode.ALWAYS,  # Habilitar el desplazamiento
                expand=True,
            ),
            height=600,  # Ajustar la altura del contenedor
            width=900,   # Ajustar el ancho del contenedor si es necesario
            border_radius=15,
            padding=ft.padding.all(10)
        )

        # Crear el contenedor principal con encabezado fijo y tabla desplazable
        main_container = ft.Container(
            expand=True,
            bgcolor=ft.colors.WHITE10,
            padding=ft.padding.only(left=30, top=80, bottom=30, right=580),
            border_radius=15,
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                table_header,
                                scrollable_table_container
                            ],
                        ),
                        expand=True,
                        height=630,
                        bgcolor=ft.colors.BLACK12,
                        padding=ft.padding.all(10),
                        border_radius=15,
                    )
                ]
            )
        )

        # Devolver el contenedor principal
        return main_container

