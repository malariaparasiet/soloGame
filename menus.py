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
        self.killedMenuActive = False
        self.screen = screen
        self.mousepos = None

    def UpdateVars(self):
        self.mousepos = pygame.mouse.get_pos()

    def killedMenuCheck(self):
        from main import player
        if self.gameRunning == False and player.health <= 0:
            self.killedMenuActive = True

    def mainMenu(self):
        font = pygame.font.Font("graphics\AurulentSansMNerdFontPropo-Regular.otf", 30)

        mainMenu_Text1 = font.render(f'This is the main menu', False, (255,255,255))
        mainMenu_Text1Rect = mainMenu_Text1.get_rect(center=(infoObject.current_w / 2, infoObject.current_h / 2))
        self.screen.blit(mainMenu_Text1, mainMenu_Text1Rect)

        mainMenu_Text2 = font.render("Start gaming!", False, (255,255,255))
        mainMenu_Text2Rect = mainMenu_Text2.get_rect(center=(infoObject.current_w / 2, infoObject.current_h / 2 + 50))
        self.screen.blit(mainMenu_Text2, mainMenu_Text2Rect)

        # self.mousepos = pygame.mouse.get_pos()

        # print(self.mousepos)

        if mainMenu_Text2Rect.collidepoint(pygame.mouse.get_pos()):
            print(pygame.mouse.get_pos())
            if pygame.mouse.get_pressed()[0]:  # Left click
                logging.info("Starting the game!")
                self.mainMenuActive = False
                self.gameRunning = True

    def killedMenu(self):
        pass