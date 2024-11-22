import pygame, math, logging
from pygame.locals import *

# Initializing
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s -  %(levelname)s - %(message)s")

# Krijg informatie over de monitor zodat je automatisch fullscreen wordt gezet
infoObject = pygame.display.Info()

screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), HWSURFACE | DOUBLEBUF)

clock = pygame.time.Clock()

class Player(object):
    def __init__(self, speed, health):
        # Position player to middle & player variables
        self.x = infoObject.current_w / 2
        self.y = infoObject.current_h / 2
        self.speed = speed
        self.health = health
        self.correction_angle = 0
        self.rot_image_rect = None
        self.angle = None
        self.isKilled = False
        self.canTakeHit = True
        self.lastHitTime = 0

        # Image magic for scaling
        self.load_image("graphics/playerIMg.png")
        logging.info("Initialized player class!")

    def load_image(self, path):
        """Load and scale player image."""
        try:
            self.oldImage = pygame.image.load(path)
            self.scaledImage = pygame.transform.scale(self.oldImage, (63, 41))
            self.rectImage = self.scaledImage.get_rect(center=(self.x, self.y))
        except pygame.error:
            logging.error(f"Failed to load image: {path}")

    def play_sound(self, sound_path):
        """Play a sound."""
        try:
            sound = pygame.mixer.Sound(sound_path)
            pygame.mixer.Sound.play(sound, 0)
        except pygame.error:
            logging.error(f"Failed to load sound: {sound_path}")

    def movement(self):
        """Player movement based on keyboard input."""
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_d]:
            self.rectImage.centerx += self.speed
        if self.keys[pygame.K_a]:
            self.rectImage.centerx -= self.speed
        if self.keys[pygame.K_w]:
            self.rectImage.centery -= self.speed
        if self.keys[pygame.K_s]:
            self.rectImage.centery += self.speed

    def check_if_inside_boundary(self):
        """Ensure the player stays within screen boundaries."""
        self.rectImage.right = min(self.rectImage.right, infoObject.current_w)
        self.rectImage.left = max(self.rectImage.left, 0)
        self.rectImage.bottom = min(self.rectImage.bottom, infoObject.current_h)
        self.rectImage.top = max(self.rectImage.top, 0)

    def player_looks_at_mouse(self):
        """Make the player sprite look at the mouse position."""
        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - self.rectImage.centerx, my - self.rectImage.centery
        self.angle = math.degrees(math.atan2(-dy, dx)) - self.correction_angle

        # Rotate player sprite
        rot_image = pygame.transform.rotate(self.scaledImage, self.angle)
        self.rot_image_rect = rot_image.get_rect(center=self.rectImage.center)
        screen.blit(rot_image, self.rot_image_rect.topleft)

    def is_being_touched_by_enemy(self, enemy):
        """Check if player is being touched by an enemy and update health."""

        for enemy in enemy.enemyList:
            if enemy['rect'].colliderect(self.rot_image_rect) and self.health > 0 and self.canTakeHit:
                self.lastHitTime = pygame.time.get_ticks()
                self.canTakeHit = False
                self.play_sound("graphics/retroHurt.mp3")
                self.health -= 5

            # Ensure player can only be hit once every 750ms
            if not self.canTakeHit and pygame.time.get_ticks() - self.lastHitTime > 750:
                self.canTakeHit = True

            if self.health <= 0 and not self.isKilled:
                self.isKilled = True
                self.play_sound("graphics/gameOver.mp3")

