from datetime import datetime,timedelta


def hola():
    num=1
    letra="a"
    return {'num':num,'letra':letra}

print(hola()['num'])
print(hola()['letra'])

fechaHoraIngreso="25/11/2022 18:29:34"
fechaHoraEgreso="25/11/2022 21:23:57"
fecha1=datetime.strptime(fechaHoraIngreso,"%d/%m/%Y %H:%M:%S")
fecha2=datetime.strptime(fechaHoraEgreso,"%d/%m/%Y %H:%M:%S")
tiempoEstadia=(fecha2-fecha1)/timedelta(minutes=1)
print(tiempoEstadia)