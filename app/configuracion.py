import os.path

class Config:
    DEBUG=True #OJO QUE TENIENDO EN TRUE HACE QUE AL PRINCIPIO SE EJECUTE T0D0 2 VECES
    CARPETA_TEMPLATES=os.path.abspath('./app/views/templates')
    CARPETA_STATIC=os.path.abspath('./app/views/static')
    SECRET_KEY='unallavesecretaredificil'
    cantParkings=10
    cantPisos=3                 #MODIFICAR en basedatos.py PARA QUE SIRVA CON X CANTIDAD DE PISOS
    maximoParkingsMensuales=3
    formatoFecha='%d/%m/%Y %H:%M:%S'
    formatoFechaCorta='%d/%m/%Y'