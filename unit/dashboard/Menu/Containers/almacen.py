import re
import flet as ft
from pages.authentication.utils.ccs import *
from datetime import datetime
from pages.dashboard.Menu.Containers.data_hub import InventoryDB
from pages.dashboard.Menu.Containers.active_cafe_manager import *  # Asegúrate de que la importación esté en su lugar
#################INVARIABLE#########################################################################################################################

class Build_Zone_Almacen(ft.Control):
    selected_entity_id = None  # Variable de clase para almacenar el ID de la entidad seleccionada
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.data = []  # Crear instancia de los datos de la tabla
        self.db = InventoryDB()  # Crear instancia de InventoryDB
        self.insert_row_button = None  # Inicializar referencia para el botón de "Insertar Fila"
        self.dropdown = None  # Inicializar referencia para el menú desplegable

    def build_zone_almacen(self):
        self.insert_row_button = ft.TextButton(
            text="Insertar Fila",
            on_click=self.choose_row_type,
            icon=ft.icons.ADD_ROUNDED,
            disabled=False
        )

        self.list_view = ft.ListView(
            controls=[],
            expand=True,
            auto_scroll=False,
        )

        self.container = ft.Container(
            bgcolor=ft.colors.WHITE10,
            expand=True,
            padding=ft.padding.only(left=30, top=80, bottom=30, right=30),
            border_radius=15,
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                self.insert_row_button,
                            ]
                        )
                    ),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                self.build_table_header(),
                                self.list_view
                            ],
                        ),
                        expand=True,
                        height=587,
                        bgcolor=ft.colors.BLACK12,
                        padding=ft.padding.only(left=50, right=50, top=20, bottom=20),
                        border_radius=15,
                    )
                ]
            )
        )

        self.update_table()
        return self.container

    def build_table_header(self):
        return ft.Row(
            controls=[
                ft.Container(ft.Text("Producto"), width=350),
                ft.Container(ft.Text("Precio"), width=100),
                ft.Container(ft.Text("Cantidad"), width=100),
                ft.Container(ft.Text("Fecha"), width=100),
                ft.Container(ft.Text("Importe"), width=100),
                ft.Container(ft.Text("Deposito"), width=100),
                ft.Container(ft.Text("Inventario"), width=100),
                ft.Container(ft.Text("Editar"), width=50),
                ft.Container(ft.Text("Eliminar"), width=60),
            ],
            spacing=10,
            #padding=ft.padding.only(bottom=10)
        )

    def build_table(self):
        # if entity_id:
        #     self.data = self.db.get_entity_data(entity_id)
        # else:
        self.data = []  # Inicialmente vacía si no se selecciona ninguna entidad
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(item["Producto"])),
                    ft.DataCell(ft.Text(str(item["Precio"]))),
                    ft.DataCell(ft.Text(str(item["Cantidad"]))),
                    ft.DataCell(ft.Text(item["Fecha"])),
                    ft.DataCell(ft.Text(str(item["Importe"]))),
                    ft.DataCell(ft.Text(str(item["Deposito"]))),
                    ft.DataCell(ft.Text(str(item["Inventario"]))),
                    ft.DataCell(ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, i=i: self.edit_row(i))),
                    ft.DataCell(ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, i=i: self.delete_row(i))),
                ],
            ) for i, item in enumerate(self.data)
        ]

        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Producto")),
                ft.DataColumn(ft.Text("Precio")),
                ft.DataColumn(ft.Text("Cantidad"), numeric=True),
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Importe")),
                ft.DataColumn(ft.Text("Deposito")),
                ft.DataColumn(ft.Text("Inventario")),
                ft.DataColumn(ft.Text("Editar")),
                ft.DataColumn(ft.Text("Eliminar")),
            ],
            rows=rows,
        )

    def load_data_from_db(self):
        self.data = self.db.get_all_almacen()
        self.update_table()

    def choose_row_type(self, e):
        self.page.dialog = ft.CupertinoAlertDialog(
            title=ft.Text("*SELECIONA UN INGRESO*", text_align=ft.TextAlign.CENTER),
            content=ft.Container(
                content=ft.Column([
                    ft.TextButton(text="Producto", on_click=lambda e: self.add_row(e, "Producto")),
                    ft.TextButton(text="Deposito", on_click=lambda e: self.add_row(e, "Deposito")),
                ]),
                padding=ft.padding.all(10),
                width=300,
                height=None,
            ),
            actions=[
                ft.TextButton(text="Cancelar", on_click=self.close_dialog),
            ],
        )
        self.page.dialog.open = True
        self.page.update()
        
    def add_row(self, e, row_type):
        self.temp_row = {"Producto": "", "Precio": 0.0, "Cantidad": 0, "Fecha": datetime.now().strftime("%Y-%m-%d"), "Importe": 0.0, "Deposito": "", "Inventario": 0.0}
        
        self.producto_field = ft.TextField(label="Producto", on_change=lambda e: self.update_field_temp("Producto", e.control.value))
        self.precio_field = ft.TextField(label="Precio", on_change=lambda e: self.update_field_temp("Precio", e.control.value))
        self.cantidad_field = ft.TextField(label="Cantidad", on_change=lambda e: self.update_field_temp("Cantidad", e.control.value))
        self.deposito_field = ft.TextField(label="Deposito", on_change=lambda e: self.update_field_temp("Deposito", e.control.value))

        if row_type == "Producto":
            fields = [self.producto_field, self.precio_field, self.cantidad_field]
        else:
            fields = [self.deposito_field]

        self.page.dialog = ft.CupertinoAlertDialog(
            title=ft.Text(f"*Inserta {row_type}*", text_align=ft.TextAlign.CENTER),
            content=ft.Container(
                content=ft.Column(fields),
                padding=ft.padding.all(10),
                width=400,
                height=None,
            ),
            actions=[
                ft.TextButton(text="Insertar", on_click=lambda e: self.save_new_row(row_type)),
                ft.TextButton(text="Cancelar", on_click=self.close_dialog),
            ],
        )
        self.page.dialog.open = True
        self.page.update()

    def edit_row(self, index):
        self.temp_row = self.data[index].copy()  # Crear una copia temporal de la fila
        row_type = "Producto" if self.temp_row["Producto"] != "DEPÓSITO" else "Deposito"

        fields = [
            ft.TextField(
                label="Producto", 
                value=self.data[index]["Producto"], 
                on_change=lambda e: self.update_field_temp("Producto", e.control.value, index)
            ) if row_type == "Producto" else ft.TextField(
                label="Deposito", 
                value=self.data[index]["Deposito"], 
                on_change=lambda e: self.update_field_temp("Deposito", e.control.value, index)
            ),
            ft.TextField(
                label="Precio", 
                value=self.data[index]["Precio"], 
                on_change=lambda e: self.update_field_temp("Precio", e.control.value, index)
            ) if row_type == "Producto" else None,
            ft.TextField(
                label="Cantidad", 
                value=self.data[index]["Cantidad"], 
                on_change=lambda e: self.update_field_temp("Cantidad", e.control.value, index)
            ) if row_type == "Producto" else None,
        ]

        # Filtrar los controles que no son None
        fields = [field for field in fields if field is not None]

        self.page.dialog = ft.CupertinoAlertDialog(
            title=ft.Text(f"*Modificar {row_type}*", text_align=ft.TextAlign.CENTER),
            content=ft.Container(
                content=ft.Column(
                    controls=fields
                ),
                padding=ft.padding.all(10),
                width=400,
                height=None,
            ),
            actions=[
                ft.TextButton(text="Guardar", on_click=lambda e: self.save_changes(index)),
                ft.TextButton(text="Cancelar", on_click=self.close_dialog),
            ],
        )
        self.page.dialog.open = True
        self.page.update()
  
    #####SAVES FUNTIONS#####################################################################
    def calculate_almacen_fields(self):
        # Calcula los campos del almacén si es necesario
        for item in self.data:
            if item["Importe"] is None:
                item["Importe"] = float(item["Precio"]) * float(item["Cantidad"])
            if item["Inventario"] is None:
                last_inventario = self.data[-1]["Inventario"] if len(self.data) > 1 else 0
                item["Inventario"] = last_inventario + item["Importe"] - item["Deposito"]

    def save_new_row(self, row_type):
        try:
            if row_type == "Producto" and not self.temp_row["Producto"].strip():
                self.show_error_dialog("El nombre del producto no puede estar vacío.")
                return

            # Asegurar que la fecha es un objeto datetime
            if isinstance(self.temp_row["Fecha"], str):
                try:
                    fecha_formateada = datetime.strptime(self.temp_row["Fecha"], '%Y-%m-%d')
                except ValueError:
                    self.show_error_dialog("Formato de fecha inválido. Use el formato YYYY-MM-DD.")
                    return
            else:
                fecha_formateada = self.temp_row["Fecha"]

            fecha_formateada_str = fecha_formateada.strftime('%Y-%m-%d')

            # Verificación y conversión de valores a float
            precio = self.temp_row["Precio"]
            cantidad = self.temp_row["Cantidad"]
            deposito = self.temp_row["Deposito"]

            try:
                precio_float = float(precio) if precio else 0.0
                cantidad_int = int(cantidad) if cantidad else 0
                deposito_float = float(deposito) if deposito else 0.0
            except ValueError as e:
                self.show_error_dialog(f"Error al convertir los valores: {str(e)}")
                return

            if row_type == "Deposito":
                if not self.data:
                    self.show_error_dialog("No puedes agregar un depósito con el inventario vacío.")
                    return
                last_row = self.data[0]
                if "Inventario Almacén" not in last_row:
                    self.show_error_dialog("El último registro no contiene la clave 'Inventario Almacén'.")
                    return
                if deposito_float > float(last_row["Inventario Almacén"]):
                    self.show_error_dialog("El depósito no puede ser mayor que el inventario actual.")
                    return

                self.temp_row["Inventario Almacén"] = float(last_row["Inventario Almacén"]) - deposito_float
                self.temp_row["Producto"] = "DEPÓSITO"

                self.db.insert_almacen_item(
                    producto="DEPÓSITO", 
                    precio_costo=0, 
                    cantidad=0, 
                    fecha=fecha_formateada_str,
                    importe=0, 
                    deposito=deposito_float, 
                    inventario_almacen=self.temp_row["Inventario Almacén"]
                )
            else:
                if self.data:
                    last_row = self.data[0]
                    importe = precio_float * cantidad_int
                    if "Inventario Almacén" not in last_row:
                        self.show_error_dialog("El último registro no contiene la clave 'Inventario Almacén'.")
                        return
                    self.temp_row["Importe"] = importe
                    self.temp_row["Inventario Almacén"] = float(last_row["Inventario Almacén"]) + importe
                else:
                    importe = precio_float * cantidad_int
                    self.temp_row["Importe"] = importe
                    self.temp_row["Inventario Almacén"] = importe

                self.db.insert_almacen_item(
                    producto=self.temp_row["Producto"], 
                    precio_costo=precio_float, 
                    cantidad=cantidad_int, 
                    fecha=fecha_formateada_str,
                    importe=self.temp_row["Importe"], 
                    deposito=deposito_float, 
                    inventario_almacen=self.temp_row["Inventario Almacén"]
                )

            self.data.append(self.temp_row)
            self.update_table()
            self.close_dialog(None)
        except Exception as e:
            self.show_error_dialog(f"Error al insertar datos: {str(e)}")
        finally:
            self.page.update()

    def save_changes(self, index):
        if index < 0 or index >= len(self.data):
            self.show_error_dialog(f"Index {index} fuera de rango para 'self.data' con tamaño {len(self.data)}.")
            return

        self.update_inventory_from(0)

        start_index = 0
        ultima_fila = len(self.data) - 1
        for i in range(start_index, len(self.data)):
            row = self.data[ultima_fila]
            self.db.update_almacen_item(
                id=row["id"], 
                producto=row["Producto"], 
                precio_costo=row["Precio"], 
                cantidad=row["Cantidad"], 
                fecha=row["Fecha"], 
                importe=row["Importe"], 
                deposito=row["Deposito"], 
                inventario_almacen=row["Inventario Almacén"]
            )
            ultima_fila -= 1

        self.page.dialog.open = False
        self.update_table()
        self.page.update()
        self.close_dialog(None)
   
    #########UPDATE FUNTIONS#################################################################
    # def update_field_temp(self, field, value, index=None):            
    #     if field == "Producto" and not re.match(r"^[a-z A-Z]+$", value):
    #         self.show_error_dialog("Producto solo puede contener letras desde A hasta Z.")
    #         return
    #     elif field == "Precio" and not re.match(r"^\d*\.?\d*$", value):
    #         self.show_error_dialog("El Precio solo puede contener números y un punto.")
    #         return
    #     elif field == "Cantidad" and not re.match(r"^\d+$", value):
    #         self.show_error_dialog("La Cantidad solo puede ser un número natural.")
    #         return
    #     elif field == "Deposito" and not re.match(r"^\d*\.?\d*$", value):
    #         self.show_error_dialog("El Deposito solo puede contener números y un punto.")
    #         return

    #     if index is not None:
    #         if index < len(self.data):
    #             self.data[index][field] = value.upper() if field == "Producto" else value
    #         else:
    #             self.show_error_dialog(f"Index {index} fuera de rango para 'self.data' con tamaño {len(self.data)}.")
    #     else:
    #         self.temp_row[field] = value.upper() if field == "Producto" else value
    def update_field_temp(self, field, value, index=None):            
        if field == "Producto" and not re.match(r"^[a-z A-Z]+$", value):
            self.producto_field.error_text = "Solo letras desde A - Z."
            self.producto_field.update()
            return
        elif field == "Precio" and not re.match(r"^\d*\.?\d*$", value):
            self.precio_field.error_text = "Solo datos numéricos enteros."
            self.precio_field.update()
            return
        elif field == "Cantidad" and not re.match(r"^\d+$", value):
            self.cantidad_field.error_text = "Solo datos numéricos naturales."
            self.cantidad_field.update()
            return
        elif field == "Deposito" and not re.match(r"^\d*\.?\d*$", value):
            self.deposito_field.error_text = "Solo datos numéricos enteros."
            self.deposito_field.update()
            return

        # Limpiar el texto de error si todas las validaciones son correctas
        if field == "Producto":
            self.producto_field.error_text = ""
            self.producto_field.update()
        elif field == "Precio":
            self.precio_field.error_text = ""
            self.precio_field.update()
        elif field == "Cantidad":
            self.cantidad_field.error_text = ""
            self.cantidad_field.update()
        elif field == "Deposito":
            self.deposito_field.error_text = ""
            self.deposito_field.update()

        if index is not None:
            if index < len(self.data):
                self.data[index][field] = value.upper() if field == "Producto" else value
            else:
                self.show_error_dialog(f"Index {index} fuera de rango para 'self.data' con tamaño {len(self.data)}.")
        else:
            self.temp_row[field] = value.upper() if field == "Producto" else value

    def update_inventory_from(self, start_index=0):
        if start_index < 0 or start_index >= len(self.data):
            return

        for i in range(len(self.data) - 1, -1, -1):
            precio = float(self.data[i]["Precio"]) if self.data[i]["Precio"] else 0.0
            cantidad = float(self.data[i]["Cantidad"]) if self.data[i]["Cantidad"] else 0
            deposito = float(self.data[i]["Deposito"]) if self.data[i]["Deposito"] else 0.0

            importe = precio * cantidad
            self.data[i]["Importe"] = importe
            if i == len(self.data) - 1:
                self.data[i]["Inventario Almacén"] = importe - deposito
            else:
                next_row = self.data[i + 1]
                inventario = float(next_row["Inventario Almacén"]) + importe - deposito
                self.data[i]["Inventario Almacén"] = max(inventario, 0)

            row_id = self.data[i]["id"]
            self.db.update_almacen_item(
                id=row_id, 
                producto=self.data[i]["Producto"], 
                precio_costo=self.data[i]["Precio"], 
                cantidad=self.data[i]["Cantidad"], 
                fecha=self.data[i]["Fecha"], 
                importe=self.data[i]["Importe"], 
                deposito=self.data[i]["Deposito"], 
                inventario_almacen=self.data[i]["Inventario Almacén"]
            )

        self.update_table()

    def update_table(self):
        self.data = self.db.get_all_almacen()
        if not self.data:
            return

        self.data.sort(key=lambda x: x["id"], reverse=True)  # Ordenar por id en orden descendente
        rows = [
            ft.Row(
                controls=[
                    ft.Container(ft.Text(item["Producto"]), width=350),
                    ft.Container(ft.Text(str(item["Precio"])), width=100),
                    ft.Container(ft.Text(str(item["Cantidad"])), width=100),
                    ft.Container(ft.Text(item["Fecha"]), width=100),
                    ft.Container(ft.Text(str(item["Importe"])), width=100),
                    ft.Container(ft.Text(str(item["Deposito"])), width=100),
                    ft.Container(ft.Text(str(item["Inventario Almacén"])), width=100),
                    ft.Container(ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, i=i: self.edit_row(i)), width=50),
                    ft.Container(ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, i=i: self.delete_row(i)), width=60),
                ]
            ) for i, item in enumerate(self.data)
        ]
        self.list_view.controls = rows
        if self.list_view.page:
            self.list_view.update()
        self.page.update()

   ##########DELETE FUNTIONS##################################################################
    def delete_row(self, index):
        self.show_confirm_delete_dialog(index)
    
   ##########CONFIRM FUNTIONS ########################################################### 
    def show_confirm_delete_dialog(self, index):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Confirm Delete"),
            content=ft.Text("¿Estás seguro de que deseas eliminar esta fila?"),
            actions=[
                ft.TextButton(text="Yes", on_click=lambda e: self.confirm_delete_row(index)),
                ft.TextButton(text="No", on_click=self.close_dialog),
            ],
        )
        self.page.dialog.open = True
        self.page.update()

    def confirm_delete_row(self, index):
        try:
            row_id = self.data[index]["id"]
            self.db.delete_almacen_item(row_id)
            self.data.pop(index)
            self.update_table()
            self.close_dialog(None)
        except Exception as e:
            self.show_error_dialog(f"Error al eliminar datos: {str(e)}")

   ##########DIALOG FUNTIONS DIALOG###########################################################   
    def show_error_dialog(self, message):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[
                ft.TextButton(text="OK", on_click=self.close_dialog),
            ],
        )
        self.page.dialog.open = True
        self.page.update()
    
    def close_dialog(self, e):
        self.page.dialog.open = False
        self.page.update()
  
 
