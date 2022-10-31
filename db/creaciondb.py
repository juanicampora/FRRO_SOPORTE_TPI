"""Creacion e Inicializacion de las Tablas de la Base de Datos SQL"""

from random import randint
import sqlite3

conn=sqlite3.connect('db/basedatos.db')
cursor=conn.cursor()

cantidad_parkings=25


# Tener en cuenta que los tipos de variables que soporta SQLITE son: NULL, INTEGER, REAL, TEXT, BLOB
# Para el tpi vamos a usar INTEGER en vez de BOOLEAN, TEXT en vez de DATE
def crear_tablas():
    #Tabla Precio
    cursor.execute('''CREATE TABLE IF NOT EXISTS precio (
                    idPrecio INTEGER PRIMARY KEY AUTOINCREMENT,
                    precioBase REAL NOT NULL,
                    precioMinuto REAL NOT NULL,
                    fechaPrecio TEXT NOT NULL,
                    vigente INTEGER NOT NULL
                    )''')
    #Tabla Descuento
    cursor.execute('''CREATE TABLE IF NOT EXISTS descuento (
                    idDescuento INTEGER PRIMARY KEY AUTOINCREMENT,
                    descripcion TEXT NOT NULL,
                    valor REAL NOT NULL,
                    vigente INTEGER NOT NULL
                    )''')                
    #Tabla Cliente
    cursor.execute('''CREATE TABLE IF NOT EXISTS cliente (
                    patente INTEGER PRIMARY KEY,
                    celular INTEGER,
                    idDescuento INTEGER,
                    FOREIGN KEY (idDescuento) REFERENCES descuento(idDescuento)
                    )''')
    #Tabla Trabajador
    cursor.execute('''CREATE TABLE IF NOT EXISTS trabajador (
                    usuario TEXT PRIMARY KEY,
                    password TEXT NOT NULL,
                    nombreApellido TEXT NOT NULL
                    )''')
    #Tabla Parking
    cursor.execute('''CREATE TABLE IF NOT EXISTS parking (
                    nroParking INTEGER PRIMARY KEY AUTOINCREMENT,
                    piso INTEGER NOT NULL,
                    ocupado INTEGER NOT NULL
                    )''')
    #Tabla Estadia
    cursor.execute('''CREATE TABLE IF NOT EXISTS estadia (
                    patente TEXT,
                    fechaHoraIngreso TEXT,
                    fecha_nacimiento TEXT,
                    nroParking INTEGER NOT NULL,
                    FOREIGN KEY (patente) REFERENCES cliente(patente),
                    FOREIGN KEY (nroParking) REFERENCES parking(nroParking)
                    PRIMARY KEY(patente,fechaHoraIngreso)
                    )''')
    conn.commit()

def inicializar_tablas():
    for i in range(cantidad_parkings):
        pisoaleatorio=randint(1,3)
        cursor.execute('''INSERT INTO parking (piso,ocupado)
                            VALUES(?,?)''', (pisoaleatorio,0))
    conn.commit()

# crear_tablas()
# inicializar_tablas()

conn.close()
