import flet as ft
from pages.authentication.utils.ccs import Ccs
from pages.dashboard.Menu.Containers.data_hub import InventoryDB
from pages.authentication.utils.user import UserDB
import threading
import time
from datetime import datetime
     
#################################################################################################################################################################3
class Build_Zone_New_Order(ft.Control):
    def __init__(self, page, dashboard):
        super().__init__()
        self.page = page
        self.dashboard = dashboard  # Referencia a DashboardPage
        self.main_app = dashboard.main_app  # Referencia a MainApp
        self.ccs = Ccs()
        self.db = InventoryDB()
        self.db_user = UserDB()
        self.cargar_datos()
        self.fila_venta = []  # Inicializar el atributo fila_venta
        self.list_view = ft.ListView(controls=[], expand=True, auto_scroll=False)
        self.list_view_ventas = ft.ListView(controls=[], expand=True, auto_scroll=False)

        self.textfield_dinero_recibido = ft.TextField(
            value="0",
            label="Dinero Recibido",
            hint_text="Introduce el monto",
            width=200,
        )
        
###################################################################      
    def cargar_datos(self):
        try:
            # Verificar si la tabla está vacía
            existing_data = self.db.get_all_categories()
            
            # Si la tabla está vacía, insertar los datos simulados
            if not existing_data:
                datos_simulados = [
                    {"start_range": "1",    "end_range": "100"},
                    {"start_range": "101",  "end_range": "200"},
                    {"start_range": "201",  "end_range": "300"},
                    {"start_range": "301",  "end_range": "400"},
                    {"start_range": "401",  "end_range": "500"},
                    {"start_range": "501",  "end_range": "600"},
                    {"start_range": "601",  "end_range": "700"},
                    {"start_range": "701",  "end_range": "800"},
                    {"start_range": "801",  "end_range": "900"},
                    {"start_range": "901",  "end_range": "1000"},
                    {"start_range": "1001", "end_range": "2000"},
                    {"start_range": "2001", "end_range": "3000"},
                    {"start_range": "3001", "end_range": "4000"},
                    {"start_range": "4001", "end_range": "5000"},
                    {"start_range": "5001", "end_range": "6000"},
                    {"start_range": "6001", "end_range": "10000"},
                    
                ]
                for dato in datos_simulados:
                    self.db.insert_category(dato["start_range"], dato["end_range"])
                self.datos = datos_simulados
            else:
                # Si la tabla ya contiene datos, cargarlos
                self.datos = existing_data
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            self.datos = []  # Asegurarse de que `self.datos` tenga un valor por defecto en caso de error
            
 
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            self.datos = []  # Asegurarse de que `self.datos` tenga un valor por defecto en caso de error
            
    def crear_filas(self):
        filas = []
        for dato in self.datos:
            filas.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.IconButton(icon=ft.icons.SEARCH, on_click=lambda e: self.buscar_datos(dato)),
                                width=100  # Ancho fijo para el contenedor de la acción
                            ),
                            ft.Container(
                                content=ft.Text(f"DE {dato['start_range']} A {dato['end_range']}"),
                                width=200  # Ancho fijo para el contenedor de la categoría
                            ),
                        ],
                        spacing=10,
                    ),
                    padding=ft.padding.only(bottom=5)
                )
            )
        return filas
      
    def build_table_header(self):
        return ft.Row(
            controls=[
                ft.Container(ft.Text("    Buscar", size=18), width=100),
                ft.Container(ft.Text("Categoría", size=18), width=200),
            ],
            spacing=10,
        )

####################################################################
    def crear_filas_ventas(self):
        filas_venta = []
        for item in self.fila_venta:
            filas_venta.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(content=ft.Text(f"{item['producto']}", size=13, weight=ft.FontWeight.BOLD, width=170)),
                            ft.Container(content=ft.Text(f"{item['cantidad']}", size=13, weight=ft.FontWeight.BOLD, width=80)),
                            ft.Container(content=ft.Text(f"{item['precio_venta']}", size=13, weight=ft.FontWeight.BOLD, width=50)),
                            ft.Container(content=ft.IconButton(icon=ft.icons.CLOSE_OUTLINED, on_click=lambda e, item=item: self.remove_from_table(item)),
                                width=100
                            ),
                        ],
                        spacing=10,
                    ),
                    padding=ft.padding.only(bottom=5)
                )
            )
        return filas_venta

    def build_table_header_ventas(self):
        return ft.Row(
            controls=[
                ft.Container(ft.Text("  Productos", size=18), width=170),
                ft.Container(ft.Text("Cantidad", size=18), width=90),
                ft.Container(ft.Text("  Precio", size=18), width=80),
                ft.Container(ft.IconButton(icon=ft.icons.REMOVE_SHOPPING_CART_OUTLINED, disabled=True, disabled_color=ft.colors.WHITE54), width=50),
            ],
            spacing=5,
        )

    def actualizar_filas_ventas(self):
        usuario = self.db_user.get_last_login_user()
        establecimiento = self.db_user.get_user_local(usuario)
        tabla = f"productos_a_vender_{establecimiento}"

        # Obtener todos los productos vendidos de la base de datos
        productos_vendidos = self.db.obtener_todos_productos_a_vender(tabla)

        filas_venta = []
        for producto in productos_vendidos:
            filas_venta.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(content=ft.Text(f"{producto[0]}", size=13, weight=ft.FontWeight.BOLD, width=170)),  # Producto_vender
                            ft.Container(content=ft.Text(f"{producto[1]}", size=13, weight=ft.FontWeight.BOLD, width=80)),   # cantidad
                            ft.Container(content=ft.Text(f"{producto[2]}", size=13, weight=ft.FontWeight.BOLD, width=50)),   # precio
                            ft.Container(content=ft.IconButton(icon=ft.icons.CLOSE_OUTLINED, on_click=lambda e, item=producto: self.remove_from_table(item)),
                                width=100
                            ),
                        ],
                        spacing=10,
                    ),
                    padding=ft.padding.only(bottom=5)
                )
            )
        self.list_view_ventas.controls = filas_venta
        self.list_view_ventas.update()

    def obtener_datos_inventario_usuario(self):
        usuario = self.db_user.get_last_login_user()
        establecimiento = self.db_user.get_user_local(usuario)
        inventario = self.db.get_all_inventario_almacen_establecimiento(establecimiento)
        return inventario

##########1era    #########################################################  
    def build_zone_new_order(self):
        self.list_view = ft.ListView(
            controls=self.crear_filas(),
            expand=True,
            auto_scroll=False,
        )
        self.list_view_ventas = ft.ListView(
            controls=self.crear_filas_ventas(),
            expand=True,
            auto_scroll=False,
        )
        
        # Campo de texto para Dinero Recibido
        self.textfield_dinero_recibido = ft.TextField(
            value="0",
            label="Dinero Recibido",
            hint_text="Introduce el monto",
            width=200,
        )

        # Datos del inventario del usuario
        inventario_usuario = self.obtener_datos_inventario_usuario()
        contenedores_productos = [
            ft.Container(
                content=ft.Stack(
                    controls=[
                        ft.Container(
                            content=ft.Text(f"{item['cantidad']}", size=12, weight=ft.FontWeight.BOLD),
                            alignment=ft.alignment.top_right,
                            padding=ft.padding.only(top=5, right=5)
                        ),
                        ft.Container(
                            content=ft.Text(f"{item['producto']}", size=14, weight=ft.FontWeight.BOLD),
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=ft.Text(f"${item['precio_venta']}", size=12, weight=ft.FontWeight.BOLD),
                            alignment=ft.alignment.bottom_right,
                            padding=ft.padding.only(bottom=5, right=5)
                        )
                    ],
                ),
                padding=ft.padding.all(5),
                border_radius=10,
                bgcolor=ft.colors.LIGHT_GREEN,
                width=189,  # Ancho específico
                height=100,  # Alto específico
                on_click=lambda e, item=item: self.on_product_click(e, item),
                animate=ft.Animation(400, "easeInOutQuad"),  # Añadir animación con duración y tipo
            )
            for item in inventario_usuario
        ]

        # Crear filas de productos en una cuadrícula de 4 columnas
        filas_productos = []
        for i in range(0, len(contenedores_productos), 4):
            fila = ft.Row(
                controls=contenedores_productos[i:i+4],
                spacing=10,
            )
            filas_productos.append(fila)

        self.container = ft.Container(
            bgcolor=ft.colors.WHITE10,
            expand=True,
            padding=ft.padding.only(left=3, top=50, bottom=5, right=3),
            border_radius=15,
            content=ft.ResponsiveRow(
                expand=True,  # Expande la fila principal
                controls=[
                    ft.Container(
                        padding=ft.padding.all(5),
                        expand=True,
                        border_radius=15,
                        content=ft.Row(
                            expand=True,  # Asegura que la columna interior se expanda
                            controls=[
                                ft.Container(
                                    padding=ft.padding.all(10),
                                    bgcolor=ft.colors.BLACK12,
                                    expand=False,  # También expande el último contenedor hacia abajo
                                    height=665,  # Asigna una altura para el tercer contenedor
                                    width=430,  # Tamaño más pequeño
                                    border_radius=15,
                                    content=ft.Column(
                                        controls=[
                                            ft.Container(
                                                content=ft.Column(
                                                    controls=[
                                                        self.build_table_header_ventas(),
                                                        self.list_view_ventas,
                                                        #self.textfield_dinero_recibido,  # Agregamos el TextField aquí
                                                        ft.Row(
                                                            controls=[
                                                                ft.TextButton(
                                                                    text="Abrir cuenta",
                                                                    icon=ft.icons.ACCOUNT_BOX_OUTLINED,
                                                                    on_click=lambda e: self.abrir_cuenta()
                                                                ),
                                                                ft.TextButton(
                                                                    text="Pagar ahora",
                                                                    icon=ft.icons.PAYMENTS_OUTLINED,
                                                                    on_click=lambda e: self.pagar_ahora()
                                                                ),
                                                            ],
                                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                                        ),
                                                    ],
                                                ),
                                                expand=True,
                                                height=550,
                                                padding=ft.padding.all(5),
                                                border_radius=15,
                                            )
                                        ]
                                    )
                                ),
                                ft.VerticalDivider(width=1, thickness=1),
                                ft.Container(
                                    padding=ft.padding.all(5),
                                    bgcolor=ft.colors.BLACK12,
                                    expand=True,
                                    border_radius=15,
                                    height=665,  # Asigna una altura para el segundo contenedor
                                    content=ft.Column(
                                        controls=filas_productos,
                                        scroll=ft.ScrollMode.AUTO  # Agregar scroll automático
                                    )
                                ),
                                ft.VerticalDivider(width=1, thickness=1),
                                ft.Container(
                                    padding=ft.padding.all(2),
                                    bgcolor=ft.colors.BLACK12,
                                    expand=False,  # También expande el último contenedor hacia abajo
                                    height=665,  # Asigna una altura para el tercer contenedor
                                    width=250,  # Tamaño más pequeño
                                    border_radius=15,
                                    content=ft.Column(
                                        controls=[
                                            ft.Container(
                                                content=ft.Column(
                                                    controls=[
                                                        self.build_table_header(),
                                                        self.list_view,
                                                    ],
                                                ),
                                                expand=True,
                                                height=550,
                                                padding=ft.padding.only(bottom=16, top=16),
                                                border_radius=15,
                                            )
                                        ]
                                    )
                                ),
                            ]
                        )
                    )
                ]
            )
        )
        return self.container

###########2do########################################################
    def reload_all_containers(self):
        print("Recargando todos los contenedores de inventario...")
        print("Estructura de self.container:")
        print(self.container.content.controls)
        # Obtener los datos actualizados del inventario desde la base de datos
        inventario_usuario = self.obtener_datos_inventario_usuario()
        print(f"Datos de inventario recargados: {inventario_usuario}")

        # Crear contenedores directamente dentro de esta función
        contenedores_productos = [
            ft.Container(
                content=ft.Stack(
                    controls=[
                        ft.Container(
                            content=ft.Text(f"{item['cantidad']}", size=12, weight=ft.FontWeight.BOLD),
                            alignment=ft.alignment.top_right,
                            padding=ft.padding.only(top=5, right=5),
                        ),
                        ft.Container(
                            content=ft.Text(f"{item['producto']}", size=14, weight=ft.FontWeight.BOLD),
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=ft.Text(f"${item['precio_venta']}", size=12, weight=ft.FontWeight.BOLD),
                            alignment=ft.alignment.bottom_right,
                            padding=ft.padding.only(bottom=5, right=5),
                        ),
                    ],
                ),
                padding=ft.padding.all(5),
                border_radius=10,
                bgcolor=ft.colors.LIGHT_GREEN,
                width=189,  # Ancho específico del contenedor de producto
                height=100,  # Alto específico del contenedor de producto
                on_click=lambda e, item=item: self.on_product_click(e, item),
                animate=ft.Animation(400, "easeInOutQuad"),  # Añadir animación con duración y tipo
            )
            for item in inventario_usuario
        ]

        # Crear filas de productos en una cuadrícula de 4 columnas
        filas_productos = [
            ft.Row(
                controls=contenedores_productos[i:i+4],
                spacing=10,  # Espacio entre los productos en la fila
            )
            for i in range(0, len(contenedores_productos), 4)
        ]

        # Actualizar el contenedor principal de productos sin afectar el diseño general
        for container in self.container.content.controls:
            if isinstance(container, ft.Container) and any(isinstance(control, ft.Row) for control in container.content.controls):
                container.content.controls = filas_productos
                container.update()  # Forzar la actualización visual del contenedor
                print("Contenedor de inventario actualizado correctamente.")
                break

    def abrir_cuenta(self):
        print("Abrir cuenta clicked")

    def buscar_datos(self, dato):
        # Implementar la lógica de búsqueda aquí
        print(f"Buscando datos para: DE {dato['start_range']} A {dato['end_range']}")
 
    def guardar_producto_vendido(self, item):
        usuario = self.db_user.get_last_login_user()
        establecimiento = self.db_user.get_user_local(usuario)
        tabla = f"productos_a_vender_{establecimiento}"

        # Verificar si el producto ya existe en la tabla
        producto_existente = self.db.obtener_producto_vendido(tabla, item['producto'])

        if producto_existente:
            # Si el producto ya existe, actualizar la cantidad
            nueva_cantidad = int(producto_existente[2]) + 1  # Asumiendo que la cantidad está en el índice 2 de la tupla
            self.db.actualizar_producto_vendido(tabla, item['producto'], nueva_cantidad)
        else:
            # Si el producto no existe, insertarlo
            producto_vendido = {
                "Producto_vender": item['producto'],
                "cantidad": 1,  # Cantidad fija en 1 para cada click
                "precio": item['precio_venta'],
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Fecha y hora actual
            }
            self.db.insert_producto_vendido(tabla, producto_vendido)
        
        # Actualizar la tabla visual
        self.actualizar_filas_ventas()

    def on_product_click(self, e, item):
        # Verificar si los módulos ya están bloqueados
        self.dashboard.main_app.bloquear_modulos()
        self.page.update()

        try:
            # Lógica para manejar el clic en el producto
            usuario = self.db_user.get_last_login_user()
            establecimiento = self.db_user.get_user_local(usuario)
            tabla_almacen = f"Almacen_{establecimiento.replace(' ', '_')}"

            if item['cantidad'] > 0:
                item['cantidad'] -= 1
                self.db.actualizar_cantidad_producto(tabla_almacen, item['producto'], item['cantidad'])
                print(f"Producto actualizado: {item['producto']} - Nueva cantidad: {item['cantidad']}")
                self.actualizar_cantidad_producto_visual(item['producto'], item['cantidad'])
            else:
                print("El producto no tiene stock suficiente.")

        except Exception as ex:
            print(f"Error durante la operación del producto: {ex}")

        finally:
            # Desbloquear módulos solo después de que toda la operación haya terminado
            #self.dashboard.main_app.bloquear_modulos()
            self.page.update()
###################################################################
    def calcular_total_a_pagar(self):
        usuario = self.db_user.get_last_login_user()
        establecimiento = self.db_user.get_user_local(usuario)
        tabla = f"productos_a_vender_{establecimiento}"

        # Obtener todos los productos vendidos de la base de datos
        productos_vendidos = self.db.obtener_todos_productos_a_vender(tabla)

        total = sum(int(producto[1]) * float(producto[2]) for producto in productos_vendidos)
        return total

    def actualizar_dinero_recibido(self, e):
        self.dinero_recibido = float(e.control.value) if e.control.value else 0.0

    def cerrar_dialogo_pago(self):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

            # Restablecer el campo de texto a 0
            if self.textfield_ref.current:
                self.textfield_ref.current.value = "0"
                self.textfield_ref.current.update()

    def validar_dinero_recibido(self, e):
        try:
            self.dinero_recibido = float(self.textfield_ref.current.value)
        except ValueError:
            self.dinero_recibido = 0.0
        self.actualizar_error_texto()

    def agregar_dinero(self, cantidad):
        if self.textfield_ref.current:
            # Obtener el valor actual del TextField y sumarle la cantidad
            try:
                valor_actual = float(self.textfield_ref.current.value)
            except ValueError:
                valor_actual = 0.0
            
            nuevo_valor = valor_actual + cantidad
            self.textfield_ref.current.value = f"{nuevo_valor:.0f}"
            self.textfield_ref.current.update()
            
            # Actualizar la validación del dinero recibido
            self.validar_dinero_recibido(None)

    def actualizar_error_texto(self):
        total_a_pagar = self.calcular_total_a_pagar()
        if self.dinero_recibido < total_a_pagar:
            falta = total_a_pagar - self.dinero_recibido
            self.error_text_ref.current.value = f"Faltan {falta:.0f} CUP"
            self.error_text_ref.current.color = ft.colors.RED
        elif self.dinero_recibido > total_a_pagar:
            cambio = self.dinero_recibido - total_a_pagar
            self.error_text_ref.current.value = f"Devolver {cambio:.0f} CUP"
            self.error_text_ref.current.color = ft.colors.YELLOW
        else:
            self.error_text_ref.current.value = "Exacto"
            self.error_text_ref.current.color = ft.colors.GREEN

        self.error_text_ref.current.update()

#########################################################################
    def mostrar_alerta_no_productos(self):
        alert_dialog = ft.AlertDialog(
            title=ft.Text("No hay productos para vender"),
            # content=ft.Text("No hay productos en la tabla de ventas."),
        )

        self.page.dialog = alert_dialog
        self.page.dialog.open = True
        self.page.update()

        def close_alert():
            time.sleep(0.8)
            alert_dialog.open = False
            self.page.update()

        threading.Thread(target=close_alert).start()

    def remove_from_table(self, item):
        usuario = self.db_user.get_last_login_user()
        establecimiento = self.db_user.get_user_local(usuario)
        tabla_venta = f"productos_a_vender_{establecimiento}"
        tabla_almacen = f"Almacen_{establecimiento.replace(' ', '_')}"

        producto = item[0]
        cant_exist = self.db.obtener_cantidad(tabla_almacen, producto)
        nueva_cantidad = int(item[1]) + int(cant_exist[0])

        # Eliminar el producto de la tabla de ventas
        self.db.eliminar_producto_de_venta(tabla_venta, producto)
        print(f"Producto eliminado de {tabla_venta}: {producto}")

        # Actualizar la cantidad en el inventario
        self.db.actualizar_cantidad_producto(tabla_almacen, producto, nueva_cantidad)
        print(f"Cantidad actualizada en {tabla_almacen} para {producto}: {nueva_cantidad}")

        # Recargar el inventario visual
        self.reload_all_containers()

        # Eliminar la fila correspondiente en la lista de ventas visual
        for fila in self.list_view_ventas.controls:
            producto_en_fila = fila.content.controls[0].content.value
            if producto_en_fila == producto:
                self.list_view_ventas.controls.remove(fila)
                print(f"Fila eliminada de la vista de ventas: {producto}")
                break

        # Actualizar la lista visual de ventas
        self.list_view_ventas.update()

        print("Inventario visual y lista de ventas sincronizados.")
              
    def actualizar_inventario_visual(self):
        print("Actualizando el inventario visual sin deformar el diseño...")

        # Obtener los datos actualizados del inventario desde la base de datos
        inventario_usuario = self.obtener_datos_inventario_usuario()
        print(f"Datos de inventario actualizados: {inventario_usuario}")

        # Buscar el subcontenedor que contiene las filas de productos
        for container in self.container.content.controls:
            if isinstance(container, ft.Container) and container.expand:  # Asegúrate de identificar correctamente el contenedor expandible
                filas_productos = []

                # Crear las filas actualizadas
                contenedores_productos = [
                    self.crear_contenedor_producto(item) for item in inventario_usuario
                ]
                for i in range(0, len(contenedores_productos), 4):
                    fila = ft.Row(
                        controls=contenedores_productos[i:i+4],
                        spacing=10,
                    )
                    filas_productos.append(fila)

                # Actualizar únicamente el contenido de las filas de productos
                container.content.controls = filas_productos
                container.update()
                print("Productos actualizados visualmente.")
                break
          
    def reload_inventory(self):
        print("Forzando la recarga del inventario...")

        # Obtener los datos actualizados del inventario desde la base de datos
        inventario_usuario = self.obtener_datos_inventario_usuario()
        print(f"Datos del inventario: {inventario_usuario}")

        # Crear contenedores para cada producto
        contenedores_productos = [
            ft.Container(
                content=ft.Stack(
                    controls=[
                        ft.Container(
                            content=ft.Text(f"{item['cantidad']}", size=12, weight=ft.FontWeight.BOLD),
                            alignment=ft.alignment.top_right,
                            padding=ft.padding.only(top=5, right=5),
                        ),
                        ft.Container(
                            content=ft.Text(f"{item['producto']}", size=14, weight=ft.FontWeight.BOLD),
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=ft.Text(f"${item['precio_venta']}", size=12, weight=ft.FontWeight.BOLD),
                            alignment=ft.alignment.bottom_right,
                            padding=ft.padding.only(bottom=5, right=5),
                        ),
                    ],
                ),
                padding=ft.padding.all(5),
                border_radius=10,
                bgcolor=ft.colors.LIGHT_GREEN,
                width=189,
                height=100,
                on_click=lambda e, item=item: self.on_product_click(e, item),
            )
            for item in inventario_usuario
        ]

        # Crear filas de productos en una cuadrícula de 4 columnas
        filas_productos = [
            ft.Row(
                controls=contenedores_productos[i:i+4],
                spacing=10,
            )
            for i in range(0, len(contenedores_productos), 4)
        ]

        # Crear un nuevo contenedor principal
        nuevo_contenedor = ft.Container(
            expand=True,
            borderradius=15,
            padding=ft.padding.all(5),
            bgcolor=ft.colors.WHITE10,
            content=ft.Column(
                controls=filas_productos,
                spacing=10,
            ),
        )

        # Reemplazar completamente el contenedor
        self.page.controls.remove(self.container)  # Elimina el contenedor actual de la página
        self.container = nuevo_contenedor  # Asigna el nuevo contenedor
        self.page.controls.append(self.container)  # Agrega el nuevo contenedor a la página

        # Actualizar la página para reflejar los cambios
        self.page.update()
        print("Contenedor principal reemplazado y la página actualizada.")
 
#########################################################################   
    def pagar_ahora(self):
        if self.dashboard.main_app.menus_disabled:
            print("Los menús están bloqueados. No se puede proceder con el pago.")
            return

        usuario = self.db_user.get_last_login_user()
        establecimiento = self.db_user.get_user_local(usuario)
        table_name_venta = f"productos_a_vender_{establecimiento}"

        # Verificar si hay productos en la tabla de productos a vender
        productos_vendidos = self.db.obtener_todos_productos_a_vender(table_name_venta)
        if not productos_vendidos:
            self.mostrar_alerta_no_productos()
            return

        total_a_pagar = self.calcular_total_a_pagar()
        self.textfield_ref = ft.Ref[ft.TextField]()
        self.error_text_ref = ft.Ref[ft.Text]()

        # Inicializar el TextField a 0
        self.textfield_ref.current = ft.TextField(
            value="0",  # Inicializar el valor del TextField a 0
            label="Dinero recibido del cliente",
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self.validar_dinero_recibido
        )

        dialogo_pago = ft.AlertDialog(
            title=ft.Text("Confirmar Pago"),
            content=ft.Container(
                content=ft.Column(
                    [   
                        ft.Container(
                            padding=10,
                            content=ft.Column(
                                controls=[
                                    ft.Container(
                                        padding=ft.padding.only(left=190, right=100),
                                        content=ft.Column(
                                            [
                                                ft.Text(
                                                    "TOTAL A PAGAR",
                                                    size=29,
                                                    weight=ft.FontWeight.BOLD,
                                                    text_align=ft.TextAlign.CENTER
                                                ),
                                                ft.Text(
                                                    f"{total_a_pagar:.0f} CUP",
                                                    size=24,
                                                    weight=ft.FontWeight.BOLD,
                                                    text_align=ft.TextAlign.CENTER
                                                ),  # Mostrar el total a pagar
                                            ]
                                        )
                                    ),           
                                    self.textfield_ref.current,  # Referencia al TextField
                                    ft.Text(
                                        ref=self.error_text_ref,
                                        color=ft.colors.RED,
                                        size=16,
                                        weight=ft.FontWeight.BOLD
                                    )  # Texto para mostrar faltante o cambio
                                ]
                            )
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text="1",
                                    icon=ft.icons.ATTACH_MONEY,
                                    width=120,
                                    on_click=lambda e: self.agregar_dinero(1)
                                ),
                                ft.ElevatedButton(
                                    text="3",
                                    icon=ft.icons.ATTACH_MONEY,
                                    width=120,
                                    on_click=lambda e: self.agregar_dinero(3)
                                ),
                                ft.ElevatedButton(
                                    text="5",
                                    icon=ft.icons.ATTACH_MONEY,
                                    width=120,
                                    on_click=lambda e: self.agregar_dinero(5)
                                ),
                                ft.ElevatedButton(
                                    text="10",
                                    icon=ft.icons.ATTACH_MONEY,
                                    width=120,
                                    on_click=lambda e: self.agregar_dinero(10)
                                ),
                                ft.ElevatedButton(
                                    text="20",
                                    icon=ft.icons.ATTACH_MONEY,
                                    width=120,
                                    on_click=lambda e: self.agregar_dinero(20)
                                )
                            ],
                            spacing=5
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text="50",
                                    icon=ft.icons.ATTACH_MONEY,
                                    width=120,
                                    on_click=lambda e: self.agregar_dinero(50)
                                ),
                                ft.ElevatedButton(
                                    text="100",
                                    icon=ft.icons.ATTACH_MONEY,
                                    width=120,
                                    on_click=lambda e: self.agregar_dinero(100)
                                ),
                                ft.ElevatedButton(
                                    text="200",
                                    icon=ft.icons.ATTACH_MONEY,
                                    width=120,
                                    on_click=lambda e: self.agregar_dinero(200)
                                ),
                                ft.ElevatedButton(
                                    text="500",
                                    icon=ft.icons.ATTACH_MONEY,
                                    width=120,
                                    on_click=lambda e: self.agregar_dinero(500)
                                ),
                                ft.ElevatedButton(
                                    text="1000",
                                    icon=ft.icons.ATTACH_MONEY,
                                    width=120,
                                    on_click=lambda e: self.agregar_dinero(1000)
                                )
                            ],
                            spacing=5
                        )
                    ],
                    spacing=20
                ),
                expand=True,  # Ancho del diálogo
                height=300  # Alto del diálogo
            ),
            actions=[
                ft.TextButton(
                    text="Cancelar",
                    on_click=lambda e: self.cerrar_dialogo_pago()
                ),
                ft.TextButton(
                    text="Confirmar",
                    on_click=self.confirmar_pago
                )
            ],
            on_dismiss=lambda e: print("Diálogo de pago cerrado")
        )

        self.page.dialog = dialogo_pago
        self.page.dialog.open = True
        self.page.update()

    def cerrar_dialogo_pago(self):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

            # Restablecer el campo de texto a 0
            if self.textfield_ref.current:
                self.textfield_ref.current.value = "0"
                self.textfield_ref.current.update()

    def confirmar_pago(self, e):
        usuario = self.db_user.get_last_login_user()
        establecimiento = self.db_user.get_user_local(usuario)
        table_name_vendidos = f"productos_vendidos_{establecimiento}"
        table_name_venta = f"productos_a_vender_{establecimiento}"
        table_name_almacen = f"Almacen_{establecimiento.replace(' ', '_')}"

        total_a_pagar = self.calcular_total_a_pagar()

        # Verificar si el dinero recibido es suficiente
        if self.dinero_recibido < total_a_pagar:
            self.error_text_ref.current.value = f"No se puede confirmar la venta. Faltan {total_a_pagar - self.dinero_recibido:.0f} CUP."
            self.error_text_ref.current.color = ft.colors.RED
            self.error_text_ref.current.update()
            return  # Salir de la función sin proceder con el pago

        productos_vendidos = self.db.obtener_todos_productos_a_vender(table_name_venta)

        self.db.confirmar_pago(table_name_vendidos,productos_vendidos,usuario,table_name_almacen,table_name_venta)

        self.list_view_ventas.controls.clear()
        self.list_view_ventas.update()

        print("Filas de la tabla de ventas visual eliminadas.")
        
        self.actualizar_inventario_visual()

        # Restablecer el campo de texto a 0
        if self.textfield_ref.current:
            self.textfield_ref.current.value = "0"
            self.textfield_ref.current.update()

        print(f"Pago confirmado, total a pagar: {self.calcular_total_a_pagar():.0f} CUP, dinero recibido: {self.textfield_ref.current.value} CUP")
        self.cerrar_dialogo_pago()

#########################################################################  
    def actualizar_cantidad_producto_visual(self, producto, nueva_cantidad):
        for container in self.container.content.controls:
            # Asegurarse de que el container sea del tipo esperado
            if isinstance(container, ft.Container) and hasattr(container.content, "controls"):
                for fila in container.content.controls:  # Fila en el contenedor
                    if hasattr(fila, "controls"):  # Verificar que la fila tiene controles
                        for control in fila.controls:  # Producto dentro de la fila
                            if isinstance(control, ft.Container) and producto in control.content.controls[1].content.value:
                                # Actualizar solo la cantidad del producto específico
                                cantidad_control = control.content.controls[0]
                                cantidad_control.content = ft.Text(f"{nueva_cantidad}", size=12, weight=ft.FontWeight.BOLD)
                                control.update()
                                print(f"Producto actualizado visualmente: {producto}, nueva cantidad: {nueva_cantidad}")
                                return
            else:
                print(f"El objeto no tiene controles: {container}")
                
    def cancelar_operacion(self):
        self.dashboard.main_app.menus_disabled = False
        self.dashboard.update()
        print("Operación cancelada. Los módulos están habilitados nuevamente.")
        
    def completar_venta(self):
        self.page.main_app.menus_disabled  = False
        self.page.update()
        print("Venta completada. Los módulos están habilitados nuevamente.")