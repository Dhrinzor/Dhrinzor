import os
import shutil
import time
import flet as ft
from DB.DB_Negocio import DBNegocio  # Importar la gestión de la base de datos
from DB.DB_Local_Independiente import DBLocalIndependiente  # Importar la gestión de la base de datos
from DB.DB_Local import DBLocal  # Importar la gestión de la base de datos

class PageContent:
    def __init__(self, page, navigate_to, app):
        self.page = page
        self.navigate_to = navigate_to
        self.app = app  # Referencia al objeto principal (`InstallPage`)
        self.selected_mode = None  # Variable para almacenar el modo seleccionado

    def install_process(self):
        # Verificar que se haya seleccionado un modo
        if not self.selected_mode:
            error_message.value = "Debe seleccionar un modo para continuar."
            error_message.visible = True
            self.page.update()
            return

        # Deshabilitar los radio botones para evitar cambios adicionales
        for radio in mode_selector.content.controls:
            radio.disabled = True
            radio.label_style = ft.TextStyle(color=ft.colors.BLACK)  # Mantener el texto negro
        mode_selector.update()  # Actualizar para reflejar el estado visual

        # Ruta para las carpetas de destino
        magiccorp_path = os.path.join("C:\\", "MagicCorp")
        db_dest_path = os.path.join(magiccorp_path, "DB")

        try:
            # Inicializar variables de progreso
            total_steps = 10  # Número total de pasos en el flujo
            current_step = 0

            def update_progress(message, add_to_list=True):
                """Actualiza la barra de progreso y añade ítems al ListView con pausas controladas."""
                nonlocal current_step
                current_step += 1
                pb.value = current_step / total_steps
                if add_to_list:
                    file_list.controls.append(ft.Text(message))
                self.page.update()
                time.sleep(0.2)  # Pausa más breve para acelerar pero mantener visualización en tiempo real

            # # Crear carpetas necesarias
            # if not os.path.exists(magiccorp_path):
            #     os.mkdir(magiccorp_path)
            #     update_progress("Creando carpeta principal MagicCorp...")

            # if not os.path.exists(db_dest_path):
            #     os.mkdir(db_dest_path)
            #     update_progress("Creando carpeta de bases de datos...")

            # Copiar archivos
            files_to_copy = ["license.txt", "sync_version.bat", "version.txt", "test.txt", "README.md", "install.nsi", "requirements.txt"]
            for file_name in files_to_copy:
                source_path = os.path.join(os.getcwd(), file_name)
                destination_path = os.path.join(magiccorp_path, file_name)

                if not os.path.exists(source_path):
                    pb.value = 0
                    pb.color = ft.colors.RED
                    success_message.value += f"Error: No se encontró el archivo '{file_name}'\n"
                    self.page.update()
                    raise FileNotFoundError(f"No se encontró el archivo '{file_name}' en la raíz local.")

                shutil.copy(source_path, destination_path)
                update_progress(f"Archivo copiado: {file_name}")

            # Copiar carpeta src
            src_path = os.path.join(os.getcwd(), "src")
            destination_src_path = os.path.join(magiccorp_path, "src")

            if not os.path.exists(src_path):
                pb.value = 0
                pb.color = ft.colors.RED
                success_message.value += "Error: No se encontró la carpeta 'src'\n"
                self.page.update()
                raise FileNotFoundError("No se encontró la carpeta 'src' en la raíz local.")

            shutil.copytree(src_path, destination_src_path, dirs_exist_ok=True)
            update_progress("Carpetas copiada con éxito.")

            # Leer el nombre del negocio desde key.txt
            key_file_path = os.path.join(magiccorp_path, "key.txt")
            if not os.path.exists(key_file_path):
                pb.value = 0
                pb.color = ft.colors.RED
                success_message.value += "Error: No se encontró el archivo key.txt\n"
                self.page.update()
                raise FileNotFoundError(f"No se encontró el archivo key.txt en {magiccorp_path}.")
            
            version_file_path = os.path.join(os.getcwd(), "version.txt")
            if not os.path.exists(version_file_path):
                pb.value = 0
                pb.color = ft.colors.RED
                success_message.value += "Error: No se encontró el archivo version.txt\n"
                self.page.update()
                raise FileNotFoundError("No se encontró el archivo version.txt en la raíz local.")

            # Leer la versión desde version.txt
            with open(version_file_path, "r", encoding="utf-8") as version_file:
                version = version_file.read().strip()

            # Actualizar el archivo key.txt
            with open(key_file_path, "r+", encoding="utf-8") as key_file:
                content = key_file.readlines()
                for i, line in enumerate(content):
                    if "Versión:" in line:
                        content[i] = f"   Versión: {version}\n"
                    if "Tipo de instalación:" in line:
                        content[i] = f"   Tipo de instalación: {self.selected_mode}\n"
                key_file.seek(0)
                key_file.writelines(content)
                key_file.truncate()

            update_progress("Archivo key.txt actualizado con éxito.")
            business_name = None
            with open(key_file_path, "r", encoding="utf-8") as key_file:
                for line in key_file:
                    if "Negocio:" in line:
                        business_name = line.split(":")[1].strip()
                        break

            if not business_name:
                pb.value = 0
                success_message.value += "Error: No se encontró el nombre del negocio en key.txt\n"
                self.page.update()
                raise ValueError("El archivo 'key.txt' no contiene un nombre válido para el negocio.")

            business_db_path = os.path.join(db_dest_path, f"DB_{business_name}.db")

            if not os.path.exists(business_db_path):
                raise FileNotFoundError(f"No se encontró el archivo de base de datos: {business_db_path}")

            # Configurar las tablas según el modo seleccionado
            if self.selected_mode == "Local":
                update_progress("Base de Datos para el modo 'Local'configurada con exito.")
                db_local = DBLocal(business_name)
                db_local.create_tables()
            elif self.selected_mode == "Negocio":
                update_progress("Base de Datos para el modo 'Negocio' configurada con exito.")
                db_negocio = DBNegocio(business_db_path)
                db_negocio.setup_negocio_tables()
            elif self.selected_mode == "Local Independiente":
                update_progress("Base de Datos para el modo 'Local Independiente'configurada con exito.")
                db_local_independiente = DBLocalIndependiente(business_name)
                db_local_independiente.setup_local_independent_tables()
            else:
                raise ValueError(f"Modo seleccionado '{self.selected_mode}' no válido.")

            pb.value = 1.0  # Progreso completo
            pb.color = ft.colors.GREEN
            update_progress("¡Instalación completada exitosamente!", add_to_list=False)

            # Mostrar mensaje final en success_message
            success_message.value = "¡La instalación se realizó con éxito!"
            success_message.visible = True
            error_message.visible = False
            install_button.visible = False
            continue_button.visible = True
            self.page.update()

        except Exception as e:
            pb.value = 0
            pb.color = ft.colors.RED
            success_message.value += "Error durante la instalación. Revise los detalles.\n"
            self.page.update()
            error_message.value = f"Error: {str(e)}"
            error_message.visible = True
            success_message.visible = False
            install_button.visible = True
            continue_button.visible = False
            self.page.update()
              
    def proceed_to_next(self):
        # Actualizar el checkbox correspondiente en `InstallPage`
        if hasattr(self.app, "_update_checkboxes"):
            self.app._update_checkboxes("Install_tools")  # Actualizar checkbox correspondiente
        else:
            print("Error: No se pudo actualizar el checkbox.")

        # Navegar al siguiente módulo
        self.navigate_to("unit.installers.Performance")

    def select_mode(self, e):
        self.selected_mode = e.control.value
        print(f"Modo seleccionado: {self.selected_mode}")

    def show(self):
        # Barra de progreso inicial con bordes ovalados
        global pb, success_message, error_message, install_button, continue_button, mode_selector, file_list
        pb = ft.ProgressBar(
            width=500,
            height=15,
            value=0,
            bgcolor=ft.colors.GREY_300,
            color=ft.colors.GREEN,
            border_radius=10  # Bordes redondeados para apariencia ovalada
        )

        # Mensajes dinámicos
        success_message = ft.Text(value="", color=ft.colors.GREEN, visible=False)
        error_message = ft.Text(value="", color=ft.colors.RED, visible=False)

        # Botón único para instalar
        install_button = ft.ElevatedButton(
            text="Instalar",
            on_click=lambda _: self.install_process(),
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE,
            icon=ft.icons.DOWNLOAD,  # Icono más profesional
        )

        # Botón para continuar (inicialmente invisible)
        continue_button = ft.ElevatedButton(
            text="Continuar",
            on_click=lambda _: self.proceed_to_next(),
            bgcolor=ft.colors.BLUE,
            color=ft.colors.WHITE,
            visible=False,  # Oculto al inicio
        )

        # Elemento descriptivo
        description_text = ft.Text(
            "Seleccione el modo de instalación y presione 'Instalar' para comenzar.",
            size=16,
            color=ft.colors.BLACK,
            text_align=ft.TextAlign.CENTER,
        )

        # Radios para seleccionar el modo
        mode_selector = ft.RadioGroup(
            content=ft.Column(
                controls=[
                    ft.Radio(
                        value="Negocio",
                        label="Modo Negocio (Administrador del almacén principal)",
                        label_style=ft.TextStyle(color=ft.colors.BLACK)  # Estilo del texto negro
                    ),
                    ft.Radio(
                        value="Local",
                        label="Modo Local (Gestión de inventario y ventas)",
                        label_style=ft.TextStyle(color=ft.colors.BLACK)  # Estilo del texto negro
                    ),
                    ft.Radio(
                        value="Local Independiente",
                        label="Modo Local Independiente (Gestión de almacen, inventario y ventas)",
                        label_style=ft.TextStyle(color=ft.colors.BLACK)  # Estilo del texto negro
                    ),
                ],
            ),
            on_change=self.select_mode
        )

        # ListView para mostrar los archivos copiados
        file_list = ft.ListView(expand=True, spacing=10, padding=10, auto_scroll=True)

        # Estructura de la página
        return ft.Container(
            bgcolor=ft.colors.WHITE,
            expand=True,
            padding=ft.padding.all(20),
            content=ft.Column(
                controls=[
                    ft.Text("Asistente de Instalación  MagicCorp", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE,text_align=ft.TextAlign.CENTER,),
                    description_text,  # Texto introductorio
                    mode_selector,  # Radios para seleccionar el modo
                    ft.Divider(height=20, thickness=2),  # Línea divisoria para estética
                    pb,  # Barra de progreso con bordes ovalados
                    file_list,  # ListView para mostrar el progreso
                    success_message,  # Mensaje de éxito
                    error_message,  # Mensaje de error
                    install_button,  # Botón para instalar
                    continue_button,  # Botón para continuar
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
        )
        
   