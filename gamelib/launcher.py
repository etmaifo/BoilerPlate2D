import pygame
from pygame import *
from camera import *
from menu import *
from level import *
from background import *
try:
    import android
except ImportError:
    android = None


class Engine:
    def __init__(self, width=SCREEN.width, height=SCREEN.height):
        pygame.init()
        pygame.font.init()
        # pygame.mixer.init()

        self.width = width
        self.height = height
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.display.set_caption("Name of Game")
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.fpsClock = pygame.time.Clock()
        self.fps = 30
        self.ticks = 0

        self.state = "menu"
        self.stage = Stage()
        self.score = 0
        self.life = 3
        self.timer = 0
        self.font = pygame.font.Font(os.path.join("fonts", "tinyfont.ttf"), 16)
        self.font.set_bold(True)
        self.text = self.font.render("0000", True, (0, 0 ,0), (55, 25, 55))
        self.textRect = self.text.get_rect()
        self.textRect.y = 30

        self.camera = Camera(self.complex_camera, self.stage.level.width, self.stage.level.height)
        bg_img = FILES.get_path("img", "bg.png")
        self.bg = Bg(0, 0, self.width, self.height, bg_img)
        self.menu = Menu(self.width, self.height)

        self.display_rects = []
        for sprite in self.stage.level.entities:
            self.display_rects.append(sprite.rect)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_j:
                    if self.fps > 15:
                        self.fps = 15
                    else:
                        self.fps = 30
                if event.key == K_t:
                    pygame.image.save(self.screen, FILES.get_path("screenshots", "screen01.jpg"))

                if event.key == K_ESCAPE:
                    self.state = "menu"
                    self.menu.addResumeButton()

            if event.type == MOUSEBUTTONDOWN:
                self.state = self.menu.getActiveState()

            if self.state == "game":
                if self.stage.level.timer == 0:
                    self.stage.level.timer = pygame.time.get_ticks()/1000.0
                self.stage.level.player.handleEvents(event)

            elif self.state == "menu":
                self.menu.handleEvents(event)

            elif self.state == "exit":
                pygame.quit()
                sys.exit()

    def update(self):
        self.camera.update(self.stage.level.player)
        self.bg.update()

        if self.state == "menu":
            self.menu.update()
        elif self.state == "game":
            self.stage.level.update()
            self.stage.update()
            if self.stage.level.intro:
                self.timer = 0

            if self.ticks > self.fps:
                self.ticks = 0
                self.timer += 1
            else:
                self.ticks += 1

            self.text = self.font.render(str(self.timer), True, (150, 125 ,112))
            self.textRect = self.text.get_rect()
            self.textRect.centerx = self.screen.get_rect().centerx
            self.textRect.y = 10

    def draw(self):
        self.screen.fill((30, 30, 30))

        if self.state == "game":

            self.screen.blit(self.bg.image, self.screen.get_rect())
            for entity in self.stage.level.entities:
                self.screen.blit(entity.image, self.camera.apply(entity))
            self.screen.blit(self.text, self.textRect)

        elif self.state == "menu":
            for button in self.menu.buttons_group:
                self.screen.blit(button.image, (button.rect.x, button.rect.y))
                self.screen.blit(button.text, button.center(button.text))

    # Lifecycle starts here
    def runGame(self, fps=30):
        self.fps = fps
        while True:
            self.handleEvents()
            self.update()
            self.draw()

            pygame.display.update()
            pygame.display.set_caption("Platformer Template - " + str(int(self.fpsClock.get_fps()))+" FPS")
            self.fpsClock.tick(self.fps)

    def simple_camera(self, cameraRect, target_rect):
        x, y, dummy, dummy = target_rect
        dummy, dummy, w, h = cameraRect

        return pygame.Rect(int(self.width/2)-x, int(self.height/2)-y, w, h)

    def complex_camera(self, cameraRect, target_rect):
        x, y, dummy, dummy = target_rect
        dummy, dummy, w, h = cameraRect
        x, y  = int(self.width/2)-x, int(self.height/2) - y

        x = min(0, x)
        x = max(-(cameraRect.width-self.width), x)
        y = max(-(cameraRect.height-self.height), y)
        y = min(0, y)

        return pygame.Rect(x, y, w, h)
