from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta

from app.db.basedatos import bbdd
from app.db.modelos import Precio,Descuento,Cliente,Trabajador,Parking,Estadia
from os import path
from app.controller.clases import ResumenEstadia,ResumenPagoCochera,FinPagoMensual
from app.configuracion import Config

class Controlador():
    def __init__(self,cantParkings):
        existiaBD=path.exists('app/db/basedatos.sqlite') # verifica si la bbdd existia antes intentar conectarse y crearla para luego inicializarla
        self.base=bbdd(cantParkings)
        if not(existiaBD):
            self.base.inicializar_tablas()
    
    def error(self):
        self.base.error()

    def devTrabajador(self,usuarioIngresado):
        return self.base.dev_trabajador_id(usuarioIngresado)

    def devTrabajadorId(self,idIngresado):
        return self.base.dev_trabajador_id(idIngresado)

    def verifTrabajador(self,userIngresado,passIngresada):
        trabajador=self.base.dev_trabajador(userIngresado)
        if trabajador==None:
            return ('MalUser',None)
        elif trabajador.check_password(trabajador.password,passIngresada):
            return ('Bien',trabajador)
        else:
            return ('MalPass',None)
    
    def altaTrabajador(self,nuevoTrabajador:Trabajador)->bool:
        return self.base.alta_trabajador(nuevoTrabajador)

    def devOcupadoParking(self,nroParking)->bool:
        resultado=self.base.dev_ocupado_parking(nroParking)
        if resultado==None:
            return 'Inexistente'
        elif resultado:
            return 'Ocupado'
        else:
            return 'Libre'

    def verifParkingDisponible(self)->bool:
        if self.devParkingDisponible() is None:
            return False
        else:
            return True 
    
    def devCliente(self,patenteIngresada):
        patenteIngresada=patenteIngresada.replace(" ", "")
        return self.base.dev_cliente(patenteIngresada)

    def devClienteMensual(self,documentoIngresado):
        return self.base.dev_cliente_mensual(documentoIngresado)
    
    def devDescuento(self,idIngresado):
        return self.base.dev_descuento(idIngresado)
    
    def devPrecioActualDiario(self):
        return self.base.dev_precio_actual_diario()
    
    def devPrecioActualMensual(self):
        return self.base.dev_precio_actual_mensual()

    def devParkingDisponible(self):
        return self.base.dev_nro_parking_disponible()

    def devParkingsDisponibles(self):
        parkingDisponible=self.base.dev_parkings_disponibles()
        tuplaParkingDisponible=[]
        for parking in parkingDisponible:
            tuplaParkingDisponible.append((parking.piso,parking.nroParking))
        return tuplaParkingDisponible

    def altaCliente(self,nuevoCliente:Cliente):
        nuevoCliente.patente=nuevoCliente.patente.replace(" ", "")
        viejoCliente=self.devCliente(nuevoCliente.patente)
        nroParking=self.devParkingDisponible()
        if viejoCliente is None:
            self.base.alta_cliente(nuevoCliente)
            self.base.asignar_descuento_basico(nuevoCliente.patente)
            self.base.activar_estadia_cliente(nuevoCliente,nroParking)
            return 'Alta'
        elif viejoCliente.activo:
            return 'Activo'    
        elif viejoCliente.celular!=nuevoCliente.celular:
            self.base.actualizar_celular_cliente(nuevoCliente)
            self.base.activar_estadia_cliente(nuevoCliente,nroParking)
            return 'Actualizado'
        else:
            self.base.activar_estadia_cliente(nuevoCliente,nroParking)
            return 'Activado'

    def calculaCosto(self,estadia:Estadia):
        tiempoEstadia=( datetime.strptime(estadia.fechaHoraEgreso,Config.formatoFecha) - datetime.strptime(estadia.fechaHoraIngreso,Config.formatoFecha) ) / timedelta(minutes=1) 
        precioActual=self.devPrecioActualDiario()
        costo=precioActual.precioBase + tiempoEstadia*precioActual.precioMinuto
        return {'costo':costo,'tiempoEstadia':round(tiempoEstadia,2),'precioBase':round(precioActual.precioBase,2)}

    def bajaCliente(self,patentebaja):
        patentebaja=patentebaja.replace(" ", "")
        clienteBajar=self.devCliente(patentebaja)
        if clienteBajar is None:
            respuesta={'resultado':'Mal'}
            return respuesta
        elif clienteBajar.activo:
            respuestaDesactivada=self.base.desactivar_estadia_cliente(patentebaja)
            nroparkingliberar=respuestaDesactivada['nroParking']
            estadiaDesactivada=respuestaDesactivada['estadiaDesactivada']
            self.base.liberar_parking(nroparkingliberar)
            costoytiempo=self.calculaCosto(estadiaDesactivada)
            costo=round(costoytiempo['costo'],2)
            tiempoEstadia=costoytiempo['tiempoEstadia']
            precioBase=costoytiempo['precioBase']
            descuento=self.devDescuento(clienteBajar.idDescuento)
            if descuento.vigente:
                descuentoAplicado=descuento.valor
                descripcionDescuento=descuento.descripcion
                monto=round((costo-descuentoAplicado*costo/100),2)
            else:
                monto=costo
                descuentoAplicado=0
                descripcionDescuento='Descuento no vigente'
            resumenEstadia=ResumenEstadia(patente=patentebaja,tiempo=tiempoEstadia,costo=costo,precioBase=precioBase,descuento=descuentoAplicado,descripcionDescuento=descripcionDescuento,monto=monto)
            respuesta={'resultado':'Baja','resumenEstadia':resumenEstadia}
            return respuesta
        else:
            respuesta={'resultado':'Inactivo'}
            return respuesta

    def listarEstadiasClientesActivos(self):
        return self.base.dev_estadias_activas()
        
    def listarDescuentosDiarios(self):
        return self.base.dev_lista_descuentos_diarios()

    def listarDescuentosMensuales(self):
        return self.base.dev_lista_descuentos_mensuales()

    def listarDescuentosVigentes(self):
        return self.base.dev_lista_descuentos_vigentes()
    
    def listarDescuentosMensualesVigentes(self):
        return self.base.dev_lista_descuentos_mensuales_vigentes()

    def nuevoDescuento(self,descripcionIngresada,valorIngresado,tipoIngresado):
        self.base.nuevo_descuento(descripcionIngresada,valorIngresado,tipoIngresado)

    def bajaDescuento(self,idbaja):
        if self.devDescuento(idbaja) is None:
            return 'Mal'
        elif self.devDescuento(idbaja).vigente:
            self.base.desactivar_descuento(idbaja)
            return 'Baja'
        else:
            return 'Desactivado'

    def altaDescuento(self,idalta):
        if self.devDescuento(idalta) is None:
            return 'Mal'
        elif self.devDescuento(idalta).vigente:
            return 'Activo'
        else:
            self.base.activar_descuento(idalta)
            return 'Alta'

    def borrarDescuento(self,idborrar):
        if self.devDescuento(idborrar) is None:
            return 'Mal'
        else:
            self.base.borrar_descuento(idborrar)
            return 'Borrado'

    def calculaNuevoPrecioPorcentajeDiario(self,porcentajeBase,porcentajeMinuto):
        precioBaseActual=self.devPrecioActualDiario().precioBase
        precioMinutoActual=self.devPrecioActualDiario().precioMinuto
        nuevoPrecioBase=round(precioBaseActual+precioBaseActual*porcentajeBase/100,2)
        nuevoPrecioMinuto=round(precioMinutoActual+precioMinutoActual*porcentajeMinuto/100,2)
        return (nuevoPrecioBase,nuevoPrecioMinuto)
    
    def calculaNuevoPrecioPorcentajeMensual(self,porcentajeBase):
        precioBaseActual=self.devPrecioActualMensual().precioBase
        nuevoPrecioBase=round(precioBaseActual+precioBaseActual*porcentajeBase/100,2)
        return nuevoPrecioBase

    def nuevoPrecioDiario(self,precioBase,precioMinuto):
        self.base.nuevo_precio_diario(precioBase,precioMinuto)
    
    def nuevoPrecioMensual(self,precioBase):
        self.base.nuevo_precio_mensual(precioBase)

    def bajaPrecioAnteriorDiario(self):
        self.base.baja_precio_anterior_diario()
    
    def bajaPrecioAnteriorMensual(self):
        self.base.baja_precio_anterior_mensual()

    def listarPreciosDiarios(self):
        precios=self.base.dev_lista_precios_diarios()
        preciosOrdenados=sorted(precios, key=lambda precio: datetime.strptime(precio.fechaAlta,Config.formatoFecha), reverse=True)
        return preciosOrdenados
    
    def listarPreciosMensual(self):
        precios=self.base.dev_lista_precios_mensual()
        preciosOrdenados=sorted(precios, key=lambda precio: datetime.strptime(precio.fechaAlta,Config.formatoFechaCorta), reverse=True)
        return preciosOrdenados

    def asignarDescuento(self,patenteIngresada,idDescuentoIngresado:int):
        clienteIngresado=self.devCliente(patenteIngresada)
        if  clienteIngresado==None:
            return 'No existe cliente con la patente ingresada'
        idDescuentoClienteIngresado=int(clienteIngresado.idDescuento)
        if idDescuentoClienteIngresado==idDescuentoIngresado:
            return 'Ya tiene ese descuento asignado'
        else:
            self.base.asignar_descuento(clienteIngresado.patente,idDescuentoIngresado)
            return 'Asignado'
             
    def verifCantMensuales(self):
        cantMensuales=len(self.base.dev_parkings_mensuales_ocupados())
        return (cantMensuales<Config.maximoParkingsMensuales)

    def validarParkingIngresado(self,nroParkingIngresado):
        if nroParkingIngresado=='':
            return self.devParkingDisponible()
        nroParkingIngresado=int(nroParkingIngresado)
        estadoParking=self.devOcupadoParking(nroParkingIngresado)
        if estadoParking=='Ocupado':
            return 'Ocupado'
        elif estadoParking=='Inexistente':
            return 'Inexistente'
        else:
            return nroParkingIngresado

    def validarClienteMensual(self,documentoIngresado):
        resultado=self.devClienteMensual(documentoIngresado)
        if resultado is None:
            return 'Nuevo'
        elif resultado.activo:
            return 'Activo'
        else:
            return 'Registrado'

    def altaClienteMensual(self,nuevoClienteMensual,mesesDeseados): 
        validacionClienteMensual=self.validarClienteMensual(nuevoClienteMensual.documento)
        if validacionClienteMensual=='Activo':
            return 'Activo'
        elif validacionClienteMensual=='Registrado':
            self.base.activar_cliente_mensual(nuevoClienteMensual)
            self.base.ocupar_parking_mensual(nroParkingOcupar=nuevoClienteMensual.nroParking)
            self.base.nuevo_abono(nuevoClienteMensual.documento,mesesDeseados)
            return 'Actualizado'
        else:
            self.base.alta_cliente_mensual(nuevoClienteMensual)
            self.base.ocupar_parking_mensual(nroParkingOcupar=nuevoClienteMensual.nroParking)
            self.base.nuevo_abono(nuevoClienteMensual.documento,mesesDeseados)
            return 'Alta'
    
    def bajaClienteMensual(self,documentobaja):
        clienteBajar=self.devClienteMensual(documentobaja)
        if clienteBajar is None:
            return 'Inexistente'
        elif clienteBajar.activo:
            self.base.desactivar_abono_cliente(documentobaja)
            self.base.liberar_parking_mensual(clienteBajar.nroParking)
            self.base.desactivar_cliente_mensual(clienteBajar.documento)
            return 'Baja'
        else:
            return 'Inactivo'

    def ordenarListaClientesMensualesActivos(self,listaClientesMensualesActivos):
        listaOrdenada=sorted(listaClientesMensualesActivos, key=lambda lista: datetime.strptime(lista[6],Config.formatoFechaCorta))
        return listaOrdenada

    def listarClientesMensualesActivos(self):
        listado=self.base.dev_lista_clientes_mensuales_activos()
        print(listado)
        nuevolistado=[]
        hoy = datetime.now().date()
        print(hoy)
        for l in listado:
            fechaVencimiento=datetime.strptime(l[6],Config.formatoFechaCorta).date()
            print(fechaVencimiento)
            if fechaVencimiento<=hoy:
                nueval=(l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7],l[8],'False')
                nuevolistado.append(nueval)
            else: 
                nueval=(l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7],l[8],'True')
                nuevolistado.append(nueval)
        print(nuevolistado)
        ordenado=self.ordenarListaClientesMensualesActivos(nuevolistado)
        print(ordenado)
        return ordenado

    def asignarDescuentoMensual(self,documentoIngresado,idDescuentoIngresado:int):
        clienteIngresado=self.devClienteMensual(documentoIngresado)
        if  clienteIngresado==None:
            return 'No existe cliente con el documento ingresado'
        idDescuentoClienteIngresado=int(clienteIngresado.idDescuento)
        if idDescuentoClienteIngresado==idDescuentoIngresado:
            return 'Ya tiene ese descuento asignado'
        else:
            self.base.asignar_descuento_mensual(clienteIngresado.documento,idDescuentoIngresado)
            return 'Asignado'
    
    def calcularMesesDeuda(self,fechaVencimiento):
        fechaVencimiento=datetime.strptime(fechaVencimiento,Config.formatoFechaCorta)
        fechaActual=datetime.now()
        mesesDeuda=0
        while fechaVencimiento.month<=fechaActual.month and fechaVencimiento.year<=fechaActual.year:
            mesesDeuda+=1
            fechaVencimiento=fechaVencimiento+relativedelta(months=1)
        return mesesDeuda

    def resumenPagoMensual(self,documentoIngresado):
        cliente=self.devClienteMensual(documentoIngresado)
        if  cliente==None:
            return 'Inexistente'
        else:
            if cliente.activo:
                abono=self.base.dev_abono_cliente(documentoIngresado)
                descuento=self.base.dev_descuento(cliente.idDescuento)
                mesesDeuda=self.calcularMesesDeuda(abono.fechaVencimiento)
                precio=self.base.dev_precio_actual_mensual()
                monto=precio.precioBase*mesesDeuda*(1-descuento.valor/100)
                resumen=ResumenPagoCochera(documento=cliente.documento,nombre=cliente.nombre,fechaVencimiento=abono.fechaVencimiento,fechaDeseada=abono.fechaDeseada,mesesDeuda=mesesDeuda,
                                            valorDescuento=descuento.valor,descripcionDescuento=descuento.descripcion,precioMes=precio.precioBase,monto=monto)
                return resumen
            else:
                return 'Inactivo'
    
    def finPagoMensual(self,mesesPagar,mesesOcupar,documentoPrevio):
        datosPrevios=self.resumenPagoMensual(documentoPrevio)
        nombre=datosPrevios.nombre
        costo=datosPrevios.precioMes
        monto=costo*(1-datosPrevios.valorDescuento/100)
        finPago=FinPagoMensual(nombre=nombre,documento=documentoPrevio,mesesPagar=mesesPagar,mesesOcupar=mesesOcupar,costo=costo,monto=monto,valorDescuento=datosPrevios.valorDescuento,descripcionDescuento=datosPrevios.descripcionDescuento)
        return finPago

    def efectuarPagoMensual(self,documento,mesesPagar,mesesOcupar):
        self.base.actualizar_abono_mensual(documento,mesesPagar,mesesOcupar)