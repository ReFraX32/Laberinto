"""
MODULO: Logica del Laberinto recursivo
Contiene la definicion del laberinto fijo de 40x40 posiciones y las funciones
recursivas para resolverlo y comparar salidas mediante backtracking.
Utiliza pilas para el seguimiento del camino en la estructura LIFO.
Toda la interfaz visual se delega a interfaz.py.
"""

import sys
import tda_pila

# Aumentar limite de llamadas recursivas de 1000 a 5000
sys.setrecursionlimit(5000)


def obtener_laberinto():
    """
    ABSTRACCION: Devuelve la matriz del laberinto fijo de 40x40 posiciones.
    - Entrada: Ninguna.
    - Salida: Matriz bidimensional (lista de listas) con paredes ('X'), caminos ('.'), entrada ('E') y dos salidas ('S').
    """
    filas = [
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "XEX...X...X...........X.........X.....SX",
        "X.X.X.X.X.X.XXXXXXXXX.X.XXXXXXX.X.XXX.XX",
        "X.X.X.X.X.X...X.....X.X.X...X...X.X...XX",
        "X.X.X.X.X.XXX.X.XXX.X.X.X.X.XXXXX.X.X.XX",
        "X...X...X.X...X...X...X.X.X.......X.X.XX",
        "XXXXXXXXX.X.XXXXX.XXXXX.X.XXXXX.XXX.X.XX",
        "X.X.....X...X...X.....X...X...X.X...X.XX",
        "X.X.XXX.XXXXX.X.XXXXX.XXXXX.X.XXX.XXX.XX",
        "X.X.X.X...X...X.....X...X...X.....X...XX",
        "X.X.X.XXX.X.XXX.XXXXXXX.X.XXXXXXXXX.XXXX",
        "X.X.X...X.X...X.......X...X.....X...X.XX",
        "X.X.XXX.X.XXX.XXXXXXX.XXXXX.XXX.X.XXX.XX",
        "X.X...X.X.....X.....X...X...X...X.X...XX",
        "X.XXX.X.XXXXXXX.XXX.XXX.X.XXX.X.X.XXX.XX",
        "X.....X.......X.X...X...X.X...X.X.....XX",
        "X.XXXXX.X.XXX.X.X.XXX.XXX.X.XXXXXXXXX.XX",
        "X...X...X.X.X.X.X...X.....X.........X.XX",
        "XXX.XXXXX.X.X.X.XXXXXXXXXXXXXXX.X.XXX.XX",
        "X.X.......X.X.X.X.....X...X.....X.X...XX",
        "X.XXXXXXXXX.X.X.X.X.X.X.X.X.XXXXX.X.XXXX",
        "X...........X.X...X.X.X.X...X.....X...XX",
        "X.XXXXXXX.X.X.XXXXX.XXX.X.XXXXXXXXXXX.XX",
        "X.X.....X.X.X...X...X...X.X.........X.XX",
        "X.XXXXX.X.XXXXX.X.XXX.XXXXX.XXXXXXX.X.XX",
        "X.X.....X.X...X.X...X.X...X.......X...XX",
        "X.X.X.XXX.X.X.X.XXX.X.X.X.XXXXXXX.XXXXXX",
        "X...X.X...X.X...X...X...X.....X.X.X...XX",
        "XXXXX.X.X.X.XXXXX.XXXXXXX.XXX.X.X.X.X.XX",
        "X.....X.X.X.X.....X...X...X.....X.X.X.XX",
        "X.XXXXX.XXX.X.X.XXX.X.X.X.XXXXX.X.XXX.XX",
        "X.X...X.....X.X.X...X...X.X...X.X...X.XX",
        "X.X.X.XXXXXXX.XXX.XXX.XXXXX.X.XXXXX.X.XX",
        "X.X.X.X...X...X...X...X.....X.....X.X.XX",
        "X.X.X.X.X.X.XXX.XXXXX.X.XXXXXXXXX.X.X.XX",
        "X...X.X.X.X.X...X...X.X...X...X.X.X.X.XX",
        "XXXXX.X.X.X.X.XXX.X.XXXXX.X.X.X.X.X.X.XX",
        "X.......X...X.....X.........X...X.....XX",
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXSXX",
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    ]

    # Convertir la lista de strings en una matriz de listas de caracteres
    matriz = []
    for fila in filas:
        fila_individual = []
        for caracter in fila:
            fila_individual.append(caracter)
        matriz.append(fila_individual)
    return matriz


def copiar_laberinto(matriz):
    """
    ABSTRACCION: Genera una copia independiente de la matriz recibida.
    - Entrada: matriz (lista de listas).
    - Salida: Nueva lista de listas con los mismos elementos.
    """
    copia = []
    for fila in matriz:
        fila_copiada = []
        for celda in fila:
            fila_copiada.append(celda)
        copia.append(fila_copiada)
    return copia


def buscar_posicion(laberinto, simbolo):
    """
    ABSTRACCION: Busca las coordenadas de un caracter especifico dentro del laberinto.
    - Entrada: laberinto (lista de listas), simbolo (str de un solo caracter).
    - Salida: Tupla con (fila, columna) si lo encuentra, o (None, None) en caso contrario.
    """
    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[0])):
            if laberinto[fila][columna] == simbolo:
                return fila, columna
    return None, None


def buscar_todas_las_salidas(laberinto):
    """
    ABSTRACCION: Encuentra todas las coordenadas marcadas como salida ('S') en el laberinto.
    - Entrada: laberinto (lista de listas).
    - Salida: Lista de tuplas con las coordenadas de las salidas [(fila, columna), ...].
    """
    lista_salidas = []
    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[0])):
            if laberinto[fila][columna] == "S":
                lista_salidas.append((fila, columna))
    return lista_salidas


def contar_pasos_camino(laberinto):
    """
    ABSTRACCION: Cuenta la cantidad de casillas marcadas con asterisco en la solucion.
    - Entrada: laberinto (lista de listas).
    - Salida: Cantidad de casillas que forman el camino recorrido (int).
    """
    total_pasos = 0
    for fila in laberinto:
        for celda in fila:
            if celda == "*":
                total_pasos += 1
    return total_pasos


def resolver(laberinto, fila, columna):
    """
    ABSTRACCION: Resuelve el laberinto mediante recursion con retroceso (backtracking).
    - Entrada: laberinto (lista de listas), fila (int), columna (int).
    - Salida: Booleano que indica True si encontro una salida o False si no.
    """
    # Paso 1: Verificar si estamos fuera de los limites del mapa
    if fila < 0 or fila >= len(laberinto) or columna < 0 or columna >= len(laberinto[0]):
        return False

    # Paso 2: Verificar si chocamos con una pared o con una casilla ya visitada
    if laberinto[fila][columna] == "X" or laberinto[fila][columna] == "*":
        return False

    # Paso 3: Verificar si llegamos a una salida
    if laberinto[fila][columna] == "S":
        return True

    # Marcar la casilla actual con asterisco como parte del camino
    laberinto[fila][columna] = "*"

    # Probar las cuatro direcciones: arriba, abajo, izquierda y derecha
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for salto_fila, salto_columna in direcciones:
        nueva_fila = fila + salto_fila
        nueva_columna = columna + salto_columna
        if resolver(laberinto, nueva_fila, nueva_columna):
            return True

    # Retroceso (backtracking): Desmarcar la casilla si el camino no sirvio
    laberinto[fila][columna] = "."
    return False


def obtener_pasos_resolucion(laberinto_base, fila_inicio, columna_inicio):
    """
    ABSTRACCION: Registra cada paso de avance y retroceso del algoritmo utilizando pilas.
    - Entrada: laberinto_base (lista de listas), fila_inicio (int), columna_inicio (int).
    - Salida: Lista de tuplas con las acciones registradas [('marcar', fila, columna), ...].
    """
    copia = copiar_laberinto(laberinto_base)
    historial_de_pasos = []
    pila_camino = tda_pila.Pila()

    def buscar(fila_actual, columna_actual):
        # 1. Comprobar limites
        if fila_actual < 0 or fila_actual >= len(copia) or columna_actual < 0 or columna_actual >= len(copia[0]):
            return False

        # 2. Comprobar paredes o casillas ya visitadas
        if copia[fila_actual][columna_actual] == "X" or copia[fila_actual][columna_actual] == "*":
            return False

        # 3. Llegada a la meta
        if copia[fila_actual][columna_actual] == "S":
            tda_pila.apilar(pila_camino, (fila_actual, columna_actual))
            historial_de_pasos.append(("meta", fila_actual, columna_actual))
            return True

        # Marcar avance y apilar la posicion en la pila
        copia[fila_actual][columna_actual] = "*"
        tda_pila.apilar(pila_camino, (fila_actual, columna_actual))

        if (fila_actual, columna_actual) != (fila_inicio, columna_inicio):
            historial_de_pasos.append(("marcar", fila_actual, columna_actual))

        # Explorar direcciones: arriba, abajo, izquierda, derecha
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for salto_fila, salto_columna in direcciones:
            nueva_fila = fila_actual + salto_fila
            nueva_columna = columna_actual + salto_columna
            if buscar(nueva_fila, nueva_columna):
                return True

        # Retroceso: desmarcar la celda y desapilar
        copia[fila_actual][columna_actual] = "."
        tda_pila.desapilar(pila_camino)

        if (fila_actual, columna_actual) != (fila_inicio, columna_inicio):
            historial_de_pasos.append(("desmarcar", fila_actual, columna_actual))

        return False

    buscar(fila_inicio, columna_inicio)
    return historial_de_pasos


def obtener_pasos_comparacion(laberinto_base, fila_inicio, columna_inicio):
    """
    ABSTRACCION: Busca ambas salidas paso a paso y determina cual es la mas corta.
    - Entrada: laberinto_base (lista de listas), fila_inicio (int), columna_inicio (int).
    - Salida: Tupla con (historial_de_pasos, salida_ganadora, pasos_salida_1, pasos_salida_2).
    """
    salidas = buscar_todas_las_salidas(laberinto_base)
    if len(salidas) < 2:
        return [], None, 0, 0

    salida_1 = salidas[0]
    salida_2 = salidas[1]

    # Medir distancia a Salida 1 (tratando Salida 2 como pasillo temporal)
    laberinto_salida_1 = copiar_laberinto(laberinto_base)
    laberinto_salida_1[salida_2[0]][salida_2[1]] = "."
    encontrada_1 = resolver(laberinto_salida_1, fila_inicio, columna_inicio)
    if encontrada_1:
        pasos_salida_1 = contar_pasos_camino(laberinto_salida_1)
    else:
        pasos_salida_1 = 99999

    # Medir distancia a Salida 2 (tratando Salida 1 como pasillo temporal)
    laberinto_salida_2 = copiar_laberinto(laberinto_base)
    laberinto_salida_2[salida_1[0]][salida_1[1]] = "."
    encontrada_2 = resolver(laberinto_salida_2, fila_inicio, columna_inicio)
    if encontrada_2:
        pasos_salida_2 = contar_pasos_camino(laberinto_salida_2)
    else:
        pasos_salida_2 = 99999

    # Determinar cual salida es mas corta
    if pasos_salida_1 <= pasos_salida_2:
        salida_ganadora = salida_1
        nombre_ganadora = "Salida 1"
        pasos_ganadora = pasos_salida_1
    else:
        salida_ganadora = salida_2
        nombre_ganadora = "Salida 2"
        pasos_ganadora = pasos_salida_2

    # Registrar la animacion buscando ambas salidas
    copia = copiar_laberinto(laberinto_base)
    historial_de_pasos = []
    salidas_encontradas = []

    def buscar_ambas(fila_actual, columna_actual):
        if len(salidas_encontradas) == 2:
            return True

        if fila_actual < 0 or fila_actual >= len(copia) or columna_actual < 0 or columna_actual >= len(copia[0]):
            return False

        if copia[fila_actual][columna_actual] == "X" or copia[fila_actual][columna_actual] == "*":
            return False

        # Comprobar si llegamos a una de las dos salidas
        es_salida = (copia[fila_actual][columna_actual] == "S" or (fila_actual, columna_actual) == salida_1 or (fila_actual, columna_actual) == salida_2)
        if es_salida and (fila_actual, columna_actual) not in salidas_encontradas:
            salidas_encontradas.append((fila_actual, columna_actual))
            historial_de_pasos.append(("meta", fila_actual, columna_actual))
            if len(salidas_encontradas) == 2:
                return True

        simbolo_previo = copia[fila_actual][columna_actual]
        copia[fila_actual][columna_actual] = "*"

        if (fila_actual, columna_actual) != (fila_inicio, columna_inicio):
            historial_de_pasos.append(("marcar", fila_actual, columna_actual))

        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for salto_fila, salto_columna in direcciones:
            nueva_fila = fila_actual + salto_fila
            nueva_columna = columna_actual + salto_columna
            if buscar_ambas(nueva_fila, nueva_columna):
                if len(salidas_encontradas) == 2:
                    return True

        # Retroceso si no se encontraron ambas salidas por este camino
        if len(salidas_encontradas) < 2:
            if es_salida:
                copia[fila_actual][columna_actual] = simbolo_previo
            else:
                copia[fila_actual][columna_actual] = "."

            if (fila_actual, columna_actual) != (fila_inicio, columna_inicio):
                historial_de_pasos.append(("desmarcar", fila_actual, columna_actual))

        return False

    buscar_ambas(fila_inicio, columna_inicio)
    return historial_de_pasos, salida_ganadora, pasos_salida_1, pasos_salida_2


if __name__ == "__main__":
    import interfaz
    interfaz.iniciar()