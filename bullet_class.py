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
        self.bulletList = []
        self.clip_size = 30
        logging.info("Initialized bullet class!")

    def update(self):
        # Update the position of each bullet based on its angle
        for bullet in self.bulletList:
            bullet['x'] += self.velocity * math.cos(bullet['angle'])
            bullet['y'] -= self.velocity * math.sin(bullet['angle'])
            
            # Check if the bullet is off-screen
            if (bullet['x'] < 0 or bullet['x'] > infoObject.current_w or
                bullet['y'] < 0 or bullet['y'] > infoObject.current_h):
                self.bulletList.remove(bullet)  # Remove bullet if it is off-screen

    def shooting(self, player):
        self.keys = pygame.key.get_pressed()
        reload = False
        if pygame.mouse.get_pressed()[0] and pygame.time.get_ticks() % 4 == 0 and self.clip_size > 0:
            self.clip_size -= 1
            #Maak hier iets zodat de speler weet dat die moet reloaden
            self.keys = pygame.key.get_pressed()
            angle_rad = math.radians(player.angle)  # Ensure we're using radians
            # Calculate the spawn position based on the weapon's offset
            x = player.rot_image_rect.centerx + 26 * math.cos(angle_rad)
            y = player.rot_image_rect.centery - 9 * math.sin(angle_rad)

            # Add the new bullet to the list
            self.bulletList.append({'x': x, 'y': y, 'angle': angle_rad})
            logging.info(f"Bullet fired at: x: {x}, y: {y}")
        elif self.keys[pygame.K_r]:
            lastReloadTime = pygame.time.get_ticks()
            reload = True
            self.clip_size = 30
        if reload and pygame.time.get_ticks() - lastReloadTime > 1000:
            reload = False

    def draw(self):
        for bullet in self.bulletList:
            rectImage = self.scaledImage.get_rect(center=(bullet['x'], bullet['y']))
            screen.blit(self.scaledImage, rectImage)