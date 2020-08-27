# coding=utf-8
#genera diccionarios que contienen el numero de viajes que no se realizan en zona paga ni solo en metro,
#también genera un diccionario de viajes reales, viajes_reales[origen][destino][alternativa]
#se crean las alternativa de viaje utilizada y se asigna un indice de par OD

import glob
import json
import pickle
import time
from collections import defaultdict

import dill
import numpy as np
import pandas as pd  # this is how I usually import pandas

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
path_viajes ='D:\\Datos_viajes\\viajes_input\\Mayo_2018'
df=leer_datos(path_viajes)
print('{0} secs'.format(time.time() - start_time))

dates = pd.to_datetime(df['tiemposubida'], format='%Y%m%d %H:%M:%S', errors='ignore')
dates = dates.map(lambda x: x.strftime('%Y-%m-%d'))
dates.name = 'fecha'
df = pd.concat([df, dates], axis=1)

viajes_totales = len(df.id)
print('viajes totales=', viajes_totales)

#Selecciono viajes que tengan tiempo de caminata asignado
df=df[(df['netapa']==1) | ((df['netapa']==2) & (df['tcaminata_1era_etapa'].notnull())) | ((df['netapa']==3) & (df['tcaminata_1era_etapa'].notnull()) & (df['tcaminata_2da_etapa'].notnull()))].reset_index(drop=True)
print('viajes que tengan tiempo de caminata asignado', df.count()[0])

# Selecciono viajes que en total el tiempo de viaje sea superior o igual a 4 minutos
df = df[((df['tviaje_min'] > 4))].reset_index(drop=True)

print('viajes con tpo total de viaje superior a 4 min=', df.count()[0])

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

def alternativas(x):

    #se busca servicio formato transantiago de la etapa 1 en diccionario para transformar en servicio formato usuario
    if x[3] in dict_servicio_llave_codigoTS:
        x[3] = dict_servicio_llave_codigoTS[x[3]][0]

    #(T506 06I pasa a T506 00I)si el servicio no se encuentra en el diccionario se trasnforma el texto quitandole el numero variante interno para ver si ahora encuentra el servicio en el diccionario
    else:
        servicio_variable = x[3].split(" ")
        servicio_modificado = ''

        if len(servicio_variable) == 3:
            servicio_modificado = ''.join([servicio_variable[0], ' ', servicio_variable[1], ' ', '00', servicio_variable[2][-1]])

        elif len(servicio_variable) == 2:
            servicio_modificado = ''.join([servicio_variable[0], ' ', '00', servicio_variable[1][-1]])

        else:
            servicio_modificado = ''

        print(servicio_modificado)
        if servicio_modificado in dict_servicio_llave_codigoTS:
            x[3] = dict_servicio_llave_codigoTS[servicio_modificado][0]

    #mismo paso previo para la etapa 2
    if x[6] in dict_servicio_llave_codigoTS:
        x[6] = dict_servicio_llave_codigoTS[x[6]][0]

    # (T506 06I pasa a T506 00I)si el servicio no se encuentra en el diccionario se trasnforma el texto quitandole el numero variante interno para ver si ahora encuentra el servicio en el diccionario
    else:
        servicio_variable = x[6].split(" ")
        servicio_modificado = ''

        if len(servicio_variable) == 3:
            servicio_modificado = ''.join(
                [servicio_variable[0], ' ', servicio_variable[1], ' ', '00', servicio_variable[2][-1]])

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

    else:
        cadena_alternativa = ''.join([x[1],'/',x[3],'/',x[2]])

    if x[0] == 1:
        return cadena_alternativa

    else:

        #si el servicio de la etapa 2 es metro
        if x[11] == 'METRO':
            x[4] = dict_metro[x[4]]
            x[5] = dict_metro[x[5]]
            cadena_alternativa = ''.join([cadena_alternativa, '/', x[4], '/', x[5]])

        else:
            if x[2] == x[4]:
                cadena_alternativa = ''.join([cadena_alternativa, '/', x[6], '/', x[5]])

            else:
                cadena_alternativa = ''.join([cadena_alternativa, '/', x[4], '/', x[6], '/', x[5]])

        if x[0] == 2:

            return cadena_alternativa

        else:

            if x[12] == 'METRO':
                x[7] = dict_metro[x[7]]
                x[8] = dict_metro[x[8]]
                cadena_alternativa = ''.join([cadena_alternativa, '/', x[7], '/', x[8]])

            else:
                if x[5] == x[7]:
                    cadena_alternativa = ''.join([cadena_alternativa, '/', x[9], '/', x[8]])

                else:
                    cadena_alternativa = ''.join([cadena_alternativa, '/', x[7], '/', x[9], '/', x[8]])

            return cadena_alternativa

df['alternativa_viaje']=df[['netapa',
                            'paraderosubida_1era','paraderobajada_1era','serv_1era_etapa',
                            'paraderosubida_2da','paraderobajada_2da','serv_2da_etapa',
                            'paraderosubida_3era','paraderobajada_3era','serv_3era_etapa',
                            'tipotransporte_1era', 'tipotransporte_2da', 'tipotransporte_3era']].apply(alternativas, axis=1)

df_sin_ZP = df[(df['tipotransporte_1era']!='ZP') & (df['tipotransporte_2da']!='ZP') &  (df['tipotransporte_3era']!='ZP') & (df['id']!='-')]

print('viajes que no se realizan en zona paga', df_sin_ZP.count()[0])

df_sin_ZP_sin_metro = df_sin_ZP[(df_sin_ZP['id']!='-') & ((df_sin_ZP['netapa']>1)|((df_sin_ZP['netapa']==1) & (df_sin_ZP['tipotransporte_1era']!='METRO')))]

#print('viajes que no se realizan en zona paga ni solo en metro', df_sin_ZP_sin_metro.count()[0])

viajes = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:0)))
viajes_reales = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:0)))

for idx, row in df_sin_ZP_sin_metro.iterrows():
    OD_paradero = row['idx_OD_paradero'].split("/")
    alternativa = row['alternativa_viaje']
    origen = OD_paradero[0]
    destino = OD_paradero[1]
    viajes[origen][destino][alternativa] += 1

for idx, row in df.iterrows():
    OD_paradero = row['idx_OD_paradero'].split("/")
    alternativa = row['alternativa_viaje']
    origen = OD_paradero[0]
    destino = OD_paradero[1]
    viajes_reales[origen][destino][alternativa] += 1


dump_file1 = open('tmp\\dict_servicio_llave_codigoTS.pkl', 'wb')
pickle.dump(dict_servicio_llave_codigoTS, dump_file1)
dump_file1.close()

dump_file1 = open('tmp\\dict_servicio_llave_usuario.pkl', 'wb')
pickle.dump(dict_servicio_llave_usuario, dump_file1)
dump_file1.close()

dump_file2 = open('tmp\\viajes.pkl', 'wb')
dill.dump(viajes, dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_reales.pkl', 'wb')
dill.dump(viajes_reales, dump_file2)
dump_file2.close()

#df_eval = df_sin_ZP[(df_sin_ZP['id']!='-') & ((df_sin_ZP['netapa']>1)|((df_sin_ZP['netapa']==1) & (df_sin_ZP['tipotransporte_1era']!='METRO')))].groupby(['idx_OD_paradero'])['idx_OD_paradero'].size().nlargest(100)

#print(df_eval)