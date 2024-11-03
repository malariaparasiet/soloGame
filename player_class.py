import pygame, math, logging
from pygame.locals import *

#initializing
pygame.init()
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s -  %(levelname)s - %(message)s")

# Krijg informatie over de monitor zodat je automatisch fullscreen wordt gezet
infoObject = pygame.display.Info()

screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), HWSURFACE | DOUBLEBUF )

clock = pygame.time.Clock()

# Maak class voor player

class Player(object):
    def __init__(self, speed, health):

        #position player to middle & player variables
        self.x = infoObject.current_w / 2
        self.y = infoObject.current_h / 2
        self.speed = speed
        self.health = health
        self.correction_angle = 0
        self.rot_image_rect = None
        self.angle = None

        #image magic because scaling n shi
        self.oldImage = pygame.image.load("graphics/playerIMg.png")
        self.scaledImage =  pygame.transform.scale(self.oldImage, (63, 41))
        self.rectImage = self.scaledImage.get_rect(center=(self.x, self.y))
        logging.info("Initialized player class!")

    #functie om movement mogelijk te maken
    def movement(self):
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_d]:
            self.rectImage.centerx += self.speed
        if self.keys[pygame.K_a]:
            self.rectImage.centerx -= self.speed
        if self.keys[pygame.K_w]:
            self.rectImage.centery -= self.speed
        if self.keys[pygame.K_s]:
            self.rectImage.centery += self.speed

    #kijken of de speler niet buiten de game kan lopen
    def checkIfInsideBoundry(self):
        if self.rectImage.right >= infoObject.current_w:
            self.rectImage.right = infoObject.current_w
        if self.rectImage.left <= 0:
            self.rectImage.left = 0
        if self.rectImage.bottom >= infoObject.current_h:
            self.rectImage.bottom = infoObject.current_h
        if self.rectImage.top <= 0:
            self.rectImage.top = 0

    # wiskunde magie zodat de speler naar de muis kijkt
    def playerLooksAtMouse(self):
        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - self.rectImage.centerx, my - self.rectImage.centery
        self.angle = math.degrees(math.atan2(-dy, dx)) - self.correction_angle

        # draaien
        rot_image = pygame.transform.rotate(self.scaledImage, self.angle)
        self.rot_image_rect = rot_image.get_rect(center=self.rectImage.center)

        screen.blit(rot_image, self.rot_image_rect.topleft)