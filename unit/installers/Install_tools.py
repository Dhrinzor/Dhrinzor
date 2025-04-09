import os
import shutil
import time
import flet as ft
from DB.DB_Negocio import DBNegocio  # Importar la gestión de la base de datos

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
            # Crear la carpeta MagicCorp si no existe
            if not os.path.exists(magiccorp_path):
                os.mkdir(magiccorp_path)

            # Crear la carpeta DB dentro de MagicCorp si no existe
            if not os.path.exists(db_dest_path):
                os.mkdir(db_dest_path)

            # Copiar archivos individuales
            files_to_copy = [
                "license.txt",
                "sync_version.bat",
                "version.txt",
                "test.txt",
                "README.md",
                "install.nsi",
                "requirements.txt",
            ]

            total_files = len(files_to_copy)
            progress_increment = 0.3 / (total_files + 2)  # Avance proporcional (incluye carpetas a copiar)

            for index, file_name in enumerate(files_to_copy):
                source_path = os.path.join(os.getcwd(), file_name)
                destination_path = os.path.join(magiccorp_path, file_name)

                if not os.path.exists(source_path):
                    pb.value = 0  # Reiniciar progreso en caso de error
                    pb.color = ft.colors.RED  # Indicar error
                    self.page.update()
                    raise FileNotFoundError(f"No se encontró el archivo '{file_name}' en la raíz local.")

                # Copiar archivo
                shutil.copy(source_path, destination_path)
                print(f"Archivo '{file_name}' copiado exitosamente a {destination_path}")

                # Actualizar progreso después de cada archivo copiado
                pb.value += progress_increment
                self.page.update()

            # Actualizar la línea Version: en key.txt
            key_file_path = os.path.join(magiccorp_path, "key.txt")
            version_file_path = os.path.join(os.getcwd(), "version.txt")

            if not os.path.exists(key_file_path):
                raise FileNotFoundError(f"No se encontró el archivo 'key.txt' en {magiccorp_path}.")
            if not os.path.exists(version_file_path):
                raise FileNotFoundError("No se encontró el archivo 'version.txt' en la raíz local.")

            # Leer la versión desde version.txt
            with open(version_file_path, "r", encoding="utf-8") as version_file:
                version = version_file.read().strip()

            # Actualizar key.txt con la versión
            with open(key_file_path, "r+", encoding="utf-8") as key_file:
                content = key_file.readlines()
                for i, line in enumerate(content):
                    if "Version:" in line:
                        content[i] = f"          Version: {version}\n"
                        break
                key_file.seek(0)
                key_file.writelines(content)
                key_file.truncate()
            print(f"Archivo 'key.txt' actualizado con la versión: {version}")

            # Copiar la carpeta src con su contenido
            src_path = os.path.join(os.getcwd(), "src")
            destination_src_path = os.path.join(magiccorp_path, "src")

            if not os.path.exists(src_path):
                pb.value = 0  # Reiniciar progreso en caso de error
                pb.color = ft.colors.RED  # Indicar error
                self.page.update()
                raise FileNotFoundError("No se encontró la carpeta 'src' en la raíz local.")

            # Copiar toda la carpeta src y su contenido
            shutil.copytree(src_path, destination_src_path, dirs_exist_ok=True)
            print(f"Carpeta 'src' copiada exitosamente a {destination_src_path}")

            # Actualizar progreso después de copiar la carpeta src
            pb.value += progress_increment
            self.page.update()

            # Leer el nombre del negocio desde el archivo key.txt
            business_name = None
            with open(key_file_path, "r", encoding="utf-8") as key_file:
                for line in key_file:
                    if "Negocio:" in line:
                        business_name = line.split(":")[1].strip()
                        break

            if not business_name:
                pb.value = 0  # Reiniciar progreso en caso de error
                self.page.update()
                raise ValueError("El archivo 'key.txt' no contiene un nombre válido para el negocio.")

            # Ruta del archivo de base de datos del negocio
            business_db_path = os.path.join(db_dest_path, f"DB_{business_name}.db")

            # Verificar si existe el archivo con el nombre correcto
            if not os.path.exists(business_db_path):
                pb.value = 0  # Reiniciar progreso en caso de error
                self.page.update()
                raise FileNotFoundError(f"No se encontró el archivo de base de datos: {business_db_path}. Asegúrese de mover el archivo correcto.")

            # Actualizar progreso antes de inicializar la base de datos
            pb.value = 0.8
            self.page.update()

            # Inicializar el objeto DBNegocio con la ruta correcta
            db_negocio = DBNegocio(business_db_path)

            # Configurar las tablas dependiendo del modo seleccionado
            if self.selected_mode == "Negocio":
                db_negocio.setup_negocio_tables()
            elif self.selected_mode == "Local":
                print("Modo 'Local' no implementado completamente.")
            elif self.selected_mode == "Local Independiente":
                print("Modo 'Local Independiente' no implementado completamente.")
            else:
                raise ValueError(f"Modo seleccionado '{self.selected_mode}' no válido.")

            # Actualizar progreso después de configurar las tablas
            pb.value = 1.0  # Progreso completo
            pb.color = ft.colors.GREEN  # Cambiar el color a verde
            self.page.update()

            # Mensaje de éxito
            success_message.value = (
                f"¡Instalación completada como modo '{self.selected_mode}'! "
                "Presione 'Continuar' para proceder."
            )
            success_message.visible = True
            error_message.visible = False
            install_button.visible = False  # Ocultar botón de instalar
            continue_button.visible = True  # Mostrar botón de continuar
            self.page.update()

        except Exception as e:
            # Reiniciar progreso en caso de error
            pb.value = 0  # Reiniciar barra
            pb.color = ft.colors.RED  # Cambiar el color a rojo
            self.page.update()

            # Mostrar mensaje de error
            error_message.value = f"Error: {str(e)}"
            error_message.visible = True
            success_message.visible = False
            install_button.visible = True  # Mostrar botón de instalar nuevamente
            continue_button.visible = False  # Ocultar botón de continuar
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
        global pb, success_message, error_message, install_button, continue_button, mode_selector
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
                        label="Modo Local (Gestión de almacen, inventario y ventas)",
                        label_style=ft.TextStyle(color=ft.colors.BLACK)  # Estilo del texto negro
                    ),
                ],
            ),
            on_change=self.select_mode
        )

        # Estructura de la página
        return ft.Container(
            bgcolor=ft.colors.WHITE,
            expand=True,
            padding=ft.padding.all(20),
            content=ft.Column(
                controls=[
                    ft.Text("Asistente de Instalación - MagicCorp", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE),
                    description_text,  # Texto introductorio
                    mode_selector,  # Radios para seleccionar el modo
                    ft.Divider(height=20, thickness=2),  # Línea divisoria para estética
                    pb,  # Barra de progreso con bordes ovalados
                    success_message,  # Mensaje de éxito
                    error_message,  # Mensaje de error
                    install_button,  # Botón para instalar
                    continue_button,  # Botón para continuar
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
        )