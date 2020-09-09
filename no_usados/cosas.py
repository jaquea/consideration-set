import pandas as pd
import re
import unicodedata
from igraph import *
from HeapBinaria import HeapBinaria
import pickle
import dill
import pandas as pd
import random
import utm
import matplotlib.pyplot as pl
import time

dump_file2 = open('../tmp/viajes_procesados.pkl', 'rb')
viajes = dill.load(dump_file2)
dump_file2.close()

print(len(viajes))
for destino in viajes:
    print(viajes[destino])

def strip_accents(text):
    """
    Strip accents from input String.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError):  # unicode is a default on python 3
        pass
    # text = re.sub('[ ]+', '_', text)
    # text.replace(' ', '')
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)


def text_to_id(text):
    """
    Convert input text to id.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    text = strip_accents(text.lower())
    # text = re.sub('[ ]+', '_', text)
    # text.replace(' ', '')
    text = re.sub('[^0-9a-zA-Z_-]', '', text)
    text = text.split('-')[0]
    return text


df_tiempos = pd.read_csv( 'C:\Users\jacke\Desktop\ChicagoSketch\\tiempos_metro.csv', encoding='latin1', sep=';')

for idx, row in df_tiempos.iterrows():
    cabeza = row['Inicio']
    cola = row['Fin']
    tiempo = float(row['tViaje'])
    frecuencia = 60 / float(row['espera_pam1'])

    cabeza = row['Inicio']
    cola = row['Fin']
    tiempo = float(row['tViaje'])
    frecuencia = 60 / float(row['espera_pam1'])

    cabeza = cabeza.split(' L1')[0]
    cabeza = cabeza.split(' L2')[0]
    cabeza = cabeza.split(' L4')[0]
    cabeza = cabeza.split(' L5')[0]
    cabeza = cabeza.split(' L6')[0]
    cabeza = cabeza.replace(" ", "")
    cabeza = text_to_id(cabeza)

    cola = cola.split(' L1')[0]
    cola = cola.split(' L2')[0]
    cola = cola.split(' L4')[0]
    cola = cola.split(' L5')[0]
    cola = cola.split(' L6')[0]
    cola = cola.replace(" ", "")
    cola = text_to_id(cola)

    #print(cabeza, cola, tiempo, frecuencia)