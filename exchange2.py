
import random
from datetime import datetime

moedas = ["bitcoin", "ethereum", "ripple"]

siglas = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "ripple": "XRP"
}

taxa_compra = {
    "bitcoin": 0.02,
    "ethereum": 0.01,
    "ripple": 0.01
}

taxa_venda = {
    "bitcoin": 0.03,
    "ethereum": 0.02,
    "ripple": 0.01
}

def criar_arquivos():

    arquivos = ["investidores.txt", "cotacoes.txt", "extratos.txt"]

    for nome in arquivos:
        arquivo = open(nome, "a")
        arquivo.close()

    arquivo = open("cotacoes.txt", "r")
    linhas = arquivo.readlines()
    arquivo.close()

    if len(linhas) == 0:
        arquivo = open("cotacoes.txt", "w")
        arquivo.write("350000.00;16000.00;2.50\n")
        arquivo.close()

    arquivo = open("investidores.txt", "r")
    linhas = arquivo.readlines()
    arquivo.close()

    if len(linhas) == 0:
        arquivo = open("investidores.txt", "w")
        arquivo.write("53860919806;Yvis Morales;123321;999999999.00;0.0;0.0;0.0\n")
        arquivo.close()

def carregar_cotacoes():

    arquivo = open("cotacoes.txt", "r")
    dados = arquivo.readlines()[0].strip().split(";")
    arquivo.close()

    cotacoes = {}

    for i in range(3):
        cotacoes[moedas[i]] = float(dados[i])

    return cotacoes


def salvar_cotacoes(cotacoes):

    arquivo = open("cotacoes.txt", "w")

    arquivo.write("%.2f;%.2f;%.2f\n" % (
        cotacoes["bitcoin"],
        cotacoes["ethereum"],
        cotacoes["ripple"]
    ))

    arquivo.close()

def carregar_investidores():

    investidores = {}

    arquivo = open("investidores.txt", "r")

    for linha in arquivo.readlines():

        dados = linha.strip().split(";")

        investidores[dados[0]] = {
            "nome": dados[1],
            "senha": dados[2],
            "reais": float(dados[3]),
            "bitcoin": float(dados[4]),
            "ethereum": float(dados[5]),
            "ripple": float(dados[6])
        }

    arquivo.close()

    return investidores


def salvar_investidores(investidores):

    arquivo = open("investidores.txt", "w")

    for cpf in investidores:

        pessoa = investidores[cpf]

        arquivo.write("%s;%s;%s;%.2f;%.8f;%.8f;%.8f\n" % (
            cpf,
            pessoa["nome"],
            pessoa["senha"],
            pessoa["reais"],
            pessoa["bitcoin"],
            pessoa["ethereum"],
            pessoa["ripple"]
        ))

    arquivo.close()

def registrar_extrato(cpf, pessoa, operacao, valor, moeda, cotacao, taxa):

    data = datetime.now().strftime("%d-%m-%Y %H:%M")

    arquivo = open("extratos.txt", "a")

    arquivo.write("%s;%s;%s;%.2f;%s;%.2f;%.2f;%.2f;%.8f;%.8f;%.8f\n" % (
        cpf,
        data,
        operacao,
        valor,
        moeda,
        cotacao,
        taxa,
        pessoa["reais"],
        pessoa["bitcoin"],
        pessoa["ethereum"],
        pessoa["ripple"]
    ))

    arquivo.close()

def ler_valor(mensagem):

    texto = input(mensagem).replace(",", ".")

    if texto.replace(".", "", 1).isdigit():
        return float(texto)

    return -1


def confirmar_senha(pessoa):

    senha = input("Digite sua senha: ")

    if senha == pessoa["senha"]:
        return True

    print("Senha incorreta!")
    return False


def formatar_cpf(cpf):

    return cpf[0:3] + "." + cpf[3:6] + "." + cpf[6:9] + "-" + cpf[9:11]



# Consulta de saldo e extrato

def consultar_saldo(cpf, investidores):

    pessoa = investidores[cpf]

    print("\nSEU SALDO")
    print("Nome:", pessoa["nome"])
    print("CPF:", formatar_cpf(cpf))
    print("Reais: R$ %.2f" % pessoa["reais"])
    print("Bitcoin: %.4f" % pessoa["bitcoin"])
    print("Ethereum: %.4f" % pessoa["ethereum"])
    print("Ripple: %.4f" % pessoa["ripple"])


def consultar_extrato(cpf, investidores):

    pessoa = investidores[cpf]

    print("\n===== SEU EXTRATO =====")
    print("Nome:", pessoa["nome"])
    print("CPF:", formatar_cpf(cpf))

    arquivo = open("extratos.txt", "r")

    for linha in arquivo.readlines():

        dados = linha.strip().split(";")

        if dados[0] == cpf:

            print("%s | %s | R$ %s | %s | Cotação: %s | Taxa: %s" % (
                dados[1],
                dados[2],
                dados[3],
                dados[4],
                dados[5],
                dados[6]
            ))

    arquivo.close()

# Depósito e saque
def depositar(cpf, investidores):

    valor = ler_valor("Digite o valor que deseja depositar: R$ ")

    if valor <= 0:
        print("Valor inválido!")

    else:

        investidores[cpf]["reais"] += valor

        salvar_investidores(investidores)

        registrar_extrato(
            cpf, investidores[cpf], "+", valor, "REAL", 0.0, 0.0
        )

        print("Depósito realizado com sucesso!")

        consultar_saldo(cpf, investidores)


def sacar(cpf, investidores):

    valor = ler_valor("Digite o valor que deseja sacar: R$ ")

    if valor <= 0:
        print("Valor inválido!")

    elif valor > investidores[cpf]["reais"]:
        print("Você não possui saldo suficiente!")

    else:

        investidores[cpf]["reais"] -= valor

        salvar_investidores(investidores)

        registrar_extrato(
            cpf, investidores[cpf], "-", valor, "REAL", 0.0, 0.0
        )

        print("Saque realizado com sucesso!")

        consultar_saldo(cpf, investidores)

def escolher_moeda():

    cotacoes = carregar_cotacoes()

    print("\nCRIPTOMOEDAS DISPONÍVEIS")

    for i in range(3):

        moeda = moedas[i]

        print("%d - %s (%s)" % (
            i + 1,
            moeda,
            siglas[moeda]
        ))

        print("Cotação: R$ %.2f" % cotacoes[moeda])
        print("Taxa de compra: %d%%" % (taxa_compra[moeda] * 100))
        print("Taxa de venda: %d%%\n" % (taxa_venda[moeda] * 100))

    opcao = input("Escolha uma moeda (1 a 3): ")

    if opcao.isdigit():

        if 1 <= int(opcao) <= 3:
            return moedas[int(opcao) - 1]

    print("Opção inválida!")
    return ""


def comprar(cpf, investidores):

    moeda = escolher_moeda()

    if moeda == "":
        return

    cotacoes = carregar_cotacoes()

    valor = ler_valor("Quanto deseja investir em reais? R$ ")

    if valor <= 0:
        print("Valor inválido!")
        return

    taxa = valor * taxa_compra[moeda]

    pessoa = investidores[cpf]

    if valor + taxa > pessoa["reais"]:

        print("Saldo insuficiente para realizar a compra!")

    else:

        quantidade = valor / cotacoes[moeda]

        pessoa["reais"] -= valor + taxa
        pessoa[moeda] += quantidade

        salvar_investidores(investidores)

        registrar_extrato(
            cpf, pessoa, "+", valor, siglas[moeda], cotacoes[moeda], taxa
        )

        print("\nCompra realizada com sucesso!")
        print("Quantidade comprada: %.6f %s" % (
            quantidade, siglas[moeda]
        ))
        print("Taxa cobrada: R$ %.2f" % taxa)

def vender(cpf, investidores):

    moeda = escolher_moeda()

    if moeda == "":
        return

    cotacoes = carregar_cotacoes()

    pessoa = investidores[cpf]

    print("Você possui %.6f %s" % (
        pessoa[moeda],
        siglas[moeda]
    ))

    valor = ler_valor("Quanto deseja vender em reais? R$ ")

    if valor <= 0:
        print("Valor inválido!")
        return

    quantidade = valor / cotacoes[moeda]

    if quantidade > pessoa[moeda]:

        print("Você não possui criptomoedas suficientes!")

    else:

        taxa = valor * taxa_venda[moeda]

        pessoa[moeda] -= quantidade
        pessoa["reais"] += valor - taxa

        salvar_investidores(investidores)

        registrar_extrato(
            cpf, pessoa, "-", valor, siglas[moeda], cotacoes[moeda], taxa
        )

        print("\nVenda realizada com sucesso!")
        print("Quantidade vendida: %.6f %s" % (
            quantidade, siglas[moeda]
        ))
        print("Valor recebido: R$ %.2f" % (valor - taxa))
        print("Taxa cobrada: R$ %.2f" % taxa)


def atualizar_cotacao():

    cotacoes = carregar_cotacoes()

    print("\nATUALIZAÇÃO DAS COTAÇÕES")

    for moeda in moedas:

        variacao = random.uniform(-0.05, 0.05)

        cotacoes[moeda] = cotacoes[moeda] * (1 + variacao)

        print("%s: R$ %.2f (%+.2f%%)" % (
            moeda,
            cotacoes[moeda],
            variacao * 100
        ))

    salvar_cotacoes(cotacoes)

    print("\nCotações atualizadas!")


def menu_investidor(cpf):

    while True:

        investidores = carregar_investidores()

        print("\nEXCHANGE DE CRIPTOMOEDAS")
        print("1 - Consultar saldo")
        print("2 - Consultar extrato")
        print("3 - Depositar dinheiro")
        print("4 - Sacar dinheiro")
        print("5 - Comprar criptomoedas")
        print("6 - Vender criptomoedas")
        print("7 - Atualizar cotações")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":

            if confirmar_senha(investidores[cpf]):
                consultar_saldo(cpf, investidores)

        elif opcao == "2":

            if confirmar_senha(investidores[cpf]):
                consultar_extrato(cpf, investidores)

        elif opcao == "3":

            depositar(cpf, investidores)

        elif opcao == "4":

            sacar(cpf, investidores)

        elif opcao == "5":

            if confirmar_senha(investidores[cpf]):
                comprar(cpf, investidores)

        elif opcao == "6":

            if confirmar_senha(investidores[cpf]):
                vender(cpf, investidores)

        elif opcao == "7":

            atualizar_cotacao()

        elif opcao == "0":

            print("Tchau!!!")
            break

        else:

            print("Opção inválida! Tente novamente.")

def main():

    criar_arquivos()

    print("===== BEM-VINDO À EXCHANGE =====")

    cpf = input("Digite seu CPF (somente números): ")
    senha = input("Digite sua senha: ")

    investidores = carregar_investidores()

    if cpf in investidores and investidores[cpf]["senha"] == senha:

        print("\nLogin realizado com sucesso!")

        menu_investidor(cpf)

    else:

        print("\nCPF ou senha incorretos!")


main()
