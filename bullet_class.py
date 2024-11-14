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

# Klasse voor de kogels
class Bullet:
    def __init__(self, velocity):
        self.velocity = velocity  # Snelheid van de kogel
        self.bulletIMG = pygame.image.load("graphics/bulletIMG.png").convert_alpha()  # Laad de kogelafbeelding
        self.scaledImage = pygame.transform.scale(self.bulletIMG, (45, 45))  # Schaal de afbeelding
        self.bulletList = []  # Lijst om actieve kogels bij te houden
        self.clip_size = 30  # Aantal kogels in het magazijn
        self.reload = False  # Indicatie voor herladen
        self.shoot = True  # Indicatie of de speler kan schieten
        self.lastReloadTime = 0  # Tijd van de laatste herlaadactie
        self.lastShootTime = 0  # Tijd van het laatste schot
        self.score = 0  # Score van de speler
        logging.info("Geïnitialiseerd bullet klasse!") 

    def update(self):
        """Update de positie van elke kogel en controleer of deze nog binnen het scherm is."""
        for bullet in self.bulletList:
            # Update positie gebaseerd op de hoek
            bullet['x'] += self.velocity * math.cos(bullet['angle'])
            bullet['y'] -= self.velocity * math.sin(bullet['angle'])
            bullet['rect'] = self.scaledImage.get_rect(center=(bullet['x'], bullet['y']))  # Update rect van de kogel

            # Verwijder de kogel als deze buiten het scherm is
            if (bullet['x'] < 0 or bullet['x'] > infoObject.current_w or
                bullet['y'] < 0 or bullet['y'] > infoObject.current_h):
                self.bulletList.remove(bullet)

    def shooting(self, player):
        """Logica voor het schieten, inclusief herladen en cooldown."""
        keys = pygame.key.get_pressed()

        # Controleer of de linkermuisknop is ingedrukt, er nog kogels zijn, en of schieten is toegestaan
        if pygame.mouse.get_pressed()[0] and self.clip_size > 0 and self.shoot:
            self.lastShootTime = pygame.time.get_ticks()  # Tijd van laatste schot vastleggen
            self.shoot = False  # Schieten tijdelijk uitschakelen (cooldown)

            self.clip_size -= 1  # Verlaag het aantal kogels in het magazijn

            # Bereken de positie en hoek voor de nieuwe kogel
            angle_rad = math.radians(player.angle)
            x = player.rot_image_rect.centerx + 26 * math.cos(angle_rad)
            y = player.rot_image_rect.centery - 9 * math.sin(angle_rad)

            # Voeg de nieuwe kogel toe aan de lijst
            bullet_rect = self.scaledImage.get_rect(center=(x, y))
            self.bulletList.append({'x': x, 'y': y, 'angle': angle_rad, 'rect': bullet_rect})

        # Cooldown logica voor het schieten
        if not self.shoot and pygame.time.get_ticks() - self.lastShootTime > 100:
            self.shoot = True

        # Controleer op herladen
        if keys[pygame.K_r] and not self.reload:
            self.lastReloadTime = pygame.time.get_ticks()  # Tijd van herladen vastleggen
            self.reload = True
            self.clip_size = 30  # Volledig magazijn herladen

        # Herladen voltooien na 1 seconde
        if self.reload and pygame.time.get_ticks() - self.lastReloadTime > 1000:
            self.reload = False

    def draw(self):
        """Teken alle actieve kogels op het scherm."""
        for bullet in self.bulletList:
            bullet['rect'] = self.scaledImage.get_rect(center=(bullet['x'], bullet['y']))
            screen.blit(self.scaledImage, bullet['rect'])

    def check_if_shot_enemy(self, enemy):
        """Controleer of een kogel een vijand raakt."""
        for bullet in self.bulletList:
            for enemy_data in enemy.enemyList:
                if bullet['rect'].colliderect(enemy_data['rect']):  # Controleer botsing
                    self.bulletList.remove(bullet)  # Verwijder de kogel bij een treffer
                    shotEnemy = pygame.mixer.Sound("graphics/enemyShot.mp3")
                    pygame.mixer.Sound.play(shotEnemy, 0)
                    enemy.enemyList.remove(enemy_data)  # Verwijder de vijand bij een treffer
                    self.score += 100  # Verhoog de score
                    break  # Stop met zoeken nadat een vijand geraakt is
