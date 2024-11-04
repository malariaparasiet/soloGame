import pygame, sys, math, random, logging
from pygame.locals import *

# Initializing
pygame.init()
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s -  %(levelname)s - %(message)s")

# Get monitor information for full screen
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), HWSURFACE | DOUBLEBUF)

clock = pygame.time.Clock()

# Bullet class
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
            bullet['rect'] = self.scaledImage.get_rect(center=(bullet['x'], bullet['y']))  # Update bullet rect

            # Check if the bullet is off-screen
            if (bullet['x'] < 0 or bullet['x'] > infoObject.current_w or
                bullet['y'] < 0 or bullet['y'] > infoObject.current_h):
                self.bulletList.remove(bullet)  # Remove bullet if it is off-screen

    def shooting(self, player):
        keys = pygame.key.get_pressed()
        reload = False
        if pygame.mouse.get_pressed()[0] and pygame.time.get_ticks() % 4 == 0 and self.clip_size > 0:
            self.clip_size -= 1
            angle_rad = math.radians(player.angle)  # Ensure we're using radians
            x = player.rot_image_rect.centerx + 26 * math.cos(angle_rad)
            y = player.rot_image_rect.centery - 9 * math.sin(angle_rad)

            # Add the new bullet to the list with rect
            bullet_rect = self.scaledImage.get_rect(center=(x, y))
            self.bulletList.append({'x': x, 'y': y, 'angle': angle_rad, 'rect': bullet_rect})
            logging.info(f"Bullet fired at: x: {x}, y: {y}")
        elif keys[pygame.K_r]:
            lastReloadTime = pygame.time.get_ticks()
            reload = True
            self.clip_size = 30
        if reload and pygame.time.get_ticks() - lastReloadTime > 1000:
            reload = False

    def draw(self):
        for bullet in self.bulletList:
            bullet['rect'] = self.scaledImage.get_rect(center=(bullet['x'], bullet['y']))  # Update bullet rect
            screen.blit(self.scaledImage, bullet['rect'])

    def check_if_shot_enemy(self, enemy):
        for bullet in self.bulletList:
            for enemy_data in enemy.enemyList:  # Iterate over each enemy dictionary in enemyList
                if bullet['rect'].colliderect(enemy_data['rect']):
                    self.bulletList.remove(bullet)  # Remove the bullet if it hits an enemy
                    enemy.enemyList.remove(enemy_data)  # Remove the enemy if it’s hit
                    break  # Exit inner loop once the bullet has been removed
