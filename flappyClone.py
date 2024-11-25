# https://www.pygame.org/docs/ biblioteca do pygame
import pygame
import sys
import random
import os

pygame.init()

pygame.mixer.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Flappy Bird Clone")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()

# Obtém o caminho correto para o diretório onde o executável está
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

bg_image = pygame.image.load(os.path.join(base_path, "assets/bg.jpg")).convert_alpha()
bird_image = pygame.image.load(os.path.join(base_path, "assets/bird.jpg")).convert_alpha()

bird = {"x": 300, "y": 250, "width": 30, "height": 30, "gravity": 0.4, "lift": -7, "velocity": 0}

pipes = []

frame_count = 0
score = 0
game_over = False

try:
    pygame.mixer.music.load(os.path.join(base_path, "assets/music.mp3")) 
    pygame.mixer.music.play(loops=-1)
except pygame.error as e:
    print(f"Erro ao carregar música: {e}")
    sys.exit()

try:
    jumpSound = pygame.mixer.Sound(os.path.join(base_path, "assets/jump.mp3"))
    deathSound = pygame.mixer.Sound(os.path.join(base_path, "assets/death.mp3"))
except pygame.error as e:
    print(f"Erro ao carregar som: {e}")
    sys.exit()

def draw_bird():
    screen.blit(bird_image, (bird["x"], bird["y"]))

def update_bird():
    global game_over
    bird["velocity"] += bird["gravity"]
    bird["y"] += bird["velocity"]

    # Verificar colisão com as bordas
    if bird["y"] + bird["height"] > 720 or bird["y"] < 0:
        game_over = True

def draw_pipes():
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, (pipe["x"], 0, pipe["width"], pipe["height"]))
        pygame.draw.rect(screen, GREEN, (pipe["x"], pipe["height"] + pipe["gap"], pipe["width"], 720 - pipe["height"] - pipe["gap"]))

def update_pipes():
    global score, pipe_speed
    
    pipe_speed = 4 + score / 300

    if frame_count % 83 == 0:  # Criar novos canos a cada 90 frames
        pipe_height = random.randint(50, 720 // 2)
        pipe_gap = 120 
        pipes.append({"x": 1280, "height": pipe_height, "width": 30, "gap": pipe_gap})

    # Mover os canos para a esquerda
    for pipe in pipes:
           pipe["x"] -= pipe_speed

    # Remover canos fora da tela
    pipes[:] = [pipe for pipe in pipes if pipe["x"] + pipe["width"] > 0]

    # Incrementar o score
    for pipe in pipes:
        if bird["x"] + bird["width"] > pipe["x"] and not pipe.get("score", False):
            score += 100
            pipe["score"] = True

def check_collision():
    global game_over
    for pipe in pipes:
        if (bird["x"] < pipe["x"] + pipe["width"] and
                bird["x"] + bird["width"] > pipe["x"] and
                (bird["y"] < pipe["height"] or bird["y"] + bird["height"] > pipe["height"] + pipe["gap"])):
            game_over = True
            deathSound.play()



def game_loop():
    global frame_count, game_over, pipes, score
    while True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                     pygame.quit()
                     sys.exit()
                if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_SPACE:  # Verifica se a barra de espaço foi pressionada
                        jumpSound.play()
                        if not game_over:   
                                bird["velocity"] = bird["lift"]
                        else:
                                # Reiniciar o jogo ao pressionar espaço
                                pipes = []
                                bird["y"] = 150
                                bird["velocity"] = 0
                                score = 0
                                frame_count = 0
                                game_over = False

        if not game_over:
             update_bird()
             update_pipes()
             check_collision()

        screen.blit(bg_image, (0,0))
        draw_bird()
        draw_pipes()

        # Contabiliza os pontos
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = font.render("Game Over", True, WHITE)
            screen.blit(game_over_text, (1280 // 2 - 50, 720 // 2))

        pygame.display.flip()

        frame_count += 1

        clock.tick(60)

if __name__ == "__main__":
    game_loop()
