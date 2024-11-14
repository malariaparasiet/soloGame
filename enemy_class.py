import pygame
import sys
import math
import random
import logging
from pygame.locals import *

# Initialiseer Pygame en stel logging in
pygame.init()
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s -  %(levelname)s - %(message)s")

# Verkrijg informatie over de monitor voor automatisch fullscreen
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), HWSURFACE | DOUBLEBUF)

clock = pygame.time.Clock()

class Enemy:
    def __init__(self, health, spawnrate, speed):
        # Initialiseer eigenschappen van de vijand
        self.health = health  # Gezondheid van de vijand
        self.spawnrate = spawnrate  # Spawnrate bepaalt hoe vaak vijanden verschijnen
        self.speed = speed  # Snelheid waarmee de vijanden bewegen
        self.oldImage = pygame.image.load("graphics/enemyIMG.png").convert_alpha()  # Laad de vijand afbeelding
        self.scaledImage = pygame.transform.scale(self.oldImage, (63, 41))  # Schaal de afbeelding
        self.enemyList = []  # Lijst met actieve vijanden
        logging.info("Geïnitialiseerd enemy klasse!")

    def GenerateEnemy(self):
        """Genereer vijanden op willekeurige locaties."""
        # Willekeurige spawnlogica: de vijand spawnt alleen als een bepaalde kans gehaald wordt
        if random.randint(1, 5) == random.randint(1, 5) and len(self.enemyList) <= 35:
            posX = random.randint(0, infoObject.current_w)
            posY = random.randint(0, infoObject.current_h)
            
            # Maak een rect voor de vijand en voeg het toe aan de lijst
            rectImage = self.scaledImage.get_rect(center=(posX, posY))
            self.enemyList.append({'rect': rectImage, 'health': self.health})  # Vijand heeft eigen rect en gezondheid

    def move_towards_player(self, player):
        """Beweeg vijanden in de richting van de speler."""
        for enemy in self.enemyList:
            rect = enemy['rect']
            # Bereken de richting naar de speler
            dx, dy = player.rot_image_rect.x - rect.x, player.rot_image_rect.y - rect.y
            dist = math.hypot(dx, dy)  # Bereken de afstand tot de speler
            if dist != 0:
                dx, dy = dx / dist, dy / dist  # Normaliseer de vector
            else:
                continue  # Als de afstand 0 is, beweeg niet

            # Beweeg de vijand met de gespecificeerde snelheid in de richting van de speler
            rect.x += dx * self.speed
            rect.y += dy * self.speed

    # Methode om te controleren of de vijand de speler raakt (momenteel uitgeschakeld)
    # def check_if_shot(self, player):
    #     for enemy in self.enemyList:
    #         if enemy['rect'].colliderect(player.rot_image_rect):
    #             logging.debug(f"Collision detected between player and enemy at {enemy['rect'].topleft}")

    def look_at_player(self, player):
        """Laat de vijand naar de speler kijken door de afbeelding te roteren."""
        for enemy in self.enemyList:
            rect = enemy['rect']
            # Bereken de richting naar de speler om de rotatiehoek te bepalen
            mx, my = player.rot_image_rect.x, player.rot_image_rect.y
            dx, dy = mx - rect.centerx, my - rect.centery
            angle = math.degrees(math.atan2(-dy, dx))  # Bereken de rotatiehoek

            # Draai de afbeelding en positioneer deze
            rot_image = pygame.transform.rotate(self.scaledImage, angle)
            rot_image_rect = rot_image.get_rect(center=rect.center)
            screen.blit(rot_image, rot_image_rect.topleft)  # Teken de geroteerde afbeelding
