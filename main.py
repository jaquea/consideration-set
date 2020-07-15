from igraph import *
import pickle
import dill

from hyperpath import Hyperpath

#se procesan los viajes
dump_file2 = open('tmp\\viajes_procesados.pkl', 'rb')
viajes = dill.load(dump_file2)
dump_file2.close()

viajes_p = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:0)))
viajes_p = viajes['T-8-71-PO-33']['T-20-68-NS-5']

#genero y leo grafo
dump_file1 = open('tmp\\grafo.igraph', 'rb')
g = pickle.load(dump_file1)
dump_file1.close()

dump_file2 = open('tmp\\paradero_cercano_dic.pkl', 'rb')
paradero_cercano_dic = dill.load(dump_file2)
dump_file2.close()

hiperruta_minimo = defaultdict(lambda: defaultdict (list))

cont = 0
for destino in viajes:
    cont += 1
    print(destino, cont)

    hyperpath_obj = Hyperpath(g, destination=destino, transfer_penalty=16,
                              waiting_penalty=2)

    hiper_ruta = hyperpath_obj._hyperpath

    destination_index = hiper_ruta.vs.find(name2=destino).index

    for ori in viajes[destino]:

        tpo_mas_corto = 1000

        for origen in paradero_cercano_dic[ori]:
            print(origen)

            if origen not in hiper_ruta.vs["name2"]:
                continue

            origin_index = hiper_ruta.vs.find(name2=origen).index

            path_set = hyperpath_obj.find_all_paths(origin_index, destination_index, maxlen=None, mode='OUT')

            format_path = hyperpath_obj.format_paths(path_set)

            for camino in format_path:

                if camino not in hiperruta_minimo[ori][destino]:
                    hiperruta_minimo[ori][destino].append(camino)

print(hiperruta_minimo)
