def buscar(*args):
    a = args[0] + 2
    b = args[1] + 3
    c = args[2] + 4
    d = args[3] + 5
    e = args[4] + 6
    return a,b,c,d,e

print(buscar(1,2,3,4,5))
from datetime import datetime, timedelta

d = datetime.today().day
m = datetime.today().month
y = datetime.today().year

ahora = datetime(y,m,d)


inicio1 = datetime(2020,1,1)
final1 = datetime(2020,1,10)
inicio2 = datetime(2020,1,22)
final2 = datetime(2020,2,6)
inicio3 = datetime(2020,2,19)
final3 = datetime(2020,3,4)
inicio4 = datetime(2020,3,17)
final4 = datetime(2020,3,31)
inicio5 = datetime(2020,4,13)
final5 = datetime(2020,4,27)
inicio6 = datetime(2020,5,10)
final6 = datetime(2020,5,25)
inicio7 = datetime(2020,6,6)
final7 = datetime(2020,6,21)
inicio8 = datetime(2020,7,4)
final8 = datetime(2020,7,18)
inicio9 = datetime(2020,7,31)
final9 = datetime(2020,8,14)
inicio10 = datetime(2020,8,27)
final10 = datetime(2020,9,11)
inicio11 = datetime(2020,9,23)
final11 = datetime(2020,10,8)
inicio12 = datetime(2020,10,20)
final12 = datetime(2020,11,4)
inicio13 = datetime(2020,11,17)
final13 = datetime(2020,12,1)
inicio14 = datetime(2020,12,14)
final14 = datetime(2020,12,28)

lista_fechas1 = [inicio1 + timedelta(days=d) for d in range((final1 - inicio1).days +1)]
lista_fechas2 = [inicio2 + timedelta(days=d) for d in range((final2 - inicio2).days +1)]
lista_fechas3 = [inicio3 + timedelta(days=d) for d in range((final3 - inicio3).days +1)]
lista_fechas4 = [inicio4 + timedelta(days=d) for d in range((final4 - inicio4).days +1)]
lista_fechas5 = [inicio5 + timedelta(days=d) for d in range((final5 - inicio5).days +1)]
lista_fechas6 = [inicio6 + timedelta(days=d) for d in range((final6 - inicio6).days +1)]
lista_fechas7 = [inicio7 + timedelta(days=d) for d in range((final7 - inicio7).days +1)]
lista_fechas8 = [inicio8 + timedelta(days=d) for d in range((final8 - inicio8).days +1)]
lista_fechas9 = [inicio9 + timedelta(days=d) for d in range((final9 - inicio9).days +1)]
lista_fechas10 = [inicio10 + timedelta(days=d) for d in range((final10 - inicio10).days +1)]
lista_fechas11 = [inicio11 + timedelta(days=d) for d in range((final11 - inicio11).days +1)]
lista_fechas12 = [inicio12 + timedelta(days=d) for d in range((final12 - inicio12).days +1)]
lista_fechas13 = [inicio13 + timedelta(days=d) for d in range((final13 - inicio13).days +1)]
lista_fechas14 = [inicio14 + timedelta(days=d) for d in range((final14 - inicio14).days +1)]

lista_fechas15 = [final1 + timedelta(days=d) for d in range((final1 - inicio1).days + 4)]
lista_fechas16 = [final2 + timedelta(days=d) for d in range((final2 - inicio2).days -1)]
lista_fechas17 = [final3 + timedelta(days=d) for d in range((final3 - inicio3).days)]
lista_fechas18 = [final4 + timedelta(days=d) for d in range((final4 - inicio4).days)]
lista_fechas19 = [final5 + timedelta(days=d) for d in range((final5 - inicio5).days)]
lista_fechas20 = [final6 + timedelta(days=d) for d in range((final6 - inicio6).days -2)]
lista_fechas21 = [final7 + timedelta(days=d) for d in range((final7 - inicio7).days -1)]
lista_fechas22 = [final8 + timedelta(days=d) for d in range((final8 - inicio8).days)]
lista_fechas23 = [final9 + timedelta(days=d) for d in range((final9 - inicio9).days)]
lista_fechas24 = [final10 + timedelta(days=d) for d in range((final10 - inicio10).days -2)]
lista_fechas25 = [final11 + timedelta(days=d) for d in range((final11 - inicio11).days -2)]
lista_fechas26 = [final12 + timedelta(days=d) for d in range((final12 - inicio12).days -1)]
lista_fechas27 = [final13 + timedelta(days=d) for d in range((final13 - inicio13).days)]
lista_fechas28 = [final14 + timedelta(days=d) for d in range((final14 - inicio14).days -10)]



dia_0 = ahora
dia_1 = ahora + timedelta(days=1)
dia_2 = ahora + timedelta(days=2)
dia_3 = ahora + timedelta(days=3)
dia_4 = ahora + timedelta(days=4)
dia_5 = ahora + timedelta(days=5)
dia_6 = ahora + timedelta(days=6)
dia_7 = ahora + timedelta(days=7)
dia_8 = ahora + timedelta(days=8)
dia_9 = ahora + timedelta(days=9)
dia_10 = ahora + timedelta(days=10)
dia_11 = ahora + timedelta(days=11)
dia_12 = ahora + timedelta(days=12)
dia_13 = ahora + timedelta(days=13)
dia_14 = ahora + timedelta(days=14)
dia_15 = ahora + timedelta(days=15)
dia_16 = ahora + timedelta(days=16)
dia_17 = ahora + timedelta(days=17)
dia_18 = ahora + timedelta(days=18)
dia_19 = ahora + timedelta(days=19)
dia_20 = ahora + timedelta(days=20)
dia_21 = ahora + timedelta(days=21)
dia_22 = ahora + timedelta(days=22)
dia_23 = ahora + timedelta(days=23)

dias = [dia_0,dia_1,dia_2,dia_3,dia_4,dia_5,dia_6,dia_7,dia_8,dia_9,dia_10,dia_11,dia_12,dia_13,dia_14,dia_15,dia_16,dia_17,dia_18,dia_19,dia_20,dia_21,dia_22,dia_23]
dias_ascenso = []
dias_descenso = []

def buscarascenso(lista):
    for i in dias:
        if i in lista:
            dias_ascenso.append(i)
    return dias_ascenso

def buscardescenso(lista):
    for i in dias:
        if i in lista:
            dias_descenso.append(i)
    return dias_descenso


def buscar(lista):
    if ahora in lista:
        return True
    else:
        return False

def buscarsiguiente1(lista):
    if dia_1 in lista:
        return True
    else:
        return False

def buscarsiguiente2(lista):
    if dia_2 in lista:
        return True
    else:
        return False
def buscarsiguiente3(lista):
    if dia_3 in lista:
        return True
    else:
        return False
def buscarsiguiente4(lista):
    if dia_4 in lista:
        return True
    else:
        return False
def buscarsiguiente5(lista):
    if dia_5 in lista:
        return True
    else:
        return False
def buscarsiguiente6(lista):
    if dia_6 in lista:
        return True
    else:
        return False


ascendente = False

b1 = map(buscar,
           [lista_fechas1, lista_fechas2, lista_fechas3, lista_fechas4, lista_fechas5, lista_fechas6, lista_fechas7,
            lista_fechas8, lista_fechas9, lista_fechas10, lista_fechas11, lista_fechas12, lista_fechas13, lista_fechas14])
b2 = map(buscarsiguiente1,
            [lista_fechas1, lista_fechas2, lista_fechas3, lista_fechas4, lista_fechas5, lista_fechas6, lista_fechas7,
             lista_fechas8, lista_fechas9, lista_fechas10, lista_fechas11, lista_fechas12, lista_fechas13,lista_fechas14])
b3 = map(buscarsiguiente2,
            [lista_fechas1, lista_fechas2, lista_fechas3, lista_fechas4, lista_fechas5, lista_fechas6, lista_fechas7,
             lista_fechas8, lista_fechas9, lista_fechas10, lista_fechas11, lista_fechas12, lista_fechas13,lista_fechas14])
b4 = map(buscarsiguiente3,
            [lista_fechas1, lista_fechas2, lista_fechas3, lista_fechas4, lista_fechas5, lista_fechas6, lista_fechas7,
             lista_fechas8, lista_fechas9, lista_fechas10, lista_fechas11, lista_fechas12, lista_fechas13,lista_fechas14])
b5 = map(buscarsiguiente4,
            [lista_fechas1, lista_fechas2, lista_fechas3, lista_fechas4, lista_fechas5, lista_fechas6, lista_fechas7,
             lista_fechas8, lista_fechas9, lista_fechas10, lista_fechas11, lista_fechas12, lista_fechas13,lista_fechas14])
b6 = map(buscarsiguiente5,
            [lista_fechas1, lista_fechas2, lista_fechas3, lista_fechas4, lista_fechas5, lista_fechas6, lista_fechas7,
             lista_fechas8, lista_fechas9, lista_fechas10, lista_fechas11, lista_fechas12, lista_fechas13,lista_fechas14])
b7 = map(buscarsiguiente6,
            [lista_fechas1, lista_fechas2, lista_fechas3, lista_fechas4, lista_fechas5, lista_fechas6, lista_fechas7,
             lista_fechas8, lista_fechas9, lista_fechas10, lista_fechas11, lista_fechas12, lista_fechas13,lista_fechas14])
b8 = map(buscarascenso,
            [lista_fechas1, lista_fechas2, lista_fechas3, lista_fechas4, lista_fechas5, lista_fechas6, lista_fechas7,
             lista_fechas8, lista_fechas9, lista_fechas10, lista_fechas11, lista_fechas12, lista_fechas13,lista_fechas14])
b9 = map(buscardescenso,
            [lista_fechas15, lista_fechas16, lista_fechas17, lista_fechas18, lista_fechas19, lista_fechas20, lista_fechas21,
             lista_fechas22, lista_fechas23, lista_fechas24, lista_fechas25, lista_fechas26, lista_fechas27,lista_fechas28])


def declarar(coso):
    for i in coso:
        if i:
            ascendente = True
            return ascendente


# if ascendente:
#       print('La luna es ascendente')
# else:
#       print('La luna es descendente')
print('Para el dia de hoy ' + str(ahora) + ':')
if declarar(b1):
    print('Hoy la luna es ascendente')
else:
    print('Hoy la luna es descendente')
for i in b8:
    pass
for i in dias_ascenso:
    print(f'Dias de ascenso {i}')
print('##################')
for i in b9:
    pass
for i in dias_descenso:
    print(f'Dias de descenso {i}')

print(lista_fechas3)
print(lista_fechas16)
for i in dias:
    if i in dias_ascenso:
        print(f'{i} luna ascendente')
    if i in dias_descenso:
        print(f'{i} luna descendente')
