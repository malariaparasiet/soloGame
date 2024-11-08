import pygame, sys, math, random, logging
from pygame.locals import *

#initializing
pygame.init()
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s -  %(levelname)s - %(message)s")

# Krijg informatie over de monitor zodat je automatisch fullscreen wordt gezet
infoObject = pygame.display.Info()

screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), HWSURFACE | DOUBLEBUF )

clock = pygame.time.Clock()

# Maak class voor achtergrond

class Background(object):
    def __init__(self):
        self.background_ogImg = pygame.image.load("graphics/backgroundIMG.png").convert()
        self.background_image = pygame.transform.scale(self.background_ogImg, (infoObject.current_w, infoObject.current_h))
        logging.info("Initialized background class!")

    def draw(self):
        screen.blit(self.background_image, (0,0))