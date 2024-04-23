menu ='''
    Bem vindo ao Banco BumBleBee!

        Digite [1] para Depósito;
        Digite [2] para Saque;
        Digite [3] para Extrato;
        Digite [4] para Sair.
'''

saldo = 0
extrato = ""
LIMITE_SAQUE = 500
LIMITE_DIARIO = 3

while True:

    opc = int(input(menu))

    if (opc == 1):
        valor = int(input("Digite o valor do seu depósito: "))

        if (valor > 0):
            saldo += valor
            extrato += f"\n Depósito -- R$ {valor:.2F}"
        else:
            print("Digite um valor válido para depósito")
            continue

    elif (opc == 2):
        valor = int(input("Digite o valor do seu saque: "))

        if (valor <= LIMITE_SAQUE and LIMITE_DIARIO > 0):
            saldo -= valor
            extrato += f"\n Saque -- R$ {valor:.2F}"
        else:
            print("Digite um valor válido para depósito")
            continue

    elif (opc == 3):
        print(extrato)

    elif (opc == 4):
        break

    else:
        print("Digite uma opção válida para realizar as operações.")