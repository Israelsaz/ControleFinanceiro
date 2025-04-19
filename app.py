from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui' # Necessário para usar flash messages

# Nome do arquivo para salvar os dados
ARQUIVO_DADOS = "dados_financeiros.json"

# Variáveis globais para armazenar as transações
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
            json.dump(dados, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Ocorreu um erro ao salvar os dados: {e}")

def calcular_saldo_atual():
    total_receitas = sum(item['valor'] for item in receitas)
    total_despesas = sum(item['valor'] for item in despesas)
    return total_receitas - total_despesas

@app.route('/')
def index():
    carregar_dados() # Carrega os dados sempre que a página principal é acessada
    saldo = calcular_saldo_atual()
    return render_template('index.html', receitas=receitas, despesas=despesas, saldo=saldo)

@app.route('/add_receita', methods=['POST'])
def add_receita():
    try:
        descricao = request.form['descricao']
        valor_str = request.form['valor']
        valor = float(valor_str.replace(',', '.'))
        if valor < 0:
            flash("Erro: O valor da receita não pode ser negativo.", 'error')
        elif not descricao:
             flash("Erro: A descrição da receita não pode estar vazia.", 'error')
        else:
            receitas.append({"descricao": descricao, "valor": valor})
            salvar_dados()
            flash(f"Receita '{descricao}' adicionada com sucesso!", 'success')
    except ValueError:
        flash("Erro: Valor inválido. Por favor, insira um número.", 'error')
    except Exception as e:
        flash(f"Ocorreu um erro inesperado: {e}", 'error')
    return redirect(url_for('index'))

@app.route('/add_despesa', methods=['POST'])
def add_despesa():
    try:
        descricao = request.form['descricao']
        valor_str = request.form['valor']
        valor = float(valor_str.replace(',', '.'))
        if valor < 0:
            flash("Erro: O valor da despesa não pode ser negativo.", 'error')
        elif not descricao:
             flash("Erro: A descrição da despesa não pode estar vazia.", 'error')
        else:
            despesas.append({"descricao": descricao, "valor": valor})
            salvar_dados()
            flash(f"Despesa '{descricao}' adicionada com sucesso!", 'success')
    except ValueError:
        flash("Erro: Valor inválido. Por favor, insira um número.", 'error')
    except Exception as e:
        flash(f"Ocorreu um erro inesperado: {e}", 'error')
    return redirect(url_for('index'))

if __name__ == "__main__":
    carregar_dados() # Carrega os dados uma vez ao iniciar o servidor
    app.run(debug=True) # debug=True para facilitar o desenvolvimento
