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
        print(f"\nFuncionário '{nome}' cadastrado com sucesso!")
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

    print(f"\n✅ Selecionado para edição: {nome_atual} (CPF: {editar.get('cpf')})")

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
    cargo_lower = cargo.lower()
    cargos_sem_extra = ["gerente", "diretor"]
    
    # Verifica se algum dos cargos sem extra está CONTIDO no cargo
    tem_restricao = any(restricao in cargo_lower for restricao in cargos_sem_extra)
    
    if tem_restricao:
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

def obter_setor_funcionario(cargo: str) -> str:
    """
    Identifica o setor do funcionário baseado no cargo.
    Retorna o setor ou None se não encontrado.
    """
    for setor, cargos_dict in SETORES_DA_EMPRESA.items():
        if cargo in cargos_dict:
            return setor
    return None

def gerar_folha_pagamento():
    """
    Gera relatório de folha de pagamento com seleção por setor e funcionário.
    Permite selecionar qual funcionário calcular a folha de pagamento.
    """
    # Carregar funcionários cadastrados
    funcionarios = carregar_todos_funcionarios()
    
    if not funcionarios:
        print("Nenhum funcionário cadastrado para gerar folha.")
        return
    
    # Organizar funcionários por setor
    funcionarios_por_setor = {}
    for f in funcionarios:
        setor = obter_setor_funcionario(f["cargo"])
        if setor:
            if setor not in funcionarios_por_setor:
                funcionarios_por_setor[setor] = []
            funcionarios_por_setor[setor].append(f)
    
    if not funcionarios_por_setor:
        print("Nenhum funcionário com setor válido encontrado.")
        return
    
    # Menu de seleção de setor
    setores_lista = sorted(funcionarios_por_setor.keys())
    
    print("\n" + "=" * 70)
    print("SELEÇÃO DE SETOR PARA FOLHA DE PAGAMENTO")
    print("=" * 70)
    
    for i, setor in enumerate(setores_lista, start=1):
        qtd_func = len(funcionarios_por_setor[setor])
        print(f"{i}. {setor} ({qtd_func} funcionário(s))")
    print(f"{len(setores_lista) + 1}. Gerar folha de TODOS os setores")
    print("0. Cancelar")
    print("=" * 70)
    
    while True:
        try:
            escolha_setor = input("Selecione o setor (ou 0 para cancelar): ").strip()
            escolha_setor_idx = int(escolha_setor)
            
            if escolha_setor_idx == 0:
                print("Operação cancelada.")
                return
            elif escolha_setor_idx == len(setores_lista) + 1:
                # Gerar para todos os setores
                gerar_folha_todos_setores(funcionarios_por_setor, setores_lista)
                return
            elif 1 <= escolha_setor_idx <= len(setores_lista):
                setor_selecionado = setores_lista[escolha_setor_idx - 1]
                gerar_folha_setor(setor_selecionado, funcionarios_por_setor[setor_selecionado])
                return
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

def gerar_folha_setor(setor: str, funcionarios_setor: list):
    """
    Gera a folha de pagamento para um setor específico.
    Permite selecionar qual funcionário calcular.
    """
    print("\n" + "=" * 70)
    print(f"FOLHA DE PAGAMENTO - SETOR: {setor}")
    print("=" * 70)
    
    # Ordenar por nome
    funcionarios_ordenados = sorted(funcionarios_setor, key=lambda x: x["nome"])
    
    # Menu de seleção de funcionário
    print("\nSELECIONE UM FUNCIONÁRIO:")
    print("-" * 70)
    
    for i, f in enumerate(funcionarios_ordenados, start=1):
        print(f"{i}. {f['nome']:40} ({f['cargo']})")
    
    print("0. Voltar")
    print("-" * 70)
    
    while True:
        try:
            escolha_func = input("Selecione o funcionário: ").strip()
            escolha_func_idx = int(escolha_func)
            
            if escolha_func_idx == 0:
                return
            elif 1 <= escolha_func_idx <= len(funcionarios_ordenados):
                funcionario_selecionado = funcionarios_ordenados[escolha_func_idx - 1]
                calcular_folha_funcionario(funcionario_selecionado)
                return
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

def gerar_folha_todos_setores(funcionarios_por_setor: dict, setores_lista: list):
    """
    Gera a folha de pagamento para todos os setores.
    """
    print("\n" + "=" * 70)
    print("FOLHA DE PAGAMENTO - TODOS OS SETORES")
    print("=" * 70)
    
    total_geral_bruto = 0.0
    total_geral_irpf = 0.0
    total_geral_liquido = 0.0
    
    for setor in setores_lista:
        funcionarios_ordenados = sorted(funcionarios_por_setor[setor], key=lambda x: x["nome"])
        
        print("\n" + "─" * 70)
        print(f"SETOR: {setor}")
        print("─" * 70)
        
        for f in funcionarios_ordenados:
            # Input de horas
            print(f"\n[{f['nome']}]")
            try:
                horas_trab = float(input(f"  Horas trabalhadas (padrão 220h): ") or "220")
                horas_ext = float(input(f"  Horas extras: ") or "0")
            except ValueError:
                horas_trab = 220.0
                horas_ext = 0.0
            
            # Cálculos
            bruto = calcular_salario_bruto(horas_trab, f["valor_hora"])
            extra = calcular_horas_extras(horas_ext, f["valor_hora"], f["cargo"])
            total_bruto = bruto + extra
            irpf = calcular_irpf(total_bruto)
            liquido = calcular_liquido(total_bruto, irpf)
            
            # Acumular totais
            total_geral_bruto += total_bruto
            total_geral_irpf += irpf
            total_geral_liquido += liquido
            
            # Exibir
            paga_ir = "Sim" if irpf > 0 else "Não"
            print(f"  Cargo: {f['cargo']:35} | Valor/hora: R$ {f['valor_hora']:7.2f}")
            print(f"  Salário Base ({horas_trab:6.0f}h): R$ {bruto:10.2f}")
            print(f"  Horas Extras ({horas_ext:6.0f}h + 50%): R$ {extra:10.2f}")
            print(f"  ├─ Total Bruto: R$ {total_bruto:10.2f}")
            print(f"  ├─ IRPF: R$ {irpf:10.2f} ({paga_ir})")
            print(f"  └─ Líquido: R$ {liquido:10.2f}")
    
    # Resumo geral
    print("\n" + "=" * 70)
    print("RESUMO GERAL - TODOS OS SETORES")
    print("=" * 70)
    print(f"Total Bruto Geral: R$ {total_geral_bruto:10.2f}")
    print(f"Total IRPF Geral:  R$ {total_geral_irpf:10.2f}")
    print(f"Total Líquido Geral: R$ {total_geral_liquido:10.2f}")
    print("=" * 70)

def calcular_folha_funcionario(funcionario: dict):
    """
    Calcula e exibe a folha de pagamento de um funcionário específico.
    """
    print("\n" + "=" * 70)
    print(f"FOLHA DE PAGAMENTO - {funcionario['nome'].upper()}")
    print("=" * 70)
    
    # Dados pessoais
    print("\n[DADOS PESSOAIS]")
    print(f"Nome: {funcionario['nome']}")
    print(f"CPF: {funcionario['cpf']}")
    print(f"RG: {funcionario['rg']}")
    print(f"Endereço: {funcionario['endereco']}")
    print(f"Telefone: {funcionario['telefone']}")
    
    # Input de horas
    print("\n[INFORMAÇÕES DE HORAS]")
    try:
        horas_trab = float(input("Horas trabalhadas (padrão 220h): ") or "220")
        horas_ext = float(input("Horas extras: ") or "0")
    except ValueError:
        horas_trab = 220.0
        horas_ext = 0.0
    
    # Cálculos
    print("\n[CÁLCULOS]")
    bruto = calcular_salario_bruto(horas_trab, funcionario["valor_hora"])
    extra = calcular_horas_extras(horas_ext, funcionario["valor_hora"], funcionario["cargo"])
    total_bruto = bruto + extra
    irpf = calcular_irpf(total_bruto)
    liquido = calcular_liquido(total_bruto, irpf)
    
    paga_ir = "Sim" if irpf > 0 else "Não"
    
    # Exibição formatada
    print(f"Cargo: {funcionario['cargo']}")
    print(f"Valor/hora: R$ {funcionario['valor_hora']:.2f}")
    print(f"Quantidade de filhos: {funcionario['qtd_filhos']}")
    
    print("\n[FOLHA DE PAGAMENTO]")
    print(f"Salário Base ({horas_trab:.0f}h × R${funcionario['valor_hora']:.2f}): R$ {bruto:10.2f}")
    print(f"Horas Extras ({horas_ext:.0f}h + 50%): R$ {extra:10.2f}")
    print("-" * 70)
    print(f"Total Bruto: R$ {total_bruto:10.2f}")
    print(f"IRPF (-): R$ {irpf:10.2f}")
    print(f"Paga IRPF: {paga_ir}")
    print("=" * 70)
    print(f"SALÁRIO LÍQUIDO: R$ {liquido:10.2f}")
    print("=" * 70)