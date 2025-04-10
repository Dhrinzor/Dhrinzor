import os
import flet as ft

class PageContent:
    def __init__(self, page, navigate_to, app):
        self.page = page
        self.navigate_to = navigate_to
        self.app = app  # Referencia a `InstallPage`
        
    def create_license_file(self):
                #"""Crea o actualiza el archivo key.txt en C:\MagicCorp con el formato especificado."""
                try:
                    # Ruta de la carpeta y archivo key.txt
                    magiccorp_path = os.path.join("C:\\", "MagicCorp")
                    key_file_path = os.path.join(magiccorp_path, "license.txt")

                    # Asegurarse de que la carpeta MagicCorp existe
                    if not os.path.exists(magiccorp_path):
                        os.makedirs(magiccorp_path)  # Crea la carpeta si no existe
                        print(f"Carpeta creada: {magiccorp_path}")

                    # Contenido del archivo key.txt con el formato solicitado
                    license_content = f"""Contrato de Licencia para el Usuario Final (CLUF)
                IMPORTANTE: LEA DETENIDAMENTE ANTES DE USAR ESTE SOFTWARE
                Este contrato de licencia para el usuario final (CLUF) constituye un acuerdo legal entre usted (el "Usuario") y Dhrinzor Corporation. Al instalar, copiar o usar este software de cualquier forma, usted acepta los términos y condiciones establecidos en este contrato. Si no está de acuerdo con los términos, debe desinstalar el software inmediatamente y ponerse en contacto con el servicio de atención al cliente de Dhrinzor Corporation a través del correo electrónico corporationdhrinzor@gmail.com para obtener un reembolso completo, siempre que lo haga dentro de los primeros treinta (30) días posteriores a la compra.

                1. Propiedad del Software
                Este software, incluyendo todo material impreso, documentación en línea o electrónica y cualquier trabajo derivado (el "Programa"), es propiedad exclusiva de Dhrinzor Corporation. El Usuario recibe una licencia limitada para usar el Programa bajo los términos establecidos en este CLUF. Queda estrictamente prohibida toda reproducción, distribución o uso no autorizado del Programa.

                2. Licencia de Uso Limitado
                Dhrinzor Corporation concede al Usuario una licencia limitada, no exclusiva e intransferible para instalar y usar una (1) copia del Programa en un solo dispositivo, ya sea un ordenador personal, portátil o de trabajo.

                3. Restricciones de Uso
                El Usuario tiene prohibido:
                - Copiar, modificar, descompilar, desensamblar, realizar ingeniería inversa o crear trabajos derivados del Programa sin la autorización previa y escrita de Dhrinzor Corporation.
                - Usar componentes del Programa por separado en más de un dispositivo.
                - Transferir, vender, alquilar, arrendar o conceder sublicencias del Programa a terceros sin el consentimiento previo y por escrito de Dhrinzor Corporation.
                - Utilizar el Programa para fines comerciales, tales como en cibercafés, centros de juegos o establecimientos similares. Para uso comercial, póngase en contacto con dhrinzordh@gmail.com para obtener un contrato de licencia especial.

                4. Terminación
                Este contrato será válido hasta su terminación. Dhrinzor Corporation se reserva el derecho de finalizar el CLUF si el Usuario incumple alguno de sus términos. En tal caso, el Usuario debe desinstalar y eliminar todas las copias del Programa inmediatamente.

                5. Garantía Limitada
                El Programa se proporciona "tal cual" sin ninguna garantía expresa o implícita, incluyendo, entre otras, garantías de comerciabilidad o idoneidad para un propósito particular. Sin embargo, Dhrinzor Corporation garantiza que los medios físicos que contienen el Programa estarán libres de defectos materiales durante un periodo de 90 días a partir de la fecha de compra. En caso de defectos, Dhrinzor Corporation puede optar por:
                - Reparar el defecto.
                - Proporcionar un producto similar o de menor valor.
                - Reembolsar el precio de compra.

                6. Limitación de Responsabilidad
                Dhrinzor Corporation y sus afiliados no serán responsables de daños directos, indirectos, incidentales o consecuentes derivados del uso del Programa. Esto incluye, pero no se limita a, pérdida de ingresos, interrupción del negocio o fallos de sistemas informáticos.

                7. Atención al Cliente
                El Usuario puede contactar al equipo de soporte de Dhrinzor Corporation para asistencia técnica o consultas relacionadas con el Programa, enviando un correo electrónico a corporationdhrinzor@gmail.com.

                8. Jurisdicción
                Este contrato se rige por las leyes aplicables en la jurisdicción del domicilio de Dhrinzor Corporation. Algunas jurisdicciones pueden no permitir ciertas limitaciones de garantía, por lo que algunas de las disposiciones aquí contenidas pueden no aplicarse en su caso.
                """

                    # Escribir el contenido en license.txt
                    with open(key_file_path, "w", encoding="utf-8") as file:
                        file.write(license_content)
                    print(f"Archivo key.txt creado correctamente en {key_file_path}")

                except Exception as ex:
                    raise Exception(f"Error al crear el archivo license.txt: {str(ex)}")
            

    def show(self):
        # Crear el archivo de licencia si no existe
        self.create_license_file()

        # Leer el contenido del archivo de licencia
        license_path = r"C:\MagicCorp\license.txt"
        try:
            with open(license_path, "r", encoding="utf-8") as file:
                license_text = file.read().splitlines()
        except FileNotFoundError:
            license_text = ["No se encontró el archivo de licencia. Verifique la instalación."]
            print("Error: El archivo de licencia no existe en la ruta especificada.")
        except UnicodeDecodeError as e:
            license_text = ["Error al leer el archivo de licencia. Codificación incompatible."]
            print(f"Error de decodificación: {e}")

        # Crear elementos para el ListView con el texto de la licencia
        license_items = [ft.Text(line, size=16, color=ft.colors.BLACK) for line in license_text]

        # Crear la estructura de la página
        return ft.Container(
            bgcolor=ft.colors.WHITE,
            expand=True,
            padding=ft.padding.all(10),
            content=ft.Column(
                controls=[
                    ft.Container(
                        bgcolor=ft.colors.WHITE,
                        padding=ft.padding.all(5),
                        border_radius=10,
                        content=ft.Text(
                            "Acuerdo de Licencia",
                            size=25,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.BLACK,
                            text_align="center",
                        ),
                    ),
                    ft.Container(margin=ft.margin.only(top=2)),
                    ft.Container(
                        bgcolor=ft.colors.GREY_200,
                        padding=ft.padding.all(5),
                        border_radius=10,
                        content=ft.ListView(
                            controls=license_items,
                        ),
                        height=355,
                        width=550,
                    ),
                    ft.Container(margin=ft.margin.only(top=5)),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                text="Aceptar",
                                on_click=self._handle_accept_license,
                                bgcolor=ft.colors.GREEN,
                                color=ft.colors.WHITE,
                            ),
                            ft.ElevatedButton(
                                text="Rechazar",
                                on_click=self._handle_reject_license,
                                bgcolor=ft.colors.RED,
                                color=ft.colors.WHITE,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
        )

    def _handle_accept_license(self, e):
        print("Licencia aceptada.")
        if hasattr(self.app, "_update_checkboxes"):
            self.app._update_checkboxes("License")
        else:
            print("Error: No se pudo actualizar el checkbox.")
        self.navigate_to("unit.installers.Bussinesname")

    def _handle_reject_license(self, e):
        print("Licencia rechazada.")
        self.navigate_to("unit.installers.Welcome")