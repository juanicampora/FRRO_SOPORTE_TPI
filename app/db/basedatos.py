from datetime import datetime
from random import randint
from sqlalchemy import create_engine,insert,select
from sqlalchemy.orm import sessionmaker
from .modelos import Base,Precio,Descuento,Cliente,Trabajador,Parking,Estadia

from sqlalchemy.ext.declarative import declarative_base


class bbdd():
    def inicializar_tablas(self):
        nuevo_descuento=Descuento(1,'Sin descuento',0,True)
        nuevo_trabajador=Trabajador('admin','123','Administrador')
        self.session.add(nuevo_descuento)
        self.session.add(nuevo_trabajador)
        self.session.commit()
        for i in range(1,self.cantidad_parkings+1):
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
        query=self.session.query(Descuento).filter_by(idDescuento=idBuscado)
        return query.first()

    def alta_cliente(self,nuevoCliente:Cliente) -> bool:
        self.session.add(nuevoCliente)
        self.session.commit()
    
    def actualizar_celular_cliente(self,nuevoCliente:Cliente):
        self.session.query(Cliente).filter_by(patente=nuevoCliente.patente).update({Cliente.celular:nuevoCliente.celular})
        self.session.commit()

    def nro_parking_disponible(self):
        parkingDisponible=self.session.query(Parking).filter_by(ocupado=False).first()
        if parkingDisponible is None:
            return None
        else:
            return parkingDisponible.nroParking

    def activar_estadia_cliente(self,nuevoCliente:Cliente,nroParkingAsignar:int):
        self.session.query(Cliente).filter_by(patente=nuevoCliente.patente).update({Cliente.activo:True})
        nuevaEstadia=Estadia(nuevoCliente.patente,datetime.now().strftime("%d/%m/%Y %H:%M:%S"),None,nroParkingAsignar)
        self.session.query(Parking).filter_by(nroParking=nroParkingAsignar).update({Parking.ocupado:True})
        self.session.add(nuevaEstadia)
        self.session.commit()
    
    def desactivar_estadia_cliente(self,patenteBaja):
        self.session.query(Cliente).filter_by(patente=patenteBaja).update({Cliente.activo:False})
        estadia=self.session.query(Estadia).filter_by(patente=patenteBaja,fechaHoraEgreso=None).first()
        self.session.query(Estadia).filter_by(patente=patenteBaja).update({Estadia.fechaHoraEgreso:datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
        self.session.commit()
        return estadia.nroParking

    def liberar_parking(self,nroParkingLiberar):
        self.session.query(Parking).filter_by(nroParking=nroParkingLiberar).update({Parking.ocupado:False})

    def dev_estadias_activas(self):
        #lista=self.session.query(Estadia,Cliente,Parking).filter_by(fechaHoraEgreso=None).join(Cliente).join(Parking).all()
        lista_desorganizada=self.session.query(Estadia,Cliente,Parking).filter_by(fechaHoraEgreso=None).join(Cliente).join(Parking).order_by(Parking.piso,Parking.nroParking).all()
        i=0
        columnas=5
        filas=len(lista_desorganizada)
        lista=[[0 for _ in range(columnas)]]*filas
        for l in lista_desorganizada:
            #print(f'Piso: {l[2].piso} Nro Parking: {l[0].nroParking} Patente:{l[0].patente} Celular:{l[1].celular} FechaHoraIngreso: {l[0].fechaHoraIngreso}')
            lista[i]=[l[2].piso,l[0].nroParking,l[0].patente,l[1].celular,l[0].fechaHoraIngreso]
            i+=1        
        return lista

    def __init__(self):
        self.cantidad_parkings=30

        engine=create_engine('sqlite:///app/db/basedatos.sqlite',connect_args={'check_same_thread': False})
        Base.metadata.create_all(engine)
        Session= sessionmaker(bind=engine)
        self.session= Session()
        


