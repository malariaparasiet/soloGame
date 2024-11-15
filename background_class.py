import pygame
import sys
import math
import random
import logging
from pygame.locals import *

# Initialiseer Pygame en stel logging in
pygame.init()
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s -  %(levelname)s - %(message)s")

# Krijg informatie over de monitor om automatisch fullscreen te activeren
infoObject = pygame.display.Info()

# Stel het scherm in op fullscreen
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), HWSURFACE | DOUBLEBUF)

clock = pygame.time.Clock()

# Klasse voor het weergeven van de achtergrond
class Background:
    def __init__(self):
        # Laad de originele achtergrondafbeelding en schaal deze naar de schermgrootte
        self.background_ogImg = pygame.image.load("graphics/backgroundIMG.png").convert()
        self.background_image = pygame.transform.scale(
            self.background_ogImg, (infoObject.current_w, infoObject.current_h)
        )
        logging.info("Achtergrondklasse geïnitialiseerd!")  # Log dat de achtergrond succesvol is geïnitialiseerd

    def draw(self):
        screen.blit(self.background_image, (0, 0))  # Plaatst de afbeelding op (0, 0) zodat deze het hele scherm vult
