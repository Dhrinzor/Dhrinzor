import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import flet as ft
from pages.dashboard.Menu.Containers.active_cafe_manager import *
from pages.authentication.utils.ccs import *
from pages.dashboard.Menu.Containers.data_hub import InventoryDB
import threading

class Build_Zone_Inventario(ft.Control):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.container = None
        self.data = []
        self.db = InventoryDB()
        self.dropdown = None
        self.active_cafe_manager = ActiveCafeManager()
        self.active_cafe_id = self.active_cafe_manager.get_active_cafe()
        self.first_cafe_id = self.active_cafe_id
        self.list_view = ft.ListView(controls=[], expand=True, auto_scroll=False)
        self.grouped_products = []
        self.cafe_name_input = ft.TextField(label="Nombre de la cafetería")
        self.sale_prices = {}
        self.quantities = {}
        self.transferencias_container = None  # Inicializar transferencias_container

        # Obtener todas las cafeterías y configurar active_cafe_id y first_cafe_id
        cafes = self.db.get_all_cafeterias()
        if cafes:  # Si hay cafeterías disponibles
            if not self.active_cafe_id:  # Si no hay café activo
                self.active_cafe_id = cafes[0]['id']
            self.first_cafe_id = self.active_cafe_id
            self.active_cafe_manager.set_active_cafe(self.active_cafe_id)
        else:
            print("Advertencia: No hay cafeterías disponibles.")
            self.first_cafe_id = None  # Asegúrate de manejar la ausencia de cafeterías
            self.active_cafe_id = None

    def extract_cafe_nombre(self, transferencia):
        # Extraer el nombre de la cafetería desde la cadena de transferencia
        if "TRANSFERENCIA REALIZADA HACIA LA ENTIDAD: " in transferencia:
            return transferencia.split("TRANSFERENCIA REALIZADA HACIA LA ENTIDAD: ")[1]
        return ""

    def build_zone_inventario(self):
        nuevo_cafe_button = ft.TextButton(
            text="Nueva Cafetería",
            icon=ft.icons.ADD_CIRCLE,
            on_click=self.nueva_cafeteria
        )
        
        cafes = self.db.get_all_cafeterias()
        active_cafe_id = self.active_cafe_manager.get_active_cafe()
        
        dropdown_items = []
        if cafes:
            for cafe in cafes:
                dropdown_items.append(
                    ft.CupertinoContextMenu(
                        content=ft.Text(cafe['nombre']),
                        actions=[
                            ft.CupertinoContextMenuAction(
                                text="Modificar",
                                on_click=lambda e, cafe_id=cafe['id']: self.modificar_cafeteria(cafe_id)
                            ),
                            ft.CupertinoContextMenuAction(
                                text="Eliminar",
                                is_destructive_action=True,
                                on_click=lambda e, cafe_id=cafe['id']: self.eliminar_cafeteria(cafe_id)
                            )
                        ]
                    )
                )
            self.dropdown = ft.Dropdown(
                options=[ft.dropdown.Option(text=cafe['nombre'], key=cafe['id']) for cafe in cafes],
                on_change=self.on_cafe_change,
                value=active_cafe_id if active_cafe_id else None
            )
        else:
            self.dropdown = ft.Dropdown(
                options=[],
                hint_text="Cafeterías",
                on_change=self.on_cafe_change,
            )
        
        self.cafe_name_input = ft.TextField(
            label="Nombre de la cafetería",
            error_text=""
        )
        
        transferencia_button = ft.TextButton(
            text="Transferencia",
            icon=ft.icons.SEND,
            on_click=self.transferencia_inventario
        )

        header_row = ft.Row(
            controls=[
                nuevo_cafe_button,
                self.dropdown,
                transferencia_button
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        # Inicializar transferencias_container correctamente
        self.transferencias_container = ft.Container(
            bgcolor=ft.colors.BLACK12,
            expand=False,
            padding=ft.padding.only(left=10, top=10, bottom=10, right=10),
            border_radius=15,
            content=ft.Column(
                controls=[]
            )
        )

        self.container = ft.Container(####TABLA DE TRANSFERENCIAS
            bgcolor=ft.colors.WHITE10,
            expand=False,
            padding=ft.padding.only(left=10, top=10, bottom=83, right=10),
            border_radius=15,
            content=ft.Column(
                controls=[
                    header_row,
                    self.transferencias_container
                ]
            )
        )
        
        return self.container

    def update_table(self, cafe_id):
        if not cafe_id:
            print("Advertencia: No se puede actualizar la tabla porque cafe_id es None.")
            self.transferencias_container.content.controls = [ft.Text("No se encontraron transferencias para esta cafetería.")]
            self.page.update()
            return

        transferencias = self.db.get_all_transferencias_exitosas()

        if not transferencias:
            no_transferencias_msg = ft.Text("No se han realizado transferencias.")
            self.transferencias_container.content.controls = [no_transferencias_msg]
        else:
            rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(transferencia["transferencia"])),
                        ft.DataCell(ft.Text(transferencia["fecha"])),
                        ft.DataCell(ft.TextButton(text="Consultar", on_click=lambda e, cafe_id=transferencia["cafe_id"], fecha=transferencia["fecha"], cafe_nombre=self.extract_cafe_nombre(transferencia["transferencia"]): self.consultar_inventario(cafe_id, fecha, cafe_nombre)))
                    ],
                ) for transferencia in transferencias
            ]

            transferencias_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Transferencias Exitosas")),
                    ft.DataColumn(ft.Text("Fecha")),
                    ft.DataColumn(ft.Text("Acciones")),
                ],
                rows=rows,
            )

            scrollable_container = ft.Container(
                content=ft.Column(
                    controls=[transferencias_table],
                    scroll=ft.ScrollMode.AUTO  # Activar scroll automático
                ),
                height=570,  # Ajustar la altura para que se habilite el scroll si hay muchas transferencias
            )

            self.transferencias_container.content.controls = [scrollable_container]

        self.page.update()

    def nueva_cafeteria(self, e):
        dialog = ft.CupertinoAlertDialog(
            title=ft.Text("Crear Nueva Cafetería"),
            content=ft.Column(
                controls=[
                    self.cafe_name_input
                ]
            ),
            actions=[
                ft.TextButton("Guardar", on_click=self.guardar_nueva_cafeteria),
                ft.TextButton("Cancelar", on_click=self.cancelar)
            ]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def guardar_nueva_cafeteria(self, e):
        nueva_cafe_nombre = self.cafe_name_input.value
        
        # Verificación de caracteres permitidos
        if not nueva_cafe_nombre.replace(" ", "").isalpha():
            self.cafe_name_input.error_text = "Solo letras y espacios."
            self.cafe_name_input.update()
            return
        
        nueva_cafe_nombre = nueva_cafe_nombre.upper()  # Convertir a mayúsculas

        # Verificar si la cafetería ya existe en la base de datos
        existing_cafe = self.db.get_cafe_by_name(nueva_cafe_nombre)
        if existing_cafe:
            self.cafe_name_input.error_text = "La cafetería ya existe."
            self.cafe_name_input.update()
            return

        # Limpiar el texto de error si todas las validaciones son correctas
        self.cafe_name_input.error_text = ""
        
        # Llamar a la función para crear la nueva cafetería en la base de datos
        cafe_id = self.db.create_new_cafe(nueva_cafe_nombre)
        self.active_cafe_manager.set_active_cafe(cafe_id)
        
        # Crear la tabla de inventario para la nueva cafetería
        self.db.create_inventory_table_for_cafe(cafe_id)
        
        # Actualizar el dropdown con la nueva lista de cafeterías
        cafes = self.db.get_all_cafeterias()
        dropdown_items = [ft.dropdown.Option(text=cafe['nombre'], key=cafe['id']) for cafe in cafes]
        self.dropdown.options = dropdown_items
        self.dropdown.value = cafe_id  # Seleccionar automáticamente la nueva cafetería
        self.dropdown.update()
        
        # Restablecer el valor del campo de entrada de nombre de cafetería
        self.cafe_name_input.value = ""
        self.cafe_name_input.update()
        
        # Cerrar el cuadro de diálogo
        self.page.dialog.open = False
        self.page.update()

    def cancelar(self, e):
        self.page.dialog.open = False
        self.page.update()

    def on_cafe_change(self, e):
        cafe_id = self.dropdown.value
        if not cafe_id:
            print("Advertencia: El usuario no seleccionó una cafetería válida.")
            return
        self.active_cafe_manager.set_active_cafe(cafe_id)
        self.first_cafe_id = cafe_id  # Actualizar first_cafe_id
        self.active_cafe_id = cafe_id  # También actualizar active_cafe_id
        print(f"Cafetería activa actualizada: {cafe_id}")
################################################################################
    def transferencia_inventario(self, e):
        # Verificar si existen cafeterías
        cafes = self.db.get_all_cafeterias()
        if not cafes:
            error_dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text("No existen cafeterías registradas. Por favor, cree una antes de realizar una transferencia."),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: self.cancelar(e))],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            self.page.dialog = error_dialog
            error_dialog.open = True
            self.page.update()
            return

        # Obtener todos los productos existentes
        productos = self.db.get_all_productos_existentes()

        # Crear filas de la tabla para cada producto existente
        rows = []
        for producto in productos:
            precio_costo = producto['precio_costo']
            precio_venta = precio_costo * 1.2

            # Aplicar las validaciones adicionales
            if precio_venta < 40:
                precio_venta = round(precio_venta, 2)
            elif 40 <= precio_venta < 100:
                precio_venta = round(precio_venta / 5) * 5
            else:  # precio_venta >= 100
                precio_venta = round(precio_venta / 10) * 10

            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Container(content=ft.Text(producto["producto"]), width=300)),
                        ft.DataCell(ft.Container(content=ft.Text(f"{precio_costo:.2f}"), width=120)),  # Dos decimales
                        ft.DataCell(ft.Container(content=ft.Text(str(producto["cantidad"])), width=50)),
                        ft.DataCell(ft.Container(content=ft.TextField(value=f"{precio_venta:.0f}", on_change=self.validate_precio_venta), width=100)),
                        ft.DataCell(ft.Container(content=ft.TextField(on_change=lambda e, prod_cantidad=producto["cantidad"]: self.validate_cantidad_a_transferir(e, prod_cantidad)), width=100))
                    ]
                )
            )

        self.transferencia_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Producto")),
                ft.DataColumn(ft.Text("Precio Costo")),
                ft.DataColumn(ft.Text("Cantidad Existente")),
                ft.DataColumn(ft.Text("Precio Venta")),
                ft.DataColumn(ft.Text("Cantidad a Ingresar"))
            ],
            rows=rows,
            heading_row_height=0  # Ocultar la fila de encabezado
        )

        # Crear encabezado personalizado
        custom_header = ft.Row(
            controls=[
                ft.Container(ft.Text("Producto", weight=ft.FontWeight.BOLD), width=300),
                ft.Container(ft.Text("Precio Costo", weight=ft.FontWeight.BOLD), width=120),
                ft.Container(ft.Text("Cantidad", weight=ft.FontWeight.BOLD), width=120),
                ft.Container(ft.Text("Precio Venta", weight=ft.FontWeight.BOLD), width=100),
                ft.Container(ft.Text("Transferir Cantidad", weight=ft.FontWeight.BOLD), width=120),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=10
        )

        # Crear contenedor con scroll para la tabla de productos
        scrollable_container = ft.Container(
            content=ft.Column(
                controls=[self.transferencia_table],
                scroll=ft.ScrollMode.AUTO  # Scroll automático
            ),
            width=1000,  # Ajustar ancho para que la tabla tenga suficiente espacio
            height=500,  # Altura fija para que aparezca el scroll si hay muchos productos
        )

        table = ft.Container(
            content=ft.Column(
                controls=[
                    custom_header,
                    scrollable_container
                ],
            ),
            expand=True,
            height=650,
            bgcolor=ft.colors.BLACK12,
            padding=ft.padding.all(10),
            border_radius=15,
        )

        # Crear botón de transferencia
        transferencia_button = ft.TextButton(
            text="Transferencia",
            icon=ft.icons.TRANSFER_WITHIN_A_STATION,
            on_click=self.realizar_transferencia
        )

        # Crear diálogo con el contenedor con scroll y el botón de transferencia
        dialog = ft.AlertDialog(
            title=ft.Text("Transferencia de Inventario"),
            content=table,
            actions=[
                transferencia_button,
                ft.TextButton("Cerrar", on_click=lambda e: self.cancelar(e))
            ]
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def validate_precio_venta(self, e):
        try:
            value = float(e.control.value)
            e.control.error_text = ""  # Borrar mensaje de error si el valor es un número
        except ValueError:
            e.control.error_text = "números"  # Mostrar mensaje de error si no es un número
        e.control.update()

    def validate_cantidad_a_transferir(self, e, cantidad_existente):
        try:
            value = int(e.control.value)
            cantidad_existente = int(cantidad_existente)
            if value < 0:
                raise ValueError("NÚMEROS>0")
            if value > cantidad_existente:
                raise ValueError(f"MAYOR A ({cantidad_existente})")
            e.control.error_text = ""  # Borrar mensaje de error si el valor es válido
        except ValueError as ve:
            e.control.error_text = str(ve)  # Mostrar mensaje de error si el valor no es válido
        e.control.update()

    def get_cantidad_a_transferir(self, producto_nombre):
        for row in self.transferencia_table.rows:
            if row.cells[0].content.content.value == producto_nombre:
                try:
                    cantidad_a_transferir = int(row.cells[4].content.content.value)
                    return cantidad_a_transferir
                except ValueError:
                    return None
        return None

    def get_precio_venta(self, producto_nombre):
        for row in self.transferencia_table.rows:
            if row.cells[0].content.content.value == producto_nombre:
                try:
                    precio_venta = float(row.cells[3].content.content.value)
                    return precio_venta
                except ValueError:
                    return None
        return None

    def consultar_inventario(self, cafe_id, fecha, cafe_nombre):
        # Obtener los datos del inventario para la cafetería seleccionada en la fecha especificada
        inventario = self.db.get_inventario_cafe(cafe_id, fecha)

        # Crear filas de la tabla para cada producto en el inventario
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(producto["producto"])),
                    ft.DataCell(ft.Text(f"{producto['precio_costo']:.0f}")),
                    ft.DataCell(ft.Text(f"{producto['precio_venta']:.0f}")),
                    ft.DataCell(ft.Text(str(producto["cantidad"]))),
                    ft.DataCell(ft.Text(f"{producto['beneficios']:.0f}")),
                    ft.DataCell(ft.Text(producto["fecha"]))
                ],
            ) for producto in inventario
        ]

        inventario_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Producto")),
                ft.DataColumn(ft.Text("Precio Costo")),
                ft.DataColumn(ft.Text("Precio Venta")),
                ft.DataColumn(ft.Text("Cantidad")),
                ft.DataColumn(ft.Text("Beneficios")),
                ft.DataColumn(ft.Text("Fecha"))
            ],
            rows=rows,
        )

        # Crear el diálogo con la tabla de inventario
        dialog = ft.AlertDialog(
            title=ft.Text(f"TRANSFERENCIA HACIA: {cafe_nombre} DEL DIA: {fecha}"),
            content=inventario_table,
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: self.cancelar(e))
            ]
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def realizar_transferencia(self, e):
        # Paso 1: Validar todas las filas de la tabla
        for row in self.transferencia_table.rows:
            cantidad_cell = row.cells[4]
            precio_venta_cell = row.cells[3]

            # Verificar errores en los campos
            if cantidad_cell.content.content.error_text or precio_venta_cell.content.content.error_text:
                # Mostrar mensaje de error al usuario
                error_dialog = ft.AlertDialog(
                    title=ft.Text("Error de Validación"),
                    content=ft.Text("Por favor, corrige los errores antes de continuar."),
                    actions=[ft.TextButton("Cerrar", on_click=lambda e: self.cancelar(e))]
                )
                self.page.dialog = error_dialog
                error_dialog.open = True
                self.page.update()
                return  # Salir del método si hay errores

        # Paso 2: Proceder con la lógica de transferencia si no hay errores
        productos = self.db.get_all_productos_existentes()
        active_cafe_id = self.active_cafe_manager.get_active_cafe()
        active_cafe_nombre = self.db.get_cafe_name_by_id(active_cafe_id)

        productos_transferidos = []
        for producto in productos:
            cantidad_a_transferir = self.get_cantidad_a_transferir(producto["producto"])
            precio_venta = self.get_precio_venta(producto["producto"])
            if cantidad_a_transferir is None or precio_venta is None:
                continue

            if cantidad_a_transferir <= 0:
                continue

            nueva_cantidad = producto["cantidad"] - cantidad_a_transferir
            if nueva_cantidad == 0:
                self.db.delete_producto(producto["producto"])
            else:
                self.db.update_producto_cantidad(producto["producto"], nueva_cantidad)

            productos_transferidos.append({
                "producto": producto["producto"],
                "precio_costo": producto["precio_costo"],
                "precio_venta": precio_venta,
                "cantidad": cantidad_a_transferir
            })

        for producto in productos_transferidos:
            self.db.insert_transferencia_cafe(
                active_cafe_id,
                producto["producto"],
                producto["precio_costo"],
                producto["precio_venta"],
                producto["cantidad"]
            )

        if productos_transferidos:
            self.db.insert_transferencia_exitosa(active_cafe_nombre, active_cafe_id)

        self.update_table(active_cafe_id)
        self.page.dialog.open = False
        self.page.update()

        success_dialog = ft.AlertDialog(
            title=ft.Text("Éxito"),
            content=ft.Text("La transferencia se ha realizado con éxito."),
        )
        self.page.dialog = success_dialog
        success_dialog.open = True
        self.page.update()

        def close_success_dialog():
            success_dialog.open = False
            self.page.update()

        timer = threading.Timer(0.6, close_success_dialog)
        timer.start()
