from igraph import *
from HeapBinaria import HeapBinaria
import pickle
import dill
import pandas as pd
import random
import utm
import matplotlib.pyplot as pl
import time
import csv
import pandas as pd
import json

with open('C:\Users\jacke\Desktop\info_servicios.json') as data_file:
    data = json.loads(data_file.read())

df = pd.DataFrame.from_dict(data, orient='columns')

df= df[(df['servicio']=='L5-R')]

for idx, row in df.iterrows():
    frec_nom = row['frec_nom']/60
    paradas = row['paradas'] #lista
    sentido = row['sentido']
    servicio = str(row['servicio'])
    servicio_user = row['servicio_user']
    t_ADATRAP = row['t_ADATRAP'] #lista
    t_GTFS = row['t_GTFS'] #lista
    vertice_anterior = ''

    print('ver',paradas, frec_nom, t_ADATRAP, t_GTFS)



dump_file3 = open('hiperruta_minimo.pkl', 'rb')
hiperruta_minimo = dill.load(dump_file3)
dump_file3.close()

dump_file1 = open('grafo.igraph', 'rb')
g = pickle.load(dump_file1)
dump_file1.close()

dump_file2 = open('tiempos.pkl', 'rb')
dict_tiempos = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('paradero_cercano_dic.pkl', 'rb')
paradero_cercano_dic = dill.load(dump_file2)
dump_file2.close()

dump_file3 = open('frecuencias.pkl', 'rb')
dict_frecuencia = dill.load(dump_file3)
dump_file3.close()

dump_file3 = open('paraderos_coord_dic.pkl', 'rb')
paraderos_coord_dic = dill.load(dump_file3)
dump_file3.close()

dump_file2 = open('viajes_procesados.pkl', 'rb')
viajes = dill.load(dump_file2)
dump_file2.close()

#print(dict_tiempos['L4V-R']['M-RG'])
#print(dict_tiempos['L4V-R']['M-TB'])

#hiperruta_minimo_p = defaultdict(lambda: defaultdict (list))
#hiperruta_minimo_p['L-13-63-40-PO']['T-20-188-SN-54']=hiperruta_minimo['L-13-63-40-PO']['T-20-188-SN-54']
#hiperruta_minimo = defaultdict(lambda: defaultdict (list))
#hiperruta_minimo=hiperruta_minimo_p

alternativas_ele_hip = defaultdict(list)

cont = 0
for o in hiperruta_minimo:
    cont += 1
    #print(o, cont)
    for d in hiperruta_minimo[o]:
        for c in hiperruta_minimo[o][d]:
            #tiempo de viaje en bus
            lista = c.split('/')
            print(o,d,c)

            tipo_nodo_anterior = ''
            tipo_nodo_anterior_anterior = ''
            tipo_nodo_actual = ''
            nodo_anterior_anterior = ''
            nodo_anterior = ''
            tpo_metro = 0
            tpo_bus = 0
            tpo_caminata_trasbordo = 0
            tpo_espera_inicial = 0
            tpo_espera_trasbordo = 0
            trasbordo_bus_metro = 0
            trasbordo_bus_bus = 0
            trasbordo_metro_bus = 0
            modo_anterior = ''
            modo_actual = ''

            for n in lista:
                # si el nodo es un paradero
                if n in g.vs['name2'] and (g.vs["tipo"][g.vs.find(name2=n).index]) == 'paradero':
                    tipo_nodo_actual = 'paradero'
                    #print('paradero')

                #si el nodo es un servicio
                else:
                    tipo_nodo_actual = 'servicio'
                    #print('servicio')

                    #trasbordo a metro
                    if nodo_anterior[:2] == 'M-':
                        modo_actual = 'metro'

                        if modo_anterior == 'bus':
                            trasbordo_bus_metro += 1

                    #trasbordo a bus
                    else:
                        modo_actual = 'bus'

                        if modo_anterior == 'bus':
                            trasbordo_bus_bus += 1

                        if modo_anterior == 'metro':
                            trasbordo_metro_bus += 1



                #tiempo de viaje en vehiculo
                #si el arco es de tipo paradero-servicio-paradero
                if tipo_nodo_actual == tipo_nodo_anterior_anterior and tipo_nodo_anterior=='servicio' and tipo_nodo_actual =='paradero':

                    #si es arco en metro
                    if n[:2] == 'M-' and nodo_anterior_anterior[:2] == 'M-':
                        n_destino = g.vs.find(name2=n).index
                        n_origen = g.vs.find(name2=nodo_anterior_anterior).index

                        #calcular tiempo de espera y tiempo de viaje en metro
                        str1 = nodo_anterior + 'V-I'
                        str2 = nodo_anterior + 'V-R'
                        str3 = nodo_anterior + 'R-I'
                        str4 = nodo_anterior + 'R-R'
                        str5 = nodo_anterior + '-I'
                        str6 = nodo_anterior + '-R'

                        servicios = [str1, str2, str3, str4, str5, str6]

                        frecuencia = 0
                        contador = 0

                        print(servicios)

                        for str in servicios:
                            print(str, n, nodo_anterior_anterior)
                            if str in dict_tiempos:
                                dif = dict_tiempos[str][n] - dict_tiempos[str][nodo_anterior_anterior]
                                print(dif, dict_tiempos[str][n], dict_tiempos[str][nodo_anterior_anterior])
                                if dif > 0 and dict_tiempos[str][n]>-1 and dict_tiempos[str][nodo_anterior_anterior]>-1:
                                    print('frecuencia',str,nodo_anterior_anterior, dict_frecuencia[str][nodo_anterior_anterior])
                                    frecuencia += dict_frecuencia[str][nodo_anterior_anterior]
                                    contador += 1
                        tpo_espera = contador/frecuencia
                        #print('tpo_viaje',g.shortest_paths_dijkstra(source=n_origen, target=n_destino, weights=g.es["peso"], mode=OUT)[0][0])
                        tpo_viaje = g.shortest_paths_dijkstra(source=n_origen, target=n_destino, weights=g.es["peso"], mode=OUT)[0][0] - tpo_espera
                        tpo_metro += tpo_viaje

                        if tpo_espera_inicial == 0:
                            tpo_espera_inicial += tpo_espera

                        else:
                            tpo_espera_trasbordo += tpo_espera

                    #si es arco en bus
                    else:
                        tpo_bus += (dict_tiempos[nodo_anterior][n] - dict_tiempos[nodo_anterior][nodo_anterior_anterior])
                        tpo_espera = 1/dict_frecuencia[nodo_anterior][nodo_anterior_anterior]

                        if tpo_espera_inicial == 0:
                            tpo_espera_inicial += tpo_espera

                        else:
                            tpo_espera_trasbordo += tpo_espera

                #tiempo de caminata en trasbordo
                #si el arco es de tipo paradero-paradero
                if tipo_nodo_actual == tipo_nodo_anterior and tipo_nodo_actual == 'paradero':
                    x1 = float(paraderos_coord_dic[n][0])
                    y1 = float(paraderos_coord_dic[n][1])

                    x2 = float(paraderos_coord_dic[nodo_anterior][0])
                    y2 = float(paraderos_coord_dic[nodo_anterior][1])

                    dist = abs(x1 - x2) + abs(y1 - y2)

                    tpo_caminata_trasbordo += (dist * 60 / (1000 * 4))

                tipo_nodo_anterior_anterior = tipo_nodo_anterior
                tipo_nodo_anterior = tipo_nodo_actual

                nodo_anterior_anterior = nodo_anterior
                nodo_anterior = n

                modo_anterior = modo_actual

            #print('tpo_metro',tpo_metro, 'tpo_bus', tpo_bus, 'tpo_caminata_trasbordo', tpo_caminata_trasbordo, 'tpo_espera_inicial', tpo_espera_inicial, 'tpo_espera_trasbordo',
             #     tpo_espera_trasbordo, 'trasbordo_bus_metro', trasbordo_bus_metro, 'trasbordo_bus_bus', trasbordo_bus_bus, 'trasbordo_metro_bus', trasbordo_metro_bus)

            alternativas_ele_hip[c]=[1, c, viajes[d][o][c], tpo_metro, tpo_bus, tpo_caminata_trasbordo, tpo_espera_inicial, tpo_espera_trasbordo, trasbordo_bus_metro, trasbordo_bus_bus, trasbordo_metro_bus]


#print(dict_tiempos['T405 00I']['E-20-53-PO-95'])
#print(dict_tiempos['T405 00I']['T-14-128-PO-20'])

#print('hiper-ruta')
#print(hiperruta_minimo['E-20-53-PO-95']['T-14-110-PO-10'])

#calcular el maximo numero de alternativa maxima
cant_max_alternativas = 0
for o in hiperruta_minimo:
    for d in hiperruta_minimo[o]:
        largo = len(hiperruta_minimo[o][d])

        if largo > cant_max_alternativas:
            cant_max_alternativas = largo

print('cant_max_alternativas',cant_max_alternativas)

# se demora 58 minutos
start = time.time()

posicion = 0
resultado = pd.DataFrame()

while posicion <= (cant_max_alternativas-1):

    lista = []
    #print('iteracion')

    for o in hiperruta_minimo:
        for d in hiperruta_minimo[o]:
            #print(hiperruta_minimo[o][d])
            #si hay mas caminos que el marcador posicion se agrega c, el camino
            if len (hiperruta_minimo[o][d]) > posicion:
                c = hiperruta_minimo[o][d][posicion]
                lista.append(alternativas_ele_hip[c])
            else:
                c = 0
                lista.append([0,c, 0,0, 0, 0, 0, 0, 0, 0, 0])

    cont = posicion+1

    #print(unicode(cont))

    headers = [''.join(['AVAIL', unicode(cont)]), ''.join(['CAMINO', unicode(cont)]), ''.join(['VIAJES', unicode(cont)]), ''.join(['TPOMETRO', unicode(cont)]), ''.join(['TPOBUS', unicode(cont)]), ''.join(['TPOCAM', unicode(cont)]),
               ''.join(['TESPINC', unicode(cont)]),  ''.join(['TESPINT', unicode(cont)]), ''.join(['BUS_METRO', unicode(cont)]), ''.join(['BUS_BUS', unicode(cont)]), ''.join(['METRO_BUS', unicode(cont)])]

    dataframe = pd.DataFrame(lista, columns=headers)
    resultado = pd.concat([resultado, dataframe],  axis=1, sort=False)
    posicion += 1

#Agrego los atributos de origen y destino
lista = []
for o in hiperruta_minimo:
    for d in hiperruta_minimo[o]:
        viajes_totales = sum([viajes[d][o][camino] for camino in viajes[d][o]])
        viajes_en_hiperruta = sum([viajes[d][o][camino] for camino in hiperruta_minimo[o][d]])
        lista.append([o, d, viajes_totales, viajes_en_hiperruta])


dataframe = pd.DataFrame(lista, columns = ['ORIGEN', 'DESTINO', 'viajes_totales', 'viajes_en_hiperruta'])
resultado = pd.concat([resultado, dataframe],  axis=1, sort=False)

#resultado.to_csv("resultado.csv", encoding='utf-8', index=False, sep=',')

print('{0} seconds'.format(time.time() - start))

print('cant_max_alternativas',cant_max_alternativas)

#Multiplicamos filas en base al numero de viajes, ya que en R la libreria lee el vector por cada viaje desagregado
#resultado = resultado.head(2)
new_df = resultado.loc[resultado.index.repeat(resultado['VIAJES1'] + resultado['VIAJES2'] + resultado['VIAJES3'] + resultado['VIAJES4'] +
                                              resultado['VIAJES5'] + resultado['VIAJES6'] + resultado['VIAJES7'] + resultado['VIAJES8'] +
                                              resultado['VIAJES9'])].reset_index(drop=True)
#new_df = new_df.loc[new_df.index.repeat(new_df['VIAJES2'])].assign(CHOICE2=1).reset_index(drop=True)

new_df.to_csv("new_df0.csv", encoding='utf-8', index=False, sep=',')

contador = 0

new_df['CHOICE1'] = 0
new_df['CHOICE2'] = 0
new_df['CHOICE3'] = 0
new_df['CHOICE4'] = 0
new_df['CHOICE5'] = 0
new_df['CHOICE6'] = 0
new_df['CHOICE7'] = 0
new_df['CHOICE8'] = 0
new_df['CHOICE9'] = 0

for index, row in resultado.iterrows():
    viajes1 = row['VIAJES1']
    viajes2 = row['VIAJES2']
    viajes3 = row['VIAJES3']
    viajes4 = row['VIAJES4']
    viajes5 = row['VIAJES5']
    viajes6 = row['VIAJES6']
    viajes7 = row['VIAJES7']
    viajes8 = row['VIAJES8']
    viajes9 = row['VIAJES9']


    lista_viajes = [viajes1, viajes2, viajes3, viajes4, viajes5, viajes6, viajes7, viajes8, viajes9]

    print(lista_viajes)

    choice = 1
    for l in lista_viajes:
        cont = choice
        choice += 1
        for i in range(l):
            new_df.at[i + contador, ''.join(['CHOICE', unicode(cont)])] = 1

            print(i+contador, cont)

        contador += l

#resultado.to_csv("resultado.csv", encoding='utf-8', index=False, sep=',')
new_df.to_csv("new_df1.csv", encoding='utf-8', index=False, sep=',')