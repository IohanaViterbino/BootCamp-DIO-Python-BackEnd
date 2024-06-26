from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        # recebe uma instancia de conta
        self.contas.append(conta)

    def mostrar_contas(self):
        if len(self.contas) >= 1:
            [print(item) for item in self.contas]
        else:
            print("\nNão foi encontrado nenhum registro de contas anteriores.")
    
    def procurar_conta(self, numero):
        for conta in self.contas:
            if(conta.numero == numero):
                return (True, conta)
            else:
                continue
        return (False,)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nasimento, **kws):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nasimento
        super().__init__(**kws)
    
    def __str__(self):
        return f"""\
            Nome:\t{self.nome}
            CPF:\t{self.cpf}
        """

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        #recebe uma instancia de cliente
        self._historico = Historico()
        # iniciação de um obj histórico

    @classmethod
    def nova_conta(cls, cliente, numero):
        print("Conta criada com sucesso!")
        return cls(cliente=cliente, numero=numero)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        excede_limite_saldo = valor > self._saldo
        
        if excede_limite_saldo:
            print("Operação falhou! Não será possível sacar o dinheiro por falta de saldo.")

        elif (valor <= self._saldo and valor > 0):
            self._saldo -= valor 
            print( "Operação realizada com sucesso!")
            return True, self._saldo
        else:
            print( "Operação falhou! O valor informado é inválido.")
        
        return (False,)

    def depositar(self, valor):
        if (valor > 0):
            self._saldo += valor
            print("Operação realizada com sucesso!")
            return True, self._saldo
        else:
            print("Operação falhou! Digite um valor válido para depósito")
            return (False,)

class ContaCorrente(Conta):
    def __init__(self, limite=500, limite_saques=3, **kw):
        self._limite = limite
        self._limite_saques = limite_saques
        super().__init__(**kw)

    @property
    def limite(self):
        return self._limite
    
    @property
    def limite_saques(self):
        return self._limite_saques

    def sacar(self, valor):
        saques_realizados = len(
            [transacao for transacao in self.historico.transacoes if transacao["Tipo de transação"] == Saque.__name__]
        )

        excede_limite_saques = saques_realizados >= self.limite_saques
        excede_limite_dinheiro = valor > self.limite
        
        
        if excede_limite_saques:
            print( "Operação falhou! Limite diário de saques atingido.")

        elif excede_limite_dinheiro:
            print( "Operação falhou! Digite um valor válido para saque")
        
        else:
            return super().sacar(valor)
        
        return (False,)

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            Conta Corrente:\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
    
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            "Tipo de transação": transacao.__class__.__name__,
            "Valor": f"R$ {transacao.valor:.2f}",
            "Data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })
        
    def mostrar_transacoes(self):
        if len(self.transacoes) >= 1:
            [print(item) for item in self.transacoes]
        else:
            print("\nNão foi encontrado nenhum registro de transações anteriores.")

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(cls, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        super().__init__()

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        transacao = conta.depositar(self.valor)

        if transacao[0]:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        super().__init__()

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        transacao = conta.sacar(self.valor)

        if transacao[0]:
            conta.historico.adicionar_transacao(self)

class Banco:
    def __init__(self, nome):
        self._nome = nome
        self._clientes = []

    @property
    def nome(self):
        return self._nome

    @property
    def clientes(self):
        return self._clientes

    def adicionar_cliente(self, cliente):
        self.clientes.append(cliente)
        print("Cliente cadastrado com sucesso!")

    def procurar_cliente(self, cpf):
        for usuario in self.clientes:
            if(usuario.cpf == cpf):
                return (True, usuario)
            else:
                continue
        return (False,)
    
    def listar_usuarios(self):
        if len(self.clientes) >= 1:
            [print(usuario) for usuario in self.clientes]
        else:
            print("\nNão foi encontrado nenhum registro.")

bancoBBB = Banco(nome="BumBle Bee")

menuOperacoes = f'''
    Bem vindo ao Banco {bancoBBB.nome}!

        Digite [1] para Depósito;
        Digite [2] para Saque;
        Digite [3] para Extrato;
        Digite [4] para Voltar ao menu anterior.
=> '''

menuUsuario = f'''
    Bem vindo ao Banco {bancoBBB.nome}!

        Digite [1] para Cadastrar usuário;
        Digite [2] para Listar contas do usuário;
        Digite [3] para Criar conta corrente;
        Digite [4] para Listar usuários;
        Digite [5] para Voltar ao menu anterior.
'''

menuInicial = f'''
    Bem vindo ao Banco {bancoBBB.nome}!

        Digite [1] para Área do usuário;
        Digite [2] para Área de operações bancárias;
        Digite [3] para Sair.
'''

while True:
    opi = int(input(menuInicial))

    if opi == 1:
        #menu de usuarios
        while True:
            opu = int(input(menuUsuario))

            if (opu == 1):
                nome = input("Digite o nome do usuário: ")
                data = input("Digite a data de nascimento do usuário: ")
                cpf = int(input("Digite o cpf do usuário: "))
                logradouro = input("Digite o logradouro do usuário: ")
                numero = input("Digite o numero da residência do usuário: ")
                bairro = input("Digite o bairro da residência do usuário: ")
                estado = input("Digite o cidade/estado do usuário: ")

                endereco = f"{logradouro}, {numero} - {bairro} - {estado}"
                bancoBBB.adicionar_cliente(PessoaFisica(cpf=cpf, nome=nome, data_nasimento=data, endereco=endereco))
            
            elif (opu == 2):
                cpf = int(input("Digite o cpf do usuário: "))

                usuario = bancoBBB.procurar_cliente(cpf=cpf)

                if usuario[0] == True:
                    usuario[1].mostrar_contas()
                else:
                    print("Usuário não encontrado!")

            elif (opu == 3):
                cpf = int(input("Digite o cpf do usuário: "))

                usuario = bancoBBB.procurar_cliente(cpf=cpf)

                if usuario[0] == True:
                    numero = int(input("Digite o numero da nova conta: "))

                    conta_criada =ContaCorrente.nova_conta(cliente=usuario[1], numero=numero)
                    usuario[1].adicionar_conta(conta=conta_criada)
                else:
                    print("Usuário não encontrado!")

            elif (opu == 4):
                bancoBBB.listar_usuarios()

            elif (opu == 5):
                break

            else:
                print("Operação inválida, digite uma opção válida para realizar a operação desejada.")

            
    if opi == 2:
        #menu de operações
        while True:
            opo = int(input(menuOperacoes))

            if (opo == 1):
                cpf = int(input("Digite o cpf do usuário: "))
                usuario = bancoBBB.procurar_cliente(cpf=cpf)

                if usuario[0] == True:
                    numero = int(input("Digite o numero da conta: "))
                    conta = usuario[1].procurar_conta(numero=numero)

                    if conta[0]:
                        valor = float(input("Digite o valor do seu depósito: "))  
                        deposito = Deposito(valor=valor) 

                        deposito.registrar(conta=conta[1])
                    else:
                        print("Conta não encontrada!")
                    
                else:
                    print("Usuário não encontrado!")

            elif (opo == 2):
                cpf = int(input("Digite o cpf do usuário: "))
                usuario = bancoBBB.procurar_cliente(cpf=cpf)

                if usuario[0] == True:
                    numero = int(input("Digite o numero da conta: "))
                    conta = usuario[1].procurar_conta(numero=numero)

                    if conta[0]:
                        valor = float(input("Digite o valor do seu saque: "))  
                        saque = Saque(valor=valor) 

                        saque.registrar(conta=conta[1])
                    else:
                        print("Conta não encontrada!")
                    
                else:
                    print("Usuário não encontrado!")

            elif (opo == 3):
                cpf = int(input("Digite o cpf do usuário: "))
                usuario = bancoBBB.procurar_cliente(cpf=cpf)

                if usuario[0] == True:
                    numero = int(input("Digite o numero da conta: "))
                    conta = usuario[1].procurar_conta(numero=numero)

                    if conta[0]:
                        conta[1].historico.mostrar_transacoes()
                    else:
                        print("Conta não encontrada!")
                    
                else:
                    print("Usuário não encontrado!")

            elif (opo == 4):
                break

            else:
                print("Operação inválida, digite uma opção válida para realizar a operação desejada.")

    elif opi == 3:
        break

    else:
        print("Operação inválida, digite uma opção válida para realizar a operação desejada.")
