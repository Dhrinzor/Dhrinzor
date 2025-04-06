import flet as ft
from pages.authentication.utils.ccs import Ccs

class Build_Zone_Change_Duty(ft.Control):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.ccs = Ccs()
   
    def build_zone_change_duty(self):     
        return ft.Container(
                    # opacity=0.8,
                    bgcolor=ft.colors.WHITE10,
                    expand=True,
                    padding=ft.padding.only(left=30, top=30, bottom=680),
                    border_radius=15,
                    content=ft.Column(
                        controls=[ft.Text("Cambio de Turno")
                            
                        ]
                    )
                )