import pickle
import time

import dill
from igraph import *
from collections import defaultdict

from HeapBinaria import HeapBinaria



start_time = time.time()

heap = HeapBinaria()

alfa = 2 #penalizacion tiempo espera
caminata = 7

dump_file2 = open('tiempos.pkl', 'rb')
dict_tiempos = dill.load(dump_file2)
dump_file2.close()

dump_file3 = open('frecuencias.pkl', 'rb')
dict_frecuencia = dill.load(dump_file3)
dump_file3.close()

dump_file2 = open('viajes_procesados.pkl', 'rb')
viajes = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('paradero_cercano_dic.pkl', 'rb')
paradero_cercano_dic = dill.load(dump_file2)
dump_file2.close()

print(len(viajes))

viajes_p = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:0)))

#viajes_p['T-13-54-SN-70']['M-TB'] = viajes['T-13-54-SN-70']['M-TB'] #
viajes_p['T-8-71-PO-33']['T-20-68-NS-5'] = viajes['T-8-71-PO-33']['T-20-68-NS-5']
viajes_p['T-8-71-PO-33']['T-20-68-NS-5'] = viajes['T-8-71-PO-33']['T-20-68-NS-5']

viajes = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:0)))

viajes=viajes_p


print('genere los viajes')

#dump_file = open('paraderos_coord_dic', 'rb')
#paraderos_coord_dic = pickle.load(dump_file)
#dump_file.close()
def hyperpath (g, destino):
    conj_paradero = defaultdict(list)
    conj_paradero_inf = defaultdict(list)
    # inicializacion
    #inicializacion del algoritmo
    for i in range(0,len(g.vs)):
        g.vs[i]["tau"]=float('inf')
        g.vs[i]["tau_inf"] = float('inf')
        g.vs[i]["frecuencia"] = 0

    n_destino = g.vs.find(name2=destino).index

    g.vs[n_destino]["tau"] = 0
    g.vs[n_destino]["tau_inf"] = 0

    S = []

    nodo_seleccionado = (n_destino, 0)

    while len(S) < len(g.vs) + 1 and nodo_seleccionado != None:

        a = nodo_seleccionado[0]

        for j in g.neighborhood(a, order=1, mode=IN)[1:]:

            desde= j

            #print(g.vs[j]['name2'], g.vs[a]['name2'])
            #print(g.vs[desde]["tipo"], g.vs[a]["tipo"])

            if a not in S:

                #tiempo del arco evaluado
                tpo_arco = g.es[g.get_eid(desde,a,directed=True, error=True)]['tpo_viaje']

                #tiempo que hay desde la cola del arco hacia el destino
                tpo_nodo_a = min(g.vs[a]["tau"], g.vs[a]["tau_inf"])

                t_colita = tpo_arco + tpo_nodo_a
                t_colita_copia = t_colita
                #t_colita = g.es[g.get_eid(desde, a, directed=True, error=True)]['peso'] + min(g.vs[a]["tau"], g.vs[a]["tau"])

                #si se baja de un servicio a un paradero
                if g.vs[a]["tipo"] == 'paradero' and g.vs[desde]["tipo"] == 'servicio':

                    t_colita = t_colita + caminata

                    #if a != n_destino:
                        #t_colita = t_colita + caminata

                    #else:
                        #t_colita = tpo_nodo_a

                if g.vs[a]["tipo"] == 'paradero' and g.vs[desde]["tipo"] == 'paradero' and a == n_destino:

                    t_colita = tpo_nodo_a

                #print('t_colita', t_colita)

                #frecuencia del arco, al inicio toma valor cero
                frec_arco = g.es[g.get_eid(desde, a, directed=True, error=True)]['frecuencia']

                #si es arco sin tiempo de espera
                if frec_arco == float('inf') and t_colita < g.vs[desde]["tau_inf"]:

                    g.vs[desde]["tau_inf"] = t_colita
                    #copia.vs[desde]["tau_inf"] = t_colita_copia

                    #conj_paradero_inf[desde]=[((desde, a),  t_colita, copia.vs[desde]["tau_inf"], copia.vs[desde]["frecuencia"])]

                    conj_paradero_inf[desde] = [((desde, a), t_colita)]

                    heap.insertar((desde, t_colita))

                #si es arco con espera
                if frec_arco < float('inf') and t_colita < g.vs[desde]["tau"]:

                    if ((g.vs[desde]["frecuencia"])==0 and (g.vs[desde]["tau"])==float('inf')):

                        g.vs[desde]["tau"] = (alfa + frec_arco * t_colita) / float(((g.vs[desde]["frecuencia"]) + frec_arco))
                        #copia.vs[desde]["tau"] = (1 + frec_arco * t_colita_copia) / float(((copia.vs[desde]["frecuencia"]) + frec_arco))

                    else:
                        g.vs[desde]["tau"] = ((g.vs[desde]["frecuencia"]) * (g.vs[desde]["tau"]) + frec_arco * t_colita) / ((g.vs[desde]["frecuencia"]) + frec_arco)
                        #copia.vs[desde]["tau"] = ((copia.vs[desde]["frecuencia"]) * (copia.vs[desde]["tau"]) + frec_arco * t_colita_copia) / ((copia.vs[desde]["frecuencia"]) + frec_arco)

                    g.vs[desde]["frecuencia"] = ((g.vs[desde]["frecuencia"])+ frec_arco)
                    #copia.vs[desde]["frecuencia"] = ((copia.vs[desde]["frecuencia"]) + frec_arco)

                    conj_paradero[desde].append(((desde, a), t_colita_copia))

                    heap.insertar((desde, g.vs[desde]["tau"]))

                    #print('nodo', g.vs[desde]["name"], 'tau:', g.vs[desde]["tau"], 't_colita:', t_colita)

                    for elemento in conj_paradero[desde]:

                        #print("hola",desde, conj_paradero[desde])

                        if elemento[1]> g.vs[desde]["tau"]:

                            #print('elemento removido', elemento)

                            conj_paradero[desde].remove(elemento)

                            frecuencia_arco = g.es[g.get_eid(elemento[0][0],elemento[0][1],directed=True, error=True)]['frecuencia']
                            frecuencia_nodo = g.vs[elemento[0][0]]["frecuencia"]
                            tau_nodo = g.vs[elemento[0][0]]["tau"]
                            tarco_colita = elemento[1]

                            g.vs[desde]["tau"] = (frecuencia_nodo*tau_nodo - frecuencia_arco*tarco_colita)/(frecuencia_nodo-frecuencia_arco)

                            #frecuencia_arco = copia.es[copia.get_eid(elemento[0][0], elemento[0][1], directed=True, error=True)]['frecuencia']
                            #frecuencia_nodo = copia.vs[elemento[0][0]]["frecuencia"]
                            #tau_nodo = copia.vs[elemento[0][0]]["tau"]
                            #tarco_colita = elemento[1]

                            #copia.vs[desde]["tau"] = (frecuencia_nodo * tau_nodo - frecuencia_arco * tarco_colita) / ( frecuencia_nodo - frecuencia_arco)

            #print('nodo_seleccionado_pre', 'name:', g.vs[j]["name"], 'frecuencia:', g.vs[j]['frecuencia'], "tau:", g.vs[j]["tau"], "tau_inf:", g.vs[j]["tau_inf"])
        nodo_seleccionado = heap.extraer()
        #print('nodo_seleccionado', nodo_seleccionado)

        if a not in S:
            S.append(a)


    arcos=[]
    nodos=[]
    arcos_grafico=[]

    lista_peso=[]
    lista_frecuencia=[]
    lista_tpo_viaje=[]

    for nodo in conj_paradero_inf:

        for elemento in conj_paradero_inf[nodo]:

            if nodo in conj_paradero:

                tpo_sin_frecuencia = g.vs[nodo]["tau_inf"] #no hay tiempo de espera
                tpo_con_frecuencia = g.vs[nodo]["tau"] #hay tiempo de espera

                #print ('nodo', i, g.vs[i]["tau"], g.vs[i]["tau_inf"], g.vs[i]["frecuencia"])

                if tpo_sin_frecuencia <= tpo_con_frecuencia:

                    nodo1 = elemento[0][0]
                    nodo2 = elemento[0][1]
                    #print('es sin frecuencia', nodo1, nodo2, g.vs["name"][nodo1], g.vs["name"][nodo2], g.vs["tipo"][nodo1],g.vs["tipo"][nodo2])
                    arcos_grafico.append((str(nodo1), str(nodo2),g.vs["name2"][nodo1],g.vs["name2"][nodo2]))
                    arcos.append((str(nodo1), str(nodo2)))

                    lista_peso.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['peso'])
                    lista_frecuencia.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['frecuencia'])
                    lista_tpo_viaje.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['tpo_viaje'])

                    if (nodo1, g.vs["tipo"][nodo1],g.vs["name2"][nodo1]) not in nodos:
                        nodos.append((nodo1, g.vs["tipo"][nodo1],g.vs["name2"][nodo1]))

                    if (nodo2, g.vs["tipo"][nodo2], g.vs["name2"][nodo2]) not in nodos:
                        nodos.append((nodo2, g.vs["tipo"][nodo2], g.vs["name2"][nodo2]))

            else:

                nodo1 = elemento[0][0]
                nodo2 = elemento[0][1]
                # print('es sin frecuencia', nodo1, nodo2, g.vs["name"][nodo1], g.vs["name"][nodo2], g.vs["tipo"][nodo1],g.vs["tipo"][nodo2])
                arcos.append((str(nodo1), str(nodo2)))

                arcos_grafico.append((str(nodo1), str(nodo2), g.vs["name2"][nodo1], g.vs["name2"][nodo2]))

                lista_peso.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['peso'])
                lista_frecuencia.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['frecuencia'])
                lista_tpo_viaje.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['tpo_viaje'])

                if (nodo1, g.vs["tipo"][nodo1], g.vs["name2"][nodo1]) not in nodos:
                    nodos.append((nodo1, g.vs["tipo"][nodo1], g.vs["name2"][nodo1]))

                if (nodo2, g.vs["tipo"][nodo2], g.vs["name2"][nodo2]) not in nodos:
                    nodos.append((nodo2, g.vs["tipo"][nodo2], g.vs["name2"][nodo2]))

    for nodo in conj_paradero:

        for elemento in conj_paradero[nodo]:

            if nodo in conj_paradero_inf:

                tpo_sin_frecuencia = g.vs[nodo]["tau_inf"]  # no hay tiempo de espera
                tpo_con_frecuencia = g.vs[nodo]["tau"]  # hay tiempo de espera

                # print ('nodo', i, g.vs[i]["tau"], g.vs[i]["tau_inf"], g.vs[i]["frecuencia"])

                if tpo_sin_frecuencia > tpo_con_frecuencia:

                    nodo1 = elemento[0][0]
                    nodo2 = elemento[0][1]
                    # print('es sin frecuencia', nodo1, nodo2, g.vs["name"][nodo1], g.vs["name"][nodo2], g.vs["tipo"][nodo1],g.vs["tipo"][nodo2])
                    arcos.append((str(nodo1), str(nodo2)))
                    lista_peso.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['peso'])
                    lista_frecuencia.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['frecuencia'])
                    lista_tpo_viaje.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['tpo_viaje'])
                    arcos_grafico.append((str(nodo1), str(nodo2), g.vs["name2"][nodo1], g.vs["name2"][nodo2]))

                    if (nodo1, g.vs["tipo"][nodo1], g.vs["name2"][nodo1]) not in nodos:
                        nodos.append((nodo1, g.vs["tipo"][nodo1], g.vs["name2"][nodo1]))

                    if (nodo2, g.vs["tipo"][nodo2], g.vs["name2"][nodo2]) not in nodos:
                        nodos.append((nodo2, g.vs["tipo"][nodo2], g.vs["name2"][nodo2]))

            else:

                nodo1 = elemento[0][0]
                nodo2 = elemento[0][1]
                # print('es sin frecuencia', nodo1, nodo2, g.vs["name"][nodo1], g.vs["name"][nodo2], g.vs["tipo"][nodo1],g.vs["tipo"][nodo2])
                arcos.append((str(nodo1), str(nodo2)))
                lista_peso.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['peso'])
                lista_frecuencia.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['frecuencia'])
                lista_tpo_viaje.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['tpo_viaje'])
                arcos_grafico.append((str(nodo1), str(nodo2), g.vs["name2"][nodo1], g.vs["name2"][nodo2]))

                if (nodo1, g.vs["tipo"][nodo1], g.vs["name2"][nodo1]) not in nodos:
                    nodos.append((nodo1, g.vs["tipo"][nodo1], g.vs["name2"][nodo1]))

                if (nodo2, g.vs["tipo"][nodo2], g.vs["name2"][nodo2]) not in nodos:
                    nodos.append((nodo2, g.vs["tipo"][nodo2], g.vs["name2"][nodo2]))


    q = Graph(directed=True)

    for v in nodos:
        #print(v[0])
        q.add_vertex(name=str(v[0]), tipo= v[1], name2= v[2])
    q.add_edges(arcos)
    q.es["peso"]=lista_peso
    return q

'''
dump_file1 = open('grafo.igraph', 'rb')
g = pickle.load(dump_file1)
dump_file1.close()
#q = hyperpath(g, 'T-14-110-PO-10')
'''
def find_all_paths(graph, start, end, mode = 'OUT', maxlen = None):
    def find_all_paths_aux(adjlist, start, end, path, maxlen = None):
        path = path + [start]
        if start == end:
            return [path]
        paths = []
        if maxlen is None or len(path) <= maxlen:
            for node in adjlist[start] - set(path):
                paths.extend(find_all_paths_aux(adjlist, node, end, path, maxlen))
        return paths
    adjlist = [set(graph.neighbors(node, mode = mode))for node in xrange(graph.vcount())]
    all_paths = []
    start = start if type(start) is list else [start]
    end = end if type(end) is list else [end]
    for s in start:
        for e in end:
            all_paths.extend(find_all_paths_aux(adjlist, s, e, [], maxlen))
    return all_paths

print('pase las funciones')
'''
caminos = find_all_paths(q, q.vs.find(name2='E-20-53-PO-95').index, q.vs.find(name2='T-14-110-PO-10').index, mode='OUT', maxlen=None)

for j in caminos:
    print('camino')
    for i in j:
        print(i, q.vs[i]['name2'])

print('FIN')
'''

Dict_caminos = defaultdict(lambda: defaultdict (lambda: defaultdict (list)))
hiperruta_minimo = defaultdict(lambda: defaultdict (list))
itinerario_minimo = defaultdict(lambda: defaultdict(list))
ruta_minima = defaultdict(lambda: defaultdict (list))
camino_minimo = defaultdict(lambda: defaultdict(list))
servicios_dict = defaultdict(lambda: defaultdict (lambda: defaultdict (list)))
Dict_caminos_etapa = defaultdict(lambda: defaultdict (lambda: defaultdict (lambda: defaultdict (list))))

hiperruta_proporcion = defaultdict(lambda: defaultdict (lambda: defaultdict (float)))
itinerario_minimo_proporcion = defaultdict(lambda: defaultdict (lambda: defaultdict (float)))
ruta_minima_proporcion = defaultdict(lambda: defaultdict (lambda: defaultdict (float)))

dump_file1 = open('grafo.igraph', 'rb')
g = pickle.load(dump_file1)
dump_file1.close()

cont = 0
for destino in viajes:
    cont += 1
    print(destino, cont)

    # cargar grafo desde archivo

    q = hyperpath(g, destino)

    hyperpath_obj = Hyperpath(g, destination=destino, transfer_penalty=16,
                              waiting_penalty=2)

    destination_index = hyperpath_obj._hyperpath.vs.find(name2=destino).index

    for ori in viajes[destino]:

        tpo_mas_corto = 1000

        for origen in paradero_cercano_dic[ori]:
            print(origen)
            if origen not in q.vs["name2"]:
                continue

            origin_index = hyperpath_obj._hyperpath.vs.find(name2=origen).index
            path_set = hyperpath_obj.find_all_paths(origin_index, destination_index, maxlen=None, mode='OUT')
            format_path = hyperpath_obj.format_paths(path_set)

            n_origen = q.vs.find(name2=origen).index
            caminos = find_all_paths(q, n_origen, n_destino, mode='OUT', maxlen=None)

            for j in caminos:
                prob_camino = 1
                camino = ''
                camino_paradero = ''
                metro_inicial = ''
                metro_final = ''
                serv_metro = ''
                n_iteracion = 0
                tipo_nodo_anterior = ''
                tipo_nodo_actual = ''
                ultimo_nodo = j[-1]
                nodo_anterior = ''

                print('camino nuevo')

                for n in j:

                    #print(camino)

                    #print(n, q.vs[n]['name2'],g.vs["tipo"][g.vs.find(name2=q.vs[n]['name2']).index])

                    n_iteracion += 1

                    #si el nodo es un paradero
                    if (g.vs["tipo"][g.vs.find(name2=q.vs[n]['name2']).index]) == 'paradero':

                        tipo_nodo_actual = 'paradero'

                        frecuencia_total = g.vs[g.vs.find(name2=q.vs[n]['name2']).index]["frecuencia"]
                        nombre_nodo = q.vs[n]['name2']

                        # si el camino esta vacio agrego el primer nodo al string camino
                        if camino == '':
                            #print('entre 1')
                            camino = nombre_nodo
                            camino_paradero = nombre_nodo
                            if nombre_nodo[:2] == 'M-':
                                metro_inicial = nombre_nodo

                        # si el camino esta vacio agrego el primer nodo al string camino
                        elif (n_iteracion == 2 and tipo_nodo_actual == tipo_nodo_anterior):
                            #print('entre 2')
                            camino = nombre_nodo
                            camino_paradero = nombre_nodo
                            metro_inicial = ''
                            if nombre_nodo[:2] == 'M-':
                                metro_inicial = nombre_nodo

                        #si es el ultimo nodo
                        elif (n == ultimo_nodo or q.vs[ultimo_nodo]['name2']==q.vs[n]['name2']):
                            #print('entre 3')

                            #si el nodo anterior es igual al nodo actual
                            if  tipo_nodo_anterior == tipo_nodo_actual:

                                if metro_final != '':
                                    serv_metro = serv_metro.replace('V', '')
                                    serv_metro = serv_metro.replace('R', '')
                                    serv_metro = serv_metro.replace('-', '')
                                    serv_metro = serv_metro.replace('I', '')

                                    camino = camino + '/' + serv_metro + '/' + metro_final
                                    camino_paradero = camino_paradero + '/' + metro_final

                                    metro_final = ''
                                    metro_inicial = ''
                                    serv_metro = ''

                                continue
                            # si el nodo anterior es distinto al nodo actual
                            else:
                                #print('entre 4')
                                #si es metro
                                if nombre_nodo[:2] == 'M-' and metro_inicial != '':
                                    #print('entre 5')
                                    metro_final = nombre_nodo
                                    serv_metro = serv_metro.replace('V', '')
                                    serv_metro = serv_metro.replace('R', '')
                                    serv_metro = serv_metro.replace('-', '')
                                    serv_metro = serv_metro.replace('I', '')

                                    camino = camino + '/' + serv_metro + '/' + metro_final
                                    camino_paradero = camino_paradero + '/' + metro_final

                                    metro_final = ''
                                    metro_inicial = ''
                                    serv_metro = ''
                                #si es bus
                                else:
                                    camino = camino + '/' + nombre_nodo
                                    camino_paradero = camino_paradero + '/' + nombre_nodo
                        #si es un nodo intermedio
                        else:
                            #si es metro
                            #print('entre donde debo entrar')
                            if nombre_nodo[:2] == 'M-' and metro_inicial == '':
                                metro_inicial = nombre_nodo

                                camino = camino + '/' + nombre_nodo
                                camino_paradero = camino_paradero + '/' + nombre_nodo

                            elif nombre_nodo[:2] == 'M-' and metro_inicial != '':
                                metro_final = nombre_nodo
                                serv_metro = serv_metro.replace('V', '')
                                serv_metro = serv_metro.replace('R', '')
                                serv_metro = serv_metro.replace('-', '')
                                serv_metro = serv_metro.replace('I', '')

                                camino = camino + '/' + serv_metro + '/' + metro_final
                                camino_paradero = camino_paradero + '/' + metro_final

                                metro_inicial = metro_final
                                metro_final = ''
                                serv_metro = ''

                            # si no es metro
                            else:
                                if metro_final != '':
                                    serv_metro = serv_metro.replace('V', '')
                                    serv_metro = serv_metro.replace('R', '')
                                    serv_metro = serv_metro.replace('-', '')
                                    serv_metro = serv_metro.replace('I', '')

                                    camino = camino + '/' + serv_metro + '/' + metro_final
                                    camino_paradero = camino_paradero + '/' + metro_final

                                    metro_final = ''
                                    metro_inicial = ''
                                    serv_metro = ''

                                camino = camino + '/' + nombre_nodo
                                camino_paradero = camino_paradero + '/' + nombre_nodo

                    #si el nodo no es un paradero (posee paradero/servicio)
                    else:

                        tipo_nodo_actual = 'servicio'
                        frecuencia_arco = g.es[g.get_eid(g.vs.find(name2=nodo_anterior).index, g.vs.find(name2=q.vs[n]['name2']).index,directed=True, error=True)]['frecuencia']

                        if frecuencia_arco < float('inf') and metro_inicial == '':
                            prob_arco = frecuencia_arco / frecuencia_total
                            prob_camino = prob_camino * prob_arco
                            servicio = q.vs[n]['name2'].split("/")[1]
                            camino = camino + '/' + servicio

                        if metro_inicial != '' and metro_final == '':
                            servicio = q.vs[n]['name2'].split("/")[1]
                            serv_metro = servicio
                            serv_metro = serv_metro.replace('V', '')
                            serv_metro = serv_metro.replace('R', '')
                            serv_metro = serv_metro.replace('-', '')
                            serv_metro = serv_metro.replace('I', '')

                        #print('aqui_estoy',nodo_anterior, q.vs[n]['name2'], frecuencia_arco, prob_camino)

                    #print(q.vs[n]['name2'], tipo_nodo_actual)


                    if tipo_nodo_actual == 'paradero' and tipo_nodo_anterior=='servicio':
                        #print(nodo_anterior.split("/"), len(nodo_anterior.split("/")))

                        if len(nodo_anterior.split("/"))>1:
                            if nodo_anterior.split("/")[1] not in Dict_caminos_etapa[ori][destino][paradero_anterior][q.vs[n]['name2']]:
                                Dict_caminos_etapa[ori][destino][paradero_anterior][q.vs[n]['name2']].append(nodo_anterior.split("/")[1])

                    #print(Dict_caminos_etapa)

                    if tipo_nodo_actual == 'paradero':
                        paradero_anterior = q.vs[n]['name2']

                    nodo_anterior = q.vs[n]['name2']

                    tipo_nodo_anterior = tipo_nodo_actual

                    #print(camino)

                print('camino',camino)

                # diccionario que contiene como llaves el origen destino y el camino como secuecia de paradero y el elemento es el camino con los servicios
                if camino not in Dict_caminos[ori][destino][camino_paradero]:
                    Dict_caminos[ori][destino][camino_paradero].append(camino)
                    hiperruta_minimo[ori][destino].append(camino)

                if camino not in hiperruta_proporcion[ori][destino]:
                    hiperruta_proporcion[ori][destino][camino]= prob_camino

                print('hiper-ruta',hiperruta_minimo[ori][destino])

            path = q.get_all_shortest_paths(n_origen, to=n_destino, weights=q.es["peso"], mode=OUT)
            tpo_camino = q.shortest_paths_dijkstra(source=n_origen, target=n_destino, weights=q.es["peso"], mode=OUT)[0][0]

            if (tpo_camino < tpo_mas_corto):
                camino_minimo[ori][destino] = path
                tpo_mas_corto = tpo_camino

            elif (tpo_camino == tpo_mas_corto):
                for j in path:
                    camino_minimo[ori][destino].append(j)

        for j in camino_minimo[ori][destino]:
            camino = ''
            camino_paradero = ''
            metro_inicial = ''
            metro_final = ''
            serv_metro = ''
            n_iteracion = 0
            tipo_nodo_anterior = ''
            tipo_nodo_actual = ''
            ultimo_nodo = j[-1]

            for n in j:
                n_iteracion += 1

                if (g.vs["tipo"][g.vs.find(name2=q.vs[n]['name2']).index]) == 'paradero':

                    tipo_nodo_actual = 'paradero'
                    nombre_nodo = q.vs[n]['name2']

                    # si el camino esta vacio agrego el primer nodo al string camino
                    if camino == '':
                        camino = nombre_nodo
                        camino_paradero = nombre_nodo
                        if nombre_nodo[:2] == 'M-':
                            metro_inicial = nombre_nodo

                    # si el camino esta vacio agrego el primer nodo al string camino
                    elif (n_iteracion == 2 and tipo_nodo_actual == tipo_nodo_anterior):
                        camino = nombre_nodo
                        camino_paradero = nombre_nodo
                        metro_inicial = ''
                        if nombre_nodo[:2] == 'M-':
                            metro_inicial = nombre_nodo

                    elif (n == ultimo_nodo or q.vs[ultimo_nodo]['name2'] == q.vs[n]['name2']):
                        if tipo_nodo_anterior == tipo_nodo_actual:

                            if metro_final != '':

                                serv_metro = serv_metro.replace('V', '')
                                serv_metro = serv_metro.replace('R', '')
                                serv_metro = serv_metro.replace('-', '')
                                serv_metro = serv_metro.replace('I', '')
                                camino = camino + '/' + serv_metro + '/' + metro_final
                                camino_paradero = camino_paradero + '/' + metro_final
                                metro_final = ''
                                metro_inicial = ''
                                serv_metro = ''

                            continue


                        else:

                            if nombre_nodo[:2] == 'M-' and metro_inicial != '':

                                metro_final = nombre_nodo
                                serv_metro = serv_metro.replace('V', '')
                                serv_metro = serv_metro.replace('R', '')
                                serv_metro = serv_metro.replace('-', '')
                                serv_metro = serv_metro.replace('I', '')
                                camino = camino + '/' + serv_metro + '/' + metro_final
                                camino_paradero = camino_paradero + '/' + metro_final
                                metro_final = ''
                                metro_inicial = ''
                                serv_metro = ''


                            else:

                                camino = camino + '/' + nombre_nodo
                                camino_paradero = camino_paradero + '/' + nombre_nodo

                    else:
                        if nombre_nodo[:2] == 'M-' and metro_inicial == '':
                            metro_inicial = nombre_nodo

                            camino = camino + '/' + nombre_nodo
                            camino_paradero = camino_paradero + '/' + nombre_nodo

                        elif nombre_nodo[:2] == 'M-' and metro_inicial != '':

                            metro_final = nombre_nodo

                            serv_metro = serv_metro.replace('V', '')
                            serv_metro = serv_metro.replace('R', '')
                            serv_metro = serv_metro.replace('-', '')
                            serv_metro = serv_metro.replace('I', '')

                            camino = camino + '/' + serv_metro + '/' + metro_final
                            camino_paradero = camino_paradero + '/' + metro_final

                            metro_inicial = metro_final
                            metro_final = ''
                            serv_metro = ''

                        # si no es metro
                        else:
                            if metro_final != '':
                                serv_metro = serv_metro.replace('V', '')
                                serv_metro = serv_metro.replace('R', '')
                                serv_metro = serv_metro.replace('-', '')
                                serv_metro = serv_metro.replace('I', '')

                                camino = camino + '/' + serv_metro + '/' + metro_final
                                camino_paradero = camino_paradero + '/' + metro_final

                                metro_final = ''
                                metro_inicial = ''
                                serv_metro = ''

                            camino = camino + '/' + nombre_nodo
                            camino_paradero = camino_paradero + '/' + nombre_nodo


                else:

                    tipo_nodo_actual = 'servicio'
                    frecuencia_arco = g.es[g.get_eid(g.vs.find(name2=nodo_anterior).index, g.vs.find(name2=q.vs[n]['name2']).index,
                                  directed=True, error=True)]['frecuencia']

                    if frecuencia_arco < float('inf') and metro_inicial == '':
                        servicio = q.vs[n]['name2'].split("/")[1]
                        camino = camino + '/' + servicio

                    if metro_inicial != '' and metro_final == '':
                        servicio = q.vs[n]['name2'].split("/")[1]
                        serv_metro = servicio

                nodo_anterior = q.vs[n]['name2']
                tipo_nodo_anterior = tipo_nodo_actual

            if camino not in itinerario_minimo[ori][destino]:
                itinerario_minimo[ori][destino].append(camino)

        #alternativa agregada
        tpo_ruta_agregada_minima = float('inf')
        for c in Dict_caminos[ori][destino]:
            camin = c.split('/')

            for elemento in Dict_caminos[ori][destino][c]:
                elem = elemento.split('/')
                for e in elem:
                    if e not in camin:
                        servicios_dict[ori][destino][c].append(e)
        for cam_paradero in Dict_caminos[ori][destino]:
            paraderos = cam_paradero.split('/')
            par_anterior = ''
            serv_anteriores=[]
            #serv_posteriores=[]
            tpo_total = 0
            lista_servicios = []


            for p in paraderos:
                tpo_espera = 0
                tpo_etapa = 0
                #si es el primer paradero del camino
                #serv_posteriores = []
                if par_anterior=='':
                    #print('soy_primero')
                    #recorro los nodos del grafo q
                    for i in q.vs["name2"]:
                        #si es un nodo servicio y el paradero corresponde al evaluado
                        if len(i.split('/'))>1 and i.split('/')[0]==p and i.split('/')[1] in servicios_dict[ori][destino][cam_paradero]:
                            #agrego a servicios anteriores el servicio
                            serv_anteriores.append(i.split('/')[1])

                #si no es el primer paradero del camino
                else:

                    if p[:2] == 'M-' and par_anterior[:2] == 'M-':
                        n_destino = q.vs.find(name2=p).index
                        n_origen = q.vs.find(name2=par_anterior).index

                        tpo_etapa = q.shortest_paths_dijkstra(source=n_origen, target=n_destino, weights=q.es["peso"], mode=OUT)[0][0]
                        tpo_espera = -1

                    else:

                        if par_anterior in Dict_caminos_etapa[ori][destino] and p in Dict_caminos_etapa[ori][destino][par_anterior]:

                            for s in Dict_caminos_etapa[ori][destino][par_anterior][p]:
                                frecuencia = dict_frecuencia[s][p]
                                tpo_espera += dict_frecuencia[s][p]
                                tpo_etapa += (dict_tiempos[s][p] - dict_tiempos[s][par_anterior]) * frecuencia

                                #print(s, par_anterior, p, frecuencia, (dict_tiempos[s][p] - dict_tiempos[s][par_anterior]))


                        #recorro los nodos del grafo q
                        #for i in q.vs["name2"]:
                            # si es un nodo servicio y el paradero corresponde al evaluado
                            #if len(i.split('/'))>1 and i.split('/')[0]==p and i.split('/')[1] in servicios_dict[ori][destino][cam_paradero]:
                                # agrego a servicios posteriores el servicio
                                #serv_posteriores.append(i.split('/')[1])

                        #recorro los servicios del paradero inicial
                        #for s in serv_anteriores:
                            #si el servicio pasa por el paradero posterior
                            #if s in serv_posteriores:
                                #print(par_anterior, s, p)

                                #if s in lista_servicios:
                                    #continue

                                #lista_servicios.append(s)

                                #frecuencia = dict_frecuencia[s][p]
                                #tpo_espera += dict_frecuencia[s][p]
                                #tpo_etapa += (dict_tiempos[s][p]- dict_tiempos[s][par_anterior])*frecuencia

                                #tpo_arco = g.es[g.get_eid(desde, a, directed=True, error=True)]['tpo_viaje']

                    if tpo_espera >0 :
                        tpo_total +=(1/tpo_espera)+(tpo_etapa/tpo_espera)

                    elif tpo_espera == -1 :
                        tpo_total += tpo_etapa

                    #serv_anteriores = serv_posteriores

                par_anterior = p

            if tpo_total < tpo_ruta_agregada_minima:
                tpo_ruta_agregada_minima = tpo_total
                ruta_agregada_minima = cam_paradero

        ruta_minima[ori][destino]=Dict_caminos[ori][destino][ruta_agregada_minima]

for o in itinerario_minimo:
    for d in itinerario_minimo[o]:
        total = 0
        for c in itinerario_minimo[o][d]:
            total += hiperruta_proporcion[o][d][c]

        for c in itinerario_minimo[o][d]:
            itinerario_minimo_proporcion[o][d][c] = hiperruta_proporcion[o][d][c]/total

for o in ruta_minima:
    for d in ruta_minima[o]:
        total = 0
        for c in ruta_minima[o][d]:
            total += hiperruta_proporcion[o][d][c]

        for c in ruta_minima[o][d]:
            ruta_minima_proporcion[o][d][c] = hiperruta_proporcion[o][d][c]/total
'''
print('hiper-ruta')
for o in hiperruta_proporcion:
    for d in hiperruta_proporcion[o]:
        for c in hiperruta_proporcion[o][d]:
            print(c, hiperruta_proporcion[o][d][c])


print('itinerario minimo')
for o in itinerario_minimo_proporcion:
    for d in itinerario_minimo_proporcion[o]:
        for c in itinerario_minimo_proporcion[o][d]:
            print(c, itinerario_minimo_proporcion[o][d][c])

print('ruta minima')
for o in ruta_minima_proporcion:
    for d in ruta_minima_proporcion[o]:
        for c in ruta_minima_proporcion[o][d]:
            print(c, ruta_minima_proporcion[o][d][c])

'''
dump_file2 = open('itinerario_minimo.pkl', 'wb')
dill.dump(itinerario_minimo, dump_file2)
dump_file2.close()

dump_file2 = open('hiperruta_minimo.pkl', 'wb')
dill.dump(hiperruta_minimo, dump_file2)
dump_file2.close()

dump_file2 = open('Dict_caminos.pkl', 'wb')
dill.dump(Dict_caminos, dump_file2)
dump_file2.close()

dump_file2 = open('ruta_minima.pkl', 'wb')
dill.dump(ruta_minima, dump_file2)
dump_file2.close()

dump_file2 = open('hiperruta_proporcion.pkl', 'wb')
dill.dump(hiperruta_proporcion, dump_file2)
dump_file2.close()

dump_file2 = open('itinerario_minimo_proporcion.pkl', 'wb')
dill.dump(itinerario_minimo_proporcion, dump_file2)
dump_file2.close()

dump_file2 = open('ruta_minima_proporcion.pkl', 'wb')
dill.dump(ruta_minima_proporcion, dump_file2)
dump_file2.close()



#print(hiperruta_minimo)

#print(ruta_minima)

#print(itinerario_minimo)

'''
q.vs["label"] = q.vs["name2"]
color_dict = {"paradero": "white", "servicio": "pink"}
q.vs["color"] = [color_dict[tipo] for tipo in q.vs["tipo"]]
plot(q, bbox = (1000, 800), margin = 20)

for a in arcos_grafico:
    print('a', a)
'''
'''
paraderos_serv_y = defaultdict(float)
paraderos_serv_x = defaultdict(float)


for a in arcos_grafico:
    #print('a', a)
    #si es arco de caminata entre paraderos
    #if a[2] in paraderos_coord_dic and a[3] in paraderos_coord_dic:
        #x_1 = float(paraderos_coord_dic[a[2]][0])
        #y_1 = float(paraderos_coord_dic[a[2]][1])

        #x_2 = float(paraderos_coord_dic[a[3]][0])
        #y_2 = float(paraderos_coord_dic[a[3]][1])

        #print('soy arco entre paraderos', a[2], a[3], x_1, y_1, x_2, y_2)

        #pl.plot(x_1, y_1, 'ob')
        #pl.plot(x_2, y_2, 'ob')
        #pl.plot([x_1, x_2], [y_1, y_2], 'red')


    #si es un arco de subida
    if a[2] in paraderos_coord_dic and a[3] not in paraderos_coord_dic:

        x_1 = float(paraderos_coord_dic[a[2]][0])
        y_1 = float(paraderos_coord_dic[a[2]][1])

        if a[3] not in paraderos_serv_y:
            paraderos_serv[a[3]] = float(paraderos_serv[a[3]]) + 50
            x_2 = x_1 + float(paraderos_serv[a[2]])
            y_2 = y_1 + float(paraderos_serv[a[2]])
            paraderos_serv_y[a[3]] = y_2
            paraderos_serv_x[a[3]] = x_2

        x_2 = paraderos_serv_x[a[3]]
        y_2 = paraderos_serv_y[a[3]]

        #print('soy arco de subida', a[2], x_1, y_1, a[3], x_2, y_2)

        pl.plot(x_1, y_1, color='grey', marker='o')
        #pl.plot(x_2, y_2, 'p')
        #pl.plot([x_1, x_2], [y_1, y_2], 'grey')

    # si es un arco de bajada
    elif a[3] in paraderos_coord_dic and a[2] not in paraderos_coord_dic:
        x_2 = float(paraderos_coord_dic[a[3]][0])
        y_2 = float(paraderos_coord_dic[a[3]][1])

        if a[2] not in paraderos_serv_y:
            paraderos_serv[a[3]] = float(paraderos_serv[a[3]]) + 50
            x_1 = x_2 + float(paraderos_serv[a[3]])
            y_1 = y_2 + float(paraderos_serv[a[3]])
            paraderos_serv_y[a[2]] = y_1
            paraderos_serv_x[a[2]] = x_1

        x_1 = paraderos_serv_x[a[2]]
        y_1 = paraderos_serv_y[a[2]]

        #pl.plot(x_1, y_1, 'ob')
        pl.plot(x_2, y_2, color='grey', marker='o')
        #pl.plot([x_1, x_2], [y_1, y_2], 'grey')

    #si es un arco de linea
    elif a[2] not in paraderos_coord_dic and a[3] not in paraderos_coord_dic:

        par1 = a[2].split("/")[0]
        par2 = a[3].split("/")[0]


        if a[2] not in paraderos_serv_y:
            paraderos_serv[par1] = float(paraderos_serv[par1]) + 50
            paraderos_serv_y[a[2]] = float(paraderos_coord_dic[par1][1]) + paraderos_serv[par1]
            paraderos_serv_x[a[2]] = float(paraderos_coord_dic[par1][0]) + paraderos_serv[par1]

        if a[3] not in paraderos_serv_y:
            paraderos_serv[par2] = float(paraderos_serv[par2]) + 50
            paraderos_serv_y[a[3]] = float(paraderos_coord_dic[par2][1]) + paraderos_serv[par2]
            paraderos_serv_x[a[3]] = float(paraderos_coord_dic[par2][0]) + paraderos_serv[par2]

        y_1 = float(paraderos_serv_y[a[2]])
        x_1 = float(paraderos_serv_x[a[2]])

        x_2 = float(paraderos_serv_x[a[3]])
        y_2 = float(paraderos_serv_y[a[3]])


        #print('soy arco de linea', a[2], par1,  x_1, y_1, a[3], par2, x_2, y_2)
        #pl.plot([x_1, x_2], [y_1, y_2], 'grey')


'''




'''
print('caminos')
for j in caminos:

    nodo_anterior = ''
    frecuencia_anterior = 0
    prob_camino = 1
    tiempo_vehiculo = 0
    for i in j:
        nombre = q.vs[i]["name2"] # busco nombre del nodo en el grafo de hiperrutas
        indice = g.vs.find(name=nombre).index # busco el indice del nodo en el grafo de hiperrutas
        frecuencia = g.vs[indice]["frecuencia"]
        tau = g.vs[indice]["tau"]
        tau_inf = g.vs[indice]["tau_inf"]
        tipo = g.vs[indice]["tipo"]
        #print (i, q.vs[i]["name"],q.vs[i]["name2"], frecuencia, tau_inf, g.vs[indice]["tipo"])

        if nodo_anterior != '':
            indice_arco = ((g.vs.find(name=nodo_anterior).index,), (g.vs.find(name=nombre).index,))
            frecuencia_arco = g.es.find(_between=indice_arco)['frecuencia']
            tiempo_vehiculo += g.es.find(_between=indice_arco)['tpo_viaje']

            if frecuencia_anterior>0:
                prob_camino = prob_camino * (frecuencia_arco/frecuencia_anterior)

        nodo_anterior = nombre
        frecuencia_anterior = frecuencia

    #print(j, prob_camino, tiempo_vehiculo-caminata, frecuencia, g.vs[indice]["frecuencia"])


#print('caminos',caminos)
#r = Graph(directed=True)
#rarcos = []
#rarcos_grafico = []

contador_camino = 1

nodos = []
servicios = []


color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(len(caminos))]

contador_color = 0

for j in caminos:
    print('nuevo camino', contador_camino)
    nombre_anterior = ''
    nombre_g_anterior = ''
    for i in j:
        nombre = q.vs[i]["name2"]  # busco nombre del nodo en el grafo de hiperrutas
        indice = g.vs.find(name=nombre).index
        servi = g.vs[indice]["name2"].split('/')
        nombre_g = g.vs[indice]["name2"]
        #print('nombre_g', nombre_g)
        if len(servi)>1:
            servi = servi[1]
        elif servi[0]==origen:
            servi='Origen'
        elif servi[0]==destino:
            servi='Destino'
        else:
            servi = 'paradero'
        #print('mirar',g.vs[indice]["tipo"])

        if servi not in servicios:
            servicios.append(servi)

        if nombre_g_anterior !='':
            #arco de caminata
            if nombre_g_anterior in paraderos_coord_dic and nombre_g in paraderos_coord_dic:
                x_1 = float(paraderos_coord_dic[nombre_g_anterior][0])
                y_1 = float(paraderos_coord_dic[nombre_g_anterior][1])

                x_2 = float(paraderos_coord_dic[nombre_g][0])
                y_2 = float(paraderos_coord_dic[nombre_g][1])

                # print('soy arco entre paraderos', a[2], a[3], x_1, y_1, x_2, y_2)

                pl.plot(x_1, y_1, color='blue', marker='o')
                pl.plot(x_2, y_2, color='blue', marker='o')
                pl.plot([x_1, x_2], [y_1, y_2], 'red')

            # si es un arco de subida
            elif nombre_g_anterior in paraderos_coord_dic and nombre_g not in paraderos_coord_dic:

                x_1 = float(paraderos_coord_dic[nombre_g_anterior][0])
                y_1 = float(paraderos_coord_dic[nombre_g_anterior][1])

                x_2 = paraderos_serv_x[nombre_g]
                y_2 = paraderos_serv_y[nombre_g]

                # print('soy arco de subida', a[2], x_1, y_1, a[3], x_2, y_2)

                pl.plot(x_1, y_1, color='blue', marker='o')
                # pl.plot(x_2, y_2, 'p')
                pl.plot([x_1, x_2], [y_1, y_2], 'blue')

            # si es un arco de bajada
            elif nombre_g in paraderos_coord_dic and nombre_g_anterior not in paraderos_coord_dic:
                x_2 = float(paraderos_coord_dic[nombre_g][0])
                y_2 = float(paraderos_coord_dic[nombre_g][1])

                x_1 = paraderos_serv_x[nombre_g_anterior]
                y_1 = paraderos_serv_y[nombre_g_anterior]


                # print('soy arco de subida', a[2], x_1, y_1, a[3], x_2, y_2)

                #pl.plot(x_1, y_1, 'ob')
                pl.plot(x_2, y_2, color='blue', marker='o')
                pl.plot([x_1, x_2], [y_1, y_2], 'blue')

            # si es un arco de linea
            elif nombre_g_anterior not in paraderos_coord_dic and nombre_g not in paraderos_coord_dic:

                y_1 = float(paraderos_serv_y[nombre_g_anterior])
                x_1 = float(paraderos_serv_x[nombre_g_anterior])

                x_2 = float(paraderos_serv_x[nombre_g])
                y_2 = float(paraderos_serv_y[nombre_g])

                # print('soy arco de linea', a[2], par1,  x_1, y_1, a[3], par2, x_2, y_2)

                # pl.plot(x_1, y_1, 'p')
                # pl.plot(x_2, y_2, 'p')
                pl.plot([x_1, x_2], [y_1, y_2], color[contador_color])

        if g.vs[indice]["tipo"]=='servicio':
            tipo_camino = contador_camino

        else:
            tipo_camino = 0

        #if str(nombre) not in nodos:
            #r.add_vertex(name=str(nombre), name2=g.vs[indice]["name2"], tipo=g.vs[indice]["tipo"], camino = tipo_camino, serv = servi)
            #nodos.append(str(nombre))


        #if nombre_anterior != '' and (str(nombre_anterior), str(nombre)) not in rarcos:
            #rarcos.append((str(nombre_anterior), str(nombre)))
            #rarcos_grafico.append((nombre_g_anterior, nombre_g, servi))

        frecu = g.vs[indice]["frecuencia"]

        if frecu > 0:
            frec_total = g.vs[indice]["frecuencia"]
            print (nombre, g.vs[indice]["name2"], g.vs[indice]["frecuencia"], g.vs[indice]["tau"], g.vs[indice]["tau_inf"], tipo_camino)

        if nombre_anterior != '':
            frecu = g.es[g.get_eid(str(nombre_anterior), str(nombre), directed=True, error=True)]['frecuencia']
            if frecu != float('inf'):
                print('frecuencia_arco', frecu, 'frec_total',frec_total,'prob', round(frecu/frec_total,3), 'servicio', servi)

        nombre_anterior = nombre
        nombre_g_anterior = nombre_g

    contador_camino += 1
    contador_color += 1

#r.add_edges(rarcos)
print('{0} secs'.format(time.time() - start_time))
pl.show()
'''