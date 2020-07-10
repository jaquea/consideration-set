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
                a = nodo_seleccionado[0]
                if a not in S:
                    break

            S.append(a)

            for j in g.neighborhood(a, order=1, mode=IN)[1:]:

                desde = j

                # tiempo del arco evaluado
                tpo_arco = g.es[g.get_eid(desde, a, directed=True, error=True)]['tpo_viaje']
                tpo_nodo_a = min(g.vs[a]["tau"], g.vs[a]["tau_inf"])
                t_colita = tpo_arco + tpo_nodo_a

                # si se baja de un servicio a un paradero y el paradero no es el destino se considera una penalizacion por trasbordo
                if g.vs[a]["tipo"] == 'paradero' and g.vs[desde]["tipo"] == 'servicio' and a != n_destination:
                    t_colita = t_colita + transfer_penalty

                # frecuencia del arco, al inicio toma valor cero
                frec_arco = g.es[g.get_eid(desde, a, directed=True, error=True)]['frecuencia']

                # si es arco sin tiempo de espera
                if frec_arco == float('inf') and t_colita < g.vs[desde]["tau_inf"]:
                    g.vs[desde]["tau_inf"] = t_colita
                    conj_paradero_inf[desde] = [((desde, a), t_colita)]
                    heap.insertar((desde, t_colita))

                # si es arco con espera
                if frec_arco < float('inf') and t_colita < g.vs[desde]["tau"]:

                    if ((g.vs[desde]["frecuencia"]) == 0 and (g.vs[desde]["tau"]) == float('inf')):
                        g.vs[desde]["tau"] = (waiting_penalty + frec_arco * t_colita) / float(
                            ((g.vs[desde]["frecuencia"]) + frec_arco))

                    else:
                        g.vs[desde]["tau"] = ((g.vs[desde]["frecuencia"]) * (
                        g.vs[desde]["tau"]) + frec_arco * t_colita) / ((g.vs[desde]["frecuencia"]) + frec_arco)

                    g.vs[desde]["frecuencia"] = ((g.vs[desde]["frecuencia"]) + frec_arco)

                    conj_paradero[desde].append(((desde, a), t_colita))

                    heap.insertar((desde, g.vs[desde]["tau"]))

                for elemento in conj_paradero[desde]:

                    if elemento[1] > g.vs[desde]["tau"]:
                        conj_paradero[desde].remove(elemento)

                        frecuencia_arco = g.es[g.get_eid(elemento[0][0], elemento[0][1], directed=True, error=True)][
                            'frecuencia']
                        frecuencia_nodo = g.vs[elemento[0][0]]["frecuencia"]
                        tau_nodo = g.vs[elemento[0][0]]["tau"]
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
