from igraph import *
from HeapBinaria import HeapBinaria
import pickle
import pandas as pd
import random
import utm
import matplotlib.pyplot as pl
import time

start_time = time.time()

heap = HeapBinaria()

g = Graph(directed=True)
g.add_vertices(13)
g.add_edges([(0,1), (1,0), (1,5), (0,2), (2,0), (2,6), (0,3), (3,0), (3,7), (0,4), (4,0), (4,12), (5,8), (8,5), (6,8), (8,6), (7,8), (8,7), (8,9), (9,8), (9,10), (10,11), (11,10), (12,11), (11,12)])

g.vs["name"] = ["A", "A/1", "A/2", "A/3", "A/4", "B/1", "B/2", "B/3", "B", "B/5", "D/5", "D", "D/4"]
g.vs["tipo"] = ["Paradero", "servicio", "servicio", "servicio", "servicio", "servicio", "servicio", "servicio", "Paradero", "servicio", "servicio", "Paradero", "servicio"]
g.es["frecuencia"] = [float(5.0/60.0), float('inf'), float('inf'), float(5.0/60.0), float('inf'), float('inf'), float(5.0/60.0), float('inf'), float('inf'), float(10.0/60.0), float('inf'), float('inf'), float('inf'), float(5.0/60.0), float('inf'), float(5.0/60.0), float('inf'), float(5.0/60.0), float(10.0/60.0), float('inf'), float('inf'),float('inf'), float(10.0/60.0), float('inf'), float(10.0/60.0)]
g.es["tpo_viaje"] = [0, 0, 6, 0, 0, 5.5, 0, 0, 5, 0, 0, 24, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0,0]

lista_peso = []

for i in range(0,len(g.es["frecuencia"])):

    if g.es["frecuencia"][i] < float('inf'):
        frec = 1/g.es["frecuencia"][i]

    else:
        frec = 0

    peso = g.es["tpo_viaje"][i] + frec

    lista_peso.append(peso)

print(lista_peso)

g.es["peso"] = lista_peso
#print('frecuencias',g.es["frecuencia"])
alfa = 1 #penalizacion tiempo espera
caminata = 0 #otiempo de viaje a la que equivale un trasbord

conj_paradero = defaultdict(list)
conj_paradero_inf = defaultdict(list)

for i in range(0,len(g.vs)):
    g.vs[i]["tau"]=float('inf')
    g.vs[i]["tau_inf"] = float('inf')
    g.vs[i]["frecuencia"] = 0


destino = 'D'

n_destino = g.vs.find(name=destino).index

g.vs[n_destino]["tau"] = 0
g.vs[n_destino]["tau_inf"] = 0

#copia = Graph(directed=True)
#copia = g

#copia.vs[n_destino]["tau"] = 0
#copia.vs[n_destino]["tau_inf"] = 0

S=[]

#copia.vs["label"] = copia.vs["name"]
#color_dict = {"Paradero": "white", "servicio": "pink"}
#copia.vs["color"] = [color_dict[tipo] for tipo in copia.vs["tipo"]]
#plot(g, bbox = (800, 800), margin = 20)

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
                t_colita = t_colita + caminata

            # frecuencia del arco, al inicio toma valor cero
            frec_arco = g.es[g.get_eid(desde, a, directed=True, error=True)]['frecuencia']

            # si es arco sin tiempo de espera
            if frec_arco == float('inf') and t_colita < g.vs[desde]["tau_inf"]:
                #print('arco', desde, a)

                g.vs[desde]["tau_inf"] = t_colita
                #copia.vs[desde]["tau_inf"] = t_colita_copia

                #print('tpo', copia.vs[desde]["tau_inf"])

                #conj_paradero_inf[desde] = [((desde, a), t_colita_copia, copia.vs[desde]["tau_inf"], copia.vs[desde]["frecuencia"])]
                conj_paradero_inf[desde] = [((desde, a), t_colita)]

                heap.insertar((desde, t_colita))

            # si es arco con espera
            if frec_arco < float('inf') and t_colita < g.vs[desde]["tau"]:

                #print('arco de espera', desde, a)
                #print('frecuencia_antes')
                #print(desde, copia.vs[desde]["name"], copia.vs[a]["name"], copia.vs[desde]["frecuencia"], frec_arco)

                if ((g.vs[desde]["frecuencia"]) == 0 and (g.vs[desde]["tau"]) == float('inf')):

                    g.vs[desde]["tau"] = (alfa + frec_arco * t_colita) / float(((g.vs[desde]["frecuencia"]) + frec_arco))
                    #copia.vs[desde]["tau"] = (1 + frec_arco * t_colita_copia) / float(((copia.vs[desde]["frecuencia"]) + frec_arco))

                else:
                    g.vs[desde]["tau"] = ((g.vs[desde]["frecuencia"]) * (g.vs[desde]["tau"]) + frec_arco * t_colita) / ((g.vs[desde]["frecuencia"]) + frec_arco)
                    #copia.vs[desde]["tau"] = ((copia.vs[desde]["frecuencia"]) * (copia.vs[desde]["tau"]) + frec_arco * t_colita_copia) / ((copia.vs[desde]["frecuencia"]) + frec_arco)

                #g.vs[desde]["frecuencia"] = ((g.vs[desde]["frecuencia"]) + frec_arco)
                g.vs[desde]["frecuencia"] += frec_arco

                #print('frecuencia_despues')
                #print(desde, copia.vs[desde]["name"], copia.vs[desde]["frecuencia"], frec_arco)

                #conj_paradero[desde].append(((desde, a), t_colita_copia, copia.vs[desde]["tau"], copia.vs[desde]["frecuencia"]))
                conj_paradero[desde].append(((desde, a), t_colita_copia))

                heap.insertar((desde, g.vs[desde]["tau"]))

                #print('tpo', copia.vs[desde]["tau"])

                # print('nodo', g.vs[desde]["name"], 'tau:', g.vs[desde]["tau"], 't_colita:', t_colita)

                for elemento in conj_paradero[desde]:

                    # print("hola",desde, conj_paradero[desde])

                    if elemento[1] > g.vs[desde]["tau"]:
                        # print('elemento removido', elemento)

                        conj_paradero[desde].remove(elemento)

                        frecuencia_arco = g.es[g.get_eid(elemento[0][0], elemento[0][1], directed=True, error=True)]['frecuencia']
                        frecuencia_nodo = g.vs[elemento[0][0]]["frecuencia"]
                        tau_nodo = g.vs[elemento[0][0]]["tau"]
                        tarco_colita = elemento[1]

                        g.vs[desde]["tau"] = (frecuencia_nodo * tau_nodo - frecuencia_arco * tarco_colita) / (frecuencia_nodo - frecuencia_arco)

                        #frecuencia_arco = copia.es[copia.get_eid(elemento[0][0], elemento[0][1], directed=True, error=True)]['frecuencia']
                        #frecuencia_nodo = copia.vs[elemento[0][0]]["frecuencia"]
                        #tau_nodo = copia.vs[elemento[0][0]]["tau"]
                        #tarco_colita = elemento[1]

                        #copia.vs[desde]["tau"] = (frecuencia_nodo * tau_nodo - frecuencia_arco * tarco_colita) / (frecuencia_nodo - frecuencia_arco)

                        g.vs[desde]["frecuencia"] = ((g.vs[desde]["frecuencia"]) - frecuencia_arco)
                        #copia.vs[desde]["frecuencia"] = ((copia.vs[desde]["frecuencia"]) - frecuencia_arco)

    nodo_seleccionado = heap.extraer()
    # print('nodo_seleccionado', nodo_seleccionado)

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
                arcos_grafico.append((str(nodo1), str(nodo2),g.vs["name"][nodo1],g.vs["name"][nodo2]))
                arcos.append((str(nodo1), str(nodo2)))

                lista_peso.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['peso'])
                lista_frecuencia.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['frecuencia'])
                lista_tpo_viaje.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['tpo_viaje'])

                #print('aqui',(str(nodo1), str(nodo2)))

                if (nodo1, g.vs["tipo"][nodo1],g.vs["name"][nodo1]) not in nodos:
                    nodos.append((nodo1, g.vs["tipo"][nodo1],g.vs["name"][nodo1]))

                if (nodo2, g.vs["tipo"][nodo2], g.vs["name"][nodo2]) not in nodos:
                    nodos.append((nodo2, g.vs["tipo"][nodo2], g.vs["name"][nodo2]))

        else:

            nodo1 = elemento[0][0]
            nodo2 = elemento[0][1]
            # print('es sin frecuencia', nodo1, nodo2, g.vs["name"][nodo1], g.vs["name"][nodo2], g.vs["tipo"][nodo1],g.vs["tipo"][nodo2])
            arcos.append((str(nodo1), str(nodo2)))
            #print('aqui', (str(nodo1), str(nodo2)))
            lista_peso.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['peso'])
            lista_frecuencia.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['frecuencia'])
            lista_tpo_viaje.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['tpo_viaje'])

            arcos_grafico.append((str(nodo1), str(nodo2), g.vs["name"][nodo1], g.vs["name"][nodo2]))

            if (nodo1, g.vs["tipo"][nodo1], g.vs["name"][nodo1]) not in nodos:
                nodos.append((nodo1, g.vs["tipo"][nodo1], g.vs["name"][nodo1]))

            if (nodo2, g.vs["tipo"][nodo2], g.vs["name"][nodo2]) not in nodos:
                nodos.append((nodo2, g.vs["tipo"][nodo2], g.vs["name"][nodo2]))

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
                #print('aqui', (str(nodo1), str(nodo2)))
                arcos_grafico.append((str(nodo1), str(nodo2), g.vs["name2"][nodo1], g.vs["name2"][nodo2]))

                if (nodo1, g.vs["tipo"][nodo1], g.vs["name"][nodo1]) not in nodos:
                    nodos.append((nodo1, g.vs["tipo"][nodo1], g.vs["name"][nodo1]))

                if (nodo2, g.vs["tipo"][nodo2], g.vs["name"][nodo2]) not in nodos:
                    nodos.append((nodo2, g.vs["tipo"][nodo2], g.vs["name"][nodo2]))

        else:

            nodo1 = elemento[0][0]
            nodo2 = elemento[0][1]
            # print('es sin frecuencia', nodo1, nodo2, g.vs["name"][nodo1], g.vs["name"][nodo2], g.vs["tipo"][nodo1],g.vs["tipo"][nodo2])
            arcos.append((str(nodo1), str(nodo2)))
            lista_peso.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['peso'])
            lista_frecuencia.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['frecuencia'])
            lista_tpo_viaje.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['tpo_viaje'])
            #print('aqui', (str(nodo1), str(nodo2)))
            arcos_grafico.append((str(nodo1), str(nodo2), g.vs["name"][nodo1], g.vs["name"][nodo2]))

            if (nodo1, g.vs["tipo"][nodo1], g.vs["name"][nodo1]) not in nodos:
                nodos.append((nodo1, g.vs["tipo"][nodo1], g.vs["name"][nodo1]))

            if (nodo2, g.vs["tipo"][nodo2], g.vs["name"][nodo2]) not in nodos:
                nodos.append((nodo2, g.vs["tipo"][nodo2], g.vs["name"][nodo2]))

q = Graph(directed=True)

for v in nodos:
    #print(v[0])
    q.add_vertex(name=str(v[0]), tipo= v[1], name2= v[2])

q.add_edges(arcos)
q.es["peso"]=lista_peso


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

origen = 'A'
id = g.vs.find(name=origen).index

name2 = g.vs[id]['name']

n_origen = q.vs.find(name2=name2).index


name3 = g.vs[n_destino]['name']
n_destino = q.vs.find(name2=name3).index

caminos = find_all_paths(q, n_origen, n_destino, mode = 'OUT', maxlen = None)

Dict_caminos = defaultdict(lambda: defaultdict (lambda: defaultdict (list)))
hiperruta_minimo = defaultdict(lambda: defaultdict (list))

for j in caminos:
    prob_camino = 1
    camino = ''
    camino_paradero = ''

    for n in j:

        if (g.vs["tipo"][g.vs.find(name=q.vs[n]['name2']).index])=='Paradero':

            frecuencia_total = g.vs[g.vs.find(name=q.vs[n]['name2']).index]["frecuencia"]

            if camino =='':
                camino = q.vs[n]['name2']
                camino_paradero = q.vs[n]['name2']

            else:
                camino = camino + '/' + q.vs[n]['name2']
                camino_paradero = camino_paradero + '/' + q.vs[n]['name2']


        else:
            frecuencia_arco = g.es[g.get_eid(g.vs.find(name=nodo_anterior).index, g.vs.find(name=q.vs[n]['name2']).index, directed=True, error=True)]['frecuencia']

            if frecuencia_arco < float('inf'):
                prob_arco = frecuencia_arco/frecuencia_total
                prob_camino = prob_camino * prob_arco
                servicio = q.vs[n]['name2'].split("/")[1]
                camino = camino + '/' + servicio


        nodo_anterior = q.vs[n]['name2']

    #Dict_caminos[origen][destino][camino_paradero].append((camino, prob_camino))
    Dict_caminos[origen][destino][camino_paradero].append(camino)
    hiperruta_minimo[origen][destino].append(camino)


##probabilidad de los caminos de la hiper-ruta

print('Probabilidad de cada camino en la hiper-ruta')
print(Dict_caminos)

print("ruta minima")

ruta_min = q.shortest_paths_dijkstra(source='0', target='11', weights=q.es["peso"], mode=OUT)

print(ruta_min)
path= q.get_all_shortest_paths('0', to='11', weights=q.es["peso"], mode=OUT)

itinerario_min = ''
serv_anterior=''
for n in path[0]:
    if itinerario_min == '':
        itinerario_min = q.vs[n]['name2']

    else:
        lista = q.vs[n]['name2'].split('/')
        if len (lista)>1:
            if lista[1]!=serv_anterior:
                itinerario_min = itinerario_min + '/' + lista[1]
                serv_anterior = lista[1]
        else:
            itinerario_min = itinerario_min + '/' + q.vs[n]['name2']

itinerario_minimo = defaultdict(lambda: defaultdict (list))
itinerario_minimo ['A']['D']=[itinerario_min]
print(itinerario_minimo)

print("alternativa agregada minima")

ruta_minima = defaultdict(lambda: defaultdict (list))

for cam_paradero in Dict_caminos[origen][destino]:
    #print('cam_paradero', cam_paradero)
    paraderos = cam_paradero.split('/')
    par_anterior = ''
    serv_anteriores=[]
    serv_posteriores=[]
    #print(cam_paradero)
    tpo_total = 0
    tpo_ruta_agregada_minima = float('inf')
    for p in paraderos:
        tpo_espera = 0
        tpo_etapa = 0
        #si es el primer paradero del camino
        serv_posteriores = []
        if par_anterior=='':
            #print('soy_primero')
            #recorro los nodos del grafo q
            for i in q.vs["name2"]:
                #si es un nodo servicio y el paradero corresponde al evaluado
                if len(i.split('/'))>1 and i.split('/')[0]==p:
                    #agrego a servicios anteriores el servicio
                    serv_anteriores.append(i.split('/')[1])

        #si no es el primer paradero del camino
        else:
            #recorro los nodos del grafo q
            for i in q.vs["name2"]:
                # si es un nodo servicio y el paradero corresponde al evaluado
                if len(i.split('/'))>1 and i.split('/')[0]==p:
                    # agrego a servicios posteriores el servicio
                    serv_posteriores.append(i.split('/')[1])

            #recorro los servicios del paradero inicial
            for s in serv_anteriores:
                #si el servicio pasa por el paradero posterior
                if s in serv_posteriores:
                    #print(par_anterior, s, p)

                    #tiempo de espera
                    desde = q.vs.find(name2=par_anterior).index
                    a = q.vs.find(name2=par_anterior+'/'+s).index
                    tpo_espera += (1/q.es[q.get_eid(desde, a, directed=True, error=True)]['peso'])
                    frecuencia = (1/q.es[q.get_eid(desde, a, directed=True, error=True)]['peso'])
                    #print(desde, a, tpo_espera)

                    #tiempo de viaje
                    desde = q.vs.find(name2=par_anterior+'/'+s).index
                    a = q.vs.find(name2=p+'/'+s).index
                    tpo_etapa += float(q.es[q.get_eid(desde, a, directed=True, error=True)]['peso'])*frecuencia
                    serv_anteriores = serv_posteriores
                    #print(desde, a, tpo_etapa)
                    #tpo_arco = g.es[g.get_eid(desde, a, directed=True, error=True)]['tpo_viaje']
            tpo_total += (1/tpo_espera) + (tpo_etapa/tpo_espera)
        par_anterior = p

    if tpo_total < tpo_ruta_agregada_minima:
        tpo_ruta_agregada_minima = tpo_total
        ruta_agregada_minima = cam_paradero

ruta_minima['A']['D']=Dict_caminos['A']['D'][cam_paradero]

print(ruta_minima)

viajes = defaultdict(lambda: defaultdict (lambda: defaultdict (list)))

viajes['A']['D']['A/4/D']=15
viajes['A']['D']['A/1/B/5/D']=10
viajes['A']['D']['A/2/B/5/D']=1
viajes['A']['D']['A/3/B/5/D']=5

n_ruta_minima = 0
n_itinerario_minimo = 0
n_hiperruta = 0

for o in viajes:
    for d in viajes[o]:
        itinerarios_minimos = itinerario_minimo [o][d]
        rutas_minimas = ruta_minima[o][d]
        hiperutas_minimas = hiperruta_minimo[o][d]

        for camino in viajes[o][d]:
            n_viaje = viajes[origen][destino][camino]

            #verficar si el camino es itinerario minimo
            if camino in itinerarios_minimos:
                n_itinerario_minimo += n_viaje

            if camino in rutas_minimas:
                n_ruta_minima += n_viaje

            if camino in hiperutas_minimas:
                n_hiperruta += n_viaje




print('n_itinerario_minimo', n_itinerario_minimo)
print('n_ruta_minima', n_ruta_minima)
print('n_hiperruta', n_hiperruta)

print(q.vs['name2'])

print(1/float('inf'))