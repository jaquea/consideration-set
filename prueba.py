# -*- coding: utf-8 -*-
from igraph import *
from math import sin, cos, sqrt, atan2
import pandas as pd
import re
import unicodedata
import utm
from Quitar_variante import *
from Tiempos_frecuencias_buses import *



# EPSG:32719   zone:19s
class Crear_grafo():
    ''' clase para crear grafo '''
    def __init__(self):
        self.vertices = []
        self.arcos = []
        self.paradero_coord_dic = defaultdict(list)
        self.paradero_cercano_dic = defaultdict(list)

    def strip_accents(self,text):
        """
        Strip accents from input String.

        :param text: The input string.
        :type text: String.

        :returns: The processed String.
        :rtype: String.
        """
        try:
            text = unicode(text, 'utf-8')
        except (TypeError, NameError):  # unicode is a default on python 3
            pass
        #text = re.sub('[ ]+', '_', text)
        #text.replace(' ', '')
        text = unicodedata.normalize('NFD', text)
        text = text.encode('ascii', 'ignore')
        text = text.decode("utf-8")
        return str(text)

    def text_to_id(self,text):
        """
        Convert input text to id.

        :param text: The input string.
        :type text: String.

        :returns: The processed String.
        :rtype: String.
        """
        text = self.strip_accents(text.lower())
        #text = re.sub('[ ]+', '_', text)
        #text.replace(' ', '')
        text = re.sub('[^0-9a-zA-Z_-]', '', text)
        text = text.split('-')[0]
        return text

    def crear_grafo(self, ruta_archivo_nodos, ruta_archivo_metro, radio, ruta_archivo_perfiles, ruta_tpo_metro):

        archivo_nodos = open(ruta_archivo_nodos, 'r')

        self.g = Graph(directed=True)

        servicio_anterior = ''
        correlativo_anterior = 0
        nodo_servicio_anterior = ''
        paradero_anterior = ''

        q = Quitar_variante()
        t = Obtener_tiempos()


        print('inicie calculo de tiempos')

        t.tiempos(ruta_archivo_perfiles, ruta_tpo_metro)

        print('termine calculo de tiempos')

        print('inicie grafo de paraderos')

        #paraderos y arcos entre servicios y paraderos
        for linea in archivo_nodos:

            servicio = str(linea.split("|")[0])
            paradero = linea.split("|")[4]
            correlativo = linea.split("|")[3]
            latitud = linea.split("|")[7]
            longitud = linea.split("|")[8]

            servicio = q.quitar_variante(servicio)

            nodo_servicio=paradero+"/"+servicio

            #nodos
            self.vertices.append((paradero, latitud, longitud))
            self.vertices.append((nodo_servicio, latitud, longitud))

            #arco de subida, tiempo de viaje distinto de cero y tiempo de espera igual a cero
            if paradero in t.frecuencia and servicio in t.frecuencia[paradero]:
                self.arcos.append((paradero, nodo_servicio, 0, t.frecuencia[paradero][servicio]))

            else:
                self.arcos.append((paradero, nodo_servicio, 0, -1))

            #arco de bajada, tiempo de viaje y tiempo de espera igual a cero
            self.arcos.append((nodo_servicio,paradero, 0, 0))

            #arcos entre paraderos de un mismo servicio
            if (servicio==servicio_anterior and int(correlativo)==int(correlativo_anterior)+1):

                if paradero_anterior in t.tiempo and paradero in t.tiempo[paradero_anterior]:
                        #si el servicio se encuentra el diccionario se agrega su tiempo de viaje
                        if servicio in t.tiempo[paradero_anterior][paradero]:
                            self.arcos.append((nodo_servicio_anterior, nodo_servicio, t.tiempo[paradero_anterior][paradero][servicio][0], 0))

                        #si el servicio no se encuentra en el diccionario tiempo se agrega tiempo de viaje del arco
                        elif paradero_anterior in t.tiempo_paraderos and paradero in t.tiempo_paraderos[paradero_anterior]:
                            self.arcos.append((nodo_servicio_anterior, nodo_servicio, t.tiempo_paraderos[paradero_anterior][paradero], 0))

                        #no se encontró tiempo de viaje
                        else:
                            self.arcos.append((nodo_servicio_anterior, nodo_servicio, -1, 0))


            servicio_anterior = servicio
            correlativo_anterior = correlativo
            nodo_servicio_anterior = nodo_servicio
            paradero_anterior = paradero

        print('termine grafo de paraderos')

        print('inicie grafo de metro')

        estaciones = pd.read_csv(ruta_archivo_metro, encoding='latin1', sep=';')
        actual = ''
        previo = ''
        nodo_servicio_previo = ''
        nodo_servicio_actual = ''
        contador = 0

        #nodos y arcos linea 1

        for idx, row in estaciones[estaciones['Id Linea'] == 'L1'].iterrows():

            actual = self.text_to_id(row['Estacion'])
            nodo_servicio_actual = actual + "/" + 'L1'

            if contador == 0:
                previo = actual
                nodo_servicio_previo = nodo_servicio_actual

            else:
                if (previo, actual) == (self.text_to_id('SAN PABLO - SP'), self.text_to_id('SAN PABLO - SP')):
                    break

                if previo==actual:
                    previo = actual
                    nodo_servicio_previo = nodo_servicio_actual
                    continue

                if previo == self.text_to_id('U. LATINOAMERICANA - LA'):
                    previo = self.text_to_id('UNION LATINO AMERICANA')

                if actual == self.text_to_id('U. LATINOAMERICANA - LA'):
                    actual = self.text_to_id('UNION LATINO AMERICANA')

                if previo == self.text_to_id('U. DE SANTIAGO - US'):
                    previo = self.text_to_id('UNIVERSIDAD DE SANTIAGO')

                if actual == self.text_to_id('U. DE SANTIAGO - US'):
                    actual = self.text_to_id('UNIVERSIDAD DE SANTIAGO')

                nodo_servicio_actual = actual + "/" + 'L1'

                # nodos
                self.vertices.append((actual, 0, 0))
                self.vertices.append((nodo_servicio_actual, 0, 0))

                # arco de subida
                if actual in t.frecuencia_metro:
                    self.arcos.append((actual, nodo_servicio_actual, 0, t.frecuencia_metro[actual]))

                else:
                    self.arcos.append((actual, nodo_servicio_actual, 0, -1))



                # arco de bajada
                self.arcos.append((nodo_servicio_actual, actual, 0, 0))

                # arcos entre paraderos de un mismo servicio
                if previo in t.tiempo_metro and actual in t.tiempo_metro[previo]:
                    self.arcos.append((nodo_servicio_previo, nodo_servicio_actual, t.tiempo_metro[previo][actual], 0))

                else:
                    self.arcos.append((nodo_servicio_previo, nodo_servicio_actual, -1, 0))

                if actual in t.tiempo_metro and previo in t.tiempo_metro[previo]:
                    self.arcos.append((nodo_servicio_actual, nodo_servicio_previo,  t.tiempo_metro[actual][previo], 0))

                else:
                    self.arcos.append((nodo_servicio_actual, nodo_servicio_previo, -1, 0))

                #print((nodo_servicio_previo, nodo_servicio_actual, 0))

                previo = actual

                nodo_servicio_previo = nodo_servicio_actual

            contador += 1



        # nodos y arcos linea 2 color rojo

        actual = ''
        previo = ''
        nodo_servicio_previo = ''
        nodo_servicio_actual = ''
        contador = 0

        for idx, row in estaciones[estaciones['Id Linea'] == 'L2'].iterrows():

            actual = self.text_to_id(row['Estacion'])
            nodo_servicio_actual = actual + "/" + 'L2R'

            if actual == 'einstein' or actual == 'cerroblanco' or actual == 'toesca' or actual == 'rondizonni' or actual == 'sanmiguel' or actual == 'departamental'  or actual == 'elparron':
                continue

            if contador == 0:
                previo = actual
                nodo_servicio_previo = nodo_servicio_actual

            else:
                if (previo, actual) == (self.text_to_id('VESPUCIO NORTE - AV'), self.text_to_id('VESPUCIO NORTE - AV')):
                    break

                if previo == actual:
                    previo = actual
                    nodo_servicio_previo = nodo_servicio_actual
                    continue

                if previo == self.text_to_id('CIUDAD DEL NIÑO - CN'):
                    previo = self.text_to_id('CIUDAD DEL NINO')

                if actual == self.text_to_id('CIUDAD DEL NIÑO - CN'):
                    actual = self.text_to_id('CIUDAD DEL NINO')

                nodo_servicio_actual = actual + "/" + 'L2R'

                # nodos
                self.vertices.append((actual, 0, 0))
                self.vertices.append((nodo_servicio_actual, 0, 0))

                # arco de subida
                if actual in t.frecuencia_metro:
                    self.arcos.append((actual, nodo_servicio_actual, 0, t.frecuencia_metro[actual]))

                else:
                    self.arcos.append((actual, nodo_servicio_actual, 0, -1))

                # arco de bajada
                self.arcos.append((nodo_servicio_actual, actual, 0, 0))

                # arcos entre paraderos de un mismo servicio
                if previo in t.tiempo_metro and actual in t.tiempo_metro[previo]:
                    self.arcos.append((nodo_servicio_previo, nodo_servicio_actual, t.tiempo_metro[previo][actual], 0))

                else:
                    self.arcos.append((nodo_servicio_previo, nodo_servicio_actual, -1, 0))

                if actual in t.tiempo_metro and previo in t.tiempo_metro[previo]:
                    self.arcos.append((nodo_servicio_actual, nodo_servicio_previo, t.tiempo_metro[actual][previo], 0))

                else:
                    self.arcos.append((nodo_servicio_actual, nodo_servicio_previo, -1, 0))
                #print((nodo_servicio_previo, nodo_servicio_actual, 0))

                previo = actual

                nodo_servicio_previo = nodo_servicio_actual



            contador += 1


        # nodos y arcos linea 2 color verde

        actual = ''
        previo = ''
        nodo_servicio_previo = ''
        nodo_servicio_actual = ''
        contador = 0

        for idx, row in estaciones[estaciones['Id Linea'] == 'L2'].iterrows():

            actual = self.text_to_id(row['Estacion'])
            nodo_servicio_actual = actual + "/" + 'L2V'

            if actual == 'dorsal' or actual == 'cementerios' or actual == 'patronato' or actual == 'parqueohiggins' or actual == 'elllano' or actual == 'lovial'  or actual == 'ciudaddelnino':
                continue

            if contador == 0:
                previo = actual
                nodo_servicio_previo = nodo_servicio_actual

            else:
                if (previo, actual) == (self.text_to_id('VESPUCIO NORTE - AV'), self.text_to_id('VESPUCIO NORTE - AV')):
                    break

                if previo == actual:
                    previo = actual
                    nodo_servicio_previo = nodo_servicio_actual
                    continue

                if previo == self.text_to_id('CIUDAD DEL NIÑO - CN'):
                    previo = self.text_to_id('CIUDAD DEL NINO')

                if actual == self.text_to_id('CIUDAD DEL NIÑO - CN'):
                    actual = self.text_to_id('CIUDAD DEL NINO')

                nodo_servicio_actual = actual + "/" + 'L2V'

                # nodos
                self.vertices.append((actual, 0, 0))
                self.vertices.append((nodo_servicio_actual, 0, 0))

                # arco de subida
                if actual in t.frecuencia_metro:
                    self.arcos.append((actual, nodo_servicio_actual, 0, t.frecuencia_metro[actual]))

                else:
                    self.arcos.append((actual, nodo_servicio_actual, 0, -1))

                # arco de bajada
                self.arcos.append((nodo_servicio_actual, actual, 0, 0))

                # arcos entre paraderos de un mismo servicio
                if previo in t.tiempo_metro and actual in t.tiempo_metro[previo]:
                    self.arcos.append((nodo_servicio_previo, nodo_servicio_actual, t.tiempo_metro[previo][actual], 0))

                else:
                    self.arcos.append((nodo_servicio_previo, nodo_servicio_actual, -1, 0))

                if actual in t.tiempo_metro and previo in t.tiempo_metro[previo]:
                    self.arcos.append((nodo_servicio_actual, nodo_servicio_previo, t.tiempo_metro[actual][previo], 0))

                else:
                    self.arcos.append((nodo_servicio_actual, nodo_servicio_previo, -1, 0))

                #print((nodo_servicio_previo, nodo_servicio_actual, 0))

                previo = actual

                nodo_servicio_previo = nodo_servicio_actual



            contador += 1

        # nodos y arcos linea 5 color rojo

        actual = ''
        previo = ''
        nodo_servicio_previo = ''
        nodo_servicio_actual = ''
        contador = 0

        for idx, row in estaciones[estaciones['Id Linea'] == 'L5'].iterrows():

            actual = self.text_to_id(row['Estacion'])
            nodo_servicio_actual = actual + "/" + 'L5R'

            if actual == 'pedreros' or actual == 'caminoagricola'  or actual == 'rodrigodearaya' or actual == 'santaisabel' or actual == 'cumming' or actual == 'grutalourdes' or actual == 'loprado' or actual == 'lasparcelas_' or actual == 'delsol':
                continue

            elif contador == 0:
                previo = actual
                nodo_servicio_previo = nodo_servicio_actual

            else:
                #print(actual)
                if (previo, actual) == (self.text_to_id('PLAZA MAIPU - PM'), self.text_to_id('PLAZA MAIPU - PM')):
                    break

                if previo == actual:
                    previo = actual
                    nodo_servicio_previo = nodo_servicio_actual
                    continue

                if previo == self.text_to_id('LA FLORIDA - LF'):
                    previo = self.text_to_id('BELLAVISTA DE LA FLORIDA')

                if actual == self.text_to_id('LA FLORIDA - LF'):
                    actual = self.text_to_id('BELLAVISTA DE LA FLORIDA')

                if previo == self.text_to_id('GRUTA LOURDES - GL'):
                    previo = self.text_to_id('GRUTA DE LOURDES')

                if actual == self.text_to_id('GRUTA LOURDES - GL'):
                    actual = self.text_to_id('GRUTA DE LOURDES')

                if previo == self.text_to_id('ÑUBLE - NU'):
                    previo = self.text_to_id('NUBLE')

                if actual == self.text_to_id('ÑUBLE - NU'):
                    actual = self.text_to_id('NUBLE')

                if previo == self.text_to_id('MIRADOR AZUL - MA'):
                    previo = self.text_to_id('MIRADOR')

                if actual == self.text_to_id('MIRADOR AZUL - MA'):
                    actual = self.text_to_id('MIRADOR')

                if previo == self.text_to_id('PEDREROS - PE'):
                    previo = self.text_to_id('PEDRERO')

                if actual == self.text_to_id('PEDREROS - PE'):
                    actual = self.text_to_id('PEDRERO')

                nodo_servicio_actual = actual + "/" + 'L5R'

                # nodos
                self.vertices.append((actual, 0, 0))
                self.vertices.append((nodo_servicio_actual, 0, 0))

                # arco de subida
                if actual in t.frecuencia_metro:
                    self.arcos.append((actual, nodo_servicio_actual, 0, t.frecuencia_metro[actual]))

                else:
                    self.arcos.append((actual, nodo_servicio_actual, 0, -1))

                # arco de bajada
                self.arcos.append((nodo_servicio_actual, actual, 0, 0))

                # arcos entre paraderos de un mismo servicio
                if previo in t.tiempo_metro and actual in t.tiempo_metro[previo]:
                    self.arcos.append((nodo_servicio_previo, nodo_servicio_actual, t.tiempo_metro[previo][actual], 0))

                else:
                    self.arcos.append((nodo_servicio_previo, nodo_servicio_actual, -1, 0))

                if actual in t.tiempo_metro and previo in t.tiempo_metro[previo]:
                    self.arcos.append((nodo_servicio_actual, nodo_servicio_previo, t.tiempo_metro[actual][previo], 0))

                else:
                    self.arcos.append((nodo_servicio_actual, nodo_servicio_previo, -1, 0))

                #print((nodo_servicio_previo, nodo_servicio_actual, 0))

                previo = actual

                nodo_servicio_previo = nodo_servicio_actual

            contador += 1

         # nodos y arcos linea 5 color verde

        actual = ''
        previo = ''
        nodo_servicio_previo = ''
        nodo_servicio_actual = ''
        contador = 0

        for idx, row in estaciones[estaciones['Id Linea'] == 'L5'].iterrows():

            actual = self.text_to_id(row['Estacion'])
            nodo_servicio_actual = actual + "/" + 'L5V'

            if actual == 'miradorazul' or actual == 'sanjoaquin' or actual == 'carlosvaldovinos' or actual == 'parquebustamante' or actual == 'quintanormal' or actual == 'blanqueado'  or actual == 'barrancas' or actual == 'montetabor' or actual == 'santiagobueras':
                continue

            elif contador == 0:
                previo = actual
                nodo_servicio_previo = nodo_servicio_actual

            else:
                #print(actual)
                if (previo, actual) == (self.text_to_id('PLAZA MAIPU - PM'), self.text_to_id('PLAZA MAIPU - PM')):
                    break

                if previo == actual:
                    previo = actual
                    nodo_servicio_previo = nodo_servicio_actual
                    continue

                if previo == self.text_to_id('LA FLORIDA - LF'):
                    previo = self.text_to_id('BELLAVISTA DE LA FLORIDA')

                if actual == self.text_to_id('LA FLORIDA - LF'):
                    actual = self.text_to_id('BELLAVISTA DE LA FLORIDA')

                if previo == self.text_to_id('GRUTA LOURDES - GL'):
                    previo = self.text_to_id('GRUTA DE LOURDES')

                if actual == self.text_to_id('GRUTA LOURDES - GL'):
                    actual = self.text_to_id('GRUTA DE LOURDES')

                if previo == self.text_to_id('ÑUBLE - NU'):
                    previo = self.text_to_id('NUBLE')

                if actual == self.text_to_id('ÑUBLE - NU'):
                    actual = self.text_to_id('NUBLE')

                if previo == self.text_to_id('MIRADOR AZUL - MA'):
                    previo = self.text_to_id('MIRADOR')

                if actual == self.text_to_id('MIRADOR AZUL - MA'):
                    actual = self.text_to_id('MIRADOR')

                if previo == self.text_to_id('PEDREROS - PE'):
                    previo = self.text_to_id('PEDRERO')

                if actual == self.text_to_id('PEDREROS - PE'):
                    actual = self.text_to_id('PEDRERO')

                nodo_servicio_actual = actual + "/" + 'L5V'

                # nodos
                self.vertices.append((actual, 0, 0))
                self.vertices.append((nodo_servicio_actual, 0, 0))

                # arco de subida
                if actual in t.frecuencia_metro:
                    self.arcos.append((actual, nodo_servicio_actual, 0, t.frecuencia_metro[actual]))

                else:
                    self.arcos.append((actual, nodo_servicio_actual, 0, -1))

                # arco de bajada
                self.arcos.append((nodo_servicio_actual, actual, 0, 0))

                # arcos entre paraderos de un mismo servicio
                if previo in t.tiempo_metro and actual in t.tiempo_metro[previo]:
                    self.arcos.append((nodo_servicio_previo, nodo_servicio_actual, t.tiempo_metro[previo][actual], 0))

                else:
                    self.arcos.append((nodo_servicio_previo, nodo_servicio_actual, -1, 0))

                if actual in t.tiempo_metro and previo in t.tiempo_metro[previo]:
                    self.arcos.append((nodo_servicio_actual, nodo_servicio_previo, t.tiempo_metro[actual][previo], 0))

                else:
                    self.arcos.append((nodo_servicio_actual, nodo_servicio_previo, -1, 0))

                #print((nodo_servicio_previo, nodo_servicio_actual, 0))

                previo = actual

                nodo_servicio_previo = nodo_servicio_actual

            contador += 1

        # nodos y arcos linea 4 color rojo

        actual = ''
        previo = ''
        nodo_servicio_previo = ''
        nodo_servicio_actual = ''
        contador = 0

        for idx, row in estaciones[estaciones['Id Linea'] == 'L4'].iterrows():

            actual = self.text_to_id(row['Estacion'])
            nodo_servicio_actual = actual + "/" + 'L4R'

            if actual == 'protectoradelainfancia_' or actual == 'sanjosedelaestrella' or actual == 'rojasmagallanes' or actual == 'rotondaquilin' or actual == 'rotondagrecia' or actual == 'simonbolivar'  or actual == 'colon':
                continue

            elif contador == 0:
                previo = actual
                nodo_servicio_previo = nodo_servicio_actual

            else:
                #print(actual)
                if (previo, actual) == (self.text_to_id('TOBALABA - TOB'), self.text_to_id('TOBALABA - TOB')):
                    break

                if previo == actual:
                    previo = actual
                    nodo_servicio_previo = nodo_servicio_actual
                    continue

                if previo == self.text_to_id('COLÓN - COL'):
                    previo = self.text_to_id('CRISTOBAL COLON')

                if actual == self.text_to_id('COLÓN - COL'):
                    actual = self.text_to_id('CRISTOBAL COLON')

                if previo == self.text_to_id('BILBAO - BIL'):
                    previo = self.text_to_id('FRANCISCO BILBAO')

                if actual == self.text_to_id('BILBAO - BIL'):
                    actual = self.text_to_id('FRANCISCO BILBAO')

                if previo == self.text_to_id('ROTONDA GRECIA - RGR'):
                    previo = self.text_to_id('GRECIA')

                if actual == self.text_to_id('ROTONDA GRECIA - RGR'):
                    actual = self.text_to_id('GRECIA')

                if previo == self.text_to_id('HOSP. SÓTERO DEL RÍO - HSR'):
                    previo = self.text_to_id('HOSPITAL SOTERO DEL RIO')

                if actual == self.text_to_id('HOSP. SÓTERO DEL RÍO - HSR'):
                    actual = self.text_to_id('HOSPITAL SOTERO DEL RIO')

                if previo == self.text_to_id('PLAZA PUENTE ALTO - PPA'):
                    previo = self.text_to_id('PLAZA DE PUENTE ALTO')

                if actual == self.text_to_id('PLAZA PUENTE ALTO - PPA'):
                    actual = self.text_to_id('PLAZA DE PUENTE ALTO')

                if previo == self.text_to_id('PLAZA EGAÑA - PEG'):
                    previo = self.text_to_id('PLAZA EGANA')

                if actual == self.text_to_id('PLAZA EGAÑA - PEG'):
                    actual = self.text_to_id('PLAZA EGANA')

                if previo == self.text_to_id('ROTONDA QUILÍN - RQU'):
                    previo = self.text_to_id('QUILIN')

                if actual == self.text_to_id('ROTONDA QUILÍN - RQU'):
                    actual = self.text_to_id('QUILIN')

                if previo == self.text_to_id('VICUÑA MACKENNA - VMA'):
                    previo = self.text_to_id('VICUNA MACKENNA')

                if actual == self.text_to_id('VICUÑA MACKENNA - VMA'):
                    actual = self.text_to_id('VICUNA MACKENNA')

                nodo_servicio_actual = actual + "/" + 'L4R'

                # nodos
                self.vertices.append((actual, 0, 0))
                self.vertices.append((nodo_servicio_actual, 0, 0))

                # arco de subida
                if actual in t.frecuencia_metro:
                    self.arcos.append((actual, nodo_servicio_actual, 0, t.frecuencia_metro[actual]))

                else:
                    self.arcos.append((actual, nodo_servicio_actual, 0, -1))

                # arco de bajada
                self.arcos.append((nodo_servicio_actual, actual, 0, 0))

                # arcos entre paraderos de un mismo servicio
                if previo in t.tiempo_metro and actual in t.tiempo_metro[previo]:
                    self.arcos.append((nodo_servicio_previo, nodo_servicio_actual, t.tiempo_metro[previo][actual], 0))

                else:
                    self.arcos.append((nodo_servicio_previo, nodo_servicio_actual, -1, 0))

                if actual in t.tiempo_metro and previo in t.tiempo_metro[previo]:
                    self.arcos.append((nodo_servicio_actual, nodo_servicio_previo, t.tiempo_metro[actual][previo], 0))

                else:
                    self.arcos.append((nodo_servicio_actual, nodo_servicio_previo, -1, 0))

                #print((nodo_servicio_previo, nodo_servicio_actual, 0))

                previo = actual

                nodo_servicio_previo = nodo_servicio_actual

            contador += 1

        # nodos y arcos linea 4 color verde

        actual = ''
        previo = ''
        nodo_servicio_previo = ''
        nodo_servicio_actual = ''
        contador = 0

        for idx, row in estaciones[estaciones['Id Linea'] == 'L4'].iterrows():

            actual = self.text_to_id(row['Estacion'])
            nodo_servicio_actual = actual + "/" + 'L4V'

            if actual == 'lasmercedes' or actual == 'losquillayes' or actual == 'lastorres' or actual == 'lospresidentes' or actual == 'losorientales' or actual == 'principedegales' or actual == 'trinidad':
                continue

            elif contador == 0:
                previo = actual
                nodo_servicio_previo = nodo_servicio_actual

            else:
                #print(actual)
                if (previo, actual) ==  (self.text_to_id('TOBALABA - TOB'), self.text_to_id('TOBALABA - TOB')):
                    break

                if previo == actual:
                    previo = actual
                    nodo_servicio_previo = nodo_servicio_actual
                    continue

                if previo == self.text_to_id('COLÓN - COL'):
                    previo = self.text_to_id('CRISTOBAL COLON')

                if actual == self.text_to_id('COLÓN - COL'):
                    actual = self.text_to_id('CRISTOBAL COLON')

                if previo == self.text_to_id('BILBAO - BIL'):
                    previo = self.text_to_id('FRANCISCO BILBAO')

                if actual == self.text_to_id('BILBAO - BIL'):
                    actual = self.text_to_id('FRANCISCO BILBAO')

                if previo == self.text_to_id('ROTONDA GRECIA - RGR'):
                    previo = self.text_to_id('GRECIA')

                if actual == self.text_to_id('ROTONDA GRECIA - RGR'):
                    actual = self.text_to_id('GRECIA')

                if previo == self.text_to_id('HOSP. SÓTERO DEL RÍO - HSR'):
                    previo = self.text_to_id('HOSPITAL SOTERO DEL RIO')

                if actual == self.text_to_id('HOSP. SÓTERO DEL RÍO - HSR'):
                    actual = self.text_to_id('HOSPITAL SOTERO DEL RIO')

                if previo == self.text_to_id('PLAZA PUENTE ALTO - PPA'):
                    previo = self.text_to_id('PLAZA DE PUENTE ALTO')

                if actual == self.text_to_id('PLAZA PUENTE ALTO - PPA'):
                    actual = self.text_to_id('PLAZA DE PUENTE ALTO')

                if previo == self.text_to_id('PLAZA EGAÑA - PEG'):
                    previo = self.text_to_id('PLAZA EGANA')

                if actual == self.text_to_id('PLAZA EGAÑA - PEG'):
                    actual = self.text_to_id('PLAZA EGANA')

                if previo == self.text_to_id('ROTONDA QUILÍN - RQU'):
                    previo = self.text_to_id('QUILIN')

                if actual == self.text_to_id('ROTONDA QUILÍN - RQU'):
                    actual = self.text_to_id('QUILIN')

                if previo == self.text_to_id('VICUÑA MACKENNA - VMA'):
                    previo = self.text_to_id('VICUNA MACKENNA')

                if actual == self.text_to_id('VICUÑA MACKENNA - VMA'):
                    actual = self.text_to_id('VICUNA MACKENNA')


                nodo_servicio_actual = actual + "/" + 'L4V'

                # nodos
                self.vertices.append((actual, 0, 0))
                self.vertices.append((nodo_servicio_actual, 0, 0))

                # arco de subida
                if actual in t.frecuencia_metro:
                    self.arcos.append((actual, nodo_servicio_actual, 0, t.frecuencia_metro[actual]))

                else:
                    self.arcos.append((actual, nodo_servicio_actual, 0, -1))

                # arco de bajada
                self.arcos.append((nodo_servicio_actual, actual, 0, 0))

                # arcos entre paraderos de un mismo servicio
                if previo in t.tiempo_metro and actual in t.tiempo_metro[previo]:
                    self.arcos.append((nodo_servicio_previo, nodo_servicio_actual, t.tiempo_metro[previo][actual], 0))

                else:
                    self.arcos.append((nodo_servicio_previo, nodo_servicio_actual, -1, 0))

                if actual in t.tiempo_metro and previo in t.tiempo_metro[previo]:
                    self.arcos.append((nodo_servicio_actual, nodo_servicio_previo, t.tiempo_metro[actual][previo], 0))

                else:
                    self.arcos.append((nodo_servicio_actual, nodo_servicio_previo, -1, 0))

                #print((nodo_servicio_previo, nodo_servicio_actual, 0))

                previo = actual

                nodo_servicio_previo = nodo_servicio_actual

            contador += 1

        # nodos y arcos linea 4A

        actual = ''
        previo = ''
        nodo_servicio_previo = ''
        nodo_servicio_actual = ''
        contador = 0

        for idx, row in estaciones[estaciones['Id Linea'] == 'L4A'].iterrows():

            actual = self.text_to_id(row['Estacion'])
            nodo_servicio_actual = actual + "/" + 'L4A'

            if contador == 0:
                previo = actual
                nodo_servicio_previo = nodo_servicio_actual

            else:
                #print(actual)
                if (previo, actual) == (self.text_to_id('LA CISTERNA - LCI'), self.text_to_id('LA CISTERNA - LCI')):
                    break

                if previo == actual:
                    previo = actual
                    nodo_servicio_previo = nodo_servicio_actual
                    continue

                if previo == self.text_to_id('VICUÑA MACKENNA - VIM'):
                    previo = self.text_to_id('VICUNA MACKENNA')

                if actual == self.text_to_id('VICUÑA MACKENNA - VIM'):
                    actual = self.text_to_id('VICUNA MACKENNA')

                nodo_servicio_actual = actual + "/" + 'L4A'

                # nodos
                self.vertices.append((actual, 0, 0))
                self.vertices.append((nodo_servicio_actual, 0, 0))

                # arco de subida
                if actual in t.frecuencia_metro:
                    self.arcos.append((actual, nodo_servicio_actual, 0, t.frecuencia_metro[actual]))

                else:
                    self.arcos.append((actual, nodo_servicio_actual, 0, -1))

                # arco de bajada
                self.arcos.append((nodo_servicio_actual, actual, 0, 0))

                # arcos entre paraderos de un mismo servicio
                if previo in t.tiempo_metro and actual in t.tiempo_metro[previo]:
                    self.arcos.append((nodo_servicio_previo, nodo_servicio_actual, t.tiempo_metro[previo][actual], 0))

                else:
                    self.arcos.append((nodo_servicio_previo, nodo_servicio_actual, -1, 0))

                if actual in t.tiempo_metro and previo in t.tiempo_metro[previo]:
                    self.arcos.append((nodo_servicio_actual, nodo_servicio_previo, t.tiempo_metro[actual][previo], 0))

                else:
                    self.arcos.append((nodo_servicio_actual, nodo_servicio_previo, -1, 0))

                #print((nodo_servicio_previo, nodo_servicio_actual, 0))

                previo = actual

                nodo_servicio_previo = nodo_servicio_actual

            contador += 1

        # nodos y arcos linea 6

        actual = ''
        previo = ''
        nodo_servicio_previo = ''
        nodo_servicio_actual = ''
        contador = 0

        for idx, row in estaciones[estaciones['Id Linea'] == 'L6'].iterrows():

            actual = self.text_to_id(row['Estacion'])
            nodo_servicio_actual = actual + "/" + 'L6'

            if contador == 0:
                previo = actual
                nodo_servicio_previo = nodo_servicio_actual

            else:
                #print(actual)
                if (previo, actual) == (self.text_to_id('CERRILLOS - CER'), self.text_to_id('CERRILLOS - CER')):
                    break

                if previo == actual:
                    previo = actual
                    nodo_servicio_previo = nodo_servicio_actual
                    continue

                if previo == self.text_to_id('ÑUBLE - NUB'):
                    previo = self.text_to_id('NUBLE')

                if actual == self.text_to_id('ÑUÑOA - NNO'):
                    actual = self.text_to_id('NUNOA')

                if previo == self.text_to_id('PEDRO AGUIRRE CERDA - PAC'):
                    previo = self.text_to_id('PDTE PEDRO AGUIRRE CERDA')

                if actual == self.text_to_id('PEDRO AGUIRRE CERDA - PAC'):
                    actual = self.text_to_id('PDTE PEDRO AGUIRRE CERDA')

                nodo_servicio_actual = actual + "/" + 'L6'

                # nodos
                self.vertices.append((actual, 0, 0))
                self.vertices.append((nodo_servicio_actual, 0, 0))

                # arco de subida
                if actual in t.frecuencia_metro:
                    self.arcos.append((actual, nodo_servicio_actual, 0, t.frecuencia_metro[actual]))

                else:
                    self.arcos.append((actual, nodo_servicio_actual, 0, -1))

                # arco de bajada
                self.arcos.append((nodo_servicio_actual, actual, 0, 0))

                # arcos entre paraderos de un mismo servicio
                if previo in t.tiempo_metro and actual in t.tiempo_metro[previo]:
                    self.arcos.append((nodo_servicio_previo, nodo_servicio_actual, t.tiempo_metro[previo][actual], 0))

                else:
                    self.arcos.append((nodo_servicio_previo, nodo_servicio_actual, -1, 0))

                if actual in t.tiempo_metro and previo in t.tiempo_metro[previo]:
                    self.arcos.append((nodo_servicio_actual, nodo_servicio_previo, t.tiempo_metro[actual][previo], 0))

                else:
                    self.arcos.append((nodo_servicio_actual, nodo_servicio_previo, -1, 0))

                #print((nodo_servicio_previo, nodo_servicio_actual, 0))

                previo = actual

                nodo_servicio_previo = nodo_servicio_actual

            contador += 1

        print('termine grafo de metro')

        print('inicie grafo de caminata')

        #arcos de caminata

        paraderos = pd.read_csv(RUTA_ARCHIVO_NODOS, encoding='latin1', sep='|')
        metro = pd.read_csv(RUTA_ARCHIVO_ESTACIONES, encoding='latin1', sep=',')

        metro['x'] = metro[['LATITUD', 'LONGITUD']].apply(lambda x: round(utm.from_latlon(x[0], x[1])[0], 2), axis=1)
        metro['y'] = metro[['LATITUD', 'LONGITUD']].apply(lambda x: round(utm.from_latlon(x[0], x[1])[1], 2), axis=1)

        paraderos['x'] = paraderos[['Latitud', 'Longitud']].apply(lambda x: round(utm.from_latlon(x[0], x[1])[0], 2), axis=1)
        paraderos['y'] = paraderos[['Latitud', 'Longitud']].apply(lambda x: round(utm.from_latlon(x[0], x[1])[1], 2), axis=1)

        #coordenadas estaciones de paraderos
        for idx, row in paraderos.iterrows():

            paradero = row['Codigo']
            x = row['x']
            y = row['y']

            self.paradero_coord_dic[paradero]=[x, y]

        #coordenadas estaciones de metro
        for idx, row in metro.iterrows():

            paradero = self.text_to_id(row['ESTANDAR'])

            if paradero==self.text_to_id('ÑUBLE'):
                paradero = self.text_to_id('NUBLE')

            if paradero==self.text_to_id('ÑUÑOA'):
                paradero = self.text_to_id('NUNOA')

            if paradero==self.text_to_id('VICUÑA MACKENNA'):
                paradero = self.text_to_id('VICUNA MACKENNA')

            if paradero==self.text_to_id('PLAZA EGAÑA'):
                paradero = self.text_to_id('PLAZA EGANA')

            if paradero==self.text_to_id('CIUDAD DEL NIÑO'):
                paradero = self.text_to_id('CIUDAD DEL NINO')

            x = row['x']
            y = row['y']

            self.paradero_coord_dic[paradero]=[x, y]

        for llave1 in self.paradero_coord_dic:
            for llave2 in self.paradero_coord_dic:
                if llave1 != llave2:
                    x1 = float(self.paradero_coord_dic[llave1][0])
                    y1 = float(self.paradero_coord_dic[llave1][1])
                    x2 = float(self.paradero_coord_dic[llave2][0])
                    y2 = float(self.paradero_coord_dic[llave2][1])
                    dist = (((x1 - x2) ** 2) + ((y1 - y2) ** 2)) ** 0.5
                    dist = abs(x1 - x2) + abs(y1 - y2)

                    if dist <= radio:
                        costo = dist*60/(1000*4)
                        self.arcos.append((llave1, llave2, costo, 0))
                        self.paradero_cercano_dic[llave1].append(llave2)

        print('termine grafo de caminata')


RUTA_ARCHIVO_NODOS = 'C:\Users\jacke\Desktop\paraderos.stop'
RUTA_ARCHIVO_METRO = 'C:\Users\jacke\Desktop\ChicagoSketch\Lion.csv'
RUTA_ARCHIVO_ESTACIONES = 'D:\Datos_viajes\metro\Diccionario-EstacionesMetro.csv'

#se saca de los perfiles de carga generados por ADATRAP para obtener tiempos de arcos y frecuencia de servicios
RUTA_ARCHIVO_PERFILES = 'D:\Datos_viajes\perfiles_input\salida.csv'

#este archivo está preprocesado por mauricio para obtener tiempos de viaje y espera en metro
RUTA_TPO_METRO = 'C:\Users\jacke\Desktop\ChicagoSketch\\tiempos_metro.csv'


radio=300
g=Crear_grafo()
g.crear_grafo(RUTA_ARCHIVO_NODOS, RUTA_ARCHIVO_METRO, radio, RUTA_ARCHIVO_PERFILES, RUTA_TPO_METRO)

print('inicio')
#arcos=list(set(g.arcos))
arcos=g.arcos
print(arcos)
print('fin')
#vertices=list(set(g.vertices))
vertices=g.vertices

#print(g.paradero_coord_dic)

#for i in g.paradero_coord_dic:
#    print(i, g.paradero_coord_dic[i])

for a in arcos:
    cabeza = a[0]
    cola = a[1]
    tpo_viaje = a[2]
    frecuencia = a[3]

    row = [cabeza, cola, tpo_viaje, frecuencia]

    with open('arcos.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)

    csvFile.close()

for v in vertices:
    nodo = v[0]
    latitud = v[1]
    longitud = v[2]

    row=[nodo, latitud, longitud]

    with open('vertices.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)

    csvFile.close()






