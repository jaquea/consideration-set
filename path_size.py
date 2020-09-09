# -*- coding: utf-8 -*-
import json
import pandas as pd
import utm
from collections import defaultdict
import dill
import math


def obtener_arcos(df, servicio_user, sentido, par_subida, par_bajada):
    df_servicio = df[((df['servicio_user'] == servicio_user) & (df['sentido'] == sentido))]

    for id, row in df_servicio.iterrows():
        paradas = row['paradas']
        paradas_coords = row['paradas_coords']
        cabeza = ''
        contador = 0
        distancia_total = 0
        arcos = []
        paraderos = []
        contador_par_subida = 0

        for par in paradas:

            y1_long = paradas_coords[contador][0]
            x1_lat = paradas_coords[contador][1]
            x1 = utm.from_latlon(x1_lat, y1_long)[0]
            y1 = utm.from_latlon(x1_lat, y1_long)[1]
            par = par[0]
            # print(par)

            if contador_par_subida == 0 and par == par_subida:
                paraderos.append(par)
                cabeza = par
                contador_par_subida += 1

            if par != par_subida and contador_par_subida > 0:
                dist_arco = (((x1 - x2) ** 2) + ((y1 - y2) ** 2)) ** 0.5
                distancia_total += dist_arco
                arcos.append((cabeza, par, dist_arco))
                paraderos.append(par)
                cabeza = par

                if par == par_bajada:
                    if distancia_total == 0:
                        return None
                    else:
                        return [arcos, [distancia_total], paraderos]

            contador += 1
            x2 = x1
            y2 = y1


def distancia_sobrepuesta(lista1, lista2):
    paradero1 = lista1[2]
    paradero2 = lista2[2]
    dist_sobrepuesta = 0

    # primer paradero
    stop1_1 = paradero1[0]
    # ultimo paradero
    stop1_2 = paradero1[-1]

    stop2_1 = paradero2[0]
    stop2_2 = paradero2[-1]

    # caso1: ambos paraderos de la lista 1 están contendios en la lista 2
    if stop1_1 in paradero2 and stop1_2 in paradero2:
        return lista1[1][0]

    # caso2: el primer paradero de la lista 1 está contenido en la lista 2 pero el último paradero de la lista 1 no está contenido en la lista 2
    if stop1_1 in paradero2 and stop1_2 not in paradero2 and stop2_2 in paradero1:
        for row in lista1[0]:
            dist_arco = row[2]
            dist_sobrepuesta += dist_arco
            if row[1] == stop2_2:
                return dist_sobrepuesta

    # caso3: el último paradero de la lista 1 está contenido en la lista 2 pero el primer paradero de la lista 1 no está contenido en la lista 2
    if stop1_1 not in paradero2 and stop1_2 in paradero2 and stop2_1 in paradero1:
        comienzo = False
        for row in lista1[0]:
            dist_arco = row[2]
            if row[0] == stop2_1:
                # hago verdadero una variable para que después de encontrar el primer paradero de la lista 2 en la lista1 comience a sumar las distancias
                comienzo = True
            if comienzo:
                dist_sobrepuesta += dist_arco

        return dist_sobrepuesta

    # caso4: ambos paraderos de la lista 2 están contendios en la lista 1
    if stop2_1 in paradero1 and stop2_2 in paradero1:
        return lista2[1][0]

    # caso5: el primer paradero de la lista 1 está contenido en la lista 2 pero el último paradero de la lista 1 no está contenido en la lista 2, está contenido en el caso 3
    if stop2_1 in paradero1 and stop2_2 not in paradero1 and stop1_2 in paradero2:
        # print('entrecaso5')
        for row in lista2[0]:
            dist_arco = row[2]
            dist_sobrepuesta += dist_arco
            if row[1] == stop1_2:
                return dist_sobrepuesta

    # caso 6 está contenido en el caso 2

    return dist_sobrepuesta


##print(distancia_sobrepuesta (lista1, lista2))
##resultado es 466.19436059

def process_frame_alt(diccionario_alternativas, g):
    ps_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for origen in diccionario_alternativas:
        llavesubida = origen

        for destino in diccionario_alternativas[origen]:
            llavebajada = destino

            for alternativa in diccionario_alternativas[origen][destino]:
                estrategia = alternativa

                lista = estrategia.split('/')

                tipo_nodo_anterior = ''
                tipo_nodo_anterior_anterior = ''
                nodo_anterior_anterior = ''
                nodo_anterior = ''
                n_etapa = 0

                for n in lista:
                    # si el nodo es un paradero
                    if n in g.vs['name2'] and (g.vs["tipo"][g.vs.find(name2=n).index]) == 'paradero':
                        tipo_nodo_actual = 'paradero'

                        if tipo_nodo_anterior == 'servicio' and tipo_nodo_anterior_anterior == 'paradero':
                            n_etapa += 1
                            ruta = nodo_anterior
                            subida = nodo_anterior_anterior
                            bajada = n

                            llave = ''.join([llavesubida, '/', llavebajada])

                            ps_dict[llave][estrategia][n_etapa].append((ruta, subida, bajada))

                    else:
                        tipo_nodo_actual = 'servicio'

                    tipo_nodo_anterior_anterior = tipo_nodo_anterior
                    tipo_nodo_anterior = tipo_nodo_actual

                    nodo_anterior_anterior = nodo_anterior
                    nodo_anterior = n

    return ps_dict


def obtener_servicio_sentido(serv, sub, baj, dict_tiempos):
    if len(serv.split('-')) > 1:  # es servicio en bus
        serv1 = serv.split('-')[0]
        sentido = serv.split('-')[1]
        return (serv1, sentido)

    else:
        str1 = serv + 'V-I'
        str2 = serv + 'V-R'
        str3 = serv + 'R-I'
        str4 = serv + 'R-R'
        str5 = serv + '-I'
        str6 = serv + '-R'

        servicios = [str1, str2, str3, str4, str5, str6]

        for str in servicios:

            if str in dict_tiempos:
                dif = dict_tiempos[str][baj] - dict_tiempos[str][sub]
                if dif > 0 and dict_tiempos[str][baj] > -1 and dict_tiempos[str][sub] > -1:
                    serv1 = str.split('-')[0]
                    sentido = str.split('-')[1]

                    return (serv1, sentido)


def correlacion(df, PS, dict_tiempos):
    alerta = 0
    sin_asignacion = 0

    Path_Size_dist = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))

    for llave in PS:
        alerta += 1
        print('llave:', llave, 'alerta:', alerta)

        paradero_subida = llave.split('/')[0]
        paradero_bajada = llave.split('/')[1]

        for est in PS[llave]:

            distancia_estrategia = 0
            PS_estrategia = 0


            for et in PS[llave][est]:
                PS_etapa = 0
                distancia_etapa = 0

                # evaluo todos los servicios de la etapa
                for (serv, sub, baj) in PS[llave][est][et]:
                    serv_sentido = obtener_servicio_sentido(serv, sub, baj, dict_tiempos)

                    #si el servicio no se proceso en el diccionario de de llave transantiago
                    if serv_sentido == None:continue

                    serv = serv_sentido[0]
                    sentido = serv_sentido[1]

                    # obtengo arcos del servicio evaluado
                    obtener_arc = obtener_arcos(df, serv, sentido, sub, baj)

                    # print(obtener_arc)
                    if obtener_arc == None: continue

                    distancia_servicio = obtener_arc[1][0]

                    # variable que guarda la cantidad de alternativas que tienen el arco a
                    N_estrategia = 0

                    # máxima distancia sobrepuesta del servicio
                    distancia_sobrepuesta_estrategia = 0

                    for est2 in PS[llave]:  # recorro estrategias de la tupla
                        N_etapas = 0

                        for et2 in PS[llave][est2]:  # recorro etapa de la tupla
                            # print('\033[91m'+'\033[1m'+'etapa:'+'\033[0m',et2)
                            for (serv2, sub2, baj2) in PS[llave][est2][et2]:  # recorro servicio de la tupla

                                serv_sentido = obtener_servicio_sentido(serv2, sub2, baj2, dict_tiempos)

                                if serv_sentido == None:continue

                                serv2 = serv_sentido[0]
                                sentido2 = serv_sentido[1]
                                obtener_arcos2 = obtener_arcos(df, serv2, sentido2, sub2, baj2)

                                if obtener_arcos2 == None: continue

                                distancia_sobrep = distancia_sobrepuesta(obtener_arc, obtener_arcos2)

                                if distancia_sobrep > distancia_sobrepuesta_estrategia:
                                    distancia_sobrepuesta_estrategia = distancia_sobrep

                                if distancia_sobrep > 0:
                                    N_etapas += 1

                                # despues de recorrer todas las etapas
                                if N_etapas > 0:
                                    N_estrategia += 1

                    # después de recorrer todas las estrategias para verificar si el arco está incluido se suma
                    # la correlación del arco
                    PS_a = distancia_sobrepuesta_estrategia * math.log(1.0 / N_estrategia)

                    if PS_etapa >= PS_a:
                        distancia_etapa = distancia_servicio
                        PS_etapa = PS_a

                if distancia_etapa == 0:
                    Path_Size_dist[paradero_subida][paradero_bajada][est] = 10000
                    break

                # se suma la distancia de la etapa a la distancia total de la estrategia
                distancia_estrategia += distancia_etapa

                PS_estrategia += PS_etapa

            # print('distancia_estrategia',distancia_estrategia)
            # se calcula el path size de la de la estrategia

            if distancia_estrategia > 0:
                PS_estrategia = (1 / distancia_estrategia) * PS_estrategia


                # print('correlacion_estrategia', PS_estrategia)
                Path_Size_dist[paradero_subida][paradero_bajada][est] = PS_estrategia

            else:
                Path_Size_dist[paradero_subida][paradero_bajada][est] = 10000

    return Path_Size_dist


# print(process_frame_alt(viajes_alternativas_procesados,g)['T-13-104-PO-15/M-TB']['T-13-104-PO-15/401-I/E-13-54-SN-10/M-PM/L5/M-BA/L1/M-TB'])
# el resultado es defaultdict(<type 'list'>, {1: [(u'401-I', u'T-13-104-PO-15', u'E-13-54-SN-10')], 2: [(u'L5', u'M-PM', u'M-BA')], 3: [(u'L1', u'M-BA', u'M-TB')]})


def main():
    dump_file1 = open('tmp\\viajes_alternativas_desaglosadas_procesados.pkl', 'rb')
    viajes_alternativas_desaglosadas_procesados = dill.load(dump_file1)
    dump_file1.close()

    dump_file2 = open('tmp\\paradero_cercano_dic.pkl', 'rb')
    paradero_cercano_dic = dill.load(dump_file2)
    dump_file2.close()

    dump_file2 = open('tmp\\tiempos.pkl', 'rb')
    dict_tiempos = dill.load(dump_file2)
    dump_file2.close()

    viajes_alternativas_procesados_p = defaultdict(lambda: defaultdict(list))

    # hay una alternativa que va en sentido contrario
    # viajes_alternativas_procesados_p['E-14-170-NS-5']['L-17-19-35-PO'] = viajes_alternativas_desaglosadas_procesados['E-14-170-NS-5']['L-17-19-35-PO']
    #los paraderos del 109 no estan bien asignados
    #viajes_alternativas_procesados_p['T-13-104-PO-15']['M-TB'] = viajes_alternativas_desaglosadas_procesados['T-13-104-PO-15']['M-TB']
    # viajes_alternativas_procesados_p['T-13-54-SN-60']['M-TB'] = viajes_alternativas_procesados['T-13-54-SN-60']['M-TB']
    # viajes_alternativas_procesados_p['L-33-52-5-OP']['L-33-52-155-PO'] = viajes_alternativas_procesados['L-33-52-5-OP']['L-33-52-155-PO']
    # viajes_alternativas_procesados_p['M-CS']['T-18-156-PO-37']= viajes_alternativas_procesados['M-CS'] ['T-18-156-PO-37']

    viajes_alternativas_procesados = defaultdict(lambda: defaultdict(list))
    viajes_alternativas_procesados = viajes_alternativas_procesados_p

    dump_file1 = open('tmp\\grafo.igraph', 'rb')
    g = dill.load(dump_file1)
    dump_file1.close()

    with open('inputs\\info_servicios.json') as data_file:
        data = json.loads(data_file.read())

    df = pd.DataFrame.from_dict(data, orient='columns')

    PS = process_frame_alt(viajes_alternativas_procesados, g)
    # T-13-104-PO-15/109-R/E-13-278-PO-15/M-PM/L5/M-BA/L1/M-TB
    print('PS', PS['T-34-270-SN-30/T-31-134-SN-20']['T-13-104-PO-15/109-R/E-13-278-PO-15/M-PM/L5/M-BA/L1/M-TB'][2])
    print(viajes_alternativas_procesados)
    print(correlacion(df, PS, paradero_cercano_dic, dict_tiempos))


if __name__ == '__main__':
    main()
