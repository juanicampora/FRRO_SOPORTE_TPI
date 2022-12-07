from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Trabajador(Base,UserMixin):
    __tablename__ = 'trabajador'
    id            = Column(Integer, primary_key=True)
    usuario       = Column(String, nullable=False)
    password      = Column(String, nullable=False)
    nombreApellido= Column(String, nullable=False)


    def __init__(self, usuario, password, nombreApellido):
        self.usuario=usuario
        self.password=generate_password_hash(password)
        self.nombreApellido=nombreApellido

    @classmethod
    def check_password(self,hashed_password,password):
        return check_password_hash(hashed_password,password)

class Precio(Base):
    __tablename__ = 'precio'
    idPrecio    = Column(Integer,   primary_key=True,   autoincrement=True)
    precioBase  = Column(Float,     nullable=False)
    precioMinuto= Column(Float,     nullable=False)
    fechaAlta   = Column(String,    nullable=False)
    fechaBaja   = Column(String,    nullable=True)

    def __init__(self, idPrecio, precioBase,precioMinuto,fechaAlta, fechaBaja):
        self.idPrecio=idPrecio
        self.precioBase=precioBase
        self.precioMinuto=precioMinuto
        self.fechaAlta=fechaAlta
        self.fechaBaja=fechaBaja

class Descuento(Base):
    __tablename__ = 'descuento'
    idDescuento   = Column(Integer, primary_key=True,   autoincrement=True)
    descripcion   = Column(String,  nullable=False)
    valor         = Column(Integer, nullable=False) 
    vigente       = Column(Boolean, nullable=False,     default=True)

    def __init__(self, idDescuento, descripcion, valor, vigente):
        self.idDescuento=idDescuento
        self.descripcion=descripcion
        self.valor=valor
        self.vigente=vigente

class Cliente(Base):
    __tablename__ = 'cliente'
    patente       = Column(String, primary_key=True)
    celular       = Column(Integer, nullable=True)
    activo        = Column(Boolean, nullable=False)
    idDescuento   = Column(Integer, ForeignKey('descuento.idDescuento') ,nullable=True)

    def __init__(self, patente, celular, activo):
        self.patente=patente
        self.celular=celular
        self.activo=activo

class Parking(Base):
    __tablename__ = 'parking'
    nroParking    = Column(Integer, primary_key=True)
    piso          = Column(Integer, nullable=False)
    ocupado       = Column(Boolean, nullable=False, default=False)
    mensual       = Column(Boolean, nullable=False, default=False)

    def __init__(self, nroParking, piso, ocupado):
        self.nroParking=nroParking
        self.piso=piso
        self.ocupado=ocupado

class Estadia(Base):
    __tablename__    = 'estadia'
    patente          = Column(String, ForeignKey('cliente.patente'), primary_key=True)
    fechaHoraIngreso = Column(String, primary_key=True)
    fechaHoraEgreso  = Column(String, nullable=True)
    nroParking       = Column(Integer, ForeignKey('parking.nroParking'), nullable=False)

    def __init__(self, patente, fechaHoraIngreso, fechaHoraEgreso, nroParking):
        self.patente=patente
        self.fechaHoraIngreso=fechaHoraIngreso
        self.fechaHoraEgreso=fechaHoraEgreso
        self.nroParking=nroParking

class ClienteMensual(Base):
    __tablename__ = 'clientemensual'
    documento     = Column(String,  primary_key=True)
    nombre        = Column(String,  nullable=False)
    celular       = Column(Integer, nullable=True)
    activo        = Column(Boolean, nullable=False)
    nroParking    = Column(Integer, ForeignKey('parking.nroParking'), nullable=False)
    idDescuento   = Column(Integer, ForeignKey('descuento.idDescuento') ,nullable=True)

    def __init__(self, documento,nombre,celular,activo,nroParking,idDescuento):
        self.documento=documento
        self.nombre=nombre
        self.celular=celular
        self.activo=activo
        self.nroParking=nroParking
        self.idDescuento=idDescuento

class Abono(Base):
    __tablename__    = 'abono'
    documento        = Column(String, ForeignKey('clientemensual.documento'), primary_key=True)
    fechaInicio      = Column(String, primary_key=True)
    fechaDeseada     = Column(String, nullable=True)
    fechaVencimiento = Column(String, nullable=True)
    fechaFin         = Column(String, nullable=True)

    def __init__(self, documento, fechaInicio, fechaDeseada, fechaVencimiento):
        self.documento=documento
        self.fechaInicio=fechaInicio
        self.fechaDeseada=fechaDeseada
        self.fechaVencimiento=fechaVencimiento
