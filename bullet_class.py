import pygame, sys, math, random, logging
from pygame.locals import *

#initializing
pygame.init()
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s -  %(levelname)s - %(message)s")

# Krijg informatie over de monitor zodat je automatisch fullscreen wordt gezet
infoObject = pygame.display.Info()

screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), HWSURFACE | DOUBLEBUF )

clock = pygame.time.Clock()

# Maak class voor bullets

class Bullet(object):
    def __init__(self, velocity):
        self.velocity = velocity
        self.bulletIMG = pygame.image.load("graphics/bulletIMG.png").convert_alpha()
        self.scaledImage = pygame.transform.scale(self.bulletIMG, (45, 45))
        self.rectImage = None
        self.x = None
        self.y = None
        self.bulletList = []
        logging.info("Initialized bullet class!")

    def debugShooting(self):
        from main import player
        if pygame.mouse.get_pressed()[0]:
            self.x, self.y = player.rot_image_rect.centerx, player.rot_image_rect.centery
            self.rectImage = self.scaledImage.get_rect(center=(self.x + 26 * math.cos(player.angle), self.y + 9 * math.sin(player.angle)))
            screen.blit(self.scaledImage, self.rectImage)
            logging.info(f"Center x: {player.rot_image_rect.centerx}, center y: {player.rot_image_rect.centery}")