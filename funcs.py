import pygame, math, random
from config import *
from assets import *


def setup():
    clock = pygame.time.Clock()

    total_time = pygame.time.get_ticks() # Variável que guarda o tempo total desde que o jogo foi iniciado

    assets = load_assets()

    all_sprites = pygame.sprite.Group()
    all_platforms = pygame.sprite.Group()
    all_enemies = pygame.sprite.Group()
    all_pukes = pygame.sprite.Group()
    all_spikes = pygame.sprite.Group()
    all_flags = pygame.sprite.Group()

    groups = {}
    groups["all_sprites"] = all_sprites
    groups["all_platforms"] = all_platforms
    groups["all_enemies"] = all_enemies
    groups["all_pukes"] = all_pukes
    groups["all_spikes"] = all_spikes
    groups["all_flags"] = all_flags
    return clock,total_time,assets,all_sprites,all_platforms,all_enemies,all_spikes,all_flags,groups

def gira(lines, angle, amount):
    new_lines = lines.copy()
    new_lines[0] += math.cos(math.radians(angle)) * amount
    new_lines[1] += math.sin(math.radians(angle)) * amount
    return new_lines

def draw_cubes(window, background_polygon_color, cube_scroll, square_effects):
    if random.randint(1, 60) == 1:
        square_effects.append([[random.randint(0, window.get_width()), - 90 + cube_scroll], random.randint(0, 359), random.randint(10, 30) / 20, random.randint(15, 50), random.randint(10, 40) / 500])

    for i, effect in sorted(enumerate(square_effects), reverse = True):
        effect[0][1] += effect[2]
        effect[1] += effect[2] * effect[4]
        effect[3] -= effect[4] / 2
        points = [
                gira(effect[0], math.degrees(effect[1]), effect[3]),
                gira(effect[0], math.degrees(effect[1]) + 90, effect[3]),
                gira(effect[0], math.degrees(effect[1]) + 180, effect[3]),
                gira(effect[0], math.degrees(effect[1]) + 270, effect[3]),
            ]
        if effect[3] < 1:
            square_effects.pop(i)
        else:
            pygame.draw.polygon(window, background_polygon_color, points, 2)

def cronometro(window, total_time):
    font_timer = pygame.font.Font(None, 36) # Fonte para escrever o timer
    passed_time = pygame.time.get_ticks() - total_time # Variável que guarda o tempo que passou desde o começo do nível
    seconds = passed_time // 1000 # Variável que guarda os segundos
    minutes = passed_time // 60000 # Variável que guarda os minutos
    if seconds >= 60:
        seconds = seconds - 60*(int(minutes))
    if seconds < 10:
        seconds = "0" + str(seconds)
    if minutes < 10:
        minutes = "0" + str(minutes)
    tempo = "{0}:{1}.{2}".format(minutes, seconds, str(passed_time)[-3:])
    timer = font_timer.render(tempo, True, WHITE)
    timer_rect = timer.get_rect()
    timer_rect.centerx = WIDTH/2
    timer_rect.top = 10
    window.blit(timer, timer_rect)
    return tempo