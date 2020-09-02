from HeapBinaria import HeapBinaria
from igraph import *

class Shortest():
    def __init__(self, grafo,  origin, destination, dict_servicio_llave_codigoTS):
        self.g = grafo
        self.destination = destination
        self.origin = origin
        self.origin_index = grafo.vs.find(name2=origin).index
        self.destination_index = grafo.vs.find(name2=destination).index
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
            nombre_nodo = self.g.vs[n]['name2']
            indice_nodo_actual = self.g.vs.find(name2=nombre_nodo).index
            if (self.g.vs["tipo"][indice_nodo_actual]) == 'paradero':

                tipo_nodo_actual = 'paradero'

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
                    n_paradero += 1
                    camino = nombre_nodo
                    camino_paradero = nombre_nodo
                    camino_resumido = nombre_nodo
                    metro_inicial = ''
                    if nombre_nodo[:2] == 'M-':
                        metro_inicial = nombre_nodo

                # si es el ultimo nodo
                elif (n == ultimo_nodo or self.g.vs[ultimo_nodo]['name2'] == nombre_nodo):
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

                    # si es bus
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
                if frecuencia_arco < float('inf') and tipo_nodo_anterior != 'servicio' and nodo_anterior[:2] != 'M-':
                    prob_arco = 1 #esto lo mantengo solamente porque estaba codificado desde antes
                    prob_camino = prob_camino * prob_arco
                    servicio = nombre_nodo.split("/")[1]
                    camino = camino + '/' + self.dict_servicio_llave_codigoTS[servicio][0]
                    camino_resumido = camino_resumido + '/' + self.dict_servicio_llave_codigoTS[servicio][0]

                # si es arco de subida a metro
                elif metro_inicial != '' and metro_final == '' and tipo_nodo_anterior != 'servicio' and nodo_anterior[:2]=='M-':
                    servicio = nombre_nodo.split("/")[1]
                    serv_metro = servicio
                    serv_metro = serv_metro.replace('V', '')
                    serv_metro = serv_metro.replace('R', '')
                    serv_metro = serv_metro.replace('-', '')
                    serv_metro = serv_metro.replace('I', '')
                    camino = camino + '/' + serv_metro

            nodo_anterior = nombre_nodo

            tipo_nodo_anterior = tipo_nodo_actual

        return camino, camino_paradero, prob_camino, camino_resumido

    def get_all_shortest_paths_desglosado(self):

        path_set = self.g.get_all_shortest_paths(self.origin_index, to=self.destination_index, weights=self.g.es["peso"],mode=OUT)
        path = []
        for j in path_set:
            camino = self.format_paths(j)[0]
            path.append(camino)
        return path



