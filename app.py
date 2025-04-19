from flask import Flask, render_template, request, redirect, url_for, flash
# Importar funções do nosso módulo de controle financeiro
import controle_financeiro as cf

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui' # Mantenha uma chave segura em produção

@app.route('/')
def index():
    # Carrega os dados usando a função do módulo
    cf.carregar_dados()
    # Calcula o saldo usando a função do módulo
    saldo_info = cf.calcular_saldo()
    # Obtém as transações ordenadas
    transacoes = cf.get_transacoes_ordenadas()

    return render_template(
        'index.html',
        receitas=transacoes['receitas'],
        despesas=transacoes['despesas'],
        saldo=saldo_info['saldo'],
        total_receitas=saldo_info['total_receitas'],
        total_despesas=saldo_info['total_despesas']
    )

@app.route('/add_receita', methods=['POST'])
def add_receita():
    try:
        descricao = request.form['descricao']
        valor_str = request.form['valor']
        categoria = request.form.get('categoria', 'Geral') # .get com valor padrão
        data_str = request.form.get('data') # .get retorna None se não existir

        # Validação básica no lado do servidor
        if not descricao:
            flash("Erro: A descrição não pode estar vazia.", 'error')
            return redirect(url_for('index'))
        if not valor_str:
             flash("Erro: O valor não pode estar vazio.", 'error')
             return redirect(url_for('index'))

        valor = float(valor_str.replace(',', '.'))

        # Chama a função refatorada do módulo controle_financeiro
        sucesso = cf.adicionar_receita(descricao, valor, categoria, data_str)

        if sucesso:
            cf.salvar_dados() # Salva se a adição foi bem-sucedida
            flash(f"Receita '{descricao}' adicionada com sucesso!", 'success')
        else:
            # A função adicionar_receita já deve ter logado o erro específico
            # Podemos adicionar uma mensagem genérica aqui se quisermos
            flash("Erro ao adicionar receita. Verifique os dados e tente novamente.", 'error')

    except ValueError:
        flash("Erro: Valor inválido. Por favor, insira um número.", 'error')
    except Exception as e:
        flash(f"Ocorreu um erro inesperado: {e}", 'error')
        print(f"Erro inesperado em add_receita: {e}") # Log do erro no console do servidor

    return redirect(url_for('index'))

@app.route('/add_despesa', methods=['POST'])
def add_despesa():
    try:
        descricao = request.form['descricao']
        valor_str = request.form['valor']
        categoria = request.form.get('categoria', 'Geral')
        data_str = request.form.get('data')

        if not descricao:
            flash("Erro: A descrição não pode estar vazia.", 'error')
            return redirect(url_for('index'))
        if not valor_str:
             flash("Erro: O valor não pode estar vazio.", 'error')
             return redirect(url_for('index'))

        valor = float(valor_str.replace(',', '.'))

        # Chama a função refatorada do módulo controle_financeiro
        sucesso = cf.adicionar_despesa(descricao, valor, categoria, data_str)

        if sucesso:
            cf.salvar_dados()
            flash(f"Despesa '{descricao}' adicionada com sucesso!", 'success')
        else:
            flash("Erro ao adicionar despesa. Verifique os dados e tente novamente.", 'error')

    except ValueError:
        flash("Erro: Valor inválido. Por favor, insira um número.", 'error')
    except Exception as e:
        flash(f"Ocorreu um erro inesperado: {e}", 'error')
        print(f"Erro inesperado em add_despesa: {e}")

    return redirect(url_for('index'))

if __name__ == "__main__":
    cf.carregar_dados() # Carrega os dados uma vez ao iniciar o servidor
    app.run(debug=True) # debug=True facilita o desenvolvimento
