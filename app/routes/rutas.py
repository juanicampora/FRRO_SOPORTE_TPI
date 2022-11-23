from flask import Blueprint,render_template, request, redirect,url_for ,session,send_from_directory,flash
from flask_login import LoginManager,login_user,logout_user,login_required

from app.configuracion import Config
from app.db.modelos import Precio,Descuento,Cliente,Trabajador,Parking,Estadia
from app.controller.controlador import Controlador


global_rutas=Blueprint("rutasglobales",__name__,template_folder=Config.CARPETA_TEMPLATES,static_folder=Config.CARPETA_STATIC)
controlador=Controlador()

@global_rutas.route('/')
def raiz():
    return redirect(url_for('rutasglobales.login'))

@global_rutas.route('/inicio')
def inicio():
    return render_template('index.html')

@global_rutas.route('/add')     #esto deberia reemplazarse con el /alta
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

@global_rutas.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        _usuario= request.form['txtUsuario']
        _password= request.form['txtPassword']
        resultado=controlador.verifTrabajador(_usuario,_password)
        if resultado[0]=='Bien':
            login_user(resultado[1])
            return render_template("index.html")
        elif resultado[0]=='MalUser':
            flash('Usuario incorrecto')
            return render_template("login2.html")
        else:
            flash('Contraseña incorrecta')
            return render_template("login2.html")
    else:
        return render_template("login2.html")
        
@global_rutas.route('/registro')
def registro():
    return render_template('registro.html')