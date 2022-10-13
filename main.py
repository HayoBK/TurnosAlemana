# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %%
# Aqui copiar desde Pythonista
# %%
import math
import heapq
import datetime
from datetime import timedelta

import matplotlib.pyplot as plt

# %%
COVID_Val_DS = 1  # Valor dia de semana
COVID_Val_FD = 1.5  # Valor fin de semana y feriado

AM = 1  # Valor una mañana de lunes a viernes
PM = 1.2  # Valor una tarde de lunes a jueves
FridayPM = 1.5  # Valor una tarde de viernes
Night = 2  # Valor una noche de lunes a viernes 1.5
WeekEnd = 6.3  # Valor un sabado o un domingo     5.5.
# Valor WeekEnd es 1.5 veces el valor
# sumado de AM+PM+Night
print('Calculando...')
# %%
print('Valoracion de cada tipo de Turno')
print('@ Valor Mañanas=', AM)
print('@ Valor Tardes= ', PM)
print('@ Valor Viernes Tardes=', FridayPM)
print('@ Valor Noches= ', Night)
print('@ Valor Fines de Semana (sabado o domingo)=', WeekEnd)
print('  El valor de un fin de semana es el 150% del valor ')
print('  de la suma de la mañana-tarde-noche de un dia de  ')
print('  lunes a jueves ')

# %%
# Definir Clase para mantener informacion de
# cada dia calendario
Dias_de_Semana = 0
Dias_de_Fin_de_Semana = 0
C_AM = 0
C_PM = 0
C_FridayPM = 0
C_Night = 0
C_WeekEnd = 0
meses = 9  # meses a evaluar y asignar


class UnDia:
    def __init__(self, SuFecha):
        self.fecha = SuFecha
        self.N_AM = "Sin asignar"
        self.N_PM = "Sin asignar"
        self.N_Night = "Sin asignar"

        F = []
        F.append(datetime.date(2021, 4, 2))
        F.append(datetime.date(2021, 4, 3))
        F.append(datetime.date(2021, 4, 4))

        F.append(datetime.date(2021, 5, 21))
        F.append(datetime.date(2021, 5, 22))
        F.append(datetime.date(2021, 5, 23))

        F.append(datetime.date(2021, 6, 28))
        F.append(datetime.date(2021, 6, 27))
        F.append(datetime.date(2021, 6, 26))

        F.append(datetime.date(2021, 7, 16))
        F.append(datetime.date(2021, 7, 17))
        F.append(datetime.date(2021, 7, 18))

        F.append(datetime.date(2021, 9, 17))
        F.append(datetime.date(2021, 9, 18))
        F.append(datetime.date(2021, 9, 19))

        F.append(datetime.date(2021, 10, 9))
        F.append(datetime.date(2021, 10, 10))
        F.append(datetime.date(2021, 10, 11))

        F.append(datetime.date(2021, 10, 30))
        F.append(datetime.date(2021, 10, 31))

        F.append(datetime.date(2021, 11, 1))

        F.append(datetime.date(2021, 12, 8))
        F.append(datetime.date(2021, 12, 24))
        F.append(datetime.date(2021, 12, 25))
        F.append(datetime.date(2021, 12, 26))
        F.append(datetime.date(2021, 12, 31))

        F.append(datetime.date(2022, 1, 1))
        F.append(datetime.date(2022, 1, 2))

        self.Feriado = 0
        for f in F:
            if self.fecha == f:
                self.N_AM = "Feriado o Especial"
                self.N_PM = "Feriado o Especial"
                self.N_Night = "Feriado o Especial"
                self.wDay = "Feriado o Especial"
                self.Feriado = 1

        if self.Feriado == 0:
            if self.fecha.isoweekday() < 5:
                self.tipodia = "Lunes a Jueves"
                global C_AM
                C_AM += 1
                global C_PM
                C_PM += 1
                global C_Night
                C_Night += 1

            elif self.fecha.isoweekday() == 5:
                self.tipodia = "Viernes"
                # global C_AM
                C_AM += 1
                global C_FridayPM
                C_FridayPM += 1
                # global C_Night
                C_Night += 1

            else:
                self.tipodia = "Fin de Semana"
                global C_WeekEnd
                C_WeekEnd += 1

        # asignacion Feriados, Fin de Semana Largos

        # print(SuFecha,' es un ',self.tipodia)


# %%
# Fijar fechas de inicio y final de la generacion
# de turnoS
fecha_inicio = datetime.date(2021, 3, 29)
fecha_final = datetime.date(2022, 1, 2)
rfecha = fecha_inicio
Dia = []
Conteo_Dias_Semana = 0
Conteo_Dias_Fin_de_Semana = 0

# Ciclo inicial para definir calendario basico
while rfecha <= fecha_final:
    Dia.append(UnDia(rfecha))  # Aqui se genera un dia del calendario
    rfecha = rfecha + timedelta(days=1)

# %%
# Dias_de_Semana = 60
# Dias_de_Fin_de_Semana = 26
# %%
delta = 10  # año de referencia
CZERO_AM = 0
CZERO_PM = 0
CZERO_Night = 3.66
CZERO_FridayPM = 1
CZERO_WeekEnd = 1.33

CargaZERO = CZERO_AM * AM + CZERO_PM * PM + CZERO_FridayPM * FridayPM + CZERO_Night * Night + CZERO_WeekEnd * WeekEnd

C12_AM = 4
C12_PM = 0
C12_Night = 0
C12_FridayPM = 0
C12_WeekEnd = 0.33

Carga12 = C12_AM * AM + C12_PM * PM + C12_FridayPM * FridayPM + C12_Night * Night + C12_WeekEnd * WeekEnd

m = (Carga12 - CargaZERO) / delta
n = delta - m * Carga12
m = -0.9  # ESTE VALOR "APLANA la curva de distribución"
n = 16.75
print('m= ', m)
print('n= ', n)

# %%

# Definir Clase para manejar los datos de cada medico
total_LoadScore = 0
total_FindeSemanaScore = 0
CheckCargaAntiq2021 = 0


class Medico:
    def __init__(self, id, nombre, año, mes, dia, Cat):
        self.A_AM = 0
        self.A_PM = 0
        self.A_FridayPM = 0
        self.A_Night = 0
        self.A_WeekEnd = 0

        self.Conteo_Sabados = 0
        self.Conteo_Domingos = 0

        self.id = int(id)
        self.nombre = nombre
        self.ingreso = datetime.date(año, mes, dia)
        self.Cat = Cat
        self.Medida = datetime.date(2021, 4, 1)  # Aqui se fija el dia en el que se mide antiguedad
        Dif = self.Medida - self.ingreso
        self.Antiq = Dif.days / 365
        self.CargaAntiq2021 = self.Antiq * m + n  # -self.Antiq*0.0075+0.1212
        if self.Cat == 'AUSENTE':
            self.CargaAntiq2021 = 0
        global CheckCargaAntiq2021
        CheckCargaAntiq2021 += self.CargaAntiq2021

        self.CargaReal = 0

        self.AntiqNz = (self.Antiq / 12) - 0.5
        self.LoadScore = 1 - self.AntiqNz + 0.5
        global total_LoadScore
        total_LoadScore += self.LoadScore
        global total_FindeSemanaScore
        if self.Cat != 'Yoda-Sin Noches':
            total_FindeSemanaScore += self.LoadScore


Medicos = []
Medicos.append(Medico(0, 'Emmerich', 2010, 5, 1, 'Yoda-Sin Noches'))
Medicos.append(Medico(1, 'Finkelstein', 2011, 1, 1, 'Yoda-Sin Noches'))
Medicos.append(Medico(2, 'Fernandez', 2012, 2, 1, 'Master-Mañanas'))
Medicos.append(Medico(3, 'Gomez', 2013, 7, 1, 'Master-Mañanas'))
Medicos.append(Medico(4, 'Bravo', 2013, 7, 1, 'Master-Mañanas'))
Medicos.append(Medico(5, 'Iñiguez', 2014, 1, 1, 'Knight-Tardes'))
Medicos.append(Medico(6, 'Breinbauer', 2014, 1, 1, 'Knight-Tardes'))
Medicos.append(Medico(7, 'Arredondo', 2014, 8, 1, 'Knight-Tardes'))
Medicos.append(Medico(8, 'Carrasco', 2014, 8, 1, 'Padawan-Sin Fijo'))
Medicos.append(Medico(9, 'Culaciati', 2014, 8, 1, 'Knight-Tardes'))
Medicos.append(Medico(10, 'Contreras', 2017, 1, 1, 'AUSENTE'))
Medicos.append(Medico(11, 'Cisternas', 2017, 11, 1, 'Padawan-Sin Fijo'))
Medicos.append(Medico(12, 'Pio', 2018, 1, 13, 'Padawan-Sin Fijo'))
Medicos.append(Medico(13, 'Alvo', 2019, 11, 1, 'Padawan-Sin Fijo'))
# Medicos.append(Medico(14,'Newbie',2020,3,1,'Padawan-Sin Fijo'))
Max_Medicos_id = 13
check2 = 0
check3 = 0
Dias_de_Semana_Asignados = 0
Dias_Fin_de_Semana_Asignados = 0
# %%
Check = 0
for med in Medicos:
    med.CargaAntiq2021 = med.CargaAntiq2021 / CheckCargaAntiq2021
    Check += med.CargaAntiq2021
# %%
# for med in Medicos:
#    print(med.nombre)
#    print(med.Antiq)
#    print(med.CargaAntiq2021)

# print(CheckCargaAntiq2021)
# print(Check)
# %%
print('AM:', C_AM)
print('PM:', C_PM)
print('FridayPM:', C_FridayPM)
print('Night:', C_Night)
print('Weekend:', C_WeekEnd)
CargaMaxima = C_AM * AM + C_PM * PM + C_FridayPM * FridayPM + C_Night * Night + C_WeekEnd * WeekEnd
print('Carga Maxima del periodo: ', CargaMaxima)
Count_AM = C_AM
Count_PM = C_PM
Count_FridayPM = C_FridayPM
Count_Night = C_Night
Count_WeekEnd = C_WeekEnd
# %%
Check = 0
for med in Medicos:
    med.CargaMax = 0  # Maxima carga a asignar durante el periodo
    med.CargaRestante = med.CargaMax  # Lo que queda por asignar aun
    med.CargaReal = 0  # Lo asignado
    if med.Cat != 'AUSENTE':
        med.CargaMax = med.CargaAntiq2021 * CargaMaxima
        med.CargaRestante = med.CargaMax
        Check += med.CargaMax
    print(med.nombre, ' tiene una carga a asignar de ', med.CargaMax)
print('Los siguientes numeros deben ser iguales =', CargaMaxima, ' y ', Check)
# %%
for dia in Dia:
    NombreAM = 'Sin asignar'
    NombrePM = 'Sin asignar'
    # print(dia.fecha,' es un ',dia.tipodia)
    if dia.Feriado == 0:
        if dia.fecha.isoweekday() == 1:
            NombreAM = 'Emmerich'
            NombrePM = 'Iñiguez'
            dia.wDay = 'Lunes'
        elif dia.fecha.isoweekday() == 2:
            NombreAM = 'Finkelstein'
            NombrePM = 'Breinbauer'
            dia.wDay = 'Martes'
        elif dia.fecha.isoweekday() == 3:
            NombreAM = 'Fernandez'
            NombrePM = 'Arredondo'
            dia.wDay = 'Miércoles'
        elif dia.fecha.isoweekday() == 4:
            NombreAM = 'Bravo'
            NombrePM = 'Culaciati'
            dia.wDay = 'Jueves'
        elif dia.fecha.isoweekday() == 5:
            NombreAM = 'Gomez'
            dia.wDay = 'Viernes'
        elif dia.fecha.isoweekday() == 6:
            dia.wDay = 'Sábado'
        elif dia.fecha.isoweekday() == 7:
            dia.wDay = 'Domingo'

        if dia.fecha.isoweekday() < 6:
            for med in Medicos:
                if med.nombre == NombreAM:
                    C_AM -= 1
                    med.CargaReal += AM
                    dia.N_AM = NombreAM
                    med.A_AM += 1
                    print('La mañana la hace ', dia.N_AM)
                if med.nombre == NombrePM:
                    C_PM -= 1
                    med.CargaReal += PM
                    dia.N_PM = NombrePM
                    med.A_PM += 1

                    print('La tarde la hace ', dia.N_PM)

# %%
print('AM:', C_AM)
print('PM:', C_PM)
print('FridayPM:', C_FridayPM)
print('Night:', C_Night)
print('Weekend:', C_WeekEnd)
# %%
# update Carga
CargaRestanteTotal = 0
for med in Medicos:
    med.CargaRestante = med.CargaMax - med.CargaReal
    CargaRestanteTotal += med.CargaRestante
    print('A ', med.nombre, ' queda por asignarle: ', med.CargaRestante)

print()

for med in Medicos:
    med.Factor = med.CargaRestante / CargaRestanteTotal
    print('A ', med.nombre, ' le corresponde proporcionalmente asignar: ', med.Factor)
# %%
# Asignar Numero de Viernes Tarde
# update Carga
CargaRestanteTotal = 0
for med in Medicos:
    if med.Cat == 'Padawan-Sin Fijo':
        med.CargaRestante = med.CargaMax - med.CargaReal
        CargaRestanteTotal += med.CargaRestante
        print('A ', med.nombre, ' queda por asignarle: ', med.CargaRestante)

print()

Check = C_FridayPM
for med in Medicos:
    if med.Cat == 'Padawan-Sin Fijo':
        med.Factor = med.CargaRestante / CargaRestanteTotal
        med.A_FridayPM = round(C_FridayPM * med.Factor)
        Check -= med.A_FridayPM
        print('A ', med.nombre, ' le corresponde proporcionalmente asignar: ', med.Factor)
        print('Lo que equivale a los siguientes turnos: ', med.A_FridayPM)

print()
print('Turno de Viernes tarde sin asingar -error - : ', Check)

C_FridayPM = Check
while Check != 0:
    for med in reversed(Medicos):
        if Check > 0:
            med.A_FridayPM += 1
            Check -= 1
        if Check < 0:
            med.A_FridayPM -= 1
            Check += 1

print('Turno de Viernes Tarde sin asingar -error - : ', Check)
C_FridayPM = Check
# %%
# Asignar Numero Fines de Semana
# update Carga
CargaRestanteTotal = 0
for med in Medicos:
    if (med.Cat == 'Knight-Tardes') or (med.Cat == 'Master-Mañanas') or (med.Cat == 'Padawan-Sin Fijo') or (med.Cat == 'Yoda-Sin Noches'):
        med.CargaRestante = med.CargaMax - med.CargaReal
        CargaRestanteTotal += med.CargaRestante
        print('A ', med.nombre, ' queda por asignarle: ', med.CargaRestante)

print()

Check = C_WeekEnd
for med in Medicos:
    if (med.Cat == 'Knight-Tardes') or (med.Cat == 'Master-Mañanas') or (med.Cat == 'Padawan-Sin Fijo') or (med.Cat == 'Yoda-Sin Noches'):
        med.Factor = med.CargaRestante / CargaRestanteTotal
        med.A_WeekEnd = round(C_WeekEnd * med.Factor)
        Check -= med.A_WeekEnd
        print('A ', med.nombre, ' le corresponde proporcionalmente asignar: ', med.Factor)
        print('Lo que equivale a los siguientes turnos: ', med.A_WeekEnd)

print()
print('Turno de Fin de Semana sin asingar -error - : ', Check)
C_WeekEnd = Check

while Check != 0:
    for med in reversed(Medicos):
        if Check > 0:
            med.A_WeekEnd += 1
            Check -= 1
        if Check < 0:
            med.A_WeekEnd -= 1
            Check += 1

print('Turno de Fin de Semana sin asingar -error - : ', Check)
C_WeekEnd = Check
# %%
print('AM:', C_AM)
print('PM:', C_PM)
print('FridayPM:', C_FridayPM)
print('Night:', C_Night)
print('Weekend:', C_WeekEnd)
# %%
# Asignar Numero Noches
# update Carga
CargaRestanteTotal = 0
for med in Medicos:
    if (med.Cat == 'Knight-Tardes') or (med.Cat == 'Master-Mañanas') or (med.Cat == 'Padawan-Sin Fijo'):
        med.CargaRestante = med.CargaMax - med.CargaReal
        CargaRestanteTotal += med.CargaRestante
        print('A ', med.nombre, ' queda por asignarle: ', med.CargaRestante)

print()

Check = C_Night
for med in Medicos:
    if (med.Cat == 'Knight-Tardes') or (med.Cat == 'Master-Mañanas') or (med.Cat == 'Padawan-Sin Fijo'):
        med.Factor = med.CargaRestante / CargaRestanteTotal
        med.A_Night = round(C_Night * med.Factor)
        Check -= med.A_Night
        print('A ', med.nombre, ' le corresponde proporcionalmente asignar: ', med.Factor)
        print('Lo que equivale a los siguientes turnos: ', med.A_Night)

print()
print('Turno de Noche sin asingar -error - : ', Check)
C_Night = Check

while Check != 0:
    for med in reversed(Medicos):
        if Check > 0:
            med.A_Night += 1
            Check -= 1
        if Check < 0:
            med.A_Night -= 1
            Check += 1

print('Turno de Noche sin asingar -error - : ', Check)
C_Night = Check
# %%
print('AM:', C_AM)
print('PM:', C_PM)
print('FridayPM:', C_FridayPM)
print('Night:', C_Night)
print('Weekend:', C_WeekEnd)
# %%

# %%
print('RESUMEN POR MEDICO')
print(' ')
ForPandas = []
Antiguedad = []
Carga = []
CargaT = []
Nombres = []
CargaBruta = []
GId = []

print('Valoracion de cada tipo de Turno')
print('@ Valor Mañanas=', AM)
print('@ Valor Tardes= ', PM)
print('@ Valor Viernes Tardes=', FridayPM)
print('@ Valor Noches= ', Night)
print('@ Valor Fines de Semana (sabado o domingo)=', WeekEnd)
print()

for med in Medicos:
    print(med.nombre, 'tendra %.2f años de antiguedad' % med.Antiq)
    print('  medido al ', med.Medida)
    print('  siendo Categoria:', med.Cat)
    # print('  con carga de maximo personal: %.2f ' % med.CargaMax)
    p = med.CargaMax / CargaMaxima * 100
    med.CargaReal = med.A_AM * AM + med.A_PM * PM + med.A_FridayPM * FridayPM + med.A_Night * Night + med.A_WeekEnd * WeekEnd
    med.CargaPorcentual = med.CargaReal / CargaMaxima * 100

    print('  con carga calculada (del total de carga del periodo): %.2f (Porcentaje) ' % p)
    print('  con carga real asignada (del total de carga del periodo): %.2f (Porcentaje) ' % med.CargaPorcentual)
    print('  @ Mañanas asignados = ', med.A_AM)
    print('  @ Tardes asignados = ', med.A_PM)
    print('  @ Noches asignados = ', med.A_Night)
    print('  @ Viernes Tardes asignados = ', med.A_FridayPM)
    print('  @ Fines de semana asignados = ', med.A_WeekEnd)
    print('  equivalente a %.2f Mañanas al mes' % (med.A_AM / meses))
    print('  equivalente a %.2f Tardes al mes' % (med.A_PM / meses))
    print('  equivalente a %.2f Noches al mes' % (med.A_Night / meses))
    print('  equivalente a %.2f Viernes Tarde al mes' % (med.A_FridayPM / meses))
    print('  equivalente a %.2f Fines de semana al mes' % (med.A_WeekEnd / meses))
    med.m_AM = med.A_AM / meses
    med.m_PM = med.A_PM / meses
    med.m_Night = med.A_Night / meses
    med.m_FridayPM = med.A_FridayPM / meses
    med.m_WeekEnd = med.A_WeekEnd / meses
    #	print('  Carga en puntaje bruto= %.2f' %(med.FinalLoad*TotalFinalLoad))
    #	OverLoad =(0-(med.OpLoad-med.FinalLoad)/med.OpLoad )*100
    #	print('  Porcentaje de sobrecarga= %.2f'%OverLoad)
    medList = [med.nombre, med.Antiq, med.Cat, (med.CargaMax / CargaMaxima * 100), med.CargaPorcentual, med.A_AM, med.A_PM, med.A_FridayPM, med.A_Night, med.A_WeekEnd, med.m_AM,
               med.m_PM, med.m_FridayPM, med.m_Night, med.m_WeekEnd]
    ForPandas.append(medList)
    Columnas2 = ['Medico', 'Antiguedad', 'Categoria', 'Carga Sugerida en Porcentaje del total', 'Carga Asignada en Porcentaje del total', 'Mañanas en el periodo',
                 'Tardes en el periodo', 'Viernes Tardes en el periodo', 'Noches en el periodo', 'Fines de Semana en el periodo', 'Mañanas promedio al mes',
                 'Tardes promedio al mes', 'Viernes promedio Tardes al mes', 'Noches promedio al mes', 'Fines de Semana promedio al mes']
    MedDF = pd.DataFrame(ForPandas, columns=Columnas2)
    Export2 = MedDF.to_excel('AA - Medicos Abril-Diciembre 2021.xlsx', index=None, header=True)
    # Columnas = 'Medico','Antiguedad','Categoria','Carga Teorica','Carga Real','Carga Real Bruta','SobreCarga(pctje)','Mañanas','Tardes','Noches','Viernes Tardes', 'Viernes Noches', 'Sabados', 'Domingos'
    Antiguedad.append(med.Antiq)
    Carga.append(med.CargaPorcentual)
    CargaT.append(med.CargaMax / CargaMaxima * 100)
    print(' ')
# CargaBruta.append((med.FinalLoad*TotalFinalLoad))
# Nombres.append(med.nombre)
# GId.append(med.id)

# %%

# %%
plt.scatter(Antiguedad, Carga)
plt.xlabel('Antiguedad')
plt.ylabel('Carga')
plt.show()

# %%
plt.scatter(Antiguedad, CargaT)
plt.xlabel('Antiguedad')
plt.ylabel('Carga Teorica')
plt.show()

# %%
# ORDENAR LISTA DE FINES DE SEMANA
TuList = []
for med in Medicos:
    if med.A_WeekEnd > 0:
        med.TCount = med.A_WeekEnd
        med.Fq = (Count_WeekEnd / med.TCount)
        med.Pri = med.Fq / 2
        heapq.heappush(TuList, (med.Pri, med.id, med.TCount, med.Fq))

LongListWeekEnd = []
AssignCount = 0
while Count_WeekEnd > AssignCount:
    B = heapq.heappop(TuList)
    if B[2] > 0:
        LongListWeekEnd.append(Medicos[B[1]].id)
        AssignCount += 1
        if (B[2] - 1) > 0:
            heapq.heappush(TuList, ((B[0] + B[3]), B[1], B[2] - 1, B[3]))
# print ('Secuencia Domingos:')
i = 0
FinalListWeekEnd = []
for L in LongListWeekEnd:
    heapq.heappush(FinalListWeekEnd, (i, Medicos[L].nombre))
    i += 1
    # print(i,L,Medicos[L].nombre)
# %%
# Asignar Fines de Semana a Calendario
InsD = 0
for D in Dia:
    # print(D.fecha.isoweekday())
    if D.fecha.isoweekday() > 5:
        # print('+++++++++++++++++++++')
        # print(Dia.index(D))
        if D.N_AM == 'Sin asignar':
            C = heapq.heappop(FinalListWeekEnd)
            # print(C)
            D.N_AM = C[1]
            D.N_PM = C[1]
            D.N_Night = C[1]
            for med in Medicos:
                if D.N_AM == med.nombre:
                    if D.fecha.isoweekday() == 6:
                        med.Conteo_Sabados += 1
                    elif D.fecha.isoweekday() == 7:
                        med.Conteo_Domingos += 1
            InsD += 1
# %%
# ORDENAR LISTA DE Viernes Tarde
TuList = []
for med in Medicos:
    if med.A_FridayPM > 0:
        med.TCount = med.A_FridayPM
        med.Fq = (Count_FridayPM / med.TCount)
        med.Pri = med.Fq / 2
        heapq.heappush(TuList, (med.Pri, med.id, med.TCount, med.Fq))

LongListFridayPM = []
AssignCount = 0
while Count_FridayPM > AssignCount:
    B = heapq.heappop(TuList)
    if B[2] > 0:
        LongListFridayPM.append(Medicos[B[1]].id)
        AssignCount += 1
        if (B[2] - 1) > 0:
            heapq.heappush(TuList, ((B[0] + B[3]), B[1], B[2] - 1, B[3]))
# print ('Secuencia Domingos:')
i = 0
FinalListFridayPM = []
for L in LongListFridayPM:
    heapq.heappush(FinalListFridayPM, (i, Medicos[L].nombre))
    i += 1
    # print(i,L,Medicos[L].nombre)
# %%
# Asignar Viernes Tarde a Calendario
InsD = 0
for D in Dia:
    # print(D.fecha.isoweekday())
    if D.fecha.isoweekday() == 5:
        # print('+++++++++++++++++++++')
        # print(Dia.index(D))
        if D.N_PM == 'Sin asignar':
            C = heapq.heappop(FinalListFridayPM)
            # print(C)
            D.N_PM = C[1]
            InsD += 1
# %%
# ORDENAR LISTA DE Noches
TuList = []
for med in Medicos:
    if med.A_Night > 0:
        med.TCount = med.A_Night
        med.Fq = (Count_Night / med.TCount)
        med.Pri = med.Fq / 2
        heapq.heappush(TuList, (med.Pri, med.id, med.TCount, med.Fq))

LongListNight = []
AssignCount = 0
while Count_Night > AssignCount:
    B = heapq.heappop(TuList)
    if B[2] > 0:
        LongListNight.append(Medicos[B[1]].id)
        AssignCount += 1
        if (B[2] - 1) > 0:
            heapq.heappush(TuList, ((B[0] + B[3]), B[1], B[2] - 1, B[3]))
# print ('Secuencia Domingos:')
i = 0
FinalListNight = []
for L in LongListNight:
    heapq.heappush(FinalListNight, (i, Medicos[L].nombre))
    i += 1
    # print(i,L,Medicos[L].nombre)
# %%
# Asignar Noches a Calendario
InsD = 0
for D in Dia:
    # print(D.fecha.isoweekday())
    if D.fecha.isoweekday() < 6:
        # print('+++++++++++++++++++++')
        # print(Dia.index(D))
        if D.N_Night == 'Sin asignar':
            C = heapq.heappop(FinalListNight)
            # print(C)
            D.N_Night = C[1]
            InsD += 1
# %%
ForPandasCal = []
for D in Dia:
    print(D.fecha, ' es ', D.wDay)
    print('Mañana la hace: ', D.N_AM)
    print('Tarde la hace : ', D.N_PM)
    print('Noche la hace : ', D.N_Night)
    ForPandasCal.append([D.fecha.year, D.fecha.month, D.fecha.day, D.wDay, D.N_AM, D.N_PM, D.N_Night])
    Columnas3 = ['Año', 'Mes', 'Dia', 'Tipo de Dia', 'Mañana', 'Tarde', 'Noche']
    MedDF = pd.DataFrame(ForPandasCal, columns=Columnas3)
    Export3 = MedDF.to_excel('AA - Calendario Abril-Diciembre 2021.xlsx', index=None, header=True)
# %%
ForPandas4 = []
for med in Medicos:
    medListFD = [med.nombre, med.Conteo_Sabados, med.Conteo_Domingos]
    ForPandas4.append(medListFD)
Columnas2 = ['Medico', 'Sabados', 'Domingos']
MedDF4 = pd.DataFrame(ForPandas4, columns=Columnas2)
Export2 = MedDF4.to_excel('AA - Recuento Fines de semana Abril-Diciembre 2021.xlsx', index=None, header=True)
# %%

# %%
for med in Medicos:
    print(med.nombre, ' hace Fines de seman al mes: ', med.A_WeekEnd / meses)
# %%

# %%
CheckT = pd.read_excel('CC Check Turnos.xlsx')
print(CheckT)
# %%
print('why1')
for med in Medicos:
    med.Ch_AM = 0
    med.Ch_PM = 0
    med.Ch_Night = 0
    med.Ch_FridayPM = 0
    med.Ch_WeekEnd = 0
    med.Ch_Carga = 0

Ch_Carga_Total = 0
print('why2')
for ind, row in CheckT.iterrows():
    print(ind)
    dd = datetime.datetime.strptime(str(row['Fecha']), '%Y-%m-%d %H:%M:%S')
    ddd = datetime.date(int(dd.year), int(dd.month), int(dd.day))
    # print(ddd)
    for dia in Dia:
        # print(dia.fecha)
        if ddd == dia.fecha:
            if dia.Feriado != 1:
                print('El dia ', ddd, 'No es feriado o especial')
                if dia.tipodia == "Lunes a Jueves":
                    AMAM = AM
                    PMPM = PM
                    NightNight = Night
                elif dia.tipodia == "Viernes":
                    AMAM = AM
                    PMPM = FridayPM
                    NightNight = Night
                elif dia.tipodia == "Fin de Semana":
                    AMAM = WeekEnd / 3
                    PMPM = WeekEnd / 3
                    NightNight = WeekEnd / 3

                for med in Medicos:
                    if row['Mañana'] == med.nombre:
                        med.Ch_Carga += AMAM
                        Ch_Carga_Total += AMAM

                    if row['Tarde'] == med.nombre:
                        med.Ch_Carga += PMPM
                        Ch_Carga_Total += PMPM
                    if row['Noche'] == med.nombre:
                        med.Ch_Carga += NightNight
                        Ch_Carga_Total += NightNight
                        med.Ch_Night += 1
                print(Ch_Carga_Total)
            else:
                print('El dia ', ddd, 'ES FERIADO O ESPECIAL')

            # print(dia.fecha, 'yeah')
# %%
Ch_A = 0
Ch_T = 0
CheckTab = []
for med in Medicos:
    med.Ch_CargaA = (med.Ch_Carga / Ch_Carga_Total * 100)
    Ch_A += med.Ch_CargaA
    med.Ch_CargaT = (med.CargaMax / CargaMaxima * 100)
    Ch_T += med.Ch_CargaT
    print(med.nombre, ' carga teorica', med.Ch_CargaT, ' y carga asignada', med.Ch_CargaA)
    lista = [med.nombre, med.Ch_CargaA, 'Carga Asignada']
    CheckTab.append(lista)
    lista = [med.nombre, med.Ch_CargaT, 'Carga Teórica']
    CheckTab.append(lista)
    print(med.Ch_Night)
print(Ch_T, Ch_A)

Columnas6 = ['Medico', 'Carga', 'Tipo de Carga']
MedDF9 = pd.DataFrame(CheckTab, columns=Columnas6)
sns.color_palette("coolwarm")
G1 = sns.barplot(x='Carga', y='Medico', data=MedDF9, hue='Tipo de Carga')
# %%
ForPandas8 = []
for med in Medicos:
    medListAlpha = [med.nombre, med.Ch_CargaT, med.Ch_CargaA]
    ForPandas8.append(medListAlpha)
Columnas2 = ['Medico', 'Carga Teorica', 'Carga Asignada']
MedDF6 = pd.DataFrame(ForPandas8, columns=Columnas2)
Export2 = MedDF6.to_excel('AAA - Revision Asignacion Real.xlsx', index=None, header=True)
# %%
