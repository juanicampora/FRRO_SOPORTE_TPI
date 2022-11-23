from app.db.basedatos import bbdd
from app.db.modelos import Precio,Descuento,Cliente,Trabajador,Parking,Estadia

class Controlador():
    def __init__(self):
        self.base=bbdd()
        #self.base.inicializar_tablas() # QUITAR COMENTARIO PARA INICIALIZAR LOS PARKINGS

    def verifTrabajador(self,userIngresado,passIngresada):
        trabajador=self.base.dev_trabajador(userIngresado)
        
        if trabajador==None:
            return ('MalUser',None)
        elif trabajador.check_password(trabajador.password,passIngresada):
            return ('Bien',trabajador)
        else:
            return ('MalPass',None)
    def devTrabajador(self,userIngresado):
        return self.base.dev_trabajador(userIngresado)
        
    def altaCliente(self,nuevoCliente:Cliente):
        self.base.alta_cliente(nuevoCliente)