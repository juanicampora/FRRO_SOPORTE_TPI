import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base,Precio,Descuento,Cliente,Trabajador,Parking,Estadia

from sqlalchemy.ext.declarative import declarative_base

class bbdd():
    def __init__(self):
        cantidad_parkings=25

        engine=create_engine('sqlite:///db/basedatossss.sqlite')
        Base.metadata.create_all(engine)
        Session= sessionmaker(bind=engine)
        session= Session()
    
    # db.inicializar_tablas()




# def inicializar_tablas():
    # for i in range(cantidad_parkings):
        # pisoaleatorio=randint(1,3)
        # cursor.execute('''INSERT INTO parking (piso,ocupado)
                            # VALUES(?,?)''', (pisoaleatorio,0))


