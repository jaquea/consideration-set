# -*- coding: utf-8 -*-
from igraph import *

def path_cost(graph, path, weights=None):
    pathcost = 0
    if len(path)>1:
        for i in range(len(path)-1):
            edge=graph.es.find(_source=path[i], _target=path[i+1])
            pathcost += edge[weights]
    return pathcost

def format_paths_k_shortest_path(graph, path, dict_servicio_llave_codigoTS):

    prob_camino = 1
    camino = ''
    camino_paradero = ''
    metro_inicial = ''
    metro_final = ''
    n_iteracion = 0
    n_anterior = ''
    tipo_nodo_anterior = ''
    ultimo_nodo = path[-1]
    nodo_anterior = ''
    n_paradero = 0
    camino_resumido = ''
    n_metro_intermedio = 0

    for n in path:
        n_iteracion += 1

        # si el nodo actual es un paradero
        nombre_nodo = graph.vs[n]['name2']
        indice_nodo_actual = graph.vs.find(name2=nombre_nodo).index
        #print(nodo_anterior, nombre_nodo)
        if (graph.vs["tipo"][indice_nodo_actual]) == 'paradero':

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
            elif (n == ultimo_nodo or graph.vs[ultimo_nodo]['name2'] == nombre_nodo):
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
            #print('nodo_anterior',nodo_anterior,'nombre_nodo',nombre_nodo)
            n_paradero = 0
            tipo_nodo_actual = 'servicio'
            #print(graph.vs.find(name2=nodo_anterior).index, graph.vs.find(name2=nombre_nodo).index)

            #print(graph.es[graph.get_eid('6310', '6260', directed=True, error=True)])
            frecuencia_arco = graph.es[
                graph.get_eid(n_anterior, n,
                               directed=True, error=True)]['frecuencia']
            #print('frecuencia', frecuencia_arco, 'metro_inicial', metro_inicial)
            # si es arco de subida a bus
            if frecuencia_arco < float('inf') and tipo_nodo_anterior != 'servicio' and nodo_anterior[:2]!='M-':
                servicio = nombre_nodo.split("/")[1]
                camino = camino + '/' + dict_servicio_llave_codigoTS[servicio][0]
                camino_resumido = camino_resumido + '/' + dict_servicio_llave_codigoTS[servicio][0]

            # si es arco de subida a metro
            elif metro_inicial != '' and metro_final == '' and tipo_nodo_anterior != 'servicio' and nodo_anterior[:2]=='M-':
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
        n_anterior = n

        tipo_nodo_anterior = tipo_nodo_actual

    return camino, camino_resumido

def in_lists(list1, list2):

    result = False
    node_result = -1

    if len(list1) < len(list2):
        toIter = list1
        toRefer = list2
    else:
        toIter = list2
        toRefer = list1

    for element in toIter:
        result = element in toRefer
        if result:
            node_result = element
            break

    return result, node_result

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    if len(lst3)>0:
        return True
    else:
        return False

def yen_igraph(g, source, target, num_k, weights, dict_servicio_llave_codigoTS, paradero_cercano_dic):
    import Queue
    graph_get_shortest_path = g.copy()
    tipo_nodo_origen = graph_get_shortest_path.vs["tipo"][source]
    tipo_nodo_destino = graph_get_shortest_path.vs["tipo"][target]

    if source == target:
        return [source], [source], [0]

    #setiamos en peso igual a cero a todos los arcos de caminata que estan proximos al origen
    #esto hara que los k caminos se busquen en el circulo de radio 100 mts
    for j in graph_get_shortest_path.neighborhood(source, order=1, mode=OUT)[1:]:
        tipo_nodo_vecino = graph_get_shortest_path.vs["tipo"][j]
        if tipo_nodo_origen == 'paradero' and tipo_nodo_vecino == 'paradero':
            edge = graph_get_shortest_path.get_eid(source, j, directed=True, error=True)
            #print(graph_get_shortest_path.es[edge].attributes())
            graph_get_shortest_path.es[edge]['peso'] = 0

    # setiamos en peso igual a cero a todos los arcos de caminata que estan proximos al destino
    # esto hara que los k caminos se busquen en el circulo de radio 100 mts
    for j in graph_get_shortest_path.neighborhood(target, order=1, mode=IN)[1:]:
        tipo_nodo_vecino = graph_get_shortest_path.vs["tipo"][j]
        if tipo_nodo_destino == 'paradero' and tipo_nodo_vecino == 'paradero':
            edge = graph_get_shortest_path.get_eid(j, target, directed=True, error=True)
            graph_get_shortest_path.es[edge]["peso"] = 0

    for arc in g.get_edgelist():
        arc_origen = arc[0]
        arc_destino = arc[1]
        tipo_nodo_origen = g.vs["tipo"][arc_origen]
        tipo_nodo_destino = g.vs["tipo"][arc_destino]

        edge_g = g.get_eid(arc_origen, arc_destino, directed=True, error=True)

        # si se baja de un servicio a un paradero y el paradero no es el destino se considera una penalizacion por trasbordo
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'servicio' and arc_destino != target and \
                g.vs[arc_destino]["name2"] not in paradero_cercano_dic[g.vs[target]["name2"]]:

            if g.vs[arc_origen]["name2"][:2] == 'M-' and g.vs[arc_destino]["name2"][:2] == 'M-':
                graph_get_shortest_path.es[edge]['peso'] = g.es[edge_g]['peso'] + 1

            else:
                graph_get_shortest_path.es[edge]['peso'] = g.es[edge_g]['peso'] + 1

    #Shortest path from the source to the target
    A = [graph_get_shortest_path.get_shortest_paths(source, to=target, weights=weights, output="vpath")[0]]

    A_costs = [path_cost(graph_get_shortest_path, A[0], weights)]

    #Initialize the heap to store the potential kth shortest path
    B = Queue.PriorityQueue()
    lista_caminos_distintos = []
    A_path_simple = []
    A_path_resumido = []

    # comparamos una lista de caminos resumidos puesto que diferentes trayectorias en metro no pueden ser reconocidas
    for path in A:
        path_simple = format_paths_k_shortest_path(g, path, dict_servicio_llave_codigoTS)[0]
        path_resumido = format_paths_k_shortest_path(g, path, dict_servicio_llave_codigoTS)[1]
        if path_resumido not in A_path_resumido:
            A_path_resumido.append(path_resumido)
            A_path_simple.append(path_simple)
            lista_caminos_distintos.append(A_path_resumido)

    for k in range(1, num_k):
        #recorre todos los nodos de un camino
        for i in range(len(A[k-1])-1):
            #Spur node is retrieved from the previous k-shortest path, k − 1
            spurNode = A[k-1][i]
            #The sequence of nodes from the source to the spur node of the previous k-shortest path
            rootPath = A[k-1][:i]

            #We store the removed edges
            removed_edges = []

            for path in A:
                if len(path) - 1 > i and rootPath == path[:i]:
                    #Remove the links that are part of the previous shortest paths which share the same root path
                    edge = graph_get_shortest_path.es.select(_source=path[i], _target=path[i+1])
                    if len(edge) == 0:
                        continue #edge already deleted
                    edge = edge[0]
                    removed_edges.append((path[i], path[i+1], edge.attributes()))
                    edge.delete()

            for n in range(len(rootPath)-1):
                if n != spurNode:
                    for j in graph_get_shortest_path.neighborhood(n, order=1, mode=OUT)[1:]:
                        edge = graph_get_shortest_path.es.select(_source=n, _target=j)
                        if len(edge) == 0:
                            continue  # edge already deleted
                        edge = edge[0]
                        removed_edges.append((n, j, edge.attributes()))
                        edge.delete()

                    if graph_get_shortest_path.is_directed():
                        for j in graph_get_shortest_path.neighborhood(n, order=1, mode=IN)[1:]:
                            edge = graph_get_shortest_path.es.select(_source=j, _target=n)
                            if len(edge) == 0:
                                continue  # edge already deleted
                            edge = edge[0]
                            removed_edges.append((j, n, edge.attributes()))
                            edge.delete()

            #Calculate the spur path from the spur node to the sink
            spurPath = graph_get_shortest_path.get_shortest_paths(spurNode, to=target, weights=weights, output="vpath")[0]

            encontro_camino = True
            if spurNode != target and len(spurPath) == 1:
                encontro_camino = False

            if target in spurPath and len(spurPath) > 0 and encontro_camino:
                #Entire path is made up of the root path and spur path
                totalPath = rootPath + spurPath
                totalPathCost = path_cost(graph_get_shortest_path, totalPath, weights)
                totalPathFormat = format_paths_k_shortest_path(g, totalPath, dict_servicio_llave_codigoTS)[0]
                totalPathFormatResumido = format_paths_k_shortest_path(g, totalPath, dict_servicio_llave_codigoTS)[1]
                nodes_totalPathFormat = totalPathFormat.split('/')

                #revisamos el penultimo nodo para evitar caminos que terminen con 3 caminatas o más al final del viaje 'L-34-80-10-SN/F01-I/L-34-40-220-PO/L-34-40-225-OP/F01c-R/L-34-76-20-SN/L-34-44-6-PO'
                if len(nodes_totalPathFormat)>1:
                    penultimo_nodo = nodes_totalPathFormat[-2]
                    if penultimo_nodo in g.vs["name2"]:
                        indice_penultimo_nodo = g.vs.find(name2=penultimo_nodo).index
                        tipo_penultimo_nodo = g.vs["tipo"][indice_penultimo_nodo]

                    else:
                        tipo_penultimo_nodo = 'servicio'

                    # revisamos el segundo nodo para evitar caminos que inicien con 3 caminatas o más al inicio del viaje
                    segundo_nodo = nodes_totalPathFormat[1]
                    if segundo_nodo in g.vs["name2"]:
                        indice_segundo_nodo = g.vs.find(name2=segundo_nodo).index
                        tipo_segundo_nodo = g.vs["tipo"][indice_segundo_nodo]

                    else:
                        tipo_segundo_nodo = 'servicio'

                else:
                    tipo_segundo_nodo = 'paradero'
                    tipo_penultimo_nodo = 'paradero'

                if totalPathFormatResumido not in lista_caminos_distintos and tipo_penultimo_nodo != 'paradero' and tipo_segundo_nodo != 'paradero':
                    #totalPath_set = set(totalPath)
                    #contains_duplicates = len(totalPath) != len(totalPath_set)
                    lista_caminos_distintos.append(totalPathFormatResumido)
                    B.put((totalPathCost, totalPath))

            #Add back the edges that were removed from the graph
            for removed_edge in removed_edges:
                node_start, node_end, cost = removed_edge
                graph_get_shortest_path.add_edge(node_start, node_end)
                edge = graph_get_shortest_path.es.select(_source=node_start, _target=node_end)[0]
                edge.update_attributes(cost)

        #Sort the potential k-shortest paths by cost
        #B is already sorted
        #Add the lowest cost path becomes the k-shortest path.

        if B.empty():
            break

        while True:
            cost_, path_ = B.get()
            path_simple = format_paths_k_shortest_path(g, path_, dict_servicio_llave_codigoTS)[0]
            path_resumido = format_paths_k_shortest_path(g, path_, dict_servicio_llave_codigoTS)[1]
            if path_resumido not in A_path_resumido:
                # We found a new path to add
                A_path_simple.append(path_simple)
                A_path_resumido.append(path_resumido)
                A.append(path_)
                A_costs.append(cost_)
                break

    return A_path_simple, A_path_resumido, A_costs


def yen_igraph_observed_parameters(g, source, target, num_k, weights, dict_servicio_llave_codigoTS, paradero_cercano_dic):
    import Queue
    graph_get_shortest_path = g.copy()
    tipo_nodo_origen = graph_get_shortest_path.vs["tipo"][source]
    tipo_nodo_destino = graph_get_shortest_path.vs["tipo"][target]

    if source == target:
        return [source], [source], [0]

    # setiamos en peso igual a cero a todos los arcos de caminata que estan proximos al origen
    # esto hara que los k caminos se busquen en el circulo de radio 100 mts
    for j in graph_get_shortest_path.neighborhood(source, order=1, mode=OUT)[1:]:
        tipo_nodo_vecino = graph_get_shortest_path.vs["tipo"][j]
        if tipo_nodo_origen == 'paradero' and tipo_nodo_vecino == 'paradero':
            edge = graph_get_shortest_path.get_eid(source, j, directed=True, error=True)
            # print(graph_get_shortest_path.es[edge].attributes())
            graph_get_shortest_path.es[edge]['peso'] = 0

    # setiamos en peso igual a cero a todos los arcos de caminata que estan proximos al destino
    # esto hara que los k caminos se busquen en el circulo de radio 100 mts
    for j in graph_get_shortest_path.neighborhood(target, order=1, mode=IN)[1:]:
        tipo_nodo_vecino = graph_get_shortest_path.vs["tipo"][j]
        if tipo_nodo_destino == 'paradero' and tipo_nodo_vecino == 'paradero':
            edge = graph_get_shortest_path.get_eid(j, target, directed=True, error=True)
            graph_get_shortest_path.es[edge]["peso"] = 0

    for arc in g.get_edgelist():
        arc_origen = arc[0]
        arc_destino = arc[1]
        tipo_nodo_origen = g.vs["tipo"][arc_origen]
        tipo_nodo_destino = g.vs["tipo"][arc_destino]

        edge_g = g.get_eid(arc_origen, arc_destino, directed=True, error=True)

        edge = graph_get_shortest_path.get_eid(arc_origen, arc_destino, directed=True, error=True)
        # si el arco es paradero->servicio se multiplica por 1.4 el tiempo de espera
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'servicio':
            graph_get_shortest_path.es[edge]['peso'] = 1.4 * g.es[edge_g]['peso']

        # si el arco es paradero->paradero se multiplica por 3 el tiempo de caminata y se asigna peso cero a caminaras alrededor de origen y destino
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'paradero':
            if arc_origen == source or arc_destino == target:
                graph_get_shortest_path.es[edge]['peso'] = 0

            else:
                graph_get_shortest_path.es[edge]['peso'] = 2.5 * g.es[edge_g]['peso']

        # si se baja de un servicio a un paradero y el paradero no es el destino se considera una penalizacion por trasbordo
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'servicio' and arc_destino != target and \
                g.vs[arc_destino]["name2"] not in paradero_cercano_dic[g.vs[target]["name2"]]:

            if g.vs[arc_origen]["name2"][:2] == 'M-' and g.vs[arc_destino]["name2"][:2] == 'M-':
                graph_get_shortest_path.es[edge]['peso'] = g.es[edge_g]['peso'] + 20.5

            else:
                graph_get_shortest_path.es[edge]['peso'] = g.es[edge_g]['peso'] + 20.5

    # Shortest path from the source to the target
    A = [graph_get_shortest_path.get_shortest_paths(source, to=target, weights=weights, output="vpath")[0]]

    A_costs = [path_cost(graph_get_shortest_path, A[0], weights)]

    # Initialize the heap to store the potential kth shortest path
    B = Queue.PriorityQueue()
    lista_caminos_distintos = []
    A_path_simple = []
    A_path_resumido = []

    # comparamos una lista de caminos resumidos puesto que diferentes trayectorias en metro no pueden ser reconocidas
    for path in A:
        path_simple = format_paths_k_shortest_path(g, path, dict_servicio_llave_codigoTS)[0]
        path_resumido = format_paths_k_shortest_path(g, path, dict_servicio_llave_codigoTS)[1]
        if path_resumido not in A_path_resumido:
            A_path_resumido.append(path_resumido)
            A_path_simple.append(path_simple)
            lista_caminos_distintos.append(A_path_resumido)

    for k in range(1, num_k):
        # recorre todos los nodos de un camino
        for i in range(len(A[k - 1]) - 1):
            # Spur node is retrieved from the previous k-shortest path, k − 1
            spurNode = A[k - 1][i]
            # The sequence of nodes from the source to the spur node of the previous k-shortest path
            rootPath = A[k - 1][:i]

            # We store the removed edges
            removed_edges = []

            for path in A:
                if len(path) - 1 > i and rootPath == path[:i]:
                    # Remove the links that are part of the previous shortest paths which share the same root path
                    edge = graph_get_shortest_path.es.select(_source=path[i], _target=path[i + 1])
                    if len(edge) == 0:
                        continue  # edge already deleted
                    edge = edge[0]
                    removed_edges.append((path[i], path[i + 1], edge.attributes()))
                    edge.delete()

            for n in range(len(rootPath) - 1):
                if n != spurNode:
                    for j in graph_get_shortest_path.neighborhood(n, order=1, mode=OUT)[1:]:
                        edge = graph_get_shortest_path.es.select(_source=n, _target=j)
                        if len(edge) == 0:
                            continue  # edge already deleted
                        edge = edge[0]
                        removed_edges.append((n, j, edge.attributes()))
                        edge.delete()

                    if graph_get_shortest_path.is_directed():
                        for j in graph_get_shortest_path.neighborhood(n, order=1, mode=IN)[1:]:
                            edge = graph_get_shortest_path.es.select(_source=j, _target=n)
                            if len(edge) == 0:
                                continue  # edge already deleted
                            edge = edge[0]
                            removed_edges.append((j, n, edge.attributes()))
                            edge.delete()

            # Calculate the spur path from the spur node to the sink
            spurPath = graph_get_shortest_path.get_shortest_paths(spurNode, to=target, weights=weights, output="vpath")[
                0]

            encontro_camino = True
            if spurNode != target and len(spurPath) == 1:
                encontro_camino = False

            if target in spurPath and len(spurPath) > 0 and encontro_camino:
                # Entire path is made up of the root path and spur path
                totalPath = rootPath + spurPath
                totalPathCost = path_cost(graph_get_shortest_path, totalPath, weights)
                totalPathFormat = format_paths_k_shortest_path(g, totalPath, dict_servicio_llave_codigoTS)[0]
                totalPathFormatResumido = format_paths_k_shortest_path(g, totalPath, dict_servicio_llave_codigoTS)[1]
                nodes_totalPathFormat = totalPathFormat.split('/')

                # revisamos el penultimo nodo para evitar caminos que terminen con 3 caminatas o más al final del viaje 'L-34-80-10-SN/F01-I/L-34-40-220-PO/L-34-40-225-OP/F01c-R/L-34-76-20-SN/L-34-44-6-PO'
                if len(nodes_totalPathFormat) > 1:
                    penultimo_nodo = nodes_totalPathFormat[-2]
                    if penultimo_nodo in g.vs["name2"]:
                        indice_penultimo_nodo = g.vs.find(name2=penultimo_nodo).index
                        tipo_penultimo_nodo = g.vs["tipo"][indice_penultimo_nodo]

                    else:
                        tipo_penultimo_nodo = 'servicio'

                    # revisamos el segundo nodo para evitar caminos que inicien con 3 caminatas o más al inicio del viaje
                    segundo_nodo = nodes_totalPathFormat[1]
                    if segundo_nodo in g.vs["name2"]:
                        indice_segundo_nodo = g.vs.find(name2=segundo_nodo).index
                        tipo_segundo_nodo = g.vs["tipo"][indice_segundo_nodo]

                    else:
                        tipo_segundo_nodo = 'servicio'

                else:
                    tipo_segundo_nodo = 'paradero'
                    tipo_penultimo_nodo = 'paradero'

                if totalPathFormatResumido not in lista_caminos_distintos and tipo_penultimo_nodo != 'paradero' and tipo_segundo_nodo != 'paradero':
                    # totalPath_set = set(totalPath)
                    # contains_duplicates = len(totalPath) != len(totalPath_set)
                    lista_caminos_distintos.append(totalPathFormatResumido)
                    B.put((totalPathCost, totalPath))

            # Add back the edges that were removed from the graph
            for removed_edge in removed_edges:
                node_start, node_end, cost = removed_edge
                graph_get_shortest_path.add_edge(node_start, node_end)
                edge = graph_get_shortest_path.es.select(_source=node_start, _target=node_end)[0]
                edge.update_attributes(cost)

        # Sort the potential k-shortest paths by cost
        # B is already sorted
        # Add the lowest cost path becomes the k-shortest path.

        if B.empty():
            break

        while True:
            cost_, path_ = B.get()
            path_simple = format_paths_k_shortest_path(g, path_, dict_servicio_llave_codigoTS)[0]
            path_resumido = format_paths_k_shortest_path(g, path_, dict_servicio_llave_codigoTS)[1]
            if path_resumido not in A_path_resumido:
                # We found a new path to add
                A_path_simple.append(path_simple)
                A_path_resumido.append(path_resumido)
                A.append(path_)
                A_costs.append(cost_)
                break

    return A_path_simple, A_path_resumido, A_costs

def link_elimination(g, source, target, num_k, weights, dict_servicio_llave_codigoTS, paradero_cercano_dic):
    import Queue

    graph_get_shortest_path = g.copy()
    tipo_nodo_origen = graph_get_shortest_path.vs["tipo"][source]
    tipo_nodo_destino = graph_get_shortest_path.vs["tipo"][target]

    #setiamos en peso igual a cero a todos los arcos de caminata que estan proximos al origen
    #esto hara que los k caminos se busquen en el circulo de radio 100 mts
    for j in graph_get_shortest_path.neighborhood(source, order=1, mode=OUT)[1:]:
        tipo_nodo_vecino = graph_get_shortest_path.vs["tipo"][j]
        if tipo_nodo_origen == 'paradero' and tipo_nodo_vecino == 'paradero':
            edge = graph_get_shortest_path.get_eid(source, j, directed=True, error=True)
            #print(graph_get_shortest_path.es[edge].attributes())
            graph_get_shortest_path.es[edge]['peso'] = 0

    # setiamos en peso igual a cero a todos los arcos de caminata que estan proximos al destino
    # esto hara que los k caminos se busquen en el circulo de radio 100 mts
    for j in graph_get_shortest_path.neighborhood(target, order=1, mode=IN)[1:]:
        tipo_nodo_vecino = graph_get_shortest_path.vs["tipo"][j]
        if tipo_nodo_destino == 'paradero' and tipo_nodo_vecino == 'paradero':
            edge = graph_get_shortest_path.get_eid(j, target, directed=True, error=True)
            graph_get_shortest_path.es[edge]["peso"] = 0

    for arc in g.get_edgelist():
        arc_origen = arc[0]
        arc_destino = arc[1]
        tipo_nodo_origen = g.vs["tipo"][arc_origen]
        tipo_nodo_destino = g.vs["tipo"][arc_destino]

        edge_g = g.get_eid(arc_origen, arc_destino, directed=True, error=True)

        # si se baja de un servicio a un paradero y el paradero no es el destino se considera una penalizacion por trasbordo
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'servicio' and arc_destino != target and \
                g.vs[arc_destino]["name2"] not in paradero_cercano_dic[g.vs[target]["name2"]]:

            if g.vs[arc_origen]["name2"][:2] == 'M-' and g.vs[arc_destino]["name2"][:2] == 'M-':
                graph_get_shortest_path.es[edge]['peso'] = g.es[edge_g]['peso'] + 1

            else:
                graph_get_shortest_path.es[edge]['peso'] = g.es[edge_g]['peso'] + 1

    #Shortest path from the source to the target
    A = [graph_get_shortest_path.get_shortest_paths(source, to=target, weights=weights, output="vpath")[0]]
    A_costs = [path_cost(graph_get_shortest_path, A[0], weights)]

    #inicializo la heap para luego encpntrar los caminos a los que se le removeran los arcos
    B = Queue.PriorityQueue()
    lista_caminos_distintos = []
    servicios_usados = []
    #recorro las rutas minimas encontradas y las agrego a la heap
    for path in A:
        path_format = format_paths_k_shortest_path(graph_get_shortest_path, path, dict_servicio_llave_codigoTS)[0]
        if path not in lista_caminos_distintos:
            lista_caminos_distintos.append(path_format)
            totalPathCost = path_cost(graph_get_shortest_path, path, weights)
            B.put((totalPathCost, path))

    contador = 0
    while (B.qsize() > 0 and contador < num_k):
        cost, path = B.get()
        contador += 1
        #vamos a recorrer todos los nodos excepto el ultimo
        for i in range(len(path)-1):
            #arco desde el nodo i al siguiente nodo
            edge = graph_get_shortest_path.es.select(_source=path[i], _target=path[i + 1])
            edge.delete()
            #calculamos el nuevo camino minimo
            NewPath = [graph_get_shortest_path.get_shortest_paths(source, to=target, weights=weights, output="vpath")[0]]

            #recorremos todos los caminos minimos
            for totalPath in NewPath:
                totalPathCost = path_cost(graph_get_shortest_path, totalPath, weights)
                # Añadir el nuevo camino minimo
                if totalPathCost > -1:
                    totalPathFormat = format_paths_k_shortest_path(g, totalPath, dict_servicio_llave_codigoTS)[0]
                    totalPathFormatResumido = format_paths_k_shortest_path(g, totalPath, dict_servicio_llave_codigoTS)[1]
                    nodes_totalPathFormat = totalPathFormat.split('/')

                    # revisamos el penultimo nodo para evitar caminos que terminen con 3 caminatas o más al final del viaje 'L-34-80-10-SN/F01-I/L-34-40-220-PO/L-34-40-225-OP/F01c-R/L-34-76-20-SN/L-34-44-6-PO'
                    if len(nodes_totalPathFormat) > 1:
                        penultimo_nodo = nodes_totalPathFormat[-2]
                        if penultimo_nodo in g.vs["name2"]:
                            indice_penultimo_nodo = g.vs.find(name2=penultimo_nodo).index
                            tipo_penultimo_nodo = g.vs["tipo"][indice_penultimo_nodo]

                        else:
                            tipo_penultimo_nodo = 'servicio'

                        # revisamos el segundo nodo para evitar caminos que inicien con 3 caminatas o más al inicio del viaje
                        segundo_nodo = nodes_totalPathFormat[1]
                        if segundo_nodo in g.vs["name2"]:
                            indice_segundo_nodo = g.vs.find(name2=segundo_nodo).index
                            tipo_segundo_nodo = g.vs["tipo"][indice_segundo_nodo]

                        else:
                            tipo_segundo_nodo = 'servicio'

                    else:
                        tipo_segundo_nodo = 'paradero'
                        tipo_penultimo_nodo = 'paradero'

                    if totalPathFormatResumido not in lista_caminos_distintos and tipo_penultimo_nodo != 'paradero' and tipo_segundo_nodo != 'paradero':
                        # totalPath_set = set(totalPath)
                        # contains_duplicates = len(totalPath) != len(totalPath_set)
                        lista_caminos_distintos.append(totalPathFormatResumido)
                        B.put((totalPathCost, totalPath))
                        A.append(totalPath)
                        A_costs.append(totalPathCost)

                        if len(A) >= num_k:
                            camino = []
                            costo_camino = []
                            camino_resumido = []
                            contador = 0

                            for path in A:
                                path_simple = format_paths_k_shortest_path(g, path, dict_servicio_llave_codigoTS)[0]
                                path_resumido = format_paths_k_shortest_path(g, path, dict_servicio_llave_codigoTS)[1]
                                if path_simple not in camino:
                                    camino.append(path_simple)
                                    costo_camino.append(A_costs[contador])
                                    camino_resumido.append(path_resumido)
                                contador += 1

                            return camino, camino_resumido, costo_camino

    camino = []
    costo_camino = []
    camino_resumido = []
    contador = 0

    for path in A:
        path_simple = format_paths_k_shortest_path(g, path, dict_servicio_llave_codigoTS)[0]
        path_resumido = format_paths_k_shortest_path(g, path, dict_servicio_llave_codigoTS)[1]
        if path_simple not in camino:
            camino.append(path_simple)
            costo_camino.append(A_costs[contador])
            camino_resumido.append(path_resumido)
        contador += 1

    return camino, camino_resumido, costo_camino

def link_elimination_observed_parameters(g, source, target, num_k, weights, dict_servicio_llave_codigoTS, paradero_cercano_dic):
    import Queue

    graph_get_shortest_path = g.copy()
    tipo_nodo_origen = graph_get_shortest_path.vs["tipo"][source]
    tipo_nodo_destino = graph_get_shortest_path.vs["tipo"][target]

    #setiamos en peso igual a cero a todos los arcos de caminata que estan proximos al origen
    #esto hara que los k caminos se busquen en el circulo de radio 100 mts
    for j in graph_get_shortest_path.neighborhood(source, order=1, mode=OUT)[1:]:
        tipo_nodo_vecino = graph_get_shortest_path.vs["tipo"][j]
        if tipo_nodo_origen == 'paradero' and tipo_nodo_vecino == 'paradero':
            edge = graph_get_shortest_path.get_eid(source, j, directed=True, error=True)
            #print(graph_get_shortest_path.es[edge].attributes())
            graph_get_shortest_path.es[edge]['peso'] = 0

    # setiamos en peso igual a cero a todos los arcos de caminata que estan proximos al destino
    # esto hara que los k caminos se busquen en el circulo de radio 100 mts
    for j in graph_get_shortest_path.neighborhood(target, order=1, mode=IN)[1:]:
        tipo_nodo_vecino = graph_get_shortest_path.vs["tipo"][j]
        if tipo_nodo_destino == 'paradero' and tipo_nodo_vecino == 'paradero':
            edge = graph_get_shortest_path.get_eid(j, target, directed=True, error=True)
            graph_get_shortest_path.es[edge]["peso"] = 0

    for arc in g.get_edgelist():
        arc_origen = arc[0]
        arc_destino = arc[1]
        tipo_nodo_origen = g.vs["tipo"][arc_origen]
        tipo_nodo_destino = g.vs["tipo"][arc_destino]

        edge_g = g.get_eid(arc_origen, arc_destino, directed=True, error=True)

        edge = graph_get_shortest_path.get_eid(arc_origen, arc_destino, directed=True, error=True)
        # si el arco es paradero->servicio se multiplica por 1.4 el tiempo de espera
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'servicio':
            graph_get_shortest_path.es[edge]['peso'] = 1.4 * g.es[edge_g]['peso']

        # si el arco es paradero->paradero se multiplica por 3 el tiempo de caminata y se asigna peso cero a caminaras alrededor de origen y destino
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'paradero':
            if arc_origen == source or arc_destino == target:
                graph_get_shortest_path.es[edge]['peso'] = 0

            else:
                graph_get_shortest_path.es[edge]['peso'] = 2.5 * g.es[edge_g]['peso']

        # si se baja de un servicio a un paradero y el paradero no es el destino se considera una penalizacion por trasbordo
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'servicio' and arc_destino != target and \
                g.vs[arc_destino]["name2"] not in paradero_cercano_dic[g.vs[target]["name2"]]:

            if g.vs[arc_origen]["name2"][:2] == 'M-' and g.vs[arc_destino]["name2"][:2] == 'M-':
                graph_get_shortest_path.es[edge]['peso'] = g.es[edge_g]['peso'] + 20.5

            else:
                graph_get_shortest_path.es[edge]['peso'] = g.es[edge_g]['peso'] + 20.5

    #Shortest path from the source to the target
    A = [graph_get_shortest_path.get_shortest_paths(source, to=target, weights=weights, output="vpath")[0]]
    A_costs = [path_cost(graph_get_shortest_path, A[0], weights)]

    #inicializo la heap para luego encpntrar los caminos a los que se le removeran los arcos
    B = Queue.PriorityQueue()
    lista_caminos_distintos = []
    servicios_usados = []
    #recorro las rutas minimas encontradas y las agrego a la heap
    for path in A:
        path_format = format_paths_k_shortest_path(graph_get_shortest_path, path, dict_servicio_llave_codigoTS)[0]
        if path not in lista_caminos_distintos:
            lista_caminos_distintos.append(path_format)
            totalPathCost = path_cost(graph_get_shortest_path, path, weights)
            B.put((totalPathCost, path))

    contador = 0
    while (B.qsize() > 0 and contador < num_k):
        cost, path = B.get()
        contador += 1
        #vamos a recorrer todos los nodos excepto el ultimo
        for i in range(len(path)-1):
            #arco desde el nodo i al siguiente nodo
            edge = graph_get_shortest_path.es.select(_source=path[i], _target=path[i + 1])
            edge.delete()
            #calculamos el nuevo camino minimo
            NewPath = [graph_get_shortest_path.get_shortest_paths(source, to=target, weights=weights, output="vpath")[0]]

            #recorremos todos los caminos minimos
            for totalPath in NewPath:
                totalPathCost = path_cost(graph_get_shortest_path, totalPath, weights)
                # Añadir el nuevo camino minimo
                if totalPathCost > -1:
                    totalPathFormat = format_paths_k_shortest_path(g, totalPath, dict_servicio_llave_codigoTS)[0]
                    totalPathFormatResumido = format_paths_k_shortest_path(g, totalPath, dict_servicio_llave_codigoTS)[1]
                    nodes_totalPathFormat = totalPathFormat.split('/')

                    # revisamos el penultimo nodo para evitar caminos que terminen con 3 caminatas o más al final del viaje 'L-34-80-10-SN/F01-I/L-34-40-220-PO/L-34-40-225-OP/F01c-R/L-34-76-20-SN/L-34-44-6-PO'
                    if len(nodes_totalPathFormat) > 1:
                        penultimo_nodo = nodes_totalPathFormat[-2]
                        if penultimo_nodo in g.vs["name2"]:
                            indice_penultimo_nodo = g.vs.find(name2=penultimo_nodo).index
                            tipo_penultimo_nodo = g.vs["tipo"][indice_penultimo_nodo]

                        else:
                            tipo_penultimo_nodo = 'servicio'

                        # revisamos el segundo nodo para evitar caminos que inicien con 3 caminatas o más al inicio del viaje
                        segundo_nodo = nodes_totalPathFormat[1]
                        if segundo_nodo in g.vs["name2"]:
                            indice_segundo_nodo = g.vs.find(name2=segundo_nodo).index
                            tipo_segundo_nodo = g.vs["tipo"][indice_segundo_nodo]

                        else:
                            tipo_segundo_nodo = 'servicio'

                    else:
                        tipo_segundo_nodo = 'paradero'
                        tipo_penultimo_nodo = 'paradero'

                    if totalPathFormatResumido not in lista_caminos_distintos and tipo_penultimo_nodo != 'paradero' and tipo_segundo_nodo != 'paradero':
                        # totalPath_set = set(totalPath)
                        # contains_duplicates = len(totalPath) != len(totalPath_set)
                        lista_caminos_distintos.append(totalPathFormatResumido)
                        B.put((totalPathCost, totalPath))
                        A.append(totalPath)
                        A_costs.append(totalPathCost)

                        if len(A) >= num_k:
                            camino = []
                            costo_camino = []
                            camino_resumido = []
                            contador = 0

                            for path in A:
                                path_simple = format_paths_k_shortest_path(g, path, dict_servicio_llave_codigoTS)[0]
                                path_resumido = format_paths_k_shortest_path(g, path, dict_servicio_llave_codigoTS)[1]
                                if path_simple not in camino:
                                    camino.append(path_simple)
                                    costo_camino.append(A_costs[contador])
                                    camino_resumido.append(path_resumido)
                                contador += 1

                            return camino, camino_resumido, costo_camino

    camino = []
    costo_camino = []
    camino_resumido = []
    contador = 0

    for path in A:
        path_simple = format_paths_k_shortest_path(g, path, dict_servicio_llave_codigoTS)[0]
        path_resumido = format_paths_k_shortest_path(g, path, dict_servicio_llave_codigoTS)[1]
        if path_simple not in camino:
            camino.append(path_simple)
            costo_camino.append(A_costs[contador])
            camino_resumido.append(path_resumido)
        contador += 1

    return camino, camino_resumido, costo_camino

def tipo_segundo_penultimo_nodo(g, totalPathFormat):
    nodes_totalPathFormat = totalPathFormat.split('/')
    # revisamos el penultimo nodo para evitar caminos que terminen con 3 caminatas o más al final del viaje 'L-34-80-10-SN/F01-I/L-34-40-220-PO/L-34-40-225-OP/F01c-R/L-34-76-20-SN/L-34-44-6-PO'
    if len(nodes_totalPathFormat) > 1:
        penultimo_nodo = nodes_totalPathFormat[-2]
        if penultimo_nodo in g.vs["name2"]:
            indice_penultimo_nodo = g.vs.find(name2=penultimo_nodo).index
            tipo_penultimo_nodo = g.vs["tipo"][indice_penultimo_nodo]

        else:
            tipo_penultimo_nodo = 'servicio'

        # revisamos el segundo nodo para evitar caminos que inicien con 3 caminatas o más al inicio del viaje
        segundo_nodo = nodes_totalPathFormat[1]
        if segundo_nodo in g.vs["name2"]:
            indice_segundo_nodo = g.vs.find(name2=segundo_nodo).index
            tipo_segundo_nodo = g.vs["tipo"][indice_segundo_nodo]

        else:
            tipo_segundo_nodo = 'servicio'

    else:
        tipo_segundo_nodo = 'paradero'
        tipo_penultimo_nodo = 'paradero'

    return tipo_segundo_nodo, tipo_penultimo_nodo

def labeling_approach(g, source, target, weights, dict_servicio_llave_codigoTS, paradero_cercano_dic, transfer_metro_penalty, transfer_other_penalty):
    graph_min_tt_in_vehicle = g.copy()
    graph_min_wt = g.copy()
    graph_min_transfer = g.copy()
    graph_min_walking_transfer = g.copy()
    graph_min_travel_time_1 = g.copy()
    graph_min_travel_time_2 = g.copy()
    graph_min_travel_time_3 = g.copy()
    graph_min_travel_time_4 = g.copy()
    graph_min_travel_time_5 = g.copy()

    lista_caminos_distintos = []
    A = []
    A_costs = []

    for arc in g.get_edgelist():
        arc_origen = arc[0]
        arc_destino = arc[1]
        tipo_nodo_origen = g.vs["tipo"][arc_origen]
        tipo_nodo_destino = g.vs["tipo"][arc_destino]


        edge_g = g.get_eid(arc_origen, arc_destino, directed=True, error=True)

        # 1) Minimal total in-vehicle travel time
        ##Si nodo origen es tipo servicio y nodo destino es tipo servicio
        edge = graph_min_tt_in_vehicle.get_eid(arc_origen, arc_destino, directed=True, error=True)
        if tipo_nodo_origen == 'servicio' and tipo_nodo_destino == 'servicio':
            graph_min_tt_in_vehicle.es[edge]['peso'] = g.es[edge_g]['peso']

        else:
            graph_min_tt_in_vehicle.es[edge]['peso'] = 0

        # 2) Minimal waiting time
        ##Si nodo origen es tipo paradero y nodo destino es tipo servicio
        edge = graph_min_wt.get_eid(arc_origen, arc_destino, directed=True, error=True)
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'servicio':
            graph_min_wt.es[edge]['peso'] = g.es[edge_g]['peso']

        else:
            graph_min_wt.es[edge]['peso'] = 0

        #3) Minimal number of transfers
        ## Si nodo origen es tipo servicio y nodo destino es tipo paradero
        edge = graph_min_transfer.get_eid(arc_origen, arc_destino, directed=True, error=True)
        if tipo_nodo_origen == 'servicio' and tipo_nodo_destino == 'paradero':
            graph_min_transfer.es[edge]['peso'] = 1

        else:
            graph_min_transfer.es[edge]['peso'] = 0

        #4) Minimal walking transfer time (no lo uso en el papaer)
        ## Si nodo origen es tipo paradero y nodo destino es tipo paradero
        edge = graph_min_walking_transfer.get_eid(arc_origen, arc_destino, directed=True, error=True)
        # si el arco es igual a paradero->paradero y no es arco de caminata en el origen ni en el destino del parOD evaluado
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'paradero' and arc_origen != source and arc_destino != target:
            graph_min_walking_transfer.es[edge]['peso'] = g.es[edge_g]['peso']

        else:
            graph_min_walking_transfer.es[edge]['peso'] = 0

        #5) Minimal total travel time( in -vehicle + waiting time + walking transfer time)
        edge = graph_min_travel_time_1.get_eid(arc_origen, arc_destino, directed=True, error=True)
        # si el arco es igual a paradero->paradero y es arco de caminata en el origen ni en el destino del parOD evaluado
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'paradero' and (arc_origen == source or arc_destino == target):
            graph_min_travel_time_1.es[edge]['peso'] = 0

        #6) Minimal total travel time (in-vehicle + 1*waiting time + 1*walking transfer time)
        edge = graph_min_travel_time_2.get_eid(arc_origen, arc_destino, directed=True, error=True)
        #si el arco es paradero->servicio se multiplica por 2 el tiempo de espera
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'servicio':
            graph_min_travel_time_2.es[edge]['peso'] = 1*g.es[edge_g]['peso']

        #si el arco es paradero->paradero se multiplica por 3 el tiepo de caminata y se asigna peso cero a caminaras alrededor de origen y destino
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'paradero':
            if arc_origen == source or arc_destino == target:
                graph_min_travel_time_2.es[edge]['peso'] = 0

            else:
                graph_min_travel_time_2.es[edge]['peso'] = 1 * g.es[edge_g]['peso']

        # 7) Minimal total travel time (in-vehicle + 5*waiting time + 3*walking transfer time)
        edge = graph_min_travel_time_3.get_eid(arc_origen, arc_destino, directed=True, error=True)
        # si el arco es paradero->servicio se multiplica por 2 el tiempo de espera
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'servicio':
            graph_min_travel_time_3.es[edge]['peso'] = 5 * g.es[edge_g]['peso']

        # si el arco es paradero->paradero se multiplica por 3 el tiepo de caminata y se asigna peso cero a caminaras alrededor de origen y destino
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'paradero':
            if arc_origen == source or arc_destino == target:
                graph_min_travel_time_3.es[edge]['peso'] = 0

            else:
                graph_min_travel_time_3.es[edge]['peso'] = 3 * g.es[edge_g]['peso']

        # 8) Minimal total travel time (in-vehicle + 5*waiting time + 5*walking transfer time)
        edge = graph_min_travel_time_4.get_eid(arc_origen, arc_destino, directed=True, error=True)
        # si el arco es paradero->servicio se multiplica por 2 el tiempo de espera
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'servicio':
            graph_min_travel_time_4.es[edge]['peso'] = 5 * g.es[edge_g]['peso']

        # si el arco es paradero->paradero se multiplica por 3 el tiepo de caminata y se asigna peso cero a caminaras alrededor de origen y destino
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'paradero':
            if arc_origen == source or arc_destino == target:
                graph_min_travel_time_4.es[edge]['peso'] = 0

            else:
                graph_min_travel_time_4.es[edge]['peso'] = 5 * g.es[edge_g]['peso']

        # 9) Minimal total travel time (in-vehicle + 5*waiting time + 8*walking transfer time)
        edge = graph_min_travel_time_5.get_eid(arc_origen, arc_destino, directed=True, error=True)
        # si el arco es paradero->servicio se multiplica por 2 el tiempo de espera
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'servicio':
            graph_min_travel_time_5.es[edge]['peso'] = 5 * g.es[edge_g]['peso']

        # si el arco es paradero->paradero se multiplica por 3 el tiepo de caminata y se asigna peso cero a caminaras alrededor de origen y destino
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'paradero':
            if arc_origen == source or arc_destino == target:
                graph_min_travel_time_5.es[edge]['peso'] = 0

            else:
                graph_min_travel_time_5.es[edge]['peso'] = 8 * g.es[edge_g]['peso']
        '''
        # 7) Minimal total travel time (in-vehicle + 2*waiting time + walking transfer time + 6*number of transfers between metro + 16*number of other transfers)
        edge = graph_min_travel_time_3.get_eid(arc_origen, arc_destino, directed=True, error=True)
        # si el arco es paradero->servicio se multiplica por 1.6 el tiempo de espera
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'servicio':
            graph_min_travel_time_3.es[edge]['peso'] = 1.6 * g.es[edge_g]['peso']

        # si el arco es paradero->paradero se multiplica por 3 el tiempo de caminata y se asigna peso cero a caminaras alrededor de origen y destino
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'paradero':
            if arc_origen == source or arc_destino == target:
                graph_min_travel_time_3.es[edge]['peso'] = 0

            else:
                graph_min_travel_time_3.es[edge]['peso'] = 3 * g.es[edge_g]['peso']

        # si se baja de un servicio a un paradero y el paradero no es el destino se considera una penalizacion por trasbordo
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'servicio' and arc_destino != target and g.vs[arc_destino]["name2"] not in paradero_cercano_dic[g.vs[target]["name2"]]:

            if g.vs[arc_origen]["name2"][:2] == 'M-' and g.vs[arc_destino]["name2"][:2] == 'M-':
                graph_min_travel_time_3.es[edge]['peso'] = g.es[edge_g]['peso'] + transfer_metro_penalty

            else:
                graph_min_travel_time_3.es[edge]['peso'] = g.es[edge_g]['peso'] + transfer_other_penalty
        '''
    # camino minimo min_tt_in_vehicle
    NewPath_1 = [graph_min_tt_in_vehicle.get_shortest_paths(source, to=target, weights=weights, output="vpath")[0]]

    # camino minimo min_wt
    NewPath_2 = [graph_min_wt.get_shortest_paths(source, to=target, weights=weights, output="vpath")[0]]

    # camino minimo min_transfer
    NewPath_3 = [graph_min_transfer.get_shortest_paths(source, to=target, weights=weights, output="vpath")[0]]

    # camino minimo min_walking_transfer
    NewPath_4 = [graph_min_walking_transfer.get_shortest_paths(source, to=target, weights=weights, output="vpath")[0]]

    # camino minimo min_travel_time_1
    NewPath_5 = [graph_min_travel_time_1.get_shortest_paths(source, to=target, weights=weights, output="vpath")[0]]

    # camino minimo min_travel_time_2
    NewPath_6 = [graph_min_travel_time_2.get_shortest_paths(source, to=target, weights=weights, output="vpath")[0]]

    # camino minimo min_travel_time_3
    NewPath_7 = [graph_min_travel_time_3.get_shortest_paths(source, to=target, weights=weights, output="vpath")[0]]

    # camino minimo min_travel_time_4
    NewPath_8 = [graph_min_travel_time_4.get_shortest_paths(source, to=target, weights=weights, output="vpath")[0]]

    # camino minimo min_travel_time_5
    NewPath_9 = [graph_min_travel_time_5.get_shortest_paths(source, to=target, weights=weights, output="vpath")[0]]

    # junto todas las rutas minimas encontradas
    NewPath = NewPath_1 + NewPath_2 + NewPath_3 + NewPath_4 + NewPath_5 + NewPath_6 + NewPath_7 + NewPath_8 + NewPath_9

    for totalPath in NewPath:
        totalPathCost = path_cost(graph_min_tt_in_vehicle, totalPath, weights)
        # Añadir el nuevo camino minimo
        if totalPathCost > -1:
            totalPathFormat = format_paths_k_shortest_path(g, totalPath, dict_servicio_llave_codigoTS)[0]
            totalPathFormatResumido = format_paths_k_shortest_path(g, totalPath, dict_servicio_llave_codigoTS)[1]
            tipo_segundo_nodo, tipo_penultimo_nodo = tipo_segundo_penultimo_nodo(g, totalPathFormat)
            if totalPathFormatResumido not in lista_caminos_distintos and tipo_penultimo_nodo != 'paradero' and tipo_segundo_nodo != 'paradero':
                lista_caminos_distintos.append(totalPathFormatResumido)
                A.append(totalPath)
                A_costs.append(totalPathCost)

    camino = []
    costo_camino = []
    camino_resumido = []
    contador = 0

    for path in A:
        path_simple = format_paths_k_shortest_path(g, path, dict_servicio_llave_codigoTS)[0]
        path_resumido = format_paths_k_shortest_path(g, path, dict_servicio_llave_codigoTS)[1]
        if path_simple not in camino:
            camino.append(path_simple)
            costo_camino.append(A_costs[contador])
            camino_resumido.append(path_resumido)
        contador += 1

    return camino, camino_resumido, costo_camino

#este es el labeling approach con los parametro provenientes del modelo de tarjetas inteligentes
def labeling_approach_observed_parameters(g, source, target, weights, dict_servicio_llave_codigoTS, paradero_cercano_dic):
    graph_min_tt_in_vehicle = g.copy()
    graph_min_travel_time_3 = g.copy()

    lista_caminos_distintos = []
    A = []
    A_costs = []

    for arc in g.get_edgelist():
        arc_origen = arc[0]
        arc_destino = arc[1]
        tipo_nodo_origen = g.vs["tipo"][arc_origen]
        tipo_nodo_destino = g.vs["tipo"][arc_destino]


        edge_g = g.get_eid(arc_origen, arc_destino, directed=True, error=True)

        # 7) Minimal total travel time (in-vehicle + 1.4*waiting time + 2.5*walking transfer time + 20.5*number of transfers)
        edge = graph_min_travel_time_3.get_eid(arc_origen, arc_destino, directed=True, error=True)
        # si el arco es paradero->servicio se multiplica por 1.6 el tiempo de espera
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'servicio':
            graph_min_travel_time_3.es[edge]['peso'] = 1.4 * g.es[edge_g]['peso']

        # si el arco es paradero->paradero se multiplica por 3 el tiempo de caminata y se asigna peso cero a caminaras alrededor de origen y destino
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'paradero':
            if arc_origen == source or arc_destino == target:
                graph_min_travel_time_3.es[edge]['peso'] = 0

            else:
                graph_min_travel_time_3.es[edge]['peso'] = 2.5 * g.es[edge_g]['peso']

        # si se baja de un servicio a un paradero y el paradero no es el destino se considera una penalizacion por trasbordo
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'servicio' and arc_destino != target and g.vs[arc_destino]["name2"] not in paradero_cercano_dic[g.vs[target]["name2"]]:

            if g.vs[arc_origen]["name2"][:2] == 'M-' and g.vs[arc_destino]["name2"][:2] == 'M-':
                graph_min_travel_time_3.es[edge]['peso'] = g.es[edge_g]['peso'] + 20.5

            else:
                graph_min_travel_time_3.es[edge]['peso'] = g.es[edge_g]['peso'] + 20.5

    # camino minimo min_travel_time_3
    NewPath_7 = [graph_min_travel_time_3.get_shortest_paths(source, to=target, weights=weights, output="vpath")[0]]

    # junto todas las rutas minimas encontradas
    NewPath = NewPath_7

    for totalPath in NewPath:
        totalPathCost = path_cost(graph_min_tt_in_vehicle, totalPath, weights)
        # Añadir el nuevo camino minimo
        if totalPathCost > -1:
            totalPathFormat = format_paths_k_shortest_path(g, totalPath, dict_servicio_llave_codigoTS)[0]
            totalPathFormatResumido = format_paths_k_shortest_path(g, totalPath, dict_servicio_llave_codigoTS)[1]
            tipo_segundo_nodo, tipo_penultimo_nodo = tipo_segundo_penultimo_nodo(g, totalPathFormat)
            if totalPathFormatResumido not in lista_caminos_distintos and tipo_penultimo_nodo != 'paradero' and tipo_segundo_nodo != 'paradero':
                lista_caminos_distintos.append(totalPathFormatResumido)
                A.append(totalPath)
                A_costs.append(totalPathCost)

    camino = []
    costo_camino = []
    camino_resumido = []
    contador = 0

    for path in A:
        path_simple = format_paths_k_shortest_path(g, path, dict_servicio_llave_codigoTS)[0]
        path_resumido = format_paths_k_shortest_path(g, path, dict_servicio_llave_codigoTS)[1]
        if path_simple not in camino:
            camino.append(path_simple)
            costo_camino.append(A_costs[contador])
            camino_resumido.append(path_resumido)
        contador += 1

    return camino, camino_resumido, costo_camino

def link_penalty(g, source, target, num_k, weights, dict_servicio_llave_codigoTS, paradero_cercano_dic):

    graph_get_shortest_path = g.copy()
    tipo_nodo_origen = graph_get_shortest_path.vs["tipo"][source]
    tipo_nodo_destino = graph_get_shortest_path.vs["tipo"][target]

    #setiamos en peso igual a cero a todos los arcos de caminata que estan proximos al origen
    #esto hara que los k caminos se busquen en el circulo de radio 100 mts
    for j in graph_get_shortest_path.neighborhood(source, order=1, mode=OUT)[1:]:
        tipo_nodo_vecino = graph_get_shortest_path.vs["tipo"][j]
        if tipo_nodo_origen == 'paradero' and tipo_nodo_vecino == 'paradero':
            edge = graph_get_shortest_path.get_eid(source, j, directed=True, error=True)
            #print(graph_get_shortest_path.es[edge].attributes())
            graph_get_shortest_path.es[edge]['peso'] = 0

    # setiamos en peso igual a cero a todos los arcos de caminata que estan proximos al destino
    # esto hara que los k caminos se busquen en el circulo de radio 100 mts
    for j in graph_get_shortest_path.neighborhood(target, order=1, mode=IN)[1:]:
        tipo_nodo_vecino = graph_get_shortest_path.vs["tipo"][j]
        if tipo_nodo_destino == 'paradero' and tipo_nodo_vecino == 'paradero':
            edge = graph_get_shortest_path.get_eid(j, target, directed=True, error=True)
            graph_get_shortest_path.es[edge]["peso"] = 0

    for arc in g.get_edgelist():
        arc_origen = arc[0]
        arc_destino = arc[1]
        tipo_nodo_origen = g.vs["tipo"][arc_origen]
        tipo_nodo_destino = g.vs["tipo"][arc_destino]

        edge_g = g.get_eid(arc_origen, arc_destino, directed=True, error=True)

        # si se baja de un servicio a un paradero y el paradero no es el destino se considera una penalizacion por trasbordo
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'servicio' and arc_destino != target and \
                g.vs[arc_destino]["name2"] not in paradero_cercano_dic[g.vs[target]["name2"]]:

            if g.vs[arc_origen]["name2"][:2] == 'M-' and g.vs[arc_destino]["name2"][:2] == 'M-':
                graph_get_shortest_path.es[edge]['peso'] = g.es[edge_g]['peso'] + 1

            else:
                graph_get_shortest_path.es[edge]['peso'] = g.es[edge_g]['peso'] + 1

    A_costs = []
    A = []
    lista_caminos_distintos = []
    iteracion = 0
    while (iteracion<num_k):

        iteracion += 1
        NewPath = [graph_get_shortest_path.get_shortest_paths(source, to=target, weights=weights, output="vpath")[0]]

        #recorro las rutas minimas encontradas y las agrego a la heap
        for totalPath in NewPath:
            totalPathCost = path_cost(graph_get_shortest_path, totalPath, weights)
            # Añadir el nuevo camino minimo
            if totalPathCost > -1:
                totalPathFormat = format_paths_k_shortest_path(g, totalPath, dict_servicio_llave_codigoTS)[0]
                totalPathFormatResumido = format_paths_k_shortest_path(g, totalPath, dict_servicio_llave_codigoTS)[1]
                tipo_segundo_nodo, tipo_penultimo_nodo = tipo_segundo_penultimo_nodo(g, totalPathFormat)
                if totalPathFormatResumido not in lista_caminos_distintos and tipo_penultimo_nodo != 'paradero' and tipo_segundo_nodo != 'paradero':
                    lista_caminos_distintos.append(totalPathFormatResumido)
                    A.append(totalPath)
                    A_costs.append(totalPathCost)

            #vamos a recorrer todos los nodos excepto el ultimo
            for i in range(len(totalPath)-1):
            #arco desde el nodo i al siguiente nodo
                edge = graph_get_shortest_path.get_eid(totalPath[i], totalPath[i + 1], directed=True, error=True)
                # print(graph_get_shortest_path.es[edge].attributes())
                nuevo_costo = graph_get_shortest_path.es[edge]['peso']*1.2
                graph_get_shortest_path.es[edge]['peso'] = nuevo_costo
    camino = []
    costo_camino = []
    camino_resumido = []
    contador = 0

    for path in A:
        path_simple = format_paths_k_shortest_path(g, path, dict_servicio_llave_codigoTS)[0]
        path_resumido = format_paths_k_shortest_path(g, path, dict_servicio_llave_codigoTS)[1]
        if path_simple not in camino:
            camino.append(path_simple)
            costo_camino.append(A_costs[contador])
            camino_resumido.append(path_resumido)
        contador += 1

    return camino, camino_resumido, costo_camino

def link_penalty_observed_parameters(g, source, target, num_k, weights, dict_servicio_llave_codigoTS, paradero_cercano_dic):

    graph_get_shortest_path = g.copy()
    tipo_nodo_origen = graph_get_shortest_path.vs["tipo"][source]
    tipo_nodo_destino = graph_get_shortest_path.vs["tipo"][target]

    #setiamos en peso igual a cero a todos los arcos de caminata que estan proximos al origen
    #esto hara que los k caminos se busquen en el circulo de radio 100 mts
    for j in graph_get_shortest_path.neighborhood(source, order=1, mode=OUT)[1:]:
        tipo_nodo_vecino = graph_get_shortest_path.vs["tipo"][j]
        if tipo_nodo_origen == 'paradero' and tipo_nodo_vecino == 'paradero':
            edge = graph_get_shortest_path.get_eid(source, j, directed=True, error=True)
            #print(graph_get_shortest_path.es[edge].attributes())
            graph_get_shortest_path.es[edge]['peso'] = 0

    # setiamos en peso igual a cero a todos los arcos de caminata que estan proximos al destino
    # esto hara que los k caminos se busquen en el circulo de radio 100 mts
    for j in graph_get_shortest_path.neighborhood(target, order=1, mode=IN)[1:]:
        tipo_nodo_vecino = graph_get_shortest_path.vs["tipo"][j]
        if tipo_nodo_destino == 'paradero' and tipo_nodo_vecino == 'paradero':
            edge = graph_get_shortest_path.get_eid(j, target, directed=True, error=True)
            graph_get_shortest_path.es[edge]["peso"] = 0

    for arc in g.get_edgelist():
        arc_origen = arc[0]
        arc_destino = arc[1]
        tipo_nodo_origen = g.vs["tipo"][arc_origen]
        tipo_nodo_destino = g.vs["tipo"][arc_destino]

        edge_g = g.get_eid(arc_origen, arc_destino, directed=True, error=True)

        edge = graph_get_shortest_path.get_eid(arc_origen, arc_destino, directed=True, error=True)
        # si el arco es paradero->servicio se multiplica por 1.4 el tiempo de espera
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'servicio':
            graph_get_shortest_path.es[edge]['peso'] = 1.4 * g.es[edge_g]['peso']

        # si el arco es paradero->paradero se multiplica por 3 el tiempo de caminata y se asigna peso cero a caminaras alrededor de origen y destino
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'paradero':
            if arc_origen == source or arc_destino == target:
                graph_get_shortest_path.es[edge]['peso'] = 0

            else:
                graph_get_shortest_path.es[edge]['peso'] = 2.5 * g.es[edge_g]['peso']

        # si se baja de un servicio a un paradero y el paradero no es el destino se considera una penalizacion por trasbordo
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'servicio' and arc_destino != target and \
                g.vs[arc_destino]["name2"] not in paradero_cercano_dic[g.vs[target]["name2"]]:

            graph_get_shortest_path.es[edge]['peso'] = g.es[edge_g]['peso'] + 20.5

    A_costs = []
    A = []
    lista_caminos_distintos = []
    iteracion = 0
    while (iteracion<num_k):

        iteracion += 1
        NewPath = [graph_get_shortest_path.get_shortest_paths(source, to=target, weights=weights, output="vpath")[0]]

        #recorro las rutas minimas encontradas y las agrego a la heap
        for totalPath in NewPath:
            totalPathCost = path_cost(graph_get_shortest_path, totalPath, weights)
            # Añadir el nuevo camino minimo
            if totalPathCost > -1:
                totalPathFormat = format_paths_k_shortest_path(g, totalPath, dict_servicio_llave_codigoTS)[0]
                totalPathFormatResumido = format_paths_k_shortest_path(g, totalPath, dict_servicio_llave_codigoTS)[1]
                tipo_segundo_nodo, tipo_penultimo_nodo = tipo_segundo_penultimo_nodo(g, totalPathFormat)
                if totalPathFormatResumido not in lista_caminos_distintos and tipo_penultimo_nodo != 'paradero' and tipo_segundo_nodo != 'paradero':
                    lista_caminos_distintos.append(totalPathFormatResumido)
                    A.append(totalPath)
                    A_costs.append(totalPathCost)

            #vamos a recorrer todos los nodos excepto el ultimo
            for i in range(len(totalPath)-1):
            #arco desde el nodo i al siguiente nodo
                edge = graph_get_shortest_path.get_eid(totalPath[i], totalPath[i + 1], directed=True, error=True)
                # print(graph_get_shortest_path.es[edge].attributes())
                nuevo_costo = graph_get_shortest_path.es[edge]['peso']*1.2
                graph_get_shortest_path.es[edge]['peso'] = nuevo_costo
    camino = []
    costo_camino = []
    camino_resumido = []
    contador = 0

    for path in A:
        path_simple = format_paths_k_shortest_path(g, path, dict_servicio_llave_codigoTS)[0]
        path_resumido = format_paths_k_shortest_path(g, path, dict_servicio_llave_codigoTS)[1]
        if path_simple not in camino:
            camino.append(path_simple)
            costo_camino.append(A_costs[contador])
            camino_resumido.append(path_resumido)
        contador += 1

    return camino, camino_resumido, costo_camino

def simulation(g, source, target, num_k, weights, dict_servicio_llave_codigoTS, paradero_cercano_dic):

    import numpy as np

    graph_get_shortest_path = g.copy()
    tipo_nodo_origen = graph_get_shortest_path.vs["tipo"][source]
    tipo_nodo_destino = graph_get_shortest_path.vs["tipo"][target]

    #setiamos en peso igual a cero a todos los arcos de caminata que estan proximos al origen
    #esto hara que los k caminos se busquen en el circulo de radio 100 mts
    for j in graph_get_shortest_path.neighborhood(source, order=1, mode=OUT)[1:]:
        tipo_nodo_vecino = graph_get_shortest_path.vs["tipo"][j]
        if tipo_nodo_origen == 'paradero' and tipo_nodo_vecino == 'paradero':
            edge = graph_get_shortest_path.get_eid(source, j, directed=True, error=True)
            #print(graph_get_shortest_path.es[edge].attributes())
            graph_get_shortest_path.es[edge]['peso'] = 0

    # setiamos en peso igual a cero a todos los arcos de caminata que estan proximos al destino
    # esto hara que los k caminos se busquen en el circulo de radio 100 mts
    for j in graph_get_shortest_path.neighborhood(target, order=1, mode=IN)[1:]:
        tipo_nodo_vecino = graph_get_shortest_path.vs["tipo"][j]
        if tipo_nodo_destino == 'paradero' and tipo_nodo_vecino == 'paradero':
            edge = graph_get_shortest_path.get_eid(j, target, directed=True, error=True)
            graph_get_shortest_path.es[edge]["peso"] = 0

    for arc in g.get_edgelist():
        arc_origen = arc[0]
        arc_destino = arc[1]
        tipo_nodo_origen = g.vs["tipo"][arc_origen]
        tipo_nodo_destino = g.vs["tipo"][arc_destino]

        edge_g = g.get_eid(arc_origen, arc_destino, directed=True, error=True)

        # si se baja de un servicio a un paradero y el paradero no es el destino se considera una penalizacion por trasbordo
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'servicio' and arc_destino != target and \
                g.vs[arc_destino]["name2"] not in paradero_cercano_dic[g.vs[target]["name2"]]:

            graph_get_shortest_path.es[edge]['peso'] = g.es[edge_g]['peso'] + 1

    A_costs = []
    A = []
    lista_caminos_distintos = []

    iteracion = 0
    while (iteracion < num_k):
        iteracion += 1

        for arc in graph_get_shortest_path.get_edgelist():
            arc_origen = arc[0]
            arc_destino = arc[1]

            edge_g = graph_get_shortest_path.get_eid(arc_origen, arc_destino, directed=True, error=True)

            nuevo_costo = abs(graph_get_shortest_path.es[edge_g]['peso'] + 2 * graph_get_shortest_path.es[edge_g]['peso'] * np.random.standard_normal())
            graph_get_shortest_path.es[edge_g]['peso'] = nuevo_costo

            NewPath = [graph_get_shortest_path.get_shortest_paths(source, to=target, weights=weights, output="vpath")[0]]

            #recorro las rutas minimas encontradas y las agrego a la heap
            for totalPath in NewPath:
                totalPathCost = path_cost(graph_get_shortest_path, totalPath, weights)
                # Añadir el nuevo camino minimo
                if totalPathCost > -1:
                    totalPathFormat = format_paths_k_shortest_path(g, totalPath, dict_servicio_llave_codigoTS)[0]
                    totalPathFormatResumido = format_paths_k_shortest_path(g, totalPath, dict_servicio_llave_codigoTS)[1]
                    tipo_segundo_nodo, tipo_penultimo_nodo = tipo_segundo_penultimo_nodo(g, totalPathFormat)
                    if totalPathFormatResumido not in lista_caminos_distintos and tipo_penultimo_nodo != 'paradero' and tipo_segundo_nodo != 'paradero':
                        lista_caminos_distintos.append(totalPathFormatResumido)
                        A.append(totalPath)
                        A_costs.append(totalPathCost)

            camino = []
            costo_camino = []
            camino_resumido = []
            contador = 0

            for path in A:
                path_simple = format_paths_k_shortest_path(g, path, dict_servicio_llave_codigoTS)[0]
                path_resumido = format_paths_k_shortest_path(g, path, dict_servicio_llave_codigoTS)[1]
                if path_simple not in camino:
                    camino.append(path_simple)
                    costo_camino.append(A_costs[contador])
                    camino_resumido.append(path_resumido)
                contador += 1

    return camino, camino_resumido, costo_camino


def simulation_observed_parameters(g, source, target, num_k, weights, dict_servicio_llave_codigoTS, paradero_cercano_dic):
    import numpy as np

    graph_get_shortest_path = g.copy()
    tipo_nodo_origen = graph_get_shortest_path.vs["tipo"][source]
    tipo_nodo_destino = graph_get_shortest_path.vs["tipo"][target]

    # setiamos en peso igual a cero a todos los arcos de caminata que estan proximos al origen
    # esto hara que los k caminos se busquen en el circulo de radio 100 mts
    for j in graph_get_shortest_path.neighborhood(source, order=1, mode=OUT)[1:]:
        tipo_nodo_vecino = graph_get_shortest_path.vs["tipo"][j]
        if tipo_nodo_origen == 'paradero' and tipo_nodo_vecino == 'paradero':
            edge = graph_get_shortest_path.get_eid(source, j, directed=True, error=True)
            # print(graph_get_shortest_path.es[edge].attributes())
            graph_get_shortest_path.es[edge]['peso'] = 0

    # setiamos en peso igual a cero a todos los arcos de caminata que estan proximos al destino
    # esto hara que los k caminos se busquen en el circulo de radio 100 mts
    for j in graph_get_shortest_path.neighborhood(target, order=1, mode=IN)[1:]:
        tipo_nodo_vecino = graph_get_shortest_path.vs["tipo"][j]
        if tipo_nodo_destino == 'paradero' and tipo_nodo_vecino == 'paradero':
            edge = graph_get_shortest_path.get_eid(j, target, directed=True, error=True)
            graph_get_shortest_path.es[edge]["peso"] = 0

    for arc in g.get_edgelist():
        arc_origen = arc[0]
        arc_destino = arc[1]
        tipo_nodo_origen = g.vs["tipo"][arc_origen]
        tipo_nodo_destino = g.vs["tipo"][arc_destino]

        edge_g = g.get_eid(arc_origen, arc_destino, directed=True, error=True)

        edge = graph_get_shortest_path.get_eid(arc_origen, arc_destino, directed=True, error=True)
        # si el arco es paradero->servicio se multiplica por 1.4 el tiempo de espera
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'servicio':
            graph_get_shortest_path.es[edge]['peso'] = 1.4 * g.es[edge_g]['peso']

        # si el arco es paradero->paradero se multiplica por 3 el tiempo de caminata y se asigna peso cero a caminaras alrededor de origen y destino
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'paradero':
            if arc_origen == source or arc_destino == target:
                graph_get_shortest_path.es[edge]['peso'] = 0

            else:
                graph_get_shortest_path.es[edge]['peso'] = 2.5 * g.es[edge_g]['peso']

        # si se baja de un servicio a un paradero y el paradero no es el destino se considera una penalizacion por trasbordo
        if tipo_nodo_origen == 'paradero' and tipo_nodo_destino == 'servicio' and arc_destino != target and \
                g.vs[arc_destino]["name2"] not in paradero_cercano_dic[g.vs[target]["name2"]]:
            graph_get_shortest_path.es[edge]['peso'] = g.es[edge_g]['peso'] + 20.5

    A_costs = []
    A = []
    lista_caminos_distintos = []

    iteracion = 0
    while (iteracion < num_k):
        iteracion += 1

        for arc in graph_get_shortest_path.get_edgelist():
            arc_origen = arc[0]
            arc_destino = arc[1]

            edge_g = graph_get_shortest_path.get_eid(arc_origen, arc_destino, directed=True, error=True)

            nuevo_costo = abs(graph_get_shortest_path.es[edge_g]['peso'] + 2 * graph_get_shortest_path.es[edge_g][
                'peso'] * np.random.standard_normal())
            graph_get_shortest_path.es[edge_g]['peso'] = nuevo_costo

            NewPath = [
                graph_get_shortest_path.get_shortest_paths(source, to=target, weights=weights, output="vpath")[0]]

            # recorro las rutas minimas encontradas y las agrego a la heap
            for totalPath in NewPath:
                totalPathCost = path_cost(graph_get_shortest_path, totalPath, weights)
                # Añadir el nuevo camino minimo
                if totalPathCost > -1:
                    totalPathFormat = format_paths_k_shortest_path(g, totalPath, dict_servicio_llave_codigoTS)[0]
                    totalPathFormatResumido = format_paths_k_shortest_path(g, totalPath, dict_servicio_llave_codigoTS)[
                        1]
                    tipo_segundo_nodo, tipo_penultimo_nodo = tipo_segundo_penultimo_nodo(g, totalPathFormat)
                    if totalPathFormatResumido not in lista_caminos_distintos and tipo_penultimo_nodo != 'paradero' and tipo_segundo_nodo != 'paradero':
                        lista_caminos_distintos.append(totalPathFormatResumido)
                        A.append(totalPath)
                        A_costs.append(totalPathCost)

            camino = []
            costo_camino = []
            camino_resumido = []
            contador = 0

            for path in A:
                path_simple = format_paths_k_shortest_path(g, path, dict_servicio_llave_codigoTS)[0]
                path_resumido = format_paths_k_shortest_path(g, path, dict_servicio_llave_codigoTS)[1]
                if path_simple not in camino:
                    camino.append(path_simple)
                    costo_camino.append(A_costs[contador])
                    camino_resumido.append(path_resumido)
                contador += 1

    return camino, camino_resumido, costo_camino
