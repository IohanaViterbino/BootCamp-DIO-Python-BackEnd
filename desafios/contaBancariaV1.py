menu ='''
    Bem vindo ao Banco BumBleBee!

        Digite [1] para Depósito;
        Digite [2] para Saque;
        Digite [3] para Extrato;
        Digite [4] para Sair.
'''

saldo = 0
extrato = ""
limite_diario = 3
LIMITE_SAQUE = 500

while True:

    opc = int(input(menu))

    if (opc == 1):
        valor = int(input("Digite o valor do seu depósito: "))

        if (valor > 0):
            saldo += valor
            extrato += f"\n Depósito -- R$ {valor:.2F}"
            print("Operação realizada com sucesso!")
        else:
            print("Digite um valor válido para depósito")

    elif (opc == 2):
        valor = int(input("Digite o valor do seu saque: "))

        if (valor <= LIMITE_SAQUE and valor > 0):
            if(limite_diario > 0 ):
                if(valor <= saldo):
                    limite_diario -= 1
                    saldo -= valor
                    extrato += f"\n Saque -- R$ {valor:.2F}"
                    print("Operação realizada com sucesso!")
                else:
                    print("Não será possível sacar o dinheiro por falta de saldo.")
            else:
                print("Limite diário de saques atingido.")
        else:
            print("Digite um valor válido para saque")

    elif (opc == 3):
        if(extrato == ""):
            print("\nNão foram realizadas movimentações.")
        else:
            print(f"\nSaldo atual -- R${saldo:.2f}\nSeu extrato:{extrato}")

    elif (opc == 4):
        break

    else:
        print("Digite uma opção válida para realizar as operações.")