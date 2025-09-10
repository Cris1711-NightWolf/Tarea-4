import pygame
import random
import sys
import math

# Inicialización de pygame
pygame.init()

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
MORADO = (128, 0, 128)
NARANJA = (255, 165, 0)
VERDE_OSCURO = (0, 100, 0)
GRIS = (40, 40, 40)
VERDE_NEO = (57, 255, 20)
AZUL_ELECTRICO = (0, 191, 255)
ROJO_ELECTRICO = (255, 20, 20)

# Configuración de la pantalla
ANCHO = 800
ALTO = 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("RETRO SNAKE - Arcade Edition")

# Reloj para controlar la velocidad del juego
reloj = pygame.time.Clock()

# Fuentes de texto retro
fuente_pequena = pygame.font.SysFont("courier", 20, bold=True)
fuente_mediana = pygame.font.SysFont("courier", 40, bold=True)
fuente_grande = pygame.font.SysFont("courier", 70, bold=True)

# Cargar imágenes o crear superficies para el fondo
def crear_fondo_retro():
    fondo = pygame.Surface((ANCHO, ALTO))
    fondo.fill(NEGRO)
    
    # Crear efecto de grid retro
    for x in range(0, ANCHO, 20):
        pygame.draw.line(fondo, (20, 20, 20), (x, 0), (x, ALTO), 1)
    for y in range(0, ALTO, 20):
        pygame.draw.line(fondo, (20, 20, 20), (0, y), (ANCHO, y), 1)
    
    # Añadir efecto de escaneo (scanlines)
    for y in range(0, ALTO, 3):
        if y % 2 == 0:
            pygame.draw.line(fondo, (0, 0, 0, 50), (0, y), (ANCHO, y), 1)
    
    return fondo

fondo = crear_fondo_retro()

# Crear obstáculos aleatorios según el nivel
def crear_obstaculos(nivel):
    obstaculos = []
    tamano_bloque = 20
    
    # Número de obstáculos según el nivel
    if nivel == 1:  # Fácil
        num_obstaculos = 5
    elif nivel == 2:  # Medio
        num_obstaculos = 10
    elif nivel == 3:  # Difícil
        num_obstaculos = 15
    
    # Generar obstáculos aleatorios
    for _ in range(num_obstaculos):
        # Asegurar que los obstáculos no estén demasiado cerca del centro
        while True:
            x = round(random.randrange(40, ANCHO - 60) / 20.0) * 20.0
            y = round(random.randrange(40, ALTO - 60) / 20.0) * 20.0
            
            # Evitar que los obstáculos estén demasiado cerca del centro (donde empieza la serpiente)
            if abs(x - ANCHO/2) > 100 or abs(y - ALTO/2) > 100:
                obstaculos.append([x, y])
                break
    
    return obstaculos

# Función para dibujar la serpiente con estilo realista
def dibujar_serpiente(bloques_serpiente, tamano_bloque, direccion):
    for i, bloque in enumerate(bloques_serpiente):
        # Cabeza de la serpiente
        if i == len(bloques_serpiente) - 1:
            # Dibujar cabeza con detalles
            pygame.draw.rect(ventana, VERDE_NEO, [bloque[0], bloque[1], tamano_bloque, tamano_bloque])
            pygame.draw.rect(ventana, VERDE_OSCURO, [bloque[0], bloque[1], tamano_bloque, tamano_bloque], 1)
            
            # Ojos de la serpiente (dependiendo de la dirección)
            if direccion == "DERECHA":
                pygame.draw.circle(ventana, NEGRO, (bloque[0] + tamano_bloque - 5, bloque[1] + 7), 4)
                pygame.draw.circle(ventana, NEGRO, (bloque[0] + tamano_bloque - 5, bloque[1] + tamano_bloque - 7), 4)
                pygame.draw.circle(ventana, BLANCO, (bloque[0] + tamano_bloque - 3, bloque[1] + 5), 1)
                pygame.draw.circle(ventana, BLANCO, (bloque[0] + tamano_bloque - 3, bloque[1] + tamano_bloque - 5), 1)
            elif direccion == "IZQUIERDA":
                pygame.draw.circle(ventana, NEGRO, (bloque[0] + 5, bloque[1] + 7), 4)
                pygame.draw.circle(ventana, NEGRO, (bloque[0] + 5, bloque[1] + tamano_bloque - 7), 4)
                pygame.draw.circle(ventana, BLANCO, (bloque[0] + 3, bloque[1] + 5), 1)
                pygame.draw.circle(ventana, BLANCO, (bloque[0] + 3, bloque[1] + tamano_bloque - 5), 1)
            elif direccion == "ARRIBA":
                pygame.draw.circle(ventana, NEGRO, (bloque[0] + 7, bloque[1] + 5), 4)
                pygame.draw.circle(ventana, NEGRO, (bloque[0] + tamano_bloque - 7, bloque[1] + 5), 4)
                pygame.draw.circle(ventana, BLANCO, (bloque[0] + 5, bloque[1] + 3), 1)
                pygame.draw.circle(ventana, BLANCO, (bloque[0] + tamano_bloque - 5, bloque[1] + 3), 1)
            elif direccion == "ABAJO":
                pygame.draw.circle(ventana, NEGRO, (bloque[0] + 7, bloque[1] + tamano_bloque - 5), 4)
                pygame.draw.circle(ventana, NEGRO, (bloque[0] + tamano_bloque - 7, bloque[1] + tamano_bloque - 5), 4)
                pygame.draw.circle(ventana, BLANCO, (bloque[0] + 5, bloque[1] + tamano_bloque - 3), 1)
                pygame.draw.circle(ventana, BLANCO, (bloque[0] + tamano_bloque - 5, bloque[1] + tamano_bloque - 3), 1)
        
        else:
            # Cuerpo de la serpiente con degradado
            intensidad = 200 - (len(bloques_serpiente) - i) * 3
            if intensidad < 50:
                intensidad = 50
            color_cuerpo = (0, intensidad, 0)
            
            pygame.draw.rect(ventana, color_cuerpo, [bloque[0], bloque[1], tamano_bloque, tamano_bloque])
            pygame.draw.rect(ventana, VERDE_OSCURO, [bloque[0], bloque[1], tamano_bloque, tamano_bloque], 1)
            
            # Añadir un patrón de escamas en el cuerpo
            if i % 2 == 0:
                pygame.draw.rect(ventana, (0, intensidad-20, 0), 
                                [bloque[0] + 4, bloque[1] + 4, tamano_bloque - 8, tamano_bloque - 8])

# Función para mostrar el mensaje de puntuación con estilo retro
def mostrar_puntuacion(puntuacion, nivel):
    texto = fuente_pequena.render(f"SCORE: {puntuacion}", True, VERDE_NEO)
    ventana.blit(texto, [20, 15])
    
    texto_nivel = fuente_pequena.render(f"LEVEL: {nivel}", True, AZUL_ELECTRICO)
    ventana.blit(texto_nivel, [ANCHO - 150, 15])

# Función para mostrar mensajes en pantalla con estilo retro
def mensaje_retro(msg, color, y_displace=0, tamanio="mediano", efecto_brillo=False):
    if tamanio == "pequeno":
        fuente = fuente_pequena
    elif tamanio == "mediano":
        fuente = fuente_mediana
    elif tamanio == "grande":
        fuente = fuente_grande
        
    texto = fuente.render(msg, True, color)
    texto_rect = texto.get_rect(center=(ANCHO/2, ALTO/2 + y_displace))
    
    # Efecto de brillo neón
    if efecto_brillo:
        texto_sombra = fuente.render(msg, True, (color[0]//3, color[1]//3, color[2]//3))
        ventana.blit(texto_sombra, (texto_rect.x + 2, texto_rect.y + 2))
        
        for i in range(3):
            texto_brillo = fuente.render(msg, True, (min(color[0] + 50, 255), min(color[1] + 50, 255), min(color[2] + 50, 255)))
            ventana.blit(texto_brillo, (texto_rect.x - i, texto_rect.y - i))
    
    ventana.blit(texto, texto_rect)

# Función para dibujar obstáculos
def dibujar_obstaculos(obstaculos, tamano_bloque):
    for obstaculo in obstaculos:
        pygame.draw.rect(ventana, MORADO, [obstaculo[0], obstaculo[1], tamano_bloque, tamano_bloque])
        pygame.draw.rect(ventana, (100, 0, 100), [obstaculo[0], obstaculo[1], tamano_bloque, tamano_bloque], 2)
        
        # Añadir efecto de neón a los obstáculos
        pygame.draw.rect(ventana, (180, 0, 180), [obstaculo[0] + 3, obstaculo[1] + 3, tamano_bloque - 6, tamano_bloque - 6], 1)

# Función para dibujar comida con estilo retro
def dibujar_comida(x, y, tamano_bloque):
    pygame.draw.rect(ventana, ROJO_ELECTRICO, [x, y, tamano_bloque, tamano_bloque])
    
    # Efecto de brillo
    pygame.draw.rect(ventana, (255, 100, 100), [x + 4, y + 4, tamano_bloque - 8, tamano_bloque - 8])
    pygame.draw.rect(ventana, (255, 200, 200), [x + 7, y + 7, tamano_bloque - 14, tamano_bloque - 14])

# Pantalla de inicio con estilo retro
def mostrar_menu_principal():
    seleccion = 0
    opciones = ["FÁCIL", "MEDIO", "DIFÍCIL", "SALIR"]
    
    while True:
        ventana.blit(fondo, (0, 0))
        
        # Título con efecto neón
        mensaje_retro("RETRO SNAKE", VERDE_NEO, -150, "grande", True)
        mensaje_retro("ARCADE EDITION", AZUL_ELECTRICO, -90, "mediano", True)
        
        # Dibujar opciones del menú
        for i, opcion in enumerate(opciones):
            color = VERDE_NEO if i == seleccion else BLANCO
            mensaje_retro(opcion, color, 20 + i * 60, "mediano")
        
        # Dibujar instrucciones
        mensaje_retro("Usa las flechas para navegar y ENTER para seleccionar", BLANCO, 250, "pequeno")
        
        pygame.display.update()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    if seleccion == 3:  # SALIR
                        pygame.quit()
                        sys.exit()
                    else:
                        return seleccion + 1  # Devuelve el nivel (1, 2 o 3)
        
        reloj.tick(10)

# Pantalla de Game Over con estilo retro
def mostrar_game_over(puntuacion, nivel):
    seleccion = 0
    opciones = ["REINTENTAR", "MENÚ PRINCIPAL", "SALIR"]
    
    while True:
        ventana.blit(fondo, (0, 0))
        
        # Título Game Over
        mensaje_retro("GAME OVER", ROJO_ELECTRICO, -150, "grande", True)
        
        # Mostrar puntuación
        mensaje_retro(f"PUNTUACIÓN: {puntuacion}", AZUL_ELECTRICO, -80, "mediano")
        mensaje_retro(f"NIVEL: {nivel}", VERDE_NEO, -30, "mediano")
        
        # Dibujar opciones
        for i, opcion in enumerate(opciones):
            color = VERDE_NEO if i == seleccion else BLANCO
            mensaje_retro(opcion, color, 50 + i * 60, "mediano")
        
        pygame.display.update()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    if seleccion == 0:  # REINTENTAR
                        return "reintentar"
                    elif seleccion == 1:  # MENÚ PRINCIPAL
                        return "menu"
                    elif seleccion == 2:  # SALIR
                        pygame.quit()
                        sys.exit()
        
        reloj.tick(10)

# Función principal del juego
def juego():
    game_over = False
    game_cerrado = False
    
    # Configuración inicial
    tamano_bloque = 20
    velocidad = 12
    
    # Seleccionar nivel desde el menú
    nivel = mostrar_menu_principal()
    
    # Ajustar velocidad según el nivel
    if nivel == 1:  # Fácil
        velocidad = 10
    elif nivel == 2:  # Medio
        velocidad = 13
    elif nivel == 3:  # Difícil
        velocidad = 16
    
    # Generar obstáculos aleatorios según el nivel
    obstaculos = crear_obstaculos(nivel)
    
    # Posición inicial de la serpiente
    cabeza_x = ANCHO / 2
    cabeza_y = ALTO / 2
    
    cambio_x = tamano_bloque
    cambio_y = 0
    direccion = "DERECHA"
    
    # Inicializar serpiente
    bloques_serpiente = []
    longitud_serpiente = 3
    
    # Inicializar la serpiente con algunos segmentos
    for i in range(longitud_serpiente):
        bloques_serpiente.append([cabeza_x - i * tamano_bloque, cabeza_y])
    
    # Posición inicial de la comida (asegurarse de que no esté en los obstáculos)
    while True:
        comida_x = round(random.randrange(0, ANCHO - tamano_bloque) / 20.0) * 20.0
        comida_y = round(random.randrange(0, ALTO - tamano_bloque) / 20.0) * 20.0
        
        # Verificar que la comida no esté en los obstáculos
        comida_valida = True
        for obstaculo in obstaculos:
            if comida_x == obstaculo[0] and comida_y == obstaculo[1]:
                comida_valida = False
                break
                
        if comida_valida:
            break
    
    # Puntuación
    puntuacion = 0
    
    while not game_over:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                game_over = True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and cambio_x == 0:
                    cambio_x = -tamano_bloque
                    cambio_y = 0
                    direccion = "IZQUIERDA"
                elif evento.key == pygame.K_RIGHT and cambio_x == 0:
                    cambio_x = tamano_bloque
                    cambio_y = 0
                    direccion = "DERECHA"
                elif evento.key == pygame.K_UP and cambio_y == 0:
                    cambio_y = -tamano_bloque
                    cambio_x = 0
                    direccion = "ARRIBA"
                elif evento.key == pygame.K_DOWN and cambio_y == 0:
                    cambio_y = tamano_bloque
                    cambio_x = 0
                    direccion = "ABAJO"
        
        # Verificar si la serpiente choca con los bordes
        if cabeza_x >= ANCHO or cabeza_x < 0 or cabeza_y >= ALTO or cabeza_y < 0:
            accion = mostrar_game_over(puntuacion, nivel)
            if accion == "reintentar":
                juego()
            elif accion == "menu":
                return
            else:
                game_over = True
        
        # Actualizar posición de la cabeza
        cabeza_x += cambio_x
        cabeza_y += cambio_y
        
        # Dibujar fondo
        ventana.blit(fondo, (0, 0))
        
        # Dibujar comida
        dibujar_comida(comida_x, comida_y, tamano_bloque)
        
        # Dibujar obstáculos
        dibujar_obstaculos(obstaculos, tamano_bloque)
        
        # Actualizar serpiente
        cabeza_serpiente = []
        cabeza_serpiente.append(cabeza_x)
        cabeza_serpiente.append(cabeza_y)
        bloques_serpiente.append(cabeza_serpiente)
        
        if len(bloques_serpiente) > longitud_serpiente:
            del bloques_serpiente[0]
        
        # Verificar si la serpiente choca consigo misma
        for bloque in bloques_serpiente[:-1]:
            if bloque[0] == cabeza_serpiente[0] and bloque[1] == cabeza_serpiente[1]:
                accion = mostrar_game_over(puntuacion, nivel)
                if accion == "reintentar":
                    juego()
                elif accion == "menu":
                    return
                else:
                    game_over = True
        
        # Verificar si la serpiente choca con los obstáculos
        for obstaculo in obstaculos:
            if cabeza_serpiente[0] == obstaculo[0] and cabeza_serpiente[1] == obstaculo[1]:
                accion = mostrar_game_over(puntuacion, nivel)
                if accion == "reintentar":
                    juego()
                elif accion == "menu":
                    return
                else:
                    game_over = True
        
        # Dibujar serpiente
        dibujar_serpiente(bloques_serpiente, tamano_bloque, direccion)
        
        # Mostrar puntuación
        mostrar_puntuacion(puntuacion, nivel)
        
        pygame.display.update()
        
        # Verificar si la serpiente come la comida
        if cabeza_x == comida_x and cabeza_y == comida_y:
            # Generar nueva comida que no esté en los obstáculos
            while True:
                comida_x = round(random.randrange(0, ANCHO - tamano_bloque) / 20.0) * 20.0
                comida_y = round(random.randrange(0, ALTO - tamano_bloque) / 20.0) * 20.0
                
                # Verificar que la comida no esté en los obstáculos
                comida_valida = True
                for obstaculo in obstaculos:
                    if comida_x == obstaculo[0] and comida_y == obstaculo[1]:
                        comida_valida = False
                        break
                
                if comida_valida:
                    break
            
            longitud_serpiente += 1
            puntuacion += 10 * nivel  # Más puntos en niveles más difíciles
        
        reloj.tick(velocidad)
    
    pygame.quit()
    sys.exit()

# Iniciar el juego
juego()
