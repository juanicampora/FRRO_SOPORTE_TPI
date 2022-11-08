from random import randint
from sqlalchemy import create_engine,insert
from sqlalchemy.orm import sessionmaker
from .modelos import Base,Precio,Descuento,Cliente,Trabajador,Parking,Estadia

from sqlalchemy.ext.declarative import declarative_base


class bbdd():
    def inicializar_tablas(self,cantidad_parkings,session):
            for i in range(cantidad_parkings):
                pisoaleatorio=randint(1,3)
                nuevo_parking=Parking(piso=pisoaleatorio,ocupado=False)
                session.add(nuevo_parking)
                session.commit()
    def __init__(self):
        cantidad_parkings=25

        engine=create_engine('sqlite:///app/db/basedatos.sqlite')
        Base.metadata.create_all(engine)
        Session= sessionmaker(bind=engine)
        session= Session()
        self.inicializar_tablas(cantidad_parkings,session)

        


