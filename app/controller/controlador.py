from app.db.basedatos import bbdd
from app.db.modelos import Precio,Descuento,Cliente,Trabajador,Parking,Estadia

class Controlador():
    def __init__(self):
        self.base=bbdd()
        #self.base.inicializar_tablas() # QUITAR COMENTARIO PARA INICIALIZAR LOS PARKINGS


    def altaCliente(self,nuevoCliente:Cliente):
        self.base.alta_cliente(nuevoCliente)