import pygame, sys, math, random
from pygame.locals import *


#pygame initializing
pygame.init()

# Krijg informatie over de monitor zodat je automatisch fullscreen wordt gezet
infoObject = pygame.display.Info()

screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), HWSURFACE | DOUBLEBUF )
pygame.display.set_icon(pygame.image.load("graphics/playerIMG.png"))
pygame.display.set_caption("SoloGame Koen Veldkamp H5")
clock = pygame.time.Clock()

# Maak class voor achtergrond

class Background(object):
    def __init__(self):
        self.background_ogImg = pygame.image.load("graphics/backgroundIMG.png").convert()

        self.background_image = pygame.transform.scale(self.background_ogImg, (infoObject.current_w, infoObject.current_h))

    def draw(self):
        screen.blit(self.background_image, (0,0))

# Maak class voor bullets

class Bullet(object):
    def __init__(self, x, y, velocity, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.velocity = velocity

    def debugShooting(self):
        if pygame.mouse.get_pressed()[0]:
            pygame.draw.circle(screen, "red", (player.rot_image_rect.x, player.rot_image_rect.y), 5)

# Maak class voor player

class Player(object):
    def __init__(self, speed, health):

        #position player to middle & player variables
        self.x = infoObject.current_w / 2
        self.y = infoObject.current_h / 2
        self.speed = speed
        self.health = health
        self.correction_angle = 0

        #image magic because scaling n shi
        self.oldImage = pygame.image.load("graphics/playerIMg.png")
        self.scaledImage =  pygame.transform.scale(self.oldImage, (62.6, 41.4))
        self.rectImage = self.scaledImage.get_rect(center=(self.x, self.y))

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
        angle = math.degrees(math.atan2(-dy, dx)) - self.correction_angle

        # draaien
        rot_image = pygame.transform.rotate(self.scaledImage, angle)
        self.rot_image_rect = rot_image.get_rect(center=self.rectImage.center)

        screen.blit(rot_image, self.rot_image_rect.topleft)
  
# Maak class voor enemy

class Enemy(object):
    def __init__(self, health, spawnrate, speed):
        self.health = health
        self.spawnrate = spawnrate
        self.speed = speed
        self.oldImage = pygame.image.load("graphics/enemyIMG.png").convert_alpha()
        self.scaledImage = pygame.transform.scale(self.oldImage, (62.6, 41.4))
        self.enemyList = []

    def GenerateEnemy(self):
        # een modules operation voor om de spawnrate te bepalen en voor semi "random" spawntijden
        if pygame.time.get_ticks() % self.spawnrate == 0 and len(self.enemyList) < 10:
            
            # random positie krijgen om een enemy te spawnen
            self.posX = random.randint(0, 1280)
            self.posY = random.randint(0, 720)

            # debug
            print(f"Generating an enemy on {self.posX}, {self.posY}")

            # als die een enemy kan spawnen dan ook de rect aanmaken en toevoegen aan een lijst zodat de enemy op het scherm blijft
            self.rectImage = self.scaledImage.get_rect(center=(self.posX, self.posY))
            self.enemyList.append(self.rectImage)  # Voeg de nieuwe vijand toe aan de lijst

    def draw(self):
        # loopt over de lijst om de enemies elk frame gewoon te spawnen zodat ze blijven
        for self.rectImage in self.enemyList:
            screen.blit(self.scaledImage, self.rectImage)

# classes callen
background = Background()
bullet = Bullet(0,0,0,0)
player = Player(7.5, 100)
enemy = Enemy(100, 20, 10)


running = True
while running:
    background.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    player.checkIfInsideBoundry()
    player.playerLooksAtMouse()
    player.movement()

    enemy.GenerateEnemy()
    enemy.draw()

    bullet.debugShooting()

    pygame.display.flip()
    clock.tick(60)