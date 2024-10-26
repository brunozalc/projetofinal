import pygame
from config import *
from assets import *
from funcs import *

class Rect(pygame.sprite.Sprite):
    def __init__(self, image, groups, assets):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.groups = groups
        self.assets = assets

class Player(Rect):
    def __init__(self, groups, assets, plat_inicial_top):
        super().__init__(assets[PLAYER_IMG], groups, assets)

        self.rect.centerx = WIDTH/2
        self.rect.bottom = plat_inicial_top

        self.speedx = 7 # Velocidade horizontal do jogador
        self.GRAVITY = 0 # Gravidade (começa em 0)
        self.max_GRAVITY = 25 # Ter uma gravidade máxima é importante, pois gravidades muito altas fazem o jogador passar por dentro das plataformas

        self.offset = 300

        self.jumps = 0 # Variável que conta o numero de pulos que o jogador deu
        self.max_jumps = 2 # Número máximo de pulos que o jogador pode dar

        self.is_on_wall = False # Variável que é True se o jogador estiver em contato com a parede, mas não com o chão e False caso contrário
        self.is_grounded = True # Variável que é True se o jogador estiver no chão e False caso contrário
        self.on_platform = False # Variável que é True se o jogador estiver em cima de uma plataforma e False caso contrário
        self.is_on_platform_right = False # Variável que é True se o jogador estiver encostando no lado direito da plataforma e False caso contrário
        self.is_on_platform_left = False # Variável que é True se o jogador estiver encostando no lado direito da plataforma e False caso contrário

    def update(self):

        if self.is_on_wall == False and self.is_on_platform_left == False and self.is_on_platform_right == False and self.on_platform == False and self.GRAVITY < self.max_GRAVITY:
            self.GRAVITY += 1

        self.rect.x += self.speedx
        self.rect.y += self.GRAVITY

        if (self.rect.right >= WIDTH or self.rect.left <= 0) and self.is_grounded == False:
            self.is_on_wall = True
        else:
            self.is_on_wall = False

        if self.is_on_wall == True or self.is_on_platform_left == True or self.is_on_platform_right == True:
            self.jumps = 0 # Resetando o numero de pulos
            self.GRAVITY = 5 # Menor gravidade para sensação de deslizamento

        if self.rect.bottom >= HEIGHT or self.on_platform == True:
            self.is_grounded = True
        else:
            self.is_grounded = False

        if self.is_grounded == True:
            self.jumps = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            if self.is_on_wall == False:
                self.speedx = -7
        if self.rect.left < 0:
            self.rect.left = 0
            if self.is_on_wall == False:
                self.speedx = 7
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.is_on_wall = False
            self.is_grounded = True

        # Resetando certas variáveis (serve para impedir que uma vez que elas fiquem True, não sejam True para sempre)
        self.on_platform = False
        self.is_on_platform_left = False
        self.is_on_platform_right = False

        # Checando colisão com plataformas
        platform_collision = pygame.sprite.spritecollide(self, self.groups["all_platforms"], False, pygame.sprite.collide_mask)
        for hit in platform_collision:
            if self.rect.topright == hit.rect.bottomleft or self.rect.topleft == hit.rect.bottomright:
                continue
            if self.rect.bottom >= hit.rect.top and self.rect.top < hit.rect.top:
                self.rect.bottom = hit.rect.top
                self.on_platform = True
                self.jumps = 0
                self.GRAVITY = 0
            elif self.rect.right >= hit.rect.left and self.rect.left < hit.rect.left and ((self.rect.top <= hit.rect.bottom and self.rect.bottom > hit.rect.top) or (self.rect.bottom > hit.rect.bottom and self.rect.top < hit.rect.bottom)):
                self.rect.right = hit.rect.left
                self.is_on_platform_left = True
            elif self.rect.left <= hit.rect.right and self.rect.right > hit.rect.right and ((self.rect.top <= hit.rect.bottom and self.rect.bottom > hit.rect.top) or (self.rect.bottom > hit.rect.bottom and self.rect.top < hit.rect.bottom)):
                self.rect.left = hit.rect.right
                self.is_on_platform_right = True
            elif self.rect.top <= hit.rect.bottom and self.rect.bottom > hit.rect.bottom:
                self.rect.top = hit.rect.bottom
                self.GRAVITY = 0

        for platform in self.groups["all_platforms"]:
            if self.is_grounded == True or self.is_on_platform_left == True or self.is_on_platform_right == True:
                continue
            else:
                platform.rect.centery -= self.GRAVITY

        for spike in self.groups["all_spikes"]:
            if self.is_grounded == True or self.is_on_platform_left == True or self.is_on_platform_right == True:
                continue
            else:
                spike.rect.centery -= self.GRAVITY

        for platform in self.groups["all_enemies"]:
            if self.is_grounded == True or self.is_on_platform_left == True or self.is_on_platform_right == True:
                continue
            else:
                platform.rect.centery -= self.GRAVITY

        for flag in self.groups["all_flags"]:
            if self.is_grounded == True or self.is_on_platform_left == True or self.is_on_platform_right == True:
                continue
            else:
                flag.rect.centery -= self.GRAVITY

class Platform(Rect):
    def __init__(self, groups, assets, centerx, centery):
        super().__init__(assets[PLATFORM], groups, assets)

        self.rect.centerx = centerx
        self.rect.centery = centery

class Init_Platform(Rect):
    def __init__(self, groups, assets, left, bottom):
        super().__init__(assets[INIT_PLAT], groups, assets)

        self.rect.left = left
        self.rect.bottom = bottom

class Enemy_1(Rect):
    def __init__(self, groups, assets, x, y, pace=3, turn=70, speed= 30):           # vira em 98, pq 150 da plataforma - player width
        super().__init__(assets["enemy1"], groups, assets)

        self.rect.center = (x, y)  # Onde está
        self.pace_ta = pace        # Tamanho do passo
        self.pace_c = 0            # distância percorrida
        self.direction = -1        # Começa a ir para esquerda
        self.turn = turn           # limitando a distância
        self.speed = speed         # "intervalo de tempo" do passo
        self.pace_t = 0            # tempo do último passo

    def update(self):
        # Implementando o movimento correto agora
        t_n = pygame.time.get_ticks()
        if (t_n > self.pace_t + self.speed):
            self.pace_t = t_n

            self.pace_c += 1
            self.rect.x  += self.direction * self.pace_ta

            if(self.pace_c >= self.turn):
                # girando para o outro lado
                self.direction *= -1
                self.pace_c = 0
            
            if(self.rect.x <= 0):
                self.direction = 1
                self.pace_c = 0
            elif(self.rect.x >= WIDTH - self.rect.width):
                self.direction = 1
                self.pace_c = 0

class Spike(Rect):
    def __init__(self, groups, assets, x_pos, bottom, rotacao):
        super().__init__(assets[SPIKE], groups, assets)

        self.rect.centerx = x_pos
        self.rect.bottom = bottom

        self.image = pygame.transform.rotate(assets[SPIKE], rotacao)

class Flag(Rect):
    def __init__(self, groups, assets, x_pos, bottom):
        super().__init__(assets[FLAG], groups, assets)
        
        self.rect.centerx = x_pos
        self.rect.bottom = bottom