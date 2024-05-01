from k_shortest_paths import simulation_observed_parameters
from k_shortest_paths import simulation
from collections import defaultdict
import dill
import os
import time
from constants import PROJECT_DIR
import pickle

#esto viene del archivo proces_viajes2.py
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

viajes_simulation_shortest_alternativas_desaglosadas_procesados = defaultdict(lambda: defaultdict(list))
viajes_simulation_shortest_alternativas_procesados = defaultdict(lambda: defaultdict(list))

viajes_simulation_shortest_alternativas_desaglosadas_procesados_observed_parameters = defaultdict(lambda: defaultdict(list))
viajes_simulation_shortest_alternativas_procesados_observed_parameters = defaultdict(lambda: defaultdict(list))

weights = "peso"
num_k = 30

for origen in viajes_alternativas_procesados:
    for destino in viajes_alternativas_procesados[origen]:
        print('origen', origen, 'destino', destino)

        origin_index = g.vs.find(name2=origen).index
        destination_index = g.vs.find(name2=destino).index

        start_time = time.clock()
        k_paths_simulation = simulation(g, origin_index, destination_index, num_k, weights, dict_servicio_llave_codigoTS, paradero_cercano_dic)
        print "simulacion", time.clock() - start_time, "seconds"

        # para simulacion
        caminos_desglosados = k_paths_simulation[0]
        caminos_resumidos = k_paths_simulation[1]
        costos = k_paths_simulation[2]
        contador = 0

        for path in caminos_resumidos:
            if path not in viajes_simulation_shortest_alternativas_procesados[origen][destino]:
                costo_path = costos[contador]
                camino = caminos_desglosados[contador]

                viajes_simulation_shortest_alternativas_desaglosadas_procesados[origen][destino].append(camino)
                viajes_simulation_shortest_alternativas_procesados[origen][destino].append(path)
            contador += 1


dump_file2 = open('tmp\\viajes_simulation_shortest_alternativas_desaglosadas_procesados.pkl', 'wb')
dill.dump(viajes_simulation_shortest_alternativas_desaglosadas_procesados, dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_simulation_shortest_alternativas_procesados.pkl', 'wb')
dill.dump(viajes_simulation_shortest_alternativas_procesados, dump_file2)
dump_file2.close()

#Simulacion con observed parameters

for origen in viajes_alternativas_procesados:
    for destino in viajes_alternativas_procesados[origen]:
        print('origen', origen, 'destino', destino)

        origin_index = g.vs.find(name2=origen).index
        destination_index = g.vs.find(name2=destino).index

        start_time = time.clock()
        k_paths_simulation = simulation_observed_parameters(g, origin_index, destination_index, num_k, weights, dict_servicio_llave_codigoTS, paradero_cercano_dic)
        print "simulacion", time.clock() - start_time, "seconds"

        # para simulacion
        caminos_desglosados = k_paths_simulation[0]
        caminos_resumidos = k_paths_simulation[1]
        costos = k_paths_simulation[2]
        contador = 0

        for path in caminos_resumidos:
            if path not in viajes_simulation_shortest_alternativas_procesados_observed_parameters[origen][destino]:
                costo_path = costos[contador]
                camino = caminos_desglosados[contador]

                viajes_simulation_shortest_alternativas_desaglosadas_procesados_observed_parameters[origen][destino].append(camino)
                viajes_simulation_shortest_alternativas_procesados_observed_parameters[origen][destino].append(path)
            contador += 1


dump_file2 = open('tmp\\viajes_simulation_shortest_alternativas_desaglosadas_procesados_observed_parameters.pkl', 'wb')
dill.dump(viajes_simulation_shortest_alternativas_desaglosadas_procesados_observed_parameters, dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_simulation_shortest_alternativas_procesados_observed_parameters.pkl', 'wb')
dill.dump(viajes_simulation_shortest_alternativas_procesados_observed_parameters, dump_file2)
dump_file2.close()
