class Quitar_variante():
    ''' clase para crear grafo '''
    def quitar_variante(self, x):

        x=str(x)

        if type(x) != str:
            return ''
        elif len(x) == 7:
            return ''.join([x[:3], x[6:7]])
        elif len(x) == 8:
            return ''.join([x[:4], x[7:8]])
        elif len(x) == 10:
            return ''.join([x[:5], x[9:10]])
        elif len(x) == 11:
            return ''.join([x[:6], x[10:11]])
        else:
            return x


