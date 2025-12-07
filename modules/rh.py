# Nome: Gustavo dos Santos Garrido
# Módulo: Recursos Humanos
# Descrição: Gerencia cadastro de funcionários e folha de pagamento.

import json
import datetime
import os


def salvar_funcionario(dados_a_salvar: list, filepath: str = "data/funcionarios.json"):
    """
    Salva (anexa) um funcionário no arquivo JSON especificado.
    Se o arquivo não existir, cria uma lista nova.
    """
    # garante que a pasta exista
    dirpath = os.path.dirname(filepath) or "."
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(dados_a_salvar, f, ensure_ascii=False, indent=2)
        
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
        print(f"Erro ao carregar os dados do arquivo: {e}")
        return []


# Aqui estão os setores e seus respectivos cargos com valores por hora (valores base).
SETORES_DA_EMPRESA = {
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
        "Coordenador de RH": 14.00
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
            
            
def cadastrar_funcionario(filepath: str = "data/funcionarios.json"):
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
    _, cargos_setor = selecionar_setor()
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

    novo_funcionario = {

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

    cadastro_completo = carregar_todos_funcionarios(filepath)
    cadastro_completo.append(novo_funcionario)

    try:
        salvar_funcionario(cadastro_completo, filepath)
        print(f"\n✨ Funcionário '{nome}' cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar o cadastro: {e}")
        pass 

    return novo_funcionario
    
    
def listar_funcionarios():
    """
    Lista todos os funcionários cadastrados no sistema.
    """
    
    cadastrados = carregar_todos_funcionarios()
    
    if not cadastrados:
        print("Nenhum funcionário cadastrado.")
        return
    
    print(">>> === Lista dos funcionarios === <<<")
    
    for indice, funcionario in enumerate(cadastrados, start=1):

        nome = funcionario.get('nome', 'NOME INDISPONÍVEL')
        cargo = funcionario.get('cargo', 'CARGO INDISPONÍVEL')
        cpf = funcionario.get('cpf', 'CPF NÃO INFORMADO')

        print(f"\n{indice}. Nome: {nome}")
        print(f"   CPF: {cpf}")
        print(f"   Cargo: {cargo}")


def editar_funcionarios(filepath: str = "data/funcionarios.json"):
    """
    Permite ao usuário selecionar um funcionário da lista e editar seus dados.
    """

    print(">>> === Editar Funcionários Cadastrados === <<<")
    cadastro = carregar_todos_funcionarios(filepath)

    if not cadastro:
        print(" Cadastro vazio. Nada para editar.")
        return

    listar_funcionarios()

    while True:
        try:
            escolha_indice = input("Digite o NÚMERO do funcionário que deseja EDITAR: ")
            indice_selecionado = int(escolha_indice) - 1

            if 0 <= indice_selecionado < len(cadastro):
                break
            else:
                print("Número fora do intervalo da lista.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

    # Acessa o dicionário do funcionário escolhido:
    editar = cadastro[indice_selecionado]
    nome_atual = editar.get('nome')

    print(f"\n✅ Selecionado para edição: **{nome_atual}** (CPF: {editar.get('cpf')})")

    #Aqui começa a edição dos campos: pode ser editado o nome, endereço e telefone.
    print("\nQuais campos deseja alterar? (Deixe em branco para manter o valor atual)")
   
    novo_nome = input(f"Novo Nome (Atual: {editar['nome']}): ").strip()
    if novo_nome:
        editar['nome'] = novo_nome

    novo_endereco = input(f"Novo Endereço (Atual: {editar['endereco']}): ").strip()
    if novo_endereco:
        editar['endereco'] = novo_endereco

    novo_telefone = input(f"Novo Telefone (Atual: {editar['telefone']}): ").strip()
    if novo_telefone:
        editar['telefone'] = novo_telefone
    print("\nPara alterar o cargo ou setor, é necessário apagar o cadastro atual e refazer o cadastro com as novas informações.")

    try:
        salvar_funcionario(cadastro, filepath)
        print(f"\nDados de '{editar['nome']}' atualizados com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar as alterações: {e}")
              
def deletar_funcionarios(filepath: str = "data/funcionarios.json"):
    """
    Permite ao usuário selecionar um funcionário da lista (pelo índice) e removê-lo permanentemente do cadastro.
    """
    
    print("\n>>> === Deletar Funcionário Cadastrado === <<<")
    
    
    cadastro = carregar_todos_funcionarios(filepath)
    
    if not cadastro:
        print("Cadastro vazio. Nada para deletar.")
        return

    listar_funcionarios()
    
    while True:
        try:
            escolha_indice = input("Digite o NÚMERO do funcionário que deseja DELETAR: ")
            indice_selecionado = int(escolha_indice) - 1

            if 0 <= indice_selecionado < len(cadastro):
                break
            else:
                print("Número fora do intervalo da lista.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")
            
    remover = cadastro[indice_selecionado]
    nome = remover.get('nome', 'Funcionário Desconhecido')
    
    confirmacao = input(f"❗ TEM CERTEZA que deseja DELETAR **{nome}**? (s/n): ").lower()
    
    if confirmacao == 's':
        cadastro.pop(indice_selecionado)
        
        print(f"Funcionário **{nome}** removido do cadastro.")
        
        salvar_funcionario(cadastro, filepath) 
    else:
        print("Operação cancelada. O cadastro não foi deletado.")
        
def calcular_salario_bruto(horas_trabalhadas, valor_hora):
    """
    Calcula salário bruto base.
    """
    return horas_trabalhadas * valor_hora

def calcular_horas_extras(horas_extras, valor_hora, cargo):
    """
    Calcula valor das horas extras.
    Gerentes e Diretores não recebem hora extra.
    """
    cargos_sem_extra = ["gerente", "diretor"]
    if cargo.lower() in cargos_sem_extra:
        return 0.0
    
    # Adicional de 50% na hora extra (padrão CLT simples para o exercício)
    valor_extra = horas_extras * (valor_hora * 1.5)
    return valor_extra

def calcular_irpf(salario_base):
    """
    Calcula o IRPF com base em tabela simplificada (exemplo 2024).
    """
    # Tabela progressiva simplificada (valores aproximados para exercício)
    if salario_base <= 2259.20:
        return 0.0
    elif salario_base <= 2826.65:
        return (salario_base * 0.075) - 169.44
    elif salario_base <= 3751.05:
        return (salario_base * 0.15) - 381.44
    elif salario_base <= 4664.68:
        return (salario_base * 0.225) - 662.77
    else:
        return (salario_base * 0.275) - 896.00

def calcular_liquido(salario_bruto, irpf):
    """
    Calcula salário líquido (Bruto - IRPF).
    Ignorando INSS para simplificação conforme enunciado foca em IRPF e faixas de desconto.
    """
    return salario_bruto - irpf

def gerar_folha_pagamento():
    """
    Gera relatório final com salários líquidos e IRPF.
    """
    print("\n--- Folha de Pagamento ---")
    
    # Carregar funcionários cadastrados
    funcionarios = carregar_todos_funcionarios()
    
    if not funcionarios:
        print("Nenhum funcionário cadastrado para gerar folha.")
        return
    
    # Ordenar por nome
    funcionarios_ordenados = sorted(funcionarios, key=lambda x: x["nome"])
    
    for f in funcionarios_ordenados:
        # Simulação de horas para o relatório (em um sistema real, viria de input ou ponto)
        horas_trab = 220 # Mensal padrão
        horas_ext = float(input("Informe a quantidade de horas extras: "))  # Exemplo
        
        bruto = calcular_salario_bruto(horas_trab, f["valor_hora"])
        extra = calcular_horas_extras(horas_ext, f["valor_hora"], f["cargo"])
        total_bruto = bruto + extra
        
        irpf = calcular_irpf(total_bruto)
        liquido = calcular_liquido(total_bruto, irpf)
        
        paga_ir = "Sim" if irpf > 0 else "Não"
        
        print(f"Nome: {f['nome']}")
        print(f"  Cargo: {f['cargo']}")
        print(f"  Salário Bruto: R$ {total_bruto:.2f}")
        print(f"  IRPF: R$ {irpf:.2f} ({paga_ir})")
        print(f"  Salário Líquido: R$ {liquido:.2f}")
        print("-" * 30)