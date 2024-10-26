import pygame, math, random
from config import *
from assets import *
from classes import *
from funcs import *

window = pygame.display.set_mode((WIDTH, HEIGHT))
square_effects = []

def level1(window, dificuldade):
    clock, total_time, assets, all_sprites, all_platforms, all_enemies, all_spikes, all_flags, groups = setup()

    background_polygon_color = (48, 48, 48)

    cube_scroll = 0

    # Plataforma inicial (a mais de baixo)
    init_plat = Init_Platform(groups, assets, 0, INIT_PLAT_START_TOP)
    all_platforms.add(init_plat)
    all_sprites.add(init_plat)

    # Jogador
    player = Player(groups, assets, init_plat.rect.top)
    all_sprites.add(player)

    # Abrindo o arquivo que possui as coordenadas de todas as plataformas do nível 1
    with open(os.path.join(TXT_DIR, "plataformas1.txt"), "r") as arquivo:
        plataformas = arquivo.readlines()

    # Outras plataformas
    for i in range(len(plataformas)):
        plat = plataformas[i].split(",")
        platform = Platform(groups, assets, int(plat[0]), int(plat[1]))
        all_platforms.add(platform)
        all_sprites.add(platform)

    if dificuldade[0] == True: # Se os inimigos estiverem ativados
    
        # Abrindo o arquivo com as coordenadas dos inimigos do nível 1
        with open(os.path.join(TXT_DIR, "posenem1.txt"), 'r') as arquivo:
            inimigo1 = arquivo.readlines()
        
        # Gerando os outros inimigos
        for i in range(len(inimigo1)):
            enem = inimigo1[i].split(',')
            enemy = Enemy_1(groups, assets, int(enem[0]), int(enem[1]))
            all_enemies.add(enemy)
            all_sprites.add(enemy)

    if dificuldade[1] == True: # Se os espinhos estiverem ativados

        # Abrindo o arquivo com as coordenadas dos espinhos do nível 1
        with open(os.path.join(TXT_DIR, "spikes1.txt"), "r") as arquivo:
            spikes = arquivo.readlines()

        # Espinhos
        for i in range(len(spikes)):
            coords = spikes[i].split(",")
            spike = Spike(groups, assets, int(coords[0]), int(coords[1]), int(coords[2]))
            all_spikes.add(spike)
            all_sprites.add(spike)

    # Flag
    flag = Flag(groups, assets, 525, -4675)
    all_flags.add(flag)

    keys_down = {}

    # Colocando a música
    pygame.mixer.music.load(os.path.join(SND_DIR, "level1_music.mp3"))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)

    running = True
    while running:
        window.fill((0, 0, 0))

        clock.tick(FPS)

        for event in pygame.event.get():

            # Sair do jogo
            if event.type == pygame.QUIT:
                running = False
                state = QUIT

            if event.type == pygame.KEYDOWN:
                keys_down[event.key] = True
                # Pular
                if event.key == pygame.K_SPACE and player.jumps < player.max_jumps:
                    if player.is_on_wall == True: # Jogador está na parede
                        player.is_on_wall = False
                        if player.rect.right >= WIDTH:
                            player.speedx = -7
                        elif player.rect.left <= 0:
                            player.speedx = 7
                    if player.is_on_platform_left == True: # Jogador está no lado esquerdo da plataforma
                        player.is_on_platform_left = False
                        player.speedx = -7
                    elif player.is_on_platform_right == True: # Jogador está no lado direito da plataforma
                        player.is_on_platform_right = False
                        player.speedx = 7

                    player.GRAVITY = -15 # Diminuir a gravidade é o que faz o jogador ir para cima
                    player.jumps += 1
                    assets[JUMP_SFX].play()

                # Voltar ao menu
                if event.key == pygame.K_ESCAPE:
                    running = False
                    state = MENU
        
        all_sprites.update()

        # Cubos!
        draw_cubes(window, background_polygon_color, cube_scroll, square_effects)

        all_sprites.draw(window)
        all_flags.draw(window)

        # Parte dos inimigos
        all_enemies.update()
            
        # Colisão com inimigo
        enemy_hit = pygame.sprite.spritecollide(player, all_enemies, False, pygame.sprite.collide_mask)
        if len(enemy_hit) > 0:

            assets[DEATH_SFX].play()
            
            player.kill()
            
            # Movendo tudo para cima e criando outro jogador
            y_moved1 = INIT_PLAT_START_TOP - init_plat.rect.top - 300
            for platform in all_platforms:
                platform.rect.centery -= abs(y_moved1)
            for enemy in all_enemies:
                enemy.rect.centery -= abs(y_moved1)
            for s in all_spikes:
                s.rect.centery -= abs(y_moved1)
            flag.rect.centery -= abs(y_moved1)
            player = Player(groups, assets, init_plat.rect.top)
            all_sprites.add(player)

        all_enemies.draw(window)

        # Fazendo tudo se mover para baixo quando o jogador se aproxima do topo
        if player.rect.centery <= player.offset:
            if player.is_grounded == True or player.is_on_platform_left == True or player.is_on_platform_right == True or player.is_on_wall == True:
                continue
            else:
                player.rect.centery += abs(player.GRAVITY)
                for platform in all_platforms:
                    platform.rect.centery += abs(player.GRAVITY)
                for s in all_spikes:
                    s.rect.centery += abs(player.GRAVITY)
                flag.rect.centery += abs(player.GRAVITY)
                for enemy in all_enemies:
                    enemy.rect.centery += abs(player.GRAVITY)

        # Fazendo tudo se mover para cima quando o jogador se aproxima do chão
        if player.rect.bottom >= HEIGHT - player.offset:
            player.rect.centery -= abs(player.GRAVITY)
            for platform in all_platforms:
                platform.rect.centery -= abs(player.GRAVITY)
            for s in all_spikes:
                s.rect.centery -= abs(player.GRAVITY)
            flag.rect.centery -= abs(player.GRAVITY)
            for enemy in all_enemies:
                enemy.rect.centery -= abs(player.GRAVITY)

        # Checando colisão do jogador com espinhos
        spike_collision = pygame.sprite.spritecollide(player, groups["all_spikes"], False, pygame.sprite.collide_mask)
        if len(spike_collision) > 0:

            assets[DEATH_SFX].play()

            player.kill()

            # Movendo tudo para cima de novo
            y_moved = INIT_PLAT_START_TOP - init_plat.rect.top - 300
            for platform in all_platforms:
                platform.rect.centery -= abs(y_moved)
            for s in all_spikes:
                s.rect.centery -= abs(y_moved)
            flag.rect.centery -= abs(y_moved)
            for enemy in all_enemies:
                enemy.rect.centery -= abs(y_moved)
            player = Player(groups, assets, init_plat.rect.top)
            all_sprites.add(player)

        # Fim do level
        if len(pygame.sprite.spritecollide(player, groups["all_flags"], False, pygame.sprite.collide_mask)) > 0:
            running = False
            state = END_SCREEN
        
        # Cronômetro
        tempo = cronometro(window, total_time)

        pygame.display.update()

    return state, tempo, dificuldade

