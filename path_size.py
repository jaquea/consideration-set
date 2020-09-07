#etapa 1: para un parOD generar diccionario que contenga todas las alternativas de viaje...este diccionario esta generado

#etapa 2: generar funcion que tome una alternativa de viaje, la recorra un diccionario con sus etapas

# 25/09/2018: se genera una función que permite obtener todos los arcos de una ruta entre un par OD de paraderos y un servicio
@functools.lru_cache(maxsize=None)
def obtener_arcos(ruta, par_subida, par_bajada):
    if par_subida[:2] == 'M-' and par_bajada[:2] == 'M-':
        arcos = [] # print(par_subida, par_bajada)

        trayectoria = func_ruta(par_subida, par_bajada)
        if len(trayectoria) == 0:
            return None

        trayectoria.reverse()

        # print(trayectoria)

        paraderos = []
        cabeza = par_subida
        contador = 0
        distancia_total = 0

        for i in trayectoria:

            paradero = i

            if contador == 0:
                contador += 1

            else:
                # print (cabeza, paradero)

                dist_arco = dis_entre_estaciones(cabeza, paradero)
                distancia_total += dist_arco
                arcos.append((cabeza, paradero, dist_arco))
                paraderos.append(cabeza)
                # print(cabeza, paradero, dist_arco)
                cabeza = paradero
                # distancia_cabeza=distancia
        paraderos.append(par_bajada)
        arcos = [arcos, [distancia_total], paraderos]
        return arcos


    else:

        conexion = psycopg2.connect(dbname="postgres", user="postgres", password="jgaf7440", host="localhost",
                                    port="5432")  # se crea la conexión

        cursor = conexion.cursor()

        cursor.execute("""select distinct serviciosentido, paradero, distenruta from perfil_junio2018_pm_arcos 
        where serviciosentido=%s and serviciosentido=%s
        order by distenruta;""", (ruta, ruta))

        profile = cursor.fetchall()

        arcos = []
        paraderos = []
        cabeza = par_subida
        correlativo_cabeza = 0
        distancia_cabeza = 0
        contador = 0
        distancia_total = 0

        for row in profile:
            servicio = row[0]
            paradero = row[1]
            distancia = row[2]

            if contador == 0 and paradero == par_subida:
                # correlativo_cabeza=correlativo
                distancia_cabeza = distancia
                contador += 1

            if paradero != par_subida and distancia_cabeza >= 0 and contador > 0:
                dist_arco = distancia - distancia_cabeza
                distancia_total += dist_arco
                arcos.append((cabeza, paradero, dist_arco))
                paraderos.append(cabeza)
                # print(cabeza, paradero, dist_arco)
                cabeza = paradero
                distancia_cabeza = distancia

            if paradero == par_bajada and contador > 0:
                paraderos.append(paradero)
                if distancia_total == 0:
                    return None
                else:
                    return [arcos, [distancia_total], paraderos]

        if contador == 0:
            return None




