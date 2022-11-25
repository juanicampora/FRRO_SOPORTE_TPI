from flask import Blueprint,render_template, request, redirect,url_for ,session,send_from_directory,flash
from flask_login import login_user,logout_user,login_required

from app.configuracion import Config
from app.db.modelos import Precio,Descuento,Cliente,Trabajador,Parking,Estadia
from app.controller.controlador import Controlador


global_rutas=Blueprint("rutasglobales",__name__,template_folder=Config.CARPETA_TEMPLATES,static_folder=Config.CARPETA_STATIC)
controlador=Controlador(Config.cantParkings)

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
        elif resultado[0]=='MalUser':
            flash('Usuario incorrecto')
            return render_template("login.html")
        else:
            flash('Contraseña incorrecta')
            return render_template("login.html")
    else:
        return render_template("login.html")
        
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
        return redirect(url_for('rutasglobales.login'))
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

@global_rutas.route('/alta')
@login_required
def alta():
    if controlador.verifParkingDisponible():
        return render_template('alta.html')
    else:
        flash('No hay Parking Disponible')
        return render_template('mensaje.html')

@global_rutas.route('/altaenv', methods=['post'])
@login_required
def altaestadia():
    nuevapatente=str(request.form.get('patente'))
    celularingresado=request.form.get('celular')
    if nuevapatente=='':
        flash('Ingrese una patente')
        return redirect(url_for('rutasglobales.alta'))
    if celularingresado=='':
        nuevocelular=None
    else:
        nuevocelular=int(celularingresado)
    nuevocliente=Cliente(patente=nuevapatente,celular=nuevocelular,activo=True)
    resultado=controlador.altaCliente(nuevocliente)
    if resultado=='Alta':
        flash('Alta')
        return redirect(url_for('rutasglobales.alta'))
    elif resultado=='Activo':
        flash('El cliente previamente fue dado de Alta')
        return redirect(url_for('rutasglobales.alta'))
    elif resultado=='Actualizado':
        flash('Alta realizada a un cliente registrado anteriormente, se actualizó su celular')
        return redirect(url_for('rutasglobales.alta'))
    else:
        flash('Alta realizada a un cliente registrado anteriormente')
        return redirect(url_for('rutasglobales.alta'))

@global_rutas.route('/baja')
@login_required
def baja():
    return render_template('baja.html')

@global_rutas.route('/bajaenv', methods=['post'])
@login_required
def bajaestadia():
    patentebaja=str(request.form.get('patente'))
    resultado=controlador.bajaCliente(patentebaja)
    if resultado=='Baja':
        flash('Baja')
        return redirect(url_for('rutasglobales.baja'))
    elif resultado=='Inactivo':
        flash('La patente ingresada corresponde a un cliente inactivo')
        return redirect(url_for('rutasglobales.baja'))
    else:
        flash('La patente ingresada no corresponde a un cliente ')
        return redirect(url_for('rutasglobales.baja'))

@global_rutas.route('/bajaenv/<patente>')
@login_required
def bajaestadiadesdelista(patente):
    patentebaja=patente
    resultado=controlador.bajaCliente(patentebaja)
    if resultado=='Baja':
        flash('Baja Realizada')
        return redirect(url_for('rutasglobales.listar'))
    elif resultado=='Inactivo':
        flash('La patente ingresada corresponde a un cliente inactivo')
        return render_template('listado.html')
    else:
        flash('La patente ingresada no corresponde a un cliente ')
        return render_template('listado.html')

@global_rutas.route('/listado')
@login_required
def listar():
    lista=controlador.listarEstadiasClientesActivos()
    return render_template('listado.html',data_lista=lista)

@global_rutas.route('/descuentos',methods=['GET','POST'])
@login_required
def listardescuentos():
    if request.method=='POST':
        descripcion= request.form['txtDescripcion']
        valor= request.form['txtValor']
        if descripcion=='' or valor=='':
            flash('Error, complete todos los campos')
            return redirect(url_for('rutasglobales.listardescuentos'))
        else:
            controlador.nuevoDescuento(descripcion,valor)
            flash('Registrado Correctamente')
            return redirect(url_for('rutasglobales.listardescuentos'))
    else:
        descuentos=controlador.listarDescuentos()
        print(descuentos)
        return render_template('listadodescuentos.html',data_descuentos=descuentos)

@global_rutas.route('/descuentos/<accion>/<idDescuento>')
@login_required
def accionlistadescuentos(accion,idDescuento):
    if accion=='baja':
        resultado=controlador.bajaDescuento(idDescuento)
        if resultado=='Baja':
            flash('Baja Realizada')
            return redirect(url_for('rutasglobales.listardescuentos'))
        elif resultado=='Desactivado':
            flash('El descuento ya se encontraba inactivo')
            return redirect(url_for('rutasglobales.listardescuentos'))
        else:
            flash('El id de cliente ingresado es inexistente ')
            return redirect(url_for('rutasglobales.listardescuentos'))
    elif accion=='alta':
        resultado=controlador.altaDescuento(idDescuento)
        if resultado=='Alta':
            flash('Alta Realizada')
            return redirect(url_for('rutasglobales.listardescuentos'))
        elif resultado=='Activo':
            flash('El descuento ya se encontraba activo')
            return redirect(url_for('rutasglobales.listardescuentos'))
        else:
            flash('El id de cliente ingresado es inexistente ')
            return redirect(url_for('rutasglobales.listardescuentos'))
