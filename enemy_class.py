import pygame, sys, math, random, logging
from pygame.locals import *

# Initializing
pygame.init()
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s -  %(levelname)s - %(message)s")

# Get monitor information for full screen
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), HWSURFACE | DOUBLEBUF)

clock = pygame.time.Clock()

class Enemy(object):
    def __init__(self, health, spawnrate, speed):
        self.health = health
        self.spawnrate = spawnrate
        self.speed = speed
        self.oldImage = pygame.image.load("graphics/enemyIMG.png").convert_alpha()
        self.scaledImage = pygame.transform.scale(self.oldImage, (63, 41))
        self.enemyList = []  # Each entry will be a dict representing an enemy
        logging.info("Initialized enemy class!")

    def GenerateEnemy(self):
        # Randomly spawn an enemy based on spawn rate and list size
        if random.randint(1,5) == random.randint(1,5) and len(self.enemyList) <= 35:
            posX = random.randint(0, infoObject.current_w)
            posY = random.randint(0, infoObject.current_h)

            # Debugging spawn position
            # logging.debug(f"Generating an enemy at position ({posX}, {posY})")

            # Create a new enemy dictionary with position and rect
            rectImage = self.scaledImage.get_rect(center=(posX, posY))
            self.enemyList.append({'rect': rectImage, 'health': self.health})  # Each enemy has its own rect and health

    def move_towards_player(self, player):
        for enemy in self.enemyList:
            rect = enemy['rect']
            # Direction vector to player
            dx, dy = player.rot_image_rect.x - rect.x, player.rot_image_rect.y - rect.y
            dist = math.hypot(dx, dy)
            if dist != 0:
                dx, dy = dx / dist, dy / dist
            else:
                continue
            # Move towards player with specified speed
            rect.x += dx * self.speed
            rect.y += dy * self.speed

    # def check_if_shot(self, player):
    #     for enemy in self.enemyList:
    #         if enemy['rect'].colliderect(player.rot_image_rect):
    #             logging.debug(f"Collision detected between player and enemy at {enemy['rect'].topleft}")

    def look_at_player(self, player):
        for enemy in self.enemyList:
            rect = enemy['rect']
            # Get direction vector to player for rotation
            mx, my = player.rot_image_rect.x, player.rot_image_rect.y
            dx, dy = mx - rect.centerx, my - rect.centery
            angle = math.degrees(math.atan2(-dy, dx))

            # Rotate and blit the image to face the player
            rot_image = pygame.transform.rotate(self.scaledImage, angle)
            rot_image_rect = rot_image.get_rect(center=rect.center)
            screen.blit(rot_image, rot_image_rect.topleft)
