### imports libs
from flask import Flask, render_template, request, redirect, url_for
from flask import  flash, get_flashed_messages, json, jsonify
from database import db
from via_cep import ViaCep
from models.usuario import Usuario
from models.medicamento import Medicamento

from repositories.usuario import UsuarioRepository
from repositories.medicamento import MedicamentoRepository


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/flask_login.db'
app.config['SECRET_KEY'] = 'aeeeeeeeeeeeeeeeeeeeeoooooooooooooooooooo'

db.init_app(app)

usuario_repository = UsuarioRepository(db)
medicamento_repository = MedicamentoRepository(db)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    """
    Define uma rota index que retorna a página index
    """
    return render_template("index.html")

@app.route("/login")
def login():
    """
    Define uma rota login que retorna a página de login
    """
    return render_template("login.html", mensagem="Entre no sistema")

@app.route("/login", methods=['POST'])
def login_post():
    """
    Recebe um login e uma senha e verifica se este
    login de usuário existe
    """
    login = request.form["login"]
    senha = request.form["password"]

    usuario = Usuario(username=login, senha=senha)
    login_correto = usuario.login()
    if(login_correto):
        # Retorna os medicamentos cadastrados se o login estiver correto
        medicamento = Medicamento.query.all()
        return render_template("login_ok.html", nome=login_correto.nome, medicamento=medicamento)
    return render_template("login.html", mensagem="Login inválido.")


### Rota de Cadastro
@app.route("/cadastro")
def cadastro():
    """
    Define uma rota cadastro que retorna a página de cadastro 
    """
    return render_template("cadastro.html")

### Métodos do Usuário
@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro_create():
    """
    Realiza o cadastro de um usuário (CREATE)
    """
    login = request.form["login"]
    senha = request.form["senha"]
    confirmar_senha = request.form["confirmar_senha"]
    nome = request.form["nome"]
    cpf = request.form["cpf"]
    email = request.form["email"]
    telefone = request.form["telefone"]
    cep = request.form["cep"]

    via_cep = ViaCep()
    resposta = via_cep.busca_cep(cep)

    if login == '':
        flash('Login é obrigatório!')

    if senha == '':
        flash('Senha é obrigatória!')

    if senha != confirmar_senha:
        flash('As senhas não são iguais!')

    if nome == '':
        flash('Nome é obrigatório!')

    if cpf == '':
        flash('CPF é obrigatório!')

    if email == '':
        flash('E-mail é obrigatório!')

    if telefone == '':
        flash('Telefone é obrigatório!')

    if cep == '':
        flash('CEP é obrigatório!')

    if resposta.status_code == 404:
        print('O CEP informado não existe!')

    if len(get_flashed_messages()) > 0:
        return render_template("cadastro.html")

    dic = resposta.json()

    usuario = Usuario(nome=nome, cpf=cpf, email=email,
                      telefone=telefone, cep=cep, logradouro=dic['logradouro'],
                      username=login, senha=senha)

    usuario.cadastrar()

    return render_template("cadastro_ok.html", usuario=usuario)

@app.route("/cadastro/show", methods=['POST', 'GET'])
def cadastro_get():
    """
    Exibe um usuario criado (READ)
    """
    if request.method == 'GET':
        usuario = Usuario.query.all()
        medicamento = Medicamento.query.all()
        
        return render_template("index.html", usuario=usuario, medicamento=medicamento)
    
"""
@app.route("/cadastro_medicamento/edit/<id>", methods=['GET', 'POST'])
def medicamento_update(id):
    
    Edita um medicamento criado (UPDATE)
    
    if request.method == 'GET':
        medicamento = medicamento_repository.get(id)

        return render_template("medicamento/editar.html", medicamento=medicamento, id=id)
    else:
        nome_medicamento = request.form['nome']
        data_validade = request.form['data_validade']

        medicamento = medicamento(nome_medicamento, data_validade, id)
        medicamento_repository.save(medicamento)

        return redirect(url_for("cadastro_medicamento"))

@app.route("/cadastro_medicamento/delete/<id>")
def medicamento_delete(id):
    
    Exclui um medicamento criado (DELETE)
    
    medicamento_repository.delete(id)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
"""

### Rota Cadastro de Medicamentos
@app.route("/cadastro_medicamento")
def medicamentos():
    """
    Define uma rota cadastro_medicamento e 
    retorna a página cadastro_medicamento
    """
    return render_template("cadastro_medicamento.html")

### Métodos do Medicamento
@app.route("/cadastro_medicamento", methods=['POST'])
def medicamentos_create():
    """
    Faz o cadastro de um medicamento (CREATE)
    """
    nome_medicamento = request.form["nome_medicamento"]
    data_validade = request.form["data_validade"]
    quantidade = request.form["quantidade"]
    peso = request.form["peso"]

    if nome_medicamento == '':
        flash('Nome do medicamento é obrigatório!')

    if data_validade == '':
        flash('A data de validade é obrigatória!')

    if quantidade == '':
        flash('A quantidade é obrigatória!')

    if len(get_flashed_messages()) > 0:
        return render_template("cadastro_medicamento.html")

    medicamento = Medicamento(nome_medicamento=nome_medicamento, data_validade=data_validade, quantidade=quantidade, peso=peso)

    medicamento.cadastrar()

    return render_template("cadastro_medicamento_ok.html", medicamento=medicamento)
"""
@app.route("/cadastro/show", methods=['GET'])
def medicamentos_get():
    
    Exibe todos medicamentos cadastrados(READ)
    
    if request.method == 'GET':
        medicamento = Medicamento.query.all()
        
        return render_template("index.html", medicamento=medicamento)
"""
@app.route("/cadastro_medicamento/edit/<id>", methods=['GET', 'POST'])
def medicamentos_update(id):
    """
    Edita um medicamento criado (UPDATE)
    """
    if request.method == 'GET':
        medicamento = medicamento_repository.get(id)

        return render_template("medicamento/editar.html", medicamento=medicamento, id=id)
    else:
        nome_medicamento = request.form['nome']
        data_validade = request.form['data_validade']

        medicamento = medicamento(nome_medicamento, data_validade, id)
        medicamento_repository.save(medicamento)

        return redirect(url_for("medicamentos"))

@app.route("/cadastro_medicamento/delete/<id>")
def medicamentos_delete(id):
    """
    Exclui um medicamento criado (DELETE)
    """
    medicamento_repository.delete(id)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

if __name__ == "__main__":
    app.run(debug=True)
