# coding=utf-8
# se debe ejecutar despues de proces_viajes.py
# se genera el archivo viajes procesados que permite entregar los viajes por par OD en base al radio de 100 mts por cada par de paraderos OD
import utm
import dill
import pandas as pd #this is how I usually import pandas
from collections import defaultdict
import csv

from random import seed
from random import randint

dump_file2 = open('tmp\\viajes.pkl', 'rb')
viajes = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_reales.pkl', 'rb')
viajes_reales = dill.load(dump_file2)
dump_file2.close()

dump_file1 = open('tmp\\viajes_alternativas_desglosadas.pkl', 'rb')
viajes_alternativas_desaglosadas = dill.load(dump_file1)
dump_file1.close()

dump_file1 = open('tmp\\viajes_alternativas.pkl', 'rb')
viajes_alternativas = dill.load(dump_file1)
dump_file1.close()

print(viajes_alternativas_desaglosadas['T-34-270-SN-30']['T-31-134-SN-20'])

#viajes_p = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:0)))

#viajes_p['T-34-313-SN-35']['M-SL']= viajes['T-34-313-SN-35']['M-SL']
#viajes_p['T-34-313-SN-35']['E-20-205-SN-65']= viajes['T-34-313-SN-35']['E-20-205-SN-65']
#viajes_p['L-34-53-25-PO']['M-SL']= viajes['L-34-53-25-PO']['M-SL']
#viajes_p['T-34-313-SN-35']['M-SL']= viajes['T-34-313-SN-35']['M-SL']

#viajes = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:0)))

#viajes=viajes_p

print(len(viajes))

lista_de_viajes= []

with open('outputs\\resumen_pares_OD.csv', 'wb') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(['origen', 'destino', 'total_viajes'])

    for origen in viajes:
        for destino in viajes[origen]:
            n = sum([viajes[origen][destino][camino] for camino in viajes[origen][destino]])
            dic_viaje = dict(origen=origen, destino=destino, n=n)
            lista_de_viajes.append(dic_viaje)
            writer.writerow([origen, destino, n])

lista_de_viajes.sort(key=lambda x: x['n'], reverse=True)

cont = 0
for elemento in lista_de_viajes:

    origen = elemento['origen']
    destino = elemento['destino']
    n = elemento['n']
    if n>=100:
        cont += 1

print(cont)
answer = set()
sampleSize = 200
answerSize = 0
lista = []

seed(200)

while answerSize < sampleSize:
    r = randint(0,cont)
    if r not in answer:
        answerSize += 1
        answer.add(r)
        parOD = lista_de_viajes[r]
        lista.append(parOD)

lista_de_viajes = lista
print(len(lista_de_viajes))
print(lista_de_viajes)

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

print ('viajes_reales',viajes_reales['M-PI']['M-SJ'])

exit(0)

viajes_procesados = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
viajes_alternativas_desaglosadas_procesados  = defaultdict(lambda: defaultdict(list))
viajes_alternativas_procesados  = defaultdict(lambda: defaultdict(list))

cont = 0
for elemento in lista_de_viajes:
    cont +=1
    origen = elemento['origen']
    destino = elemento['destino']
    print(cont)
    grupo_subida = paradero_cercano_dic[origen]
    grupo_bajada = paradero_cercano_dic[destino]
    tuplas = [(x, y) for x in grupo_subida for y in grupo_bajada]

    for par in tuplas:
        if par[0] in viajes_reales and par[1] in viajes_reales[par[0]]:
            for camino in viajes_reales[par[0]][par[1]]:
                viajes_procesados[destino][origen][camino] = viajes_reales[par[0]][par[1]][camino]

            for camino in viajes_alternativas_desaglosadas[origen][destino]:
                if camino not in viajes_alternativas_desaglosadas_procesados[origen][destino]:
                    viajes_alternativas_desaglosadas_procesados[origen][destino].append(camino)

            for camino in viajes_alternativas[origen][destino]:
                if camino not in viajes_alternativas_procesados[origen][destino]:
                    viajes_alternativas_procesados[origen][destino].append(camino)

print('viajes_alternativas_desaglosadas_procesados', viajes_alternativas_desaglosadas_procesados)
print('viajes_alternativas_procesados', viajes_alternativas_procesados)

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

print(len(viajes_procesados))
