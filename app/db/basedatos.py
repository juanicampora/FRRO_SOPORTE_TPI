from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy import create_engine,desc
from sqlalchemy.orm import sessionmaker
from .modelos import Base,Precio,Descuento,Cliente,Trabajador,Parking,Estadia,ClienteMensual,Abono
from app.configuracion import Config


class bbdd():
    def inicializar_tablas(self):
        nuevo_descuento=Descuento(1,'Sin descuento',0,False,True)
        nuevo_descuento_mensual=Descuento(2,'Sin descuento',0,True,True)
        nuevo_trabajador=Trabajador('admin','123','Administrador')
        nuevo_precio_diario=Precio(None,100,10,datetime.now().strftime(Config.formatoFecha),None,False)
        nuevo_precio_mensual=Precio(None,1000,10,datetime.now().strftime(Config.formatoFecha),None,True)
        self.session.add(nuevo_descuento)
        self.session.add(nuevo_descuento_mensual)
        self.session.add(nuevo_trabajador)
        self.session.add(nuevo_precio_diario)
        self.session.add(nuevo_precio_mensual)
        self.session.commit()
        for i in range(1,self.cantidad_parkings+1):         #MODIFICAR PARA QUE SIRVA CON X CANTIDAD DE PISOS
            if i<=self.cantidad_parkings/3:
                pisoelegido=1
            elif i<=self.cantidad_parkings/3*2:
                pisoelegido=2
            else:
                pisoelegido=3
            nuevo_parking=Parking(nroParking=i,piso=pisoelegido,ocupado=False)
            self.session.add(nuevo_parking)
            self.session.commit()

    def dev_trabajador(self,usuarioIngresado)->Trabajador:
        query=self.session.query(Trabajador).filter_by(usuario=usuarioIngresado)
        return query.first()

    def dev_trabajador_id(self,idIngresado)->Trabajador:
        query=self.session.query(Trabajador).filter_by(id=idIngresado)
        return query.first()

    def alta_trabajador(self,nuevoTrabajador:Cliente) -> bool:
        if self.dev_trabajador(nuevoTrabajador.usuario):
            return False
        else:
            self.session.add(nuevoTrabajador)
            self.session.commit()
            return True

    def dev_cliente(self,patenteCliente)-> Cliente:
        query=self.session.query(Cliente).filter_by(patente=patenteCliente)
        return query.first()

    def dev_descuento(self,idBuscado)-> Descuento:
        return self.session.query(Descuento).filter_by(idDescuento=idBuscado).first()   

    def alta_cliente(self,nuevoCliente:Cliente):
        self.session.add(nuevoCliente)
        self.session.commit()
    
    def asignar_descuento_basico(self,patenteCliente):
        self.session.query(Cliente).filter_by(patente=patenteCliente).update({Cliente.idDescuento:1})
        self.session.commit()

    def actualizar_celular_cliente(self,nuevoCliente:Cliente):
        self.session.query(Cliente).filter_by(patente=nuevoCliente.patente).update({Cliente.celular:nuevoCliente.celular})
        self.session.commit()

    def dev_ocupado_parking(self,nroParking)-> Parking:
        return self.session.query(Parking).filter_by(nroParking=nroParking).first().ocupado

    def dev_nro_parking_disponible(self):
        parkingDisponible=self.session.query(Parking).filter_by(ocupado=False).first()
        if parkingDisponible is None:
            return None
        else:
            return parkingDisponible.nroParking

    def ocupar_parking(self,nroParkingOcupar):
        self.session.query(Parking).filter_by(nroParking=nroParkingOcupar).update({Parking.ocupado:True})
        self.session.commit()

    def ocupar_parking_mensual(self,nroParkingOcupar):
        self.session.query(Parking).filter_by(nroParking=nroParkingOcupar).update({Parking.ocupado:True,Parking.mensual:True})
        self.session.commit()

    def activar_estadia_cliente(self,nuevoCliente:Cliente,nroParkingAsignar:int):
        self.session.query(Cliente).filter_by(patente=nuevoCliente.patente).update({Cliente.activo:True})
        nuevaEstadia=Estadia(nuevoCliente.patente,datetime.now().strftime(Config.formatoFecha),None,nroParkingAsignar)
        self.session.query(Parking).filter_by(nroParking=nroParkingAsignar).update({Parking.ocupado:True})
        self.session.add(nuevaEstadia)
        self.session.commit()
    
    def desactivar_estadia_cliente(self,patenteBaja):
        self.session.query(Cliente).filter_by(patente=patenteBaja).update({Cliente.activo:False})
        estadia=self.session.query(Estadia).filter_by(patente=patenteBaja,fechaHoraEgreso=None).first()
        self.session.query(Estadia).filter_by(patente=patenteBaja).update({Estadia.fechaHoraEgreso:datetime.now().strftime(Config.formatoFecha)})
        estadiaDesactivada=self.session.query(Estadia).filter_by(patente=patenteBaja,fechaHoraIngreso=estadia.fechaHoraIngreso).first()
        self.session.commit()
        return {'nroParking':estadia.nroParking,'estadiaDesactivada':estadiaDesactivada}

    def liberar_parking(self,nroParkingLiberar):
        self.session.query(Parking).filter_by(nroParking=nroParkingLiberar).update({Parking.ocupado:False})
        self.session.commit()
    
    def liberar_parking_mensual(self,nroParkingLiberar):
        self.session.query(Parking).filter_by(nroParking=nroParkingLiberar).update({Parking.ocupado:False,Parking.mensual:False})
        self.session.commit()

    def dev_estadias_activas(self):
        #lista_desorganizada=self.session.query(Estadia,Cliente,Parking,Descuento).filter_by(fechaHoraEgreso=None).join(Cliente).join(Parking).join(Descuento).order_by(Parking.piso,Parking.nroParking).all()
        #i=0
        #columnas=5
        #filas=len(lista_desorganizada)
        #lista=[[0 for _ in range(columnas)]]*filas
        #for l in lista_desorganizada:
        #    lista[i]=[l[2].piso,l[0].nroParking,l[0].patente,l[1].celular,l[0].fechaHoraIngreso,l[3].descripcion]
        #    i+=1 
        query=  """ SELECT parking.piso,parking.nroParking,cliente.patente,cliente.celular,estadia.fechaHoraIngreso,descuento.descripcion,descuento.vigente
                    FROM estadia
                    INNER JOIN cliente
                        ON cliente.patente=estadia.patente
                    INNER JOIN parking
                        ON estadia.nroParking=parking.nroParking
                    INNER JOIN descuento
                        ON cliente.idDescuento=descuento.idDescuento
                    WHERE estadia.fechaHoraEgreso IS NULL
                """
        lista=self.session.execute(query).all()
        return lista

    def dev_lista_descuentos_diarios(self):
        return self.session.query(Descuento).filter_by(mensual=False).all()
    
    def dev_lista_descuentos_mensuales(self):
        return self.session.query(Descuento).filter_by(mensual=True).all()

    def dev_lista_descuentos_vigentes(self):
        return self.session.query(Descuento).filter_by(vigente=True,mensual=False).all()   
    
    def dev_lista_descuentos_mensuales_vigentes(self):
        return self.session.query(Descuento).filter_by(vigente=True,mensual=True).all()   

    def nuevo_descuento(self,descripcionIngresada,valorIngresado,tipoIngresado):
        nuevoDescuento=Descuento(idDescuento=None,descripcion=descripcionIngresada,valor=valorIngresado,mensual=tipoIngresado,vigente=None)
        self.session.add(nuevoDescuento)
        self.session.commit()


    def desactivar_descuento(self,idBaja):
        self.session.query(Descuento).filter_by(idDescuento=idBaja).update({Descuento.vigente:False})
        self.session.commit()
    
    def activar_descuento(self,idAlta):
        self.session.query(Descuento).filter_by(idDescuento=idAlta).update({Descuento.vigente:True})
        self.session.commit()

    def nuevo_precio_diario(self,precioBase,precioMinuto):
        nuevoPrecio=Precio(idPrecio=None,precioBase=precioBase,precioMinuto=precioMinuto,fechaAlta=datetime.now().strftime(Config.formatoFecha),fechaBaja=None,mensual=False)
        self.session.add(nuevoPrecio)
        self.session.commit()
    
    def nuevo_precio_mensual(self,precioBase):
        nuevoPrecio=Precio(idPrecio=None,precioBase=precioBase,precioMinuto=None,fechaAlta=datetime.now().strftime(Config.formatoFecha),fechaBaja=None,mensual=True)
        self.session.add(nuevoPrecio)
        self.session.commit()

    def dev_lista_precios_diarios(self):
        return self.session.query(Precio).filter_by(mensual=False).all()
    
    def dev_lista_precios_mensual(self):
        return self.session.query(Precio).filter_by(mensual=True).all()

    def baja_precio_anterior_diario(self):
        self.session.query(Precio).filter_by(fechaBaja=None,mensual=False).update({Precio.fechaBaja:datetime.now().strftime(Config.formatoFecha)})
        self.session.commit()
    
    def baja_precio_anterior_mensual(self):
        self.session.query(Precio).filter_by(fechaBaja=None,mensual=True).update({Precio.fechaBaja:datetime.now().strftime(Config.formatoFecha)})
        self.session.commit()

    def dev_precio_actual_diario(self):
        return self.session.query(Precio).filter_by(fechaBaja=None,mensual=False).first()
    
    def dev_precio_actual_mensual(self):
        return self.session.query(Precio).filter_by(fechaBaja=None,mensual=True).first()

    def asignar_descuento(self,patenteCliente,idDescuentoIngresado):
        self.session.query(Cliente).filter_by(patente=patenteCliente).update({Cliente.idDescuento:idDescuentoIngresado})
        self.session.commit()

    def dev_parkings_disponibles(self):
        return self.session.query(Parking).filter_by(ocupado=False,mensual=False).all()

    def dev_parkings_mensuales_ocupados(self):
        return self.session.query(Parking).filter_by(ocupado=False,mensual=True).all()

    def dev_cliente_mensual(self,documentoClienteMensual):
        return self.session.query(ClienteMensual).filter_by(documento=documentoClienteMensual).first()

    def alta_cliente_mensual(self,nuevoClienteMensual:ClienteMensual):
        self.session.add(nuevoClienteMensual)
        self.session.commit()

    def activar_cliente_mensual(self,antiguoClienteMensual:ClienteMensual):
        self.session.query(ClienteMensual).filter_by(documento=antiguoClienteMensual.documento).update(
            {ClienteMensual.nombre:antiguoClienteMensual.nombre
            ,ClienteMensual.celular:antiguoClienteMensual.celular
            ,ClienteMensual.activo:True})
        self.session.commit()

    def nuevo_abono(self,documentoClienteMensual,mesesDeseados):
        if mesesDeseados=='':
            fechaDeseada='No especificada'
        else:
            mesesDeseados=int(mesesDeseados)
            fechaDeseada=(datetime.now()+relativedelta(months=mesesDeseados)).strftime(Config.formatoFecha)
        nuevoAbono=Abono(documento=documentoClienteMensual,fechaInicio=datetime.now().strftime(Config.formatoFecha),fechaDeseada=fechaDeseada,fechaVencimiento=datetime.now().strftime(Config.formatoFecha))
        self.session.add(nuevoAbono)
        self.session.commit()
    
    def desactivar_abono_cliente(self,documentoBaja):
        self.session.query(Abono).filter_by(documento=documentoBaja,fechaFin=None).update({Abono.fechaFin:datetime.now().strftime(Config.formatoFecha)})
        self.session.commit()

    def desactivar_cliente_mensual(self,documentoBaja):
        self.session.query(ClienteMensual).filter_by(documento=documentoBaja).update({ClienteMensual.activo:False})
        self.session.commit()
    
    def dev_lista_clientes_mensuales_activos(self):
        query=  """ SELECT parking.nroParking,piso,clientemensual.documento,clientemensual.nombre,fechaInicio, fechaDeseada, fechaVencimiento,descripcion,vigente
                    FROM abono
                    INNER JOIN clientemensual
                        ON abono.documento=clientemensual.documento
                    INNER JOIN parking
                        ON clientemensual.nroParking=parking.nroParking
                    INNER JOIN descuento
                        ON clientemensual.idDescuento=descuento.idDescuento
                    WHERE abono.fechaFin IS NULL
                """
        lista=self.session.execute(query).all()
        return lista

    def asignar_descuento_mensual(self,documentoCliente,idDescuentoIngresado):
        self.session.query(ClienteMensual).filter_by(documento=documentoCliente).update({ClienteMensual.idDescuento:idDescuentoIngresado})
        self.session.commit()

    def dev_abono_cliente(self,documentoCliente):
        return self.session.query(Abono).filter_by(documento=str(documentoCliente),fechaFin=None).first()

    def actualizar_abono_mensual(self,documentoCliente,mesesPagar,mesesOcupar):
        abonoCliente=self.dev_abono_cliente(documentoCliente)
        fechaVencimiento=abonoCliente.fechaVencimiento
        fechaDeseada=abonoCliente.fechaDeseada
        fechaDeseadaNueva=(datetime.strptime(fechaDeseada,Config.formatoFecha)+relativedelta(months=mesesOcupar)).strftime(Config.formatoFecha)
        fechaVencimientoNueva=(datetime.strptime(fechaVencimiento,Config.formatoFecha)+relativedelta(months=mesesPagar)).strftime(Config.formatoFecha)
        self.session.query(Abono).filter_by(documento=documentoCliente,fechaFin=None).update({Abono.fechaVencimiento:fechaVencimientoNueva,Abono.fechaDeseada:fechaDeseadaNueva})
        self.session.commit()

    def __init__(self,cantParkings):
        self.cantidad_parkings=cantParkings

        engine=create_engine('sqlite:///app/db/basedatos.sqlite',connect_args={'check_same_thread': False})
        Base.metadata.create_all(engine)
        Session= sessionmaker(bind=engine)
        self.session= Session()
        


