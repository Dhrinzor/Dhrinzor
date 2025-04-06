class Ccs:
    def __init__(self):
        self.alegrian = 'Algerian'
        self.arial = "Arial"
        self.normal = "Bell MT"
        self.monotype = "Monotype Corsiva"
        self.hallowin = "Chiller" 
        self.diaria = self.normal
        self.diaria_title = self.alegrian

        self.hallowin_size = 30
        self.normal_size = 20
        self.diaria_size = self.normal_size
        ##Color de Contaner General
        self.CVenta="blue"
        self.CGastos="red"
        self.CEfectivo="green"
        self.CGanancias="orange"
        self.CHoras="white"
        self.update_mode()

    def update_mode(self):
        try:
            with open("output.txt", "r") as file:
                contenido = file.read()
        except FileNotFoundError:
            contenido = "oscuro"

        self.mode = contenido

    def toggle_mode(self):
        if self.mode == "claro":
            self.mode = "oscuro"
        else:
            self.mode = "claro"

        with open("output.txt", "w") as file:
            file.write(self.mode)

        self.update_mode()

        
        