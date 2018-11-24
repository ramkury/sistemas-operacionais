class GerenciadorRecursos():

    def __init__(self):
        # True indica recurso disponível e False indica recurso ocupado.
        self.scanner = True
        self.impressoras = [True,True]
        self.modem = True
        self.SATA = [True, True]
        
    def solicita_scanner(self):
        if self.scanner:
            self.scanner = False
            return True
        else:
            return False

    def solicita_impressora(self, num):
        try:
            if self.impressoras[num-1]:
                self.impressoras[num-1] = False
                return True
            else:
                return False
        except:
            print("Número de impressora inválido.")
            return False

    def solicita_modem(self):
        if self.modem:
            self.modem = False
            return True
        else:
            return False

    def solicita_SATA(self,num):
        try:
            if self.SATA[num-1]:
                self.SATA[num-1] = False
                return True
            else:
                return False
        except:
            print("Número de SATA inválido.")
            return False

    def libera_scanner(self):
        self.scanner = True

    def libera_impressora(self, num):
        self.impressoras[num-1] = True

    def libera_modem(self):
        self.modem = True

    def libera_SATA(self, num):
        self.SATA[num-1] = True

    def print_estado_dispositivos(self):
        if self.scanner:
            print("Scanner => Livre.")
        else:
            print("Scanner => Ocupada.")

        if self.impressoras[0]:
            print("Impressora 1 => Livre.")
        else:
            print("Impressora 1 => Ocupada.")

        if self.impressoras[1]:
            print("Impressora 2 => Livre.")
        else:
            print("Impressora 2 => Ocupada.")

        if self.modem:
            print("Modem => Livre.")
        else:
            print("Modem => Ocupado.")

        if self.SATA[0]:
            print("SATA 1 => Livre.")
        else:
            print("SATA 1 => Ocupada.")

        if self.SATA[1]:
            print("SATA 2 => Livre.")
        else:
            print("SATA 2 => Ocupada.")
