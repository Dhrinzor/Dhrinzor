import flet as ft
from pages.authentication.utils.ccs import *
from pages.dashboard.Menu.Containers.data_hub import InventoryDB

class Build_Zone_Categorias(ft.Control):
    def __init__(self, page):
        super().__init__()
        self.page = page 
        self.categories = []
        self.db = InventoryDB()
        self.temp_category = ""

    def build_zone_Categorias(self):
        self.insert_row_button = ft.CupertinoButton(
            text="Insertar Categoría",
            on_click=self.add_row,
        )

        self.list_view = ft.ListView(
            controls=[],
            expand=True,
            auto_scroll=False,
        )

        self.container = ft.Container(
            expand=True,
            bgcolor=ft.colors.WHITE10,
            padding=ft.padding.only(left=30, top=30, bottom=45, right=800),
            border_radius=15,
            content=ft.Column(
                controls=[
                    ft.Container(content=ft.Row(controls=[self.insert_row_button])),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                self.build_table_header(),
                                self.list_view,
                            ],
                        ),
                        expand=True,
                        height=600,
                        bgcolor=ft.colors.BLACK12,
                        padding=ft.padding.all(10),
                        border_radius=15,
                    )
                ]
            )
        )
        self.update_categories()
        return self.container

    def build_table_header(self):
        return ft.Row(
            controls=[
                ft.Container(ft.Text("Rango"), width=305),
                ft.Container(ft.Text("Editar"), width=55),
                ft.Container(ft.Text("Eliminar"), width=60),
            ],
            spacing=10,
        )

    def add_row(self, e):
        self.temp_row = {"start_range": "", "end_range": ""}

        fields = [
            ft.TextField(
                label="Rango Inicio",
                on_change=lambda e: self.update_field_temp("start_range", e.control.value),
                keyboard_type=ft.KeyboardType.NUMBER,
            ),
            ft.TextField(
                label="Rango Final",
                on_change=lambda e: self.update_field_temp("end_range", e.control.value),
                keyboard_type=ft.KeyboardType.NUMBER,
            ),
        ]

        self.page.dialog = ft.CupertinoAlertDialog(
            title=ft.Text("Agregar Nueva Categoría"),
            content=ft.Container(
                content=ft.Column(fields),
                padding=ft.padding.all(10),
                width=400,
            ),
            actions=[
                ft.TextButton(text="Insertar", on_click=self.save_new_row),
                ft.TextButton(text="Cancelar", on_click=self.close_dialog),
            ],
        )
        self.page.dialog.open = True
        self.page.update()

    def update_field_temp(self, field, value):
        if field in ["start_range", "end_range"]:
            if not value.isdigit():
                self.show_error_dialog("El rango debe ser un número natural.")
                return
            if len(value) > 6:
                self.show_error_dialog("El rango no debe exceder de 6 caracteres.")
                return

        self.temp_row[field] = value
        self.page.update()

    def update_categories(self):
        self.categories = self.db.get_all_categories_sorted()
        rows = [
            ft.Row(
                controls=[
                    ft.Container(ft.Text(f"{item['start_range']} - {item['end_range']}"), width=300),
                    ft.Container(ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, item=item: self.edit_row(e, item)), width=50),
                    ft.Container(ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, item=item: self.confirm_delete_category(e, item)), width=60),
                ],
                spacing=10,
            ) for item in self.categories
        ]

        self.list_view.controls = rows
        self.page.update()

    def save_new_row(self, e):
        start_range = self.temp_row["start_range"]
        end_range = self.temp_row["end_range"]

        if not isinstance(start_range, str):
            start_range = str(start_range)
            end_range = str(end_range)

        if not start_range.isdigit() or not end_range.isdigit():
            self.show_error_dialog("Ambos rangos deben ser números naturales.")
            return

        if len(start_range) > 6 or len(end_range) > 6:
            self.show_error_dialog("Los rangos no deben exceder de 6 caracteres.")
            return

        start_range = int(start_range)
        end_range = int(end_range)

        if start_range >= end_range:
            self.show_error_dialog("El rango final debe ser mayor que el rango inicial.")
            return

        if self.db.is_category_duplicate(start_range, end_range):
            self.show_error_dialog("Este rango de categoría ya existe. Por favor, elige un rango diferente.")
            return

        self.db.insert_category(start_range, end_range)
        self.update_categories()
        self.page.dialog.open = False
        self.page.update()
        self.close_dialog(None)

    def save_edited_category(self, e, item):
        start_range = self.temp_row["start_range"]
        end_range = self.temp_row["end_range"]

        if not isinstance(start_range, str):
            start_range = str(start_range)
            end_range = str(end_range)

        if not start_range.isdigit() or not end_range.isdigit():
            self.show_error_dialog("Ambos rangos deben ser números naturales.")
            return

        if len(start_range) > 6 or len(end_range) > 6:
            self.show_error_dialog("Los rangos no deben exceder de 6 caracteres.")
            return

        start_range = int(start_range)
        end_range = int(end_range)

        if start_range >= end_range:
            self.show_error_dialog("El rango final debe ser mayor que el rango inicial.")
            return

        try:
            self.db.update_category(item["id"], start_range, end_range)
            self.page.dialog.open = False
            self.update_categories()
        except Exception as error:
            self.show_error_dialog(f"Error al actualizar la categoría: {error}")
        self.page.update()

    def edit_row(self, e, item):
        self.temp_row = {"start_range": item["start_range"], "end_range": item["end_range"]}

        fields = [
            ft.TextField(
                label="Rango Inicio",
                value=str(item["start_range"]),
                on_change=lambda e: self.update_field_temp("start_range", e.control.value),
                keyboard_type=ft.KeyboardType.NUMBER,
            ),
            ft.TextField(
                label="Rango Final",
                value=str(item["end_range"]),
                on_change=lambda e: self.update_field_temp("end_range", e.control.value),
                keyboard_type=ft.KeyboardType.NUMBER,
            ),
        ]

        self.page.dialog = ft.CupertinoAlertDialog(
            title=ft.Text("Editar Categoría"),
            content=ft.Container(
                content=ft.Column(fields),
                padding=ft.padding.all(10),
                width=400,
            ),
            actions=[
                ft.TextButton(text="Guardar", on_click=lambda e: self.save_edited_category(e, item)),
                ft.TextButton(text="Cancelar", on_click=self.close_dialog),
            ],
        )
        self.page.dialog.open = True
        self.page.update()

    def confirm_delete_category(self, e, item):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar Eliminación"),
            content=ft.Text(f"¿Estás seguro de que deseas eliminar la categoría {item['start_range']} - {item['end_range']}? Esta acción no se puede deshacer."),
            actions=[
                ft.TextButton(text="Sí", on_click=lambda e: self.delete_category(item["id"])),
                ft.TextButton(text="No", on_click=self.close_dialog),
            ],
        )
        self.page.dialog.open = True
        self.page.update()

    def delete_category(self, category_id):
        self.db.delete_category(category_id)
        self.update_categories()
        self.page.dialog.open = False
        self.page.update()

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

