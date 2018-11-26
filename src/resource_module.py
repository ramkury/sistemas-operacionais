class resource_manager():

    def __init__(self):
        # True indica recurso disponível e False indica recurso ocupado.
        self.scanner = True
        self.printers = [True,True]
        self.modem = True
        self.sata = [True, True]
        
    def request_scanner(self):
        if self.scanner:
            self.scanner = False
            return True
        else:
            return False

    def request_printer(self, num):
        try:
            if self.printers[num-1]:
                self.printers[num-1] = False
                return True
            else:
                return False
        except:
            print("Número de impressora inválido.")
            return False

    def request_modem(self):
        if self.modem:
            self.modem = False
            return True
        else:
            return False

    def request_sata(self,num):
        try:
            if self.sata[num-1]:
                self.sata[num-1] = False
                return True
            else:
                return False
        except:
            print("Número de SATA inválido.")
            return False

    def free_scanner(self):
        self.scanner = True

    def free_printer(self, num):
        self.printers[num-1] = True

    def free_modem(self):
        self.modem = True

    def free_sata(self, num):
        self.sata[num-1] = True

    def print_devices_state(self):
        if self.scanner:
            print("Scanner => Livre.")
        else:
            print("Scanner => Ocupada.")

        if self.printers[0]:
            print("Impressora 1 => Livre.")
        else:
            print("Impressora 1 => Ocupada.")

        if self.printers[1]:
            print("Impressora 2 => Livre.")
        else:
            print("Impressora 2 => Ocupada.")

        if self.modem:
            print("Modem => Livre.")
        else:
            print("Modem => Ocupado.")

        if self.sata[0]:
            print("SATA 1 => Livre.")
        else:
            print("SATA 1 => Ocupada.")

        if self.sata[1]:
            print("SATA 2 => Livre.")
        else:
            print("SATA 2 => Ocupada.")
