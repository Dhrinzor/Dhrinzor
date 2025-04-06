import flet as ft
import time
import shutil
import os
from pages.authentication.utils.ccs import *
from pages.authentication.utils.user import UserDB

class Build_Zone_Configuracion(ft.Control):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.db = UserDB()
        self.current_password = ft.TextField(label="Contraseña Actual", password=True, can_reveal_password=True)
        self.new_password = ft.TextField(label="Nueva Contraseña", password=True, can_reveal_password=True)
        self.confirm_new_password = ft.TextField(label="Confirmar Nueva Contraseña", password=True, can_reveal_password=True)
        self.db_path = "DB/data_hub.db"  # Actualiza con la ruta a tu base de datos
        self.backup_dir = os.path.join(os.path.expanduser("~"), "Backups")  # Directorio de respaldo en el directorio del usuario actual

        self.version = self.leer_version_desde_archivo()  # Leer la versión desde el archivo
    
    def leer_version_desde_archivo(self):
        try:
            with open("key.txt", "r") as file:
                for line in file:
                    if "Version:" in line:
                        return line.split(":")[1].strip()
        except FileNotFoundError:
            return "Unknown"  # Devolver una versión por defecto si el archivo no se encuentra
        
    def actualizar_version(self, nueva_version):
        self.version = nueva_version
        self.page.update()  # Actualiza la página para reflejar la nueva versión
        
    def build_zone_configuracion(self):
        return ft.Container(
            bgcolor=ft.colors.WHITE10,
            expand=True,
            padding=ft.padding.only(left=30, top=80, bottom=72, right=30),
            border_radius=15,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Configuración", size=30, weight=ft.FontWeight.BOLD),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text("Acerca de la Aplicación", size=20, weight=ft.FontWeight.BOLD),
                                        ft.Row(
                                            controls=[
                                                ft.Text(f"Versión: {self.version}      ", size=15, weight=ft.FontWeight.BOLD),
                                                ft.PopupMenuButton(
                                                    content=ft.Text("Opciones", size=15, weight=ft.FontWeight.BOLD),
                                                    items=[
                                                        ft.PopupMenuItem(text="Soporte Técnico", icon=ft.icons.HELP, on_click=self.soporte_tecnico),
                                                        ft.PopupMenuItem(text="Política de Privacidad", icon=ft.icons.PRIVACY_TIP, on_click=self.politica_privacidad),
                                                        ft.PopupMenuItem(text="Términos de Servicio", icon=ft.icons.DESCRIPTION, on_click=self.terminos_servicio),
                                                    ]
                                                ),
                                            ],
                                            spacing=10
                                        )
                                    ]
                                ),
                                margin=ft.margin.only(left=100)
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    
                    ft.Divider(height=20, thickness=1),

                    ft.Text("Gestión de Usuarios", size=20, weight=ft.FontWeight.BOLD),
                    ft.TextButton("Añadir Usuario", icon=ft.icons.PERSON_ADD, on_click=self.anadir_usuario),
                    ft.TextButton("Editar Usuario", icon=ft.icons.EDIT, on_click=self.editar_usuario),

                    ft.Divider(height=20, thickness=1),

                    ft.Text("Seguridad", size=20, weight=ft.FontWeight.BOLD),
                    ft.TextButton("Cambiar Contraseña", icon=ft.icons.LOCK, on_click=self.mostrar_usuarios),

                    ft.Divider(height=20, thickness=1),

                    ft.Text("Respaldo y Restauración", size=20, weight=ft.FontWeight.BOLD),
                    ft.TextButton("Realizar Respaldo", icon=ft.icons.BACKUP, on_click=self.realizar_respaldo),
                    ft.TextButton("Restaurar Respaldo", icon=ft.icons.RESTORE, on_click=self.restaurar_respaldo),
                    
                    ft.Divider(height=20, thickness=1),

                    ft.Text("Actualizar Aplicación", size=20, weight=ft.FontWeight.BOLD),
                    ft.TextButton("Buscar Actualizaciones", icon=ft.icons.REFRESH_OUTLINED, on_click=self.actualizar_app),
                ]
            )
        )

###########################################################
    def soporte_tecnico(self, e):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Soporte Técnico"),
            content=ft.Text("Para soporte técnico, contacte a dhrinzorcorporation@gmail.com"),
            actions=[
                ft.TextButton("Cerrar", on_click=self.cerrar_dialog)
            ]
        )
        self.page.dialog.open = True
        self.page.update()

    def politica_privacidad(self, e):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Política de Privacidad"),
            content=ft.Text("Nuestra política de privacidad está disponible en el siguiente enlace: [Política de Privacidad](https://ejemplo.com/politica)"),
            actions=[
                ft.TextButton("Cerrar", on_click=self.cerrar_dialog)
            ]
        )
        self.page.dialog.open = True
        self.page.update()

    def terminos_servicio(self, e):
        try:
            with open("License.txt", "r", encoding="utf-8") as file:  # Especificar el conjunto de caracteres UTF-8
                license_content = file.read()
        except FileNotFoundError:
            license_content = "El archivo License.txt no se encuentra en la raíz del proyecto."
        except UnicodeDecodeError:
            license_content = "Error al leer el contenido del archivo License.txt debido a problemas de decodificación."

        scrollable_content = ft.Column(
            controls=[
                ft.Text(license_content),
            ],
            scroll=ft.ScrollMode.ALWAYS  # Habilitar el desplazamiento siempre
        )

        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Términos de Servicio"),
            content=ft.Container(
                content=scrollable_content,
                width=500,  # Ajusta el ancho según sea necesario
                height=400,  # Ajusta la altura según sea necesario
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=self.cerrar_dialog)
            ],
            modal=True  # Asegura que el dialogo sea modal
        )
        self.page.dialog.open = True
        self.page.update()

##########################################################
    def mostrar_usuarios(self, e):
        usuarios = self.db.get_password_user()
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(usuario["Enombre"])),
                    ft.DataCell(ft.TextButton("Cambiar Contraseña", on_click=lambda _, u=usuario: self.cambiar_contrasena(u))),
                ]
            )
            for usuario in usuarios
        ]
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Acción")),
            ],
            rows=rows,
        )
        
        # Envolver la tabla en una columna con scroll
        scrollable_content = ft.Column(
            controls=[table],
            width=350,  # Ajusta el ancho según sea necesario
            height=300,  # Ajusta la altura para activar el scroll
            scroll=ft.ScrollMode.AUTO
        )
        
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Usuarios"),
            content=scrollable_content,
            actions=[ft.TextButton("Cerrar", on_click=self.cerrar_dialog)],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog.open = True
        self.page.update()

    def cambiar_contrasena(self, usuario):
        self.new_password = ft.TextField(label="Nueva Contraseña", password=True, can_reveal_password=True, width=300)
        self.confirm_new_password = ft.TextField(label="Confirmar Nueva Contraseña", password=True, can_reveal_password=True, width=300)
        
        self.dialog = ft.AlertDialog(
            title=ft.Text("Cambiar Contraseña"),
            content=ft.Column(
                controls=[
                    self.new_password,
                    self.confirm_new_password,
                ],
                tight=True  # Ajusta el tamaño del contenido
            ),
            actions=[
                ft.TextButton("Guardar", on_click=lambda _: self.guardar_contrasena(usuario["Eusuario"])),
                ft.TextButton("Cancelar", on_click=self.cerrar_dialog)
            ],
        )
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def guardar_contrasena(self, usuario):
        new_password = self.new_password.value
        confirm_new_password = self.confirm_new_password.value

        if new_password != confirm_new_password:
            self.confirm_new_password.error_text = "Las contraseñas nuevas no coinciden."
            self.page.update()
            return

        if len(new_password) < 6:
            self.new_password.error_text = "Contraseña débil: menor a 6 caracteres."
            self.page.update()
            return

        if not any(char.isupper() for char in new_password):
            self.new_password.error_text = "Debe contener al menos una letra mayúscula."
            self.page.update()
            return

        if not any(char in '!#$%&()*+,-./:;<=>?@[\\]^_`{|}~' for char in new_password):
            self.new_password.error_text = "Debe contener caracteres especiales."
            self.page.update()
            return

        self.db.update_password(usuario, new_password)

        self.page.dialog.open = False
        self.page.update()
        self.show_alert_dialog("Éxito", "La contraseña ha sido cambiada con éxito.")

    def show_alert_dialog(self, title, message):
        dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(message),
            actions=[
                ft.TextButton("Aceptar", on_click=self.cerrar_dialog)
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def clear_fields(self):
        self.current_password.value = ""
        self.new_password.value = ""
        self.confirm_new_password.value = ""
        self.current_password.error_text = None
        self.new_password.error_text = None
        self.confirm_new_password.error_text = None
        self.page.update()

###########################################################
    def realizar_respaldo(self, e):
        try:
            # Crear el directorio de respaldo si no existe
            os.makedirs(self.backup_dir, exist_ok=True)
            
            # Ruta completa para el archivo de respaldo
            backup_path = os.path.join(self.backup_dir, "database_backup.sqlite")
            
            # Copiar la base de datos al directorio de respaldo
            shutil.copy2(self.db_path, backup_path)
            
            self.page.dialog = ft.AlertDialog(
                title=ft.Text("Respaldo"),
                content=ft.Text(f"El respaldo se ha realizado con éxito en {backup_path}."),
                actions=[
                    ft.TextButton("Aceptar", on_click=self.cerrar_dialog)
                ]
            )
            self.page.dialog.open = True
            self.page.update()
        except Exception as ex:
            self.page.dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text(f"Hubo un error al realizar el respaldo: {str(ex)}"),
                actions=[
                    ft.TextButton("Aceptar", on_click=self.cerrar_dialog)
                ]
            )
            self.page.dialog.open = True
            self.page.update()

    def restaurar_respaldo(self, e):
        try:
            # Ruta completa para el archivo de respaldo
            backup_path = os.path.join(self.backup_dir, "database_backup.sqlite")
            
            # Verificar que el archivo de respaldo existe
            if not os.path.exists(backup_path):
                raise FileNotFoundError(f"No se encontró el archivo de respaldo en: {backup_path}")
            
            # Copiar el archivo de respaldo de vuelta a la ubicación original de la base de datos
            shutil.copy2(backup_path, self.db_path)
            
            self.page.dialog = ft.AlertDialog(
                title=ft.Text("Restaurar Respaldo"),
                content=ft.Text("La restauración del respaldo se ha realizado con éxito."),
                actions=[
                    ft.TextButton("Aceptar", on_click=self.cerrar_dialog)
                ]
            )
            self.page.dialog.open = True
            self.page.update()
        except Exception as ex:
            self.page.dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text(f"Hubo un error al restaurar el respaldo: {str(ex)}"),
                actions=[
                    ft.TextButton("Aceptar", on_click=self.cerrar_dialog)
                ]
            )
            self.page.dialog.open = True
            self.page.update()

##########################################################
    def anadir_usuario(self, e):
        establecimientos = self.db.get_establecimientos()
        establecimiento_options = [ft.dropdown.Option(text=est) for est in establecimientos]
        roles = ["Administrador", "Dependiente"]
        
        rol_dropdown = ft.Dropdown(
            label="Rol",
            options=[ft.dropdown.Option(text=role) for role in roles],
            width=300,
            on_change=self.on_rol_change_user
        )
        
        self.dialog_content = ft.Column(
            tight=True,  # Ajusta el tamaño del contenido
            controls=[
                ft.TextField(label="Nombre", width=300),
                ft.TextField(label="Usuario", width=300),
                ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300),
                rol_dropdown,
                ft.Dropdown(label="Establecimiento", options=establecimiento_options, width=300, disabled=True),
                ft.TextField(label="Teléfono", width=300),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        dialog = ft.AlertDialog(
            title=ft.Text("Añadir Usuario"),
            content=self.dialog_content,
            actions=[
                ft.TextButton("Guardar", on_click=self.guardar_usuario),
                ft.TextButton("Cancelar", on_click=self.cerrar_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def on_rol_change_user(self, e):
        rol = e.control.value
        establecimiento_dropdown = self.dialog_content.controls[4]
        establecimiento_dropdown.disabled = (rol == "Administrador")
        self.page.update()

    def guardar_usuario(self, e):
        nombre = self.dialog_content.controls[0].value.upper()
        usuario = self.dialog_content.controls[1].value
        contrasena = self.dialog_content.controls[2].value
        rol = self.dialog_content.controls[3].value
        establecimiento = self.dialog_content.controls[4].value
        telefono = self.dialog_content.controls[5].value

        if not all([nombre, usuario, contrasena, rol, telefono]):
            self.page.dialog.content.controls.append(ft.Text("Todos los campos son obligatorios.", color=ft.colors.RED))
            self.page.update()
            return
        
        if len(telefono) != 8 or not telefono.startswith(('5', '6')) or not telefono.isdigit():
            self.page.dialog.content.controls.append(ft.Text("El teléfono debe ser un número de 8 dígitos y empezar por 5 o 6.", color=ft.colors.RED))
            self.page.update()
            return
        
        if len(contrasena) < 6 or not any(c.isupper() for c in contrasena) or not any(c in "!@#$%^&*().,-_=+[]" for c in contrasena):
            self.page.dialog.content.controls.append(ft.Text("La contraseña debe tener al menos 6 caracteres, una mayúscula y un carácter especial o un signo de puntuación.", color=ft.colors.RED))
            self.page.update()
            return
        
        if self.db.user_exists(usuario):
            self.page.dialog.content.controls.append(ft.Text("El usuario ya existe. Por favor, elija otro nombre de usuario.", color=ft.colors.RED))
            self.page.update()
            return
        
        self.db.add_user(nombre, usuario, contrasena, rol, establecimiento, telefono)
        
        self.page.dialog.open = False
        self.page.update()
        dialog = ft.AlertDialog(
            title=ft.Text("Éxito"),
            content=ft.Text("El usuario ha sido guardado con éxito."),
            actions=[
                ft.TextButton("Aceptar", on_click=self.cerrar_dialog)
            ]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    ######################################################
    def editar_usuario(self, e):
        usuarios = self.db.get_usuarios()
        rows = [
            ft.DataRow(
                cells=[
                    #ft.DataCell(ft.Text(usuario["id"])),
                    ft.DataCell(ft.Text(usuario["Enombre"])),
                    ft.DataCell(ft.Text(usuario["Eusuario"])),
                    ft.DataCell(ft.Text(usuario["rol"])),
                    ft.DataCell(ft.TextButton("Editar", on_click=lambda _, u=usuario: self.cargar_usuario(u))),
                    ft.DataCell(ft.TextButton("Eliminar", on_click=lambda _, u=usuario: self.eliminar_usuario(u))),
                ]
            )
            for usuario in usuarios
        ]
        table = ft.DataTable(
            columns=[
                #ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Usuario")),
                ft.DataColumn(ft.Text("Rol")),
                ft.DataColumn(ft.Text("Acción")),
                ft.DataColumn(ft.Text("Eliminar")),
            ],
            rows=rows,
        )
        
        # Envolver la tabla en una columna con scroll
        scrollable_content = ft.Column(
            controls=[table],
            width=650,  # Ajusta el ancho según sea necesario
            height=300,  # Ajusta la altura para activar el scroll
            scroll=ft.ScrollMode.AUTO
        )
        
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Seleccionar Usuario para Editar o Eliminar"),
            content=scrollable_content,
            actions=[ft.TextButton("Cancelar", on_click=self.cerrar_dialog)],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog.open = True
        self.page.update()

    def eliminar_usuario(self, usuario):
        confirm_dialog = ft.AlertDialog(
            title=ft.Text("Confirmación"),
            content=ft.Text("¿Estás seguro que deseas eliminar este usuario? Esta acción no se puede deshacer."),
            actions=[
                ft.TextButton("Eliminar", on_click=lambda _: self.confirmar_eliminar_usuario(usuario["id"])),
                ft.TextButton("Cancelar", on_click=self.cerrar_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = confirm_dialog
        confirm_dialog.open = True
        self.page.update()

    def confirmar_eliminar_usuario(self, id_usuario):
        self.db.delete_user(id_usuario)
        
        self.page.dialog.open = False
        self.page.update()
        dialog = ft.AlertDialog(
            title=ft.Text("Éxito"),
            content=ft.Text("El usuario ha sido eliminado con éxito."),
            actions=[
                ft.TextButton("Aceptar", on_click=self.cerrar_dialog)
            ]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def cargar_usuario(self, usuario):
        establecimientos = self.db.get_establecimientos()
        establecimiento_options = [ft.dropdown.Option(text=est) for est in establecimientos]
        
        rol_dropdown = ft.Dropdown(
            label="Rol", 
            options=[
                ft.dropdown.Option(text="Administrador"), 
                ft.dropdown.Option(text="Dependiente")
            ],
            value=usuario["rol"],
            width=300,
            on_change=self.on_rol_change
        )
        
        self.dialog_content = ft.Column(tight=True,  # Ajusta el tamaño del contenido
            controls=[
                ft.TextField(label="Nombre", value=usuario["Enombre"], width=300),
                ft.TextField(label="Usuario", value=usuario["Eusuario"], width=300),
                rol_dropdown,
                ft.Dropdown(label="Establecimiento", options=establecimiento_options, value=usuario.get("establecimiento", ""), width=300, disabled=(usuario["rol"] == "Administrador")),
                ft.TextField(label="Teléfono", value=usuario["telefono"], width=300),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        dialog = ft.AlertDialog(
            title=ft.Text("Editar Usuario"),
            content=self.dialog_content,
            actions=[
                ft.TextButton("Guardar", on_click=lambda _: self.guardar_cambios_usuario(usuario["id"])),
                ft.TextButton("Cancelar", on_click=self.cerrar_dialog)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def on_rol_change(self, e):
        rol = e.control.value
        self.dialog_content.controls[3].disabled = (rol == "Administrador")
        self.page.update()

    def guardar_cambios_usuario(self, id_usuario):
        nombre = self.dialog_content.controls[0].value
        usuario = self.dialog_content.controls[1].value
        rol = self.dialog_content.controls[2].value
        establecimiento = self.dialog_content.controls[3].value if rol == "Dependiente" else ""
        telefono = self.dialog_content.controls[4].value

        if not all([nombre, usuario, rol, telefono]):
            self.page.dialog.content.controls.append(ft.Text("Todos los campos son obligatorios.", color=ft.colors.RED))
            self.page.update()
            return

        if len(telefono) != 8 or not telefono.startswith(('5', '6')) or not telefono.isdigit():
            self.page.dialog.content.controls.append(ft.Text("El teléfono debe ser un número de 8 dígitos y empezar por 5 o 6.", color=ft.colors.RED))
            self.page.update()
            return

        self.db.update_user(id_usuario, nombre, usuario, rol, establecimiento, telefono)
        
        self.page.dialog.open = False
        self.page.update()
        dialog = ft.AlertDialog(
            title=ft.Text("Éxito"),
            content=ft.Text("El usuario ha sido actualizado con éxito."),
            actions=[
                ft.TextButton("Aceptar", on_click=self.cerrar_dialog)
            ]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

##########################################################
    def actualizar_app(self, e):
        # Mostrar ProgressRing durante la búsqueda de actualizaciones
        progress_ring = ft.ProgressRing(width=30, height=30, stroke_width=4)
        mensaje = ft.Text("Buscando actualizaciones")

        # Mostrar el diálogo de progreso
        self.page.dialog = ft.AlertDialog(
            modal=True,
            bgcolor=None,  # Fondo transparente
            content=ft.Container(
                ft.Column(
                    [
                        progress_ring,
                        mensaje
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    tight=True,
                ),
                padding=2,
                bgcolor=None,  # Fondo transparente para el contenedor
            ),
        )
        self.page.dialog.open = True
        self.page.update()

        dots = ""
        progress_count = 0
        for i in range(0, 31):
            # Actualizar progreso
            progress_ring.value = progress_count * 0.0333  # Incremento del progreso
            time.sleep(0.1)  # Esperar 0.1 segundos para el progreso
            progress_count += 1

            # Actualizar puntos suspensivos cada 0.3 segundos
            if i % 5 == 0:
                if len(dots) < 3:
                    dots += "."
                else:
                    dots = ""
                mensaje.value = f"Buscando actualizaciones{dots:<3}"  # Alinear los puntos
            self.page.update()

        # Actualizar el mensaje final
        mensaje.value = "No se encontraron actualizaciones."
        self.page.update()

        # Cerrar el diálogo después de 1 segundos
        time.sleep(1)
        self.page.dialog.open = False
        self.page.update()

    def cerrar_dialog(self, e):
        self.page.dialog.open = False
        self.page.update()









