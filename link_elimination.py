from k_shortest_paths import link_elimination
from collections import defaultdict
import dill
import os
import time
from constants import PROJECT_DIR
import pickle

dump_file1 = open('tmp\\viajes_alternativas_procesados.pkl', 'rb')
viajes_alternativas_procesados = dill.load(dump_file1)
dump_file1.close()

dump_file1 = open(os.path.join(PROJECT_DIR,'tmp','grafo.igraph'), 'rb')
g = pickle.load(dump_file1)
dump_file1.close()

dump_file1 = open(os.path.join(PROJECT_DIR, 'tmp', 'dict_servicio_llave_codigoTS.pkl'), 'rb')
dict_servicio_llave_codigoTS = pickle.load(dump_file1)
dump_file1.close()

dump_file2 = open('tmp\\viajes_prediccion_alternativas_procesados.pkl', 'rb')
viajes_prediccion_alternativas_procesados = dill.load(dump_file2)
dump_file2.close()

viajes_link_elimination_shortest_alternativas_desaglosadas_procesados = defaultdict(lambda: defaultdict(list))
viajes_link_elimination_shortest_alternativas_procesados = defaultdict(lambda: defaultdict(list))

viajes_link_elimination_shortest_alternativas_desaglosadas_procesados_prediccion = defaultdict(lambda: defaultdict(list))
viajes_link_elimination_shortest_alternativas_procesados_prediccion  = defaultdict(lambda: defaultdict(list))

cont = 0
num_k = 30
weights = "peso"

for origen in viajes_alternativas_procesados:
    for destino in viajes_alternativas_procesados[origen]:
        print('origen', origen, 'destino', destino)

        origin_index = g.vs.find(name2=origen).index
        destination_index = g.vs.find(name2=destino).index

        start_time = time.clock()
        k_paths_link_elimination = link_elimination(g, origin_index, destination_index, num_k, weights, dict_servicio_llave_codigoTS)
        print "link_elimination", time.clock() - start_time, "seconds"

        caminos_desglosados = k_paths_link_elimination[0]
        caminos_resumidos = k_paths_link_elimination[1]
        costos = k_paths_link_elimination[2]
        contador = 0

        for path in caminos_resumidos:
            if path not in viajes_link_elimination_shortest_alternativas_procesados[origen][destino]:
                costo_path = costos[contador]
                camino = caminos_desglosados[contador]

                viajes_link_elimination_shortest_alternativas_desaglosadas_procesados[origen][destino].append(camino)
                viajes_link_elimination_shortest_alternativas_procesados[origen][destino].append(path)
            contador += 1

dump_file2 = open('tmp\\viajes_link_elimination_shortest_alternativas_desaglosadas_procesados.pkl', 'wb')
dill.dump(viajes_link_elimination_shortest_alternativas_desaglosadas_procesados, dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_link_elimination_shortest_alternativas_procesados.pkl', 'wb')
dill.dump(viajes_link_elimination_shortest_alternativas_procesados, dump_file2)
dump_file2.close()

cont = 0
num_k = 30
weights = "peso"

for origen in viajes_prediccion_alternativas_procesados:
    for destino in viajes_prediccion_alternativas_procesados[origen]:
        print('origen', origen, 'destino', destino)

        origin_index = g.vs.find(name2=origen).index
        destination_index = g.vs.find(name2=destino).index

        start_time = time.clock()
        k_paths_link_elimination = link_elimination(g, origin_index, destination_index, num_k, weights, dict_servicio_llave_codigoTS)
        print "link_elimination", time.clock() - start_time, "seconds"

        caminos_desglosados = k_paths_link_elimination[0]
        caminos_resumidos = k_paths_link_elimination[1]
        costos = k_paths_link_elimination[2]
        contador = 0

        for path in caminos_resumidos:
            if path not in viajes_link_elimination_shortest_alternativas_procesados_prediccion[origen][destino]:
                costo_path = costos[contador]
                camino = caminos_desglosados[contador]

                viajes_link_elimination_shortest_alternativas_desaglosadas_procesados_prediccion[origen][destino].append(camino)
                viajes_link_elimination_shortest_alternativas_procesados_prediccion[origen][destino].append(path)
            contador += 1

dump_file2 = open('tmp\\viajes_link_elimination_shortest_alternativas_desaglosadas_procesados_prediccion.pkl', 'wb')
dill.dump(viajes_link_elimination_shortest_alternativas_desaglosadas_procesados_prediccion, dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_link_elimination_shortest_alternativas_procesados_prediccion.pkl', 'wb')
dill.dump(viajes_link_elimination_shortest_alternativas_procesados_prediccion, dump_file2)
dump_file2.close()
