import pygame, sys, math
from pygame.locals import QUIT

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('SoloGame')
font = pygame.font.Font(None, 50)
clock = pygame.time.Clock()

background_surface = pygame.image.load("graphics/backgroundIMG.png").convert()
background_image = pygame.transform.scale(background_surface, (1280, 720))

player_ogSurface = pygame.image.load("graphics/playerIMG.png").convert_alpha()
player = pygame.transform.scale(player_ogSurface, (62.6, 41.4))
player_pos = screen.get_rect().center
player_rect = player.get_rect(center=player_pos)

zwaartekracht = 0
game_actief = True

correction_angle = 0

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Movement van de speler
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player_rect.centerx += 5
    if keys[pygame.K_LEFT]:
        player_rect.centerx -= 5
    if keys[pygame.K_UP]:
        player_rect.centery -= 5
    if keys[pygame.K_DOWN]:
        player_rect.centery += 5
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
        print("SHOOT")

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

    pygame.display.update()
    clock.tick(60)
