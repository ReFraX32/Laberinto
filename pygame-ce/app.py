"""
MODULO: Interfaz Grafica con Pygame-CE - Estilo Videojuego Arcade 8-Bit
Provee una experiencia de videojuego retro estilo Pac-Man / Dungeon Crawler
con laberintos de neon, animacion paso a paso de recursion y finalizacion formal al ganar.
Adaptado para resolución dinámica y pantallas pequeñas conservando aspect ratio.
"""

import sys
import os
import math
import pygame

# Agregar la carpeta principal para poder importar la logica de laberinto.py
carpeta_actual = os.path.dirname(os.path.abspath(__file__))
carpeta_padre = os.path.dirname(carpeta_actual)
if carpeta_padre not in sys.path:
    sys.path.append(carpeta_padre)

import laberinto

# Dimensiones internas fijas del lienzo virtual arcade
tamanio_celda = 20
columnas = 40
filas = 40
ancho_pantalla = columnas * tamanio_celda  # 800 px
alto_tablero = filas * tamanio_celda      # 800 px
alto_marquesina = 70
alto_pantalla = alto_tablero + alto_marquesina  # 870 px

# Paleta de colores arcade (Estilo Pac-Man / 80s Neon)
color_fondo_arcade = (0, 0, 0)
color_pared_exterior = (25, 25, 166)
color_pared_interior = (5, 5, 58)
color_pasillo = (0, 0, 0)
color_pellet = (255, 184, 151)
color_jugador_arcade = (255, 255, 0)
color_portal_salida = (255, 0, 85)
color_portal_entrada = (0, 255, 136)
color_laser_solucion = (0, 255, 255)

# Variables de estado del juego
laberinto_base = []
laberinto_visual = []
fila_jugador = 0
columna_jugador = 0
fila_inicio = 0
columna_inicio = 0
pasos_dados = 0
puntos_arcade = 0
mensaje_arcade = "USA FLECHAS O WASD PARA JUGAR"
tiempo_animacion = 0
victoria_arcade = False
juego_terminado = False
cola_animacion = []
pasos_por_fotograma = 3


def nuevo_laberinto():
    global laberinto_base, laberinto_visual, fila_inicio, columna_inicio
    global fila_jugador, columna_jugador, pasos_dados, puntos_arcade, mensaje_arcade
    global victoria_arcade, juego_terminado, cola_animacion

    laberinto_base = laberinto.generar_laberinto_aleatorio()
    fila_inicio, columna_inicio = laberinto.buscar_posicion(laberinto_base, "E")
    laberinto_visual = laberinto.copiar_laberinto(laberinto_base)
    fila_jugador = fila_inicio
    columna_jugador = columna_inicio
    pasos_dados = 0
    puntos_arcade = 0
    victoria_arcade = False
    juego_terminado = False
    cola_animacion = []
    laberinto_visual[fila_jugador][columna_jugador] = "P"
    mensaje_arcade = f"NIVEL INICIADO EN ({fila_inicio}, {columna_inicio})"


def reiniciar_jugador():
    global fila_jugador, columna_jugador, pasos_dados, laberinto_visual
    global mensaje_arcade, victoria_arcade, juego_terminado, cola_animacion

    laberinto_visual = laberinto.copiar_laberinto(laberinto_base)
    fila_jugador = fila_inicio
    columna_jugador = columna_inicio
    pasos_dados = 0
    victoria_arcade = False
    juego_terminado = False
    cola_animacion = []
    laberinto_visual[fila_jugador][columna_jugador] = "P"
    mensaje_arcade = "REINICIO: HEROE EN CASILLA INICIAL"


def mover_jugador(desplazamiento_fila, desplazamiento_columna):
    global fila_jugador, columna_jugador, pasos_dados, puntos_arcade
    global mensaje_arcade, victoria_arcade, juego_terminado

    if juego_terminado or len(cola_animacion) > 0:
        return

    nueva_fila = fila_jugador + desplazamiento_fila
    nueva_columna = columna_jugador + desplazamiento_columna

    if nueva_fila < 0 or nueva_fila >= filas or nueva_columna < 0 or nueva_columna >= columnas:
        mensaje_arcade = "** BORDE DEL MAPA **"
        return

    destino = laberinto_base[nueva_fila][nueva_columna]
    if destino == "X":
        mensaje_arcade = "** PARED BLOQUEANTE **"
        return

    if fila_jugador == fila_inicio and columna_jugador == columna_inicio:
        laberinto_visual[fila_jugador][columna_jugador] = "E"
    else:
        laberinto_visual[fila_jugador][columna_jugador] = "."

    if destino == "S":
        pasos_dados += 1
        puntos_arcade += 500
        fila_jugador = nueva_fila
        columna_jugador = nueva_columna
        laberinto_visual[fila_jugador][columna_jugador] = "P"
        victoria_arcade = True
        juego_terminado = True
        mensaje_arcade = f"★ STAGE CLEAR! SALIDA EN {pasos_dados} PASOS! (+500 PTS) ★"
        return

    fila_jugador = nueva_fila
    columna_jugador = nueva_columna
    pasos_dados += 1
    puntos_arcade += 10
    laberinto_visual[fila_jugador][columna_jugador] = "P"
    mensaje_arcade = f"POS: ({fila_jugador}, {columna_jugador}) | PASOS: {pasos_dados:03d} | SCORE: {puntos_arcade:05d}"


def resolver_automatico():
    global laberinto_visual, cola_animacion, juego_terminado, victoria_arcade, mensaje_arcade

    victoria_arcade = False
    juego_terminado = True
    laberinto_visual = laberinto.copiar_laberinto(laberinto_base)

    historial = laberinto.obtener_pasos_resolucion(laberinto_base, fila_inicio, columna_inicio)
    if historial:
        cola_animacion = historial
        mensaje_arcade = f"ANIMANDO BACKTRACKING: {len(historial)} PASOS TOTALES..."
    else:
        mensaje_arcade = "ERROR: LABERINTO SIN SALIDA"


def comparar_salidas():
    global laberinto_visual, cola_animacion, juego_terminado, victoria_arcade, mensaje_arcade

    historial, salida_ganadora, p1, p2, texto_resumen = laberinto.obtener_pasos_comparacion(
        laberinto_base, fila_inicio, columna_inicio
    )
    if not historial:
        mensaje_arcade = "ERROR: FALTAN SALIDAS"
        return

    mensaje_arcade = texto_resumen
    victoria_arcade = False
    juego_terminado = True
    laberinto_visual = laberinto.copiar_laberinto(laberinto_base)
    cola_animacion = historial


def iniciar():
    global tiempo_animacion, laberinto_visual, mensaje_arcade
    pygame.init()

    # Detectar el tamaño del monitor para ajustar la ventana inicial en pantallas pequeñas
    info_monitor = pygame.display.Info()
    ancho_disponible = info_monitor.current_w
    alto_disponible = info_monitor.current_h - 90  # Margen para barra de tareas del OS

    factor_escala_inicial = min(1.0, ancho_disponible / ancho_pantalla, alto_disponible / alto_pantalla)
    ventana_w = int(ancho_pantalla * factor_escala_inicial)
    ventana_h = int(alto_pantalla * factor_escala_inicial)

    # Ventana redimensionable
    ventana = pygame.display.set_mode((ventana_w, ventana_h), pygame.RESIZABLE)
    pygame.display.set_caption("PAC-MAZE 40x40 // Pygame-CE Arcade Edition")

    # Superficie virtual donde se renderiza todo a escala original
    lienzo_virtual = pygame.Surface((ancho_pantalla, alto_pantalla))

    reloj = pygame.time.Clock()
    fuente_pixel = pygame.font.SysFont("Courier New", 14, bold=True)
    fuente_hud = pygame.font.SysFont("Courier New", 13, bold=True)
    fuente_banner = pygame.font.SysFont("Courier New", 28, bold=True)
    fuente_subbanner = pygame.font.SysFont("Courier New", 16, bold=True)

    botones = [
        (pygame.Rect(10, alto_tablero + 35, 140, 26), "[G] NUEVO NIVEL", nuevo_laberinto),
        (pygame.Rect(160, alto_tablero + 35, 140, 26), "[R] RESOLVER", resolver_automatico),
        (pygame.Rect(310, alto_tablero + 35, 170, 26), "[C] COMPARAR METAS", comparar_salidas),
        (pygame.Rect(490, alto_tablero + 35, 140, 26), "[ESPACIO] REINICIAR", reiniciar_jugador),
    ]

    nuevo_laberinto()
    ejecutando = True

    while ejecutando:
        tiempo_animacion += 1

        # Calculo dinamico de dimensiones y letterboxing en cada frame
        ancho_actual, alto_actual = ventana.get_size()
        escala_x = ancho_actual / ancho_pantalla
        escala_y = alto_actual / alto_pantalla
        escala = min(escala_x, escala_y)

        nuevo_w = int(ancho_pantalla * escala)
        nuevo_h = int(alto_pantalla * escala)
        offset_x = (ancho_actual - nuevo_w) // 2
        offset_y = (alto_actual - nuevo_h) // 2

        # Conversion de coordenadas del raton de la ventana fisica al lienzo virtual
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if escala > 0:
            pos_mouse_virtual = (
                int((mouse_x - offset_x) / escala),
                int((mouse_y - offset_y) / escala)
            )
        else:
            pos_mouse_virtual = (-1, -1)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_UP, pygame.K_w):
                    mover_jugador(-1, 0)
                elif evento.key in (pygame.K_DOWN, pygame.K_s):
                    mover_jugador(1, 0)
                elif evento.key in (pygame.K_LEFT, pygame.K_a):
                    mover_jugador(0, -1)
                elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                    mover_jugador(0, 1)
                elif evento.key == pygame.K_g:
                    nuevo_laberinto()
                elif evento.key == pygame.K_r:
                    resolver_automatico()
                elif evento.key == pygame.K_c:
                    comparar_salidas()
                elif evento.key == pygame.K_SPACE:
                    reiniciar_jugador()

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for rect, _, accion in botones:
                    if rect.collidepoint(pos_mouse_virtual):
                        accion()

        if cola_animacion:
            for _ in range(pasos_por_fotograma):
                if not cola_animacion:
                    break
                accion_paso, f_paso, c_paso = cola_animacion.pop(0)
                if accion_paso in ("marcar", "marcar_optimo"):
                    laberinto_visual[f_paso][c_paso] = "*"
                elif accion_paso == "desmarcar":
                    laberinto_visual[f_paso][c_paso] = "."
                elif accion_paso in ("meta", "meta_final"):
                    laberinto_visual[f_paso][c_paso] = "S"
                elif accion_paso == "limpiar_tablero":
                    laberinto_visual = laberinto.copiar_laberinto(laberinto_base)

            if not cola_animacion:
                laberinto_visual[fila_inicio][columna_inicio] = "E"

        # Dibujar elementos del juego sobre el lienzo virtual
        lienzo_virtual.fill(color_fondo_arcade)
        pulso = int(math.sin(tiempo_animacion * 0.1) * 3)

        for fila in range(filas):
            for columna in range(columnas):
                simbolo = laberinto_visual[fila][columna]
                centro_x = columna * tamanio_celda + tamanio_celda // 2
                centro_y = fila * tamanio_celda + tamanio_celda // 2
                rect_celda = pygame.Rect(columna * tamanio_celda, fila * tamanio_celda, tamanio_celda, tamanio_celda)

                if simbolo == "X":
                    pygame.draw.rect(lienzo_virtual, color_pared_interior, rect_celda)
                    pygame.draw.rect(lienzo_virtual, color_pared_exterior, rect_celda, 1)

                elif simbolo == "E":
                    radio = 7 + pulso
                    pygame.draw.circle(lienzo_virtual, color_portal_entrada, (centro_x, centro_y), max(3, radio), 2)
                    pygame.draw.circle(lienzo_virtual, (255, 255, 255), (centro_x, centro_y), 3)

                elif simbolo == "S":
                    radio = 7 - pulso
                    pygame.draw.circle(lienzo_virtual, color_portal_salida, (centro_x, centro_y), max(3, radio), 2)
                    pygame.draw.circle(lienzo_virtual, (255, 255, 255), (centro_x, centro_y), 3)

                elif simbolo == "*":
                    pygame.draw.circle(lienzo_virtual, color_laser_solucion, (centro_x, centro_y), 4)

                elif simbolo == "P":
                    radio_heroe = 8
                    pygame.draw.circle(lienzo_virtual, color_jugador_arcade, (centro_x, centro_y), radio_heroe)
                    pygame.draw.circle(lienzo_virtual, (0, 0, 0), (centro_x + 2, centro_y - 3), 2)

                else:
                    pygame.draw.circle(lienzo_virtual, (30, 30, 60), (centro_x, centro_y), 1)

        if victoria_arcade:
            rect_banner = pygame.Rect(150, 320, 500, 160)
            superficie_banner = pygame.Surface((500, 160))
            superficie_banner.set_alpha(230)
            superficie_banner.fill((10, 10, 30))
            lienzo_virtual.blit(superficie_banner, (150, 320))

            color_borde = (255, 255, 0) if (tiempo_animacion // 15) % 2 == 0 else (0, 255, 255)
            pygame.draw.rect(lienzo_virtual, color_borde, rect_banner, 4, border_radius=8)

            txt_vic = fuente_banner.render("★ STAGE CLEAR! ★", True, (255, 255, 0))
            rect_txt_vic = txt_vic.get_rect(center=(400, 360))
            lienzo_virtual.blit(txt_vic, rect_txt_vic)

            txt_info = fuente_subbanner.render(f"PUNTAJE: {puntos_arcade} PTS | PASOS: {pasos_dados}", True, (255, 255, 255))
            rect_txt_info = txt_info.get_rect(center=(400, 400))
            lienzo_virtual.blit(txt_info, rect_txt_info)

            txt_sub = fuente_hud.render("PRESIONA [G] PARA JUGAR OTRO NIVEL", True, (0, 255, 136))
            rect_txt_sub = txt_sub.get_rect(center=(400, 440))
            lienzo_virtual.blit(txt_sub, rect_txt_sub)

        # Marquesina inferior
        rect_marquesina = pygame.Rect(0, alto_tablero, ancho_pantalla, alto_marquesina)
        pygame.draw.rect(lienzo_virtual, (10, 10, 20), rect_marquesina)
        pygame.draw.line(lienzo_virtual, color_pared_exterior, (0, alto_tablero), (ancho_pantalla, alto_tablero), 2)

        texto_1up = f"1UP: {puntos_arcade:05d}   HIGH: 99990   PASOS: {pasos_dados:03d}"
        superficie_hud = fuente_hud.render(texto_1up, True, (255, 255, 255))
        lienzo_virtual.blit(superficie_hud, (10, alto_tablero + 6))

        color_status = (255, 255, 0) if victoria_arcade else (0, 255, 255)
        superficie_msg = fuente_pixel.render(mensaje_arcade, True, color_status)
        lienzo_virtual.blit(superficie_msg, (10, alto_tablero + 20))

        for rect, texto, _ in botones:
            color_btn = (25, 25, 166) if rect.collidepoint(pos_mouse_virtual) else (15, 15, 60)
            pygame.draw.rect(lienzo_virtual, color_btn, rect, border_radius=3)
            pygame.draw.rect(lienzo_virtual, (0, 255, 255), rect, 1, border_radius=3)
            superficie_btn = fuente_hud.render(texto, True, (255, 255, 255))
            txt_rect = superficie_btn.get_rect(center=rect.center)
            lienzo_virtual.blit(superficie_btn, txt_rect)

        # Proyectar el lienzo virtual escalado a la ventana real
        ventana.fill((0, 0, 0))
        lienzo_escalado = pygame.transform.smoothscale(lienzo_virtual, (nuevo_w, nuevo_h))
        ventana.blit(lienzo_escalado, (offset_x, offset_y))

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()


if __name__ == "__main__":
    iniciar()