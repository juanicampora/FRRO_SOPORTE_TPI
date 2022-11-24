from app.db.basedatos import bbdd
from app.db.modelos import Precio,Descuento,Cliente,Trabajador,Parking,Estadia

class Controlador():
    def __init__(self):
        self.base=bbdd()
        #self.base.inicializar_tablas() # QUITAR COMENTARIO PARA INICIALIZAR LOS PARKINGS

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
    
    def altaCliente(self,nuevoCliente:Cliente):
        nuevoCliente.patente=nuevoCliente.patente.strip()
        viejoCliente=self.dev_cliente(nuevoCliente.patente)
        if viejoCliente is None:
            self.base.alta_cliente(nuevoCliente)
            self.base.activar_estadia_cliente(nuevoCliente,nroParking)
            return 'Alta'
        elif viejoCliente.activo:
            return 'Activo'    
        elif viejoCliente.celular!=nuevoCliente.celular:
            self.base.actualizar_celular_cliente(nuevoCliente)
            nroParking=self.base.nro_parking_disponible()
            self.base.activar_estadia_cliente(nuevoCliente,nroParking)
            return 'Actualizado'
        else:
            nroParking=self.base.nro_parking_disponible()
            self.base.activar_estadia_cliente(nuevoCliente,nroParking)
            return 'Activado'

    def listarEstadiasActivas(self):
        self.base.dev_estadias_activas()