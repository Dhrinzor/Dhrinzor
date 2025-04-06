import flet as ft
from pages.authentication.utils.ccs import Ccs
from pages.dashboard.Menu.Containers.data_hub import InventoryDB
from pages.authentication.utils.user import UserDB
import threading

class Build_Zone_Beginning(ft.Control):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.ccs = Ccs()
        self.db = InventoryDB()  # Asegúrate de inicializar InventoryDB aquí
        self.db_user = UserDB()
        self.list_view = ft.ListView(
            controls=[],
            expand=True,
            auto_scroll=False,
        )
        self.transferencias_container = None
        self.almacen_container = None

    def build_zone_beginning(self):
        transferencias_container = self.load_transferencias_disponibles()
        almacen_container = self.load_almacen_datos()
        self.transferencias_container = transferencias_container
        self.almacen_container = almacen_container

        # Crear encabezado fijo
        header_row = ft.Row(
            controls=[
                ft.Container(ft.Text("     Producto"), width=250),
                ft.Container(ft.Text("Precio Costo"), width=120),
                ft.Container(ft.Text("Precio Venta"), width=130),
                ft.Container(ft.Text("Cantidad"), width=130),
                ft.Container(ft.Text("Fecha"), width=90),
                ft.Container(ft.Text("Disponible"), width=170),
                ft.Container(ft.Text("Aceptar"), width=70),
            ],
            spacing=10,
        )

        return ft.Container(
            expand=True,
            bgcolor=ft.colors.WHITE10,
            padding=ft.padding.only(left=30, top=30, bottom=40, right=30),
            border_radius=15,
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Transferencias Disponibles", weight=ft.FontWeight.BOLD, size=24),
                                header_row,
                                transferencias_container,
                            ]
                        ),
                        expand=True,
                        height=660,
                        bgcolor=ft.colors.BLACK12,
                        padding=ft.padding.all(10),
                        border_radius=15,
                    ),
                    
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Datos en Almacen", weight=ft.FontWeight.BOLD, size=24),
                                almacen_container
                            ]
                        ),
                        expand=False,
                        height=620,
                        width=400,
                        bgcolor=ft.colors.BLACK12,
                        padding=ft.padding.all(10),
                        border_radius=15,
                    ),
                ],
                spacing=30
            )
        )

    def update_tables(self):
        transferencias_container = self.load_transferencias_disponibles()
        almacen_container = self.load_almacen_datos()

        if self.transferencias_container:
            self.transferencias_container.content = transferencias_container
        if self.almacen_container:
            self.almacen_container.content = almacen_container

        self.page.update()

    def close_dialog(self, dialog):
        dialog.open = False
        self.page.update()
        self.update_tables()

    def aceptar_transferencia(self, transferencia_id):
        usuario = self.db_user.get_last_login_user()
        establecimiento = self.db_user.get_user_local(usuario)
        transferencias_disponibles = self.cargar_transferencias_disponibles()
        transferencia_aceptada = next((t for t in transferencias_disponibles if t["id"] == transferencia_id), None)
        
        if transferencia_aceptada:
            print(transferencia_aceptada)
            table_name = f"Almacen_{establecimiento}"
            
            # Verificar si el producto ya existe
            existing_product = self.db.get_product_by_name(table_name, transferencia_aceptada["producto"])
            if existing_product:
                # Actualizar producto existente
                self.db.update_product_in_almacen(
                    table_name=table_name,
                    producto=transferencia_aceptada["producto"],
                    cantidad=transferencia_aceptada["cantidad"],
                    precio_costo=transferencia_aceptada["precio_costo"],
                    precio_venta=transferencia_aceptada["precio_venta"]
                )
            else:
                # Insertar nuevo producto
                self.db.insert_product_in_almacen(
                    table_name=table_name,
                    producto=transferencia_aceptada["producto"],
                    cantidad=transferencia_aceptada["cantidad"],
                    precio_costo=transferencia_aceptada["precio_costo"],
                    precio_venta=transferencia_aceptada["precio_venta"],
                    fecha=transferencia_aceptada["fecha"]
                )
            
            # Obtener cafe_id
            cafe_id = self.db.get_cafe_id_by_name(establecimiento)
            
            # Verificar si cafe_id es None
            if cafe_id is None:
                print("Error: No se pudo obtener el cafe_id para el establecimiento.")
                return  # O manejar el error de una manera adecuada
            
            # Actualizar disponibilidad
            self.db.aceptar_transferencia(cafe_id, transferencia_aceptada["producto"])
            
            # Mostrar diálogo de alerta
            dialog = ft.AlertDialog(
                title=ft.Text("Éxito"),
                content=ft.Text("La transferencia ha sido aceptada satisfactoriamente."),
                actions=[
                    ft.TextButton("OK", on_click=lambda e: self.close_dialog(dialog))
                ],
                open=True
            )
            self.page.dialog = dialog
            self.page.update()

    def cargar_almacen_establecimiento(self, transferencia_id):
        usuario = self.db_user.get_last_login_user()
        establecimiento = self.db_user.get_user_local(usuario)
        almacen_establecimiento = self.db.get_all_inventario_almacen_establecimiento(establecimiento)
        return almacen_establecimiento
    
    def cargar_transferencias_disponibles(self):
        # Obtener el ID del último usuario y el ID del establecimiento
        usuario = self.db_user.get_last_login_user()
        establecimiento = self.db_user.get_user_local(usuario)
        cafe_id = self.db.get_cafe_id_by_name(establecimiento)

        # Verificar si cafe_id es None
        if cafe_id is None:
            print("Error: No se pudo obtener el cafe_id para el establecimiento.")
            return []  # O manejar el error de una manera adecuada

        # Obtener las transferencias disponibles (disponibilidad=True)
        transferencias = self.db.get_transferencias_disponibles(cafe_id)

        # Verificar y combinar productos duplicados
        productos_unicos = {}
        for transferencia in transferencias:
            producto = transferencia["producto"]
            if producto in productos_unicos:
                productos_unicos[producto]["cantidad"] += transferencia["cantidad"]
                productos_unicos[producto]["precio_costo"] = (productos_unicos[producto]["precio_costo"] + transferencia["precio_costo"]) / 2
                productos_unicos[producto]["precio_venta"] = (productos_unicos[producto]["precio_venta"] + transferencia["precio_venta"]) / 2
            else:
                productos_unicos[producto] = transferencia

        return list(productos_unicos.values())
    
    def load_almacen_datos(self):
        # Obtener el ID del último usuario y el ID del establecimiento
        usuario = self.db_user.get_last_login_user()
        establecimiento = self.db_user.get_user_local(usuario)
        self.db.crear_almacen_establecimiento(establecimiento)
        almacen_datos = self.db.get_all_inventario_almacen_establecimiento(establecimiento)

        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Container(ft.Text(dato["producto"]), width=150)),
                    ft.DataCell(ft.Container(ft.Text(str(dato["cantidad"])), width=100)),
                ],
            ) for dato in almacen_datos
        ]

        almacen_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Producto")),
                ft.DataColumn(ft.Text("Cantidad")),
            ],
            rows=rows,
            heading_row_height=0  # Ocultar la fila del encabezado
        )

        # Crear encabezado fijo
        header_row = ft.Row(
            controls=[
                ft.Container(ft.Text("Producto"), width=150),
                ft.Container(ft.Text("Cantidad"), width=100),
            ],
            spacing=10,
        )

        scrollable_container = ft.Container(
            expand=True,
            height=550,  # Ajustar la altura para que se habilite el scroll si hay muchos datos
            bgcolor=ft.colors.BLACK12,
            padding=ft.padding.all(10),
            border_radius=15,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,  # Activar scroll automático
                controls=[
                    ft.Container(content=header_row),
                    almacen_table
                ]
            )
        )

        return scrollable_container

    def load_transferencias_disponibles(self):
        transferencias = self.cargar_transferencias_disponibles()
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Container(ft.Text(transferencia["producto"]), width=200)),  # Reducing width
                    ft.DataCell(ft.Container(ft.Text(f"{transferencia['precio_costo']:.0f}"), width=50)),  # Reducing width
                    ft.DataCell(ft.Container(ft.Text(f"{transferencia['precio_venta']:.0f}"), width=50)),  # Reducing width
                    ft.DataCell(ft.Container(ft.Text(str(transferencia["cantidad"])), width=50)),  # Reducing width
                    ft.DataCell(ft.Container(ft.Text(transferencia["fecha"]), width=80)),  # Reducing width
                    ft.DataCell(ft.Container(ft.Checkbox(value=transferencia["disponibilidad"], disabled=True), width=5)),  # Reducing width
                    ft.DataCell(ft.Container(ft.TextButton(icon=ft.icons.ADD_TASK_OUTLINED, on_click=lambda e, transferencia_id=transferencia["id"]: self.aceptar_transferencia(transferencia_id)), width=50)),  # Reducing width
                ],
            ) for transferencia in transferencias
        ]

        transferencias_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Producto")),
                ft.DataColumn(ft.Text("Precio Costo")),
                ft.DataColumn(ft.Text("Precio Venta")),
                ft.DataColumn(ft.Text("Cantidad")),
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Disponibilidad")),
                ft.DataColumn(ft.Text("Acción")),
            ],
            rows=rows,
            heading_row_height=0  # Ocultar la fila del encabezado
        )

        scrollable_container = ft.Container(
            expand=True,
            height=750,
            width=1100,# Ajustar la altura para que se habilite el scroll si hay muchas transferencias
            bgcolor=ft.colors.BLACK12,
            padding=ft.padding.all(2),
            border_radius=15,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,  # Activar scroll automático
                controls=[
                    transferencias_table
                ]
            )
        )

        self.page.update()
        return scrollable_container

