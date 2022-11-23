from flask import Blueprint,render_template, request, redirect, session,send_from_directory,url_for
from app.configuracion import Config
from app.db.modelos import Precio,Descuento,Cliente,Trabajador,Parking,Estadia
from app.controller.controlador import Controlador

global_rutas=Blueprint("rutasglobales",__name__,template_folder=Config.CARPETA_TEMPLATES,static_folder=Config.CARPETA_STATIC)
controlador=Controlador()

@global_rutas.route('/')
def login():
    return render_template('login2.html')

@global_rutas.route('/inicio')
def inicio():
    return render_template('index.html')

@global_rutas.route('/add')
def add():
    return render_template('add.html')

@global_rutas.route('/altaenv', methods=['post'])
def altacontacto():
    nuevapatente=str(request.form.get('patente'))
    nuevocelular=int(request.form.get('celular'))
    nuevocliente=Cliente(patente=nuevapatente,celular=nuevocelular)
    controlador.altaCliente(nuevocliente)
    return redirect(url_for('rutasglobales.inicio'))

@global_rutas.route('/alta')
def alta():
    return render_template('alta.html')

@global_rutas.route('/baja')
def baja():
    return render_template('baja.html')

@global_rutas.route('/listado')
def listar():
    return render_template('listado.html')

@global_rutas.route('/login', methods=['POST'])
def admin_login_post():
    _usuario= request.form['txtUsuario']
    _password= request.form['txtPassword']
    print(_usuario)
    print(_password)
    if _usuario=="admin" and _password=="123":
        return render_template("index.html")
    return render_template("login2.html")

