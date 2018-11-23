import datetime

class FileSystem():
    files = []
    
    def __init__(self):
        with open("input_files/files.txt", 'r') as f:
            lines = [l.strip() for l in f.readlines()]
        self.num_blocks = int(lines[0])
        self.bit_map = [0 for _ in range(self.num_blocks)]
        self.ocup = int(lines[1])
        
        for line in lines[2:]:
            line = line.replace(' ', '')
            info = line.split(',')

            # aloca os arquivos existentes
            if info[0].isalpha():
                info.insert(0, 0) #processo dispatcher com PID=0
                #TODO consertar a ordem do info para um padrão
                import ipdb; ipdb.set_trace()
                self.files.append(File().create(info))
                bloco_inicial = int(info[1])
                bloco_final = int(info[1])+int(info[2])
                for i in range(bloco_inicial,bloco_final):
                    self.bit_map[i] = 1 
            
            # realiza as operacoes de create e delete
            else:
                pid = info[0]
                op = info[1]
                file_name = info[2]

                if op == '0':
                    num_blocks = info[3]
                    if num_blocks > (self.num_blocks - self.ocup):
                        bloco_inicial = self.busca_espaco(num_blocks)
                        if bloco_inicial:
                            File().create(info)
                        else:
                            raise "Não há espaço"
                    else:
                        raise "Não há espaço"

                elif op == '1':
                    File().delete(info)
                else:
                    raise "Operação inválida!"

                #import ipdb; ipdb.set_trace()

    def busca_espaco(self, size):
        cont = 0
        for i,bit in enumerate(self.bit_map):
            if cont == size:
                return i
            if bit == 0:
                cont += 1
            else:
                cont = 0

        return False


class File():
    _id = 0

    def create(self, file_info):
        self.id = self._id
        self.size = int(file_info[3])
        self.name = file_info[1]
        self.created_by = file_info[0]
        self.created_in = datetime.datetime.now()

        self._id += 1

        return self

    def delete(self,file_info):
        pass
