# -*- coding: utf-8 -*-
#('tiempo que tarda', '2207.19799995 seconds')
from igraph import *
import pandas as pd
import re
import unicodedata
from datetime import datetime
import time
import csv
from Quitar_variante import *

class Obtener_tiempos():

    def __init__(self):

        # dict en paraderos y servicios
        self.tiempo = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        #dict en paraderos
        self.tiempo_paraderos = defaultdict(lambda: defaultdict(float))

        self.frecuencia = defaultdict(lambda: defaultdict(float))

        #diccionarios para metro

        self.frecuencia_metro = defaultdict(lambda: defaultdict(float))

        self.tiempo_metro = defaultdict(lambda: defaultdict(float))

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

    def tiempos(self, ruta_archivo_perfiles, ruta_tpo_metro):

        #archivo_perfiles = open(ruta_archivo_perfiles, 'r')
        print('a cargar archivo de perfiles')
        archivo_perfiles = pd.read_csv(ruta_archivo_perfiles, encoding='latin1', sep=',')
        print('terminé de cargar el archivo de perfiles')

        q = Quitar_variante()

        archivo_perfiles['serv_sent_mod'] = archivo_perfiles['serviciosentido'].apply(q.quitar_variante)

        #agregar fecha y hora

        dates = pd.to_datetime(archivo_perfiles['tiempo'], format='%Y%m%d %H:%M:%S', errors='ignore')
        fechas = dates.map(lambda x: x.strftime('%Y-%m-%d'))
        horas = dates.map(lambda x: x.strftime('%H:%M:%S'))
        fechas.name = 'fecha'
        horas.name = 'hora'

        Hinis = pd.to_datetime(archivo_perfiles['Hini'], format='%Y%m%d %H:%M:%S', errors='ignore')
        Hinis = Hinis.map(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        Hinis.name = 'Hini_act'

        archivo_perfiles = pd.concat([archivo_perfiles, fechas, horas, Hinis], axis=1)

        servicios = archivo_perfiles.serv_sent_mod.unique().tolist()

        #print (len(servicios))


        for s in servicios:
            df = archivo_perfiles[archivo_perfiles['serv_sent_mod']==s]

            df.sort_values(by=['Hini_act', 'hora'])

            paradero_anterior = ''
            Hini_anterior = ''
            hora_anterior = ''
            correlativo_anterior = 0
            distenruta_anterior = 0

            for idx, row in df.iterrows():

                servicio = str(row['serv_sent_mod'])
                paradero = str(row['paradero'])
                Hini = row['Hini_act']
                correlativo = int(row['correlativo'])
                hora = row['hora']
                distenruta = float(row['distenruta'])

                #print(servicio, paradero, Hini, Hini_anterior, correlativo, hora)

                self.frecuencia[paradero][servicio] = self.frecuencia[paradero][servicio] + 1

                if correlativo==(correlativo_anterior + 1) and Hini==Hini_anterior:

                    dif = (datetime.strptime(hora, '%H:%M:%S')-datetime.strptime(hora_anterior,'%H:%M:%S')).total_seconds()/60

                    #print (distenruta, distenruta_anterior, (distenruta - distenruta_anterior))

                    # se asumen que la velocidad minima de un bus es 4km/hr y velocidad maxima 60km/hr
                    tiempo_max = ((distenruta - distenruta_anterior))*60/(4*1000)
                    tiempo_min = ((distenruta - distenruta_anterior))*60/(60*1000)

                    #print(paradero_anterior, paradero, servicio, dif, tiempo_max, tiempo_min, (distenruta - distenruta_anterior))

                    if dif>0 and dif<=tiempo_max and dif>=tiempo_min:
                        self.tiempo[paradero_anterior][paradero][servicio].append(dif)

                paradero_anterior = paradero
                Hini_anterior = Hini
                correlativo_anterior = correlativo
                hora_anterior = hora
                distenruta_anterior = distenruta

            #print('tiempo que tarda', '{0} seconds'.format(time.time() - start))

        for par1 in self.tiempo:
            for par2 in self.tiempo[par1]:
                for serv in self.tiempo[par1][par2]:

                    suma = sum(self.tiempo[par1][par2][serv])
                    largo = len(self.tiempo[par1][par2][serv])

                    self.tiempo[par1][par2][serv]=[suma/largo]

        for par1 in self.tiempo:
            for par2 in self.tiempo[par1]:
                for serv in self.tiempo[par1][par2]:
                    if self.tiempo[par1][par2][serv][0]>7:
                        for serv2 in self.tiempo[par1][par2]:
                            if serv!=serv2 and self.tiempo[par1][par2][serv][0] > 2*self.tiempo[par1][par2][serv2][0]:
                                self.tiempo[par1][par2][serv] = self.tiempo[par1][par2][serv2]

                    if self.tiempo[par1][par2][serv][0] < 0.7:
                        for serv2 in self.tiempo[par1][par2]:
                            if serv != serv2 and self.tiempo[par1][par2][serv][0] < 0.5 * self.tiempo[par1][par2][serv2][0]:
                                self.tiempo[par1][par2][serv] = self.tiempo[par1][par2][serv2]

        for par1 in self.tiempo:
             for par2 in self.tiempo[par1]:
                 suma_total = 0
                 largo_total = 0
                 for serv in self.tiempo[par1][par2]:
                     suma_total = suma_total + suma
                     largo_total = largo_total + largo

                 self.tiempo_paraderos[par1][par2] = suma_total/largo_total

        n_dias = len(archivo_perfiles.fecha.unique().tolist())

        for par in self.frecuencia:
            for serv in self.frecuencia[par]:
                self.frecuencia[par][serv] = self.frecuencia[par][serv]/(2*n_dias)

        #tiempos de viaje y espera en metro

        df_tiempos = pd.read_csv(ruta_tpo_metro, encoding='latin1', sep=';')

        for idx, row in df_tiempos.iterrows():
            cabeza = row['Inicio']
            cola = row['Fin']
            tiempo = float(row['tViaje'])
            frecuencia = 60/float(row['espera_pam1'])

            cabeza = cabeza.split(' L1')[0]
            cabeza = cabeza.split(' L2')[0]
            cabeza = cabeza.split(' L4')[0]
            cabeza = cabeza.split(' L5')[0]
            cabeza = cabeza.split(' L6')[0]
            cabeza = cabeza.replace(" ", "")
            cabeza = self.text_to_id(cabeza)

            cola = cola.split(' L1')[0]
            cola = cola.split(' L2')[0]
            cola = cola.split(' L4')[0]
            cola = cola.split(' L5')[0]
            cola = cola.split(' L6')[0]
            cola = cola.replace(" ", "")
            cola = self.text_to_id(cola)

            self.frecuencia_metro[cabeza][cola] = frecuencia
            self.tiempo_metro[cabeza][cola] = tiempo

        cabeza == 'franklin'
        cola == 'biobio'

        self.tiempo_metro[cabeza][cola] = 1.5
        self.tiempo_metro[cola][cabeza] = 1.5
        self.frecuencia_metro[cabeza] = 14

        cabeza == 'biobio'
        cola == 'nuble'
        self.tiempo_metro[cabeza][cola] = 3.17
        self.tiempo_metro[cola][cabeza] = 3.17
        self.frecuencia_metro[cabeza] = 14


        cabeza == 'nuble'
        cola == 'estadionacional'
        self.tiempo_metro[cabeza][cola] = 2.77
        self.tiempo_metro[cola][cabeza] = 2.77
        self.frecuencia_metro[cabeza] = 14


        cabeza == 'estadionacional'
        cola == 'nunoa'
        self.tiempo_metro[cabeza][cola] = 1.75
        self.tiempo_metro[cola][cabeza] = 1.75
        self.frecuencia_metro[cabeza] = 14

        cabeza == 'nunoa'
        cola == 'inesdesuarez'
        self.tiempo_metro[cabeza][cola] = 2.48
        self.tiempo_metro[cola][cabeza] = 2.48
        self.frecuencia_metro[cabeza] = 14

        cabeza == 'losleones'
        cola == 'inesdesuarez'
        self.tiempo_metro[cabeza][cola] = 2.93
        self.tiempo_metro[cola][cabeza] = 2.93
        self.frecuencia_metro[cabeza] = 14

        cabeza == 'franklin'
        cola == 'pdtepedroaguirrecerda'
        self.tiempo_metro[cabeza][cola] = 2.48
        self.tiempo_metro[cola][cabeza] = 2.48
        self.frecuencia_metro[cabeza] = 14

        cabeza == 'lovalledor'
        cola == 'pdtepedroaguirrecerda'
        self.tiempo_metro[cabeza][cola] = 2.2
        self.tiempo_metro[cola][cabeza] = 2.2
        self.frecuencia_metro[cabeza] = 14

        cabeza == 'lovalledor'
        cola == 'cerrillos'
        self.tiempo_metro[cabeza][cola] = 2.52
        self.tiempo_metro[cola][cabeza] = 2.52
        self.frecuencia_metro[cabeza] = 14



'''

RUTA_ARCHIVO_PERFILES = 'D:\Datos_viajes\perfiles_input\salida.csv'

start = time.time()

g=Obtener_tiempos()
g.tiempos(RUTA_ARCHIVO_PERFILES)

print('tiempo que tarda', '{0} seconds'.format(time.time() - start))

for par1 in g.tiempo:
    for par2 in g.tiempo[par1]:
        for serv in g.tiempo[par1][par2]:
            row=[par1, par2, serv, g.tiempo[par1][par2][serv]]

            with open('tiempo.csv', 'a') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)

            csvFile.close()


for par1 in g.tiempo_paraderos:
    for par2 in g.tiempo_paraderos[par1]:
        row=[par1, par2, g.tiempo_paraderos[par1][par2]]

        with open('paraderos.csv', 'a') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(row)

        csvFile1.close()

for par1 in g.frecuencia:
    for par2 in g.frecuencia[par1]:
        row = [par1, par2, g.frecuencia[par1][par2]]

        with open('frecuencia.csv', 'a') as csvFile2:
            writer = csv.writer(csvFile2)
            writer.writerow(row)

        csvFile2.close()

'''