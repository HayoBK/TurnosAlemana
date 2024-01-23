# ---------------------------------------------------------------------------------
# Versión 2024_Febrero para programación de turnos Vacaciones Marzo-Diciembre 2024
# Para nuevos calculos revisar linea 48... meses a evaluar!
# En linea 60 --> añadir lista de Feriados
# En linea 223 --> cambiar fecha en la que se mide la antiguedad de cada médico. he usado la fecha justo
#   en la mitad del periodo que estamos evaluando.

# ---------------------------------------------------------------------------------

# %%
import pandas as pd
import seaborn as sns
# %%
# %%
import heapq
import datetime
from datetime import timedelta

import matplotlib.pyplot as plt

# %%
fecha_inicio = datetime.date(2024, 8, 1)
fecha_final = datetime.date(2025, 1, 11)
meses=4 # meses a evaluar y asignar
Nombre_Periodo = 'Agosto-Diciembre 2024'
diferencia = fecha_final - fecha_inicio
mitad = diferencia / 2
fecha_de_medida = fecha_inicio + mitad


COVID_Val_DS = 1  # Valor dia de semana
COVID_Val_FD = 1.5  # Valor fin de semana y feriado

AM = 1  # Valor una mañana de lunes a viernes
PM = 1.2  # Valor una tarde de lunes a jueves
FridayPM = 1.5  # Valor una tarde de viernes
Night = 2  # Valor una noche de lunes a viernes 1.5
WeekEnd = 6.3  # Valor un sabado o un domingo     5.5.
# Valor WeekEnd es 1.5 veces el valor
# sumado de AM+PM+Night

# --------------- AJUSTES x VACACIONES ----------------------

Night = 8
# --------------- -------------------- ----------------------

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
C_AM = 0                    # C_AM y parecidos es conteo de numeros de días/tramos a asignar
C_PM = 0
C_FridayPM = 0
C_Night = 0
C_WeekEnd = 0
#meses = 9  # meses a evaluar y asignar


class UnDia:
    def __init__(self, SuFecha):
        self.fecha = SuFecha
        self.N_AM = "Sin asignar"
        self.N_PM = "Sin asignar"
        self.N_Night = "Sin asignar"
        self.conflict = " - "
        # Aquí añadir lista de feriados y días especiales.
        F = []
        F.append(datetime.date(2024, 1, 1))
        F.append(datetime.date(2024, 3, 29))
        F.append(datetime.date(2024, 3, 30))
        F.append(datetime.date(2024, 3, 31))
        F.append(datetime.date(2024, 5, 1))
        F.append(datetime.date(2024, 5, 21))
        F.append(datetime.date(2024, 6, 20))
        F.append(datetime.date(2024, 7, 16))
        F.append(datetime.date(2024, 8, 15))
        F.append(datetime.date(2024, 9, 18))
        F.append(datetime.date(2024, 9, 19))
        F.append(datetime.date(2024, 5, 20))
        F.append(datetime.date(2024, 5, 21))
        F.append(datetime.date(2024, 5, 22))
        F.append(datetime.date(2024, 10, 31))
        F.append(datetime.date(2024, 11, 1))
        F.append(datetime.date(2024, 11, 2))
        F.append(datetime.date(2024, 11, 3))
        F.append(datetime.date(2024, 12, 25))
        F.append(datetime.date(2025, 1, 1))















        # ------------------------------------------------

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



# %%
# Fijar fechas de inicio y final de la generación
# de turnoS
#fecha_inicio = datetime.date(2024, 4, 1)
#fecha_final = datetime.date(2025, 1, 1)
delta3 = fecha_final-fecha_inicio
Periodo = delta3.days
rfecha = fecha_inicio
Dia = []
Conteo_Dias_Semana = 0
Conteo_Dias_Fin_de_Semana = 0

# Ciclo inicial para definir calendario basico --> Aqui se crean de verdad los día.
while rfecha <= fecha_final:
    Dia.append(UnDia(rfecha))  # Aqui se genera un dia del calendario
    rfecha = rfecha + timedelta(days=1)

# %%
# Dias_de_Semana = 60
# Dias_de_Fin_de_Semana = 26
# %%
# Esta parte de aqui, tuvo como intención generar una distribución más plana y equilibrada de turnos
# Intentó poner un minimo y un máximo de turnos a cargosear al más joven y al más viejo.
# No resultó tanto.
# Terminé armando un M y un N arbitrarios para intentar hacer lo mismo.


delta = 12  # año de referencia
CZERO_AM = 3
CZERO_PM = 1
CZERO_Night = 6
CZERO_FridayPM = 3
CZERO_WeekEnd = 1.5

CargaZERO = CZERO_AM * AM + CZERO_PM * PM + CZERO_FridayPM * FridayPM + CZERO_Night * Night + CZERO_WeekEnd * WeekEnd

C12_AM = 9
C12_PM = 1
C12_Night = 6
C12_FridayPM = 0
C12_WeekEnd = 1

Carga12 = C12_AM * AM + C12_PM * PM + C12_FridayPM * FridayPM + C12_Night * Night + C12_WeekEnd * WeekEnd

m = (Carga12 - CargaZERO) / delta
n = delta - m * Carga12
m = -0.25  # ESTE VALOR "APLANA la curva de distribución" ... estos fueron los M y N arbitrarios que luego de mucho
          # ensayo y error logré definir.

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
        self.Conteo_Vacaciones = 0

        self.Conteo_Sabados = 0
        self.Conteo_Domingos = 0

        self.id = int(id)
        self.nombre = nombre
        self.ingreso = datetime.date(año, mes, dia)
        self.Cat = Cat
        self.Medida = datetime.date(2024, 8, 1)  # Aqui se fija el dia en el que se mide antiguedad
        self.Medida = fecha_de_medida
        Dif = self.Medida - self.ingreso
        self.Antiq = Dif.days / 365
        self.CargaAntiq2021 = self.Antiq * m + n  # -self.Antiq*0.0075+0.1212
        if self.Cat == 'AUSENTE':
            self.CargaAntiq2021 = 0
        global CheckCargaAntiq2021
        CheckCargaAntiq2021 += self.CargaAntiq2021

        self.CargaReal = 0

        self.AntiqNz = (self.Antiq / 12) - 0.5
        self.LoadScore = 1 - self.AntiqNz + 0.5   # Carga del Médico
        global total_LoadScore          # Total de Carga de todos los médicos sumados
        total_LoadScore += self.LoadScore
        global total_FindeSemanaScore
        if self.Cat != 'Yoda-Sin Noches':
            total_FindeSemanaScore += self.LoadScore

        self.Vacaciones=[]
    def Vacas(self,V1a,V1m,V1d,V2a,V2m,V2d):
        V1=datetime.date(V1a,V1m,V1d)
        V2=datetime.date(V2a,V2m,V2d) + timedelta(days=1)
        delta1 = V2-V1
        self.Conteo_Vacaciones+=delta1.days
        while V1 != V2:
            self.Vacaciones.append(V1)
            V1=V1 + timedelta(days=1)

Medicos = []

# Por si acaso las categorias son:
#'Yoda-Sin Noches'
#'Master-Mañanas'
#'Knight-Tardes'
#'Padawan-Sin Fijo'
#'AUSENTE'

Medicos.append(Medico(0, 'Gomez', 2013, 7, 1, 'Yoda-Sin Noches'))
Medicos[0].Vacas(2024,1,20,2024,2,20)
Medicos.append(Medico(1, 'Bravo', 2013, 7, 1, 'Yoda-Sin Noches'))
Medicos[1].Vacas(2024,3,1,2024,3,31)
Medicos.append(Medico(2, 'Iñiguez', 2014, 1, 1, 'Yoda-Sin Noches'))
Medicos[2].Vacas(2024,1,3,2024,1,28)
Medicos.append(Medico(3, 'Breinbauer', 2014, 1, 1, 'Yoda-Sin Noches'))
Medicos[3].Vacas(2024,1,1,2024,1,7)
Medicos[3].Vacas(2024,2,5,2024,2,25)
Medicos.append(Medico(4, 'Arredondo', 2014, 8, 1, 'Yoda-Sin Noches'))
Medicos[4].Vacas(2024,2,1,2024,2,29) # 5 de marzo
Medicos.append(Medico(5, 'Carrasco', 2014, 8, 1, 'Yoda-Sin Noches'))
Medicos[5].Vacas(2024,1,3,2024,1,28)
Medicos.append(Medico(6, 'Culaciati', 2014, 8, 1, 'Yoda-Sin Noches'))
Medicos[6].Vacas(2024,1,29,2024,2,26)
Medicos.append(Medico(7, 'Contreras', 2017, 1, 1, 'Knight-Tardes'))
Medicos[7].Vacas(2024,2,1,2024,2,29) # 31 de marzo
Medicos.append(Medico(8, 'Cisternas', 2017, 11, 1, 'Knight-Tardes'))
Medicos[8].Vacas(2024,1,15,2024,1,28)
Medicos.append(Medico(9, 'Pio', 2018, 1, 13, 'Padawan-Sin Fijo'))
Medicos[9].Vacas(2024,1,20,2024,2,19)
Medicos.append(Medico(10, 'Alvo', 2019, 11, 1, 'Padawan-Sin Fijo'))
Medicos[10].Vacas(2024,2,19,2024,3,17)
#Medicos.append(Medico(12, 'Ramos',2021,9,1,'AUSENTE'))
#Medicos[12].Vacas(2024,1,14,2025,1,1)
Medicos.append(Medico(11, 'Boettiger',2021,9,1,'Padawan-Sin Fijo'))
Medicos[11].Vacas(2024,1,27,2024,2,24)
Medicos.append(Medico(12, 'Loch',2022,6,1,'Padawan-Sin Fijo'))
Medicos[12].Vacas(2024,1,8,2024,2,4)
Medicos.append(Medico(13, 'Rubio',2022,6,1,'Padawan-Sin Fijo'))
Medicos[13].Vacas(2024,1,15,2024,1,28)
Medicos.append(Medico(14, 'Recluta1',2024,4,1,'Padawan-Sin Fijo'))
Medicos[14].Vacas(2024,4,1,2024,4,15)

Max_Medicos_id = 14
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
Ch2 =0
for med in Medicos:
    med.MagicNumber = med.CargaMax/Check
    Ch2 += med.MagicNumber
    print (med.nombre, med.MagicNumber, Ch2)
print('Los siguientes numeros deben ser iguales =', CargaMaxima, ' y ', Check, ' - ',Ch2)
# %%
for dia in Dia:
    NombreAM = 'Sin asignar'
    NombrePM = 'Sin asignar'
    dia.N_AM = NombreAM
    dia.N_PM = NombrePM
    # print(dia.fecha,' es un ',dia.tipodia)
    if dia.Feriado == 0:
        if dia.fecha.isoweekday() == 1:
            NombreAM = 'Gomez'
            NombrePM = 'Cisternas'
            dia.wDay = 'Lunes'
        elif dia.fecha.isoweekday() == 2:
            NombreAM = 'Iñiguez'
            NombrePM = 'Contreras'
            dia.wDay = 'Martes'
        elif dia.fecha.isoweekday() == 3:
            NombreAM = 'Arredondo'
            NombrePM = 'Carrasco'
            dia.wDay = 'Miércoles'
        elif dia.fecha.isoweekday() == 4:
            NombreAM = 'Bravo'
            NombrePM = 'Culaciati'
            dia.wDay = 'Jueves'
        elif dia.fecha.isoweekday() == 5:
            NombreAM = 'Breinbauer'
            dia.wDay = 'Viernes'
        elif dia.fecha.isoweekday() == 6:
            dia.wDay = 'Sábado'
        elif dia.fecha.isoweekday() == 7:
            dia.wDay = 'Domingo'
        #Ajustes extraños por cambios significativos en mitad de periodo
        Limite1 = datetime.date(2024,2,1)
        Limite2 = datetime.date(2024,3,1)
        if dia.fecha < Limite2:
            if dia.fecha.isoweekday() == 1:
                NombreAM = 'Gomez'
                NombrePM = 'Carrasco'
                dia.wDay = 'Lunes'
            elif dia.fecha.isoweekday() == 2:
                NombreAM = 'Iñiguez'
                NombrePM = 'Contreras'
                dia.wDay = 'Martes'
            elif dia.fecha.isoweekday() == 3:
                NombreAM = 'Arredondo'
                NombrePM = 'Cisternas'
                dia.wDay = 'Miércoles'
            elif dia.fecha.isoweekday() == 4:
                NombreAM = 'Bravo'
                NombrePM = 'Culaciati'
                dia.wDay = 'Jueves'
            elif dia.fecha.isoweekday() == 5:
                NombreAM = 'Breinbauer'
                dia.wDay = 'Viernes'
            elif dia.fecha.isoweekday() == 6:
                dia.wDay = 'Sábado'
            elif dia.fecha.isoweekday() == 7:
                dia.wDay = 'Domingo'

        if dia.fecha < Limite1:
            if dia.fecha.isoweekday() == 1:
                NombreAM = 'Gomez'
                NombrePM = 'Carrasco'
                dia.wDay = 'Lunes'
            elif dia.fecha.isoweekday() == 2:
                NombreAM = 'Iñiguez'
                NombrePM = 'Contreras'
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
                NombreAM = 'Breinbauer'
                dia.wDay = 'Viernes'
            elif dia.fecha.isoweekday() == 6:
                dia.wDay = 'Sábado'
            elif dia.fecha.isoweekday() == 7:
                dia.wDay = 'Domingo'


        if dia.fecha.isoweekday() < 6:
            for med in Medicos:
                if (med.nombre == NombreAM) and (dia.fecha not in med.Vacaciones):
                    C_AM -= 1   # Quito uno de los bloques a asignar
                    med.CargaReal += AM   # añado carga real asignada
                    dia.N_AM = NombreAM
                    #med.A_AM += 1  # Aumento en uno el numero de mañanas asignados.
                if med.nombre == NombrePM and (dia.fecha not in med.Vacaciones):
                    C_PM -= 1
                    med.CargaReal += PM
                    dia.N_PM = NombrePM
                    #med.A_PM += 1

    print('El dia ', dia.fecha.isoweekday(), dia.fecha,' lo hace ', dia.N_AM, ' mañana y ', dia.N_PM,' tarde')

# %%
print('AM:', C_AM)  # aqui vendrían los que faltan por asignar aún.
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
# ---------------------------------------------------
# Asignar Numero Mañanas pendientes por vacaciones
# update Carga
CargaRestanteTotal = 0
MagicCarga=0
for med in Medicos:
    if med.Cat == 'Padawan-Sin Fijo':
        MagicCarga+=med.MagicNumber
        med.CargaRestante = med.CargaMax - med.CargaReal
        CargaRestanteTotal += med.CargaRestante
        print('A ', med.nombre, ' queda por asignarle: ', med.CargaRestante)
for med in Medicos:
    if med.Cat == 'Padawan-Sin Fijo':
        med.Factor=med.MagicNumber/MagicCarga

print()

Check = C_AM
for med in reversed(Medicos):
    if med.Cat == 'Padawan-Sin Fijo':

    #med.Factor = med.CargaRestante / CargaRestanteTotal
        med.A_AM = round(C_AM * med.Factor)
        Check -= med.A_AM
        print('A ', med.nombre, ' le corresponde proporcionalmente asignar: ', med.Factor)
        print('Lo que equivale a los siguientes turnos: ', med.A_AM)

print()
print('Turnos de Mañanas Lu-Vi sin asingar -error - : ', Check)

#C_AM = Check
while Check != 0:
    for med in reversed(Medicos):
        if med.Cat == 'Padawan-Sin Fijo':

            if Check > 0:
                med.A_AM += 1
                Check -= 1
            if Check < 0:
                med.A_AM -= 1
                Check += 1

print('Turno de Mañanas Lu-Vi sin asingar -error - : ', Check)
#C_AM = Check

# ---------------------------------------------------

# Asignar Numero Tardes Lu-Ju pendientes por vacaciones
# update Carga
CargaRestanteTotal = 0
for med in reversed(Medicos):
    med.CargaRestante = med.CargaMax - med.CargaReal
    CargaRestanteTotal += med.CargaRestante
    print('A ', med.nombre, ' queda por asignarle: ', med.CargaRestante)

print()

Check = C_PM
for med in reversed(Medicos):
    if med.Cat == 'Padawan-Sin Fijo':

    #med.Factor = med.CargaRestante / CargaRestanteTotal
        med.A_PM = round(C_PM * med.Factor)
        Check -= med.A_PM
        print('A ', med.nombre, ' le corresponde proporcionalmente asignar: ', med.Factor)
        print('Lo que equivale a los siguientes turnos: ', med.A_PM)

print()
print('Turnos de Mañanas Lu-Vi sin asingar -error - : ', Check)

#C_PM = Check
while Check != 0:
    for med in reversed(Medicos):
        if med.Cat == 'Padawan-Sin Fijo':

            if Check > 0:
                med.A_PM += 1
                Check -= 1
            if Check < 0:
                med.A_PM -= 1
                Check += 1

print('Turno de Tardes Lu-Vi sin asingar -error - : ', Check)
#C_PM = Check

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
        if med.Cat == 'Padawan-Sin Fijo':
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
        med.A_Night = round(C_Night * med.MagicNumber) #ERa MEd.Factor
        Check -= med.A_Night
        print('A ', med.nombre, ' le corresponde proporcionalmente asignar: ', med.Factor)
        print('Lo que equivale a los siguientes turnos: ', med.A_Night)

print()
print('Turno de Noche sin asingar -error - : ', Check)
C_Night = Check

while Check != 0:
    for med in reversed(Medicos):
        if (med.Cat != 'Yoda-Sin Noches'):
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
#    Export2 = MedDF.to_excel('AA - Medicos Abril-Diciembre 2021.xlsx', index=None, header=True)
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
#plt.scatter(Antiguedad, Carga)
#plt.xlabel('Antiguedad')
#plt.ylabel('Carga')
#plt.show()

# %%
#plt.scatter(Antiguedad, CargaT)
#plt.xlabel('Antiguedad')
#plt.ylabel('Carga Teorica')
#plt.show()

# %%
# ------------------------------------------------------------------------------------
#       ASIGNAR TURNOS A CALENDARIO
# ------------------------------------------------------------------------------------
Conflictos=[]

Cachisimos=[] # Lista de pucha... personajes a canular en caso de conflicto que no se pueda resolver...
j=0
for f in range(10):
    for med in reversed(Medicos):
        if med.Cat == 'Padawan-Sin Fijo':
            j+=1
            heapq.heappush(Cachisimos, (j,med.nombre))

## ORDENAR LISTA DE MAÑANAS PENDIENTES
TuList = []
for med in Medicos:
    if med.A_AM > 0:
        med.TCount = med.A_AM # --> Cantidad de Turnos a distribuir
        med.Fq = (C_AM / med.TCount) # --> Frecuencia
        med.Pri = med.Fq / 2        # ---> Prioridad? claro, creo que es el orden...
        heapq.heappush(TuList, (med.Pri, med.id, med.TCount, med.Fq))

LongListAM = []
AssignCount = 0
while C_AM > AssignCount:
    B = heapq.heappop(TuList)
    if B[2] > 0:
        LongListAM.append(Medicos[B[1]].id)
        AssignCount += 1
        if (B[2] - 1) > 0:
            heapq.heappush(TuList, ((B[0] + B[3]), B[1], B[2] - 1, B[3]))
i = 0
FinalListAM = []
for L in LongListAM:
    heapq.heappush(FinalListAM, (i, Medicos[L].nombre))  #--> Lista donde estan todos bien distribuiditos
    i += 1 # i, determina el lugar en la lista
    # print(i,L,Medicos[L].nombre)
# %%
# Asignar Mañanas a Calendario
InsD = 0
for D in Dia:
    # print(D.fecha.isoweekday())
    if (D.fecha.isoweekday() < 6) and (D.Feriado != 1):
        # print('+++++++++++++++++++++')
        # print(Dia.index(D))
        if D.N_AM == 'Sin asignar':
            Tolerancia=2*len(FinalListAM)
            Intentos=0
            while True:
                C = heapq.heappop(FinalListAM)
                Listo = True
                for med in Medicos:
                    if C[1] == med.nombre:
                        if (D.fecha in med.Vacaciones):
                            i+=1
                            heapq.heappush(FinalListAM, (i, med.nombre)) # volvemos a meter al sujeto a la lista
                            Listo = False
                            Intentos +=1
                if Intentos > Tolerancia:
                    Listo = True
                    Conflictos.append([D.fecha,C[1],'Conflicto de Vacaciones a revisar'])
                    D.conflict += C[1] + ' con conflicto vacaciones -'
                if Listo == True:
                    break
            # print(C)
            D.N_AM = C[1]
            InsD += 1

## ORDENAR LISTA DE TARDES PENDIENTES
TuList = []
for med in Medicos:
    if med.A_PM > 0:


        med.TCount = med.A_PM # --> Cantidad de Turnos a distribuir
        med.Fq = (C_PM / med.TCount) # --> Frecuencia
        med.Pri = med.Fq / 2        # ---> Prioridad? claro, creo que es el orden...
        heapq.heappush(TuList, (med.Pri, med.id, med.TCount, med.Fq))

LongListPM = []
AssignCount = 0
while C_PM > AssignCount:
    B = heapq.heappop(TuList)
    if B[2] > 0:
        LongListPM.append(Medicos[B[1]].id)
        AssignCount += 1
        if (B[2] - 1) > 0:
            heapq.heappush(TuList, ((B[0] + B[3]), B[1], B[2] - 1, B[3]))
# print ('Secuencia Domingos:')
i = 0
FinalListPM = []
for L in LongListPM:
    heapq.heappush(FinalListPM, (i, Medicos[L].nombre))  #--> Lista donde estan todos bien distribuiditos
    i += 1 # i, determina el lugar en la lista
    # print(i,L,Medicos[L].nombre)
# %%
# Asignar Fines de Semana a Calendario
InsD = 0
for D in Dia:
    # print(D.fecha.isoweekday())
    if (D.fecha.isoweekday() < 5) and (D.Feriado != 1):
        # print('+++++++++++++++++++++')
        # print(Dia.index(D))
        if D.N_PM == 'Sin asignar':
            Tolerancia=2*len(FinalListPM)
            Intentos=0
            while True:
                C = heapq.heappop(FinalListPM)
                Listo = True
                for med in Medicos:
                    if C[1] == med.nombre:
                        if (D.fecha in med.Vacaciones):
                            i+=1
                            heapq.heappush(FinalListPM, (i, med.nombre)) # volvemos a meter al sujeto a la lista
                            Listo = False
                            Intentos +=1
                if Intentos > Tolerancia:
                    Listo = True
                    Conflictos.append([D.fecha,C[1],'Conflicto de Vacaciones a revisar'])
                    D.conflict += C[1] + ' con conflicto vacaciones '

                if Listo == True:
                    break
            # print(C)
            D.N_PM = C[1]
            InsD += 1
# ---------------------------------------------
# ORDENAR LISTA DE FINES DE SEMANA
TuList = []
for med in Medicos:
    if med.A_WeekEnd > 0:
        med.TCount = med.A_WeekEnd # --> Cantidad de Turnos a distribuir
        med.Fq = (Count_WeekEnd / med.TCount) # --> Frecuencia
        med.Pri = med.Fq / 2        # ---> Prioridad? claro, creo que es el orden...
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
    heapq.heappush(FinalListWeekEnd, (i, Medicos[L].nombre))  #--> Lista donde estan todos bien distribuiditos
    i += 1 # i, determina el lugar en la lista
    # print(i,L,Medicos[L].nombre)
# %%




# Asignar Fines de Semana a Calendario
InsD = 0
for D in Dia:
    # print(D.fecha.isoweekday())
    if (D.fecha.isoweekday() > 5) and (D.Feriado != 1):
        # print('+++++++++++++++++++++')
        # print(Dia.index(D))
        if D.N_AM == 'Sin asignar':
            Tolerancia=2*len(FinalListWeekEnd)
            Intentos=0
            while True:
                if len(FinalListWeekEnd)>0:
                    C = heapq.heappop(FinalListWeekEnd)
                else:
                    C = heapq.heappop(Cachisimos)
                Listo = True
                for med in Medicos:
                    if C[1] == med.nombre:
                        if (D.fecha in med.Vacaciones):
                            i+=1
                            heapq.heappush(FinalListWeekEnd, (i, med.nombre)) # volvemos a meter al sujeto a la lista
                            Listo = False
                            Intentos +=1
                if Intentos > Tolerancia:
                    Listo = True
                    Conflictos.append([D.fecha,C[1],'Conflicto de Vacaciones a revisar'])
                    D.conflict += C[1] + ' con conflicto vacaciones '

                if Listo == True:
                    break
            # print(C)
            D.N_AM = C[1]
            D.N_PM = C[1]
            D.N_Night = C[1]
            for med in Medicos:  # Sacar las noches de los Yoda-Sin noches... manso jaleo...
                if D.N_Night == med.nombre:
                    if med.Cat == 'Yoda-Sin Noches':
                        while True:
                            h=False
                            Cacho = heapq.heappop(Cachisimos)
                            for med2 in Medicos:
                                if med2.nombre == Cacho[1]:
                                    if D.fecha in med2.Vacaciones:
                                        h=True
                            if h==False:
                                D.N_Night = Cacho[1]
                                break
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
    if (D.fecha.isoweekday() == 5) and (D.Feriado != 1):
        # print('+++++++++++++++++++++')
        # print(Dia.index(D))
        if D.N_PM == 'Sin asignar':

            Tolerancia = 2 * len(FinalListFridayPM)
            Intentos = 0
            while True:
                C = heapq.heappop(FinalListFridayPM)
                Listo = True
                for med in Medicos:
                    if C[1] == med.nombre:
                        if (D.fecha in med.Vacaciones):
                            i += 1
                            heapq.heappush(FinalListFridayPM, (i, med.nombre))  # volvemos a meter al sujeto a la lista
                            Listo = False
                            Intentos += 1
                if Intentos > Tolerancia:
                    Listo = True
                    Conflictos.append([D.fecha, C[1], 'Conflicto de Vacaciones a revisar'])
                    D.conflict += C[1] + ' con conflicto vacaciones '

                if Listo == True:
                    break
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
    if (D.fecha.isoweekday() < 6) and (D.Feriado != 1):
        # print('+++++++++++++++++++++')
        # print(Dia.index(D))
        if D.N_Night == 'Sin asignar':
            Tolerancia = 2 * len(FinalListNight)
            Intentos = 0
            while True:
                C = heapq.heappop(FinalListNight)
                Listo = True
                for med in Medicos:
                    if C[1] == med.nombre:
                        if (D.fecha in med.Vacaciones):
                            i += 1
                            heapq.heappush(FinalListNight, (i, med.nombre))  # volvemos a meter al sujeto a la lista
                            Listo = False
                            Intentos += 1
                if Intentos > Tolerancia:
                    Listo = True
                    Conflictos.append([D.fecha, C[1], 'Conflicto de Vacaciones a revisar'])
                    D.conflict += C[1] + ' con conflicto vacaciones '

                if Listo == True:
                    break
            # print(C)
            D.N_Night = C[1]
            InsD += 1
# %%
#  ++++++++++++++++++++++++++++++++++++++++++++++++++

# AQUI SE IMPRIMEN LOS TURNO

#  ++++++++++++++++++++++++++++++++++++++++++++++++++
ForPandasCal = []
for D in Dia:
    print(D.fecha, ' es ', D.wDay)
    print('Mañana la hace: ', D.N_AM)
    print('Tarde la hace : ', D.N_PM)
    print('Noche la hace : ', D.N_Night)
    deVacaciones = ' '
    for med in Medicos:
        if D.fecha in med.Vacaciones:
            deVacaciones+= ' - ' + med.nombre
    ForPandasCal.append([D.fecha.year, D.fecha.month, D.fecha.day, D.wDay, D.N_AM, D.N_PM, D.N_Night,D.conflict,deVacaciones])
    Columnas3 = ['Año', 'Mes', 'Dia', 'Tipo de Dia', 'Mañana', 'Tarde', 'Noche','Conflictos a Revisar','De Vacaciones']
    MedDF = pd.DataFrame(ForPandasCal, columns=Columnas3)
    nombrecito = 'AA - Calendario de Turnos(version ' + Nombre_Periodo + ').xlsx'
    Export3 = MedDF.to_excel(nombrecito, index=None, header=True)
    #           I
    #           I   Bloquea la proxima linea para bloquear la revisión Manual.
    #           V
    #MedDF = pd.read_excel('Vacaciones 2024 Manual.xlsx')
    for med in Medicos:
        med.Ch_AM = 0
        med.Ch_PM = 0
        med.Ch_Night = 0
        med.Ch_FridayPM = 0
        med.Ch_WeekEnd = 0
        med.Ch_Carga = 0
        med.Ch_Sab = 0
        med.Ch_Dom = 0
    Ch_Carga_Total = 0
    for ind, row in MedDF.iterrows():
        print(ind)
        #dd = datetime.datetime.strptime(str(row['Fecha']), '%Y-%m-%d %H:%M:%S')
        ddd = datetime.date(int(row['Año']), int(row['Mes']), int(row['Dia']))
        # print(ddd)
        for dia in Dia:
            # print(dia.fecha)
            if ddd == dia.fecha:
                if dia.Feriado != 1:
                    for med in Medicos:
                        if dia.fecha.isoweekday() == 6:
                            if row['Mañana'] == med.nombre:
                                med.Ch_Sab += 1
                        if dia.fecha.isoweekday() == 7:
                            if row['Mañana'] == med.nombre:
                                med.Ch_Dom += 1

                    print('El dia ', ddd, 'No es feriado o especial')
                    if dia.fecha.isoweekday() < 5:
                        for med in Medicos:
                            if row['Mañana'] == med.nombre:
                                med.Ch_AM += 1
                            if row['Tarde'] == med.nombre:
                                med.Ch_PM += 1
                            if row['Noche'] == med.nombre:
                                med.Ch_Night += 1
                        AMAM = AM
                        PMPM = PM
                        NightNight = Night
                    elif dia.fecha.isoweekday() == 5:
                        for med in Medicos:
                            if row['Mañana'] == med.nombre:
                                med.Ch_AM += 1
                            if row['Tarde'] == med.nombre:
                                med.Ch_FridayPM += 1
                            if row['Noche'] == med.nombre:
                                med.Ch_Night += 1
                        AMAM = AM
                        PMPM = FridayPM
                        NightNight = Night
                    elif dia.fecha.isoweekday() > 5:
                        for med in Medicos:
                            if row['Mañana'] == med.nombre:
                                med.Ch_WeekEnd += (1 / 3)
                            if row['Tarde'] == med.nombre:
                                med.Ch_WeekEnd += (1 / 3)
                            if row['Noche'] == med.nombre:
                                med.Ch_WeekEnd += (1 / 3)
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
                    print(Ch_Carga_Total)
                else:
                    print('El dia ', ddd, 'ES FERIADO O ESPECIAL')

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

for med in Medicos:
    med.periodo = (Periodo - med.Conteo_Vacaciones)/ 30.4

ForPandas8 = []
for med in Medicos:
    medListAlpha = [med.nombre, med.ingreso,med.Antiq, med.Cat,med.Conteo_Vacaciones, med.Ch_CargaT, med.Ch_CargaA, med.Ch_AM, med.Ch_PM, med.Ch_FridayPM,med.Ch_Night,
                    med.Ch_WeekEnd,med.Ch_Sab,med.Ch_Dom,med.Ch_AM/med.periodo,
                    med.Ch_PM/med.periodo,
                    med.Ch_FridayPM/med.periodo,med.Ch_Night/med.periodo,med.Ch_WeekEnd/med.periodo]
    ForPandas8.append(medListAlpha)
Columnas2 = ['Medico', 'Fecha Ingreso a SUCA', 'Antiguedad', 'Categoria', 'Dias de vacaciones', 'Carga Teorica', 'Carga Asignada', 'Mañanas','Tardes','Viernes Tarde','Noches',
             'Fines de Semana','Sábados','Domingos','Mañanas/mes','Tardes/mes',
             'ViernesTarde/mes','Noches/mes','FindeSemana/mes']
MedDF6 = pd.DataFrame(ForPandas8, columns=Columnas2)
nombrecito = 'AAA - Revision Asignacion de Salida (version ' + Nombre_Periodo +').xlsx'
Export2 = MedDF6.to_excel(nombrecito, index=None, header=True)

# %%
ForPandasCal = []
for D in Dia:
    print(D.fecha, ' es ', D.wDay)
    print('Mañana la hace: ', D.N_AM)
    print('Tarde la hace : ', D.N_PM)
    print('Noche la hace : ', D.N_Night)
    deVacaciones = ' '
    for med in Medicos:
        if D.fecha in med.Vacaciones:
            deVacaciones+= ' - ' + med.nombre
    ForPandasCal.append([D.fecha.year, D.fecha.month, D.fecha.day, D.wDay, D.N_AM, D.N_PM, D.N_Night,D.conflict,deVacaciones])
    Columnas3 = ['Año', 'Mes', 'Dia', 'Tipo de Dia', 'Mañana', 'Tarde', 'Noche','Conflictos a Revisar','De Vacaciones']
    MedDF = pd.DataFrame(ForPandasCal, columns=Columnas3)
    nombrecito = 'AA - Calendario de Turnos(version '+ Nombre_Periodo +').xlsx'
    Export3 = MedDF.to_excel(nombrecito, index=None, header=True)
    #           I
    #           I   Bloquea la proxima linea para bloquear la revisión Manual.
    #           V
    MedDF = pd.read_excel('AAA - Calendario con ajuste Manual.xlsx')
    for med in Medicos:
        med.Ch_AM = 0
        med.Ch_PM = 0
        med.Ch_Night = 0
        med.Ch_FridayPM = 0
        med.Ch_WeekEnd = 0
        med.Ch_Carga = 0
        med.Ch_Sab = 0
        med.Ch_Dom = 0
    Ch_Carga_Total = 0
    for ind, row in MedDF.iterrows():
        print(ind)
        #dd = datetime.datetime.strptime(str(row['Fecha']), '%Y-%m-%d %H:%M:%S')
        ddd = datetime.date(int(row['Año']), int(row['Mes']), int(row['Dia']))
        # print(ddd)
        for dia in Dia:
            # print(dia.fecha)
            if ddd == dia.fecha:
                if dia.Feriado != 1:
                    for med in Medicos:
                        if dia.fecha.isoweekday() == 6:
                            if row['Mañana'] == med.nombre:
                                med.Ch_Sab += 1
                        if dia.fecha.isoweekday() == 7:
                            if row['Mañana'] == med.nombre:
                                med.Ch_Dom += 1

                    print('El dia ', ddd, 'No es feriado o especial')
                    if dia.fecha.isoweekday() < 5:
                        for med in Medicos:
                            if row['Mañana'] == med.nombre:
                                med.Ch_AM += 1
                            if row['Tarde'] == med.nombre:
                                med.Ch_PM += 1
                            if row['Noche'] == med.nombre:
                                med.Ch_Night += 1
                        AMAM = AM
                        PMPM = PM
                        NightNight = Night
                    elif dia.fecha.isoweekday() == 5:
                        for med in Medicos:
                            if row['Mañana'] == med.nombre:
                                med.Ch_AM += 1
                            if row['Tarde'] == med.nombre:
                                med.Ch_FridayPM += 1
                            if row['Noche'] == med.nombre:
                                med.Ch_Night += 1
                        AMAM = AM
                        PMPM = FridayPM
                        NightNight = Night
                    elif dia.fecha.isoweekday() > 5:
                        for med in Medicos:
                            if row['Mañana'] == med.nombre:
                                med.Ch_WeekEnd += (1 / 3)
                            if row['Tarde'] == med.nombre:
                                med.Ch_WeekEnd += (1 / 3)
                            if row['Noche'] == med.nombre:
                                med.Ch_WeekEnd += (1 / 3)
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
                    print(Ch_Carga_Total)
                else:
                    print('El dia ', ddd, 'ES FERIADO O ESPECIAL')

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

for med in Medicos:
    med.periodo = (Periodo - med.Conteo_Vacaciones)/ 30.4

ForPandas8 = []
for med in Medicos:
    medListAlpha = [med.nombre, med.ingreso,med.Antiq, med.Cat,med.Conteo_Vacaciones, med.Ch_CargaT, med.Ch_CargaA, med.Ch_AM, med.Ch_PM, med.Ch_FridayPM,med.Ch_Night,
                    med.Ch_WeekEnd,med.Ch_Sab,med.Ch_Dom,med.Ch_AM/med.periodo,
                    med.Ch_PM/med.periodo,
                    med.Ch_FridayPM/med.periodo,med.Ch_Night/med.periodo,med.Ch_WeekEnd/med.periodo]
    ForPandas8.append(medListAlpha)
Columnas2 = ['Medico', 'Fecha Ingreso a SUCA', 'Antiguedad', 'Categoria', 'Dias de vacaciones', 'Carga Teorica', 'Carga Asignada', 'Mañanas','Tardes','Viernes Tarde','Noches',
             'Fines de Semana','Sábados','Domingos','Mañanas/mes','Tardes/mes',
             'ViernesTarde/mes','Noches/mes','FindeSemana/mes']
MedDF6 = pd.DataFrame(ForPandas8, columns=Columnas2)
Export2 = MedDF6.to_excel('AAA - Revision Asignacion con ajuste Manual.xlsx', index=None, header=True)

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
    med.Ch_Sab = 0
    med.Ch_Dom = 0
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
                if dia.fecha.isoweekday() == 6:
                    med.Ch_Sab+=1
                if dia.fecha.isoweekday() == 7:
                    med.Ch_Dom+=1

                print('El dia ', ddd, 'No es feriado o especial')
                if dia.fecha.isoweekday()<5:
                    for med in Medicos:
                        if row['Mañana'] == med.nombre:
                            med.Ch_AM += 1
                        if row['Tarde'] == med.nombre:
                            med.Ch_PM += 1
                        if row['Noche'] == med.nombre:
                            med.Ch_Night += 1
                    AMAM = AM
                    PMPM = PM
                    NightNight = Night
                elif dia.fecha.isoweekday() == 5:
                    for med in Medicos:
                        if row['Mañana'] == med.nombre:
                            med.Ch_AM += 1
                        if row['Tarde'] == med.nombre:
                            med.Ch_FridayPM += 1
                        if row['Noche'] == med.nombre:
                            med.Ch_Night += 1
                    AMAM = AM
                    PMPM = FridayPM
                    NightNight = Night
                elif dia.fecha.isoweekday() > 5:
                    for med in Medicos:
                        if row['Mañana'] == med.nombre:
                            med.Ch_WeekEnd += (1/3)
                        if row['Tarde'] == med.nombre:
                            med.Ch_WeekEnd += (1/3)
                        if row['Noche'] == med.nombre:
                            med.Ch_WeekEnd += (1/3)
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
#sns.color_palette("coolwarm")
#G1 = sns.barplot(x='Carga', y='Medico', data=MedDF9, hue='Tipo de Carga')
# %%
ForPandas8 = []
for med in Medicos:
    medListAlpha = [med.nombre, med.ingreso,med.Antiq, med.Cat,med.Conteo_Vacaciones,med.Ch_CargaT, med.Ch_CargaA, med.Ch_AM, med.Ch_PM, med.Ch_FridayPM,med.Ch_Night,
                    med.Ch_WeekEnd,
                    med.Ch_Sab,med.Ch_Dom,
                    med.Ch_AM/meses,
                    med.Ch_PM/meses,
                    med.Ch_FridayPM/meses,med.Ch_Night/meses,med.Ch_WeekEnd/meses]
    ForPandas8.append(medListAlpha)
Columnas2 = ['Medico', 'Fecha Ingreso a SUCA', 'Antiguedad', 'Categoria', 'Dias de vacaciones', 'Carga Teorica', 'Carga Asignada', 'Mañanas','Tardes','Viernes Tarde','Noches','Fines de Semana','Sábados','Domingos',
             'Mañanas/mes',
             'Tardes/mes',
             'ViernesTarde/mes','Noches/mes','FindeSemana/mes']
MedDF6 = pd.DataFrame(ForPandas8, columns=Columnas2)
Export2 = MedDF6.to_excel('Revision de Check Turnos.xlsx', index=None, header=True)
# %%
print('Conflictos:')
for con in Conflictos:
    print(con)
print('Listo')
