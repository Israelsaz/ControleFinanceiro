import json
import os
from datetime import datetime, date

# Arquivo principal para o controle financeiro

# Nome do arquivo para salvar os dados
ARQUIVO_DADOS = "dados_financeiros.json"

# Listas para armazenar as transações (serão carregadas do arquivo)
receitas = []
despesas = []

def carregar_dados():
    global receitas, despesas
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                receitas = dados.get('receitas', [])
                despesas = dados.get('despesas', [])
                receitas = [r for r in receitas if isinstance(r, dict) and 'valor' in r and 'descricao' in r and 'data' in r and 'categoria' in r]
                despesas = [d for d in despesas if isinstance(d, dict) and 'valor' in d and 'descricao' in d and 'data' in d and 'categoria' in d]
            print("Dados carregados com sucesso!")
        except json.JSONDecodeError:
            print(f"Erro ao ler o arquivo {ARQUIVO_DADOS}. Formato inválido. Começando com listas vazias.")
            receitas = []
            despesas = []
        except Exception as e:
            print(f"Ocorreu um erro inesperado ao carregar os dados: {e}")
            receitas = []
            despesas = []
    else:
        print("Arquivo de dados não encontrado. Começando com listas vazias.")

def salvar_dados():
    try:
        with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
            dados = {"receitas": receitas, "despesas": despesas}
            json.dump(dados, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Ocorreu um erro ao salvar os dados: {e}")

def adicionar_despesa(descricao: str, valor: float, categoria: str, data_str: str | None = None) -> bool:
    """Adiciona uma despesa à lista e retorna True se sucesso, False caso contrário."""
    try:
        if valor < 0:
            print("Erro: O valor da despesa não pode ser negativo.")
            return False

        if not data_str:
            data_obj = date.today()
        else:
            try:
                data_obj = date.fromisoformat(data_str)
            except ValueError:
                print(f"Erro: Formato de data inválido '{data_str}'. Use AAAA-MM-DD.")
                return False

        despesas.append({
            "descricao": descricao,
            "valor": valor,
            "categoria": categoria if categoria else "Geral",
            "data": data_obj.isoformat()
        })
        print(f"Despesa '{descricao}' de R${valor:.2f} adicionada.")
        return True
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao adicionar despesa: {e}")
        return False

def adicionar_receita(descricao: str, valor: float, categoria: str, data_str: str | None = None) -> bool:
    """Adiciona uma receita à lista e retorna True se sucesso, False caso contrário."""
    try:
        if valor < 0:
            print("Erro: O valor da receita não pode ser negativo.")
            return False

        if not data_str:
            data_obj = date.today()
        else:
            try:
                data_obj = date.fromisoformat(data_str)
            except ValueError:
                print(f"Erro: Formato de data inválido '{data_str}'. Use AAAA-MM-DD.")
                return False

        receitas.append({
            "descricao": descricao,
            "valor": valor,
            "categoria": categoria if categoria else "Geral",
            "data": data_obj.isoformat()
        })
        print(f"Receita '{descricao}' de R${valor:.2f} adicionada.")
        return True
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao adicionar receita: {e}")
        return False

def calcular_saldo() -> dict:
    """Calcula e retorna o total de receitas, despesas e o saldo."""
    total_receitas = sum(item['valor'] for item in receitas)
    total_despesas = sum(item['valor'] for item in despesas)
    saldo = total_receitas - total_despesas
    return {
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "saldo": saldo
    }

def get_transacoes_ordenadas() -> dict:
    """Retorna as listas de receitas e despesas ordenadas por data."""
    receitas_ordenadas = sorted(receitas, key=lambda x: x.get('data', '0000-00-00'))
    despesas_ordenadas = sorted(despesas, key=lambda x: x.get('data', '0000-00-00'))
    return {"receitas": receitas_ordenadas, "despesas": despesas_ordenadas}
