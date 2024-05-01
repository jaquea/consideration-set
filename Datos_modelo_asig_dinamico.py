# -*- coding: utf-8 -*-
import glob
import json
import pickle
import time
from collections import defaultdict
import utm

import dill
from hyperpath import Hyperpath
import pandas as pd  # this is how I usually import pandas
from shortest_paths import Shortest

dump_file1 = open('tmp\\grafo_metro.igraph', 'rb')
g_metro = pickle.load(dump_file1)
dump_file1.close()

with open('inputs\\info_servicios.json') as data_file:
    data = json.loads(data_file.read())

df = pd.DataFrame.from_dict(data, orient='columns')
dict_servicio_llave_usuario = defaultdict(list)
dict_servicio_llave_codigoTS = defaultdict(list)

for idx, row in df.iterrows():
    sentido = row['sentido']
    servicio = str(row['servicio'])
    servicio_user = row['servicio_user']
    if servicio_user+"-"+sentido not in dict_servicio_llave_codigoTS[servicio]:
        dict_servicio_llave_codigoTS[servicio].append(servicio_user+"-"+sentido)
    if servicio not in dict_servicio_llave_usuario[servicio_user+"-"+sentido]:
        dict_servicio_llave_usuario[servicio_user+"-"+sentido].append(servicio)

# Funcion para leer todos los archivo csv del directorio indicado
# Los archivo deben tener extensión .csv

#####Obtenemos diccionario de paraderos cercanos#####

###diccionarios de localizacion geografica paraderos y estaciones de metro
df_paraderos = pd.read_csv('inputs\ConsolidadoParadas.csv')
df_metro = pd.read_csv('inputs\Diccionario-EstacionesMetro.csv')

radio = 200

#se genera diccionario para guardar coordenadas de paraderos
paraderos_coord_dic = defaultdict(list)
for idx, row in df_paraderos.iterrows():
    codigo_paradero = row['Codigo paradero TS']
    x = row['x']
    y = row['y']
    paraderos_coord_dic[codigo_paradero] = (x, y)

# print(paraderos_coord_dic)

df_metro_reducido = pd.read_csv('inputs\metro_stations.csv', delimiter=";") #diccionario que formo leonel

#se genera diccionario para asignar coordenadas de estaciones de metro
dict_metro = defaultdict(str)

for idx, row in df_metro_reducido.iterrows():
    codigo = row['codigo']
    estacion = row['estacion']
    dict_metro[estacion] = codigo

df_metro['x'] = df_metro[['LATITUD', 'LONGITUD']].apply(lambda x: round(utm.from_latlon(x[0], x[1])[0], 2), axis=1)
df_metro['y'] = df_metro[['LATITUD', 'LONGITUD']].apply(lambda x: round(utm.from_latlon(x[0], x[1])[1], 2), axis=1)

for idx, row in df_metro.iterrows():
    estacion = row['ESTANDAR']
    x = row['x']
    y = row['y']
    paraderos_coord_dic[dict_metro[estacion]] = (x,y)

paradero_cercano_dic = defaultdict(list)
for llave1 in paraderos_coord_dic:
    x1 = float(paraderos_coord_dic[llave1][0])
    y1 = float(paraderos_coord_dic[llave1][1])
    for llave2 in paraderos_coord_dic:
        x2 = float(paraderos_coord_dic[llave2][0])
        y2 = float(paraderos_coord_dic[llave2][1])
        # dist = (((x1-x2)**2) + ((y1-y2)**2))**0.5
        dist = abs(x1 - x2) + abs(y1 - y2)

        if dist <= radio and llave2 not in paradero_cercano_dic[llave1]:
            paradero_cercano_dic[llave1].append(llave2)


print(paradero_cercano_dic['M-PQ'])

print(paradero_cercano_dic['M-BA'])



########################



def leer_datos (path):

    '''path=r'C:\\Users\\jacke\\Desktop\\Datos_viajes\\viajes_input
        dataframe= leer_datos (path)' '''

    allFiles = glob.glob(path + "/*.csv")
    frame = pd.DataFrame()
    list_ = []
    for file_ in allFiles:
        print(file_)
        df = pd.read_csv(file_ ,index_col=None, header=0, encoding='latin-1', sep=',')
        list_.append(df)
    frame = pd.concat(list_)

    return frame

start_time = time.time()
#path_viajes =r'D:\\Datos_viajes\\viajes_input'
path_viajes ='D:\\Mayo2018\\2018-05-08.viajes'
df=pd.read_csv(path_viajes,index_col=None, encoding='latin-1', sep='|')
print('{0} secs'.format(time.time() - start_time))

df = df[df['paraderosubida'].isin(['PARQUE OHIGGINS', 'E-20-189-OP-40', 'E-20-188-NS-45', 'T-20-189-PO-6', 'E-20-188-SN-30', 'M-PQ', 'T-20-202-NS-25', 'E-20-189-PO-5'])]
df = df[df['paraderobajada'].isin (['BAQUEDANO','BAQUEDANO L1', 'BAQUEDANO L5','M-BA', 'E-20-53-OP-5', 'E-20-192-OP-5', 'E-20-53-PO-115', 'E-20-53-OP-10', 'E-14-134-SN-30', 'E-14-134-SN-35', 'E-14-128-PO-2'])]

#dates = pd.to_datetime(df['tiemposubida'], format='%Y%m%d %H:%M:%S', errors='ignore')
#dates = dates.map(lambda x: x.strftime('%Y-%m-%d'))
#dates.name = 'fecha'
#df = pd.concat([df, dates], axis=1)


#df = df[(df['fecha']=='2018-05-24')]

viajes_totales = len(df.id)
print('viajes totales=', viajes_totales)

#Selecciono viajes que tengan tiempo de caminata asignado
df=df[(df['netapa']==1) | ((df['netapa']==2) & (df['tcaminata_1era_etapa'].notnull())) | ((df['netapa']==3) & (df['tcaminata_1era_etapa'].notnull()) & (df['tcaminata_2da_etapa'].notnull()))].reset_index(drop=True)
print('viajes que tengan tiempo de caminata asignado', df.count()[0])

# Selecciono viajes que en total el tiempo de viaje sea superior o igual a 4 minutos
df = df[((df['tviaje_min'] > 4))].reset_index(drop=True)

print('viajes con tpo total de viaje superior a 4 min=', df.count()[0])


#para prediccion
#df_prediccion = df[(df['fecha']=='2018-05-24') | (df['fecha']=='2018-05-25') | (df['fecha']=='2018-05-28') | (df['fecha']=='2018-05-29') | (df['fecha']=='2018-05-30')]

#para estimacion
#df = df[(df['fecha']!='2018-05-24') & (df['fecha']!='2018-05-25') & (df['fecha']!='2018-05-28') & (df['fecha']!='2018-05-29') & (df['fecha']!='2018-05-30')]


df_metro_reducido = pd.read_csv('inputs\\metro_stations.csv', delimiter=";") #diccionario que formo leonel

dict_metro = defaultdict(str)

for idx, row in df_metro_reducido.iterrows():
    codigo = row['codigo']
    estacion = row['estacion']
    dict_metro[estacion] = codigo

#funcion que permite generar la ruta utilizando solo paraderos
def ODparaderos(x):

    if x[0]==1:
        if x[3]=='METRO':
            return ''.join([dict_metro[x[1]], '/', dict_metro[x[2]]])

        else:
            return ''.join([x[1], '/', x[2]])

    if x[0] == 2:
        if x[3] == 'METRO' and x[4]=='METRO':
            return ''.join([dict_metro[x[1]], '/', dict_metro[x[2]]])

        elif x[3] == 'METRO' and x[4]!='METRO':
            return ''.join([dict_metro[x[1]], '/', x[2]])

        elif x[3] != 'METRO' and x[4]=='METRO':
            return ''.join([x[1], '/', dict_metro[x[2]]])

        else:
            return ''.join([x[1], '/', x[2]])

    if x[0] == 3:
        if x[3] == 'METRO' and x[5] == 'METRO':
            return ''.join([dict_metro[x[1]], '/', dict_metro[x[2]]])

        elif x[3] == 'METRO' and x[5] != 'METRO':
            return ''.join([dict_metro[x[1]], '/', x[2]])

        elif x[3] != 'METRO' and x[5] == 'METRO':
            return ''.join([x[1], '/', dict_metro[x[2]]])

        else:
            return ''.join([x[1], '/', x[2]])

df['idx_OD_paradero'] = df[['netapa', 'paraderosubida', 'paraderobajada','tipotransporte_1era', 'tipotransporte_2da', 'tipotransporte_3era']].apply(ODparaderos, axis=1)

#df_prediccion['idx_OD_paradero'] = df_prediccion[['netapa', 'paraderosubida', 'paraderobajada','tipotransporte_1era', 'tipotransporte_2da', 'tipotransporte_3era']].apply(ODparaderos, axis=1)

def alternativas(x):

    #se busca servicio formato transantiago de la etapa 1 en diccionario para transformar en servicio formato usuario
    if x[3] in dict_servicio_llave_codigoTS:
        x[3] = dict_servicio_llave_codigoTS[x[3]][0]

    #(T506 06I pasa a T506 00I)si el servicio no se encuentra en el diccionario se trasnforma el texto quitandole el numero variante interno para ver si ahora encuentra el servicio en el diccionario
    else:
        servicio_variable = x[3].split(" ")
        servicio_modificado = ''

        # si el servicio es del estilo "T506 E0 00I"
        if len(servicio_variable) == 3:
            servicio_modificado = ''.join([servicio_variable[0], ' ', servicio_variable[1], ' ', '00', servicio_variable[2][-1]])

        # si el servicio es del estilo "T314 00I"
        elif len(servicio_variable) == 2:
            servicio_modificado = ''.join([servicio_variable[0], ' ', '00', servicio_variable[1][-1]])

        else:
            servicio_modificado = ''

        if servicio_modificado in dict_servicio_llave_codigoTS:
            x[3] = dict_servicio_llave_codigoTS[servicio_modificado][0]

    #mismo paso previo para la etapa 2
    if x[6] in dict_servicio_llave_codigoTS:
        x[6] = dict_servicio_llave_codigoTS[x[6]][0]

    # (T506 06I pasa a T506 00I)si el servicio no se encuentra en el diccionario se trasnforma el texto quitandole el numero variante interno para ver si ahora encuentra el servicio en el diccionario
    else:
        servicio_variable = x[6].split(" ")

        if len(servicio_variable) == 3:
            servicio_modificado = ''.join([servicio_variable[0], ' ', servicio_variable[1], ' ', '00', servicio_variable[2][-1]])

        elif len(servicio_variable) == 2:
            servicio_modificado = ''.join([servicio_variable[0], ' ', '00', servicio_variable[1][-1]])

        else:
            servicio_modificado = ''

        if servicio_modificado in dict_servicio_llave_codigoTS:
            x[6] = dict_servicio_llave_codigoTS[servicio_modificado][0]

    #mismo paso previo para el servicio de la etapa 3
    if x[9] in dict_servicio_llave_codigoTS:
        x[9] = dict_servicio_llave_codigoTS[x[9]][0]

    else:
        servicio_variable = x[9].split(" ")
        servicio_modificado = ''

        if len(servicio_variable) == 3:
            servicio_modificado = ''.join(
                [servicio_variable[0], ' ', servicio_variable[1], ' ', '00', servicio_variable[2][-1]])

        elif len(servicio_variable) == 2:
            servicio_modificado = ''.join([servicio_variable[0], ' ', '00', servicio_variable[1][-1]])

        else:
            servicio_modificado = ''

        if servicio_modificado in dict_servicio_llave_codigoTS:
            x[9] = dict_servicio_llave_codigoTS[servicio_modificado][0]


    #si el servicio de la primera etapa es metro
    if x[10] == 'METRO':
        x[1] = dict_metro[x[1]]
        x[2] = dict_metro[x[2]]
        cadena_alternativa = ''.join([x[1],'/',x[2]])
         #encuentra la ruta minima en metro
        shortest_path = Shortest(g_metro, x[1], x[2], dict_servicio_llave_codigoTS).get_all_shortest_paths_desglosado()[0]
        cadena_alternativa_desglosada = shortest_path
    else:
        cadena_alternativa = ''.join([x[1],'/',x[3],'/',x[2]])
        cadena_alternativa_desglosada = ''.join([x[1],'/',x[3],'/',x[2]])

    if x[0] == 1:
        return cadena_alternativa, cadena_alternativa_desglosada

    else:

        #si el servicio de la etapa 2 es metro
        if x[11] == 'METRO':
            x[4] = dict_metro[x[4]]
            x[5] = dict_metro[x[5]]

            # encuentra la ruta minima en metro
            shortest_path = Shortest(g_metro, x[4], x[5], dict_servicio_llave_codigoTS).get_all_shortest_paths_desglosado()[0]
            cadena_alternativa_desglosada = ''.join([cadena_alternativa_desglosada, '/', shortest_path])
            cadena_alternativa = ''.join([cadena_alternativa, '/', x[4], '/', x[5]])
        else:
            if x[2] == x[4]:
                cadena_alternativa = ''.join([cadena_alternativa, '/', x[6], '/', x[5]])
                cadena_alternativa_desglosada = ''.join([cadena_alternativa_desglosada, '/', x[6], '/', x[5]])

            else:
                cadena_alternativa = ''.join([cadena_alternativa, '/', x[4], '/', x[6], '/', x[5]])
                cadena_alternativa_desglosada = ''.join([cadena_alternativa_desglosada, '/', x[4], '/', x[6], '/', x[5]])
        if x[0] == 2:
            return cadena_alternativa, cadena_alternativa_desglosada

        else:

            if x[12] == 'METRO':
                x[7] = dict_metro[x[7]]
                x[8] = dict_metro[x[8]]

                shortest_path = Shortest(g_metro, x[7], x[8], dict_servicio_llave_codigoTS).get_all_shortest_paths_desglosado()[0]

                cadena_alternativa_desglosada = ''.join([cadena_alternativa_desglosada, '/', shortest_path])
                cadena_alternativa = ''.join([cadena_alternativa, '/', x[7], '/', x[8]])

            else:
                if x[5] == x[7]:
                    cadena_alternativa = ''.join([cadena_alternativa, '/', x[9], '/', x[8]])
                    cadena_alternativa_desglosada = ''.join([cadena_alternativa_desglosada, '/', x[9], '/', x[8]])

                else:
                    cadena_alternativa = ''.join([cadena_alternativa, '/', x[7], '/', x[9], '/', x[8]])
                    cadena_alternativa_desglosada = ''.join([cadena_alternativa_desglosada, '/', x[7], '/', x[9], '/', x[8]])
            return cadena_alternativa, cadena_alternativa_desglosada

def alternativas_func1(*args, **kwargs):
    return alternativas(*args, **kwargs)[0]

def alternativas_func2(*args, **kwargs):
    return alternativas(*args, **kwargs)[1]

df['alternativa_viaje']=df[['netapa',
                            'paraderosubida_1era','paraderobajada_1era','serv_1era_etapa',
                            'paraderosubida_2da','paraderobajada_2da','serv_2da_etapa',
                            'paraderosubida_3era','paraderobajada_3era','serv_3era_etapa',
                            'tipotransporte_1era', 'tipotransporte_2da', 'tipotransporte_3era']].apply(alternativas_func1, axis=1)


df['alternativa_viaje_desglosada']=df[['netapa',
                            'paraderosubida_1era','paraderobajada_1era','serv_1era_etapa',
                            'paraderosubida_2da','paraderobajada_2da','serv_2da_etapa',
                            'paraderosubida_3era','paraderobajada_3era','serv_3era_etapa',
                            'tipotransporte_1era', 'tipotransporte_2da', 'tipotransporte_3era']].apply(alternativas_func2, axis=1)

#registro el minuto de inicio de viaje
df['minuto'] = df.apply(lambda row: row.tiemposubida[11:16], axis=1)

df2 = df.groupby(['minuto', 'alternativa_viaje_desglosada']).count().reset_index()

df2.to_csv("C:\\Users\\afjg7\\OneDrive\\Escritorio\\datos_parOD_PQ_BQ_agregados.csv")

#df_sin_ZP = df[(df['tipotransporte_1era']!='ZP') & (df['tipotransporte_2da']!='ZP') &  (df['tipotransporte_3era']!='ZP') & (df['id']!='-')]

#print('viajes que no se realizan en zona paga', df_sin_ZP.count()[0])

#df_sin_ZP_sin_metro = df_sin_ZP[(df_sin_ZP['id']!='-') & ((df_sin_ZP['netapa']>1)|((df_sin_ZP['netapa']==1) & (df_sin_ZP['tipotransporte_1era']!='METRO')))]


#print('viajes que no se realizan en zona paga ni solo en metro', df_sin_ZP_sin_metro.count()[0])



'''
viajes = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:0)))
#diccionario para armar conjunto de consideracion con alternativas observadas
viajes_alternativas_desagregadas = defaultdict(lambda: defaultdict(list))
viajes_alternativas = defaultdict(lambda: defaultdict(list))
viajes_reales = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:0)))

#diccionarios para prediccion
viajes_prediccion_alternativas_desagregadas = defaultdict(lambda: defaultdict(list))
viajes_prediccion_alternativas = defaultdict(lambda: defaultdict(list))
viajes_prediccion_reales = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:0)))

for idx, row in df.iterrows():
    OD_paradero = row['idx_OD_paradero'].split("/")
    alternativa = row['alternativa_viaje']
    origen = OD_paradero[0]
    destino = OD_paradero[1]
    viajes[origen][destino][alternativa] += 1

for idx, row in df.iterrows():
    OD_paradero = row['idx_OD_paradero'].split("/")
    alternativa = row['alternativa_viaje']
    alternativa_desglosada = row['alternativa_viaje_desglosada']
    origen = OD_paradero[0]
    destino = OD_paradero[1]
    viajes_reales[origen][destino][alternativa] += 1
    if alternativa not in viajes_alternativas[origen][destino]:
        viajes_alternativas_desagregadas[origen][destino].append(alternativa_desglosada)
        viajes_alternativas[origen][destino].append(alternativa)

viajes_procesados = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
viajes_alternativas_desaglosadas_procesados  = defaultdict(lambda: defaultdict(list))
viajes_alternativas_procesados  = defaultdict(lambda: defaultdict(list))

cont = 0

for origen in viajes_reales:
    for destino in viajes_reales[origen]:
        cont +=1

        print('origen', origen, 'destino', destino)
        start_time = time.clock()
        grupo_subida = paradero_cercano_dic[origen]
        grupo_bajada = paradero_cercano_dic[destino]
        tuplas = [(x, y) for x in grupo_subida for y in grupo_bajada]

        for par in tuplas:
            if par[0] in viajes_reales and par[1] in viajes_reales[par[0]]:
                for camino in viajes_reales[par[0]][par[1]]:
                    viajes_procesados[destino][origen][camino] = viajes_reales[par[0]][par[1]][camino]


print(viajes_procesados)

print(viajes_procesados["M-PQ"])

print(viajes_procesados["M-PQ"]["M-BA"])

'''