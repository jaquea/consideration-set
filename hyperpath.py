from igraph import *
from HeapBinaria import HeapBinaria

# class GraphBuilder:
#
#     @staticmethod
#     def build_graph_from_file(self, path):
#         return Graph()
#

class Hyperpath:
    def __init__(self, grafo, destination, transfer_penalty, waiting_penalty):
        self.g = grafo
        self.destination = destination
        self.transfer_penalty = transfer_penalty
        self.waiting_penalty = waiting_penalty
        self._hyperpath = self._build_hyperpath(grafo, destination, transfer_penalty, waiting_penalty)

    def format_paths(self, path_set):

        lista_caminos = []

        for j in path_set:
            prob_camino = 1
            camino = ''
            camino_paradero = ''
            metro_inicial = ''
            metro_final = ''
            n_iteracion = 0
            tipo_nodo_anterior = ''
            ultimo_nodo = j[-1]
            nodo_anterior = ''

            for n in j:
                n_iteracion += 1

                # si el nodo actual es un paradero
                nombre_nodo = self._hyperpath.vs[n]['name2']
                indice_nodo_actual = self.g.vs.find(name2=nombre_nodo).index
                if (self.g.vs["tipo"][indice_nodo_actual]) == 'paradero':

                    tipo_nodo_actual = 'paradero'
                    frecuencia_total = self.g.vs[indice_nodo_actual]["frecuencia"]

                    # si el camino esta vacio agrego el primer nodo al string camino
                    if camino == '':

                        camino = nombre_nodo
                        camino_paradero = nombre_nodo
                        if nombre_nodo[:2] == 'M-':
                            metro_inicial = nombre_nodo

                    # si el camino no esta vacio, es la segunda iteracion y el nodo anterior es igual al actual por caminata
                    elif (n_iteracion == 2 and tipo_nodo_actual == tipo_nodo_anterior):
                        # print('entre 2')
                        camino = nombre_nodo
                        camino_paradero = nombre_nodo
                        metro_inicial = ''
                        if nombre_nodo[:2] == 'M-':
                            metro_inicial = nombre_nodo

                    # si es el ultimo nodo
                    elif (n == ultimo_nodo or self._hyperpath.vs[ultimo_nodo]['name2'] == nombre_nodo):

                        # si el nodo anterior es distinto al nodo actual
                        if tipo_nodo_anterior != tipo_nodo_actual:
                            # si es metro
                            if nombre_nodo[:2] == 'M-' and metro_inicial != '':
                                # print('entre 5')
                                metro_final = nombre_nodo

                                camino = camino + '/' + metro_final
                                camino_paradero = camino_paradero + '/' + metro_final

                                metro_final = ''
                                metro_inicial = ''

                            # si es bus
                            else:
                                camino = camino + '/' + nombre_nodo
                                camino_paradero = camino_paradero + '/' + nombre_nodo
                    # si es un nodo intermedio
                    else:
                        # si es metro
                        # print('entre donde debo entrar')
                        if nombre_nodo[:2] == 'M-' and metro_inicial == '':
                            metro_inicial = nombre_nodo

                            camino = camino + '/' + nombre_nodo
                            camino_paradero = camino_paradero + '/' + nombre_nodo

                        elif nombre_nodo[:2] == 'M-' and metro_inicial != '':
                            metro_final = nombre_nodo

                            camino = camino + '/' + metro_final
                            camino_paradero = camino_paradero + '/' + metro_final

                            metro_inicial = metro_final
                            metro_final = ''
                            serv_metro = ''

                        # si no es metro
                        else:
                            camino = camino + '/' + nombre_nodo
                            camino_paradero = camino_paradero + '/' + nombre_nodo

                # si el nodo no es un paradero (posee paradero/servicio)
                else:

                    tipo_nodo_actual = 'servicio'
                    frecuencia_arco = self.g.es[
                        self.g.get_eid(self.g.vs.find(name2=nodo_anterior).index, self.g.vs.find(name2=nombre_nodo).index,
                                  directed=True, error=True)]['frecuencia']

                    #si es arco de subida a bus
                    if frecuencia_arco < float('inf') and metro_inicial == '':
                        prob_arco = frecuencia_arco / frecuencia_total
                        prob_camino = prob_camino * prob_arco
                        servicio = nombre_nodo.split("/")[1]
                        camino = camino + '/' + servicio

                    #si es arco de subida a metro
                    if metro_inicial != '' and metro_final == '':
                        servicio = nombre_nodo.split("/")[1]
                        serv_metro = servicio
                        serv_metro = serv_metro.replace('V', '')
                        serv_metro = serv_metro.replace('R', '')
                        serv_metro = serv_metro.replace('-', '')
                        serv_metro = serv_metro.replace('I', '')
                        camino = camino + '/' + serv_metro

                nodo_anterior = nombre_nodo

                tipo_nodo_anterior = tipo_nodo_actual

            lista_caminos.append(camino)
        return lista_caminos

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

    def get_elemental_paths(self):

        return []

    def get_aggregated_paths(self):

        return []

    def plot_hyperpath(self):
        """ muestra una imagen de la hiper-ruta """
        self._hyperpath.vs["label"] = self._hyperpath.vs["name2"]
        color_dict = {"paradero": "red", "servicio": "pink"}
        self._hyperpath.vs["color"] = [color_dict[tipo] for tipo in self._hyperpath.vs["tipo"]]
        plot(self._hyperpath, bbox=(1000, 800), margin=20)

    #este metodo arroja un grafo igual al original puesto que es la hiper-ruta desde todos los origenes al destino
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
                print(nodo_seleccionado)
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
                t_colita = tpo_arco + tpo_nodo_a

                # si se baja de un servicio a un paradero y el paradero no es el destino se considera una penalizacion por trasbordo
                if g.vs[a]["tipo"] == 'paradero' and g.vs[desde]["tipo"] == 'servicio' and a != n_destination:
                    t_colita = t_colita + transfer_penalty

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
                        g.vs[desde]["tau"] = (waiting_penalty + frec_arco * t_colita) / float(((g.vs[desde]["frecuencia"]) + frec_arco))

                    else:
                        g.vs[desde]["tau"] = (float(g.vs[desde]["frecuencia"]) * (
                        g.vs[desde]["tau"]) + frec_arco * t_colita) / (float(g.vs[desde]["frecuencia"]) + frec_arco)

                    g.vs[desde]["frecuencia"] = (float(g.vs[desde]["frecuencia"]) + frec_arco)

                    conj_paradero[desde].append(((desde, a), t_colita))

                    heap.insertar((desde, g.vs[desde]["tau"]))

                for elemento in conj_paradero[desde]:

                    if elemento[1] > g.vs[desde]["tau"]:
                        conj_paradero[desde].remove(elemento)

                        frecuencia_arco = float(g.es[g.get_eid(elemento[0][0], elemento[0][1], directed=True, error=True)][
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
# print(a.travel_time)
# print(a.g)
# print(a.destination)
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
