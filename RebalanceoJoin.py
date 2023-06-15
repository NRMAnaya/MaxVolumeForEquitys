import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os
import sys

from datetime import datetime


numeroFile=int(sys.argv[1])
ISIN=(sys.argv[2])
fechaColumna=str(sys.argv[3])
#tiempoVolumen=str(sys.argv[4])
print("esta es la fecha",fechaColumna)
RebalanceoDias='/home/ops/ReportesOperaciones/HechosBIVA/RebalanceoDias.txt'
df_RebalanceoDias=pd.read_csv(RebalanceoDias)
numeroArchivos=len(df_RebalanceoDias)+1 #se le suma 1 por que cuenta la primer fecha como header
print("estos son los dias: ",numeroArchivos)

###funcion para pasar a segundos
def segundos_a_segundos_minutos_y_horas(segundos):
    horas = int(segundos / 60 / 60)
    segundos -= horas*60*60
    minutos = int(segundos/60)
    segundos -= minutos*60
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"


if numeroFile==1:
    print("Aqui creamos el primer maestro combinando el file 1 con el arhcvio que solo tiene las horas ")
#    tiempoVolumen=str(int(tiempoVolumen))
#    tiempoVolumen=str(tiempoVolumen)
    numeroFile=str(int(numeroFile))
    numeroFile=str(numeroFile)
    archivo1='/home/ops/ReportesOperaciones/HechosBIVA/horasCada120seg.csv'
    archivo2='/home/ops/ReportesOperaciones/HechosBIVA/volumen'+ISIN+numeroFile+'.csv'
    df_archivo1=pd.read_csv(archivo1)
    df_archivo2=pd.read_csv(archivo2)
    print(df_archivo1)
    print(df_archivo2)
    df_archivo1['Hora Final'] = df_archivo1['Hora Final'].apply(segundos_a_segundos_minutos_y_horas) 
#    df_archivo1['Hora Final'] = df_archivo1['Hora'].apply(segundos_a_segundos_minutos_y_horas)
#    print(df_archivo1)
    df_maestro=pd.merge(df_archivo1,df_archivo2[['Hora Final','Cantidad']],on='Hora Final',how='left');
    df_maestro['Cantidad'] = df_maestro['Cantidad'].fillna(0)
    df_maestro.rename(columns = {'Cantidad':fechaColumna}, inplace = True)
 #   df_maestro2=df_maestro.drop(columns=['Hora'])
    print(df_maestro)
    df_maestro.to_csv('/home/ops/ReportesOperaciones/HechosBIVA/volumenMaestro'+ISIN+numeroFile+'.csv', index = False)
else:

    if numeroFile==2:
        print("Aqui creamos el segundo maestro combinando el file 2 con el maestro 1")
        maestro=str(int(numeroFile-1))
        maestro=str(maestro)
        numeroFile=str(numeroFile)
        print("Ya se creo el archvio ",numeroFile," se combina con el primer maestro: ",maestro)
        archivo1='/home/ops/ReportesOperaciones/HechosBIVA/volumenMaestro'+ISIN+maestro+'.csv'
        archivo2='/home/ops/ReportesOperaciones/HechosBIVA/volumen'+ISIN+numeroFile+'.csv'
        df_archivo1=pd.read_csv(archivo1)
        df_archivo2=pd.read_csv(archivo2)
        df_maestro=pd.merge(df_archivo1,df_archivo2[['Hora Final','Cantidad']],on='Hora Final',how='left');
        df_maestro.rename(columns = {'Cantidad':fechaColumna}, inplace = True)
        df_maestro.to_csv('/home/ops/ReportesOperaciones/HechosBIVA/volumenMaestro'+ISIN+numeroFile+'.csv', index = False)
    else:
        print("Ya existe un maestro y seguimos combiando")
        maestroNuevo=int(numeroFile) ###este es nuevo que vamos a crear
        maestroNuevo=str(maestroNuevo)
        maestroAnterior=int(numeroFile-1) #se combina con el file en curso, ejemplo maestro 2 (3-1=2) con el file 3
        maestroAnterior=str(maestroAnterior)
        numeroFile=str(numeroFile)
        archivo1='/home/ops/ReportesOperaciones/HechosBIVA/volumenMaestro'+ISIN+maestroAnterior+'.csv'
        archivo2='/home/ops/ReportesOperaciones/HechosBIVA/volumen'+ISIN+numeroFile+'.csv'
        df_archivo1=pd.read_csv(archivo1)
        df_archivo2=pd.read_csv(archivo2)
        df_maestro=pd.merge(df_archivo1,df_archivo2[['Hora Final','Cantidad']],on='Hora Final',how='left')
        df_maestro.rename(columns = {'Cantidad':fechaColumna}, inplace = True)
        df_maestro.to_csv('/home/ops/ReportesOperaciones/HechosBIVA/volumenMaestro'+ISIN+maestroNuevo+'.csv', index = False)






"""
numeroFile=int(sys.argv[1])
ISIN=(sys.argv[2])
fechaColumna=str(sys.argv[3])
print("esta es la fecha",fechaColumna)
RebalanceoDias='/home/ops/ReportesOperaciones/HechosBIVA/RebalanceoDias.txt'
df_RebalanceoDias=pd.read_csv(RebalanceoDias)
numeroArchivos=len(df_RebalanceoDias)+1 #se le suma 1 por que cuenta la primer fecha como header
print("estos son los dias: ",numeroArchivos)

archivo='/home/ops/ReportesOperaciones/HechosBIVA/volumen'+ISIN+numeroFile+'.csv'
horas=
"""
"""
if numeroFile==1:
    print("A penas se generó el primer file, esperamos al segundo File, pero renombramos la columna del archivo 1 para que sea la primer columna con fecha")
    numeroFile=str(numeroFile)
    archivo1='/home/ops/ReportesOperaciones/HechosBIVA/volumen'+ISIN+numeroFile+'.csv'
    df_archivo1=pd.read_csv(archivo1)
    df_archivo1.rename(columns = {'Cantidad':fechaColumna}, inplace = True)
    df_archivo1.to_csv('/home/ops/ReportesOperaciones/HechosBIVA/volumen'+ISIN+numeroFile+'.csv', index = False)
    exit()
else:
    if numeroFile==2:
        print("Aqui creamos el primer maestro combinando el file 1 con el 2")
        maestro=str(int(numeroFile-1))
        maestro=str(maestro)
        numeroFile=str(numeroFile)
        print("Ya se creo el archvio ",numeroFile," se combina con el anterior o el ultimo maestro: ",maestro)
        archivo1='/home/ops/ReportesOperaciones/HechosBIVA/volumen'+ISIN+maestro+'.csv'
        archivo2='/home/ops/ReportesOperaciones/HechosBIVA/volumen'+ISIN+numeroFile+'.csv'
        df_archivo1=pd.read_csv(archivo1)
        df_archivo2=pd.read_csv(archivo2)
        df_maestro=pd.merge(df_archivo1,df_archivo2[['Hora Final','Cantidad']],on='Hora Final',how='left');
        df_maestro.rename(columns = {'Cantidad':fechaColumna}, inplace = True)
        df_maestro.to_csv('/home/ops/ReportesOperaciones/HechosBIVA/volumenMaestro'+ISIN+maestro+'.csv', index = False)
    else:
        print("Ya existe un maestro y seguimos combiando")
        maestroNuevo=int(numeroFile-1) ###este es nuevo que vamos a crear 
        maestroNuevo=str(maestroNuevo)
        maestroAnterior=int(numeroFile-2) #se combina con el file en curso, ejemplo maestro 1 (3-2=1) con el file 3 
        maestroAnterior=str(maestroAnterior)
        numeroFile=str(numeroFile)
        archivo1='/home/ops/ReportesOperaciones/HechosBIVA/volumenMaestro'+ISIN+maestroAnterior+'.csv'
        archivo2='/home/ops/ReportesOperaciones/HechosBIVA/volumen'+ISIN+numeroFile+'.csv'
        df_archivo1=pd.read_csv(archivo1)
        df_archivo2=pd.read_csv(archivo2)
        df_maestro=pd.merge(df_archivo1,df_archivo2[['Hora Final','Cantidad']],on='Hora Final',how='left')
        df_maestro.rename(columns = {'Cantidad':fechaColumna}, inplace = True)
        df_maestro.to_csv('/home/ops/ReportesOperaciones/HechosBIVA/volumenMaestro'+ISIN+maestroNuevo+'.csv', index = False)
"""












"""
numeroFile=int((sys.argv[1]))

RebalanceoDias='/home/ops/ReportesOperaciones/HechosBIVA/RebalanceoDias.txt'
df_RebalanceoDias=pd.read_csv(RebalanceoDias)
numeroArchivos=len(df_RebalanceoDias)+1 #se le suma 1 por que cuenta la primer fecha como header
print("estos son los dias: ",numeroArchivos)

if numeroFile==1:
    print("Es el primer archvio, no se combina")
    exit()
else:
    if numeroFile==numeroArchivos:
        print("Es la ultima combinacion y ya salimos")
    else:
        print("Empezamos a combinar archvios")
"""
