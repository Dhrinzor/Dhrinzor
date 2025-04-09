import os
import shutil
import time
import flet as ft

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
        mode_selector.update()  # Actualizar para reflejar el estado

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

            # Ruta de origen de la carpeta DB en el directorio actual
            source_folder = os.path.join(os.getcwd(), "DB")
            if not os.path.exists(source_folder):
                raise FileNotFoundError(f"No se encontró la carpeta de origen: {source_folder}")

            # Obtener todos los archivos .db en la carpeta de origen
            db_files = [f for f in os.listdir(source_folder) if f.endswith(".db")]
            if not db_files:
                raise FileNotFoundError("No se encontraron archivos .db en la carpeta de origen.")

            # Configurar la barra de progreso
            total_files = len(db_files)
            pb.value = 0
            self.page.update()

            # Copiar archivos con progreso
            for i, file in enumerate(db_files):
                src_path = os.path.join(source_folder, file)
                dest_path = os.path.join(db_dest_path, file)
                shutil.copy(src_path, dest_path)

                # Actualizar barra de progreso
                pb.value = (i + 1) / total_files
                time.sleep(0.2)  # Simular retraso para visibilidad
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
            # Mostrar mensaje de error si ocurre alguna excepción
            error_message.value = f"Error: {str(e)}"
            error_message.visible = True
            success_message.visible = False
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