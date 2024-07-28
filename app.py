from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Inicialização do aplicativo Flask
app = Flask(__name__)

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# Inicialização da instância do SQLAlchemy
db = SQLAlchemy(app)

# Definição do modelo de dados para o item
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    name = db.Column(db.String(80), nullable=False)  # Nome do item
    description = db.Column(db.String(200), nullable=False)  # Descrição do item

# Rota para a página inicial que lista todos os itens
@app.route('/')
def index():
    items = Item.query.all()  # Consulta todos os itens do banco de dados
    return render_template('index.html', items=items)  # Renderiza o template com a lista de itens

# Rota para criar um novo item
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Obtém os dados do formulário
        name = request.form['name']
        description = request.form['description']
        # Cria uma nova instância de Item
        new_item = Item(name=name, description=description)
        try:
            # Adiciona o novo item ao banco de dados
            db.session.add(new_item)
            db.session.commit()
            return redirect('/')  # Redireciona para a página inicial
        except:
            return 'There was an issue adding your item'  # Retorna uma mensagem de erro
    else:
        return render_template('create.html')  # Renderiza o template de criação

# Rota para atualizar um item existente
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    item = Item.query.get_or_404(id)  # Obtém o item pelo ID ou retorna 404 se não encontrado
    if request.method == 'POST':
        # Atualiza os dados do item
        item.name = request.form['name']
        item.description = request.form['description']
        try:
            db.session.commit()  # Confirma as mudanças no banco de dados
            return redirect('/')  # Redireciona para a página inicial
        except:
            return 'There was an issue updating your item'  # Retorna uma mensagem de erro
    else:
        return render_template('update.html', item=item)  # Renderiza o template de atualização com os dados do item

# Rota para deletar um item
@app.route('/delete/<int:id>')
def delete(id):
    item = Item.query.get_or_404(id)  # Obtém o item pelo ID ou retorna 404 se não encontrado
    try:
        # Deleta o item do banco de dados
        db.session.delete(item)
        db.session.commit()
        return redirect('/')  # Redireciona para a página inicial
    except:
        return 'There was an issue deleting your item'  # Retorna uma mensagem de erro

# Executa o aplicativo Flask
if __name__ == "__main__":
    db.create_all()  # Cria as tabelas do banco de dados
    app.run(debug=True)  # Executa o aplicativo no modo debug
