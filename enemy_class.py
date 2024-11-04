import pygame, sys, math, random, logging
from pygame.locals import *

#initializing
pygame.init()
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s -  %(levelname)s - %(message)s")

# Krijg informatie over de monitor zodat je automatisch fullscreen wordt gezet
infoObject = pygame.display.Info()

screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), HWSURFACE | DOUBLEBUF )

clock = pygame.time.Clock()

class Enemy(object):
    def __init__(self, health, spawnrate, speed):
        self.health = health
        self.spawnrate = spawnrate
        self.speed = speed
        self.oldImage = pygame.image.load("graphics/enemyIMG.png").convert_alpha()
        self.scaledImage = pygame.transform.scale(self.oldImage, (63, 41))
        self.enemyList = []
        self.rectImage = None
        logging.info("Initalized enemy class!")

    def GenerateEnemy(self):
        # een modules operation voor om de spawnrate te bepalen en voor semi "random" spawntijden
        if random.randint(1,5) == random.randint(1,5) and len(self.enemyList) < 10:
            
            # random positie krijgen om een enemy te spawnen
            self.posX = random.randint(0, 1280)
            self.posY = random.randint(0, 720)

            # debug
            logging.debug(f"Generating an enemy on {self.posX}, {self.posY}")

            # als die een enemy kan spawnen dan ook de rect aanmaken en toevoegen aan een lijst zodat de enemy op het scherm blijft
            self.rectImage = self.scaledImage.get_rect(center=(self.posX, self.posY))
            self.enemyList.append(self.rectImage)  # Voeg de nieuwe vijand toe aan de lijst

    def move_towards_player(self):        
        from main import player
        for self.rectImage in self.enemyList:    
            #Vind de richtings vector tussen de zombies en de speler
            dx, dy = player.rot_image_rect.x - self.rectImage.x, player.rot_image_rect.y - self.rectImage.y
            dist = math.hypot(dx, dy)
            if dist != 0:
                dx, dy = dx / dist, dy / dist # Maak het beter
            else:
                continue
            # Ga naar de speler toe met een bepaalde snelheid
            self.rectImage.x += dx * self.speed
            self.rectImage.y += dy * self.speed

    def check_if_shot(self):        
        from main import player
        for self.rectImage in self.enemyList:
            if self.rectImage.colliderect(player.rot_image_rect):
                logging.debug(f"The list of enemies: {self.enemyList}")
    
    def look_at_player(self):        
        from main import player
        for self.rectImage in self.enemyList:
            mx, my = player.rot_image_rect.x , player.rot_image_rect.y
            dx, dy = mx - self.rectImage.centerx, my - self.rectImage.centery
            angle = math.degrees(math.atan2(-dy, dx)) - 0

            rot_image = pygame.transform.rotate(self.scaledImage, angle)
            self.rot_image_rect = rot_image.get_rect(center=self.rectImage.center)

            screen.blit(rot_image, self.rot_image_rect.topleft)