def sacar(*, valor, saques_realizados, limite_diario, limite_saques, saldo, extrato):
    excede_limite_saques = saques_realizados >= limite_diario
    excede_limite_dinheiro = valor > limite_saques
    excede_limite_saldo = valor > saldo

    if excede_limite_saques:
        print( "Limite diário de saques atingido.")

    elif excede_limite_dinheiro:
        print( "Digite um valor válido para saque")

    elif excede_limite_saldo:
        print( "Não será possível sacar o dinheiro por falta de saldo.")

    elif(valor <= saldo):
        saldo -= valor
        extrato.append(f"\n Saque -- R$ {valor:.2F}")
        saques_realizados += 1
        print( "Operação realizada com sucesso!")
        return saques_realizados, saldo
    
    else:
        print( "Operação falhou! O valor informado é inválido.")
    
    return saques_realizados, saldo

def deposito(valor, extrato, saldo, /):
    if (valor > 0):
        saldo += valor
        extrato.append(f"\n Depósito -- R$ {valor:.2F}")
        print("Operação realizada com sucesso!")
        return saldo

    else:
        print("Operação falhou! Digite um valor válido para depósito")

    return saldo

def visualizar_extrato(saldo,/,*, extrato):
    print('=' * 15, "EXTRATO", '=' * 15 )

    if len(extrato) >= 1:
        [print(item) for item in extrato]
        print(f"\n\tSaldo atual -- R${saldo:.2f}")
    else:
        print("\nNão foram realizadas movimentações.")

    print('=' * 40)

def procurar_por_cpf(*, lista, cpf):
    for usuario in lista:
        if(usuario["cpf"] == cpf):
            return True
        else:
            continue
    return False

def criar_usuario(*, nome, data_nascimento, cpf, endereco, lista):
    cpf_encontrado = procurar_por_cpf(lista=lista, cpf=cpf)
    if (cpf_encontrado == False):
        usuario = {"nome": nome, "data de nascimento": data_nascimento, "cpf": cpf, "endereço": endereco}
        lista.append(usuario)
        print("Cadastro realizado com sucesso.")
    else:
        print("CPF já foi cadastrado em outro usuário.")

def listar(lista):
    if len(lista) >= 1:
        [print(usuario) for usuario in lista]
    else:
        print("\nNão foi encontrado nenhum registro.")

def criar_conta_corrente(*, agencia, numero_conta, usuario, listaContas, listaUsuarios):
    cpf_encontrado = procurar_por_cpf(lista=listaUsuarios, cpf=usuario)
    if (cpf_encontrado):
        conta = {"agência": agencia, "conta": numero_conta, "usuário": usuario}
        listaContas.append(conta)
        print("Cadastro de conta realizado com sucesso.")
    else:
        print("CPF de usuário não encontrado.")

menuOperacoes ='''
    Bem vindo ao Banco BumBleBee!

        Digite [1] para Depósito;
        Digite [2] para Saque;
        Digite [3] para Extrato;
        Digite [4] para Voltar ao menu anterior.
=> '''

menuUsuario = '''
    Bem vindo ao Banco BumBleBee!

        Digite [1] para Criar conta corrente;
        Digite [2] para Cadastrar usuário;
        Digite [3] para Listar contas;
        Digite [4] para Listar usuários;
        Digite [5] para Voltar ao menu anterior.
'''

menuInicial = '''
    Bem vindo ao Banco BumBleBee!

        Digite [1] para Área de operações bancárias;
        Digite [2] para Área do usuário;
        Digite [3] para Sair.
'''

extrato = []
clientes = []
contas = []
saldo = 0
saques_realizados = 0
LIMITE_DIARIO = 3
LIMITE_SAQUE = 500

while True:
    #menu inicial
    opi = int(input(menuInicial))

    if (opi == 1):
        #menu de operações
        while True:
            opb = int(input(menuOperacoes))
            if (opb == 1):
                valor = float(input("Digite o valor do seu depósito: "))
                
                saldo = deposito(valor, extrato, saldo)

            elif (opb == 2):
                valor = float(input("Digite o valor do seu saque: "))

                saques_realizados, saldo = sacar(valor=valor, saldo=saldo, saques_realizados=saques_realizados, limite_diario=LIMITE_DIARIO, limite_saques=LIMITE_SAQUE, extrato=extrato)

            elif (opb == 3):
                visualizar_extrato(saldo, extrato=extrato)

            elif (opb == 4):
                break

            else:
                print("Operação inválida, digite uma opção válida para realizar a operação desejada.")

    elif(opi == 2):
        #menu do usuário
        while True:
            opu = int(input(menuUsuario))
            if (opu == 1):
                conta = input("Digite um número da conta: ")
                usuario_cpf = int(input("Digite o cpf do usuário da conta: "))

                criar_conta_corrente(agencia="0001", numero_conta=f"1-{conta}", usuario= usuario_cpf, listaContas=contas, listaUsuarios=clientes)

            elif (opu == 2):
                nome = input("Digite o nome do usuário: ")
                data = input("Digite a data de nascimento do usuário: ")
                cpf = int(input("Digite o cpf do usuário: "))
                logradouro = input("Digite o logradouro do usuário: ")
                numero = input("Digite o numero da residência do usuário: ")
                bairro = input("Digite o bairro da residência do usuário: ")
                estado = input("Digite o cidade/estado do usuário: ")

                endereco = f"{logradouro}, {numero} - {bairro} - {estado}"

                criar_usuario(nome=nome, data_nascimento= data, cpf=cpf, endereco= endereco, lista=clientes)

            elif (opu == 3):
                listar(lista=contas)

            elif (opu == 4):
                listar(lista=clientes)

            elif (opu == 5):
                break

            else:
                print("Operação inválida, digite uma opção válida para realizar a operação desejada.")

    elif (opi == 3):
        break

    else:
        print("Operação inválida, digite uma opção válida para realizar a operação desejada.")