import flet as ft
from pages.authentication.utils.ccs import *

class Build_Zone_Turno_Caja(ft.Control):
    def __init__(self, page):
        super().__init__()
        self.page = page 
        
    def build_zone_turno_caja(self):
        #####DATOS DE LA TABLA##########################

        
        return ft.Container(
                    # opacity=0.8,
                    bgcolor=ft.colors.WHITE10,
                    expand=True,
                    padding=ft.padding.only(left=30, top=30, bottom=710),
                    border_radius=15,
                    content=ft.Column(
                        controls=[
                            
                        ]
                    )
                )