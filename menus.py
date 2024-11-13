import pygame, math, logging
from pygame.locals import *

#initializing
pygame.init()
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s -  %(levelname)s - %(message)s")

# Krijg informatie over de monitor zodat je automatisch fullscreen wordt gezet
infoObject = pygame.display.Info()

clock = pygame.time.Clock()

# Maak class voor menus

class Menus(object):
    def __init__(self, screen):
        self.gameRunning = False
        self.mainMenuActive = True
        self.killedMenuActive = True
        self.screen = screen


    def mainMenu(self):

        mainMenuBG_ogImg = pygame.image.load("graphics/mainMenuBG.png").convert()
        mainMenuBG_image = pygame.transform.scale(mainMenuBG_ogImg, (infoObject.current_w, infoObject.current_h))

        self.screen.blit(mainMenuBG_image, (0,0))

        font = pygame.font.Font("graphics\AurulentSansMNerdFontPropo-Regular.otf", 30)

        mainMenu_Text1 = font.render(f'This is the main menu', False, (255,255,255))
        mainMenu_Text1Rect = mainMenu_Text1.get_rect(center=(infoObject.current_w / 2, infoObject.current_h / 2))
        self.screen.blit(mainMenu_Text1, mainMenu_Text1Rect)

        mainMenu_Text2 = font.render("Start gaming!", False, (255,255,255))
        mainMenu_Text2Rect = mainMenu_Text2.get_rect(center=(infoObject.current_w / 2, infoObject.current_h / 2 + 50))
        self.screen.blit(mainMenu_Text2, mainMenu_Text2Rect)

        if mainMenu_Text2Rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:  # Left click
                logging.info("Starting the game!")
                self.mainMenuActive = False
                self.gameRunning = True

    def killedMenu(self):

        killedMenuBG_ogImg = pygame.image.load("graphics/killedMenuBG.png").convert()
        killedMenuBG_image = pygame.transform.scale(killedMenuBG_ogImg, (infoObject.current_w, infoObject.current_h))

        self.screen.blit(killedMenuBG_image, (0,0))

        font = pygame.font.Font("graphics\AurulentSansMNerdFontPropo-Regular.otf", 30)

        killedMenuText1 = font.render(f'You got killed :(', False, (255,255,255))
        killedMenu_Text1Rect = killedMenuText1.get_rect(center=(infoObject.current_w / 2, infoObject.current_h / 2))
        self.screen.blit(killedMenuText1, killedMenu_Text1Rect)

        killedMenu_Text2 = font.render("Restart your run!", False, (255,255,255))
        killedMenu_Text2Rect = killedMenu_Text2.get_rect(center=(infoObject.current_w / 2, infoObject.current_h / 2 + 50))
        self.screen.blit(killedMenu_Text2, killedMenu_Text2Rect)

        if killedMenu_Text2Rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:  # Left click
                logging.info("Restarting the game!")
                self.gameRunning = True
                self.killedMenuActive = False
                self.gameRunning = True
                
                from main import enemy, player, bullet

                enemy.enemyList.clear()

                player.rectImage.x = infoObject.current_w / 2
                player.rectImage.y = infoObject.current_h / 2
                player.health = 100
                bullet.score = 0

                bullet.clip_size = 30

                self.killedMenuActive = True

                