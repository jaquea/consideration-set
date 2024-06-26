import json
import os
from collections import defaultdict
from unittest import TestCase

import dill
import pandas as pd

from path_size import correlacion, process_frame_alt, obtener_arcos


class PathSizeTestCase(TestCase):

    def setUp(self):
        with open(os.path.join('inputs', 'info_servicios.json')) as data_file:
            data = json.loads(data_file.read())
        self.df = pd.DataFrame.from_dict(data, orient='columns')

        with open(os.path.join('tmp', 'viajes_alternativas_desaglosadas_procesados.pkl'), 'rb') as dill_file:
            viajes_alternativas_desaglosadas_procesados = dill.load(dill_file)
        viajes_alternativas_procesados_p = defaultdict(lambda: defaultdict(list))
        #viajes_alternativas_procesados_p['T-13-104-PO-15']['M-TB'] = viajes_alternativas_desaglosadas_procesados['T-13-104-PO-15']['M-TB']
        viajes_alternativas_procesados_p['L-34-45-10-SN']['I-33-134-SN-67'] = viajes_alternativas_desaglosadas_procesados['L-34-45-10-SN']['I-33-134-SN-67']

        with open(os.path.join('tmp', 'grafo.igraph'), 'rb') as dill_file:
            g = dill.load(dill_file)

        self.PS = process_frame_alt(viajes_alternativas_procesados_p, g)

        print('PS', self.PS)

        with open(os.path.join('tmp', 'paradero_cercano_dic.pkl'), 'rb') as dill_file:
            self.paradero_cercano_dic = dill.load(dill_file)

        with open(os.path.join('tmp', 'tiempos.pkl'), 'rb') as dill_file:
            self.dict_tiempos = dill.load(dill_file)

    def test_path_size(self):
        print(correlacion(self.df, self.PS,  self.dict_tiempos))

    def test_obtener_arcos(self):
        print(obtener_arcos(self.df, '109', 'R', 'L-34-45-10-SN','I-33-134-SN-67'))


'T-25-228-SN-10/T-25-228-SN-50'