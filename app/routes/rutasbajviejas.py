@global_rutas.route('/baja',methods=['GET','POST'])
@login_required
def baja(resumenEstadia='Nada'):
    if request.method=='POST':
        patentebaja=str(request.form.get('patente'))
        respuesta=controlador.bajaCliente(patentebaja)
        if respuesta['resultado']=='Baja':
            flash('Baja')
            return render_template('bajaresultadomonto.html',datos=respuesta['resumenEstadia']) #redirect(url_for('rutasglobales.baja'))
        elif respuesta['resultado']=='Inactivo':
            flash('La patente ingresada corresponde a un cliente inactivo')
            return redirect(url_for('rutasglobales.baja'))
        else:
            flash('La patente ingresada no corresponde a un cliente ')
            return redirect(url_for('rutasglobales.baja'))
    elif resumenEstadia=='Nada':
        print("Entro aca")
        print(resumenEstadia)
        return render_template('baja.html')    
    else:
        print(resumenEstadia)
        return render_template('bajaresultadomonto.html',datos=resumenEstadia)
        
@global_rutas.route('/baja/<patente>')
@login_required
def bajaestadiadesdelista(patente):
    patentebaja=patente
    respuesta=controlador.bajaCliente(patentebaja)
    if respuesta['resultado']=='Baja':
        flash('Baja Realizada')
        resumen=respuesta['resumenEstadia']
        print(resumen)
        return redirect(url_for('rutasglobales.baja',resumenEstadia=resumen))
    elif respuesta['resultado']=='Inactivo':
        flash('La patente ingresada corresponde a un cliente inactivo')
        return render_template('listado.html')
    else:
        flash('La patente ingresada no corresponde a un cliente ')
        return render_template('listado.html')