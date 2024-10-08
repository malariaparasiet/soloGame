import pygame, sys, math, random
from pygame.locals import QUIT


#initial pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('SoloGame')
pygame.display.set_icon(pygame.image.load("graphics/playerIMG.png"))
font = pygame.font.Font(None, 50)
clock = pygame.time.Clock()

#laad fotos en maakt rects enzo zodat alles werkt
background_surface = pygame.image.load("graphics/backgroundIMG.png").convert()
background_image = pygame.transform.scale(background_surface, (1280, 720))

player_ogSurface = pygame.image.load("graphics/playerIMG.png").convert_alpha()
player = pygame.transform.scale(player_ogSurface, (62.6, 41.4))
player_pos = screen.get_rect().center
player_rect = player.get_rect(center=player_pos)

enemy_ogSurface = pygame.image.load("graphics/enemyIMG.png").convert_alpha()
enemy = pygame.transform.scale(enemy_ogSurface, (62.6, 41.4))

#angle voor de muis volg dingetje 
correction_angle = 0

#enemie list zodat het op het scherm kan blijven
enemies = []

# Brainstorm:
#   - een difficulty slider en die past dan de waarde van de zombie gen aan met de modulo zodat er meer zombies komen per difficulty
#   - Een score meter die met een multiplier
#   - Eigen map met een beetje animatie
#   - Eigen soundtrack (8 of 16-bit)


#dit word uiteindelijk bullet enzo
def shoot():
    print("Shooting")

def enemieGen():

    if pygame.time.get_ticks() % 20 == 0 and len(enemies) < 10:
        enemyPosX = random.randint(0, 1280)
        enemyPosY = random.randint(0, 720)

        print(f"Generating an enemy on {enemyPosX}, {enemyPosY}")

        enemy_rect = enemy.get_rect(center=(enemyPosX, enemyPosY))
        enemies.append(enemy_rect)  # Voeg de nieuwe vijand toe aan de lijst



while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Movement van de speler
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        player_rect.centerx += 5
    if keys[pygame.K_a]:
        player_rect.centerx -= 5
    if keys[pygame.K_w]:
        player_rect.centery -= 5
    if keys[pygame.K_s]:
        player_rect.centery += 5
    
    # Schiet mechanisme met muis
    if pygame.mouse.get_pressed()[0]:
        shoot()

    if player_rect.right >= 1280:
        player_rect.right = 1280
    if player_rect.left <= 0:
        player_rect.left = 0
    if player_rect.bottom >= 720:
        player_rect.bottom = 720
    if player_rect.top <= 0:
        player_rect.top = 0

    # Zodat de speler altijd naar de muis kijkt
    mx, my = pygame.mouse.get_pos()
    dx, dy = mx - player_rect.centerx, my - player_rect.centery
    angle = math.degrees(math.atan2(-dy, dx)) - correction_angle

    # draaien
    rot_image = pygame.transform.rotate(player, angle)
    rot_image_rect = rot_image.get_rect(center=player_rect.center)

    screen.blit(background_image, (0, 0))
    screen.blit(rot_image, rot_image_rect.topleft)

    # Debug knop(pen)
    if keys[pygame.K_q]:
        enemieGen()
    if keys[pygame.K_t] and len(enemies) > 0:
        enemies.pop(0)

    for enemy_rect in enemies:
        screen.blit(enemy, enemy_rect)

    pygame.display.update()
    clock.tick(60)