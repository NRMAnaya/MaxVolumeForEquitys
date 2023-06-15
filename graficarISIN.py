# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 09:51:11 2023

@author: nmorales
"""

import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from datetime import datetime

workbook_emisoras='C:\\Users\\nmorales\\Documents\\PythonHero\\Rebalanceo\\RebalanceoISINemisorasPrueba.txt'
df_emisoras=pd.read_csv(workbook_emisoras)


########################
###################Obtenemos la grafica del df de las emisoras
########################

numeroEmisoras=df_emisoras.shape
filas=numeroEmisoras[0]

x=0
while x<filas:
    isinEmisora=df_emisoras.loc[x, 'EMISORAS']
    workbook_ISIN='C:\\Users\\nmorales\\Documents\\PythonHero\\Rebalanceo\\volumenMaestro\\volumenMaestro'+isinEmisora+'6.csv'
    df_isin=pd.read_csv(workbook_ISIN)
    df_isin.plot(x ='Hora Final', kind='line', title=isinEmisora)
    x=x+1

##################################