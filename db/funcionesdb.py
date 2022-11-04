import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import db.models

from sqlalchemy.ext.declarative import declarative_base

cantidad_parkings=25

engine=create_engine('sqlite:///db/basedatossss.sqlite')
Session= sessionmaker(bind=engine)
session= Session()
funcdb.Base.metadata.create_all(funcdb.engine)
    # db.inicializar_tablas()

Base = declarative_base()



# def inicializar_tablas():
    # for i in range(cantidad_parkings):
        # pisoaleatorio=randint(1,3)
        # cursor.execute('''INSERT INTO parking (piso,ocupado)
                            # VALUES(?,?)''', (pisoaleatorio,0))


