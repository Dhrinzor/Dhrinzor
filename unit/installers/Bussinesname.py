import os
import shutil
import flet as ft
from DB.db_setup import BusinessDB  # Importar la función para inicializar la base de datos
class PageContent:
    def __init__(self, page, navigate_to, app):
        self.page = page
        self.navigate_to = navigate_to
        self.app = app  # Referencia a la instancia principal (`InstallPage`)

    def show(self):
        # Mostrar mensaje de error en un contenedor emergente
        def show_error_message(message):
            error_banner.content.controls[0].value = message  # Establecer el mensaje de error
            error_banner.visible = True  # Hacer visible el banner de error
            self.page.update()  # Actualizar la página

        # Ocultar el mensaje de error
        def hide_error_message(_):
            error_banner.visible = False  # Ocultar el banner de error
            self.page.update()  # Actualizar la página

        # Validar el campo de entrada
        def validate_entry(e):
            business_name = e.control.value.upper()  # Convertir entrada a mayúsculas
            e.control.value = business_name  # Actualizar el texto en el campo
            self.page.update()  # Refrescar la página

        # Actualizar el archivo key.txt con el nombre del negocio
        def create_key_file(business_name):
            """Crea o actualiza el archivo key.txt en C:\MagicCorp con el formato especificado."""
            try:
                # Ruta de la carpeta y archivo key.txt
                magiccorp_path = os.path.join("C:\\", "MagicCorp")
                key_file_path = os.path.join(magiccorp_path, "key.txt")

                # Asegurarse de que la carpeta MagicCorp existe
                if not os.path.exists(magiccorp_path):
                    os.makedirs(magiccorp_path)  # Crea la carpeta si no existe
                    print(f"Carpeta creada: {magiccorp_path}")

                # Contenido del archivo key.txt con el formato solicitado
                key_file_content = f"""
        Documento de Seguridad y Credenciales del Usuario
        "Propósito del Documento"
        Este archivo tiene como objetivo proporcionar las credenciales iniciales y las configuraciones necesarias para el uso correcto del software MagicCorp. 
        - Manténgalo seguro y fuera del alcance de terceros no autorizados.
        - Recomendamos cambiar la ubicación de este archivo a una carpeta segura.
        - El contenido de este programa podría ser utilizado de forma malintencionada si es expuesto.

        *****************MagicCorp*****************
    Negocio: {business_name}
    Versión: 
    Tipo de instalación:

        ****************PROTECCIÓN ****************
        1. **Control de Acceso:**
        - **Cifrado de Datos:** Todos los datos sensibles están cifrados para evitar accesos no autorizados.  
        - **Gestión de Usuarios:** Roles y permisos asignados para limitar acciones dentro del sistema.

        2. **Respaldo y Recuperación:**
        - **Copias de Seguridad:** Generación automática de copias de seguridad para proteger la información del negocio.  
        - **Recuperación de Contraseñas:** Opciones seguras para recuperar credenciales en caso de pérdida.

        3. **Integridad del Sistema:**
        - **Verificación de Integridad:** Mecanismos para detectar cambios no autorizados en los archivos del programa.  
        - **Auditorías de Seguridad:** Registro de todas las actividades críticas realizadas en el sistema.

        4. **Actualizaciones Automáticas:**
        - **Parcheo de Vulnerabilidades:** Actualización constante del sistema para mitigar riesgos conocidos.  
        - **Compatibilidad:** Asegura que el programa funcione en entornos actuales y futuros.

        5. **Protección del Entorno:**
        - **Bloqueo de Sesión Inactivo:** Bloqueo automático de la sesión tras un tiempo de inactividad.  
        - **Firewall:** Recomendaciones para configurar un firewall que limite conexiones no autorizadas al programa.

        6. **Política de Contraseñas:**
        - **Requisitos de Contraseñas Fuertes:** Exigir el uso de contraseñas robustas con caracteres especiales, números y mayúsculas.  
        - **Expiración de Contraseñas:** Renovación periódica de contraseñas para evitar accesos comprometidos.

        Instrucciones de Instalación
        - Extraer los archivos del paquete .RAR
        - Ejecutar la instalación en un entorno administrativo para garantizar permisos adecuados.
        - Ingresar las credenciales iniciales:- Usuario: admin
        - Contraseña: GsJEs/QT5.EeMEj4J*m4Bf81

        ****************Detalles Técnicos Adicionales****************
        - **Arquitectura del Sistema:** 64 bits 
        - **Requisitos Mínimos:**  
        - Memoria RAM: Al menos 4 GB.  
        - Almacenamiento: 1 GB de espacio libre en disco.  
        - Resolución: 1280x800 para una experiencia óptima.  
        - **Frameworks Utilizados:**  
        - Flet.  
        - SQLite para la gestión de la base de datos.  
        - **Tecnologías de Seguridad:**  
        - Cifrado DHR para protección de datos sensibles.    
        - **Compatibilidad:**  
        - Compatible con versiones superiores de Windows 10 (incluido Windows 11).  
        - Funciona con Python 3.13.3 o superior.  
        - **Versión del Software:**  
        - Fecha de Compilación: [21-6-25]  
        - Última Actualización: [21-6-25]  
        - **Licencia:**  
        - Uso bajo licencia individual.  
        - **Red y Conexión:**  
        - Conexión requerida para la sincronización con servidores No soportada.  
        
        ****************Responsabilidad del Usuario****************
        El usuario final es responsable de mantener las credenciales en un lugar seguro. No compartir ni distribuir este documento a personas no autorizadas.

        © 2025 - Dhrinzor Corporation. Todos los derechos reservados.
        """

                # Escribir el contenido en key.txt
                with open(key_file_path, "w", encoding="utf-8") as file:
                    file.write(key_file_content)
                print(f"Archivo key.txt creado correctamente en {key_file_path}")

            except Exception as ex:
                raise Exception(f"Error al crear el archivo key.txt: {str(ex)}")

        # Acción al presionar "Continuar"
        def on_continue(_):
            business_name = business_name_field.value.upper().strip()  # Obtener el nombre del negocio
            if not business_name:
                show_error_message("Por favor, ingrese un nombre válido para continuar.")  # Mostrar error si está vacío
                return
            try:
                # Crear el archivo key.txt con el formato especificado
                create_key_file(business_name)

                # Ruta de la carpeta de bases de datos
                db_path = os.path.join("C:\\", "MagicCorp", "DB")

                # Inicializar la base de datos pasando la ruta y el nombre del negocio
                BusinessDB(db_path, business_name)

                # Actualizar el checkbox correspondiente en `InstallPage`
                if hasattr(self.app, "_update_checkboxes"):
                    self.app._update_checkboxes("BusinessName")  # Activar el checkbox correspondiente
                else:
                    print("Error: No se pudo actualizar el checkbox.")

                # Navegar a la siguiente página si no hay errores
                self.navigate_to("unit.installers.Install_tools")
            except Exception as ex:
                # Mostrar el error en un banner si ocurre un problema
                show_error_message(f"Error: {str(ex)}")

        # Campo de entrada del nombre del negocio
        business_name_field = ft.TextField(
            label="Nombre del Negocio:",
            hint_text="Escriba el nombre de su empresa aquí",
            width=500,
            border_color=ft.colors.BLACK,
            color=ft.colors.BLACK,
            focused_border_color=ft.colors.BLUE,
            cursor_color=ft.colors.BLUE,
            on_change=validate_entry,  # Validación de entrada
        )

        # Botón Continuar siempre habilitado
        continue_button = ft.ElevatedButton(
            text="Registrar Negocio",
            on_click=on_continue,  # Intentar actualizar la base de datos y manejar errores
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE,
            icon=ft.icons.CHECK_CIRCLE,  # Icono más profesional
        )

        # Contenedor emergente para mensajes de error
        error_banner = ft.Container(
            visible=False,  # Inicialmente oculto
            bgcolor=ft.colors.RED,  # Fondo rojo para mayor claridad de error
            padding=ft.padding.all(10),
            border_radius=10,
            content=ft.Row(
                controls=[
                    ft.Text(
                        value="",  # El mensaje dinámico se mostrará aquí
                        color=ft.colors.WHITE,  # Texto blanco sobre fondo rojo
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.ElevatedButton(
                        text="Cerrar",
                        bgcolor=ft.colors.GREY_800,
                        color=ft.colors.WHITE,
                        on_click=hide_error_message,  # Cerrar el mensaje al presionar el botón
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        )

        # Título y descripción inicial mejorados
        title_container = ft.Container(
            bgcolor=ft.colors.BLUE,
            padding=ft.padding.all(20),
            border_radius=10,
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Registrar Nombre de su Negocio",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.WHITE,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Este nombre será el identificador principal de su negocio y no podrá cambiarse posteriormente.",
                        size=16,
                        color=ft.colors.WHITE,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                spacing=5,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        )

        return ft.Container(
            bgcolor=ft.colors.GREY_100,
            expand=True,
            padding=ft.padding.all(10),
            content=ft.Column(
                controls=[
                    title_container,
                    ft.Container(margin=ft.margin.only(top=5)),
                    ft.Container(
                        bgcolor=ft.colors.WHITE,
                        padding=ft.padding.all(15),
                        border_radius=10,
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "Proporcione el nombre de su empresa, este será el identificador de su organización.",
                                    size=16,
                                    color=ft.colors.BLACK,
                                    text_align=ft.TextAlign.LEFT,
                                ),
                                business_name_field,
                            ],
                            spacing=15,
                        ),
                    ),
                    ft.Container(margin=ft.margin.only(top=5)),
                    ft.Container(
                        content=continue_button,
                        alignment=ft.alignment.bottom_center,
                    ),
                    error_banner,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
        )