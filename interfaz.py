"""
MODULO: Interfaz Grafica del Laberinto con Pygame-CE
Permite jugar interactivamente recorriendo el laberinto fijo de 40x40, ver
la resolucion automatica paso a paso con backtracking y comparar ambas salidas.
"""

import pygame
import logica
import tda_pila

# CONFIGURACION DE DIMENSIONES Y COLORES
tamanio_celda = 20                                  # Cada casilla del laberinto mide 20x20 pixeles
filas = 40                                          # Cantidad de filas del laberinto
columnas = 40                                       # Cantidad de columnas del laberinto
ancho_pantalla = columnas * tamanio_celda           # 40 * 20 = 800 pixeles
alto_tablero = filas * tamanio_celda                # 40 * 20 = 800 pixeles
alto_panel_inferior = 80                            # 80 pixeles para textos y botones
alto_pantalla = alto_tablero + alto_panel_inferior  # Total: 880 pixeles

# Velocidad de la animacion de resolucion automatica
pasos_por_fotograma = 3

# Colores en formato RGB (Rojo, Verde, Azul)
color_fondo = (0, 0, 0)                  # Negro
color_pared_relleno = (10, 15, 60)       # Azul oscuro
color_pared_borde = (30, 60, 200)        # Azul brillante
color_pasillo = (30, 40, 70)             # Puntos tenues en el camino
color_jugador = (255, 255, 0)            # Amarillo
color_salida = (255, 0, 90)              # Rosa
color_entrada = (0, 255, 140)            # Verde esmeralda
color_solucion = (0, 255, 255)           # Celeste

# ESTADO DEL JUEGO
juego = {
    "tablero_base": [],                          # Matriz original del laberinto con 'X', '.', 'E', 'S'
    "tablero_visual": [],                        # Matriz que se dibuja en pantalla (incluye '*' y 'P')
    "fila_inicio": 0,                            # Fila de la entrada 'E'
    "columna_inicio": 0,                         # Columna de la entrada 'E'
    "fila_jugador": 0,                           # Fila actual del personaje
    "columna_jugador": 0,                        # Columna actual del personaje
    "pasos": 0,                                  # Cantidad de pasos recorridos
    "mensaje": "USA FLECHAS O WASD PARA JUGAR",
    "bloqueado": False,                          # True cuando termina la partida o hay animacion
    "cola_animacion": [],                        # Lista de pasos pendientes para animar
    "esperando_cartel": None,                    # Indica que cartel mostrar al terminar la animacion
    "mostrar_cartel": False,                     # Si es True, se dibuja la ventana modal en pantalla
    "titulo_cartel": "",                         # Titulo principal del cartel modal
    "linea_cartel_1": "",                        # Primera linea de detalle
    "linea_cartel_2": "",                        # Segunda linea de detalle
    "historial_movimientos": None                # Pila con las coordenadas recorridas
}


def maximizar_ventana():
    """
    ABSTRACCION: En Windows, le solicita al sistema operativo maximizar la ventana
    para que ocupe toda la pantalla manteniendo la barra de titulo y bordes estandar.
    - Entrada: Ninguna.
    - Salida: Ninguna.
    """
    try:
        import ctypes
        # Obtenemos el identificador de ventana de Pygame
        id_ventana = pygame.display.get_wm_info().get("window")
        if id_ventana:
            # El numero 3 representa el comando SW_MAXIMIZE de Windows
            ctypes.windll.user32.ShowWindow(id_ventana, 3)
    except Exception:
        pass


def reiniciar_laberinto():
    """
    ABSTRACCION: Reinicia la partida, cargando el mapa y ubicando al jugador en 'E'.
    - Entrada: Ninguna.
    - Salida: Ninguna.
    """
    juego["tablero_base"] = logica.obtener_laberinto()
    juego["fila_inicio"], juego["columna_inicio"] = logica.buscar_posicion(juego["tablero_base"], "E")
    juego["tablero_visual"] = logica.copiar_laberinto(juego["tablero_base"])

    # Ubicar al jugador en la entrada inicial
    juego["fila_jugador"] = juego["fila_inicio"]
    juego["columna_jugador"] = juego["columna_inicio"]
    juego["tablero_visual"][juego["fila_jugador"]][juego["columna_jugador"]] = "P"

    # Restablecer datos de la partida
    juego["pasos"] = 0
    juego["mensaje"] = "USA FLECHAS O WASD PARA JUGAR"
    juego["bloqueado"] = False
    juego["cola_animacion"] = []
    juego["esperando_cartel"] = None
    juego["mostrar_cartel"] = False

    # Inicializar la pila de movimientos con la posicion inicial
    juego["historial_movimientos"] = tda_pila.Pila()
    tda_pila.apilar(juego["historial_movimientos"], (juego["fila_inicio"], juego["columna_inicio"]))


def mover_jugador(desplazamiento_fila, desplazamiento_columna):
    """
    ABSTRACCION: Intenta mover al personaje una posicion si el camino esta libre.
    - Entrada: desplazamiento_fila (-1, 0, 1), desplazamiento_columna (-1, 0, 1).
    - Salida: Ninguna.
    """
    # Si la partida ya finalizo o se esta ejecutando una animacion, no permitir mover
    if juego["bloqueado"] == True or len(juego["cola_animacion"]) > 0:
        return

    nueva_fila = juego["fila_jugador"] + desplazamiento_fila
    nueva_columna = juego["columna_jugador"] + desplazamiento_columna

    # 1. Comprobar que no se salga de los limites del laberinto
    if nueva_fila < 0 or nueva_fila >= filas or nueva_columna < 0 or nueva_columna >= columnas:
        juego["mensaje"] = "** BORDE DEL MAPA **"
        return

    # 2. Comprobar si hay una pared
    celda_destino = juego["tablero_base"][nueva_fila][nueva_columna]
    if celda_destino == "X":
        juego["mensaje"] = "** HAY UNA PARED **"
        return

    # 3. Restaurar la casilla anterior (deja 'E' si era el inicio, sino '.')
    if juego["fila_jugador"] == juego["fila_inicio"] and juego["columna_jugador"] == juego["columna_inicio"]:
        juego["tablero_visual"][juego["fila_jugador"]][juego["columna_jugador"]] = "E"
    else:
        juego["tablero_visual"][juego["fila_jugador"]][juego["columna_jugador"]] = "."

    # 4. Apilar el nuevo paso
    tda_pila.apilar(juego["historial_movimientos"], (nueva_fila, nueva_columna))

    # 5. Colocar al personaje en la nueva coordenada
    juego["fila_jugador"] = nueva_fila
    juego["columna_jugador"] = nueva_columna
    juego["pasos"] += 1
    juego["tablero_visual"][juego["fila_jugador"]][juego["columna_jugador"]] = "P"

    # 6. Comprobar si llego a una de las salidas
    if celda_destino == "S":
        juego["bloqueado"] = True
        juego["mostrar_cartel"] = True
        juego["titulo_cartel"] = "¡LLEGASTE A LA SALIDA!"
        juego["linea_cartel_1"] = f"REALIZASTE {juego['pasos']} PASOS"
        juego["linea_cartel_2"] = "OBJETIVO ALCANZADO DE MANERA MANUAL"
        juego["mensaje"] = "LLEGADA A LA META"
    else:
        juego["mensaje"] = f"POSICIÓN: ({juego['fila_jugador']}, {juego['columna_jugador']})"


def resolver_automatico():
    """
    ABSTRACCION: Obtiene los pasos recursivos de backtracking y activa la animacion.
    - Entrada: Ninguna.
    - Salida: Ninguna.
    """
    historial = logica.obtener_pasos_resolucion(juego["tablero_base"], juego["fila_inicio"], juego["columna_inicio"])
    if len(historial) > 0:
        juego["mostrar_cartel"] = False
        juego["bloqueado"] = True
        juego["pasos"] = 0
        juego["tablero_visual"] = logica.copiar_laberinto(juego["tablero_base"])
        juego["cola_animacion"] = historial
        juego["mensaje"] = f"RESOLVIENDO PASO A PASO ({len(historial)} ACCIONES)..."
        juego["esperando_cartel"] = "resolucion"


def comparar_salidas():
    """
    ABSTRACCION: Compara la distancia a ambas salidas y anima la busqueda en vivo.
    - Entrada: Ninguna.
    - Salida: Ninguna.
    """
    historial, ganadora, pasos_s1, pasos_s2 = logica.obtener_pasos_comparacion(
        juego["tablero_base"], juego["fila_inicio"], juego["columna_inicio"]
    )
    if len(historial) > 0:
        juego["mostrar_cartel"] = False
        juego["bloqueado"] = True
        juego["pasos"] = 0
        juego["tablero_visual"] = logica.copiar_laberinto(juego["tablero_base"])
        juego["cola_animacion"] = historial
        juego["mensaje"] = "COMPARANDO SALIDAS..."

        if pasos_s1 <= pasos_s2:
            texto_ganadora = f"SALIDA 1 EN {ganadora} ({pasos_s1} PASOS)"
        else:
            texto_ganadora = f"SALIDA 2 EN {ganadora} ({pasos_s2} PASOS)"

        juego["titulo_cartel"] = "COMPARACIÓN DE SALIDAS"
        juego["linea_cartel_1"] = f"SALIDA 1: {pasos_s1} PASOS   |   SALIDA 2: {pasos_s2} PASOS"
        juego["linea_cartel_2"] = f"MÁS EFICIENTE: {texto_ganadora}"
        juego["esperando_cartel"] = "comparacion"


def iniciar():
    """
    ABSTRACCION: Bucle principal de la aplicacion grafica en Pygame.
    Controla los eventos, la actualizacion de fotogramas y el dibujo en pantalla.
    - Entrada: Ninguna.
    - Salida: Ninguna.
    """
    # Inicializar la biblioteca Pygame
    pygame.init()

    # Permitir que al mantener apretada una tecla, el movimiento continue
    # (primer valor: retraso inicial de 200 ms, segundo valor: repeticion cada 60 ms)
    pygame.key.set_repeat(200, 60)

    # Crear la ventana con soporte para redimensionarse
    ventana = pygame.display.set_mode((ancho_pantalla, alto_pantalla), pygame.RESIZABLE)
    pygame.display.set_caption("Laberinto 40x40 Recursivo")

    # Maximizar la ventana en Windows
    maximizar_ventana()

    # Creamos una superficie virtual con el tamaño original (800x880).
    superficie = pygame.Surface((ancho_pantalla, alto_pantalla))
    reloj = pygame.time.Clock()

    # Fuentes de texto
    fuente_texto = pygame.font.SysFont("Courier New", 13, bold=True)
    fuente_hud = pygame.font.SysFont("Courier New", 12, bold=True)
    fuente_banner = pygame.font.SysFont("Courier New", 26, bold=True)
    fuente_subbanner = pygame.font.SysFont("Courier New", 15, bold=True)

    # Definicion de los tres botones inferiores: (rectangulo_en_pantalla, texto, funcion)
    botones = [
        (pygame.Rect(40, alto_tablero + 40, 210, 30), "[R] RESOLVER", resolver_automatico),
        (pygame.Rect(290, alto_tablero + 40, 220, 30), "[C] COMPARAR SALIDAS", comparar_salidas),
        (pygame.Rect(550, alto_tablero + 40, 210, 30), "[ESPACIO] REINICIAR", reiniciar_laberinto),
    ]

    reiniciar_laberinto()
    ejecutando = True
    contador_fotogramas = 0

    # BUCLE PRINCIPAL DEL JUEGO
    while ejecutando:
        contador_fotogramas += 1

        # Calculo para adaptar la imagen a cualquier tamaño de monitor sin deformar
        ancho_ventana, alto_ventana = ventana.get_size()
        escala = min(ancho_ventana / ancho_pantalla, alto_ventana / alto_pantalla)
        ancho_escalado = int(ancho_pantalla * escala)
        alto_escalado = int(alto_pantalla * escala)
        margen_x = (ancho_ventana - ancho_escalado) // 2
        margen_y = (alto_ventana - alto_escalado) // 2

        # Convertir la posicion del mouse a las coordenadas de la superficie de 800x880
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if escala > 0:
            pos_mouse = (int((mouse_x - margen_x) / escala), int((mouse_y - margen_y) / escala))
        else:
            pos_mouse = (-1, -1)

        # 1. GESTION DE EVENTOS (TECLADO, MOUSE Y CIERRE)
        for evento in pygame.event.get():
            # Si el usuario hace clic en la 'X' de cerrar la ventana
            if evento.type == pygame.QUIT:
                ejecutando = False

            # Si el usuario presiona una tecla
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    mover_jugador(-1, 0)
                elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    mover_jugador(1, 0)
                elif evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    mover_jugador(0, -1)
                elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    mover_jugador(0, 1)
                elif evento.key == pygame.K_r:
                    resolver_automatico()
                elif evento.key == pygame.K_c:
                    comparar_salidas()
                elif evento.key == pygame.K_SPACE:
                    reiniciar_laberinto()

            # Si el usuario hace clic con el boton izquierdo del mouse
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for rectangulo, texto_btn, funcion_accion in botones:
                    # Comprobamos si el clic ocurrio dentro del rectangulo del boton
                    if rectangulo.collidepoint(pos_mouse):
                        funcion_accion()

        # 2. ACTUALIZACION DE ANIMACION PASO A PASO
        if len(juego["cola_animacion"]) > 0:
            for _ in range(pasos_por_fotograma):
                if len(juego["cola_animacion"]) == 0:
                    break
                # Extraer la primera accion de la lista
                accion, fila_p, col_p = juego["cola_animacion"].pop(0)

                if accion == "marcar":
                    juego["tablero_visual"][fila_p][col_p] = "*"
                    juego["pasos"] += 1
                elif accion == "desmarcar":
                    juego["tablero_visual"][fila_p][col_p] = "."
                    if juego["pasos"] > 0:
                        juego["pasos"] -= 1
                elif accion == "meta":
                    juego["tablero_visual"][fila_p][col_p] = "S"
                    juego["pasos"] += 1

            # Si se terminaron todos los pasos de la animacion
            if len(juego["cola_animacion"]) == 0:
                juego["tablero_visual"][juego["fila_inicio"]][juego["columna_inicio"]] = "E"

                if juego["esperando_cartel"] == "resolucion":
                    pasos_totales = logica.contar_pasos_camino(juego["tablero_visual"])
                    juego["mostrar_cartel"] = True
                    juego["titulo_cartel"] = "¡LABERINTO RESUELTO!"
                    juego["linea_cartel_1"] = f"CAMINO ENCONTRADO EN {pasos_totales} PASOS"
                    juego["linea_cartel_2"] = "RESOLUCIÓN HECHA DE MANERA AUTOMÁTICA"
                    juego["mensaje"] = f"SALIDA ENCONTRADA EN {pasos_totales} PASOS"
                    juego["esperando_cartel"] = None

                elif juego["esperando_cartel"] == "comparacion":
                    juego["mostrar_cartel"] = True
                    juego["mensaje"] = "COMPARACIÓN FINALIZADA"
                    juego["esperando_cartel"] = None

        # 3. DIBUJAR EL LABERINTO EN LA SUPERFICIE
        superficie.fill(color_fondo)

        for fila in range(filas):
            for col in range(columnas):
                simbolo = juego["tablero_visual"][fila][col]
                centro_x = col * tamanio_celda + tamanio_celda // 2
                centro_y = fila * tamanio_celda + tamanio_celda // 2
                rect_celda = pygame.Rect(col * tamanio_celda, fila * tamanio_celda, tamanio_celda, tamanio_celda)

                if simbolo == "X":
                    # Pared: rectangulo azul oscuro con borde azul brillante
                    pygame.draw.rect(superficie, color_pared_relleno, rect_celda)
                    pygame.draw.rect(superficie, color_pared_borde, rect_celda, 1)
                elif simbolo == "E":
                    # Entrada: circulo verde con punto blanco en el centro
                    pygame.draw.circle(superficie, color_entrada, (centro_x, centro_y), 7, 2)
                    pygame.draw.circle(superficie, (255, 255, 255), (centro_x, centro_y), 2)
                elif simbolo == "S":
                    # Salida: circulo rosa con punto blanco en el centro
                    pygame.draw.circle(superficie, color_salida, (centro_x, centro_y), 7, 2)
                    pygame.draw.circle(superficie, (255, 255, 255), (centro_x, centro_y), 2)
                elif simbolo == "*":
                    # Camino recorrido / solucion: punto celeste
                    pygame.draw.circle(superficie, color_solucion, (centro_x, centro_y), 3)
                elif simbolo == "P":
                    # Personaje: circulo amarillo con punto de ojo negro
                    pygame.draw.circle(superficie, color_jugador, (centro_x, centro_y), 7)
                    pygame.draw.circle(superficie, (0, 0, 0), (centro_x + 2, centro_y - 2), 2)
                else:
                    # Pasillo libre: punto azul tenue
                    pygame.draw.circle(superficie, color_pasillo, (centro_x, centro_y), 1)

        # 4. DIBUJAR CARTEL MODAL INTERACTIVO
        if juego["mostrar_cartel"] == True:
            # Fondo semitransparente para el cartel
            rect_cartel = pygame.Rect(100, 310, 600, 180)
            superficie_cartel = pygame.Surface((600, 180))
            superficie_cartel.set_alpha(235)
            superficie_cartel.fill((10, 10, 35))
            superficie.blit(superficie_cartel, (100, 310))

            # Borde que alterna suavemente de color entre amarillo y celeste
            if (contador_fotogramas // 20) % 2 == 0:
                color_borde = (255, 255, 0)
            else:
                color_borde = (0, 255, 255)
            pygame.draw.rect(superficie, color_borde, rect_cartel, 4, border_radius=10)

            # Textos informativos dentro del cartel
            texto_tit = fuente_banner.render(juego["titulo_cartel"], True, (255, 255, 0))
            texto_l1 = fuente_subbanner.render(juego["linea_cartel_1"], True, (255, 255, 255))
            texto_l2 = fuente_subbanner.render(juego["linea_cartel_2"], True, (0, 255, 255))
            texto_l3 = fuente_hud.render("PRESIONA [ESPACIO] PARA REINICIAR", True, (0, 255, 140))

            # Centrar cada texto en el medio del cartel (X = 400)
            superficie.blit(texto_tit, texto_tit.get_rect(center=(400, 345)))
            superficie.blit(texto_l1, texto_l1.get_rect(center=(400, 385)))
            superficie.blit(texto_l2, texto_l2.get_rect(center=(400, 420)))
            superficie.blit(texto_l3, texto_l3.get_rect(center=(400, 458)))

        # 5. DIBUJAR PANEL INFERIOR (PASOS, ESTADO Y BOTONES)
        rect_marquesina = pygame.Rect(0, alto_tablero, ancho_pantalla, alto_panel_inferior)
        pygame.draw.rect(superficie, (10, 10, 25), rect_marquesina)
        pygame.draw.line(superficie, color_pared_borde, (0, alto_tablero), (ancho_pantalla, alto_tablero), 2)

        # Linea 1: Contador de pasos
        texto_pasos = fuente_hud.render(f"PASOS: {juego['pasos']:03d}", True, (200, 200, 200))
        superficie.blit(texto_pasos, (40, alto_tablero + 6))

        # Linea 2: Mensaje de estado actual
        if juego["mostrar_cartel"] == True:
            color_mensaje = (255, 255, 0)
        else:
            color_mensaje = (0, 255, 255)
        texto_msg = fuente_texto.render(juego["mensaje"], True, color_mensaje)
        superficie.blit(texto_msg, (40, alto_tablero + 22))

        # Dibujar los 3 botones
        for rectangulo, texto_btn, _ in botones:
            # Si el mouse esta encima del boton, se ilumina un poco mas
            if rectangulo.collidepoint(pos_mouse):
                color_btn = (40, 50, 160)
            else:
                color_btn = (20, 25, 70)

            pygame.draw.rect(superficie, color_btn, rectangulo, border_radius=4)
            pygame.draw.rect(superficie, (0, 255, 255), rectangulo, 1, border_radius=4)
            superficie_texto_btn = fuente_hud.render(texto_btn, True, (255, 255, 255))
            superficie.blit(superficie_texto_btn, superficie_texto_btn.get_rect(center=rectangulo.center))

        # 6. MOSTRAR EN LA VENTANA FISICA
        ventana.fill((0, 0, 0))
        superficie_escalada = pygame.transform.smoothscale(superficie, (ancho_escalado, alto_escalado))
        ventana.blit(superficie_escalada, (margen_x, margen_y))

        # Actualiza la pantalla para mostrar todos los cambios dibujados
        pygame.display.flip()

        # Limitar la velocidad del juego a 60 fotogramas por segundo
        reloj.tick(60)

    # Al salir del bucle, cerrar Pygame
    pygame.quit()

if __name__ == "__main__":
    iniciar()