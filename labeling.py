from k_shortest_paths import labeling_approach
from k_shortest_paths import labeling_approach_observed_parameters
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

dump_file2 = open('tmp\\paradero_cercano_dic.pkl', 'rb')
paradero_cercano_dic = dill.load(dump_file2)
dump_file2.close()

viajes_labeling_shortest_alternativas_desaglosadas_procesados = defaultdict(lambda: defaultdict(list))
viajes_labeling_shortest_alternativas_procesados = defaultdict(lambda: defaultdict(list))
viajes_labeling_shortest_alternativas_desaglosadas_procesados_observed_parameters  = defaultdict(lambda: defaultdict(list))
viajes_labeling_shortest_alternativas_procesados_observed_parameters  = defaultdict(lambda: defaultdict(list))


cont = 0
num_k = 30
weights = "peso"

largo = len(viajes_alternativas_procesados)
n_iteracion = 0

for origen in viajes_alternativas_procesados:
    n_iteracion += 1

    for destino in viajes_alternativas_procesados[origen]:
        print('origen', origen, 'destino', destino, "n", n_iteracion, "total", largo)

        origin_index = g.vs.find(name2=origen).index
        destination_index = g.vs.find(name2=destino).index

        transfer_metro_penalty = 14
        transfer_other_penalty = 14

        start_time = time.clock()
        k_paths_labeling = labeling_approach(g, origin_index, destination_index, weights, dict_servicio_llave_codigoTS,
                                             paradero_cercano_dic, transfer_metro_penalty, transfer_other_penalty)

        k_paths_labeling_observed_parameters = labeling_approach_observed_parameters(g, origin_index, destination_index, weights, dict_servicio_llave_codigoTS,
                                             paradero_cercano_dic)

        # para labelling
        caminos_desglosados = k_paths_labeling[0]
        caminos_resumidos = k_paths_labeling[1]
        costos = k_paths_labeling[2]
        contador = 0

        for path in caminos_resumidos:
            if path not in viajes_labeling_shortest_alternativas_procesados[origen][destino]:
                costo_path = costos[contador]
                camino = caminos_desglosados[contador]

                viajes_labeling_shortest_alternativas_desaglosadas_procesados[origen][destino].append(camino)
                viajes_labeling_shortest_alternativas_procesados[origen][destino].append(path)
            contador += 1

        # para labelling con observed parameters
        caminos_desglosados = k_paths_labeling[0] + k_paths_labeling_observed_parameters[0]
        caminos_resumidos = k_paths_labeling[1] + k_paths_labeling_observed_parameters[1]
        costos = k_paths_labeling[2] + k_paths_labeling_observed_parameters[2]
        contador = 0

        for path in caminos_resumidos:
            if path not in viajes_labeling_shortest_alternativas_procesados_observed_parameters[origen][destino]:
                costo_path = costos[contador]
                camino = caminos_desglosados[contador]

                viajes_labeling_shortest_alternativas_desaglosadas_procesados_observed_parameters[origen][destino].append(camino)
                viajes_labeling_shortest_alternativas_procesados_observed_parameters[origen][destino].append(path)
            contador += 1

    print "labeling", time.clock() - start_time, "seconds"

dump_file2 = open('tmp\\viajes_labeling_shortest_alternativas_desaglosadas_procesados.pkl', 'wb')
dill.dump(viajes_labeling_shortest_alternativas_desaglosadas_procesados, dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_labeling_shortest_alternativas_procesados.pkl', 'wb')
dill.dump(viajes_labeling_shortest_alternativas_procesados, dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_labeling_shortest_alternativas_desaglosadas_procesados_observed_parameters.pkl', 'wb')
dill.dump(viajes_labeling_shortest_alternativas_desaglosadas_procesados_observed_parameters, dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_labeling_shortest_alternativas_procesados_observed_parameters.pkl', 'wb')
dill.dump(viajes_labeling_shortest_alternativas_procesados_observed_parameters, dump_file2)
dump_file2.close()
