# -*- coding: utf-8 -*-
import scipy.io
import json
from pprint import pprint
import pandas as pd
from igraph import *
from HeapBinaria import HeapBinaria
from time import time
import pickle
import math
import utm
import matplotlib.pyplot as pl
#se leen los datos y se genera el grafo, es el primer codigo que se debe correr
heap = HeapBinaria()

###diccionarios de localizacion geografica paraderos y estaciones de metro
df_paraderos = pd.read_csv('C:\Users\jacke\Desktop\ConsolidadoParadas.csv')
df_metro = pd.read_csv('C:\Users\jacke\Desktop\Diccionario-EstacionesMetro.csv')
df_metro_reducido = pd.read_csv('C:\Users\jacke\Desktop\metro_stations.csv', delimiter=";") #diccionario que formo leonel

radio = 100

paraderos_coord_dic = defaultdict(list)
#metro_coord_dic = defaultdict(list)
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
    paraderos_coord_dic[codigo_paradero] = (x,y)
    paraderos_serv[codigo_paradero] = 0

#print(paraderos_coord_dic)

df_metro['x'] = df_metro[['LATITUD', 'LONGITUD']].apply(lambda x: round(utm.from_latlon(x[0], x[1])[0],2), axis = 1)
df_metro['y'] = df_metro[['LATITUD', 'LONGITUD']].apply(lambda x: round(utm.from_latlon(x[0], x[1])[1],2), axis = 1)

for idx, row in df_metro.iterrows():
    estacion = row['ESTANDAR']
    x = row['x']
    y = row['y']
    if estacion in traduccion_metro:
        est_trad = traduccion_metro[estacion]
        paraderos_coord_dic[est_trad] = (x, y)

dump_file = open('paraderos_coord_dic', 'wb')
pickle.dump(paraderos_coord_dic, dump_file)
dump_file.close()

paradero_cercano_dic = defaultdict(list)
for llave1 in paraderos_coord_dic:
    x1 = float(paraderos_coord_dic[llave1][0])
    y1 = float(paraderos_coord_dic[llave1][1])
    for llave2 in paraderos_coord_dic:
        if llave1 != llave2:
            x2 = float(paraderos_coord_dic[llave2][0])
            y2 = float(paraderos_coord_dic[llave2][1])
            #dist = (((x1-x2)**2) + ((y1-y2)**2))**0.5
            dist = abs(x1-x2) + abs(y1-y2)

            if dist <= radio:
                costo = dist*60/(1000*4)
                paradero_cercano_dic[llave1].append((llave2, costo))

print('ya genere arcos de caminata')

with open('C:\Users\jacke\Desktop\info_servicios.json') as data_file:
    data = json.loads(data_file.read())

df = pd.DataFrame.from_dict(data, orient='columns')

#df= df[(df['servicio']=='T405 00I') | (df['servicio']=='L1-I')]

print(df.head())

dict_paradas = defaultdict(int)
dict_tiempos = defaultdict(lambda: defaultdict(lambda: -1))
dict_frecuencia = defaultdict(lambda: defaultdict(lambda: 0))

contador_vertice = 20000
contador_arco = 0
numero = 0

arcos = []
vertices = []


for idx, row in df.iterrows():
    frec_nom = row['frec_nom']/60
    paradas = row['paradas'] #lista
    sentido = row['sentido']
    servicio = str(row['servicio'])
    servicio_user = row['servicio_user']
    t_ADATRAP = row['t_ADATRAP'] #lista
    t_GTFS = row['t_GTFS'] #lista
    vertice_anterior = ''

    # arcos servicio
    cont_par = 0
    contador_vertice_anterior = 0

    tiempo_total = 0

    for par in paradas:
        if str(par[0]) not in dict_paradas:
            dict_paradas[str(par[0])] = numero
            numero = numero +1

        vertice = str(par[0])+"/"+servicio

        dict_frecuencia[servicio][str(par[0])] = float(frec_nom)

        if type(t_ADATRAP[cont_par][0]) == float or type(t_ADATRAP[cont_par][0]) == int:
            tiempo_total += t_ADATRAP[cont_par][0]
            dict_tiempos[servicio][str(par[0])] = tiempo_total

        elif type(t_GTFS[cont_par][0]) == float or type(t_GTFS[cont_par][0]) == int:
            tiempo_total += t_GTFS[cont_par][0]
            dict_tiempos[servicio][str(par[0])] = tiempo_total


        #arco subida
        arcos.append((dict_paradas[str(par[0])], contador_vertice, frec_nom, 0, str(par[0]), vertice))

        if (dict_paradas[str(par[0])], str(par[0]), 'paradero') not in vertices:
            vertices.append((dict_paradas[str(par[0])], str(par[0]), 'paradero'))

        if (contador_vertice, vertice, 'servicio') not in vertices:
            vertices.append((contador_vertice, vertice, 'servicio'))

        contador_arco += 1


        #print('arcos subida:', dict_paradas[str(par[0])], contador_vertice, frec_nom, 0)


        #arco bajada
        arcos.append((contador_vertice, dict_paradas[str(par[0])], float('inf'), 0, vertice, str(par[0])))
        contador_arco += 1



        #print('arcos bajada:', contador_vertice, dict_paradas[str(par[0])], 0, 0)

        #arcos de servicio
        if vertice_anterior != '':

            if type(t_ADATRAP[cont_par][0])==float:
                arcos.append((contador_vertice_anterior, contador_vertice, float('inf'), t_ADATRAP[cont_par][0], vertice_anterior, vertice))
                contador_arco += 1

            else:
                arcos.append((contador_vertice_anterior, contador_vertice, float('inf'), t_GTFS[cont_par][0], vertice_anterior, vertice))
                contador_arco += 1




            #print('arcos servicio:', contador_vertice - 1, contador_vertice, float('inf'), t_ADATRAP[cont_par][0])

        cont_par += 1
        vertice_anterior = vertice
        contador_vertice_anterior = contador_vertice
        contador_vertice += 1

#print(len(arcos), len(vertices))


t_ini=time()
g = Graph(directed=True)
#g.add_vertices(70464)

#print(vertices)

for v in vertices:
    g.add_vertex(name=str(v[0]), name2=v[1], tipo=v[2])

    #if v[2]=='paradero' and v[1] in paradero_cercano_dic:
        #print(v[1], 'tiene paraderos cercanos')

    #else:
        #print(v[1], 'no tiene paraderos cercanos')

for v in vertices:
    name = str(v[0])
    name2 = v[1]
    tipo = v[2]

    #print(name, name2, tipo)

    if tipo == 'paradero' and name2 in paradero_cercano_dic:
        for par in paradero_cercano_dic[name2]:
            vertice_cercano = par[0]
            if vertice_cercano in g.vs['name2']:
                #print(name, name2, tipo, vertice_cercano)
                indice = g.vs.find(name2=vertice_cercano).index
                #print(indice, name, name2, tipo, vertice_cercano)
                name_par = g.vs[indice]["name"]
                arcos.append((name, name_par, float('inf'), par[1], name2, g.vs[indice]["name2"]))

for a in arcos:
    g.add_edge(str(a[0]), str(a[1]), frecuencia= a[2], tpo_viaje=a[3], peso=(1/float(a[2]))+a[3])

    #print(a)

    #print('arco',str(a[0]), str(a[1]), a[2], a[3])



import dill


t_fin=time()

t_ejecucion = t_fin - t_ini

print(t_ejecucion)

# guardar grafo en un archivo
dump_file1 = open('grafo.igraph', 'wb')
pickle.dump(g, dump_file1)
dump_file1.close()

dump_file2 = open('tiempos.pkl', 'wb')
dill.dump(dict_tiempos, dump_file2)
dump_file2.close()

dump_file3 = open('frecuencias.pkl', 'wb')
dill.dump(dict_frecuencia, dump_file3)
dump_file3.close()

dump_file2 = open('paraderos_coord_dic.pkl', 'wb')
dill.dump(paraderos_coord_dic, dump_file2)
dump_file2.close()

print('grafo guardado en archivo!')

'''
print('aqui parte nombre de los arcos')

file = open("C:\Users\Jacqueline\Desktop\ParQGIS.txt", "w")
file.write("id|tipoarco|linea")

paraderos_serv_y = defaultdict(float)
paraderos_serv_x = defaultdict(float)

contador = 0
for a in arcos:
    print('a', a)
    contador += 1
    #si es arco de caminata entre paraderos
    if a[4] in paraderos_coord_dic and a[5] in paraderos_coord_dic:
        x_1 = float(paraderos_coord_dic[a[4]][0])
        y_1 = float(paraderos_coord_dic[a[4]][1])

        x_2 = float(paraderos_coord_dic[a[5]][0])
        y_2 = float(paraderos_coord_dic[a[5]][1])

        id = contador
        tipoarco = 'soy arco entre paraderos'

        linea = "{}|{}|LINESTRING({} {},{} {})".format(id,tipoarco,x_1,y_1,x_2,y_2)

        file.write("\n" + linea)

        print('soy arco entre paraderos', a[4], a[5])

        pl.plot(x_1, y_1, 'ob')
        pl.plot(x_2, y_2, 'ob')
        pl.plot([x_1, x_2], [y_1, y_2], 'red')


    #si es un arco de subida
    elif a[4] in paraderos_coord_dic and a[5] not in paraderos_coord_dic:

        paraderos_serv[a[4]] = float(paraderos_serv[a[4]]) + 30

        x_1 = float(paraderos_coord_dic[a[4]][0])
        y_1 = float(paraderos_coord_dic[a[4]][1])

        x_2 = x_1 + float(paraderos_serv[a[4]])
        y_2 = y_1 + float(paraderos_serv[a[4]])

        paraderos_serv_y[a[5]] = y_2
        paraderos_serv_x[a[5]] = x_2

        id = contador
        tipoarco = 'soy arco de subida'

        linea = "{}|{}|LINESTRING({} {},{} {})".format(id, tipoarco, x_1, y_1, x_2, y_2)

        file.write("\n" + linea)

        print('soy arco de subida', a[4], x_1, y_1, a[5], x_2, y_2)

        pl.plot(x_1, y_1, 'ob')
        #pl.plot(x_2, y_2, 'p')
        pl.plot([x_1, x_2], [y_1, y_2], 'grey')

    #si es un arco de linea
    elif a[4] not in paraderos_coord_dic and a[5] not in paraderos_coord_dic:

        par1 = a[4].split("/")[0]
        par2 = a[5].split("/")[0]

        paraderos_serv[a[4]] = float(paraderos_serv[a[4]]) + 30

        y_1 = float(paraderos_serv_y[a[4]])
        x_1 = float(paraderos_serv_x[a[4]])

        x_2 = float(paraderos_serv_x[a[5]])
        y_2 = float(paraderos_serv_y[a[5]])

        id = contador
        tipoarco = 'soy arco de linea'

        linea = "{}|{}|LINESTRING({} {},{} {})".format(id, tipoarco, x_1, y_1, x_2, y_2)

        print('soy arco de linea', a[4], par1,  x_1, y_1, a[5], par2, x_2, y_2)

        #pl.plot(x_1, y_1, 'p')
        #pl.plot(x_2, y_2, 'p')
        pl.plot([x_1, x_2], [y_1, y_2], 'green')





    print (a)
file.close()
pl.show()



'''