import datetime

class FileSystem():
    
    def __init__(self):

        # Inicializa o FileSystem com os arquivos já contidos no disco

        print("\nSistema de arquivos =>")

        with open("input_files/files.txt", 'r') as f:
            lines = [l.strip() for l in f.readlines()]

        self.num_blocks = int(lines[0]) # Número de blocos ocupados
        self.bit_map = [0 for _ in range(self.num_blocks)] # Mapa de bits
        self.ocup = int(lines[1]) # Número de segmentos ocupados
        self.operation_num = 0 # Número da operação realizada
        self.files = {} # Arquivos contidos no disco e seus respectivos endereços iniciais
        self.operations = []
        
        for line in lines[2:]:
            line = line.replace(' ', '')
            info = line.split(',')

            # Aloca os arquivos já existentes no disco
            if info[0].isalpha():
                info.insert(0, -1) # Processo dispatcher não possui PID, inserido -1
                initial_block = int(info[2])
                final_block = int(info[2])+int(info[3])
                info.pop(2) # Mantém info no padrão desejado
                # Verifica se não há inconsistência nos arquivos iniciais do disco em files.txt
                if final_block > self.num_blocks:
                    print("Inconsistência! O arquivo files.txt contém arquivos que não cabem no disco.")
                    print("Arquivo {} não inserido.".format(info[1]))
                else:
                    for i in range(initial_block,final_block):
                        self.bit_map[i] = 1
                    self.files[initial_block] = File(info)
            else:
                # Salva a lista de operações
                self.operations.append(info)
            

    def run_operations(self, processes):
        # Realiza as operacoes de create e delete
        # @processes: é uma lista de objetos process()
        
        for info in self.operations:
            # info está no padrão do arquivo files.txt, ou seja,
            # [pid, op_code, file_name, (num_blocks, se op_code==0)]
                
            pid = int(info[0])
            op = info[1]
            file_name = info[2]

            try:
                proc_ind = [p.pid for p in processes].index(pid)
            except ValueError:
                # Processo que não existe.
                print("Operação {} => Falha".format(self.operation_num))
                self.operation_num += 1
                print("Não existe o processo {}.".format(pid))
                continue

            process = processes[proc_ind]
            
            # Processo tem tempo de processamento disponível?
            if process.proc_time > 0:

                # Criar arquivo
                if op == '0':
                    
                    # Arquivo existe?
                    if file_name not in [f.name for f in self.files.values()]:

                        num_blocks = int(info[3])
                        if num_blocks <= (self.num_blocks - self.ocup):
                            info.pop(1) # Mantém info no padrão desejado
                            initial_block = self.seek_continuous_free_space(num_blocks)
                            
                            # Existe espaço contínuo disponível para este tamanho de bloco?
                            if initial_block != -1:
                                self.files[initial_block] = File(info)
                                for i in range(initial_block,initial_block+num_blocks):
                                    self.bit_map[i] = 1 
                                
                                if num_blocks > 1:
                                    blocks_str = ''
                                    for bl in range(initial_block, initial_block+num_blocks):
                                        if bl == initial_block+num_blocks-1:
                                            blocks_str = blocks_str[:-2]
                                            blocks_str += ' e ' + str(bl)
                                            break
                                        blocks_str += str(bl) + ', '
                                    message = "O processo {} criou o arquivo {} nos blocos {}. Sucesso.".format(pid, file_name, blocks_str)
                                else:
                                    message = "O processo {} criou o arquivo {} no bloco {}. Sucesso.".format(pid, file_name, initial_block)
                                
                                self.ocup += num_blocks
                                print("Operação {} => Sucesso".format(self.operation_num))
                                print(message)
                            
                            else:
                                print("Operação {} => Falha".format(self.operation_num))
                                print("O processo {} não pode criar o arquivo {}. Não há espaço."
                                .format(pid, file_name))
                        else:
                            print("Operação {} => Falha".format(self.operation_num))
                            print("O processo {} não pode criar o arquivo {}. Não há espaço."
                                .format(pid, file_name))

                    else:
                        print("Operação {} => Falha".format(self.operation_num))
                        print("O arquivo {} já existe.".format(file_name))

                # Deletar arquivo
                elif op == '1':

                    file = self.get_file(file_name)
                    # Verifica se arquivo existe
                    if file:
                        # Verica se é um processo de tempo real
                        # Ou se o processo que quer deletar é o criador do arquivo
                        # (para caso seja um processo de usuário)
                        if (process.priority==0) or (file.created_by == pid):
                            if self.delete_file(file):
                                print("Operação {} => Sucesso".format(self.operation_num))
                                print("O processo {} deletou o arquivo {}.".format(pid, file_name))
                        else:
                            print("Operação {} => Falha".format(self.operation_num))
                            print("O processo {} não pode deletar o arquivo {}".format(pid, file_name))
                    
                    else:
                        print("Operação {} => Falha".format(self.operation_num))
                        print("Arquivo {} não existe.".format(file_name))

                else:
                    print("Operação {} => Falha".format(self.operation_num))
                    print("Operação inválida!")
            
            else:
                print("Operação {} => Falha".format(self.operation_num))
                print("Falha! O processo {} já encerrou o seu tempo de processamento.".format(pid))

            process.proc_time -= 1
            self.operation_num += 1
                

    def seek_continuous_free_space(self, size):
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
            return None
        else:
            return [f for f in self.files.values()][file_ind]


    def delete_file(self, file):
        for f in self.files.items():
            if f[1]==file:
                initial_block = f[0]
                break
        for i in range(initial_block,initial_block+file.size):
            self.bit_map[i] = 0
        self.ocup -= file.size
        self.files.pop(initial_block)
        return True


    def print_disk_occup_map(self):
        print("\nMapa de ocupação do disco")
        map_str = '|'
        bit_map_iter = iter(enumerate(self.bit_map))
        for i,bit in bit_map_iter:
            if bit:
                for j in range(self.files[i].size):
                    map_str += "{}|".format(self.files[i].name)
                    if not j == self.files[i].size-1:
                        next(bit_map_iter)
            else:
                map_str += '0|'
        map_str += '\n'
        print(map_str)


class File():
    _id = 0

    def __init__(self, file_info):
        # file_info[0] => pid
        # file_info[1] => name
        # file_info[2] => size
        self.id = File._id
        self.size = int(file_info[2])
        self.name = file_info[1]
        self.created_by = int(file_info[0])
        self.created_at = datetime.datetime.now()

        File._id += 1
