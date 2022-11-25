from app.db.basedatos import bbdd
from app.db.modelos import Precio,Descuento,Cliente,Trabajador,Parking,Estadia
from os import path

class Controlador():
    def __init__(self):
        existiaBD=path.exists('app/db/basedatos.sqlite') # verifica si la bbdd existia antes intentar conectarse y crearla para luego inicializarla
        self.base=bbdd()
        if not(existiaBD):
            self.base.inicializar_tablas()
    
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

    def verifParkingDisponible(self)->bool:
        if self.base.nro_parking_disponible is None:
            return False
        else:
            return True 
    
    def devCliente(self,patenteIngresada):
        return self.base.dev_cliente(patenteIngresada)
    
    def devDescuento(self,idIngresado):
        return self.base.dev_descuento(idIngresado)

    def altaCliente(self,nuevoCliente:Cliente):
        nuevoCliente.patente=nuevoCliente.patente.replace(" ", "")
        viejoCliente=self.devCliente(nuevoCliente.patente)
        nroParking=self.base.nro_parking_disponible()
        if viejoCliente is None:
            self.base.alta_cliente(nuevoCliente)
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

    def bajaCliente(self,patentebaja):
        patentebaja=patentebaja.replace(" ", "")
        if self.devCliente(patentebaja) is None:
            return 'Mal'
        elif self.devCliente(patentebaja).activo:
            nroparkingliberar=self.base.desactivar_estadia_cliente(patentebaja)
            self.base.liberar_parking(nroparkingliberar)
            return 'Baja'
        else:
            return 'Inactivo'

    def listarEstadiasClientesActivos(self):
        return self.base.dev_estadias_activas()
        
    def listarDescuentos(self):
        return self.base.dev_lista_descuentos()

    def nuevoDescuento(self,descripcionIngresada,valorIngresado):
        self.base.nuevo_descuento(descripcionIngresada,valorIngresado)

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


        