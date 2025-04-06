import flet as ft
from pages.authentication.utils.ccs import Ccs

class Build_Zone_Title(ft.Control):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.ccs = Ccs()
    def build_zone_title(self):
        return ft.Container(
                    # opacity=0.8,
                    bgcolor=ft.colors.WHITE10,
                    expand=True,
                    padding=ft.padding.all(10),
                    
                    border_radius=15,
                    content=ft.Column(
                                controls=[
                                    ft.Container(
                                        content=ft.Text(value="  THE MAGIC CARD  ",font_family=self.ccs.diaria_title, size=self.ccs.hallowin_size, style="headlineLarge"),
                                        alignment=ft.alignment.top_left,
                                    ),
                                    ft.Container(
                                        content=ft.Text(value="  Casa central de la cadena ",font_family=self.ccs.arial, size=self.ccs.normal_size, style="headlineLarge"),
                                        alignment=ft.alignment.top_left,
                                    ) 
                                ]
                            )
                        )