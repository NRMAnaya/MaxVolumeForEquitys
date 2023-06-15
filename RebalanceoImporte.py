import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os
import sys

from datetime import datetime



ISIN=(sys.argv[1])
numeroFile=(sys.argv[2])
fecha=(sys.argv[3])
SegundosEntrada=(sys.argv[4])
Segundos=float(SegundosEntrada)
print("Este es el numero de emisora", ISIN)
print("Este es el numero de emisora", numeroFile)
print("Este es el numero de emisora", fecha)
print("Estos son los segundos entre la suma de hechos (ejemp 60 =1min;300=5min)", Segundos)

workbook_inicial='/home/ops/ReportesOperaciones/HechosBIVA/hechosemisora'+ISIN+numeroFile+'.txt'




#############################################################################
################funcion que cambia horas minutos y segundos a solo segundos
#############################################################################

def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

"""
def get_sec(time_str):
    try:
        int(time_str)
        h, m, s = time_str.split(':')
        return int(h) * 3600 + int(m) * 60 + int(s)
    except:
        return int(50500)
"""
###############################################################################
############# EN ESTA FUNCION TRANSFORMAMOS LOS SEGUNDOS A HORA NORMAL en las dos columnas del data frame que vamos a graficar
###############################################################################

###funcion para pasar a segundos
def segundos_a_segundos_minutos_y_horas(segundos):
    horas = int(segundos / 60 / 60)
    segundos -= horas*60*60
    minutos = int(segundos/60)
    segundos -= minutos*60
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"



#############################################################################
################cambiamos el df a solo segundos para manejarlo desde ahi y lo ordenamos si quieres ver como esta, solo imprimelo print(df_2)
#############################################################################
df_inicial=pd.read_csv(workbook_inicial)
df_inicial['srcTime'] = pd.to_datetime(df_inicial['srcTime']) #cambiamos el srcTime a tipo de dato datetime
df_inicial['srcTime'] = df_inicial['srcTime'] - pd.Timedelta(hours=6, minutes=0, seconds=0) #ajustamos las horas a horario "noraml"
df_inicial['Time'] = df_inicial['srcTime'].dt.strftime('%H:%M:%S') # le quitamos la fecha para solo dejar las hroas minuts y seguindos
df_inicial['Miliseconds'] = df_inicial['srcTime'].dt.strftime('.%f') # guardamos las milesimas de segundo en otra columna
df_inicial['Time'] = df_inicial['Time'].apply(get_sec) ##aplicamos la funcion para cambiar horas minutos y segundos a solo segundos
df_inicial["Time"] = df_inicial['Time'].astype(str) + df_inicial["Miliseconds"] #juntamos las columnas de segundos.milisegundos
df_inicial=df_inicial[['TradeId','Time','instrument','Price','Quantity']] ##seleccionamos las columnas que nos interesan
n = 1
#df_inicial1=df_inicial.iloc[:-n]
df_2inicial=df_inicial.sort_values('Time') #ordenamos el DF por el tiempo, recuerda que aqui el tiempo ya esta en formato segundos.milesegundos
df_2=df_2inicial.iloc[:-n] #eliminamos lo svalores raros

df_2['Quantity'] = df_2['Quantity'].astype(int)

#############################################################################
#################   EMEZAMOS A HACER LOS CALCULOS
#############################################################################

df_grafica = pd.DataFrame(columns = ['Hora Inicial' , 'Hora Final', 'Cantidad'])

before_market=float(25200.00000) ###### esto es a las 7:00 am
hora_inicial=float(27000.00000) ####empieza en 2700 segundos por que serían las 7:30 am, este lo tendrías que cambiar en caso de ser necesario
cantidadTotal=0



#############################################################################
#################   EMEZAMOS A hacer calculos de volumen que se hace before market (7:00 a 7:30)
#############################################################################

for i in range(len(df_2)):
    if float(df_2.iloc[i]['Time'])<hora_inicial:
       cantidadTotal=cantidadTotal+df_2.iloc[i]['Quantity']
    else:
        df_grafica=df_grafica.append({'Hora Inicial' : int(25200), 'Hora Final' : int(27000), 'Cantidad' : int(cantidadTotal)} , ignore_index=True)
        cantidadTotal=0
        cantidadTotal=cantidadTotal+df_2.iloc[i]['Quantity']
        break
print ("Before Market Done")


###############################################################################
#######en este for por cada rango de tiempo en segundos que existe en la variable "Segundos" tomamos el volumen y lo sumamos, en caso de que quieras un rango mayor de tiempo, pues solo le pones 10 o lo que necesites en el if
###############################################################################

cantidadTotal=0
for i in range(len(df_2)):
    if float(df_2.iloc[i]['Time'])>=float(27000.00000):
        if float(df_2.iloc[i]['Time'])<=float(hora_inicial+Segundos):
            cantidadTotal=cantidadTotal+df_2.iloc[i]['Quantity']
            #print("esta es la cantidad",df_2.iloc[i]['Quantity'])
        else:
            df_grafica=df_grafica.append({'Hora Inicial' : int(hora_inicial), 'Hora Final' : int(hora_inicial+Segundos), 'Cantidad' : int(cantidadTotal)} , ignore_index=True)
            #print("Pasaron 5 minutos y esta es la suma: ", cantidadTotal)
            cantidadTotal=0
            cantidadTotal=cantidadTotal+df_2.iloc[i]['Quantity']
            hora_inicial=hora_inicial+Segundos
print ("During Market Done")



###############################################################################
####esta linea es por qu een el if ignora la última linea del archvio, por eso aquí ya nada más lo agregamos
df_grafica=df_grafica.append({'Hora Inicial' : int(hora_inicial), 'Hora Final' : int(hora_inicial+Segundos), 'Cantidad' : int(cantidadTotal)} , ignore_index=True)
###############################################################################


##########
####Pasamos a horas minutos y segundos las dos columnas del df y lo guardamos como csv
##########
df_grafica['Hora Inicial'] = df_grafica['Hora Inicial'].apply(segundos_a_segundos_minutos_y_horas)
df_grafica['Hora Final'] = df_grafica['Hora Final'].apply(segundos_a_segundos_minutos_y_horas)
df_grafica=df_grafica[['Hora Final','Cantidad']] ##seleccionamos las columnas que nos interesan


print("este es el df creado:\n ", df_grafica)

df_grafica.to_csv('/home/ops/ReportesOperaciones/HechosBIVA/volumen'+ISIN+numeroFile+'.csv', index = False)



