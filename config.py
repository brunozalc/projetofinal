from os import path

# Pastas onde estão os assets
FNT_DIR = path.abspath(path.join(path.dirname(__file__), "assets", "fonts") )# Pasta de fontes
IMG_DIR = path.abspath(path.join(path.dirname(__file__), "assets", "images")) # Pasta de imagens
SND_DIR = path.abspath(path.join(path.dirname(__file__), "assets", "sounds")) # Pasta de sons
TXT_DIR = path.abspath(path.join(path.dirname(__file__))) # Pasta de textos

# Dados gerais do jogo
WIDTH = 600    # Largura da tela
HEIGHT = 750   # Altura da tela
FPS = 50       # Frames por segundo

# Define tamanhos
PLAYER_WIDTH = 52
PLAYER_HEIGHT = 52
PLATFORM_WIDTH = 150
PLATFORM_HEIGHT = 100
ENEMY_1_WIDTH = 80
ENEMY_1_HEIGHT = 60
#ENEMY_2_WIDTH = 60
#ENEMY_2_HEIGHT = 60

INIT_PLAT_START_TOP = HEIGHT + 200

# Tamanhos de botões
LEVEL_BUTTON_WIDTH = 180
LEVEL_BUTTON_HEIGHT = 70
LEVEL1_BUTTON_XPOS = 200
LEVEL1_BUTTON_YPOS = 230
LEVEL2_BUTTON_XPOS = 200
LEVEL2_BUTTON_YPOS = 330
LEVEL3_BUTTON_XPOS = 200
LEVEL3_BUTTON_YPOS = 430

# Define cores
WHITE = (255, 255, 255)
GRAY = (130, 130, 130)
LIGHT_GRAY = (168, 168, 168)
DARK_GRAY = ((48, 48, 48))
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_RED = (150, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREEN = (0, 150, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (0, 0, 150)
DARK_BLUE = (0, 51, 102)
DARKEST_BLUE = (0, 25, 51)
YELLOW = (255, 255, 0)
LIGHT_YELLOW = (150, 150, 0)

# Estados do jogo
INIT = 0
MENU = 1
LEVEL1 = 2
LEVEL2 = 3
LEVEL3 = 4
END_SCREEN = 5
QUIT = 6