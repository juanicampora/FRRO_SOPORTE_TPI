from flask import Blueprint,render_template, request, redirect,url_for ,session,send_from_directory,flash
from flask_login import login_user,logout_user,login_required

from app.configuracion import Config
from app.db.modelos import Precio,Descuento,Cliente,Trabajador,Parking,Estadia
from app.controller.controlador import Controlador


global_rutas=Blueprint("rutasglobales",__name__,template_folder=Config.CARPETA_TEMPLATES,static_folder=Config.CARPETA_STATIC)
controlador=Controlador()

@global_rutas.route('/')
def raiz():
    return redirect(url_for('rutasglobales.login'))

@global_rutas.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        _usuario= request.form['txtUsuario']
        _password= request.form['txtPassword']
        resultado=controlador.verifTrabajador(_usuario,_password)
        if resultado[0]=='Bien':
            login_user(resultado[1])
            print(f'Logueado usuario: {resultado[1].nombreApellido}')
            flash('Bienvenido ')
            return redirect(url_for('rutasglobales.inicio'))
            #return render_template('index.html')
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

@global_rutas.route('/registroenv', methods=['post'])
def registrotrabajador():
    nuevoUser=str(request.form.get('txtUsuario'))
    nuevaPassword=str(request.form.get('txtPassword'))
    nuevoNombre=str(request.form.get('txtNombre'))
    if nuevoUser=='':
        flash('Debe ingresar un Usuario')
        return render_template('registro.html')
    if nuevaPassword=='':
        flash('Debe ingresar una Contraseña')
        return render_template('registro.html')
    nuevoTrabajador=Trabajador(usuario=nuevoUser,password=nuevaPassword,nombreApellido=nuevoNombre)
    resultado=controlador.altaTrabajador(nuevoTrabajador)
    if resultado:
        flash('Registrado correctamente, Inicie Sesión')
        return render_template('registrocorrecto.html') #Como mejora se podria usar login2.html usando un if para que muestre cartel verde en vez de rojo
    else:
        flash('El usuario ingresado ya existe')
        return render_template('registro.html')

@global_rutas.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('rutasglobales.login'))

@global_rutas.route('/inicio')
@login_required
def inicio():
    return render_template('index.html')

@global_rutas.route('/add')     #esto deberia reemplazarse con el /alta
@login_required
def add():
    return render_template('add.html')

@global_rutas.route('/altaenv', methods=['post'])
@login_required
def altacontacto():
    nuevapatente=str(request.form.get('patente'))
    nuevocelular=int(request.form.get('celular'))
    nuevocliente=Cliente(patente=nuevapatente,celular=nuevocelular)
    controlador.altaCliente(nuevocliente)
    return redirect(url_for('rutasglobales.inicio'))

@global_rutas.route('/alta')
@login_required
def alta():
    return render_template('alta.html')

@global_rutas.route('/baja')
@login_required
def baja():
    return render_template('baja.html')

@global_rutas.route('/listado')
@login_required
def listar():
    return render_template('listado.html')
