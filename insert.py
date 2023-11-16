import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, g
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from random import randint

from helpers import apology, login_required

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Função para conectar ao banco de dados
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect("distribuidora2.db")
        g.db.row_factory = sqlite3.Row
    return g.db

# Função para fechar a conexão com o banco de dados
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()



# Configure connection to SQLite database
'''conn = sqlite3.connect("quiz.db")
conn.row_factory = sqlite3.Row
db = conn.cursor()'''

admsenha = "Cliente3"

senha = generate_password_hash(admsenha)

with app.app_context():
    db = get_db()
    db.execute("INSERT INTO clientes (CNPJ, nome, endereco, senha) VALUES ('33.333.333/0001-33', 'cli3', 'rua a, 003', ?)", (senha,))
    db.commit()

print(senha)