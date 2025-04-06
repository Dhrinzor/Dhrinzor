import os
import importlib
import flet as ft

class InstallPage:
    def __init__(self, page: ft.Page):
        self.page = page
        # Inicializa los checkboxes correctamente
        self.checkbox_instalar = ft.Checkbox(
            label="Bienvenido", value=False, fill_color="white", disabled=True
        )
        self.checkbox_license = ft.Checkbox(
            label="Licencia", value=False, fill_color="white", disabled=True
        )
        self.checkbox_business_name = ft.Checkbox(
            label="Registrar Negocio", value=False, fill_color="white", disabled=True
        )
        self.checkbox_herramientas = ft.Checkbox(
            label="Instalar herramientas", value=False, fill_color="white", disabled=True
        )
        self.checkbox_preferencias = ft.Checkbox(
            label="Preferencias", value=False, fill_color="white", disabled=True
        )
        # Ruta absoluta para version.txt
        path = r"D:\APP\the magic card program\version.txt"

        # Diagnóstico del archivo version.txt
        print("Directorio actual:", os.getcwd())
        if not os.path.exists(path):
            self.version = "Versión desconocida"
            print("El archivo version.txt no existe en la ruta especificada.")
        else:
            with open(path, "r") as file:
                self.version = file.read().strip()

    def show(self):
        print("Mostrando la página de instalación...")  # Depuración
        self.page.title = "Instalador - Negocio"
        self.page.horizontal_alignment = "center"
        self.page.vertical_alignment = "center"
        self.page.padding = 150

        # Añade un título centrado encima de los checkboxes
        titulo_checkboxes = ft.Text(
            value="Opciones de Instalación",
            size=25,
            weight=ft.FontWeight.BOLD,
            color="white",
            text_align="center",
        )
        version = ft.Text(f"Versión: {self.version}", size=15, weight=ft.FontWeight.BOLD)

        # Añade un divisor para separar el título de los checkboxes
        divisor = ft.Divider(color="white", thickness=1)

        # Sección izquierda con los checkboxes y el título
        left_section = ft.Container(
            width=350,
            height=600,
            bgcolor=ft.Colors.BLUE,
            border_radius=10,
            padding=10,
            content=ft.Column(
                controls=[
                    titulo_checkboxes,
                    divisor,
                    self.checkbox_instalar,
                    self.checkbox_license,
                    self.checkbox_business_name,
                    self.checkbox_herramientas,
                    self.checkbox_preferencias,
                    divisor,
                    version,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=15,
            ),
        )

        # Sección derecha vacía por ahora
        self.right_section = ft.Container(
            expand=True,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
        )

        # Layout principal
        layout = ft.Container(
            width=900,
            height=600,
            bgcolor=ft.Colors.BLACK54,
            border_radius=10,
            padding=20,
            content=ft.Row(
                controls=[left_section, self.right_section],
                expand=True,
                spacing=4,
            ),
        )

        self.page.add(layout)
        self._load_page("unit.installers.Welcome")  # Carga la primera página

    def _load_page(self, module_name):
        try:
            print(f"Cargando módulo: {module_name}")  # Depuración
            module = importlib.import_module(f"{module_name}")
            if not hasattr(module, "PageContent"):
                raise AttributeError(f"El módulo {module_name} no contiene la clase PageContent.")

            content = module.PageContent(self.page, self._navigate_to, self)
            if not hasattr(content, "show"):
                raise AttributeError(f"La clase PageContent en {module_name} no tiene un método show válido.")

            self.right_section.content = content.show()
            self.right_section.update()
        except Exception as e:
            print(f"Error al cargar el módulo {module_name}: {e}")

    def _navigate_to(self, next_module):
        print(f"Navegando al módulo: {next_module}")  # Depuración
        self._load_page(next_module)

    def actualizar_checkboxes(self):
        print("Actualizando el checkbox 'Bienvenido'...")  # Confirmar que el método es llamado
        if self.checkbox_instalar:
            self.checkbox_instalar.value = True
            self.checkbox_instalar.disabled = False
            print("Checkbox 'Bienvenido' actualizado.")
        self.page.update()