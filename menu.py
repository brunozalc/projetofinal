import pygame
from os import path
from config import *
from assets import CHECK, E_CHECK, MENU_FONT, load_assets

def menu(screen):
    clock = pygame.time.Clock()
    assets = load_assets()

    # Initialize game state
    dificuldade = [True, True]
    state = None

    # Load and play background music
    pygame.mixer.music.load(path.join(SND_DIR, "menu_music.mp3"))
    pygame.mixer.music.play(loops=-1)

    running = True
    while running:
        # Limit frame rate
        clock.tick(FPS)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = QUIT
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if inside_button(mouse_pos, LEVEL1_BUTTON_XPOS, LEVEL1_BUTTON_YPOS):
                    state = LEVEL1
                    running = False
                elif inside_button(mouse_pos, LEVEL2_BUTTON_XPOS, LEVEL2_BUTTON_YPOS):
                    state = LEVEL2
                    running = False
                elif inside_button(mouse_pos, LEVEL3_BUTTON_XPOS, LEVEL3_BUTTON_YPOS):
                    state = LEVEL3
                    running = False
                elif inside_button(mouse_pos, 50, 550):
                    dificuldade[0] = not dificuldade[0]
                elif inside_button(mouse_pos, 50, 630):
                    dificuldade[1] = not dificuldade[1]

        # Draw the menu
        screen.fill(BLACK)
        draw_button(screen, LEVEL1_BUTTON_XPOS, LEVEL1_BUTTON_YPOS, LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT, "LEVEL 1", inside_button(pygame.mouse.get_pos(), LEVEL1_BUTTON_XPOS, LEVEL1_BUTTON_YPOS), assets[MENU_FONT], GRAY, DARK_GRAY)
        draw_button(screen, LEVEL2_BUTTON_XPOS, LEVEL2_BUTTON_YPOS, LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT, "LEVEL 2", inside_button(pygame.mouse.get_pos(), LEVEL2_BUTTON_XPOS, LEVEL2_BUTTON_YPOS), assets[MENU_FONT], DARK_BLUE, DARKEST_BLUE)
        draw_button(screen, LEVEL3_BUTTON_XPOS, LEVEL3_BUTTON_YPOS, LEVEL_BUTTON_WIDTH, LEVEL_BUTTON_HEIGHT, "LEVEL 3", inside_button(pygame.mouse.get_pos(), LEVEL3_BUTTON_XPOS, LEVEL3_BUTTON_YPOS), assets[MENU_FONT], RED, LIGHT_RED)
        draw_toggle(screen, dificuldade[0], 50, 550, "Inimigos", assets[MENU_FONT], assets[CHECK], assets[E_CHECK])
        draw_toggle(screen, dificuldade[1], 50, 630, "Espinhos", assets[MENU_FONT], assets[CHECK], assets[E_CHECK])

        # Update the display
        pygame.display.flip()

    return state, dificuldade

def inside_button(mouse_pos, x, y):
    """Check if mouse position is inside the button area."""
    mx, my = mouse_pos
    return x <= mx <= x + LEVEL_BUTTON_WIDTH and y <= my <= y + LEVEL_BUTTON_HEIGHT

def draw_button(screen, x, y, width, height, text, is_hovered, font, color, hover_color):
    """Draw a button with optional hover effect."""
    button_color = hover_color if is_hovered else color
    pygame.draw.rect(screen, button_color, (x, y, width, height))
    rendered_text = font.render(text, True, WHITE if is_hovered else GRAY)
    screen.blit(rendered_text, (x + 7, y + 15))

def draw_toggle(screen, is_active, x, y, label, font, check_img, e_check_img):
    """Draw a toggle switch with a label."""
    img = check_img if is_active else e_check_img
    screen.blit(img, (x, y))
    label_text = font.render(label, True, WHITE)
    screen.blit(label_text, (x + 75, y + 10))
