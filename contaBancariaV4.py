from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        if(conta.historico.limite_transacoes_diarias() >= conta.limite_transacao):
            print("Operação falhou! Limite diário de transações atingido.")
        else:
            transacao.registrar(conta)

    def adicionar_conta(self, conta):
        # recebe uma instancia de conta
        self.contas.append(conta)

    def mostrar_contas(self):
        # (depois) passar o interador com as contas como argumento
        if len(self.contas) >= 1:            
            for i in Iterador(iteravel=self.contas):
                print(i)
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
    def __init__(self, limite=500, limite_transacao=10, **kw):
        self._limite = limite
        self._limite_transacao = limite_transacao
        super().__init__(**kw)

    @property
    def limite(self):
        return self._limite
    
    @property
    def limite_transacao (self):
        return self._limite_transacao

    def sacar(self, valor):
        excede_limite_dinheiro = valor > self.limite
        
        if excede_limite_dinheiro:
            print( "Operação falhou! Digite um valor válido para saque")
        
        else:
            return super().sacar(valor)
        
        return (False,)
    
    def depositar(self, valor):
        return super().depositar(valor)
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            Conta Corrente:\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
    
class Historico:
    # adicionnar o gerador aqui
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

    def gerador_relatorios(self, tipo_transacao = None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["Tipo de transação"].lower() == tipo_transacao.lower():
                yield transacao

    def limite_transacoes_diarias(self):
        mascara = "%d-%m-%Y"
        hoje = datetime.today().strftime(mascara)
        transacoes_diarias = [transacao for transacao in self.transacoes if datetime.strptime(transacao["Data"].split()[0], mascara) == datetime.strptime(hoje, mascara)]
        return len(transacoes_diarias)

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

class Iterador:
    # depois tentar fazer com usuário e contas juntos
    def __init__(self, iteravel: list):
        self.contas = iteravel
        self.contador = 0

    def __iter__(self):
        return self

    def __next__(self):
        # retorno é as informações básicas da conta
        try:
            conta = self.contas[self.contador]
            self.contador += 1
            return conta
        except IndexError:
            raise StopIteration

class Banco:
    # iterador colocar aqui
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
        # passar o interador com as contas como argumento
        if len(self.clientes) >= 1:
            for i in Iterador(iteravel=self.clientes):
                print(i)
        else:
            print("\nNão foi encontrado nenhum registro.")

# os decoradores irão funcionar como o menu
# o decorardor tem que printar a data e hora da ação
def log_transacao(funcao):
    def envelope():
        result = funcao()
        # pode ter mensagem de log levemente direfente para os retornos da funcao, eg. tentativa e sucesso 
        result = "tentativa" if result == False else "sucesso"
        print(f"{datetime.now().strftime("%d-%m-%Y %H:%M:%S")} : {result} de {funcao.__name__.upper()}")
        return result
       
    return envelope

@log_transacao
def sacar():
    cpf = int(input("Digite o cpf do usuário: "))
    usuario = bancoBBB.procurar_cliente(cpf=cpf)
    status = True

    if usuario[0] == True:
        numero = int(input("Digite o numero da conta: "))
        conta = usuario[1].procurar_conta(numero=numero)

        if conta[0]:
            valor = float(input("Digite o valor do seu saque: "))  
            saque = Saque(valor=valor) 

            usuario[1].realizar_transacao(conta=conta[1], transacao=saque)
        else:
            print("Conta não encontrada!")
            status = False
    else:
        print("Usuário não encontrado!")
        status = False
    
    return status

@log_transacao
def depositar():
    cpf = int(input("Digite o cpf do usuário: "))
    usuario = bancoBBB.procurar_cliente(cpf=cpf)
    status = True

    if usuario[0] == True:
        numero = int(input("Digite o numero da conta: "))
        conta = usuario[1].procurar_conta(numero=numero)

        if conta[0]:
            valor = float(input("Digite o valor do seu depósito: "))  
            deposito = Deposito(valor=valor) 

            usuario[1].realizar_transacao(conta=conta[1], transacao=deposito)
        else:
            print("Conta não encontrada!")
            status = False
        
    else:
        print("Usuário não encontrado!")
        status = False
    
    return status

@log_transacao
def exibir_extrato():
    # chamar o gerador de relatórios
    cpf = int(input("Digite o cpf do usuário: "))
    usuario = bancoBBB.procurar_cliente(cpf=cpf)
    status = True

    if usuario[0] == True:
        numero = int(input("Digite o numero da conta: "))
        conta = usuario[1].procurar_conta(numero=numero)
        saldo_conta = f"\nSaldo atual: {conta[1].saldo:.2f}\n"

        if conta[0]:
            opex = int(input(menuExtrato))

            match opex:
                case 1:
                    for transacao in conta[1].historico.gerador_relatorios(tipo_transacao = "Deposito"):
                        print(f"{transacao['Tipo de transação']} -- {transacao["Valor"]} em {transacao["Data"]}")
                    print(saldo_conta)
                case 2:
                    for transacao in conta[1].historico.gerador_relatorios(tipo_transacao = "Saque"):
                        print(f"{transacao['Tipo de transação']} -- {transacao["Valor"]} em {transacao["Data"]}")
                    print(saldo_conta)

                case 3:
                    for transacao in conta[1].historico.gerador_relatorios():
                        print(f"{transacao['Tipo de transação']} -- {transacao["Valor"]} em {transacao["Data"]}")
                    print(saldo_conta)

                case _:
                    print("Operação inválida! Opção não reconhecida.")
                    status = False

            # mostrar saldo da conta
        else:
            print("Conta não encontrada!")
            status = False
    else:
        print("Usuário não encontrado!")
        status = False
    
    return status

@log_transacao
def cadastrar_cliente():
    nome = input("Digite o nome do usuário: ")
    data = input("Digite a data de nascimento do usuário: ")
    cpf = int(input("Digite o cpf do usuário: "))
    logradouro = input("Digite o logradouro do usuário: ")
    numero = input("Digite o numero da residência do usuário: ")
    bairro = input("Digite o bairro da residência do usuário: ")
    estado = input("Digite o cidade/estado do usuário: ")

    endereco = f"{logradouro}, {numero} - {bairro} - {estado}"
    bancoBBB.adicionar_cliente(PessoaFisica(cpf=cpf, nome=nome, data_nasimento=data, endereco=endereco))
    
    return True

@log_transacao
def cadastrar_conta():
    cpf = int(input("Digite o cpf do usuário: "))
    usuario = bancoBBB.procurar_cliente(cpf=cpf)
    status = True

    if usuario[0] == True:
        numero = int(input("Digite o numero da nova conta: "))

        conta_criada =ContaCorrente.nova_conta(cliente=usuario[1], numero=numero)
        usuario[1].adicionar_conta(conta=conta_criada)
    else:
        print("Usuário não encontrado!")
        status = False
    
    return status

bancoBBB = Banco(nome="BumBle Bee")

menuExtrato = f'''
        Digite [1] para mostrar depósitos;
        Digite [2] para mostrar saques;
        Digite [3] para mostrar extrato completo;
=>  '''

menuOperacoes = f'''
    Bem vindo ao Banco {bancoBBB.nome}!

        Digite [1] para Depósito;
        Digite [2] para Saque;
        Digite [3] para Extrato;
        Digite [4] para Voltar ao menu anterior.
=>  '''

menuUsuario = f'''
    Bem vindo ao Banco {bancoBBB.nome}!

        Digite [1] para Cadastrar usuário;
        Digite [2] para Listar contas do usuário;
        Digite [3] para Criar conta corrente;
        Digite [4] para Listar usuários;
        Digite [5] para Voltar ao menu anterior.
=>  '''

menuInicial = f'''
    Bem vindo ao Banco {bancoBBB.nome}!

        Digite [1] para Área do usuário;
        Digite [2] para Área de operações bancárias;
        Digite [3] para Sair.
=>  '''

while True:
    opi = int(input(menuInicial))
    match opi:
        case 1:  # Menu de usuários
            while True:
                opu = int(input(menuUsuario))

                match opu:
                    case 1:
                        cadastrar_cliente()
                        break
                    case 2:
                        # iteração
                        cpf = int(input("Digite o cpf do usuário: "))

                        usuario = bancoBBB.procurar_cliente(cpf=cpf)

                        if usuario[0] == True:
                            usuario[1].mostrar_contas()
                        else:
                            print("Usuário não encontrado!")
                        break
                    case 3:
                        cadastrar_conta()
                        break
                    case 4:
                        bancoBBB.listar_usuarios()
                        break
                    case 5:
                        break
                    case _:
                        print("Operação inválida, digite uma opção válida para realizar a operação desejada.")
                        break

        case 2:  # Menu de operações
            while True:
                opo = int(input(menuOperacoes))
                match opo:
                    case 1:
                        depositar()
                        break
                    case 2:
                        sacar()
                        break
                    case 3:
                        exibir_extrato()
                        break
                    case 4:
                        break
                    case _:
                        print("Operação inválida, digite uma opção válida para realizar a operação desejada.")
                        break

        case 3:
            break
        case _:
            print("Operação inválida, digite uma opção válida para realizar a operação desejada.")
