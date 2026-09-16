"""
MODULO: Resolucion de Laberintos Mediante Algoritmos Recursivos
Programa que modela, navega y resuelve un laberinto de 40x40 posiciones.
Permite generacion aleatoria simple, navegacion manual con teclado (WASD y flechas),
resolucion automatica y comparacion de salidas usando backtracking recursivo.
"""

import subprocess
import sys
import time
import random

# Aumentar el limite de llamadas recursivas para evitar errores en una matriz de 40x40
sys.setrecursionlimit(5000)


def generar_laberinto_aleatorio():
    """
    ABSTRACCION: Genera una matriz de 40x40 con entrada, salidas y caminos aleatorios de forma simple.
    - Entrada: Ninguna.
    - Salida: Matriz bidimensional (lista de listas) con paredes ('X'), caminos ('.'), entrada ('E') y dos salidas ('S').
    """
    total_filas = 40
    total_columnas = 40

    # 1. Crear el mapa lleno de paredes 'X'
    matriz = []
    for fila in range(total_filas):
        matriz.append(["X"] * total_columnas)

    # 2. Abrir pasillos conectando cada celda impar hacia arriba o hacia la izquierda
    for fila in range(1, total_filas - 1, 2):
        for columna in range(1, total_columnas - 1, 2):
            matriz[fila][columna] = "."
            opciones_de_conexion = []
            if fila > 1:
                opciones_de_conexion.append((-1, 0))  # Opcion de conectar hacia arriba
            if columna > 1:
                opciones_de_conexion.append((0, -1))  # Opcion de conectar hacia la izquierda

            if len(opciones_de_conexion) > 0:
                paso_fila, paso_columna = random.choice(opciones_de_conexion)
                matriz[fila + paso_fila][columna + paso_columna] = "."

    # 3. Reunir todas las casillas transitables para elegir entrada y salidas al azar
    casillas_disponibles = []
    for fila in range(1, total_filas - 1, 2):
        for columna in range(1, total_columnas - 1, 2):
            casillas_disponibles.append((fila, columna))

    random.shuffle(casillas_disponibles)

    # Entrada aleatoria
    fila_entrada, columna_entrada = casillas_disponibles.pop()

    # Salidas aleatorias (buscamos que esten a una distancia minima para que no queden pegadas a la entrada)
    salidas_elegidas = []
    for fila_candidata, columna_candidata in casillas_disponibles:
        distancia = abs(fila_candidata - fila_entrada) + abs(columna_candidata - columna_entrada)
        if distancia >= 15:
            salidas_elegidas.append((fila_candidata, columna_candidata))
            if len(salidas_elegidas) == 2:
                break

    # Si la distancia de 15 no se cumplio para dos salidas, tomar las dos primeras disponibles
    if len(salidas_elegidas) < 2:
        salidas_elegidas = casillas_disponibles[:2]

    fila_salida_1, columna_salida_1 = salidas_elegidas[0]
    fila_salida_2, columna_salida_2 = salidas_elegidas[1]

    # Colocar los simbolos en la matriz
    matriz[fila_entrada][columna_entrada] = "E"
    matriz[fila_salida_1][columna_salida_1] = "S"
    matriz[fila_salida_2][columna_salida_2] = "S"

    return matriz


def copiar_laberinto(matriz):
    """
    ABSTRACCION: Genera una copia independiente de la matriz recibida.
    - Entrada: matriz (lista de listas).
    - Salida: Nueva lista de listas con los mismos elementos.
    """
    copia = []
    for fila in matriz:
        copia.append(list(fila))
    return copia


def mostrar_laberinto(laberinto, pausa=0.01):
    """
    ABSTRACCION: Limpia la pantalla e imprime el estado actual del laberinto.
    - Entrada: laberinto (lista de listas), pausa (float con el tiempo de espera en segundos).
    - Salida: Ninguna.
    """
    subprocess.run(["cls"], shell=True)
    for fila in laberinto:
        print(" ".join(fila))
    if pausa > 0:
        time.sleep(pausa)


def buscar_posicion(laberinto, simbolo):
    """
    ABSTRACCION: Busca las coordenadas de un caracter especifico dentro del laberinto.
    - Entrada: laberinto (lista de listas), simbolo (str de longitud 1).
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
    - Salida: Lista de tuplas con las coordenadas [(fila, columna), ...].
    """
    lista_de_salidas = []
    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[0])):
            if laberinto[fila][columna] == "S":
                lista_de_salidas.append((fila, columna))
    return lista_de_salidas


def contar_pasos_camino(laberinto):
    """
    ABSTRACCION: Cuenta la cantidad de casillas marcadas con asterisco en la solucion.
    - Entrada: laberinto (lista de listas).
    - Salida: Cantidad de casillas que forman el camino (int).
    """
    total_pasos = 0
    for fila in laberinto:
        for celda in fila:
            if celda == "*":
                total_pasos += 1
    return total_pasos


def leer_tecla():
    """
    ABSTRACCION: Lee una tecla presionada en tiempo real. Soporta W, A, S, D y flechas direccionales del teclado.
    - Entrada: Ninguna.
    - Salida: String con la direccion ('arriba', 'abajo', 'izquierda', 'derecha', 'salir') o None.
    """
    try:
        import msvcrt
        tecla = msvcrt.getch()

        # En Windows, las flechas envian un codigo de prefijo especial (0x00 o 0xe0)
        if tecla in (b"\x00", b"\xe0"):
            codigo_flecha = msvcrt.getch()
            if codigo_flecha == b"H":
                return "arriba"
            elif codigo_flecha == b"P":
                return "abajo"
            elif codigo_flecha == b"K":
                return "izquierda"
            elif codigo_flecha == b"M":
                return "derecha"
        else:
            letra = tecla.decode("latin1", errors="ignore").lower()
            if letra == "w":
                return "arriba"
            elif letra == "s":
                return "abajo"
            elif letra == "a":
                return "izquierda"
            elif letra == "d":
                return "derecha"
            elif letra in ("q", "\x1b"):
                return "salir"
    except Exception:
        entrada = input("Mover (W=Arriba, S=Abajo, A=Izq, D=Der, Q=Salir): ").strip().lower()
        if entrada == "w":
            return "arriba"
        elif entrada == "s":
            return "abajo"
        elif entrada == "a":
            return "izquierda"
        elif entrada == "d":
            return "derecha"
        elif entrada == "q":
            return "salir"

    return None


def jugar_manual(laberinto_base):
    """
    ABSTRACCION: Permite al usuario recorrer el laberinto en vivo usando el teclado.
    - Entrada: laberinto_base (lista de listas).
    - Salida: Ninguna.
    """
    laberinto = copiar_laberinto(laberinto_base)
    fila_entrada, columna_entrada = buscar_posicion(laberinto, "E")

    if fila_entrada is None:
        print("Error: No se encontro la entrada E.")
        input("Presione Enter para volver...")
        return

    fila_jugador = fila_entrada
    columna_jugador = columna_entrada
    pasos_dados = 0
    mensaje_alerta = ""

    while True:
        # Colocar al jugador temporalmente en la matriz
        laberinto[fila_jugador][columna_jugador] = "P"
        mostrar_laberinto(laberinto, 0.0)
        print(f"Posicion: ({fila_jugador}, {columna_jugador}) | Pasos: {pasos_dados}")
        print("Moverse: W/A/S/D o Flechas | Salir: Q")
        if mensaje_alerta != "":
            print(mensaje_alerta)
            mensaje_alerta = ""

        # Restaurar la celda al mover el jugador (si es la entrada conserva 'E', si no '.')
        if fila_jugador == fila_entrada and columna_jugador == columna_entrada:
            laberinto[fila_jugador][columna_jugador] = "E"
        else:
            laberinto[fila_jugador][columna_jugador] = "."

        # Capturar tecla presionada por el usuario
        direccion = leer_tecla()

        if direccion == "salir":
            print("Partida cancelada.")
            time.sleep(1)
            break

        nueva_fila = fila_jugador
        nueva_columna = columna_jugador

        if direccion == "arriba":
            nueva_fila -= 1
        elif direccion == "abajo":
            nueva_fila += 1
        elif direccion == "izquierda":
            nueva_columna -= 1
        elif direccion == "derecha":
            nueva_columna += 1
        else:
            continue

        # Validar limites de la matriz
        if nueva_fila < 0 or nueva_fila >= len(laberinto) or nueva_columna < 0 or nueva_columna >= len(laberinto[0]):
            mensaje_alerta = "Limite del tablero."
            continue

        # Validar pared
        if laberinto[nueva_fila][nueva_columna] == "X":
            mensaje_alerta = "Hay una pared."
            continue

        # Validar si llego a una salida
        if laberinto[nueva_fila][nueva_columna] == "S":
            pasos_dados += 1
            laberinto[nueva_fila][nueva_columna] = "P"
            mostrar_laberinto(laberinto, 0.0)
            print(f"Llegaste a la salida en {pasos_dados} pasos!")
            input("Presione Enter para volver al menu...")
            break

        fila_jugador = nueva_fila
        columna_jugador = nueva_columna
        pasos_dados += 1


def resolver(laberinto, fila, columna, pausa=0.01):
    """
    ABSTRACCION: Resuelve el laberinto mediante recursividad con retroceso (backtracking).
    - Entrada: laberinto (lista de listas), fila (int), columna (int), pausa (float).
    - Salida: Booleano que indica True si encontro una salida o False si no (bool).
    """
    # Casos base: fuera de los limites
    if fila < 0 or fila >= len(laberinto) or columna < 0 or columna >= len(laberinto[0]):
        return False

    # Casos base: pared o casilla ya visitada
    if laberinto[fila][columna] in ("X", "*"):
        return False

    # Caso base: llegada a una salida
    if laberinto[fila][columna] == "S":
        if pausa > 0:
            mostrar_laberinto(laberinto, pausa)
        return True

    # Marcar el paso en el camino actual
    laberinto[fila][columna] = "*"
    if pausa > 0:
        mostrar_laberinto(laberinto, pausa)

    # Explorar las cuatro direcciones (arriba, abajo, izquierda, derecha)
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for desplazamiento_fila, desplazamiento_columna in movimientos:
        if resolver(laberinto, fila + desplazamiento_fila, columna + desplazamiento_columna, pausa):
            return True

    # Retroceso: desmarcar si ninguna direccion sirvio
    laberinto[fila][columna] = "."
    if pausa > 0:
        mostrar_laberinto(laberinto, pausa)
    return False


def obtener_pasos_resolucion(laberinto_base, fila_inicio, columna_inicio, salida_bloqueada=None):
    """
    ABSTRACCION: Ejecuta backtracking recursivo registrando cada avance y retroceso para animacion paso a paso.
    - Entrada: laberinto_base (lista de listas), fila_inicio (int), columna_inicio (int), salida_bloqueada (tupla opcional).
    - Salida: Lista de tuplas con las acciones registradas [('marcar', fila, columna), ('desmarcar', fila, columna), ...].
    """
    copia = copiar_laberinto(laberinto_base)
    # Si se especifica una salida ignorada, se trata como pasillo normal para permitir transito
    if salida_bloqueada is not None:
        copia[salida_bloqueada[0]][salida_bloqueada[1]] = "."

    historial_de_pasos = []

    def buscar(fila_actual, columna_actual):
        if fila_actual < 0 or fila_actual >= len(copia) or columna_actual < 0 or columna_actual >= len(copia[0]):
            return False
        if copia[fila_actual][columna_actual] in ("X", "*"):
            return False
        if copia[fila_actual][columna_actual] == "S":
            historial_de_pasos.append(("meta", fila_actual, columna_actual))
            return True

        copia[fila_actual][columna_actual] = "*"
        historial_de_pasos.append(("marcar", fila_actual, columna_actual))

        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for desplazamiento_fila, desplazamiento_columna in movimientos:
            if buscar(fila_actual + desplazamiento_fila, columna_actual + desplazamiento_columna):
                return True

        copia[fila_actual][columna_actual] = "."
        historial_de_pasos.append(("desmarcar", fila_actual, columna_actual))
        return False

    buscar(fila_inicio, columna_inicio)
    return historial_de_pasos


def obtener_pasos_comparacion(laberinto_base, fila_inicio, columna_inicio):
    """
    ABSTRACCION: Busca ambas salidas recursivamente registrando el hallazgo de la primera y la busqueda de la segunda.
    - Entrada: laberinto_base (lista de listas), fila_inicio (int), columna_inicio (int).
    - Salida: Tupla con (historial_de_pasos, salida_ganadora, pasos_salida_1, pasos_salida_2, texto_resumen).
    """
    salidas = buscar_todas_las_salidas(laberinto_base)
    if len(salidas) < 2:
        return [], None, 0, 0, "Error: No hay suficientes salidas para comparar."

    salida_1 = salidas[0]
    salida_2 = salidas[1]

    # Probar camino hacia Salida 1 (tratando Salida 2 como pasillo para no cortar ramas)
    laberinto_salida_1 = copiar_laberinto(laberinto_base)
    laberinto_salida_1[salida_2[0]][salida_2[1]] = "."
    encontrado_salida_1 = resolver(laberinto_salida_1, fila_inicio, columna_inicio, pausa=0.0)
    pasos_salida_1 = contar_pasos_camino(laberinto_salida_1) if encontrado_salida_1 else 99999

    # Probar camino hacia Salida 2 (tratando Salida 1 como pasillo para no cortar ramas)
    laberinto_salida_2 = copiar_laberinto(laberinto_base)
    laberinto_salida_2[salida_1[0]][salida_1[1]] = "."
    encontrado_salida_2 = resolver(laberinto_salida_2, fila_inicio, columna_inicio, pausa=0.0)
    pasos_salida_2 = contar_pasos_camino(laberinto_salida_2) if encontrado_salida_2 else 99999

    if pasos_salida_1 <= pasos_salida_2 and encontrado_salida_1:
        salida_ganadora = salida_1
        matriz_ganadora = laberinto_salida_1
        texto_resumen = f"Salida 1 en {salida_1}: {pasos_salida_1} pasos | Salida 2 en {salida_2}: {pasos_salida_2} pasos -> Mas eficiente: Salida 1 ({pasos_salida_1} pasos)"
    elif encontrado_salida_2:
        salida_ganadora = salida_2
        matriz_ganadora = laberinto_salida_2
        texto_resumen = f"Salida 1 en {salida_1}: {pasos_salida_1} pasos | Salida 2 en {salida_2}: {pasos_salida_2} pasos -> Mas eficiente: Salida 2 ({pasos_salida_2} pasos)"
    else:
        return [], None, 0, 0, "Error: No se pudo alcanzar ninguna salida."

    # Registrar pasos de busqueda de ambas salidas
    copia = copiar_laberinto(laberinto_base)
    historial_de_pasos = []
    salidas_encontradas = set()

    def buscar_ambas(fila_actual, columna_actual):
        if len(salidas_encontradas) == 2:
            return True

        if fila_actual < 0 or fila_actual >= len(copia) or columna_actual < 0 or columna_actual >= len(copia[0]):
            return False
        if copia[fila_actual][columna_actual] in ("X", "*"):
            return False

        es_salida = (copia[fila_actual][columna_actual] == "S" or (fila_actual, columna_actual) in (salida_1, salida_2))
        if es_salida and (fila_actual, columna_actual) not in salidas_encontradas:
            salidas_encontradas.add((fila_actual, columna_actual))
            historial_de_pasos.append(("meta", fila_actual, columna_actual))
            if len(salidas_encontradas) == 2:
                return True

        simbolo_previo = copia[fila_actual][columna_actual]
        copia[fila_actual][columna_actual] = "*"
        if (fila_actual, columna_actual) != (fila_inicio, columna_inicio):
            historial_de_pasos.append(("marcar", fila_actual, columna_actual))

        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for desplazamiento_fila, desplazamiento_columna in movimientos:
            if buscar_ambas(fila_actual + desplazamiento_fila, columna_actual + desplazamiento_columna):
                if len(salidas_encontradas) == 2:
                    return True

        if len(salidas_encontradas) < 2:
            copia[fila_actual][columna_actual] = simbolo_previo if es_salida else "."
            if (fila_actual, columna_actual) != (fila_inicio, columna_inicio):
                historial_de_pasos.append(("desmarcar", fila_actual, columna_actual))

        return False

    buscar_ambas(fila_inicio, columna_inicio)

    # Limpiar tablero y marcar la ruta ganadora final
    historial_de_pasos.append(("limpiar_tablero", 0, 0))
    for fila in range(len(laberinto_base)):
        for columna in range(len(laberinto_base[0])):
            if matriz_ganadora[fila][columna] == "*" and (fila, columna) != (fila_inicio, columna_inicio):
                historial_de_pasos.append(("marcar_optimo", fila, columna))
    historial_de_pasos.append(("meta_final", salida_ganadora[0], salida_ganadora[1]))

    return historial_de_pasos, salida_ganadora, pasos_salida_1, pasos_salida_2, texto_resumen


def ejecutar_automatico(laberinto_base):
    """
    ABSTRACCION: Ejecuta la resolucion automatica hacia la primera salida que encuentre y muestra el resultado.
    - Entrada: laberinto_base (lista de listas).
    - Salida: Ninguna.
    """
    laberinto = copiar_laberinto(laberinto_base)
    fila_entrada, columna_entrada = buscar_posicion(laberinto, "E")

    if fila_entrada is None:
        print("Error: No se encontro la entrada E.")
        input("Presione Enter para volver...")
        return

    encontrado = resolver(laberinto, fila_entrada, columna_entrada, 0.01)

    # Restaurar la E para mostrar el camino completo
    laberinto[fila_entrada][columna_entrada] = "E"
    mostrar_laberinto(laberinto, 0.0)

    if encontrado:
        total_pasos = contar_pasos_camino(laberinto)
        print(f"Salida encontrada en {total_pasos} pasos.")
    else:
        print("No se encontro ninguna salida.")

    input("Presione Enter para volver al menu...")


def comparar_salidas(laberinto_base):
    """
    ABSTRACCION: Recorre el laberinto hacia ambas salidas y calcula cual requiere menos movimientos.
    - Entrada: laberinto_base (lista de listas).
    - Salida: Ninguna. Imprime la comparacion y muestra el camino mas corto en pantalla.
    """
    fila_entrada, columna_entrada = buscar_posicion(laberinto_base, "E")
    lista_de_salidas = buscar_todas_las_salidas(laberinto_base)

    if fila_entrada is None or len(lista_de_salidas) < 2:
        print("Error: No hay suficientes salidas para comparar.")
        input("Presione Enter para volver...")
        return

    fila_salida_1, columna_salida_1 = lista_de_salidas[0]
    fila_salida_2, columna_salida_2 = lista_de_salidas[1]

    # Probar camino hacia Salida 1 (tratando Salida 2 como pasillo temporal)
    laberinto_salida_1 = copiar_laberinto(laberinto_base)
    laberinto_salida_1[fila_salida_2][columna_salida_2] = "."
    encontrado_salida_1 = resolver(laberinto_salida_1, fila_entrada, columna_entrada, 0.0)
    laberinto_salida_1[fila_salida_2][columna_salida_2] = "S"
    pasos_salida_1 = contar_pasos_camino(laberinto_salida_1) if encontrado_salida_1 else None

    # Probar camino hacia Salida 2 (tratando Salida 1 como pasillo temporal)
    laberinto_salida_2 = copiar_laberinto(laberinto_base)
    laberinto_salida_2[fila_salida_1][columna_salida_1] = "."
    encontrado_salida_2 = resolver(laberinto_salida_2, fila_entrada, columna_entrada, 0.0)
    laberinto_salida_2[fila_salida_1][columna_salida_1] = "S"
    pasos_salida_2 = contar_pasos_camino(laberinto_salida_2) if encontrado_salida_2 else None

    # Comparar resultados y elegir el camino mas corto
    coordenadas_salida_1 = (fila_salida_1, columna_salida_1)
    coordenadas_salida_2 = (fila_salida_2, columna_salida_2)

    if pasos_salida_1 is not None and pasos_salida_2 is not None:
        if pasos_salida_1 < pasos_salida_2:
            camino_ganador = laberinto_salida_1
            mensaje = f"La Salida 1 en {coordenadas_salida_1} es mas corta ({pasos_salida_1} pasos vs {pasos_salida_2} pasos)."
        elif pasos_salida_2 < pasos_salida_1:
            camino_ganador = laberinto_salida_2
            mensaje = f"La Salida 2 en {coordenadas_salida_2} es mas corta ({pasos_salida_2} pasos vs {pasos_salida_1} pasos)."
        else:
            camino_ganador = laberinto_salida_1
            mensaje = f"Ambas salidas tienen la misma distancia ({pasos_salida_1} pasos)."
    elif pasos_salida_1 is not None:
        camino_ganador = laberinto_salida_1
        mensaje = f"Solo se alcanzo la Salida 1 en {coordenadas_salida_1} ({pasos_salida_1} pasos)."
    elif pasos_salida_2 is not None:
        camino_ganador = laberinto_salida_2
        mensaje = f"Solo se alcanzo la Salida 2 en {coordenadas_salida_2} ({pasos_salida_2} pasos)."
    else:
        camino_ganador = laberinto_base
        mensaje = "No se pudo alcanzar ninguna salida."

    camino_ganador[fila_entrada][columna_entrada] = "E"
    mostrar_laberinto(camino_ganador, 0.0)
    print("Comparacion de salidas:")
    print(f"- Salida 1 en {coordenadas_salida_1}: {pasos_salida_1} pasos")
    print(f"- Salida 2 en {coordenadas_salida_2}: {pasos_salida_2} pasos")
    print(mensaje)
    input("Presione Enter para volver al menu...")


def menu_principal():
    """
    ABSTRACCION: Muestra el menu de opciones y controla el flujo del programa.
    - Entrada: Ninguna.
    - Salida: Ninguna.
    """
    laberinto_actual = generar_laberinto_aleatorio()

    while True:
        subprocess.run(["cls"], shell=True)
        print("=== Laberinto 40x40 ===")
        print("1. Jugar manual (WASD o Flechas)")
        print("2. Resolver automaticamente")
        print("3. Comparar ambas salidas (camino mas corto)")
        print("4. Generar nuevo laberinto aleatorio")
        print("5. Salir")
        opcion = input("Ingrese una opcion: ").strip()

        if opcion == "1":
            jugar_manual(laberinto_actual)
        elif opcion == "2":
            ejecutar_automatico(laberinto_actual)
        elif opcion == "3":
            comparar_salidas(laberinto_actual)
        elif opcion == "4":
            laberinto_actual = generar_laberinto_aleatorio()
            mostrar_laberinto(laberinto_actual, 0.0)
            print("Nuevo laberinto generado.")
            input("Presione Enter para continuar...")
        elif opcion == "5":
            print("Fin del programa.")
            break
        else:
            print("Opcion invalida.")
            time.sleep(1)


if __name__ == "__main__":
    menu_principal()