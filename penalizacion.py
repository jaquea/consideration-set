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

heap = HeapBinaria()

alfa = 1 #penalizacion tiempo espera
caminata = 5 #tiempo de viaje a la que equivale un trasbordo

dump_file2 = open('tiempos.pkl', 'rb')
dict_tiempos = dill.load(dump_file2)
dump_file2.close()

dump_file3 = open('frecuencias.pkl', 'rb')
dict_frecuencia = dill.load(dump_file3)
dump_file3.close()

dump_file2 = open('paradero_cercano_dic.pkl', 'rb')
paradero_cercano_dic = dill.load(dump_file2)
dump_file2.close()

def hyperpath (g, destino, alfa, caminata):
    conj_paradero = defaultdict(list)
    conj_paradero_inf = defaultdict(list)
    # inicializacion
    # inicializacion del algoritmo
    for i in range(0, len(g.vs)):
        g.vs[i]["tau"] = float('inf')
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

            desde = j

            if a not in S:

                # tiempo del arco evaluado
                tpo_arco = g.es[g.get_eid(desde, a, directed=True, error=True)]['tpo_viaje']

                # tiempo que hay desde la cola del arco hacia el destino
                tpo_nodo_a = min(g.vs[a]["tau"], g.vs[a]["tau_inf"])

                t_colita = tpo_arco + tpo_nodo_a
                t_colita_copia = t_colita
                # t_colita = g.es[g.get_eid(desde, a, directed=True, error=True)]['peso'] + min(g.vs[a]["tau"], g.vs[a]["tau"])

                if g.vs[a]["tipo"] == 'paradero':

                    if a != n_destino:
                        t_colita = t_colita + caminata

                    else:
                        t_colita = tpo_nodo_a

                # frecuencia del arco, al inicio toma valor cero
                frec_arco = g.es[g.get_eid(desde, a, directed=True, error=True)]['frecuencia']

                # si es arco sin tiempo de espera
                if frec_arco == float('inf') and t_colita < g.vs[desde]["tau_inf"]:
                    g.vs[desde]["tau_inf"] = t_colita
                    # copia.vs[desde]["tau_inf"] = t_colita_copia

                    # conj_paradero_inf[desde]=[((desde, a),  t_colita, copia.vs[desde]["tau_inf"], copia.vs[desde]["frecuencia"])]

                    conj_paradero_inf[desde] = [((desde, a), t_colita)]

                    heap.insertar((desde, t_colita))

                # si es arco con espera
                if frec_arco < float('inf') and t_colita < g.vs[desde]["tau"]:

                    if ((g.vs[desde]["frecuencia"]) == 0 and (g.vs[desde]["tau"]) == float('inf')):

                        g.vs[desde]["tau"] = (alfa + frec_arco * t_colita) / float(
                            ((g.vs[desde]["frecuencia"]) + frec_arco))
                        # copia.vs[desde]["tau"] = (1 + frec_arco * t_colita_copia) / float(((copia.vs[desde]["frecuencia"]) + frec_arco))

                    else:
                        g.vs[desde]["tau"] = ((g.vs[desde]["frecuencia"]) * (
                            g.vs[desde]["tau"]) + frec_arco * t_colita) / ((g.vs[desde]["frecuencia"]) + frec_arco)
                        # copia.vs[desde]["tau"] = ((copia.vs[desde]["frecuencia"]) * (copia.vs[desde]["tau"]) + frec_arco * t_colita_copia) / ((copia.vs[desde]["frecuencia"]) + frec_arco)

                    g.vs[desde]["frecuencia"] = ((g.vs[desde]["frecuencia"]) + frec_arco)
                    # copia.vs[desde]["frecuencia"] = ((copia.vs[desde]["frecuencia"]) + frec_arco)

                    conj_paradero[desde].append(((desde, a), t_colita_copia))

                    heap.insertar((desde, g.vs[desde]["tau"]))

                    # print('nodo', g.vs[desde]["name"], 'tau:', g.vs[desde]["tau"], 't_colita:', t_colita)

                    for elemento in conj_paradero[desde]:

                        # print("hola",desde, conj_paradero[desde])

                        if elemento[1] > g.vs[desde]["tau"]:
                            # print('elemento removido', elemento)

                            conj_paradero[desde].remove(elemento)

                            frecuencia_arco = \
                                g.es[g.get_eid(elemento[0][0], elemento[0][1], directed=True, error=True)]['frecuencia']
                            frecuencia_nodo = g.vs[elemento[0][0]]["frecuencia"]
                            tau_nodo = g.vs[elemento[0][0]]["tau"]
                            tarco_colita = elemento[1]

                            g.vs[desde]["tau"] = (frecuencia_nodo * tau_nodo - frecuencia_arco * tarco_colita) / (
                                frecuencia_nodo - frecuencia_arco)

                            # frecuencia_arco = copia.es[copia.get_eid(elemento[0][0], elemento[0][1], directed=True, error=True)]['frecuencia']
                            # frecuencia_nodo = copia.vs[elemento[0][0]]["frecuencia"]
                            # tau_nodo = copia.vs[elemento[0][0]]["tau"]
                            # tarco_colita = elemento[1]

                            # copia.vs[desde]["tau"] = (frecuencia_nodo * tau_nodo - frecuencia_arco * tarco_colita) / ( frecuencia_nodo - frecuencia_arco)

                            # print('nodo_seleccionado_pre', 'name:', g.vs[j]["name"], 'frecuencia:', g.vs[j]['frecuencia'], "tau:", g.vs[j]["tau"], "tau_inf:", g.vs[j]["tau_inf"])
        nodo_seleccionado = heap.extraer()
        # print('nodo_seleccionado', nodo_seleccionado)

        if a not in S:
            S.append(a)

    arcos = []
    nodos = []
    arcos_grafico = []

    lista_peso = []
    lista_frecuencia = []
    lista_tpo_viaje = []

    for nodo in conj_paradero_inf:

        for elemento in conj_paradero_inf[nodo]:

            if nodo in conj_paradero:

                tpo_sin_frecuencia = g.vs[nodo]["tau_inf"]  # no hay tiempo de espera
                tpo_con_frecuencia = g.vs[nodo]["tau"]  # hay tiempo de espera

                # print ('nodo', i, g.vs[i]["tau"], g.vs[i]["tau_inf"], g.vs[i]["frecuencia"])

                if tpo_sin_frecuencia <= tpo_con_frecuencia:

                    nodo1 = elemento[0][0]
                    nodo2 = elemento[0][1]
                    # print('es sin frecuencia', nodo1, nodo2, g.vs["name"][nodo1], g.vs["name"][nodo2], g.vs["tipo"][nodo1],g.vs["tipo"][nodo2])
                    arcos_grafico.append((str(nodo1), str(nodo2), g.vs["name2"][nodo1], g.vs["name2"][nodo2]))
                    arcos.append((str(nodo1), str(nodo2)))

                    lista_peso.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['peso'])
                    lista_frecuencia.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['frecuencia'])
                    lista_tpo_viaje.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['tpo_viaje'])

                    if (nodo1, g.vs["tipo"][nodo1], g.vs["name2"][nodo1]) not in nodos:
                        nodos.append((nodo1, g.vs["tipo"][nodo1], g.vs["name2"][nodo1]))

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
        # print(v[0])
        q.add_vertex(name=str(v[0]), tipo=v[1], name2=v[2])
    q.add_edges(arcos)
    q.es["peso"] = lista_peso
    return q

    for v in nodos:
        #print(v[0])
        q.add_vertex(name=str(v[0]), tipo= v[1], name2= v[2])

    q.add_edges(arcos)
    q.es["peso"]=lista_peso

    return q

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
    adjlist = [set(graph.neighbors(node, mode = mode)) \
        for node in xrange(graph.vcount())]
    all_paths = []
    start = start if type(start) is list else [start]
    end = end if type(end) is list else [end]
    for s in start:
        for e in end:
            all_paths.extend(find_all_paths_aux(adjlist, s, e, [], maxlen))
    return all_paths

def hiperruta(caminos):
    hiperruta_minimo = defaultdict(lambda: defaultdict(list))
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

        for n in j:

            n_iteracion += 1

            if (g.vs["tipo"][g.vs.find(name2=q.vs[n]['name2']).index]) == 'paradero':

                tipo_nodo_actual = 'paradero'

                frecuencia_total = g.vs[g.vs.find(name2=q.vs[n]['name2']).index]["frecuencia"]
                nombre_nodo = q.vs[n]['name2']

                # si el camino esta vacio agrego el primer nodo al string camino
                if camino == '' or (n_iteracion == 2 and tipo_nodo_actual == tipo_nodo_anterior):
                    camino = nombre_nodo
                    camino_paradero = nombre_nodo
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
                frecuencia_arco = g.es[
                    g.get_eid(g.vs.find(name2=nodo_anterior).index, g.vs.find(name2=q.vs[n]['name2']).index,
                              directed=True, error=True)]['frecuencia']

                if frecuencia_arco < float('inf') and metro_inicial == '':
                    prob_arco = frecuencia_arco / frecuencia_total
                    prob_camino = prob_camino * prob_arco
                    servicio = q.vs[n]['name2'].split("/")[1]
                    camino = camino + '/' + servicio

                if metro_inicial != '' and metro_final == '':
                    servicio = q.vs[n]['name2'].split("/")[1]
                    serv_metro = servicio

            nodo_anterior = q.vs[n]['name2']
            tipo_nodo_anterior = tipo_nodo_actual

        # diccionario que contiene como llaves el origen destino y el camino como secuecia de paradero y el elemento es el camino con los servicios
        if camino not in hiperruta_minimo[ori][destino]:
            hiperruta_minimo[ori][destino].append(camino)

    return hiperruta_minimo

epsilon_anterior = 0
epsilon = 0
caminata = 0
alfa = 1
caminata_final = 0

viajes = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))

dump_file2 = open('tmp/viajes_procesados.pkl', 'rb')
viajes = dill.load(dump_file2)
dump_file2.close()

viajes_p = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:0)))

viajes_p['T-14-128-PO-20']['E-20-53-PO-95']= viajes['T-14-128-PO-20']['E-20-53-PO-95']
#viajes_p['T-34-313-SN-35']['E-20-205-SN-65']= viajes['T-34-313-SN-35']['E-20-205-SN-65']
#viajes_p['L-34-53-25-PO']['M-SL']= viajes['L-34-53-25-PO']['M-SL']
#viajes_p['T-34-313-SN-35']['M-SL']= viajes['T-34-313-SN-35']['M-SL']

viajes = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:0)))

viajes=viajes_p

iteraciones = 0

while (epsilon > epsilon_anterior or (iteraciones < 20 and epsilon == epsilon_anterior)):
    t_ini = time.time()
    epsilon_anterior = epsilon
    hiperruta_minimo = defaultdict(lambda: defaultdict (list))
    cont = 0
    total_viajes = 0
    viajes_en_hiperruta = 0

    for destino in viajes:
        cont += 1
        print(destino, cont)

        # cargar grafo desde archivo
        dump_file1 = open('grafo.igraph', 'rb')
        g = pickle.load(dump_file1)
        dump_file1.close()
        q = hyperpath(g, destino, alfa, caminata)
        n_destino = q.vs.find(name2=destino).index
        lista_caminos_evaluados=[]

        for ori in viajes[destino]:

            for origen in paradero_cercano_dic[ori]:
                if origen not in q.vs["name2"]:
                    continue

                n_origen = q.vs.find(name2=origen).index
                caminos = find_all_paths(q, n_origen, n_destino, mode='OUT', maxlen=None)

                hiperruta_minimo = hiperruta(caminos)
                for c in viajes[destino][ori]:
                    if c not in lista_caminos_evaluados and c in hiperruta_minimo[origen][destino]:
                        n_viajes = viajes[destino][ori][c]
                        viajes_en_hiperruta += n_viajes
                        lista_caminos_evaluados.append(c)

            for c in viajes[destino][ori]:
                n_viajes = viajes[destino][ori][c]
                total_viajes += n_viajes



    epsilon = viajes_en_hiperruta / float(total_viajes)

    t_fin = time.time()

    t_ejecucion = t_fin - t_ini

    print('caminata=', caminata, 'epsilon=', epsilon, 'viajes_en_hiperruta=', viajes_en_hiperruta, 'total_viajes=', total_viajes, 't_ejecucion', t_ejecucion)

    if (epsilon > epsilon_anterior) or (iteraciones < 20 and epsilon == epsilon_anterior):
        if (epsilon == epsilon_anterior):
            iteraciones += 1
        else:
            caminata_final = caminata
            iteraciones = 0
        caminata += 5

    else:
        print('penalizacion caminata:', caminata_final)

    print('iteraciones', iteraciones, 'epsilon', epsilon, 'epsilon_anterior', epsilon_anterior)





