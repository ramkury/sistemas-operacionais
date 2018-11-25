import datetime

class FileSystem():
    files = {} # Arquivos contidos no disco e seus respectivos endereços iniciais
    
    def __init__(self, processes):

        with open("input_files/files.txt", 'r') as f:
            lines = [l.strip() for l in f.readlines()]
        self.num_blocks = int(lines[0]) # Número de blocos ocupados
        self.bit_map = [0 for _ in range(self.num_blocks)] # Mapa de bits
        self.ocup = int(lines[1]) # Número de segmentos ocupados
        self.operation = 0 # Número da operação realizada
        
        print("Sistema de arquivos =>")
        for line in lines[2:]:
            line = line.replace(' ', '')
            info = line.split(',')

            # Aloca os arquivos já existentes no disco
            if info[0].isalpha():
                info.insert(0, -1) # Processo dispatcher não possui PID, inserido -1
                bloco_inicial = int(info[2])
                bloco_final = int(info[2])+int(info[3])
                info.pop(2) # Mantém info no padrão desejado
                self.files[bloco_inicial] = File().create(info, protected=False)
                for i in range(bloco_inicial,bloco_final):
                    self.bit_map[i] = 1 
            
            # Realiza as operacoes de create e delete
            else:
                pid = int(info[0])
                op = info[1]
                file_name = info[2]

                try:
                    proc_ind = [p.pid for p in processes].index(pid)
                except ValueError:
                    # Processo que não existe.
                    print("Operação {} => Falha".format(self.operation))
                    self.operation += 1
                    print("Não existe o processo {}.".format(pid))
                    continue

                proc = processes[proc_ind]
                
                # Processo tem tempo de processamento disponível?
                if proc.proc_time > 0:

                    # Criar arquivo
                    if op == '0':

                        # Arquivo existe?
                        if file_name not in [f.name for f in self.files.values()]:

                            num_blocks = int(info[3])
                            if num_blocks <= (self.num_blocks - self.ocup):
                                info.pop(1) # Mantém info no padrão desejado
                                bloco_inicial = self.busca_espaco(num_blocks)
                                
                                # Existe espaço contínuo disponível para este tamanho de bloco?
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
                                        mensagem = "O processo {} criou o arquivo {} nos blocos {}. Sucesso.".format(pid, file_name, blocos)
                                    else:
                                        mensagem = "O processo {} criou o arquivo {} no bloco {}. Sucesso.".format(pid, file_name, bloco_inicial)
                                    
                                    self.ocup += num_blocks
                                    print("Operação {} => Sucesso".format(self.operation))
                                    print(mensagem)
                                
                                else:
                                    print("Operação {} => Falha".format(self.operation))
                                    print("O processo {} não pode criar o arquivo {}. Não há espaço."
                                    .format(pid, file_name))

                            else:
                                print("Operação {} => Falha".format(self.operation))
                                print("O processo {} não pode criar o arquivo {}. Não há espaço."
                                    .format(pid, file_name))

                        else:
                            print("Operação {} => Falha".format(self.operation))
                            print("O arquivo {} já existe.".format(file_name))

                    # Deletar arquivo
                    elif op == '1':

                        file = self.get_file(file_name)
                        # Se arquivo existir, senão o erro já foi tratado na função get_file()
                        if file:
                            # Verica se é um processo de tempo real
                            # Ou se o processo que quer deletar é o criador do arquivo
                            # (para caso seja um processo de usuário)
                            if (proc.priority==0) or (file.created_by == pid):
                                if self.delete_file(file):
                                    print("Operação {} => Sucesso".format(self.operation))
                                    print("O processo {} deletou o arquivo {}.".format(pid, file_name))
                            else:
                                print("Operação {} => Falha".format(self.operation))
                                print("O processo {} não pode deletar o arquivo {}".format(pid, file_name))

                    else:
                        print("Operação {} => Falha".format(self.operation))
                        print("Operação inválida!")
                
                else:
                    print("Operação {} => Falha".format(self.operation))
                    print("Falha! O processo {} já encerrou o seu tempo de processamento.".format(pid))

                proc.proc_time -= 1
                self.operation += 1

        self.print_mapa_ocupacao()
                

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


    def print_mapa_ocupacao(self):
        print("\nMapa de ocupação do disco")
        mapa = '|'
        bit_map_iter = iter(enumerate(self.bit_map))
        for i,bit in bit_map_iter:
            if bit:
                for j in range(self.files[i].size):
                    mapa += "{}|".format(self.files[i].name)
                    if not j == self.files[i].size-1:
                        next(bit_map_iter)
            else:
                mapa += '0|'
        mapa += '\n'
        print(mapa)


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
        self.created_at = datetime.datetime.now()
        self.protected = protected

        self._id += 1

        return self
