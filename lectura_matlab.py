# -*- coding: utf-8 -*-
import json
import pickle
from time import time

import dill
import pandas as pd
import utm
from igraph import *

from HeapBinaria import HeapBinaria

# se leen los datos y se genera el grafo, es el primer codigo que se debe correr
heap = HeapBinaria()

###diccionarios de localizacion geografica paraderos y estaciones de metro
df_paraderos = pd.read_csv('inputs\\ConsolidadoParadas.csv')
df_metro = pd.read_csv('inputs\\Diccionario-EstacionesMetro.csv')
df_metro_reducido = pd.read_csv('inputs\\metro_stations.csv', delimiter=";")  # diccionario que formo leonel

radio = 100

paraderos_coord_dic = defaultdict(list)
traduccion_metro = defaultdict(str)
paraderos_serv = defaultdict(int)

for idx, row in df_metro_reducido.iterrows():
    codigo = row['codigo']
    estacion = row['estacion']
    traduccion_metro[estacion] = codigo
    paraderos_serv[estacion] = 0

for idx, row in df_paraderos.iterrows():
    codigo_paradero = row['Codigo paradero TS']
    x = row['x']
    y = row['y']
    paraderos_coord_dic[codigo_paradero] = (x, y)
    paraderos_serv[codigo_paradero] = 0

df_metro['x'] = df_metro[['LATITUD', 'LONGITUD']].apply(lambda x: round(utm.from_latlon(x[0], x[1])[0], 2), axis=1)
df_metro['y'] = df_metro[['LATITUD', 'LONGITUD']].apply(lambda x: round(utm.from_latlon(x[0], x[1])[1], 2), axis=1)

for idx, row in df_metro.iterrows():
    estacion = row['ESTANDAR']
    x = row['x']
    y = row['y']
    if estacion in traduccion_metro:
        est_trad = traduccion_metro[estacion]
        paraderos_coord_dic[est_trad] = (x, y)

dump_file = open('tmp\\paraderos_coord_dic', 'wb')
pickle.dump(paraderos_coord_dic, dump_file)
dump_file.close()

paradero_cercano_dic = defaultdict(list)
paradero_cercano_dic1 = defaultdict(list)
for llave1 in paraderos_coord_dic:
    x1 = float(paraderos_coord_dic[llave1][0])
    y1 = float(paraderos_coord_dic[llave1][1])
    for llave2 in paraderos_coord_dic:
        if llave1 != llave2:
            x2 = float(paraderos_coord_dic[llave2][0])
            y2 = float(paraderos_coord_dic[llave2][1])
            # dist = (((x1-x2)**2) + ((y1-y2)**2))**0.5
            dist = abs(x1 - x2) + abs(y1 - y2)

            if dist <= radio:
                costo = dist * 60 / (1000 * 4)
                paradero_cercano_dic[llave1].append((llave2, costo))

            if dist <= radio and llave2 not in paradero_cercano_dic1[llave1]:
                paradero_cercano_dic1[llave1].append(llave2)

print('ya genere arcos de caminata')

with open('inputs\\info_servicios.json') as data_file:
    data = json.loads(data_file.read())

df = pd.DataFrame.from_dict(data, orient='columns')

# df= df[(df['servicio']=='T405 00I') | (df['servicio']=='L1-I')]

dict_paradas = defaultdict(int)
dict_tiempos = defaultdict(lambda: defaultdict(lambda: -1))
dict_frecuencia = defaultdict(lambda: defaultdict(lambda: 0))

contador_vertice = 20000
contador_arco = 0
numero = 0

arcos = []
vertices = []

arcos_metro = []
vertices_metro = []

for idx, row in df.iterrows():
    frec_nom = row['frec_nom'] / 60
    paradas = row['paradas']  # lista
    sentido = row['sentido']
    servicio = str(row['servicio'])
    servicio_user = row['servicio_user']
    t_ADATRAP = row['t_ADATRAP']  # lista
    t_GTFS = row['t_GTFS']  # lista
    vertice_anterior = ''

    # arcos servicio
    cont_par = 0
    contador_vertice_anterior = 0

    tiempo_total = 0

    for par in paradas:
        if str(par[0]) not in dict_paradas:
            dict_paradas[str(par[0])] = numero
            numero = numero + 1

        vertice = str(par[0]) + "/" + servicio

        dict_frecuencia[servicio][str(par[0])] = float(frec_nom)

        if type(t_ADATRAP[cont_par][0]) == float or type(t_ADATRAP[cont_par][0]) == int:
            tiempo_total += t_ADATRAP[cont_par][0]
            dict_tiempos[servicio][str(par[0])] = tiempo_total

        elif type(t_GTFS[cont_par][0]) == float or type(t_GTFS[cont_par][0]) == int:
            tiempo_total += t_GTFS[cont_par][0]
            dict_tiempos[servicio][str(par[0])] = tiempo_total

        # arco subida
        arcos.append((dict_paradas[str(par[0])], contador_vertice, frec_nom, 0, str(par[0]), vertice))

        if str(par[0])[:2] == 'M-':
            arcos_metro.append((dict_paradas[str(par[0])], contador_vertice, frec_nom, 0, str(par[0]), vertice))


        if (dict_paradas[str(par[0])], str(par[0]), 'paradero') not in vertices:
            vertices.append((dict_paradas[str(par[0])], str(par[0]), 'paradero'))

            if str(par[0])[:2] == 'M-':
                vertices_metro.append((dict_paradas[str(par[0])], str(par[0]), 'paradero'))

        if (contador_vertice, vertice, 'servicio') not in vertices:
            vertices.append((contador_vertice, vertice, 'servicio'))

            if str(par[0])[:2] == 'M-':
                vertices_metro.append((contador_vertice, vertice, 'servicio'))

        contador_arco += 1

        # print('arcos subida:', dict_paradas[str(par[0])], contador_vertice, frec_nom, 0)

        # arco bajada
        arcos.append((contador_vertice, dict_paradas[str(par[0])], float('inf'), 0, vertice, str(par[0])))
        contador_arco += 1

        if str(par[0])[:2] == 'M-':
            arcos_metro.append((contador_vertice, dict_paradas[str(par[0])], float('inf'), 0, vertice, str(par[0])))

        # print('arcos bajada:', contador_vertice, dict_paradas[str(par[0])], 0, 0)

        # arcos de servicio
        if vertice_anterior != '':

            if type(t_ADATRAP[cont_par][0]) == float:
                arcos.append((contador_vertice_anterior, contador_vertice, float('inf'), t_ADATRAP[cont_par][0],
                              vertice_anterior, vertice))
                contador_arco += 1

                if str(par[0])[:2] == 'M-':
                    arcos_metro.append((contador_vertice_anterior, contador_vertice, float('inf'), t_ADATRAP[cont_par][0],
                                  vertice_anterior, vertice))

            else:
                arcos.append((contador_vertice_anterior, contador_vertice, float('inf'), t_GTFS[cont_par][0],
                              vertice_anterior, vertice))
                contador_arco += 1

                if str(par[0])[:2] == 'M-':
                    arcos_metro.append((contador_vertice_anterior, contador_vertice, float('inf'), t_GTFS[cont_par][0],
                                  vertice_anterior, vertice))

            # print('arcos servicio:', contador_vertice - 1, contador_vertice, float('inf'), t_ADATRAP[cont_par][0])

        cont_par += 1
        vertice_anterior = vertice
        contador_vertice_anterior = contador_vertice
        contador_vertice += 1

# print(len(arcos), len(vertices))


t_ini = time()
g = Graph(directed=True)
g_metro = Graph(directed=True)

for v in vertices:
    g.add_vertex(name=str(v[0]), name2=v[1], tipo=v[2])

    # if v[2]=='paradero' and v[1] in paradero_cercano_dic:
    # print(v[1], 'tiene paraderos cercanos')

    # else:
    # print(v[1], 'no tiene paraderos cercanos')
for v in vertices_metro:
    g_metro.add_vertex(name=str(v[0]), name2=v[1], tipo=v[2])

for v in vertices:
    name = str(v[0])
    name2 = v[1]
    tipo = v[2]

    # print(name, name2, tipo)

    if tipo == 'paradero' and name2 in paradero_cercano_dic:
        for par in paradero_cercano_dic[name2]:
            vertice_cercano = par[0]
            if vertice_cercano in g.vs['name2']:
                # print(name, name2, tipo, vertice_cercano)
                indice = g.vs.find(name2=vertice_cercano).index
                # print(indice, name, name2, tipo, vertice_cercano)
                name_par = g.vs[indice]["name"]
                arcos.append((name, name_par, float('inf'), par[1], name2, g.vs[indice]["name2"]))
print(vertices)
print(arcos)
for a in arcos:
    g.add_edge(str(a[0]), str(a[1]), frecuencia=a[2], tpo_viaje=a[3], peso=(1 / float(a[2])) + a[3])

for a in arcos_metro:
    g_metro.add_edge(str(a[0]), str(a[1]), frecuencia=a[2], tpo_viaje=a[3], peso=(1 / float(a[2])) + a[3])

    # print(a)

    # print('arco',str(a[0]), str(a[1]), a[2], a[3])

t_fin = time()

t_ejecucion = t_fin - t_ini

print(t_ejecucion)

# guardar grafo en un archivo
dump_file1 = open('tmp\\grafo.igraph', 'wb')
pickle.dump(g, dump_file1)
dump_file1.close()

dump_file1 = open('tmp\\grafo_metro.igraph', 'wb')
pickle.dump(g_metro, dump_file1)
dump_file1.close()

dump_file1 = open('tmp\\paradero_cercano_dic.pkl', 'wb')
pickle.dump(paradero_cercano_dic1, dump_file1)
dump_file1.close()

dump_file2 = open('tmp\\tiempos.pkl', 'wb')
dill.dump(dict_tiempos, dump_file2)
dump_file2.close()

dump_file3 = open('tmp\\frecuencias.pkl', 'wb')
dill.dump(dict_frecuencia, dump_file3)
dump_file3.close()

dump_file2 = open('tmp\\paraderos_coord_dic.pkl', 'wb')
dill.dump(paraderos_coord_dic, dump_file2)
dump_file2.close()

print('grafo guardado en archivo!')
