class ResumenEstadia():
    def __init__(self,patente,tiempo,costo,precioBase,descuento,monto,descripcionDescuento):
        self.patente=patente
        self.tiempo=tiempo
        self.costo=costo
        self.preciobase=precioBase
        self.descuento=descuento
        self.descripcionDescuento=descripcionDescuento
        self.monto=monto
class ResumenPagoCochera():
    def __init__(self,documento,nombre,fechaVencimiento,fechaDeseada,mesesDeuda,valorDescuento,descripcionDescuento,precioMes,monto):
        self.documento=documento
        self.nombre=nombre
        self.fechaVencimiento=fechaVencimiento
        self.fechaDeseada=fechaDeseada
        self.mesesDeuda=mesesDeuda
        self.valorDescuento=valorDescuento
        self.descripcionDescuento=descripcionDescuento
        self.precioMes=precioMes
        self.monto=monto
class FinPagoMensual():
    def __init__(self,documento,nombre,mesesPagar,mesesOcupar,costo,valorDescuento,descripcionDescuento,monto):
        self.documento=documento
        self.nombre=nombre
        self.mesesPagar=mesesPagar
        self.mesesOcupar=mesesOcupar
        self.costo=costo
        self.valorDescuento=valorDescuento
        self.descripcionDescuento=descripcionDescuento
        self.monto=monto
    