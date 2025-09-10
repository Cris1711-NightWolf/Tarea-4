import pygame
import random
import math
import os
import json
from pygame import mixer

# Inicialización
pygame.init()
mixer.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Defender Retro")
clock = pygame.time.Clock()

# Cargar o inicializar puntuaciones
def cargar_puntuaciones():
    if os.path.exists("puntuaciones.json"):
        with open("puntuaciones.json", "r") as f:
            return json.load(f)
    return []

def guardar_puntuaciones(puntuaciones):
    with open("puntuaciones.json", "w") as f:
        json.dump(puntuaciones, f)

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 120, 255)
AMARILLO = (255, 255, 0)
MORADO = (128, 0, 128)
NARANJA = (255, 165, 0)
CIAN = (0, 255, 255)
ROSA = (255, 0, 255)
VERDE_NEON = (57, 255, 20)

# Variables del juego
player_size = 50
player_x = 400
player_y = 500
player_speed = 5
player_lives = 3
score = 0
level = 1
game_over = False
game_paused = False
player_name = ""
entering_name = True
high_scores = cargar_puntuaciones()

# Balas
bullets = []
bullet_speed = 7

# Enemigos
enemies = []
enemy_size = 40
enemy_speed = 2
enemy_spawn_rate = 30

# Obstáculos
obstacles = []
obstacle_size = 35
obstacle_speed = 3
obstacle_spawn_rate = 50

# Estrellas de fondo
stars = []
for i in range(100):
    x = random.randint(0, 800)
    y = random.randint(0, 600)
    size = random.randint(1, 3)
    brightness = random.randint(150, 255)
    speed = random.uniform(0.2, 1.0)
    stars.append([x, y, size, brightness, speed])

# Fuentes
try:
    font_small = pygame.font.Font("fonte/retro_font.ttf", 20)
    font_medium = pygame.font.Font("fonte/retro_font.ttf", 30)
    font_large = pygame.font.Font("fonte/retro_font.ttf", 48)
    font_xl = pygame.font.Font("fonte/retro_font.ttf", 64)
except:
    font_small = pygame.font.SysFont("courier", 20, bold=True)
    font_medium = pygame.font.SysFont("courier", 30, bold=True)
    font_large = pygame.font.SysFont("courier", 48, bold=True)
    font_xl = pygame.font.SysFont("courier", 64, bold=True)

# Efectos de sonido
try:
    shoot_sound = mixer.Sound("sonidos/disparo.wav")
    explosion_sound = mixer.Sound("sonidos/explosion.wav")
    game_over_sound = mixer.Sound("sonidos/game_over.wav")
    mixer.music.load("sonidos/musica_fondo.mp3")
    mixer.music.set_volume(0.5)
    mixer.music.play(-1)
except:
    print("No se pudieron cargar los sonidos")

# Función para dibujar texto con efecto retro
def draw_text(text, font, color, x, y, centered=False):
    text_surface = font.render(text, True, color)
    if centered:
        x -= text_surface.get_width() // 2
    screen.blit(text_surface, (x, y))

# Función para dibujar borde retro
def draw_retro_border():
    pygame.draw.rect(screen, VERDE_NEON, (0, 0, 800, 600), 10)
    for i in range(0, 800, 20):
        pygame.draw.rect(screen, VERDE_NEON, (i, 0, 10, 5))
        pygame.draw.rect(screen, VERDE_NEON, (i, 595, 10, 5))
    for i in range(0, 600, 20):
        pygame.draw.rect(screen, VERDE_NEON, (0, i, 5, 10))
        pygame.draw.rect(screen, VERDE_NEON, (795, i, 5, 10))

# Función para dibujar jugador (nave espacial retro)
def draw_player(x, y):
    # Cuerpo principal de la nave
    pygame.draw.polygon(screen, AZUL, [
        (x + player_size//2, y),
        (x + player_size, y + player_size),
        (x + player_size//2, y + player_size - 10),
        (x, y + player_size)
    ])
    
    # Detalles retro
    pygame.draw.rect(screen, CIAN, (x + 10, y + 15, 30, 5))
    pygame.draw.rect(screen, CIAN, (x + 15, y + 25, 20, 10))
    
    # Propulsores
    pygame.draw.polygon(screen, NARANJA, [
        (x + player_size//2 - 5, y + player_size),
        (x + player_size//2 - 15, y + player_size + 10),
        (x + player_size//2 + 5, y + player_size),
        (x + player_size//2 + 15, y + player_size + 10)
    ])

# Función para dibujar enemigos (naves enemigas retro)
def draw_enemy(x, y):
    # Cuerpo del enemigo
    pygame.draw.rect(screen, ROJO, (x, y, enemy_size, enemy_size))
    
    # Detalles retro
    pygame.draw.rect(screen, AMARILLO, (x + 5, y + 5, 10, 10))
    pygame.draw.rect(screen, AMARILLO, (x + 25, y + 5, 10, 10))
    pygame.draw.rect(screen, NARANJA, (x + 10, y + 25, 20, 10))

# Función para dibujar obstáculos (asteroides retro)
def draw_obstacle(x, y):
    # Cuerpo del asteroide
    pygame.draw.circle(screen, (100, 100, 100), (x + obstacle_size//2, y + obstacle_size//2), obstacle_size//2)
    
    # Cráteres
    pygame.draw.circle(screen, (70, 70, 70), (x + 10, y + 10), 5)
    pygame.draw.circle(screen, (70, 70, 70), (x + 25, y + 15), 3)
    pygame.draw.circle(screen, (70, 70, 70), (x + 15, y + 25), 4)

# Función para dibujar balas
def draw_bullet(x, y):
    pygame.draw.rect(screen, AMARILLO, (x, y, 5, 10))
    pygame.draw.rect(screen, NARANJA, (x, y, 5, 4))

# Función para dibujar fondo retro
def draw_retro_background():
    # Fondo espacial retro
    screen.fill(NEGRO)
    
    # Dibujar estrellas
    for star in stars:
        pygame.draw.circle(screen, (star[3], star[3], star[3]), (star[0], star[1]), star[2])
        # Mover estrellas
        star[1] += star[4]
        if star[1] > 600:
            star[1] = 0
            star[0] = random.randint(0, 800)

# Función para mostrar información en pantalla
def draw_hud():
    # Puntuación
    draw_text(f"PUNTUACION: {score}", font_small, VERDE_NEON, 10, 10)
    
    # Nivel
    draw_text(f"NIVEL: {level}", font_small, VERDE_NEON, 10, 40)
    
    # Vidas
    draw_text(f"VIDAS: {player_lives}", font_small, VERDE_NEON, 10, 70)
    
    # Jugador
    draw_text(f"JUGADOR: {player_name}", font_small, VERDE_NEON, 600, 10)

# Función para mostrar pantalla de entrada de nombre
def show_name_input_screen():
    global player_name, entering_name
    
    draw_retro_background()
    draw_retro_border()
    
    draw_text("SPACE DEFENDER RETRO", font_xl, VERDE_NEON, 400, 100, True)
    draw_text("INGRESA TU NOMBRE:", font_medium, BLANCO, 400, 200, True)
    
    # Dibujar cuadro de texto
    pygame.draw.rect(screen, VERDE_NEON, (250, 250, 300, 40), 2)
    draw_text(player_name + ("_" if pygame.time.get_ticks() % 1000 < 500 else ""), font_medium, VERDE_NEON, 400, 255, True)
    
    draw_text("PRESIONA ENTER PARA CONTINUAR", font_small, BLANCO, 400, 320, True)
    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and player_name:
                entering_name = False
                return True
            elif event.key == pygame.K_BACKSPACE:
                player_name = player_name[:-1]
            elif event.key == pygame.K_ESCAPE:
                return False
            elif len(player_name) < 12:
                if event.unicode.isalnum() or event.unicode == " ":
                    player_name += event.unicode
    
    return True

# Función para mostrar pantalla de inicio
def show_start_screen():
    draw_retro_background()
    draw_retro_border()
    
    draw_text("SPACE DEFENDER RETRO", font_xl, VERDE_NEON, 400, 100, True)
    draw_text("SELECCIONA DIFICULTAD", font_medium, BLANCO, 400, 180, True)
    
    draw_text("1 - FACIL", font_medium, VERDE, 400, 240, True)
    draw_text("2 - INTERMEDIO", font_medium, AMARILLO, 400, 290, True)
    draw_text("3 - DIFICIL", font_medium, ROJO, 400, 340, True)
    
    draw_text("MEJORES PUNTUACIONES:", font_small, CIAN, 400, 400, True)
    
    # Mostrar mejores puntuaciones
    for i, score_data in enumerate(high_scores[:5]):
        draw_text(f"{i+1}. {score_data['name']} - {score_data['score']}", font_small, BLANCO, 400, 430 + i*30, True)
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, ""
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return True, "easy"
                elif event.key == pygame.K_2:
                    return True, "medium"
                elif event.key == pygame.K_3:
                    return True, "hard"
                elif event.key == pygame.K_ESCAPE:
                    return False, ""
        clock.tick(60)
    
    return True, ""

# Función para configurar la dificultad
def setup_difficulty(difficulty):
    global enemy_speed, enemy_spawn_rate, obstacle_speed, obstacle_spawn_rate, player_lives
    
    if difficulty == "easy":
        enemy_speed = 2
        enemy_spawn_rate = 30
        obstacle_speed = 2
        obstacle_spawn_rate = 60
        player_lives = 5
    elif difficulty == "medium":
        enemy_speed = 3
        enemy_spawn_rate = 20
        obstacle_speed = 3
        obstacle_spawn_rate = 40
        player_lives = 3
    elif difficulty == "hard":
        enemy_speed = 4
        enemy_spawn_rate = 15
        obstacle_speed = 4
        obstacle_spawn_rate = 30
        player_lives = 2

# Función para mostrar game over
def show_game_over_screen():
    global high_scores, game_over
    
    # Agregar puntuación actual a las mejores puntuaciones
    high_scores.append({"name": player_name, "score": score})
    high_scores.sort(key=lambda x: x["score"], reverse=True)
    high_scores = high_scores[:7]  # Mantener solo las 7 mejores
    guardar_puntuaciones(high_scores)
    
    draw_retro_background()
    draw_retro_border()
    
    draw_text("GAME OVER", font_xl, ROJO, 400, 100, True)
    draw_text(f"PUNTUACION FINAL: {score}", font_medium, AMARILLO, 400, 180, True)
    
    draw_text("MEJORES PUNTUACIONES:", font_small, CIAN, 400, 230, True)
    
    # Mostrar mejores puntuaciones
    for i, score_data in enumerate(high_scores[:5]):
        color = VERDE_NEON if score_data["name"] == player_name and score_data["score"] == score else BLANCO
        draw_text(f"{i+1}. {score_data['name']} - {score_data['score']}", font_small, color, 400, 260 + i*30, True)
    
    draw_text("R - REINICIAR NIVEL", font_small, VERDE, 400, 430, True)
    draw_text("M - MENU PRINCIPAL", font_small, AMARILLO, 400, 460, True)
    draw_text("Q - SALIR", font_small, ROJO, 400, 490, True)
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True, "restart"
                elif event.key == pygame.K_m:
                    game_over = False  # CORRECCIÓN: Reiniciar el estado del juego
                    return True, "menu"
                elif event.key == pygame.K_q:
                    return False, "quit"
        clock.tick(60)
    
    return True, ""

# Función para reiniciar el juego
def reset_game(difficulty):
    global player_x, player_y, bullets, enemies, obstacles, score, level, game_over, player_lives
    player_x = 400
    player_y = 500
    bullets = []
    enemies = []
    obstacles = []
    score = 0
    level = 1
    game_over = False  # CORRECCIÓN: Asegurarse de que game_over sea False
    setup_difficulty(difficulty)

# Función para mostrar pantalla de pausa
def show_pause_screen():
    overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    draw_text("PAUSA", font_large, VERDE_NEON, 400, 250, True)
    draw_text("PRESIONA P PARA CONTINUAR", font_small, BLANCO, 400, 320, True)
    
    pygame.display.update()

# Función para actualizar el nivel según la puntuación
def update_level():
    global level, enemy_speed, enemy_spawn_rate, obstacle_speed, obstacle_spawn_rate
    
    if score >= 500 and level < 2:
        level = 2
        enemy_speed += 1
        enemy_spawn_rate = max(10, enemy_spawn_rate - 5)
        obstacle_speed += 1
        obstacle_spawn_rate = max(20, obstacle_spawn_rate - 10)
    elif score >= 1000 and level < 3:
        level = 3
        enemy_speed += 1
        enemy_spawn_rate = max(5, enemy_spawn_rate - 5)
        obstacle_speed += 1
        obstacle_spawn_rate = max(10, obstacle_spawn_rate - 10)

# Bucle principal
running = True
current_difficulty = "medium"

# Pantalla de entrada de nombre
while entering_name and running:
    running = show_name_input_screen()
    clock.tick(60)

# Pantalla de inicio
if running:
    running, current_difficulty = show_start_screen()
    if running:
        setup_difficulty(current_difficulty)

# Bucle del juego
while running:
    draw_retro_background()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over and not game_paused:
                bullets.append([player_x + player_size//2 - 2, player_y])
                try:
                    shoot_sound.play()
                except:
                    pass
            if event.key == pygame.K_p:
                game_paused = not game_paused
                
    if game_over:
        running, action = show_game_over_screen()
        if action == "restart":
            reset_game(current_difficulty)
        elif action == "menu":
            # Volver al menú principal
            running, current_difficulty = show_start_screen()
            if running:
                setup_difficulty(current_difficulty)
                game_over = False  # CORRECCIÓN: Asegurarse de que game_over sea False
        continue
        
    if game_paused:
        show_pause_screen()
        continue
        
    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < 800 - player_size:
        player_x += player_speed
        
    # Generar enemigos
    if random.randint(1, enemy_spawn_rate) == 1:
        enemies.append([random.randint(0, 800 - enemy_size), -enemy_size])
        
    # Generar obstáculos
    if random.randint(1, obstacle_spawn_rate) == 1:
        obstacles.append([random.randint(0, 800 - obstacle_size), -obstacle_size])
        
    # Mover enemigos
    for enemy in enemies[:]:
        enemy[1] += enemy_speed
        if enemy[1] > 600:
            enemies.remove(enemy)
        else:
            draw_enemy(enemy[0], enemy[1])
            
    # Mover obstáculos
    for obstacle in obstacles[:]:
        obstacle[1] += obstacle_speed
        if obstacle[1] > 600:
            obstacles.remove(obstacle)
        else:
            draw_obstacle(obstacle[0], obstacle[1])
            
    # Mover balas
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)
        else:
            draw_bullet(bullet[0], bullet[1])
            
    # Detectar colisiones bala-enemigo
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if (bullet[0] < enemy[0] + enemy_size and
                bullet[0] + 5 > enemy[0] and
                bullet[1] < enemy[1] + enemy_size and
                bullet[1] + 10 > enemy[1]):
                if bullet in bullets:
                    bullets.remove(bullet)
                if enemy in enemies:
                    enemies.remove(enemy)
                    score += 10 * level
                    try:
                        explosion_sound.play()
                    except:
                        pass
                    
    # Detectar colisiones jugador-enemigo
    for enemy in enemies[:]:
        if (player_x < enemy[0] + enemy_size and
            player_x + player_size > enemy[0] and
            player_y < enemy[1] + enemy_size and
            player_y + player_size > enemy[1]):
            if enemy in enemies:
                enemies.remove(enemy)
            player_lives -= 1
            try:
                explosion_sound.play()
            except:
                pass
            if player_lives <= 0:
                game_over = True
                try:
                    game_over_sound.play()
                except:
                    pass
                
    # Detectar colisiones jugador-obstáculo
    for obstacle in obstacles[:]:
        if (player_x < obstacle[0] + obstacle_size and
            player_x + player_size > obstacle[0] and
            player_y < obstacle[1] + obstacle_size and
            player_y + player_size > obstacle[1]):
            if obstacle in obstacles:
                obstacles.remove(obstacle)
            player_lives -= 1
            try:
                explosion_sound.play()
            except:
                pass
            if player_lives <= 0:
                game_over = True
                try:
                    game_over_sound.play()
                except:
                    pass
                
    # Actualizar nivel según puntuación
    update_level()
    
    draw_player(player_x, player_y)
    draw_hud()
    draw_retro_border()
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
