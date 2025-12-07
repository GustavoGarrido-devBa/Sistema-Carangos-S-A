import os
import sys
import time
import getpass
from werkzeug.security import check_password_hash

# Import modules
from modules import operacional, estoque, financeiro, rh, data_manager

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nPressione Enter para continuar...")

def login():
    """
    Função de login. 
    NOTA: getpass.getpass() não funciona bem no VS Code terminal.
    Use input() normal ou pressione Enter para pular o login (modo teste).
    """
    while True:
        clear_screen()
        print("="*40)
        print("   CARANGOS S/A - LOGIN")
        print("="*40)
        print("\n[DICA] Pressione Enter sem digitar nada para pular o login (modo teste)")
        
        username = input("\nUsuário: ").strip()
        
        # Opção de pular login para teste
        if not username:
            print("\n✓ Entrando em modo teste (sem autenticação)...")
            time.sleep(1)
            return {'username': 'teste', 'role': 'admin'}
        
        # Usar input() ao invés de getpass() para compatibilidade com VS Code
        password = input("Senha: ").strip()
        
        users = data_manager.load_data('users.json')
        
        # Se não houver usuários cadastrados, permitir acesso
        if not users:
            print("\n⚠ Nenhum usuário cadastrado. Criando acesso padrão...")
            print("✓ Entrando como administrador...")
            time.sleep(1)
            return {'username': username, 'role': 'admin'}
        
        user = next((u for u in users if u['username'] == username), None)
        
        if user and check_password_hash(user['password'], password):
            print(f"\n✓ Bem-vindo, {username}!")
            time.sleep(1)
            return user
        else:
            print("\n✗ Usuário ou senha inválidos!")
            time.sleep(1)
            
            retry = input("\nTentar novamente? (S/N): ").upper()
            if retry != 'S':
                print("Saindo...")
                sys.exit()

def menu_principal(user):
    while True:
        clear_screen()
        print("="*40)
        print(f"   CARANGOS S/A - SISTEMA INTEGRADO ({user['role']})")
        print("="*40)
        print("1. Módulo Operacional")
        print("2. Módulo de Estoque")
        print("3. Módulo Financeiro")
        print("4. Módulo de RH")
        print("0. Sair")
        print("="*40)
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            menu_operacional()
        elif opcao == '2':
            menu_estoque()
        elif opcao == '3':
            menu_financeiro()
        elif opcao == '4':
            menu_rh()
        elif opcao == '0':
            print("Saindo do sistema...")
            sys.exit()
        else:
            print("Opção inválida!")
            time.sleep(1)

def menu_operacional():
    while True:
        clear_screen()
        print("="*40)
        print("   MÓDULO OPERACIONAL")
        print("="*40)
        print("1. Registrar Produção Semanal")
        print("2. Ver Relatório de Produção")
        print("0. Voltar")
        print("="*40)
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            operacional.cadastrar_producao()
            pause()
        elif opcao == '2':
            # Load data
            dados_flat = data_manager.load_data('producao.json')
            
            # Reconstruct structure
            dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
            dados_estruturados = []
            
            for dia in dias_semana:
                turnos_dia = {"Manhã": 0, "Tarde": 0, "Noite": 0}
                rows = [row for row in dados_flat if row['dia'] == dia]
                for row in rows:
                    if row['turno'] in turnos_dia:
                        turnos_dia[row['turno']] += row['quantidade']
                dados_estruturados.append({"dia": dia, "turnos": turnos_dia})
            
            stats = operacional.calcular_estatisticas(dados_estruturados)
            ideal = operacional.calcular_capacidade_ideal()
            operacional.gerar_relatorio(dados_estruturados, stats, ideal)
            pause()
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")
            time.sleep(1)

def menu_estoque():
    while True:
        clear_screen()
        print("="*40)
        print("   MÓDULO DE ESTOQUE")
        print("="*40)
        print("1. Cadastrar Produto")
        print("2. Buscar Produto")
        print("3. Ver Relatório de Custos")
        print("0. Voltar")
        print("="*40)
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            print("\n--- Cadastro de Produto ---")
            try:
                codigo = int(input("Código: "))
                nome = input("Nome: ")
                data_fab = input("Data Fabricação (dd/mm/aaaa): ")
                fornecedor = input("Fornecedor: ")
                quantidade = int(input("Quantidade: "))
                valor_compra = float(input("Valor de Compra: R$ "))
                
                estoque.cadastrar_produto(codigo, nome, data_fab, fornecedor, quantidade, valor_compra)
            except ValueError:
                print("Erro: Valores inválidos!")
            pause()
        elif opcao == '2':
            termo = input("\nDigite o termo de busca (Nome ou Código): ")
            resultados = estoque.pesquisar_produto(termo)
            print("\n--- Resultados ---")
            for p in resultados:
                print(f"Cód: {p['codigo']} | {p['nome']} | Qtd: {p['quantidade']} | R$ {p['valor_compra']:.2f}")
            pause()
        elif opcao == '3':
            produtos = data_manager.load_data('produtos.json')
            custos = estoque.calcular_custos(produtos)
            print(f"\nCusto Total em Estoque: R$ {custos['total_atual']:.2f}")
            print(f"Custo Mensal Projetado: R$ {custos['mensal_projetado']:.2f}")
            print(f"Custo Anual Projetado: R$ {custos['anual_projetado']:.2f}")
            pause()
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")
            time.sleep(1)

def menu_financeiro():
    while True:
        clear_screen()
        print("="*40)
        print("   MÓDULO FINANCEIRO")
        print("="*40)
        print("1. Gerenciar Despesas Fixas")
        print("2. Ver Relatório Financeiro")
        print("3. Calcular Custos de Água e Luz")
        print("0. Voltar")
        print("="*40)
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            financeiro.cadastrar_despesas_fixas()
            pause()
        elif opcao == '2':
            # Gather data for report
            despesas = data_manager.load_data('despesas.json')
            total_fixo = sum(d['valor'] for d in despesas)
            
            produtos = data_manager.load_data('produtos.json')
            custo_insumos = sum(p['quantidade'] * p['valor_compra'] for p in produtos)
            
            producao = data_manager.load_data('producao.json')
            qtd_carros = sum(row['quantidade'] for row in producao)
            
            custo_total = financeiro.calcular_custo_producao(total_fixo, custo_insumos)
            custo_unitario = financeiro.calcular_custo_por_carro(custo_total, qtd_carros)
            preco_venda = financeiro.calcular_preco_venda(custo_unitario)
            
            print("\n--- Relatório Financeiro ---")
            print(f"Total Despesas Fixas: R$ {total_fixo:.2f}")
            print(f"Custo Insumos (Estoque): R$ {custo_insumos:.2f}")
            print(f"Custo Total Produção: R$ {custo_total:.2f}")
            print(f"Produção Total: {qtd_carros} unidades")
            print(f"Custo Unitário: R$ {custo_unitario:.2f}")
            print(f"Preço de Venda Sugerido: R$ {preco_venda:.2f}")
            pause()
        elif opcao == '3':
            # Nova opção: Calcular custos de água e luz baseado em horas trabalhadas
            funcionarios = data_manager.load_data('funcionarios.json')
            
            if not funcionarios:
                print("\n⚠ ATENÇÃO: Nenhum funcionário cadastrado!")
                print("Cadastre funcionários no módulo RH primeiro.")
                pause()
                continue
            
            # Gerar relatório da fábrica com as novas regras (30 dias, 24h/dia)
            financeiro.gerar_relatorio_fabrica()
            pause()
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")
            time.sleep(1)


def menu_rh():
    """Menu do módulo de Recursos Humanos"""
    while True:
        clear_screen()
        print("="*40)
        print("   MÓDULO DE RH")
        print("="*40)
        print("1. Cadastrar Funcionário")
        print("2. Listar Funcionários")
        print("3. Editar Funcionário")
        print("4. Deletar Funcionário")
        print("5. Gerar Folha de Pagamento")
        print("0. Voltar")
        print("="*40)
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            # Cadastrar funcionário (usa seleção interativa de setor/cargo)
            try:
                rh.cadastrar_funcionario()
                pause()
            except Exception as e:
                print(f"Erro ao cadastrar: {e}")
                pause()
                
        elif opcao == '2':
            # Listar todos os funcionários
            rh.listar_funcionarios()
            pause()
            
        elif opcao == '3':
            # Editar funcionário existente
            try:
                rh.editar_funcionarios()
                pause()
            except Exception as e:
                print(f"Erro ao editar: {e}")
                pause()
                
        elif opcao == '4':
            # Deletar funcionário
            try:
                rh.deletar_funcionarios()
                pause()
            except Exception as e:
                print(f"Erro ao deletar: {e}")
                pause()
                
        elif opcao == '5':
            # Gerar folha de pagamento
            try:
                rh.gerar_folha_pagamento()
                pause()
            except Exception as e:
                print(f"Erro ao gerar folha: {e}")
                pause()
                
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")
            time.sleep(1)

if __name__ == "__main__":
    user = login()
    menu_principal(user)
