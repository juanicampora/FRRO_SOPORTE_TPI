from flask import Flask,render_template, request, redirect, session,send_from_directory

app=Flask(__name__, template_folder='../views/templates', static_folder='../views/static')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/inicio')
def inicio():
    return render_template('index.html')

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/alta')
def alta():
    return render_template('alta.html')

@app.route('/baja')
def baja():
    return render_template('baja.html')

@app.route('/listado')
def listar():
    return render_template('listado.html')

@app.route('/login', methods=['POST'])
def admin_login_post():
    _usuario= request.form['txtUsuario']
    _password= request.form['txtPassword']
    print(_usuario)
    print(_password)
    if _usuario=="admin" and _password=="123":
        return render_template("index.html")

    return render_template("login.html")


