# coding=utf-8
# se debe ejecutar despues de proces_viajes.py
# se genera el archivo viajes procesados que permite entregar los viajes por par OD en base al radio de 100 mts por cada par de paraderos OD
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

'''
#estimacion con 1 semana (semana 3)

dump_file2 = open('tmp\\viajes_reales_1semana.pkl', 'rb')
viajes = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_reales_1semana.pkl', 'rb')
viajes_reales = dill.load(dump_file2)
dump_file2.close()

dump_file1 = open('tmp\\viajes_alternativas_desglosadas_1semana.pkl', 'rb')
viajes_alternativas_desaglosadas = dill.load(dump_file1)
dump_file1.close()

dump_file1 = open('tmp\\viajes_alternativas_1semana.pkl', 'rb')
viajes_alternativas = dill.load(dump_file1)
dump_file1.close()

'''
'''
#estimacion con 2 semanas (semana 3 y semana 2)

dump_file2 = open('tmp\\viajes_reales_2semanas.pkl', 'rb')
viajes = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_reales_2semanas.pkl', 'rb')
viajes_reales = dill.load(dump_file2)
dump_file2.close()

dump_file1 = open('tmp\\viajes_alternativas_desglosadas_2semanas.pkl', 'rb')
viajes_alternativas_desaglosadas = dill.load(dump_file1)
dump_file1.close()

dump_file1 = open('tmp\\viajes_alternativas_2semanas.pkl', 'rb')
viajes_alternativas = dill.load(dump_file1)
dump_file1.close()
'''

#estimacion con 3 semanas (semana 3, semana 2 y semana 1)

dump_file2 = open('tmp\\viajes_reales_3semanas.pkl', 'rb')
viajes = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_reales_3semanas.pkl', 'rb')
viajes_reales = dill.load(dump_file2)
dump_file2.close()

dump_file1 = open('tmp\\viajes_alternativas_desglosadas_3semanas.pkl', 'rb')
viajes_alternativas_desaglosadas = dill.load(dump_file1)
dump_file1.close()

dump_file1 = open('tmp\\viajes_alternativas_3semanas.pkl', 'rb')
viajes_alternativas = dill.load(dump_file1)
dump_file1.close()


#estimacion con semana 4 para prediccion
'''
dump_file2 = open('tmp\\viajes_prediccion_mismos_pares_OD_reales.pkl', 'rb')
viajes = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_prediccion_mismos_pares_OD_reales.pkl', 'rb')
viajes_reales = dill.load(dump_file2)
dump_file2.close()

dump_file1 = open('tmp\\viajes_prediccion_mismos_pares_OD_alternativas_desagregadas.pkl', 'rb')
viajes_alternativas_desaglosadas = dill.load(dump_file1)
dump_file1.close()

dump_file1 = open('tmp\\viajes_prediccion_mismos_pares_OD_alternativas.pkl', 'rb')
viajes_alternativas = dill.load(dump_file1)
dump_file1.close()
'''

#viajes_p = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:0)))

#viajes_p['T-34-313-SN-35']['M-SL']= viajes['T-34-313-SN-35']['M-SL']
#viajes_p['T-34-313-SN-35']['E-20-205-SN-65']= viajes['T-34-313-SN-35']['E-20-205-SN-65']
#viajes_p['L-34-53-25-PO']['M-SL']= viajes['L-34-53-25-PO']['M-SL']
#viajes_p['T-34-313-SN-35']['M-SL']= viajes['T-34-313-SN-35']['M-SL']

#viajes = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:0)))

#viajes=viajes_p


dump_file1 = open(os.path.join(PROJECT_DIR,'tmp','lista_de_pares_od.pkl'), 'rb')
lista_de_viajes = pickle.load(dump_file1)
dump_file1.close()

print(len(lista_de_viajes))
###diccionarios de localizacion geografica paraderos y estaciones de metro
df_paraderos = pd.read_csv('inputs\ConsolidadoParadas.csv')
df_metro = pd.read_csv('inputs\Diccionario-EstacionesMetro.csv')

radio = 100

#se genera diccionario para guardar coordenadas de paraderos
paraderos_coord_dic = defaultdict(list)
for idx, row in df_paraderos.iterrows():
    codigo_paradero = row['Codigo paradero TS']
    x = row['x']
    y = row['y']
    paraderos_coord_dic[codigo_paradero] = (x, y)

# print(paraderos_coord_dic)

df_metro_reducido = pd.read_csv('inputs\metro_stations.csv', delimiter=";") #diccionario que formo leonel

#se genera diccionario para asignar coordenadas de estaciones de metro
dict_metro = defaultdict(str)

for idx, row in df_metro_reducido.iterrows():
    codigo = row['codigo']
    estacion = row['estacion']
    dict_metro[estacion] = codigo

df_metro['x'] = df_metro[['LATITUD', 'LONGITUD']].apply(lambda x: round(utm.from_latlon(x[0], x[1])[0], 2), axis=1)
df_metro['y'] = df_metro[['LATITUD', 'LONGITUD']].apply(lambda x: round(utm.from_latlon(x[0], x[1])[1], 2), axis=1)

for idx, row in df_metro.iterrows():
    estacion = row['ESTANDAR']
    x = row['x']
    y = row['y']
    paraderos_coord_dic[dict_metro[estacion]] = (x,y)

paradero_cercano_dic = defaultdict(list)
for llave1 in paraderos_coord_dic:
    x1 = float(paraderos_coord_dic[llave1][0])
    y1 = float(paraderos_coord_dic[llave1][1])
    for llave2 in paraderos_coord_dic:
        x2 = float(paraderos_coord_dic[llave2][0])
        y2 = float(paraderos_coord_dic[llave2][1])
        # dist = (((x1-x2)**2) + ((y1-y2)**2))**0.5
        dist = abs(x1 - x2) + abs(y1 - y2)

        if dist <= radio and llave2 not in paradero_cercano_dic[llave1]:
            paradero_cercano_dic[llave1].append(llave2)

viajes_procesados = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
viajes_alternativas_desaglosadas_procesados  = defaultdict(lambda: defaultdict(list))
viajes_alternativas_procesados  = defaultdict(lambda: defaultdict(list))

with open('outputs\\resumen_pares_OD.csv', 'wb') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(['origen', 'destino', 'total_viajes'])

    for origen in viajes_reales:
        for destino in viajes_reales[origen]:
            grupo_subida = paradero_cercano_dic[origen]
            grupo_bajada = paradero_cercano_dic[destino]
            tuplas = [(x, y) for x in grupo_subida for y in grupo_bajada]
            n_total = 0

            for par in tuplas:
                if par[0] in viajes_reales and par[1] in viajes_reales[par[0]]:
                    n = sum([viajes_reales[par[0]][par[1]][camino] for camino in viajes_reales[par[0]][par[1]]])
                    n_total += n

            writer.writerow([origen, destino, n_total])

cont = 0

for elemento in lista_de_viajes:
    cont +=1
    origen = elemento['origen']
    destino = elemento['destino']
    print('origen', origen, 'destino', destino)
    start_time = time.clock()
    grupo_subida = paradero_cercano_dic[origen]
    grupo_bajada = paradero_cercano_dic[destino]
    tuplas = [(x, y) for x in grupo_subida for y in grupo_bajada]

    for par in tuplas:
        if par[0] in viajes_reales and par[1] in viajes_reales[par[0]]:
            for camino in viajes_reales[par[0]][par[1]]:
                viajes_procesados[destino][origen][camino] = viajes_reales[par[0]][par[1]][camino]

            for camino in viajes_alternativas_desaglosadas[par[0]][par[1]]:
                if camino not in viajes_alternativas_desaglosadas_procesados[origen][destino]:
                    viajes_alternativas_desaglosadas_procesados[origen][destino].append(camino)

            for camino in viajes_alternativas[par[0]][par[1]]:
                if camino not in viajes_alternativas_procesados[origen][destino]:
                    viajes_alternativas_procesados[origen][destino].append(camino)

dump_file2 = open('tmp\\viajes_alternativas_desaglosadas_procesados.pkl', 'wb')
dill.dump(viajes_alternativas_desaglosadas_procesados, dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_alternativas_procesados.pkl', 'wb')
dill.dump(viajes_alternativas_procesados, dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_procesados.pkl', 'wb')
dill.dump(viajes_procesados, dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\paradero_cercano_dic.pkl', 'wb')
dill.dump(paradero_cercano_dic, dump_file2)
dump_file2.close()

