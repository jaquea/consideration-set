from igraph import *

from HeapBinaria import HeapBinaria
import csv


# class GraphBuilder:
#
#     @staticmethod
#     def build_graph_from_file(self, path):
#         return Graph()
#

class Hyperpath:
    def __init__(self, grafo, destination, transfer_penalty, waiting_penalty, paradero_cercano_dic, dict_servicio_llave_codigoTS):
        self.g = grafo
        self.destination = destination
        self.transfer_penalty = transfer_penalty
        self.waiting_penalty = waiting_penalty
        self.paradero_cercano_dic = paradero_cercano_dic
        self._hyperpath = self._build_hyperpath(grafo, destination, transfer_penalty, waiting_penalty)
        self.destination_index = self._hyperpath.vs.find(name2=self.destination).index
        self.dict_servicio_llave_codigoTS = dict_servicio_llave_codigoTS


    def format_paths(self, path):

        prob_camino = 1
        camino = ''
        camino_paradero = ''
        metro_inicial = ''
        metro_final = ''
        n_iteracion = 0
        tipo_nodo_anterior = ''
        ultimo_nodo = path[-1]
        nodo_anterior = ''
        n_paradero = 0
        camino_resumido = ''
        n_metro_intermedio = 0

        for n in path:
            n_iteracion += 1

            # si el nodo actual es un paradero
            nombre_nodo = self._hyperpath.vs[n]['name2']
            indice_nodo_actual = self.g.vs.find(name2=nombre_nodo).index
            if (self.g.vs["tipo"][indice_nodo_actual]) == 'paradero':

                tipo_nodo_actual = 'paradero'
                frecuencia_total = self.g.vs[indice_nodo_actual]["frecuencia"]

                # si el camino esta vacio agrego el primer nodo al string camino
                if camino == '':
                    n_paradero += 1

                    camino = nombre_nodo
                    camino_resumido = nombre_nodo
                    camino_paradero = nombre_nodo
                    if nombre_nodo[:2] == 'M-':
                        metro_inicial = nombre_nodo

                # si el camino no esta vacio, es la segunda iteracion y el nodo anterior es igual al actual por caminata
                elif (n_iteracion == 2 and tipo_nodo_actual == tipo_nodo_anterior):
                    camino = nombre_nodo
                    camino_paradero = nombre_nodo
                    camino_resumido = nombre_nodo
                    metro_inicial = ''
                    if nombre_nodo[:2] == 'M-':
                        metro_inicial = nombre_nodo

                # si es el ultimo nodo
                elif (n == ultimo_nodo or self._hyperpath.vs[ultimo_nodo]['name2'] == nombre_nodo):
                    n_paradero += 1

                    # si el nodo anterior es distinto al nodo actual
                    if tipo_nodo_anterior != tipo_nodo_actual:
                        # si es metro
                        if nombre_nodo[:2] == 'M-' and metro_inicial != '':
                            metro_final = nombre_nodo

                            camino = camino + '/' + metro_final
                            camino_paradero = camino_paradero + '/' + metro_final

                            if n_metro_intermedio > 0:
                                ultimo_paradero = camino_resumido.split('/')[-1]
                                camino_resumido = camino_resumido.replace('/' + ultimo_paradero, '')

                            camino_resumido = camino_resumido + '/' + metro_final

                            metro_final = ''
                            metro_inicial = ''

                        # si es bus
                        else:
                            camino = camino + '/' + nombre_nodo
                            camino_resumido = camino_resumido + '/' + nombre_nodo
                            camino_paradero = camino_paradero + '/' + nombre_nodo
                # si es un nodo intermedio
                else:
                    # si es metro
                    n_paradero += 1
                    if nombre_nodo[:2] == 'M-' and metro_inicial == '':
                        if n_paradero > 2:
                            ultimo_paradero = camino.split('/')[-1]
                            camino = camino.replace('/' + ultimo_paradero, '')
                            camino_resumido = camino_resumido.replace('/' + ultimo_paradero, '')

                        metro_inicial = nombre_nodo

                        camino = camino + '/' + nombre_nodo
                        camino_resumido = camino_resumido + '/' + nombre_nodo
                        camino_paradero = camino_paradero + '/' + nombre_nodo

                    elif nombre_nodo[:2] == 'M-' and metro_inicial != '':
                        n_metro_intermedio += 1
                        metro_final = nombre_nodo

                        camino = camino + '/' + metro_final
                        camino_paradero = camino_paradero + '/' + metro_final

                        if n_metro_intermedio > 1:
                            ultimo_paradero = camino_resumido.split('/')[-1]
                            camino_resumido = camino_resumido.replace('/' + ultimo_paradero, '')

                        camino_resumido = camino_resumido + '/' + metro_final

                        metro_inicial = metro_final
                        metro_final = ''
                        serv_metro = ''

                    # si no es metro
                    else:
                        if n_paradero > 2:
                            ultimo_paradero = camino.split('/')[-1]
                            camino = camino.replace('/' + ultimo_paradero, '')
                            camino_resumido = camino_resumido.replace('/' + ultimo_paradero, '')
                        camino = camino + '/' + nombre_nodo
                        camino_paradero = camino_paradero + '/' + nombre_nodo
                        camino_resumido = camino_resumido + '/' + nombre_nodo

            # si el nodo es un servicio (posee paradero/servicio)
            else:
                n_paradero = 0
                tipo_nodo_actual = 'servicio'
                frecuencia_arco = self.g.es[
                    self.g.get_eid(self.g.vs.find(name2=nodo_anterior).index, self.g.vs.find(name2=nombre_nodo).index,
                                   directed=True, error=True)]['frecuencia']

                # si es arco de subida a bus
                if frecuencia_arco < float('inf') and metro_inicial == '':
                    prob_arco = frecuencia_arco / frecuencia_total
                    prob_camino = prob_camino * prob_arco
                    servicio = nombre_nodo.split("/")[1]
                    camino = camino + '/' + self.dict_servicio_llave_codigoTS[servicio][0]
                    camino_resumido = camino_resumido + '/' + self.dict_servicio_llave_codigoTS[servicio][0]

                # si es arco de subida a metro
                if metro_inicial != '' and metro_final == '' and tipo_nodo_anterior != 'servicio':
                    servicio = nombre_nodo.split("/")[1]
                    serv_metro = servicio
                    serv_metro = serv_metro.replace('V', '')
                    serv_metro = serv_metro.replace('R', '')
                    serv_metro = serv_metro.replace('-', '')
                    serv_metro = serv_metro.replace('I', '')
                    camino = camino + '/' + serv_metro

                    #se borra esto porque camino resumido no lleva la linea de metro debido a que estaciones que sirven dos lineas de metro tienen el servicio de tipo L1-L5 en la base de datos de viajes
                    #if n_metro_intermedio == 0:
                        #camino_resumido = camino_resumido + '/' + serv_metro

            nodo_anterior = nombre_nodo

            tipo_nodo_anterior = tipo_nodo_actual

        return camino, camino_paradero, prob_camino, camino_resumido

    def get_services_per_stages(self, origin):

        Dict_caminos_etapa = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))

        for origen in self.paradero_cercano_dic[origin]:

            if origen not in self._hyperpath.vs["name2"]:
                continue

            origin_index = self._hyperpath.vs.find(name2=origen).index

            path_set = self.find_all_paths(origin_index, self.destination_index, maxlen=None, mode='OUT')

            for path in path_set:
                tipo_nodo_anterior = ''
                nodo_anterior = ''
                paradero_anterior = ''
                for n in path:
                    # si el nodo actual es un paradero
                    nombre_nodo = self._hyperpath.vs[n]['name2']

                    indice_nodo_actual = self.g.vs.find(name2=nombre_nodo).index

                    if (self.g.vs["tipo"][indice_nodo_actual]) == 'paradero':

                        tipo_nodo_actual = 'paradero'

                    # si el nodo es un servicio (posee paradero/servicio)
                    else:

                        tipo_nodo_actual = 'servicio'

                    if tipo_nodo_actual == 'paradero' and tipo_nodo_anterior == 'servicio':

                        if len(nodo_anterior.split("/")) > 1:
                            if nodo_anterior.split("/")[1] not in \
                                    Dict_caminos_etapa[origin][self.destination][paradero_anterior][nombre_nodo]:
                                Dict_caminos_etapa[origin][self.destination][paradero_anterior][nombre_nodo].append(
                                    nodo_anterior.split("/")[1])

                    if tipo_nodo_actual == 'paradero':
                        paradero_anterior = nombre_nodo

                    nodo_anterior = nombre_nodo

                    tipo_nodo_anterior = tipo_nodo_actual

        return Dict_caminos_etapa

    def find_all_paths(self, start, end, maxlen=None, mode='OUT'):
        def find_all_paths_aux(adjlist, start, end, path, maxlen=None):
            path = path + [start]
            if start == end:
                return [path]
            paths = []
            if maxlen is None or len(path) <= maxlen:
                for node in adjlist[start] - set(path):
                    paths.extend(find_all_paths_aux(adjlist, node, end, path, maxlen))
            return paths

        adjlist = [set(self._hyperpath.neighbors(node, mode=mode)) for node in xrange(self._hyperpath.vcount())]
        all_paths = []
        start = start if type(start) is list else [start]
        end = end if type(end) is list else [end]
        for s in start:
            for e in end:
                all_paths.extend(find_all_paths_aux(adjlist, s, e, [], maxlen))
        return all_paths

    def get_elemental_paths(self, origin, destination):

        Dict_caminos = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        hiperruta_minimo = defaultdict(lambda: defaultdict(list))
        hiperruta_proporcion = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        hiperruta_minimo_camino_desglosado = defaultdict(lambda: defaultdict(list))

        for origen in self.paradero_cercano_dic[origin]:

            if origen not in self._hyperpath.vs["name2"]:
                continue

            origin_index = self._hyperpath.vs.find(name2=origen).index

            path_set = self.find_all_paths(origin_index, self.destination_index, maxlen=None, mode='OUT')

            for j in path_set:

                camino = self.format_paths(j)[3]
                camino_paradero = self.format_paths(j)[1]
                prob_camino = self.format_paths(j)[2]
                camino_desglosado = self.format_paths(j)[0]

                if camino not in Dict_caminos[origin][destination][camino_paradero]:
                    Dict_caminos[origin][destination][camino_paradero].append(camino)
                    hiperruta_minimo[origin][destination].append(camino)
                    hiperruta_minimo_camino_desglosado[origin][destination].append(camino_desglosado)

                if camino not in hiperruta_proporcion[origin][destination]:
                    hiperruta_proporcion[origin][destination][camino] = prob_camino


        return Dict_caminos, hiperruta_minimo, hiperruta_proporcion, hiperruta_minimo_camino_desglosado

    def get_all_shortest_paths(self, origin, hiperruta_proporcion):

        tpo_mas_corto = float('inf')
        itinerario_minimo = defaultdict(lambda: defaultdict(list))
        itinerario_minimo_proporcion = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))

        for origen in self.paradero_cercano_dic[origin]:

            if origen not in self._hyperpath.vs["name2"]:
                continue

            origin_index = self._hyperpath.vs.find(name2=origen).index

            path_set = self._hyperpath.get_all_shortest_paths(origin_index, to=self.destination_index,
                                                              weights=self._hyperpath.es["peso"], mode=OUT)
            tpo_camino = self._hyperpath.shortest_paths_dijkstra(source=origin_index, target=self.destination_index,
                                                                 weights=self._hyperpath.es["peso"], mode=OUT)[0][0]

            path = []
            for j in path_set:
                camino = self.format_paths(j)[3]
                path.append(camino)

            if (tpo_camino < tpo_mas_corto):
                itinerario_minimo[origin][self.destination] = path
                tpo_mas_corto = tpo_camino

            elif (tpo_camino == tpo_mas_corto):
                for j in path:
                    if j not in itinerario_minimo[origin][self.destination]:
                        itinerario_minimo[origin][self.destination].append(j)

        for o in itinerario_minimo:
            for d in itinerario_minimo[o]:
                total = 0
                for c in itinerario_minimo[o][d]:
                    total += hiperruta_proporcion[o][d][c]

                for c in itinerario_minimo[o][d]:
                    itinerario_minimo_proporcion[o][d][c] = hiperruta_proporcion[o][d][c] / total

        return itinerario_minimo, itinerario_minimo_proporcion

    def get_aggregate_paths(self, origin, Dict_caminos, Dict_caminos_etapa, dict_tiempos, dict_frecuencia,
                            hiperruta_proporcion):

        ruta_minima = defaultdict(lambda: defaultdict(list))
        servicios_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        ruta_minima_proporcion = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))

        tpo_ruta_agregada_minima = float('inf')

        for c in Dict_caminos[origin][self.destination]:
            camin = c.split('/')

            for elemento in Dict_caminos[origin][self.destination][c]:
                elem = elemento.split('/')
                for e in elem:
                    if e not in camin:
                        servicios_dict[origin][self.destination][c].append(e)

            for cam_paradero in Dict_caminos[origin][self.destination]:
                paraderos = cam_paradero.split('/')
                par_anterior = ''
                serv_anteriores = []
                tpo_total = 0
                lista_servicios = []

                for p in paraderos:
                    tpo_espera = 0
                    tpo_etapa = 0

                    # si es el primer paradero del camino
                    if par_anterior == '':

                        # recorro los nodos del grafo q
                        for i in self._hyperpath.vs["name2"]:
                            # si es un nodo servicio y el paradero corresponde al evaluado
                            if len(i.split('/')) > 1 and i.split('/')[0] == p and i.split('/')[1] in \
                                    servicios_dict[origin][self.destination][cam_paradero]:
                                # agrego a servicios anteriores el servicio
                                serv_anteriores.append(i.split('/')[1])

                    # si no es el primer paradero del camino
                    else:
                        # caso en que el paradero es metro
                        if p[:2] == 'M-' and par_anterior[:2] == 'M-':
                            n_destino = self._hyperpath.vs.find(name2=p).index
                            n_origen = self._hyperpath.vs.find(name2=par_anterior).index

                            tpo_etapa = self._hyperpath.shortest_paths_dijkstra(source=n_origen, target=n_destino,
                                                                                weights=self._hyperpath.es["peso"],
                                                                                mode=OUT)[0][0]
                            tpo_espera = -1

                        else:

                            if par_anterior in Dict_caminos_etapa[origin][self.destination] and p in \
                                    Dict_caminos_etapa[origin][self.destination][par_anterior]:

                                for s in Dict_caminos_etapa[origin][self.destination][par_anterior][p]:
                                    frecuencia = dict_frecuencia[s][p]
                                    tpo_espera += dict_frecuencia[s][p]
                                    tpo_etapa += (dict_tiempos[s][p] - dict_tiempos[s][par_anterior]) * frecuencia

                        if tpo_espera > 0:
                            tpo_total += (1 / tpo_espera) + (tpo_etapa / tpo_espera)

                        elif tpo_espera == -1:
                            tpo_total += tpo_etapa

                    par_anterior = p

                if tpo_total < tpo_ruta_agregada_minima:
                    tpo_ruta_agregada_minima = tpo_total
                    ruta_agregada_minima = cam_paradero

            ruta_minima[origin][self.destination] = Dict_caminos[origin][self.destination][ruta_agregada_minima]

        for o in ruta_minima:
            for d in ruta_minima[o]:
                total = 0
                for c in ruta_minima[o][d]:
                    total += hiperruta_proporcion[o][d][c]

                for c in ruta_minima[o][d]:
                    ruta_minima_proporcion[o][d][c] = hiperruta_proporcion[o][d][c] / total

        return ruta_minima, ruta_minima_proporcion

    def plot_hyperpath(self):
        """ muestra una imagen de la hiper-ruta """
        self._hyperpath.vs["label"] = self._hyperpath.vs["name2"]
        color_dict = {"paradero": "red", "servicio": "pink"}
        self._hyperpath.vs["color"] = [color_dict[tipo] for tipo in self._hyperpath.vs["tipo"]]
        plot(self._hyperpath, bbox=(1000, 800), margin=20)

    # este metodo arroja un grafo igual al original puesto que es la hiper-ruta desde todos los origenes al destino
    def _build_hyperpath(self, g, destination, transfer_penalty, waiting_penalty):

        if not isinstance(g, Graph):
            raise ValueError('g is not igraph.Graph instance')
        if not destination in g.vs['name2']:
            raise ValueError('destination node does not exist in graph')

        conj_paradero = defaultdict(list)
        conj_paradero_inf = defaultdict(list)

        # inicializacion del algoritmo
        for idx, v in enumerate(g.vs):
            v["tau"] = float('inf')
            v["tau_inf"] = float('inf')
            v["frecuencia"] = 0

        n_destination = g.vs.find(name2=destination).index

        g.vs[n_destination]["tau"] = 0
        g.vs[n_destination]["tau_inf"] = 0

        S = []

        heap = HeapBinaria()
        # Insertamos el nodo destino a la heap binario, puesto que el algoritmo parte analizando desde el destino
        heap.insertar((n_destination, 0))

        while len(S) != len(g.vs):
            # el nodo seleccionado no debe estar en S
            while True:
                nodo_seleccionado = heap.extraer()

                if nodo_seleccionado is None:
                    break
                a = nodo_seleccionado[0]
                if a not in S:
                    break

            if nodo_seleccionado is None:
                break

            S.append(a)

            for j in g.neighborhood(a, order=1, mode=IN)[1:]:

                desde = j

                # tiempo del arco evaluado
                tpo_arco = float(g.es[g.get_eid(desde, a, directed=True, error=True)]['tpo_viaje'])
                tpo_nodo_a = min(g.vs[a]["tau"], g.vs[a]["tau_inf"])

                if g.vs[desde]["name2"] not in self.paradero_cercano_dic[g.vs[n_destination]["name2"]]:
                    t_colita = tpo_arco + tpo_nodo_a

                else:
                    t_colita = tpo_nodo_a

                # si se baja de un servicio a un paradero y el paradero no es el destino se considera una penalizacion por trasbordo
                if g.vs[a]["tipo"] == 'paradero' and g.vs[desde]["tipo"] == 'servicio' and a != n_destination and g.vs[a]["name2"] not in self.paradero_cercano_dic[g.vs[n_destination]["name2"]]:
                    t_colita = t_colita + transfer_penalty
                    if g.vs[desde]["name2"][:2] == 'M-' and g.vs[a]["name2"][:2] == 'M-':
                        t_colita = t_colita - transfer_penalty + 6

                # frecuencia del arco, al inicio toma valor cero
                frec_arco = float(g.es[g.get_eid(desde, a, directed=True, error=True)]['frecuencia'])

                # si es arco sin tiempo de espera
                if frec_arco == float('inf') and t_colita < g.vs[desde]["tau_inf"]:
                    g.vs[desde]["tau_inf"] = t_colita
                    conj_paradero_inf[desde] = [((desde, a), t_colita)]
                    heap.insertar((desde, t_colita))

                # si es arco con espera
                if frec_arco < float('inf') and t_colita < g.vs[desde]["tau"]:

                    if (float(g.vs[desde]["frecuencia"]) == 0 and float(g.vs[desde]["tau"]) == float('inf')):
                        g.vs[desde]["tau"] = (waiting_penalty + frec_arco * t_colita) / float(
                            ((g.vs[desde]["frecuencia"]) + frec_arco))

                    else:
                        g.vs[desde]["tau"] = (float(g.vs[desde]["frecuencia"]) * (
                            g.vs[desde]["tau"]) + frec_arco * t_colita) / (float(g.vs[desde]["frecuencia"]) + frec_arco)

                    g.vs[desde]["frecuencia"] = (float(g.vs[desde]["frecuencia"]) + frec_arco)

                    conj_paradero[desde].append(((desde, a), t_colita))

                    heap.insertar((desde, g.vs[desde]["tau"]))

                for elemento in conj_paradero[desde]:

                    if elemento[1] > g.vs[desde]["tau"]:
                        conj_paradero[desde].remove(elemento)

                        frecuencia_arco = float(
                            g.es[g.get_eid(elemento[0][0], elemento[0][1], directed=True, error=True)][
                                'frecuencia'])
                        frecuencia_nodo = float(g.vs[elemento[0][0]]["frecuencia"])
                        tau_nodo = float(g.vs[elemento[0][0]]["tau"])
                        tarco_colita = elemento[1]

                        g.vs[desde]["tau"] = (frecuencia_nodo * tau_nodo - frecuencia_arco * tarco_colita) / (
                                frecuencia_nodo - frecuencia_arco)

        arcos = []
        nodos = []

        lista_peso = []
        lista_frecuencia = []
        lista_tpo_viaje = []

        for nodo in conj_paradero_inf:

            for elemento in conj_paradero_inf[nodo]:

                if nodo in conj_paradero:

                    tpo_sin_frecuencia = g.vs[nodo]["tau_inf"]  # no hay tiempo de espera
                    tpo_con_frecuencia = g.vs[nodo]["tau"]  # hay tiempo de espera

                    if tpo_sin_frecuencia <= tpo_con_frecuencia:

                        nodo1 = elemento[0][0]
                        nodo2 = elemento[0][1]

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
                    arcos.append((str(nodo1), str(nodo2)))

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

                    if tpo_sin_frecuencia > tpo_con_frecuencia:

                        nodo1 = elemento[0][0]
                        nodo2 = elemento[0][1]
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
                    lista_peso.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['peso'])
                    lista_frecuencia.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['frecuencia'])
                    lista_tpo_viaje.append(g.es[g.get_eid(nodo1, nodo2, directed=True, error=True)]['tpo_viaje'])

                    if (nodo1, g.vs["tipo"][nodo1], g.vs["name2"][nodo1]) not in nodos:
                        nodos.append((nodo1, g.vs["tipo"][nodo1], g.vs["name2"][nodo1]))

                    if (nodo2, g.vs["tipo"][nodo2], g.vs["name2"][nodo2]) not in nodos:
                        nodos.append((nodo2, g.vs["tipo"][nodo2], g.vs["name2"][nodo2]))

        q = Graph(directed=True)

        for v in nodos:
            q.add_vertex(name=str(v[0]), tipo=v[1], name2=v[2])

        q.add_edges(arcos)

        q.es["peso"] = lista_peso

        return q


# graph_obj = GraphBuilder.build_graph_from_file('c:\\jacke\\archivo.csv')
#
# a = Hyperpath(graph_obj, 1)
# a.get_aggregated_paths()
# a.get_elemental_paths()
#
#
# g = Graph(directed=True)
# g.add_vertex(name='nodo 1', name2='nodo 1', tipo='paradero')
# g.add_vertex(name='nodo 2', name2='nodo 2', tipo='paradero')
# g.add_edge('nodo 1', 'nodo 2', frecuencia=2, tpo_viaje=4, peso=(1/2) + 4)
# plot(g)
# destination = 'nodo 2'
# transfer_penalty = 0
# waiting_penalty = 1
# hyperpath_obj = Hyperpath(g, destination=destination, transfer_penalty = transfer_penalty, waiting_penalty = waiting_penalty)
# hyperpath_obj.plot_hyperpath()
