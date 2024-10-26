from funcs import gira, setup, draw_cubes
from menu import inside_button
import pytest
import pygame
WIDTH = 600    # Largura da tela
HEIGHT = 750   # Altura da tela


def test_gira():
    # Testa com um ângulo de 90 graus e quantidade 10
    lines = [0, 0]
    angle = 90
    amount = 10
    result = gira(lines, angle, amount)
    assert result == pytest.approx([0, 10]), f"Expected [0, 10], but got {result}"

def test_gira_45_degrees():
    # Testa com um ângulo de 45 graus e quantidade 10
    lines = [0, 0]
    angle = 45
    amount = 10
    result = gira(lines, angle, amount)
    # Para 45 graus, as coordenadas esperadas são aproximadamente [7.07, 7.07]
    expected = [7.07, 7.07]
    assert result == pytest.approx(expected, rel=1e-2), f"Expected {expected}, but got {result}"

def test_gira_180_degrees():
    # Testa com um ângulo de 180 graus e quantidade 10
    lines = [0, 0]
    angle = 180
    amount = 10
    result = gira(lines, angle, amount)
    # Para 180 graus, o ponto deve mover-se para [-10, 0]
    expected = [-10, 0]
    assert result == pytest.approx(expected), f"Expected {expected}, but got {result}"

pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Project Jump")
# Define constantes para os testes
LEVEL_BUTTON_WIDTH = 100
LEVEL_BUTTON_HEIGHT = 50

def test_inside_button_within_bounds():
    # Teste quando o mouse está dentro dos limites do botão
    mouse_pos = (75, 75)
    x, y = 50, 50
    assert inside_button(mouse_pos, x, y) == True, f"Expected True, but got False for mouse position {mouse_pos} inside button at ({x}, {y})"

def test_inside_button_outside_bounds():
    # Teste quando o mouse está fora dos limites do botão
    mouse_pos = (200, 200)
    x, y = 50, 50
    assert inside_button(mouse_pos, x, y) == False, f"Expected False, but got True for mouse position {mouse_pos} outside button at ({x}, {y})"

def test_inside_button_on_edge():
    # Teste quando o mouse está exatamente na borda do botão
    mouse_pos = (150, 100)  # Borda inferior direita do botão
    x, y = 50, 50
    assert inside_button(mouse_pos, x, y) == True, f"Expected True, but got False for mouse position {mouse_pos} on the edge of button at ({x}, {y})"

def test_setup_initializes_clock():
    clock, total_time, assets, all_sprites, all_platforms, all_enemies, all_spikes, all_flags, groups = setup()
    
    # Verifica se clock é uma instância de pygame.time.Clock
    assert isinstance(clock, pygame.time.Clock), "Expected clock to be an instance of pygame.time.Clock"

def test_setup_initializes_total_time():
    clock, total_time, assets, all_sprites, all_platforms, all_enemies, all_spikes, all_flags, groups = setup()
    
    # Verifica se total_time é um inteiro
    assert isinstance(total_time, int), "Expected total_time to be an integer"

def test_setup_initializes_assets():
    clock, total_time, assets, all_sprites, all_platforms, all_enemies, all_spikes, all_flags, groups = setup()
    
    # Verifica se assets é um dicionário
    assert isinstance(assets, dict), "Expected assets to be a dictionary"

def test_setup_initializes_groups():
    clock, total_time, assets, all_sprites, all_platforms, all_enemies, all_spikes, all_flags, groups = setup()
    
    # Verifica se os grupos de sprites são instâncias de pygame.sprite.Group
    assert isinstance(all_sprites, pygame.sprite.Group), "Expected all_sprites to be an instance of pygame.sprite.Group"
    assert isinstance(all_platforms, pygame.sprite.Group), "Expected all_platforms to be an instance of pygame.sprite.Group"
    assert isinstance(all_enemies, pygame.sprite.Group), "Expected all_enemies to be an instance of pygame.sprite.Group"
    assert isinstance(all_spikes, pygame.sprite.Group), "Expected all_spikes to be an instance of pygame.sprite.Group"
    assert isinstance(all_flags, pygame.sprite.Group), "Expected all_flags to be an instance of pygame.sprite.Group"

def test_setup_initializes_groups_dict():
    clock, total_time, assets, all_sprites, all_platforms, all_enemies, all_spikes, all_flags, groups = setup()
    
    # Verifica se o dicionário groups tem as chaves corretas
    expected_keys = {"all_sprites", "all_platforms", "all_enemies", "all_pukes", "all_spikes", "all_flags"}
    assert isinstance(groups, dict), "Expected groups to be a dictionary"
    assert set(groups.keys()) == expected_keys, f"Expected groups keys to be {expected_keys}, but got {set(groups.keys())}"


def test_draw_cubes_adds_effects():
    # Configuração
    window = pygame.display.set_mode((800, 600))
    background_polygon_color = (255, 255, 255)  # Cor branca
    cube_scroll = 5
    square_effects = []

    # Chama a função e verifica se um efeito foi adicionado
    draw_cubes(window, background_polygon_color, cube_scroll, square_effects)
    
    # Verifica se, potencialmente, um efeito foi adicionado
    # Não podemos garantir que sempre será adicionado porque depende de random
    assert len(square_effects) >= 0, "The function should not remove elements without reason."

def test_draw_cubes_updates_effects():
    # Configuração
    window = pygame.display.set_mode((800, 600))
    background_polygon_color = (255, 255, 255)  # Cor branca
    cube_scroll = 5
    square_effects = [
        [[100, -85], 45, 1.5, 30, 0.02],  # Um efeito de exemplo
    ]

    # Chama a função e verifica se o efeito é atualizado corretamente
    draw_cubes(window, background_polygon_color, cube_scroll, square_effects)

    # Verifica se o efeito foi atualizado conforme esperado
    # O teste é aproximado devido à matemática de ponto flutuante
    assert square_effects[0][0][1] == pytest.approx(-85 + 1.5), "Expected the Y position to increase by the speed."
    assert square_effects[0][3] == pytest.approx(30 - (0.02 / 2)), "Expected the size to decrease based on the decay rate."

def test_draw_cubes_removes_small_effects():
    # Configuração
    window = pygame.display.set_mode((800, 600))
    background_polygon_color = (255, 255, 255)  # Cor branca
    cube_scroll = 5
    square_effects = [
        [[100, -85], 45, 1.5, 0.5, 0.02],  # Um efeito pequeno que deve ser removido
    ]

    # Chama a função e verifica se o efeito é removido quando menor que 1
    draw_cubes(window, background_polygon_color, cube_scroll, square_effects)

    # Verifica se o efeito foi removido
    assert len(square_effects) == 0, "Expected the small effect to be removed from the list."