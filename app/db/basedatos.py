from random import randint
from sqlalchemy import create_engine,insert,select
from sqlalchemy.orm import sessionmaker
from .modelos import Base,Precio,Descuento,Cliente,Trabajador,Parking,Estadia

from sqlalchemy.ext.declarative import declarative_base


class bbdd():
    def inicializar_tablas(self):
        nuevo_descuento=Descuento(1,'Sin descuento',0,True)
        self.session.add(nuevo_descuento)
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

    def dev_cliente(self,patenteCliente)-> Cliente:
        query=self.session.execute( select(Cliente).where(Cliente.patente==patenteCliente) )
        return query.fetchone()

    def dev_descuento(self,idBuscado)-> Descuento:
        query=self.session.execute( select(Descuento).where(Descuento.idDescuento==idBuscado) )
        return query.fetchone()

    def alta_cliente(self,nuevoCliente:Cliente) -> bool:
        if self.dev_cliente(nuevoCliente.patente):
            return False
        else:
            self.session.add(nuevoCliente)
            self.session.commit()
            return True
        
    def __init__(self):
        self.cantidad_parkings=30

        engine=create_engine('sqlite:///app/db/basedatos.sqlite')
        Base.metadata.create_all(engine)
        Session= sessionmaker(bind=engine)
        self.session= Session()
        


