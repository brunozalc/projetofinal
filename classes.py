import pygame
from config import *
from assets import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, assets):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets[PLAYER_IMG]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT

        self.speedx = 7 # Velocidade horizontal do jogador
        self.GRAVITY = 0 # Gravidade (começa em 0)

        self.jumps = 0 # Variável que conta o numero de pulos que o jogador deu
        self.max_jumps = 2 # Número máximo de pulos que o jogador pode dar

        self.min_up = PLAYER_HEIGHT/4 # Váriavel que guarda a distância máxima entre o topo da plataforma e o bottom do jogador para considerar que ele está em cima da plataforma

        self.is_on_wall = False # Variável que é True se o jogador estiver em contato com a parede, mas não com o chão e False caso contrário
        self.is_grounded = True # Variável que é True se o jogador estiver no chão e False caso contrário
        self.on_platform = False # Variável que é True se o jogador estiver em cima de uma plataforma e False caso contrário
        self.is_on_platform_right = False # Variável que é True se o jogador estiver encostando no lado direito da plataforma e False caso contrário
        self.is_on_platform_left = False # Variável que é True se o jogador estiver encostando no lado direito da plataforma e False caso contrário

        self.groups = groups
        self.assets = assets

    def update(self):

        if self.is_on_wall == False and self.is_on_platform_left == False and self.is_on_platform_right == False and self.on_platform == False:
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

        platform_collision = pygame.sprite.spritecollide(self, self.groups["all_platforms"], False, pygame.sprite.collide_mask)
        for hit in platform_collision:
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

class Platform(pygame.sprite.Sprite):
    def __init__(self, groups, assets, centerx, centery):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets[PLATFORM]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect.centerx = centerx
        self.rect.centery = centery

        self.groups = groups
        self.assets = assets