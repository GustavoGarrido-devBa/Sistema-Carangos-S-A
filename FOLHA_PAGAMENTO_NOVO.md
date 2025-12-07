# 📋 Nova Funcionalidade de Folha de Pagamento com Seleção por Setor

## 🎯 Resumo das Mudanças

A função `gerar_folha_pagamento()` foi completamente refatorada para permitir:

✅ **Seleção de setor**  
✅ **Seleção de funcionário dentro do setor**  
✅ **Geração de folha para todos os setores**  
✅ **Formato profissional e organizado**  
✅ **Dados pessoais exibidos**  
✅ **Cálculos por horas customizáveis**

---

## 🏗️ Estrutura da Implementação

### Função Principal: `gerar_folha_pagamento()`
- Exibe menu de seleção de setor
- Permite selecionar um setor específico ou todos os setores
- Chama funções helper apropriadas

### Novas Funções Helper:

#### 1. `obter_setor_funcionario(cargo: str) -> str`
Identifica o setor do funcionário baseado no cargo.
```python
setor = rh.obter_setor_funcionario("Gerente Financeiro")
# Retorna: "FINANCEIRO"
```

#### 2. `_gerar_folha_setor(setor: str, funcionarios_setor: list)`
Exibe menu de seleção de funcionários de um setor específico.

#### 3. `_gerar_folha_todos_setores(funcionarios_por_setor: dict, setores_lista: list)`
Gera folha de pagamento para todos os setores com resumo geral.

#### 4. `_calcular_folha_funcionario(funcionario: dict)`
Exibe e calcula a folha de pagamento de um funcionário específico.

---

## 📊 Fluxo de Execução

```
main.py chama gerar_folha_pagamento()
    ↓
Menu: Selecione Setor
    ├─ 1. OPERACIONAL (2 funcionários)
    ├─ 2. ESTOQUE (2 funcionários)
    ├─ 3. FINANCEIRO (2 funcionários)
    ├─ 4. Gerar folha de TODOS
    └─ 0. Cancelar
    ↓
Selecionar Setor (ex: 1)
    ↓
Menu: Selecione Funcionário
    ├─ 1. João Silva (Operador de Máquinas)
    ├─ 2. Pedro Costa (Técnico de Manutenção)
    └─ 0. Voltar
    ↓
Selecionar Funcionário (ex: 1)
    ↓
Solicitar Horas:
    ├─ Horas trabalhadas (padrão 220h)
    └─ Horas extras (padrão 0h)
    ↓
Exibir Folha de Pagamento Formatada
```

---

## 💼 Exemplo de Saída - Funcionário Individual

```
======================================================================
FOLHA DE PAGAMENTO - JOÃO SILVA
======================================================================

[DADOS PESSOAIS]
Nome: João Silva
CPF: 123.456.789-00
RG: MG-12.345.678
Endereço: Rua A, 100
Telefone: (31) 99999-9999

[INFORMAÇÕES DE HORAS]
Horas trabalhadas (padrão 220h): 220
Horas extras: 10

[CÁLCULOS]
Cargo: Operador de Máquinas
Valor/hora: R$ 8.50
Quantidade de filhos: 2

[FOLHA DE PAGAMENTO]
Salário Base (220h × R$8.50): R$    1870.00
Horas Extras (10h + 50%): R$     127.50
----------------------------------------------------------------------
Total Bruto: R$    1997.50
IRPF (-): R$       0.00
Paga IRPF: Não
======================================================================
SALÁRIO LÍQUIDO: R$    1997.50
======================================================================
```

---

## 📌 Exemplo de Saída - Todos os Setores

```
======================================================================
FOLHA DE PAGAMENTO - TODOS OS SETORES
======================================================================

──────────────────────────────────────────────────────────────────────
SETOR: OPERACIONAL
──────────────────────────────────────────────────────────────────────

[João Silva]
  Horas trabalhadas (padrão 220h): 220
  Horas extras: 10

Cargo: Operador de Máquinas          | Valor/hora: R$    8.50
Salário Base (220h): R$    1870.00
Horas Extras (10h + 50%): R$     127.50
├─ Total Bruto: R$    1997.50
├─ IRPF: R$       0.00 (Não)
└─ Líquido: R$    1997.50

[Pedro Costa]
  Horas trabalhadas (padrão 220h): 220
  Horas extras: 5

Cargo: Técnico de Manutenção        | Valor/hora: R$   12.00
Salário Base (220h): R$    2640.00
Horas Extras (5h + 50%): R$      90.00
├─ Total Bruto: R$    2730.00
├─ IRPF: R$      28.29 (Sim)
└─ Líquido: R$    2701.71

──────────────────────────────────────────────────────────────────────
SETOR: ESTOQUE
──────────────────────────────────────────────────────────────────────
...

======================================================================
RESUMO GERAL - TODOS OS SETORES
======================================================================
Total Bruto Geral: R$   15234.50
Total IRPF Geral:  R$     356.12
Total Líquido Geral: R$   14878.38
======================================================================
```

---

## 🔄 Integração com main.py

Em `main.py`, a função é chamada normalmente:

```python
def menu_rh():
    while True:
        clear_screen()
        print("=" * 40)
        print("   MÓDULO DE RH")
        print("=" * 40)
        print("1. Cadastrar Funcionário")
        print("2. Ver Folha de Pagamento")
        print("0. Voltar")
        print("=" * 40)
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            # ... cadastro ...
        elif opcao == '2':
            rh.gerar_folha_pagamento()  # ← Nova interface com seleção
            pause()
        # ...
```

**O usuário agora pode:**
1. ✅ Selecionar qual setor deseja processar
2. ✅ Selecionar qual funcionário do setor
3. ✅ Informar horas personalizadas
4. ✅ Ver folha formatada e profissional

---

## 🧪 Testes Executados

| Teste | Status |
|-------|--------|
| Carregamento de dados | ✅ PASSOU |
| Função obter_setor_funcionario | ✅ PASSOU |
| Organização por setor | ✅ PASSOU |
| Cálculos por setor | ✅ PASSOU |
| Funções helper presentes | ✅ PASSOU |
| Seleção de funcionário | ✅ PASSOU |
| Estrutura de saída | ✅ PASSOU |

---

## 📝 Funcionalidades Implementadas

### ✅ Validações
- Verifica se funcionários estão cadastrados
- Verifica se setores existem
- Tratamento de entrada inválida
- Defaults para horas (220h padrão, 0 extras)

### ✅ Organização
- Funcionários agrupados por setor
- Funcionários ordenados por nome dentro de cada setor
- Menu hierárquico (Setor → Funcionário)

### ✅ Formatação
- Separadores visuais (═, ─)
- Seções bem definidas
- Alinhamento de valores monetários
- Estrutura clara e profissional

### ✅ Cálculos
- Salário bruto com horas customizáveis
- Horas extras com regra de cargo (gerentes/diretores = R$0)
- IRPF com tabela progressiva de 5 faixas
- Salário líquido

---

## 🚀 Como Usar

1. **Abra o programa** e vá para "Módulo de RH"
2. **Selecione "Ver Folha de Pagamento"**
3. **Escolha um setor** (ou todos)
4. **Selecione o funcionário**
5. **Informe as horas**
6. **Visualize a folha formatada**

---

## 📌 Notas Importantes

- A função agora é **completamente interativa** com seleção visual
- Suporta **múltiplos funcionários por setor**
- Permite **processar um funcionário ou todos de uma vez**
- Dados **organizados profissionalmente**
- **Pronto para imprimir** em PDF/relatório
