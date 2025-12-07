# Nome: Gustavo dos Santos Garrido



import json

import datetime

import os



def salvar_funcionario(funcionario: dict, filepath: str = "data/funcionarios.json"):

    """

    Salva (anexa) um funcionário no arquivo JSON especificado.

    Se o arquivo não existir, cria uma lista nova.

    """

    # garante que a pasta exista

    dirpath = os.path.dirname(filepath) or "."

    if dirpath and not os.path.exists(dirpath):

        os.makedirs(dirpath, exist_ok=True)



    # lê lista existente (ou inicia vazia)

    data = []

    if os.path.exists(filepath):

        try:

            with open(filepath, "r", encoding="utf-8") as f:

                data = json.load(f)

                if not isinstance(data, list):

                    data = []

        except Exception:

            data = []



    data.append(funcionario)



    # grava de volta

    with open(filepath, "w", encoding="utf-8") as f:

        json.dump(data, f, ensure_ascii=False, indent=2)



SETORES_DA_EMPRESA = {

    """

    Aqui estão os setores e seus respectivos cargos com valores por hora, será como os valores base.

    """

    "OPERACIONAL": {

        "Auxiliar de Produção": 6.90,

        "Operador de Máquinas": 8.50,

        "Técnico de Manutenção": 12.00,

        "Inspetor de Qualidade": 10.00,

    },

    "ESTOQUE": {

        "Auxiliar de Estoque": 7.00,

        "Analista": 8.00,

        "Coordenador": 11.00,

    },

    "FINANCEIRO": {

        "Assistente Financeiro": 9.00,

        "Analista Financeiro": 12.50,

        "Gerente Financeiro": 15.00,

    },

    "RH": {

        "Assistente de RH": 9.50,

        "Analista de RH": 11.50,

        "Coordenador de RH": 14.00,

    },

}

def selecionar_setor():

    """

    Mostra os setores disponíveis e permite selecionar um deles.

    """

    print("\n--- SELEÇÃO DE SETOR ---")

    print("1. Operacional")

    print("2. Estoque")

    print("3. Financeiro")

    print("4. RH")

   

    nome_setor = ""

    cargos_setor = {}

   

    while True:

        try:

            escolha_setor = input("Selecione o setor do contratado (1-4): ")

            match escolha_setor:

                case '1':

                    nome_setor = "OPERACIONAL"

                    # Acessamos o dicionário interno do setor escolhido:

                    cargos_setor = SETORES_DA_EMPRESA[nome_setor]

                    break  # Sai do loop externo

                case '2':

                    nome_setor = "ESTOQUE"

                    cargos_setor = SETORES_DA_EMPRESA[nome_setor]

                    break

                case '3':

                    nome_setor = "FINANCEIRO"

                    cargos_setor = SETORES_DA_EMPRESA[nome_setor]

                    break

                case '4':

                    nome_setor = "RH"

                    cargos_setor = SETORES_DA_EMPRESA[nome_setor]

                    break

                case _:

                    print("Opção de setor inválida. Tente novamente.")

        except Exception:

            print("Entrada inválida. Digite um número.")

   

    return nome_setor, cargos_setor

def selecionar_cargo(cargos_setor: dict):

    """

    Mostra as funções do setor e permite selecionar uma delas.

    Retorna uma tupla (nome_cargo, valor_hora)

    """

    print("\n--- SELEÇÃO DE FUNÇÃO ---")

    lista_funcoes = list(cargos_setor.items())

    for i, (nome, valor) in enumerate(lista_funcoes, start=1):

        print(f"{i}. {nome} (R$ {valor:.2f})")



    while True:

        escolha = input(f"Selecione a função (1-{len(lista_funcoes)}): ")

        try:

            idx = int(escolha)

            if 1 <= idx <= len(lista_funcoes):

                nome_cargo, valor_hora = lista_funcoes[idx - 1]

                return nome_cargo, valor_hora

            else:

                print("Opção inválida. Tente novamente.")

        except ValueError:

            print("Entrada inválida. Digite um número.")
            
def cadastrar_funcionario():

    """

    Cadastra um funcionário interativamente e retorna um dicionário com os dados.

    """

    nome = input("Nome do funcionário: ")

    cpf = input("CPF do funcionário: ")

    rg = input("RG do funcionário: ")

    endereco = input("Endereço do funcionário: ")

    telefone = input("Telefone do funcionário: ")

    qtd_filhos = input("Quantidade de filhos do funcionário: ")

    # Seleciona setor e função automaticamente

    nome_setor, cargos_setor = selecionar_setor()

    cargo, valor_hora = selecionar_cargo(cargos_setor)

    print(f"Função selecionada: {cargo} — R$ {valor_hora:.2f}")

    # normaliza tipos

    try:

        qtd_filhos = int(qtd_filhos)

    except Exception:

        qtd_filhos = 0



    try:

        valor_hora = float(valor_hora)

    except Exception:

        # fallback: se por algum motivo não for possível converter, usa 0.0

        valor_hora = 0.0



    funcionarios = {

        "nome": nome,

        "cpf": cpf,

        "rg": rg,

        "endereco": endereco,

        "telefone": telefone,

        "qtd_filhos": qtd_filhos,

        "cargo": cargo,

        "valor_hora": valor_hora,

        "data_cadastro": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    }

   

    # salva em JSON

    try:

        salvar_funcionario(funcionarios)

    except Exception:

        # não falhar o fluxo caso o salvamento dê problema; apenas segue retornando

        pass



    return funcionarios

def carregar_todos_funcionarios(filepath: str = "data/funcionarios.json") -> list:

    """

    Carrega todos os registros do arquivo JSON. Retorna uma lista vazia se não encontrar ou houver erro.

    """

    if not os.path.exists(filepath):

        return []

    try:

        with open(filepath, "r", encoding="utf-8") as f:

            data = json.load(f)

            if isinstance(data, list):

                return data

            else:

                return []

    except Exception as e:

        print("Er ao carregar os dados do arquivo: {e}")

        return []