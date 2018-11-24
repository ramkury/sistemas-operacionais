import datetime

class FileSystem():
    files = {}
    
    def __init__(self, processes):

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
                bloco_inicial = int(info[2])
                bloco_final = int(info[2])+int(info[3])
                info.pop(2)
                self.files[bloco_inicial] = File().create(info, protected=False)
                for i in range(bloco_inicial,bloco_final):
                    self.bit_map[i] = 1 
            
            # realiza as operacoes de create e delete
            else:
                pid = int(info[0])
                op = info[1]
                file_name = info[2]

                try:
                    proc_ind = [p.pid for p in processes].index(pid)
                except ValueError:
                    print("Não existe o processo {}.".format(pid))
                    continue
                proc = processes[proc_ind]

                if proc.proc_time > 0:
                    if op == '0':
                        if file_name not in [f.name for f in self.files.values()]:
                            num_blocks = int(info[3])
                            if num_blocks <= (self.num_blocks - self.ocup):
                                info.pop(1)
                                bloco_inicial = self.busca_espaco(num_blocks)
                                if bloco_inicial != -1:
                                    self.files[bloco_inicial] = File().create(info)
                                    for i in range(bloco_inicial,bloco_inicial+num_blocks):
                                        self.bit_map[i] = 1 
                                    if num_blocks > 1:
                                        blocos = ''
                                        for bl in range(bloco_inicial, bloco_inicial+num_blocks):
                                            if bl == bloco_inicial+num_blocks-1:
                                                blocos = blocos[:-2]
                                                blocos += ' e ' + str(bl)
                                                break
                                            blocos += str(bl) + ', '
                                        self.ocup += num_blocks
                                        print("O processo {} criou o arquivo {} nos blocos {}. Sucesso."
                                            .format(pid, file_name, blocos))
                                    else:
                                        self.ocup += num_blocks
                                        print("O processo {} criou o arquivo {} no bloco {}. Sucesso."
                                            .format(pid, file_name, bloco_inicial))
                                else:
                                    print("O processo {} não pode criar o arquivo {}. Não há espaço."
                                    .format(pid, file_name))

                            else:
                                print("O processo {} não pode criar o arquivo {}. Não há espaço."
                                    .format(pid, file_name))

                        else:
                            print("O arquivo {} já existe.".format(file_name))

                    elif op == '1':

                        fil = self.get_file(file_name)
                        if fil:
                            if not fil.protected:
                                if self.delete_file(fil):
                                    print("O processo {} deletou o arquivo {}.".format(pid, file_name))
                            else:
                                if fil.created_by == pid:
                                    if self.delete_file(fil):
                                        print("O processo {} deletou o arquivo {}.".format(pid, file_name))
                                else:
                                    print("O processo {} não pode deletar o arquivo {}".format(pid, file_name))

                    else:
                        print("Operação inválida!")
                    
                    proc.proc_time -= 1
                
                else:
                    print("Falha! O processo {} já encerrou o seu tempo de processamento.".format(pid))
                

    def busca_espaco(self, size):
        cont = 0
        for i,bit in enumerate(self.bit_map):
            if cont == size:
                return i-size
            if bit == 0:
                cont += 1
            else:
                cont = 0

        return -1


    def get_file(self, name):
        try:
            file_ind = [f.name for f in self.files.values()].index(name)
        except ValueError:
            print("Arquivo {} não existe.".format(name))
            return None
        else:
            return [f for f in self.files.values()][file_ind]


    def delete_file(self, file):
        for f in self.files.items():
            if f[1]==file:
                inicio_file = f[0]
                break
        for i in range(inicio_file,inicio_file+file.size):
            self.bit_map[i] = 0
        self.ocup -= file.size
        self.files.pop(inicio_file)
        return True


class File():
    _id = 0

    def create(self, file_info, protected=True):
        # file_info[0] => pid
        # file_info[1] => name
        # file_info[2] => size
        self.id = self._id
        self.size = int(file_info[2])
        self.name = file_info[1]
        self.created_by = file_info[0]
        self.created_in = datetime.datetime.now()
        self.protected = protected

        self._id += 1

        return self
