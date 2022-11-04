from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Precio(Base):
    __tablename__ = 'precio'
    idPrecio    = Column(Integer,   primary_key=True,   autoincrement=True)
    precioBase  = Column(Float,     nullable=False)
    precioMinuto= Column(Float,     nullable=False)
    fechaPrecio = Column(String,    nullable=False)
    vigente     = Column(Boolean,   nullable=False,     default=True)

    def __init__(self, idPrecio, precioBase,precioMinuto,fechaPrecio, vigente):
        self.idPrecio=idPrecio
        self.precioBase=precioBase
        self.precioMinuto=precioMinuto
        self.fechaPrecio=fechaPrecio
        self.vigente=vigente

class Descuento(Base):
    __tablename__ = 'descuento'
    idDescuento   = Column(Integer, primary_key=True,   autoincrement=True)
    descripcion   = Column(String,  nullable=False)
    valor         = Column(Float,   nullable=False) 
    vigente       = Column(Boolean, nullable=False,     default=True)

    def __init__(self, idDescuento, descripcion, valor, vigente):
        self.idDescuento=idDescuento
        self.descripcion=descripcion
        self.valor=valor
        self.vigente=vigente

class Cliente(Base):
    __tablename__ = 'cliente'
    patente       = Column(Integer, primary_key=True)
    celular       = Column(Integer)
    idDescuento   = Column(Integer, ForeignKey('descuento.idDescuento'))

    def __init__(self, patente, celular, idDescuento):
        self.patente=patente
        self.celular=celular
        self.idDescuento=idDescuento

class Trabajador(Base):
    __tablename__ = 'trabajador'
    usuario       = Column(String, primary_key=True)
    password      = Column(String, nullable=False)
    nombreApellido= Column(String, nullable=False)

    def __init__(self, usuario, password, nombreApellido):
        self.usuario=usuario
        self.password=password
        self.nombreApellido=nombreApellido

class Parking(Base):
    __tablename__ = 'parking'
    nroParking    = Column(Integer, primary_key=True, autoincrement=True)
    piso          = Column(Integer, nullable=False)
    ocupado       = Column(Boolean, nullable=False, default=False)

    def __init__(self, nroParking, piso, ocupado):
        self.nroParking=nroParking
        self.piso=piso
        self.ocupado=ocupado

class Estadia(Base):
    __tablename__ = 'estadia'
    patente = Column(String, ForeignKey('cliente.patente'), primary_key=True)
    fechaHoraIngreso = Column(String, primary_key=True)
    fechaHoraEgreso  = Column(String)
    nroParking       = Column(Integer, ForeignKey('parking.nroParking'), nullable=False)

    def __init__(self, patente, fechaHoraIngreso, fechaHoraEgreso, nroParking):
        self.patente=patente
        self.fechaHoraIngreso=fechaHoraIngreso
        self.fechaHoraEgreso=fechaHoraEgreso
        self.nroParking=nroParking