import dill
import csv
from collections import defaultdict

dump_file2 = open('itinerario_minimo.pkl', 'rb')
itinerario_minimo = dill.load(dump_file2)
dump_file2.close()

dump_file3 = open('hiperruta_minimo.pkl', 'rb')
hiperruta_minimo = dill.load(dump_file3)
dump_file3.close()

dump_file2 = open('Dict_caminos.pkl', 'rb')
Dict_caminos = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('viajes_procesados.pkl', 'rb')
viajes = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('ruta_minima.pkl', 'rb')
ruta_minima = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('hiperruta_proporcion.pkl', 'rb')
hiperruta_proporcion = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('itinerario_minimo_proporcion.pkl', 'rb')
itinerario_minimo_proporcion = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('ruta_minima_proporcion.pkl', 'rb')
ruta_minima_proporcion = dill.load(dump_file2)
dump_file2.close()

with open('resumen.csv', mode='w') as csvFile:
    writer = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['origen', 'destino', 'total_viajes', 'viajes_en_hiperruta', 'viajes_en_ruta_min', 'viajes_en_it_min', 'largo_hiperruta', 'largo_ruta_minima', 'itinerarios_minimos', 'largo_caminos_usados', 'p_correcta_itinerario_minimo', 'p_correcta_hiperruta', 'p_correcta_ruta_minima'])


for destino in viajes:
    for origen in viajes[destino]:
        viajes_en_it_min = 0
        viajes_en_hiperruta = 0
        viajes_en_ruta_min = 0
        total_viajes = 0
        itinerarios_minimos = itinerario_minimo[origen][destino]
        largo_hiperruta = len(hiperruta_minimo[origen][destino])
        largo_caminos_usados = len(viajes[destino][origen])
        largo_ruta_minima = len(ruta_minima[origen][destino])
        p_correcta_itinerario_minimo = 0
        p_correcta_hiperruta = 0
        p_correcta_ruta_minima = 0

        for camino in viajes[destino][origen]:
            n_viajes = viajes[destino][origen][camino]
            total_viajes += n_viajes

        for camino in viajes[destino][origen]:
            n_viajes = viajes[destino][origen][camino]
            p_o = float(n_viajes) / float(total_viajes)

            if camino in itinerario_minimo[origen][destino]:
                viajes_en_it_min += n_viajes

                p_e = itinerario_minimo_proporcion[origen][destino][camino]
                p_correcta_itinerario_minimo += min(p_e,p_o)

            if camino in hiperruta_minimo[origen][destino]:
                viajes_en_hiperruta += n_viajes

                p_e = hiperruta_proporcion[origen][destino][camino]
                p_correcta_hiperruta += min(p_e, p_o)


            if camino in ruta_minima[origen][destino]:
                viajes_en_ruta_min += n_viajes

                p_e = ruta_minima_proporcion[origen][destino][camino]
                p_correcta_ruta_minima += min(p_e, p_o)


        with open('resumen.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([origen, destino, total_viajes, viajes_en_hiperruta, viajes_en_ruta_min, viajes_en_it_min, largo_hiperruta, largo_ruta_minima, itinerarios_minimos, largo_caminos_usados, p_correcta_itinerario_minimo, p_correcta_hiperruta, p_correcta_ruta_minima])
csvFile.close()

with open('viajes_realizados.csv', mode='w') as csvFile:
    writer = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['origen', 'destino', 'camino', 'viajes'])

for destino in viajes:
    for origen in viajes[destino]:
        for camino in viajes[destino][origen]:
            with open('viajes_realizados.csv', 'a') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow([origen, destino, camino, viajes[destino][origen][camino]])

csvFile.close()

with open('hiperrutas.csv', mode='w') as csvFile:
    writer = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['origen', 'destino', 'camino', 'viajes'])

for origen in hiperruta_minimo:
    for destino in hiperruta_minimo[origen]:
        for camino in hiperruta_minimo[origen][destino]:
            with open('hiperrutas.csv', 'a') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow([origen, destino, camino])

csvFile.close()

contador_h_R=0

with open('rutas_minimas.csv', mode='w') as csvFile:
    writer = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['origen', 'destino', 'camino', 'viajes'])

for origen in ruta_minima:
    for destino in ruta_minima[origen]:
        if len(ruta_minima[origen][destino]) == len(hiperruta_minimo[origen][destino]):
            contador_h_R += 1
        for camino in ruta_minima[origen][destino]:
            with open('rutas_minimas.csv', 'a') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow([origen, destino, camino])

csvFile.close()


print('contador_h_R', contador_h_R)
'''
print('itinerario_minimo')
print(hiperruta_minimo)
for origen in itinerario_minimo:
    for destino  in itinerario_minimo[origen]:
        for camino in itinerario_minimo[origen][destino]:
            print(origen, destino, camino)
'''


'''



print('hiperruta_minimo')
print(Dict_caminos[origen][destino])

for cam_par in Dict_caminos[origen][destino]:
    for cam in Dict_caminos[origen][destino][cam_par]:
        print(cam)

print("itinerario minimo")

ruta_min = q.shortest_paths_dijkstra(source = n_origen, target = n_destino, weights=q.es["peso"], mode=OUT)



print(itinerario_minimo[origen][destino])
'''

'''
print("alternativa agregada minima")

ruta_minima = defaultdict(lambda: defaultdict (list))

for cam_paradero in Dict_caminos[origen][destino]:
    print('cam_paradero', cam_paradero)
    paraderos = cam_paradero.split('/')
    par_anterior = ''
    serv_anteriores=[]
    serv_posteriores=[]
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
                    #print('para ver el problema')
                    #print(par_anterior+'/'+s, p+'/'+s)
                    #print(a, desde)
                    tpo_etapa += (dict_tiempos[s][p]- dict_tiempos[s][par_anterior])*frecuencia
                    serv_anteriores = serv_posteriores
                    #tpo_arco = g.es[g.get_eid(desde, a, directed=True, error=True)]['tpo_viaje']
            tpo_total += (1/tpo_espera) + (tpo_etapa/tpo_espera)
        par_anterior = p

    if tpo_total < tpo_ruta_agregada_minima:
        tpo_ruta_agregada_minima = tpo_total
        ruta_agregada_minima = cam_paradero

ruta_minima[origen][destino]=Dict_caminos[origen][destino][ruta_agregada_minima]

print(ruta_minima[origen][destino])
'''