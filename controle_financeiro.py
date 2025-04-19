import json
import os

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
                receitas = dados.get('receitas', []) # Usa .get para evitar erro se a chave não existir
                despesas = dados.get('despesas', [])
            print("Dados carregados com sucesso!")
        except json.JSONDecodeError:
            print(f"Erro ao ler o arquivo {ARQUIVO_DADOS}. Começando com listas vazias.")
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
            json.dump(dados, f, indent=4, ensure_ascii=False) # indent=4 para formatar, ensure_ascii=False para caracteres acentuados
    except Exception as e:
        print(f"Ocorreu um erro ao salvar os dados: {e}")

def adicionar_despesa():
    print("\n--- Adicionar Despesa ---")
    try:
        descricao = input("Descrição da despesa: ")
        valor_str = input("Valor da despesa: ")
        valor = float(valor_str.replace(',', '.')) # Converte para float, aceitando vírgula
        if valor < 0:
            print("Erro: O valor da despesa não pode ser negativo.")
            return
        despesas.append({"descricao": descricao, "valor": valor})
        print(f"Despesa '{descricao}' de R${valor:.2f} adicionada com sucesso!")
    except ValueError:
        print("Erro: Valor inválido. Por favor, insira um número.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

def adicionar_receita():
    print("\n--- Adicionar Receita ---")
    try:
        descricao = input("Descrição da receita: ")
        valor_str = input("Valor da receita: ")
        valor = float(valor_str.replace(',', '.')) # Converte para float, aceitando vírgula
        if valor < 0:
            print("Erro: O valor da receita não pode ser negativo.")
            return
        receitas.append({"descricao": descricao, "valor": valor})
        print(f"Receita '{descricao}' de R${valor:.2f} adicionada com sucesso!")
    except ValueError:
        print("Erro: Valor inválido. Por favor, insira um número.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

def calcular_saldo():
    print("\n--- Saldo Atual ---")
    
    total_receitas = sum(item['valor'] for item in receitas)
    total_despesas = sum(item['valor'] for item in despesas)
    
    saldo = total_receitas - total_despesas
    
    print(f"Total de Receitas: R$ {total_receitas:.2f}")
    print(f"Total de Despesas: R$ {total_despesas:.2f}")
    print(f"Saldo Final:       R$ {saldo:.2f}")

def mostrar_menu():
    print("\n--- Controle Financeiro ---")
    print("1. Adicionar Receita")
    print("2. Adicionar Despesa")
    print("3. Ver Saldo")
    print("0. Sair")
    return input("Escolha uma opção: ")

def main():
    print("Bem-vindo ao seu Controle Financeiro Pessoal!")
    carregar_dados() # Carrega os dados ao iniciar
    
    while True:
        opcao = mostrar_menu()
        
        if opcao == '1':
            adicionar_receita()
        elif opcao == '2':
            adicionar_despesa()
        elif opcao == '3':
            calcular_saldo()
        elif opcao == '0':
            salvar_dados() # Salva os dados antes de sair
            print("Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Garante que a função main() só será executada quando o script for rodado diretamente
if __name__ == "__main__":
    main()
