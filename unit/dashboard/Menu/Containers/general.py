import flet as ft
from pages.authentication.utils.ccs import *


class Build_Zone_General(ft.Control):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app 
        self.ccs = Ccs()
        
        
    def build_zone_general(self):
        
        #####DATOS DE GRAFICO DE VENTAS POR TURNO##########################
        self.data = {"Ailen": 900,"Mago": 1200,"Nelson": 1500}
        limt_y=50000
        bar_groups = [
            ft.BarChartGroup(
                x=index,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=value,
                        width=10,
                        color=ft.colors.AMBER_ACCENT if index == 0 else ft.colors.LIGHT_BLUE if index == 1 else ft.colors.RED_ACCENT if index == 2 else ft.colors.DEEP_PURPLE if index == 3 else ft.colors.CYAN ,
                        tooltip=category,
                        border_radius=5,
                    )
                ],
            ) 
            for index, (category, value) in enumerate(self.data.items())
            
        ]
        
        #####DATOS DE GRAFICO DE PRODUCTOS ESTRELLA##########################
        self.PEdata = {"DULCES CRIOLLOS": 4000,"HUPMANN CON FILTRO": 3500,"POPULAR ROJO": 2350,"CHOCO MANI": 1500 ,"JABAS": 1000}
        
        PEbar_groups = [
            ft.BarChartGroup(
                x=index,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=value,
                        width=10,
                        color=ft.colors.AMBER_ACCENT if index == 0 else ft.colors.LIGHT_BLUE if index == 1 else ft.colors.RED_ACCENT  if index == 2  else ft.colors.DEEP_PURPLE if index == 3 else ft.colors.DEEP_ORANGE_ACCENT if index == 4 else ft.colors.CYAN_ACCENT,
                        tooltip=category,
                        border_radius=5,
                    )
                ],
            ) 
            for index, (category, value) in enumerate(self.PEdata.items())
            
        ]
        
        return ft.Container(
                    # opacity=0.8,
                    bgcolor=ft.colors.WHITE10,
                    expand=True,
                    padding=ft.padding.only(left=10,top=10,bottom=90),
                    border_radius=15,
                    content=ft.Column(
                        controls=[
                            #####Contenedor de los Contenedores de colores
                            ft.Row(
                                controls=[#####Inician los contenedores
                                    ###VENTAS############## 
                                    ft.Container(
                                        padding=ft.padding.all(10),
                                        bgcolor=self.ccs.CVenta,
                                        opacity=0.8,
                                        expand=True,
                                        border_radius=15,
                                        content=ft.Column(    
                                            controls=[
                                                
                                                ft.Container(
                                                    bgcolor=self.ccs.CVenta,
                                                    content=ft.Row(
                                                        controls=[
                                                                ft.Icon(ft.icons.SHOPPING_CART_OUTLINED, size=40),
                                                                ft.Text("4000000.00", font_family=self.ccs.diaria,size=40, color=ft.colors.WHITE),
                                                        ]
                                                    )
                                                ),
                                                
                                                ft.Container(
                                                    bgcolor=self.ccs.CVenta,
                                                    expand=True,
                                                    alignment=ft.alignment.bottom_right,
                                                    content=ft.Text("Venta", style="bodyMedium", color=ft.colors.WHITE),
                                                ) 
                                            ]  
                                        )
                                    ),
                                    
                                    ###GASTOS############## 
                                    ft.Container(
                                        padding=ft.padding.all(10),
                                        bgcolor=self.ccs.CGastos,
                                        opacity=0.8,
                                        expand=True,
                                        border_radius=15,
                                        content=ft.Column(    
                                            controls=[
                                                ft.Container(
                                                    bgcolor=self.ccs.CGastos,
                                                    content=ft.Row(
                                                        controls=[
                                                                ft.Icon(ft.icons.SAVINGS_OUTLINED, size=40),
                                                                ft.Text("4000000.00", font_family=self.ccs.diaria,size=40, color=ft.colors.WHITE),
                                                        ]
                                                    )
                                                ),
                                                ft.Container(
                                                    bgcolor=self.ccs.CGastos,
                                                    expand=True,
                                                    alignment=ft.alignment.bottom_right,
                                                    content=ft.Text("Gastos", style="bodyMedium", color=ft.colors.WHITE),
                                                ) 
                                            ]  
                                        )
                                    ),
                                    
                                    ###EFECTIVO##############
                                    ft.Container(
                                        padding=ft.padding.all(10),
                                        bgcolor=self.ccs.CEfectivo,
                                        opacity=0.8,
                                        expand=True,
                                        border_radius=15,
                                        content=ft.Column(    
                                            controls=[
                                                ft.Container(
                                                    bgcolor=self.ccs.CEfectivo,
                                                    content=ft.Row(
                                                        controls=[
                                                                ft.Icon(ft.icons.ATTACH_MONEY_OUTLINED, size=40),
                                                                ft.Text("4000000.00", font_family=self.ccs.diaria,size=40, color=ft.colors.WHITE),
                                                        ]
                                                    )
                                                ),
                                                ft.Container(
                                                    bgcolor=self.ccs.CEfectivo,
                                                    expand=True,
                                                    alignment=ft.alignment.bottom_right,
                                                    content=ft.Text("Efectivo", style="bodyMedium", color=ft.colors.WHITE),
                                                ) 
                                            ]  
                                        )
                                    ),
                                    
                                    ###GANANCIAS##############
                                    ft.Container(
                                        padding=ft.padding.all(10),
                                        bgcolor=self.ccs.CGanancias,
                                        opacity=0.8,
                                        expand=True,
                                        border_radius=15,
                                        content=ft.Column(    
                                            controls=[
                                                ft.Container(
                                                    bgcolor=self.ccs.CGanancias,
                                                    content=ft.Row(
                                                        controls=[
                                                                ft.Icon(ft.icons.TRENDING_UP_OUTLINED, size=40),
                                                                ft.Text("4000000.00", font_family=self.ccs.diaria,size=40, color=ft.colors.WHITE),
                                                        ]
                                                    )
                                                ),
                                                ft.Container(
                                                    bgcolor=self.ccs.CGanancias,
                                                    expand=True,
                                                    alignment=ft.alignment.bottom_right,
                                                    content=ft.Text("Ganancias", style="bodyMedium", color=ft.colors.WHITE),
                                                ) 
                                            ]  
                                        )
                                    ),
                                ]
                            ),
                            #####Contenedor de los Contenedores de horas
                            ft.Row(
                                controls=[
                                    ###Horas/Trabajo##########
                                    ft.Container(
                                        padding=ft.padding.all(10),
                                        bgcolor=ft.colors.WHITE24,
                                        expand=True,
                                        border_radius=15,
                                        content=ft.Column(    
                                            controls=[
                                                ft.Container(
                                                    
                                                    content=ft.Row(
                                                        controls=[
                                                                ft.Icon(ft.icons.TIMER_OUTLINED, size=40),
                                                                ft.Text("400.00", font_family=self.ccs.diaria,size=40),
                                                        ]
                                                    )
                                                ),
                                                ft.Container(
                                                    
                                                    expand=True,
                                                    alignment=ft.alignment.bottom_right,
                                                    content=ft.Text("Horas/Trabajo", style="bodyMedium"),
                                                ) 
                                            ]  
                                        )
                                    ),
                                    
                                    ###Gastos/Hora##########
                                    ft.Container(
                                        padding=ft.padding.all(10),
                                        bgcolor=ft.colors.WHITE24,
                                        expand=True,
                                        border_radius=15,
                                        content=ft.Column(    
                                            controls=[
                                                ft.Container(
                                                    
                                                    content=ft.Row(
                                                        controls=[
                                                                ft.Icon(ft.icons.TIMER_OFF_OUTLINED, size=40),
                                                                ft.Text("4000.00", font_family=self.ccs.diaria,size=40),
                                                        ]
                                                    )
                                                ),
                                                ft.Container(
                                                    
                                                    expand=True,
                                                    alignment=ft.alignment.bottom_right,
                                                    content=ft.Text("Gastos/Hora", style="bodyMedium"),
                                                ) 
                                            ]  
                                        )
                                    ),
                                    
                                    ###Venta-Salario/Hora##########
                                    ft.Container(
                                        padding=ft.padding.all(10),
                                        bgcolor=ft.colors.WHITE24,
                                        expand=True,
                                        border_radius=15,
                                        content=ft.Column(    
                                            controls=[
                                                ft.Container(
                                                    
                                                    content=ft.Row(
                                                        controls=[
                                                                ft.Icon(ft.icons.AV_TIMER_OUTLINED, size=40),
                                                                ft.Text("4000.00", font_family=self.ccs.diaria,size=40),
                                                        ]
                                                    )
                                                ),
                                                ft.Container(
                                                    
                                                    expand=True,
                                                    alignment=ft.alignment.bottom_right,
                                                    content=ft.Text("Venta-Salario/Hora", style="bodyMedium"),
                                                ) 
                                            ]  
                                        )
                                    ),
                                    
                                    ###Ganancias/Hora##########
                                    ft.Container(
                                        padding=ft.padding.all(10),
                                        bgcolor=ft.colors.WHITE24,
                                        expand=True,
                                        border_radius=15,
                                        content=ft.Column(    
                                            controls=[
                                                ft.Container(
                                                    
                                                    content=ft.Row(
                                                        controls=[
                                                                ft.Icon(ft.icons.ACCESS_TIME_OUTLINED, size=40),
                                                                ft.Text("40000.00", font_family=self.ccs.diaria,size=40),
                                                        ],
                                                        
                                                    )
                                                ),
                                                ft.Container(
                                                    
                                                    expand=True,
                                                    alignment=ft.alignment.bottom_right,
                                                    content=ft.Text("Ganancias/Hora", style="bodyMedium"),
                                                ) 
                                            ]  
                                        )
                                    ),
                                    
                                                                        
                                ]######Fin del primer Row
                            ),
                            ####Contenedor de la Tabla Venta por turno
                            ft.Row(
                                #height=None,
                                #expand=True,AQUI NO SE PUEDE EXPANDIR
                                controls=[#####Inician los contenedores
                                    ###VENTAS POR TURNO############## 
                                    ft.Container(
                                        bgcolor=ft.colors.WHITE24,
                                        border_radius=15,
                                        expand=True,
                                        content=ft.Column(
                                                    # expand=True,
                                                    controls=[  
                                                            ft.Container(
                                                                
                                                                alignment=ft.alignment.center,
                                                                padding=ft.padding.only(left=150),
                                                                border_radius=15,
                                                                content=ft.Row(
                                                                        
                                                                        controls=[
                                                                                ft.Icon(ft.icons.POINT_OF_SALE_OUTLINED, size=40),
                                                                                ft.Text("Ventas por turno", font_family=self.ccs.diaria,size=40),
                                                                        ],
                                                                        
                                                                        
                                                                )
                                                            ),    
                                                            #####Contenedor del grafico########
                                                            #ft.Container(self.CGrafica,expand=True,padding=ft.padding.only(left=10,bottom=10, right=10, top=50),
                                                            ft.Container(
                                                                
                                                                padding=ft.padding.all(10),
                                                                margin=10,
                                                                content=ft.BarChart(
                                                                            bar_groups=bar_groups,
                                                                            border=ft.border.all(1, ft.colors.CYAN),
                                                                            left_axis=ft.ChartAxis(
                                                                                labels_size=40, title=ft.Text("VENTAS", font_family=self.ccs.normal, size=self.ccs.normal_size), title_size=40
                                                                            ),
                                                                            bottom_axis=ft.ChartAxis(
                                                                                labels=[
                                                                                    ft.ChartAxisLabel(
                                                                                        value=index, label=ft.Container(ft.Text(category), padding=10)
                                                                                    )
                                                                                    for index, category in enumerate(self.data.keys())
                                                                                ],
                                                                                labels_size=40,
                                                                            ),
                                                                            horizontal_grid_lines=ft.ChartGridLines(
                                                                                color=ft.colors.CYAN, width=1, dash_pattern=[3, 3]
                                                                            ),
                                                                            tooltip_bgcolor=ft.colors.with_opacity(0.1, ft.colors.CYAN_ACCENT),
                                                                            max_y=limt_y,
                                                                            interactive=True,
                                                                            expand=True,
                                                                        )
                                                                
                                                            )
                                                             
                                                                            
                                                    ]
                                        )
                                    ),
                                    ft.Container(
                                        bgcolor=ft.colors.WHITE24,
                                        border_radius=15,
                                        expand=True,
                                        content=ft.ResponsiveRow(
                                                    # expand=True,
                                                    controls=[  
                                                            ft.Container(
                                                                
                                                                expand=True,
                                                                padding=ft.padding.only(left=150),
                                                                border_radius=15,
                                                                content=ft.Row(
                                                                        
                                                                        controls=[
                                                                                ft.Icon(ft.icons.EMOJI_EVENTS_OUTLINED, size=40),
                                                                                ft.Text("Productos Estrella", font_family=self.ccs.diaria,size=40),
                                                                        ],
                                                                        
                                                                        
                                                                )
                                                            ),    
                                                            #####Contenedor del grafico########
                                                            ft.Container(
                                                                
                                                                padding=ft.padding.all(10),
                                                                margin=10,
                                                                content=ft.BarChart(
                                                                            bar_groups=PEbar_groups,
                                                                            border=ft.border.all(1, ft.colors.CYAN),
                                                                            left_axis=ft.ChartAxis(
                                                                                labels_size=40, title=ft.Text("UNIDADES VENDIDAS", font_family=self.ccs.normal, size=self.ccs.normal_size), title_size=40
                                                                            ),
                                                                            
                                                                            horizontal_grid_lines=ft.ChartGridLines(
                                                                                color=ft.colors.CYAN, width=1, dash_pattern=[3, 3]
                                                                            ),
                                                                            tooltip_bgcolor=ft.colors.with_opacity(0.1, ft.colors.CYAN_ACCENT),
                                                                            max_y=5000,
                                                                            interactive=True,
                                                                            expand=True,
                                                                        )
                                                                
                                                            )
                                                             
                                                                            
                                                    ]
                                        )
                                    )
                                ]  
                            )
                        ]
                    )
                )
                                
                                  
                            
                
            
             
                
                
                
            