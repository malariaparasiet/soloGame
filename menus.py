import pygame, logging, json, sys
from pygame.locals import *

# Initializing
pygame.init()
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s -  %(levelname)s - %(message)s")

# Krijg informatie over de monitor zodat je automatisch fullscreen wordt gezet
infoObject = pygame.display.Info()

clock = pygame.time.Clock()

# Maak class voor menus
class Menus(object):
    def __init__(self, screen, player, bullet, enemy):
        self.gameRunning = False
        self.mainMenuActive = True
        self.killedMenuActive = False
        self.screen = screen
        self.bgTxtClr = (0,0,0)
        self.bgTxtClr2 = (0,0,0)
        self.kilQtBgClr = (0,0,0)
        self.highscore = 0
        self.player = player
        self.bullet = bullet
        self.enemy = enemy

    def play_sound(self, sound_path):
        """Speel een geluid af als het pad geldig is."""
        try:
            sound = pygame.mixer.Sound(sound_path)
            pygame.mixer.Sound.play(sound, 0)
        except pygame.error:
            logging.error(f"Failed to load sound: {sound_path}")

    def reset_game_state(self, enemy, player, bullet):
        """Reset de game status naar de beginwaarden."""
        enemy.enemyList.clear()
        player.health = 100
        player.rectImage.x = infoObject.current_w / 2
        player.rectImage.y = infoObject.current_h / 2
        bullet.score = 0
        bullet.clip_size = 30
        logging.info("Game state has been reset.")

    def mainMenu(self):

        try:
            with open('./score.json', 'r') as f:
                data = json.load(f)
                self.highscore = data['max_score']
        except (json.JSONDecodeError, FileNotFoundError):
            # If the file is not found or there's an error parsing, create a new file with default values
            with open('score.json', 'w') as g:
                g.write("""
        {
            "max_score": 0
        }
                            """)

            data = {"max_score": 0}

        """Weergeef het hoofdmenu en reageer op de muisinteractie."""
        mainMenuBG_ogImg = pygame.image.load("graphics/mainMenuBG.png").convert()
        mainMenuBG_image = pygame.transform.scale(mainMenuBG_ogImg, (infoObject.current_w, infoObject.current_h))
        self.screen.blit(mainMenuBG_image, (0, 0))

        font = pygame.font.Font("graphics/AurulentSansMNerdFontPropo-Regular.otf", 30)

        mainMenu_Text1 = font.render('Welcome to my super cool game with zombies!!', False, (255, 255, 255))
        mainMenu_Text1Rect = mainMenu_Text1.get_rect(center=(infoObject.current_w / 2, infoObject.current_h / 2))
        self.screen.blit(mainMenu_Text1, mainMenu_Text1Rect)

        mainMenu_Text2 = font.render("Start gaming!", False, (255, 255, 255), self.bgTxtClr)
        mainMenu_Text2Rect = mainMenu_Text2.get_rect(center=(infoObject.current_w / 2, infoObject.current_h / 2 + 50))
        self.screen.blit(mainMenu_Text2, mainMenu_Text2Rect)

        mainMenu_Text4 = font.render("Quit gaming!", False, (255, 255, 255), self.bgTxtClr2)
        mainMenu_Text4Rect = mainMenu_Text4.get_rect(center=(infoObject.current_w / 2, infoObject.current_h / 2 + 100))
        self.screen.blit(mainMenu_Text4, mainMenu_Text4Rect)

        mainMenu_Text3 = font.render(f'Current highscore: {self.highscore}', False, (255, 255, 255))
        mainMenu_Text3Rect = mainMenu_Text3.get_rect(center=(infoObject.current_w / 2, infoObject.current_h / 2 - 50))
        self.screen.blit(mainMenu_Text3, mainMenu_Text3Rect)

        if mainMenu_Text2Rect.collidepoint(pygame.mouse.get_pos()):
            self.bgTxtClr = (120, 120, 120)
            if pygame.mouse.get_pressed()[0]:  # Left click
                logging.info("Starting the game!")
                self.play_sound("graphics/clickSound.mp3")
                self.play_sound("graphics/startGame.mp3")
                self.mainMenuActive = False
                self.gameRunning = True
        else:
            self.bgTxtClr = (0, 0, 0)

        if mainMenu_Text4Rect.collidepoint(pygame.mouse.get_pos()):
            self.bgTxtClr2 = (120, 120, 120)
            if pygame.mouse.get_pressed()[0]:  # Left click
                logging.info("Closing")
                pygame.quit()
                sys.exit()
        else:
            self.bgTxtClr2 = (0, 0, 0)

    def killedMenu(self, bullet):
        """Weergeef het 'killed' menu en reageer op de muisinteractie voor herstart."""
        killedMenuBG_ogImg = pygame.image.load("graphics/killedMenuBG.png").convert()
        killedMenuBG_image = pygame.transform.scale(killedMenuBG_ogImg, (infoObject.current_w, infoObject.current_h))
        self.screen.blit(killedMenuBG_image, (0, 0))

        font = pygame.font.Font("graphics/AurulentSansMNerdFontPropo-Regular.otf", 30)

        killedMenuText1 = font.render(f'You got killed :( Your score was: {bullet.score}', False, (255, 255, 255))
        killedMenu_Text1Rect = killedMenuText1.get_rect(center=(infoObject.current_w / 2, infoObject.current_h / 2))
        self.screen.blit(killedMenuText1, killedMenu_Text1Rect)

        killedMenu_Text2 = font.render("Restart your run!", False, (255, 255, 255), self.bgTxtClr)
        killedMenu_Text2Rect = killedMenu_Text2.get_rect(center=(infoObject.current_w / 2, infoObject.current_h / 2 + 50))
        self.screen.blit(killedMenu_Text2, killedMenu_Text2Rect)

        killedMenu_Text4 = font.render("Quit gaming!", False, (255, 255, 255), self.kilQtBgClr)
        killedMenu_Text4Rect = killedMenu_Text4.get_rect(center=(infoObject.current_w / 2, infoObject.current_h / 2 + 100))
        self.screen.blit(killedMenu_Text4, killedMenu_Text4Rect)

        highScore_Text3 = font.render(f'A NEW HIGHSCORE!!! YOUR HIGHSCORE: {bullet.score}', False, (255,255,255))
        highScore_Text3Rect =  highScore_Text3.get_rect(center=(infoObject.current_w / 2, infoObject.current_h / 2 - 50))

        data = None

        try:
            with open('./score.json', 'r') as f:
                data = json.load(f)
                self.highscore = data['max_score']
        except (json.JSONDecodeError, FileNotFoundError):
            # If the file is not found or there's an error parsing, create a new file with default values
            with open('score.json', 'w') as g:
                g.write("""
        {
            "max_score": 0
        }
                            """)

            data = {"max_score": 0}

        if data['max_score'] <= bullet.score:
            self.highscore = bullet.score
            self.screen.blit(highScore_Text3, highScore_Text3Rect)
            data['max_score'] = bullet.score

            # Save the updated score back to the file
            with open('./score.json', 'w') as f:
                json.dump(data, f, indent=4)


        if killedMenu_Text2Rect.collidepoint(pygame.mouse.get_pos()):
            self.bgTxtClr = (120, 120, 120)
            if pygame.mouse.get_pressed()[0]:  # Left click
                logging.info("Restarting the game!")
                self.play_sound("graphics/clickSound.mp3")
                self.play_sound("graphics/gameOver.mp3")
                self.reset_game_state(self.enemy, self.player, self.bullet)
                self.killedMenuActive = False
                self.gameRunning = True
        else:
            self.bgTxtClr = (0, 0, 0)

        if killedMenu_Text4Rect.collidepoint(pygame.mouse.get_pos()):
            self.kilQtBgClr = (120, 120, 120)
            logging.info("Colliding with killedMenu_Text4Rect and mouse!")
            if pygame.mouse.get_pressed()[0]:  # Left click
                logging.info("Closing")
                pygame.quit()
                sys.exit()
        else:
            self.kilQtBgClr = (0, 0, 0)