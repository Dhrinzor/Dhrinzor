import flet as ft
from pages.authentication.utils.ccs import Ccs
from pages.authentication.utils.user import UserDB

class Build_Title_Employee(ft.Control):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.ccs = Ccs()
        self.db = UserDB()
        #######Cargar nombre de la cafeteria##########################
        self.active_user=self.db.get_last_login_user()
        self.establecimiento=self.db.get_user_local(self.active_user)
        
    def build_zone_title_employee(self):
        self.B_New_Order = ft.TextButton(content=ft.Row(controls=[
                                        ft.Icon(ft.icons.SHOPPING_BAG_OUTLINED ),
                                        ft.Text("Nueva Orden", font_family=self.ccs.diaria, size=self.ccs.diaria_size )],), 
                                        on_click=lambda e:  self.page.go("/New_Order"))
        self.B_Historial = ft.TextButton(content=ft.Row(controls=[
                                        ft.Icon(ft.icons.HISTORY_EDU_OUTLINED ),
                                        ft.Text("Historial", font_family=self.ccs.diaria, size=self.ccs.diaria_size )],), 
                                        on_click=lambda e:  self.page.go("/history"))
        self.B_Resumen = ft.TextButton(content=ft.Row(controls=[
                                        ft.Icon(ft.icons.SUMMARIZE_OUTLINED ),
                                        ft.Text("Resumen", font_family=self.ccs.diaria, size=self.ccs.diaria_size )],), 
                                        on_click=lambda e:  self.page.go("/summaries"))
        self.B_Cambio_Turno = ft.TextButton(content=ft.Row(controls=[
                                        ft.Icon(ft.icons.PUBLISHED_WITH_CHANGES_OUTLINED ),
                                        ft.Text("Cambio de Turno", font_family=self.ccs.diaria, size=self.ccs.diaria_size )],), 
                                        on_click=lambda e:  self.page.go("/change_duty"))
        return ft.Container(
                    # opacity=0.8,
                    bgcolor=ft.colors.WHITE10,
                    expand=True,
                    padding=ft.padding.all(10),
                    
                    border_radius=15,
                    content=ft.Column(
                                controls=[
                                    ft.Container(
                                        content=ft.Text(value=f"   CAFETERIA: {self.establecimiento}",font_family=self.ccs.diaria_title, size=self.ccs.hallowin_size, style="headlineLarge"),
                                        alignment=ft.alignment.top_left,
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.Container(
                                                content=self.B_New_Order ,
                                                alignment=ft.alignment.top_left,
                                            ), 
                                            ft.Container(
                                                content=self.B_Historial ,
                                                alignment=ft.alignment.top_left,
                                            ), 
                                            ft.Container(
                                                content=self.B_Resumen ,
                                                alignment=ft.alignment.top_left,
                                            ), 
                                            ft.Container(
                                                content=self.B_Cambio_Turno ,
                                                alignment=ft.alignment.top_left,
                                            ), 
                                            
                                        ]
                                    )
                                    
                                ]
                            )
                        )