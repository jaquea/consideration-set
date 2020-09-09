import pickle

import dill
from igraph import *

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

dump_file2 = open('../tmp/viajes_procesados.pkl', 'rb')
viajes = dill.load(dump_file2)
dump_file2.close()

print(dict_tiempos['L4V-R']['M-RG'])
print(dict_tiempos['L4V-R']['M-TB'])
print(viajes['E-13-54-SN-5'])


#hiperruta_minimo_p = defaultdict(lambda: defaultdict (list))
#hiperruta_minimo_p['L-13-63-40-PO']['T-20-188-SN-54']=hiperruta_minimo['L-13-63-40-PO']['T-20-188-SN-54']
#hiperruta_minimo = defaultdict(lambda: defaultdict (list))
#hiperruta_minimo=hiperruta_minimo_p

alternativas_ele_hip = defaultdict(list)

cont = 0
for d in viajes:
    cont += 1
    #print(o, cont)
    for o in viajes[d]:
        for c in viajes[d][o]:
            #tiempo de viaje en bus
            lista = c.split('/')
            print(c)

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

