import os
import shutil
import time
import flet as ft

class PageContent:
    def __init__(self, page, navigate_to, app):
        self.page = page
        self.navigate_to = navigate_to
        self.app = app  # Referencia al objeto principal del programa para manejar el checkbox


    def install_process(self):
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
                time.sleep(0.1)  # Simular retraso para visibilidad
                self.page.update()

            # Mensaje de éxito
            success_message.value = "¡Instalación completada con éxito! Presione 'Continuar' para proceder."
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
        # Navegar al siguiente módulo
        self.app.checkbox_herramientas.value = True  # Marcar el checkbox correspondiente
        self.app.page.update()  # Actualizar la página principal
        self.navigate_to("unit.installers.Performance")

    def show(self):
        # Barra de progreso inicial con bordes ovalados
        global pb, success_message, error_message, install_button, continue_button
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
            "Bienvenido al asistente de instalación de MagicCorp.\n"
            "Este proceso configurará los archivos necesarios para la operación del sistema. "
            "Presione 'Instalar' para comenzar.",
            size=16,
            color=ft.colors.BLACK,
            text_align=ft.TextAlign.CENTER,
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