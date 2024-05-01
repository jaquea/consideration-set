# coding=utf-8
import csv
import os
import pickle
import time
from collections import defaultdict
from random import randint
from random import seed

import dill
import pandas as pd  # this is how I usually import pandas
import utm

from constants import PROJECT_DIR

dump_file1 = open(os.path.join(PROJECT_DIR,'tmp','grafo.igraph'), 'rb')
g = pickle.load(dump_file1)
dump_file1.close()

dump_file1 = open(os.path.join(PROJECT_DIR, 'tmp', 'dict_servicio_llave_codigoTS.pkl'), 'rb')
dict_servicio_llave_codigoTS = pickle.load(dump_file1)
dump_file1.close()

#estimacion con 3 semanas (semana 3, semana 2 y semana 1)

dump_file2 = open(os.path.join(PROJECT_DIR, 'tmp', 'viajes_reales_3semanas.pkl'), 'rb')
viajes = dill.load(dump_file2)
dump_file2.close()

dump_file1 = open(os.path.join(PROJECT_DIR, 'tmp', 'viajes_alternativas_3semanas.pkl'), 'rb')
viajes_alternativas = dill.load(dump_file1)
dump_file1.close()

print(len(viajes))

lista_de_viajes= []

for origen in viajes:
    for destino in viajes[origen]:
        n = sum([viajes[origen][destino][camino] for camino in viajes[origen][destino]])
        dic_viaje = dict(origen=origen, destino=destino, n=n)
        lista_de_viajes.append(dic_viaje)

lista_de_viajes.sort(key=lambda x: x['n'], reverse=True)

# Crear una nueva lista de viajes con solo los elementos que cumplen la condición
lista_de_viajes = [elemento for elemento in lista_de_viajes
                            if elemento['n'] >= 30
                            and len(viajes_alternativas[elemento['origen']][elemento['destino']]) > 1]


cont = len(lista_de_viajes)

print(cont)
answer = set()
sampleSize = 2
answerSize = 0
lista = []

seed(400)

while answerSize < sampleSize:
    r = randint(0,cont)
    if r not in answer:
        answer.add(r)
        parOD = lista_de_viajes[r]
        lista.append(parOD)
        answerSize += 1

with open(os.path.join(PROJECT_DIR, 'tmp', 'lista_de_pares_od.pkl'), 'wb') as archivo_pickle:
    pickle.dump(lista, archivo_pickle)

print(lista)

