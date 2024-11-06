import pygame, sys, logging
from pygame.locals import *

from enemy_class import Enemy
from player_class import Player
from bullet_class import Bullet
from background_class import Background


#initializing
pygame.init()
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s -  %(levelname)s - %(message)s")

# Krijg informatie over de monitor zodat je automatisch fullscreen wordt gezet
infoObject = pygame.display.Info()

screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), HWSURFACE | DOUBLEBUF )
pygame.display.set_icon(pygame.image.load("graphics/playerIMG.png"))
pygame.display.set_caption("SoloGame Koen Veldkamp H5")
clock = pygame.time.Clock()

# classes callen en gelijk zetten aan een variable
background = Background()
bullet = Bullet(5)
player = Player(7.5, 100)
enemy = Enemy(100, 20, 6)
logging.info("Classes gecalled en geregeld!")


running = True
while running:
    background.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    player.checkIfInsideBoundry()
    player.playerLooksAtMouse()
    player.movement()
    player.updateVariables()

    enemy.GenerateEnemy()
    enemy.check_if_shot(player)
    enemy.move_towards_player(player)
    enemy.look_at_player(player)

    bullet.update()
    bullet.draw()
    bullet.shooting(player)
    bullet.check_if_shot_enemy(enemy) 

    pygame.font.init()

    font = pygame.font.Font("graphics\AurulentSansMNerdFontPropo-Regular.otf", 30)

    clipSizeText_surface = font.render(f'Bullets {bullet.clip_size}/30', False, (255,255,255))
    screen.blit(clipSizeText_surface, (infoObject.current_w - 250, infoObject.current_h - 250))

    scoreText_surface = font.render(f'Score: {player.score}', False, (255,255,255))
    screen.blit(scoreText_surface, (infoObject.current_w - 400, infoObject.current_h - 400))

    # Debug dingen
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q] and len(enemy.enemyList) > 0:
        enemy.enemyList.pop(0)
        logging.debug(f"EnemyList after popping [0]: {enemy.enemyList}")

    pygame.display.flip()
    clock.tick(60)