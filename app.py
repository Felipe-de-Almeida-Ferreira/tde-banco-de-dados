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

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    db = get_db()

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("cnpj"):
            flash("Todos od campos devem ser preenchidos")
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("senha"):
            flash("Todos od campos devem ser preenchidos")
            return redirect("/login")

        # Query database for username
        rows = db.execute("SELECT * FROM clientes WHERE cnpj = :cnpj", {"cnpj": request.form.get("cnpj")}).fetchall()
        print("rows = ", rows)
        print("rows = ", len(rows))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["senha"], request.form.get("senha")):
            print("Senha ou CPJ inválidos!")
            flash("Senha ou CPJ inválidos!")
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["user_role"] = "cliente"

        # Redirect user to home page
        return redirect("/")
        

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():

    db = get_db()
    """Register user"""
    lenght_check = 0
    uppercase_check = 0

    if request.method == "POST":
        cnpj = request.form.get("cnpj")
        nome = request.form.get("nome")
        endereco = request.form.get("endereco")
        senha = request.form.get("senha")
        csenha = request.form.get("confirma")

        cnpj_check = {
            "cnpj": cnpj
        }

        # Check if the username already exists
        cnpj_existente = db.execute("SELECT * FROM clientes WHERE cnpj = :cnpj;", cnpj_check).fetchone()
        print("cnpj_existente: ", cnpj_existente)

        if cnpj_existente:
            flash("Este CNPJ já está registrado!")
            return redirect("/login")

        if senha != csenha:
            return apology("Password and confirmation password do not match", 400)

        if cnpj and nome and senha and csenha:
            '''if len(username) < 4:
                flash("Username too short")
                return redirect("/register"), 400'''

            if len(senha) < 6:
                flash("Senha muito curta!")
              #  lenght_check +=
                return redirect("/register")

            elif not any(caractere.isupper() for caractere in senha):
                flash("Please, use at least one Uppercase letter!")
                #uppercase_check += 1
                return redirect("/register")
            else:

                hash = generate_password_hash(senha)
                data = {
                    'cnpj': cnpj,
                    'nome': nome,
                    'endereco': endereco,
                    'hash': hash
                }

                db.execute("INSERT INTO clientes (CNPJ, nome, endereco, senha) VALUES (:cnpj, :nome, :endereco, :hash);", data)
                g.db.commit()
                g.db.close()
                return redirect("/")

        else:
            flash("Preencha todos os campos!")

            return redirect("/register")
    else:
        return render_template("register.html")
    


#login dos administradores
@app.route("/adm-login", methods=["GET", "POST"])
def adm_login():
    """Log user in"""
    db = get_db()

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("email"):
            flash("Todos od campos devem ser preenchidos")
            return redirect("/adm-login")

        # Ensure password was submitted
        elif not request.form.get("senha"):
            flash("Todos od campos devem ser preenchidos")
            return redirect("/adm-login")

        # Query database for username
        rows = db.execute("SELECT * FROM admins WHERE email = :email", {"email": request.form.get("email")}).fetchall()
        print("rows = ", rows)
        print("rows = ", len(rows))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["senha"], request.form.get("senha")):
            print("Senha ou CPJ inválidos!")
            flash("Senha ou CPJ inválidos!")
            return redirect("/adm-login")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["user_role"] = "admin"

        # Redirect user to home page
        return redirect("/")
        

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("adm-login.html")

    


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    db = get_db()
    if request.method == "POST":
        user_id = session['user_id']

        id_data = {
            'user_id': user_id
        }

        cliente_cursor = db.execute("SELECT nome FROM clientes WHERE id = :user_id", id_data).fetchone()
        endereco_cursor = db.execute("SELECT endereco FROM clientes WHERE id = :user_id", id_data)

        cliente = cliente_cursor['nome']
        endereco = endereco_cursor.fetchone()['endereco']

        velho_cachorro = int(db.execute("SELECT estoque FROM racoes WHERE racao = 'ração1'").fetchone()[0])
        velho_gato = int(db.execute("SELECT estoque FROM racoes WHERE racao = 'ração2'").fetchone()[0])
        velho_hamster = int(db.execute("SELECT estoque FROM racoes WHERE racao = 'ração3'").fetchone()[0])

        print(velho_cachorro)
        print(velho_gato)
        print(velho_hamster)

        compra_cachorro = int(request.form.get("quantidade-cachorro"))
        compra_gato = int(request.form.get("quantidade-gato"))
        compra_hamster = int(request.form.get("quantidade-hamster"))

        print(compra_cachorro)
        print(compra_gato)
        print(compra_hamster)

        novo_cachorro = int(velho_cachorro - compra_cachorro)
        novo_gato = int(velho_gato - compra_gato)
        novo_hamster = int(velho_hamster - compra_hamster)

        print(novo_cachorro)
        print(novo_gato)
        print(novo_hamster)

        data_cachorro = {'novo_cachorro': novo_cachorro}
        data_gato = {'novo_gato': novo_gato}
        data_hamster = {'novo_hamster': novo_hamster}

        db.execute("UPDATE racoes SET estoque = :novo_cachorro WHERE racao = 'ração1'", data_cachorro)
        db.execute("UPDATE racoes SET estoque = :novo_gato WHERE racao = 'ração2'", data_gato)
        db.execute("UPDATE racoes SET estoque = :novo_hamster WHERE racao = 'ração3'", data_hamster)
        g.db.commit()


        rc = int(db.execute("SELECT estoque FROM racoes WHERE racao = 'ração1'").fetchone()[0])
        rg = int(db.execute("SELECT estoque FROM racoes WHERE racao = 'ração2'").fetchone()[0])
        rh = int(db.execute("SELECT estoque FROM racoes WHERE racao = 'ração3'").fetchone()[0])


        print(rc)
        print(rg)
        print(rh)

        hist_data = {
            'cliente': cliente,
            'endereco': endereco
        }

        db.execute("INSERT INTO compras (cliente, endereco, data) VALUES (:cliente, :endereco, CURRENT_TIMESTAMP)", hist_data)

        cachorro = db.execute("SELECT estoque FROM racoes WHERE racao = 'ração1'").fetchone()[0]
        gato = db.execute("SELECT estoque FROM racoes WHERE racao = 'ração2'").fetchone()[0]
        hamster = db.execute("SELECT estoque FROM racoes WHERE racao = 'ração3'").fetchone()[0]
        g.db.commit()
        g.db.close()


        if session["user_role"] == "admin":
            return render_template("adm-home.html", cachorro = cachorro, gato = gato, hamster = hamster)
        elif session["user_role"] == "cliente":
            return render_template("index.html", cachorro = cachorro, gato = gato, hamster = hamster)

    else:
        cachorro = db.execute("SELECT estoque FROM racoes WHERE racao = 'ração1'").fetchone()[0]
        gato = db.execute("SELECT estoque FROM racoes WHERE racao = 'ração2'").fetchone()[0]
        hamster = db.execute("SELECT estoque FROM racoes WHERE racao = 'ração3'").fetchone()[0]
        #racoes = dados.fetchall()

        racoes_lista = []

        '''for racao in racoes:
            racao_item = {
                'id': racao['id'],
                'racao': racao['racao'],
                'tipo_racao': racao['tipo_racao'],
                'estoque': racao['estoque']
            }

            racoes_lista.append(racao_item)'''
        
        g.db.close()

        if session["user_role"] == "admin":
            return render_template("adm-home.html", cachorro = cachorro, gato = gato, hamster = hamster)
        elif session["user_role"] == "cliente":
            return render_template("index.html", cachorro = cachorro, gato = gato, hamster = hamster)
        

@app.route("/compras")
@login_required
def compras():
    db = get_db()

    compras = db.execute("SELECT cliente, endereco, data FROM compras")
    itens = []
    
    for compra in compras:
        cliente = compra['cliente'],
        endereco = compra['endereco']
        data = compra['data']
        itens.append({
            "cliente": cliente,
            "endereco": endereco,
            "data": data
        })

    return render_template("compras.html", itens = itens)
        