import os
import sys
import tempfile

# Garantir que o diretório do projeto esteja no path para importar `modules`
sys.path.append(os.getcwd())

from modules import rh

print("Iniciando testes locais de modules/rh.py (não interativos)")

# Cria um arquivo temporário dentro da pasta data/ para simular o arquivo real
tmpdir = tempfile.mkdtemp(prefix="carangos_test_")
if not os.path.exists(tmpdir):
    os.makedirs(tmpdir)

filepath = os.path.join(tmpdir, "funcionarios.json")

# 1) Testar salvar_funcionario + carregar_todos_funcionarios
mock = [
    {
        "nome": "Teste Usuario",
        "cpf": "000.000.000-00",
        "rg": "MG-12.345.678",
        "endereco": "Rua Teste, 123",
        "telefone": "(11)99999-9999",
        "qtd_filhos": 0,
        "cargo": "Auxiliar",
        "valor_hora": 10.0,
        "data_cadastro": "01/01/2025 00:00:00"
    }
]

try:
    rh.salvar_funcionario(mock, filepath)
    carregados = rh.carregar_todos_funcionarios(filepath)
    assert isinstance(carregados, list), "carregar_todos_funcionarios deve retornar uma lista"
    assert len(carregados) == 1, f"esperado 1 registro, obteve {len(carregados)}"
    assert carregados[0]["nome"] == "Teste Usuario", "nome do registro salvo divergente"
    print("- salvar_funcionario / carregar_todos_funcionarios: OK")
except AssertionError as e:
    print(f"[FALHA] {e}")
    raise

# 2) Verificar que funções esperadas existem e são chamáveis (não-invocando as interativas)
expected_callables = [
    'salvar_funcionario',
    'carregar_todos_funcionarios',
    'selecionar_setor',
    'selecionar_cargo',
    'cadastrar_funcionario',
    'listar_funcionarios',
    'editar_funcionarios',
    'deletar_funcionarios'
]

missing = []
for name in expected_callables:
    if not hasattr(rh, name) or not callable(getattr(rh, name)):
        missing.append(name)

if missing:
    print(f"[FALHA] Funções ausentes ou não-callable em modules.rh: {missing}")
    raise SystemExit(2)
else:
    print("- presença das funções esperadas: OK")

# 3) Checar comportamento com arquivo inexistente (carregar retorna lista vazia)
no_file = os.path.join(tmpdir, "inexistente.json")
res = rh.carregar_todos_funcionarios(no_file)
assert res == [], "carregar_todos_funcionarios deve retornar [] se o arquivo não existir"
print("- carregar_todos_funcionarios com arquivo inexistente: OK")

print("Todos os testes locais de `modules/rh.py` passaram.")
print(f"Arquivo de teste criado em: {filepath}")
