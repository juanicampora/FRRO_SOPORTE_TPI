from random import randint
from sqlalchemy import create_engine,insert
from sqlalchemy.orm import sessionmaker
from .modelos import Base,Precio,Descuento,Cliente,Trabajador,Parking,Estadia

from sqlalchemy.ext.declarative import declarative_base


class bbdd():
    def inicializar_tablas(self,cantidad_parkings,session):
            for i in range(1,cantidad_parkings+1):
                if i<=cantidad_parkings/3:
                    pisoelegido=1
                elif i<=cantidad_parkings/3*2:
                    pisoelegido=2
                else:
                    pisoelegido=3
                nuevo_parking=Parking(nroParking=i,piso=pisoelegido,ocupado=False)
                session.add(nuevo_parking)
                session.commit()
    def __init__(self):
        cantidad_parkings=30

        engine=create_engine('sqlite:///app/db/basedatos.sqlite')
        Base.metadata.create_all(engine)
        Session= sessionmaker(bind=engine)
        session= Session()
        self.inicializar_tablas(cantidad_parkings,session)

        


