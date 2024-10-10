from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

dadosCli = []

class Cliente:
    def __init__(self, nome, loguin, senha, email, data_nascimento, celular):
        self.nome = nome
        self.loguin = loguin
        self.senha = senha
        self.email = email
        self.data_nascimento = data_nascimento
        self.celular = celular
        self.enderecos = []

    def adicionar_endereco(self, endereco):
        self.enderecos.append(endereco)

# Adicione um dicionário para usuários admin
admins = {'admin': 'senha_admin'}  # Exemplo: {'usuario': 'senha'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in admins and admins[username] == password:
            session['admin'] = username
            return redirect(url_for('admin_dashboard'))
        flash('Usuário ou senha inválidos.')
    return render_template('login_admin.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('login_admin'))
    return render_template('admin_dashboard.html', clientes=dadosCli)

@app.route('/login_cliente', methods=['GET', 'POST'])
def login_cliente():
    if request.method == 'POST':
        loguin = request.form['loguin']
        senha = request.form['senha']
        for cliente in dadosCli:
            if cliente.loguin == loguin and cliente.senha == senha:
                session['cliente'] = loguin
                return redirect(url_for('cliente_dashboard'))
        flash('Usuário ou senha inválidos.')
    return render_template('login_cliente.html')

@app.route('/cliente_dashboard')
def cliente_dashboard():
    if 'cliente' not in session:
        return redirect(url_for('login_cliente'))
    loguin = session['cliente']
    cliente = next((c for c in dadosCli if c.loguin == loguin), None)
    return render_template('cliente_dashboard.html', cliente=cliente)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    loguin = request.form['loguin']
    senha = request.form['senha']
    email = request.form['email']
    data_nascimento = request.form['data_nascimento']
    celular = request.form['celular']

    cliente = Cliente(nome, loguin, senha, email, data_nascimento, celular)
    dadosCli.append(cliente)
    flash('Cliente cadastrado com sucesso!')
    return redirect(url_for('index'))

@app.route('/adicionar_endereco', methods=['POST'])
def adicionar_endereco():
    loguin = request.form['loguin']
    for cliente in dadosCli:
        if cliente.loguin == loguin:
            cidade = request.form['cidade']
            bairro = request.form['bairro']
            rua = request.form['rua']
            numero = request.form['numero']
            ponto_referencia = request.form['ponto_referencia']
            endereco = Endereco(cidade, bairro, rua, numero, ponto_referencia)
            cliente.adicionar_endereco(endereco)
            flash('Endereço adicionado com sucesso!')
            return redirect(url_for('index'))
    flash('Cliente não encontrado.')
    return redirect(url_for('index'))

@app.route('/detalhes/<loguin>')
def detalhes(loguin):
    for cliente in dadosCli:
        if cliente.loguin == loguin:
            return render_template('detalhes_cliente.html', cliente=cliente)
    flash('Cliente não encontrado.')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('admin', None)
    session.pop('cliente', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)