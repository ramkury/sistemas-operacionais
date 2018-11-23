# -*- coding:utf-8 -*-

# class memory():
# Checkagem da memória para verificar se o processo está apto a ser alocado.
def check_mem(priority, base_register, mem_block, alloc):
    # Caso o pedido seja de alocar processo na memória (alloc == 1)
    if alloc == 1:
        if priority == 0:
            # Verifica se o espaço de memória pedido foi do tamanho correto definido de no máximo 64 blocos
            if mem_block > 64:
                return None
            else:
                # Verifica se há espaço suficiente para alocar o processo. Esta verificação se dá pela conta: addr_inicial_da_mem_livre + tamanho_restante_da_mem < espaço_pedido_pelo_processo
                # e se addr_inicial_da_mem_livre + espaço_pedido ultrapassa o tamanho reservado na memória de 64 blocos
                for i in range(len(rt_mem_space)):
                    if mem_block <= int(rt_mem_space[i][1]) and int(rt_mem_space[i][0]) >= 0 and int(rt_mem_space[i][0]) <= 64 and mem_block + int(rt_mem_space[i][0]) <= 64:
                        return alloc_mem(int(rt_mem_space[i][0]), mem_block, i, 0)
                
                return None
        else:
            # Verifica se o espaço de memória pedido foi do tamanho correto definido de no máximo 960 blocos
            if mem_block > 960:
                return None
            else:
                # Verifica se há espaço suficiente para alocar o processo. Esta verificação se dá pela conta: addr_inicial_da_mem_livre + tamanho_restante_da_mem < espaço_pedido_pelo_processo
                # e se addr_inicial_da_mem_livre + espaço_pedido ultrapassa o tamanho reservado na memória de 960 blocos
                for i in range(len(usr_mem_space)):
                    if mem_block <= int(usr_mem_space[i][1]) and int(usr_mem_space[i][0]) <= 1024  and mem_block + int(usr_mem_space[i][0]) <= 1024:
                        return alloc_mem(int(usr_mem_space[i][0]), mem_block, i, 1)
                
                return None

# Função que aloca o processo na memória. Ela retira o espaço pedido pelo processo da lista de espaço livre.
# Foi utilizado o first-fit, ou seja, ele aloca no primeiro espaço encontrado.
def alloc_mem(base_register, proccess_size, index, priority):
    if priority == 0:
        base = rt_mem_space[index][0]
        size = rt_mem_space[index][1]
        rt_mem_space.pop(index)
        aux = ()
        if int(size) - int(proccess_size) != 0:
            aux = (int(base) + int(proccess_size), int(size) - int(proccess_size))
            rt_mem_space.insert(index, aux)
    else:
        base = usr_mem_space[index][0]
        size = usr_mem_space[index][1]
        usr_mem_space.pop(index)
        aux = ()
        if int(size) - int(proccess_size) != 0:
            aux = (int(base) + int(proccess_size), int(size) - int(proccess_size))
            usr_mem_space.insert(index, aux)

    return base

# Função verifica a memória livre e o processo a ser liberado para que possa ser liberado corretamenteo e ocorrer coalescência caso necessário
def check_free_mem(base_register, proccess_size, priority):
    index = 0
    if priority == 0:
        # Loop para fazer verificação de onde o espaço livre irá entrar na lista de memória livre e se irá ocorres coalescência
        for i in range(len(rt_mem_space)):
            if int(base_register) + int(proccess_size) == int(rt_mem_space[i][0]):
                if index == 0:
                    index = i
                    break
            elif int(base_register) + int(proccess_size) < int(rt_mem_space[i][0]):
                if index == 0:
                    index = i
                    break
            elif int(rt_mem_space[i][0]) < int(base_register):
                index = i
    else:
        # Loop para fazer verificação de onde o espaço livre irá entrar na lista de memória livre e se irá ocorres coalescência
        for i in range(len(usr_mem_space)):
            if int(base_register) + int(proccess_size) == int(usr_mem_space[i][0]):
                if index == 0:
                    index = i
                    break
            elif int(base_register) + int(proccess_size) < int(usr_mem_space[i][0]):
                if index == 0:
                    index = i
                    break
            elif int(base_register) > int(usr_mem_space[i][0]):
                index = i

    disalloc_mem(base_register, proccess_size, index, priority)

# Função que libera a memória depois da verificação de posicionamento do processo a ser liberado   
def disalloc_mem(base_register, proccess_size, index, priority):
    # Processos com prioridade 0: Real-time proccess
    if priority == 0:
        # Caso lista vazia de espaço livre, irá liberar o espaço do processo
        if len(rt_mem_space) == 0:
            aux = (int(base_register), int(proccess_size))
            rt_mem_space.insert(0, aux)
        # Caso tenha info na lista, esse if verifica se o endereço liberado vai até o início da lista vazia, se for, ocorre coalescencia
        elif int(base_register) + int(proccess_size) == int(rt_mem_space[index][0]):
            size = rt_mem_space[index][1]
            rt_mem_space.pop(index)
            new_size = int(size) + int(proccess_size)
            aux = (int(base_register), int(new_size))
            rt_mem_space.insert(index, aux)
        # Caso tenha info na lista, esse if verifica se o endereço liberado foi menor que o início da lista vazia e posiciona o espaço antes das infos da lista
        elif int(base_register) + int(proccess_size) < int(rt_mem_space[index][0]):
            aux = (int(base_register), int(proccess_size))
            rt_mem_space.insert(index, aux)
        # Caso tenha info na lista, esse if verifica se o endereço liberado foi maior que o início da lista vazia e posiciona o espaço no lugar certo da lita
        elif int(base_register) > int(rt_mem_space[index][0]):
            if index > 0 and int(rt_mem_space[index][0]) + int(rt_mem_space[index][1]) == int(base_register):
                base_register = int(rt_mem_space[index][0])
                proccess_size += int(rt_mem_space[index][1])
                rt_mem_space.pop(index)
                aux = (int(base_register), int(proccess_size))
                rt_mem_space.insert(index, aux)
            else:
                aux = (int(base_register), int(proccess_size))
                rt_mem_space.insert(index + 1, aux)
    # Processos com prioridades 1, 2 ou 3 repetem o passo acima, porém na sua lista própria
    else:
        if len(usr_mem_space) == 0:
            aux = (int(base_register), int(proccess_size))
            usr_mem_space.insert(0, aux)
        elif int(base_register) + int(proccess_size) == int(usr_mem_space[index][0]):
            size = usr_mem_space[index][1]
            usr_mem_space.pop(index)
            new_size = int(size) + int(proccess_size)
            aux = (int(base_register), int(new_size))
            usr_mem_space.insert(index, aux)
        elif int(base_register) + int(proccess_size) < int(usr_mem_space[index][0]):
            aux = (int(base_register), int(proccess_size))
            usr_mem_space.insert(index, aux)
        elif int(base_register) > int(usr_mem_space[index][0]):
            if index > 0 and int(usr_mem_space[index][0]) + int(usr_mem_space[index][1]) == int(base_register):
                base_register = int(usr_mem_space[index][0])
                proccess_size += int(usr_mem_space[index][1])
                usr_mem_space.pop(index)
                aux = (int(base_register), int(proccess_size))
                usr_mem_space.insert(index, aux)
            else:
                aux = (int(base_register), int(proccess_size))
                usr_mem_space.insert(index + 1, aux)


# def __init__(self, size):
rt_mem_space = [(0, 64)]
usr_mem_space = [(64, 960)]

# Os valores abaixo serviu para testar a ideia de Alocação com Partição Variável, Fist-fit e Coalescencia. Caso queria testar, só rodar esse módulo apenas e
# ir modificando os valores abaixo e prioridades;

# print(rt_mem_space)
# print(usr_mem_space)

# priority = 0
# mem_block = 6

# check_mem(priority, 0, mem_block, 1)

# print(rt_mem_space)
# print(usr_mem_space)

# priority = 0
# mem_block = 50

# check_mem(priority, 0, mem_block, 1)

# print(rt_mem_space)
# print(usr_mem_space)

# priority = 0
# mem_block = 8

# check_mem(priority, 0, mem_block, 1)

# print(rt_mem_space)
# print(usr_mem_space)

# priority = 0
# base_register = 30
# mem_block = 24

# check_free_mem(base_register, mem_block, priority)

# print(rt_mem_space)
# print(usr_mem_space)

# priority = 0
# base_register = 0
# mem_block = 10

# check_free_mem(base_register, mem_block, priority)

# print(rt_mem_space)
# print(usr_mem_space)

# priority = 0
# base_register = 54
# mem_block = 2

# check_free_mem(base_register, mem_block, priority)

# print(rt_mem_space)
# print(usr_mem_space)

# ATT: Retornando None caso não dê pra alocar e o endereço base caso dê pra alocar