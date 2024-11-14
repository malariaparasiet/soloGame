import pygame
import sys
import logging
from pygame.locals import *

# Importeer aangepaste klassen
from enemy_class import Enemy
from player_class import Player
from bullet_class import Bullet
from background_class import Background
from menus import Menus

# TODO
# 1. Geluidseffecten toevoegen.
# 2. Verbeter de weergave van tekst.
# 3. Voeg animaties toe.
# 4. Versnel het spel voor meer uitdaging.
# 5. Voeg opmerkingen toe en optimaliseer de code waar mogelijk.

# Initialisatie van Pygame en de audio-instellingen
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.font.init()
pygame.init()
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s -  %(levelname)s - %(message)s")

# Krijg scherminformatie voor fullscreen-modus
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), HWSURFACE | DOUBLEBUF)
pygame.display.set_icon(pygame.image.load("graphics/playerIMG.png"))
pygame.display.set_caption("SoloGame Koen Veldkamp H5")

# Stel de achtergrondmuziek in en start deze
pygame.mixer.music.load("graphics/bgMusic.mp3")
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()

# Initialiseer klassen en log dit
background = Background()
bullet = Bullet(5)  # Snelheid van de kogel
player = Player(7.5, 100)  # Snelheid en gezondheid van de speler
enemy = Enemy(100, 20, 6)  # Gezondheid, spawnrate, snelheid van de vijanden
menus = Menus(screen)
logging.info("Classes zijn geïnitialiseerd en gereed!")

# Hoofdgame-loop
while True:
    # Event-afhandeling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Hoofdmenu weergeven als het actief is en het spel niet draait
    if menus.mainMenuActive and not menus.gameRunning:
        menus.mainMenu()

    # Game-logica als het spel draait
    elif menus.gameRunning:
        menus.killedMenuActive = True
        background.draw()  # Teken de achtergrond

        # Update speleracties
        player.check_if_inside_boundary()  # Controleer of speler binnen de grenzen is
        player.player_looks_at_mouse()  # Laat de speler naar de muis kijken
        player.movement()  # Verwerk spelerbewegingen
        player.is_being_touched_by_enemy()  # Controleer of de speler wordt geraakt door vijanden

        # Update vijandacties
        enemy.GenerateEnemy()  # Genereer nieuwe vijanden
        enemy.move_towards_player(player)  # Beweeg vijanden richting de speler
        enemy.look_at_player(player)  # Laat vijanden naar de speler kijken

        # Update kogels
        bullet.update()  # Update de posities van de kogels
        bullet.draw()  # Teken de kogels
        bullet.shooting(player)  # Verwerk schieten door de speler
        bullet.check_if_shot_enemy(enemy)  # Controleer of een vijand is geraakt

        # Teken score en statusinformatie
        font = pygame.font.Font("graphics/AurulentSansMNerdFontPropo-Regular.otf", 30)
        font_small = pygame.font.Font("graphics/AurulentSansMNerdFontPropo-Regular.otf", 15)

        # Tekst voor munitie
        clipSizeText_surface = font.render(f'Bullets {bullet.clip_size}/30', False, (255, 255, 255))
        screen.blit(clipSizeText_surface, (infoObject.current_w - 250, infoObject.current_h - 250))

        # Tekst voor score
        scoreText_surface = font.render(f'Score: {bullet.score}', False, (255, 255, 255))
        screen.blit(scoreText_surface, (infoObject.current_w - 250, infoObject.current_h - 300))

        # Gezondheid van de speler
        healthText_surface = font_small.render(f'Health: {player.health}', False, (255, 255, 255))
        screen.blit(healthText_surface, (player.rot_image_rect.x, player.rot_image_rect.y + 40))

        # Herlaadmelding als de munitie op is
        if bullet.clip_size == 0:
            needReload_surface = font_small.render('Thou should reload!', False, (255, 0, 0))
            screen.blit(needReload_surface, (player.rot_image_rect.x, player.rot_image_rect.y - 25))

        # Debug-opties voor vijanden en spelergezondheid
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q] and enemy.enemyList:
            enemy.enemyList.pop(0)  # Verwijder de eerste vijand uit de lijst
            logging.debug(f"EnemyList na het verwijderen van [0]: {enemy.enemyList}")
        if keys[pygame.K_u] and player.health > 0:
            player.health -= 25  # Verminder gezondheid van de speler voor testdoeleinden

        # Update display en houd de framerate constant
        pygame.display.flip()
        clock.tick(60)

    # Als de speler dood is, toon het "killed" menu
    if menus.killedMenuActive and player.health <= 0:
        menus.gameRunning = False
        menus.killedMenu()

    # Dubbel flip om visuele bugs te voorkomen
    pygame.display.flip()
    clock.tick(60)
