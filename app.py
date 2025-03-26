from flask import Flask, request, render_template, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'chave_secreta'  # Chave para manter a sessão

# Configuração do banco de dados
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'raulgui123!',
    'database': 'db_garagem_semecti'
}

def conectar_db():
    return mysql.connector.connect(**config)

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    nome_completo = request.form['nome_completo']
    senha = request.form['senha']
    
    conexao = conectar_db()
    cursor = conexao.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM usuarios WHERE nome_completo = %s AND senha = %s", (nome_completo, senha))
    usuario = cursor.fetchone()
    
    cursor.close()
    conexao.close()
    
    if usuario:
        session['usuario'] = usuario['nome_completo']
        session['cargo'] = usuario['cargo']
        return redirect(url_for('index'))
    else:
        flash('Credenciais inválidas, tente novamente!', 'danger')
        return redirect(url_for('login_page'))

@app.route('/index')
def index():
    if 'usuario' not in session:
        return redirect(url_for('login_page'))
    return render_template('index.html', usuario=session['usuario'], cargo=session['cargo'])

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    session.pop('cargo', None)
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)
