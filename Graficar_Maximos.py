# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 11:41:38 2023

@author: nmorales
"""
import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from datetime import datetime

workbook_emisoras='C:\\Users\\nmorales\\Documents\\PythonHero\\Rebalanceo\\RebalanceoISINemisorasPrueba.txt'
workbook_dias='C:\\Users\\nmorales\\Documents\\PythonHero\\Rebalanceo\\RebalanceoDias.txt'
workbook_emisorasName='C:\\Users\\nmorales\\Documents\\PythonHero\\Rebalanceo\\nameEmisoras.txt'

df_emisoras=pd.read_csv(workbook_emisoras)
df_dias=pd.read_csv(workbook_dias)
df_nameEmisoras=pd.read_csv(workbook_emisorasName)



df_emisoras2=pd.concat([df_emisoras,df_nameEmisoras],axis=1)


numeroEmisoras=df_emisoras.shape
filas=numeroEmisoras[0]

x=0
while x<filas:
    isinEmisora=df_emisoras.loc[x, 'EMISORAS']
    nameEmisora=df_emisoras2.loc[x, 'Emisoras']
    workbook_inicial='C:\\Users\\nmorales\\Documents\\PythonHero\\Rebalanceo\\volumenMaestro\\volumenMaestro'+isinEmisora+'6.csv'
    df_inicial=pd.read_csv(workbook_inicial)
    ###graficamos cn esta linea
    df_inicial.plot(x ='Hora Final', kind='line', title=nameEmisora)
    x=x+1
    shape = df_inicial.shape
    columnas=shape[1]
    i=1
    df_final= pd.DataFrame()
    while i<columnas:
        columna=df_inicial.columns.values[i]
        df_nuevo=df_inicial [df_inicial[columna] == df_inicial[columna]. max ()]
        #
        df_2=df_nuevo.iloc[:, [0,i]]
        df_3=df_2.rename(columns={ df_2.columns[1]: "MaxVol" })
        #print(df_3)
        if i==1:
            #print("aqui no concatenamos")
            df_final=df_3
        else:
            #print("aquí concatenamos el neuvo con el anterior y lo guardamos como elnuevo")
            df_final=pd.concat([df_final,df_3])
            
        i=i+1
    df_final2=df_final.reset_index()
    df_final3=pd.concat([df_final2,df_dias],axis=1)
    df_final3 = df_final3.drop('index', axis=1)
    print("Esta es la hora a la que hubo mas volumen de la emisora: ",nameEmisora,"\n",df_final3)
    ###guardamos el df
    #df_final3.to_csv('example.csv')









#


