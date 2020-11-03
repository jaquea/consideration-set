# -*- encoding: utf-8 -*-
import unittest
import pickle
import os
from constants import PROJECT_DIR

from igraph import *

from k_shortest_paths import yen_igraph
from k_shortest_paths import link_elimination
from k_shortest_paths import labeling_approach
from k_shortest_paths import link_penalty
from k_shortest_paths import simulation
from k_shortest_paths import format_paths_k_shortest_path


class TestKShortestPaths(unittest.TestCase):

    def test_yen_paths_grafo_real(self):

        dump_file1 = open(os.path.join(PROJECT_DIR,'tmp','grafo.igraph'), 'rb')
        g = pickle.load(dump_file1)
        dump_file1.close()

        dump_file1 = open(os.path.join(PROJECT_DIR, 'tmp', 'dict_servicio_llave_codigoTS.pkl'), 'rb')
        dict_servicio_llave_codigoTS = pickle.load(dump_file1)
        dump_file1.close()

        #origin = 'L-34-34-35-PO'
        #destination = 'M-TB'
        origin = 'L-34-41-100-OP'
        destination = 'M-BA'
        origin_index = g.vs.find(name2=origin).index
        destination_index = g.vs.find(name2=destination).index
        num_k = 3
        weights = "peso"

        k_paths = yen_igraph(g, origin_index, destination_index, num_k, weights, dict_servicio_llave_codigoTS)

        caminos_simples = [u'L-34-41-100-OP/F24-I/L-34-52-5-PO/M-EA/L4/M-VA/L5/M-BA', u'L-34-41-95-PO/712-I/T-34-269-SN-45/E12-I/L-33-65-5-OP/M-TR/L4/M-VA/L5/M-BA', u'L-34-41-95-PO/712-I/T-34-269-SN-50/E12-I/L-33-65-5-OP/M-TR/L4/M-VA/L5/M-BA']
        caminos_resumidos = [u'L-34-41-100-OP/F24-I/L-34-52-5-PO/M-EA/M-BA', u'L-34-41-95-PO/712-I/T-34-269-SN-45/E12-I/L-33-65-5-OP/M-TR/M-BA', u'L-34-41-95-PO/712-I/T-34-269-SN-50/E12-I/L-33-65-5-OP/M-TR/M-BA']
        costos = [46.31683333250615, 47.29293571343836, 47.72626904676836]
        #self.assertEqual(k_paths[0], caminos_simples)
        #self.assertEqual(k_paths[1], caminos_resumidos)
        #self.assertEqual(k_paths[2], costos)
        print(k_paths)
        #self.g.vs["label"] = self.g.vs["name2"]
        #color_dict = {"paradero": "red", "servicio": "pink"}
        #self.g.vs["color"] = [color_dict[tipo] for tipo in self.g.vs["tipo"]]
        #plot(self.g, bbox=(1000, 800), margin=20)

    def test_link_elimination(self):

        dump_file1 = open(os.path.join(PROJECT_DIR,'tmp','grafo.igraph'), 'rb')
        g = pickle.load(dump_file1)
        dump_file1.close()

        dump_file1 = open(os.path.join(PROJECT_DIR, 'tmp', 'dict_servicio_llave_codigoTS.pkl'), 'rb')
        dict_servicio_llave_codigoTS = pickle.load(dump_file1)
        dump_file1.close()

        #origin = 'L-34-34-35-PO'
        #destination = 'M-TB'
        origin = 'L-34-41-100-OP'
        destination = 'M-BA'
        origin_index = g.vs.find(name2=origin).index
        destination_index = g.vs.find(name2=destination).index
        num_k = 3
        weights = "peso"

        k_paths = link_elimination(g, origin_index, destination_index, num_k, weights, dict_servicio_llave_codigoTS)

        caminos_simples = [u'L-34-41-100-OP/F24-I/L-34-52-5-PO/M-EA/L4/M-VA/L5/M-BA', u'L-34-41-95-PO/712-I/T-34-269-SN-45/E12-I/L-33-65-5-OP/M-TR/L4/M-VA/L5/M-BA', u'L-34-41-100-OP/F23-R/T-34-270-NS-10/M-HS/L4/M-VA/L5/M-BA']
        caminos_resumidos = [u'L-34-41-100-OP/F24-I/L-34-52-5-PO/M-EA/M-BA', u'L-34-41-95-PO/712-I/T-34-269-SN-45/E12-I/L-33-65-5-OP/M-TR/M-BA', u'L-34-41-100-OP/F23-R/T-34-270-NS-10/M-HS/M-BA']
        costos = [46.31683333250615, 47.29293571343836, 48.72744999813938]
        self.assertEqual(k_paths[0], caminos_simples)
        self.assertEqual(k_paths[1], caminos_resumidos)
        self.assertEqual(k_paths[2], costos)

    def test_labeling_approach(self):

        dump_file1 = open(os.path.join(PROJECT_DIR,'tmp','grafo.igraph'), 'rb')
        g = pickle.load(dump_file1)
        dump_file1.close()

        dump_file1 = open(os.path.join(PROJECT_DIR, 'tmp', 'dict_servicio_llave_codigoTS.pkl'), 'rb')
        dict_servicio_llave_codigoTS = pickle.load(dump_file1)
        dump_file1.close()

        dump_file2 = open(os.path.join(PROJECT_DIR, 'tmp', 'paradero_cercano_dic.pkl'), 'rb')
        paradero_cercano_dic = pickle.load(dump_file2)
        dump_file2.close()

        #origin = 'L-34-34-35-PO'
        #destination = 'M-TB'
        origin = 'L-34-41-100-OP'
        destination = 'M-BA'
        origin_index = g.vs.find(name2=origin).index
        destination_index = g.vs.find(name2=destination).index
        weights = "peso"
        transfer_metro_penalty = 6
        transfer_other_penalty = 16

        k_paths = labeling_approach(g, origin_index, destination_index, weights, dict_servicio_llave_codigoTS, paradero_cercano_dic, transfer_metro_penalty, transfer_other_penalty)
        caminos_simples = [u'L-34-41-100-OP/F24-I/L-34-52-5-PO/M-EA/L4/M-VA/L5/M-BA', u'L-34-41-95-PO/712-I/T-34-269-SN-45/E12-I/L-33-65-5-OP/M-TR/L4/M-VA/L5/M-BA', u'L-34-41-100-OP/F23-R/T-34-270-NS-10/M-HS/L4/M-VA/L5/M-BA']
        caminos_resumidos = [u'L-34-41-100-OP/F24-I/L-34-52-5-PO/M-EA/M-BA', u'L-34-41-95-PO/712-I/T-34-269-SN-45/E12-I/L-33-65-5-OP/M-TR/M-BA', u'L-34-41-100-OP/F23-R/T-34-270-NS-10/M-HS/M-BA']
        costos = [46.31683333250615, 47.29293571343836, 48.72744999813938]
        #self.assertEqual(k_paths[0], caminos_simples)
        #self.assertEqual(k_paths[1], caminos_resumidos)
        #self.assertEqual(k_paths[2], costos)

        print(k_paths)

    def test_link_penalty(self):

        dump_file1 = open(os.path.join(PROJECT_DIR,'tmp','grafo.igraph'), 'rb')
        g = pickle.load(dump_file1)
        dump_file1.close()

        dump_file1 = open(os.path.join(PROJECT_DIR, 'tmp', 'dict_servicio_llave_codigoTS.pkl'), 'rb')
        dict_servicio_llave_codigoTS = pickle.load(dump_file1)
        dump_file1.close()

        #origin = 'L-34-34-35-PO'
        #destination = 'M-TB'
        origin = 'L-34-41-100-OP'
        destination = 'M-BA'
        origin_index = g.vs.find(name2=origin).index
        destination_index = g.vs.find(name2=destination).index
        weights = "peso"

        k_paths = link_penalty(g, origin_index, destination_index, weights, dict_servicio_llave_codigoTS)
        caminos_simples = [u'L-34-41-100-OP/F24-I/L-34-52-5-PO/M-EA/L4/M-VA/L5/M-BA', u'L-34-41-95-PO/712-I/T-34-269-SN-45/E12-I/L-33-65-5-OP/M-TR/L4/M-VA/L5/M-BA', u'L-34-41-100-OP/F23-R/T-34-270-NS-10/M-HS/L4/M-VA/L5/M-BA']
        caminos_resumidos = [u'L-34-41-100-OP/F24-I/L-34-52-5-PO/M-EA/M-BA', u'L-34-41-95-PO/712-I/T-34-269-SN-45/E12-I/L-33-65-5-OP/M-TR/M-BA', u'L-34-41-100-OP/F23-R/T-34-270-NS-10/M-HS/M-BA']
        costos = [46.31683333250615, 47.29293571343836, 48.72744999813938]
        #self.assertEqual(k_paths[0], caminos_simples)
        #self.assertEqual(k_paths[1], caminos_resumidos)
        #self.assertEqual(k_paths[2], costos)

        print(len(k_paths[0]))

    def test_simulation(self):
        import numpy as np

        dump_file1 = open(os.path.join(PROJECT_DIR, 'tmp', 'grafo.igraph'), 'rb')
        g = pickle.load(dump_file1)
        dump_file1.close()

        dump_file1 = open(os.path.join(PROJECT_DIR, 'tmp', 'dict_servicio_llave_codigoTS.pkl'), 'rb')
        dict_servicio_llave_codigoTS = pickle.load(dump_file1)
        dump_file1.close()

        #origin = 'L-34-34-35-PO'
        #destination = 'M-TB'
        origin = 'L-34-41-100-OP'
        destination = 'M-BA'
        origin_index = g.vs.find(name2=origin).index
        destination_index = g.vs.find(name2=destination).index
        weights = "peso"
        camino = []
        camino_resumido = []
        costo_camino = []

        k_paths = simulation(g, origin_index, destination_index, weights, dict_servicio_llave_codigoTS)

        caminos_simples = [u'L-34-41-100-OP/F24-I/L-34-52-5-PO/M-EA/L4/M-VA/L5/M-BA', u'L-34-41-95-PO/712-I/T-34-269-SN-45/E12-I/L-33-65-5-OP/M-TR/L4/M-VA/L5/M-BA', u'L-34-41-100-OP/F23-R/T-34-270-NS-10/M-HS/L4/M-VA/L5/M-BA']
        caminos_resumidos = [u'L-34-41-100-OP/F24-I/L-34-52-5-PO/M-EA/M-BA', u'L-34-41-95-PO/712-I/T-34-269-SN-45/E12-I/L-33-65-5-OP/M-TR/M-BA', u'L-34-41-100-OP/F23-R/T-34-270-NS-10/M-HS/M-BA']
        costos = [46.31683333250615, 47.29293571343836, 48.72744999813938]
        #self.assertEqual(k_paths[0], caminos_simples)
        #self.assertEqual(k_paths[1], caminos_resumidos)
        #self.assertEqual(k_paths[2], costos)

        print(k_paths)


