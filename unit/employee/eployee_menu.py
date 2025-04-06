import flet as ft
from pages.dashboard.Menu.D_Container.new_order import Build_Zone_New_Order
from pages.dashboard.Menu.D_Container.beginning import Build_Zone_Beginning
from pages.dashboard.Menu.D_Container.history import Build_Zone_History
from pages.dashboard.Menu.D_Container.summaries import Build_Zone_Summaries
from pages.dashboard.Menu.D_Container.change_duty import Build_Zone_Change_Duty
from pages.authentication.utils.ccs import *

class Build_Zone_Employee(ft.Control):
    def __init__(self, page, dashboard):
        super().__init__()
        self.page = page
        self.dashboard = dashboard  # Referencia a DashboardPage
        self.main_app = dashboard.main_app  # Referencia a MainApp
        self.ccs = Ccs()
        self.zone_beginning = Build_Zone_Beginning(self.page)
        self.zone_new_order = Build_Zone_New_Order(self.page, self)
        self.zone_history = Build_Zone_History(self.page)
        self.zone_sumamries = Build_Zone_Summaries(self.page)
        self.zone_change_duty = Build_Zone_Change_Duty(self.page)

    ###### GENERAL ###########################
    def Buil_Beginning(self):
        data_beginning = ft.Container(
            content=self.zone_beginning.build_zone_beginning(),
            border_radius=15,
            expand=True,
        )
        return ft.Row(expand=True, controls=[data_beginning])     

    ###### New Order ###########################
    def Buil_New_Order(self):
        data_new_order = ft.Container(
            content=self.zone_new_order.build_zone_new_order(),
            expand=True
        )
        return ft.Row(expand=True, controls=[data_new_order])

    ###### History ###########################
    def Buil_History(self):
        data_history = ft.Container(
            content=self.zone_history.build_zone_history(),
            expand=True
        )
        return ft.Row(expand=True, controls=[data_history])

    ###### summaries ###########################
    def Buil_Summaries(self):
        data_summaries = ft.Container(
            content=self.zone_sumamries.build_zone_summaries(),
            expand=True
        )
        return ft.Row(expand=True, controls=[data_summaries])

    ###### Turno de Caja ###########################
    def Buil_Change_Duty(self):
        data_change_duty = ft.Container(
            content=self.zone_change_duty.build_zone_change_duty(),
            expand=True
        )
        return ft.Row(expand=True, controls=[data_change_duty])


