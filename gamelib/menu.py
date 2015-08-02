from constants import *

class Menu(object):
    def __init__(self, width, height):

        self.width = width
        self.height = height
        self.cursor_index = 0

        self.font = pygame.font.Font(FILES.get_path("fonts", "tinyfont.ttf"), 30)

        self.text_play = self.font.render("Play", True, WHITE)
        self.text_resume = self.font.render("Resume", True, WHITE)
        self.text_settings = self.font.render("Settings", True, WHITE)
        self.text_credits = self.font.render("Credits", True, WHITE)
        self.text_exit = self.font.render("Exit", True, WHITE)

        self.buttons_group = pygame.sprite.Group()

        self.assemble()

    def handleEvents(self, event):
        for button in self.buttons_group:
            button.handleEvents(event)

        if event.type == KEYDOWN:
            if event.key == K_s:
                self.cursor_index += 1
            elif event.key == K_w:
                self.cursor_index -= 1

        if self.cursor_index < 0:
            self.cursor_index = 0
        elif self.cursor_index > 3:
            self.cursor_index = 3

    def assemble(self):
        button = None
        for i in range(4): # 4 buttons
            x = self.width/2 - 150/2
            y = 180 + i*60 #(i*40) + (i*20)
            if i == 0:
                button = MenuButton(x, y, self.text_play, "game", "img")
            elif i == 1:
                button = MenuButton(x, y, self.text_settings, "settings", "img")
            elif i == 2:
                button = MenuButton(x, y, self.text_credits, "credits", "img")
            elif i == 3:
                button = MenuButton(x, y, self.text_exit, "exit", "img")
            self.buttons_group.add(button)

    def getActiveState(self):
        """ Returns the state of the active(clicked/hovered over) button"""
        for button in self.buttons_group:
            if button.active:
                return button.state
        return "menu"

    def addResumeButton(self):
        """Changes text on Play button to 'Resume' while the game is paused."""
        for button in self.buttons_group:
            if button.state == "game":
                button.text = self.text_resume

    def update(self):
        pass

class MenuButton(pygame.sprite.Sprite):
    def __init__(self, x, y, text, state, image):
        pygame.sprite.Sprite.__init__(self)
        self.active = False
        self.selected = False
        self.state = state
        self.image = pygame.Surface((150, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hover_image = self.get_surface(FILES.get_path("img", "button_hover.png"), 150, 40)
        self.inactive_image = self.get_surface(FILES.get_path("img", "button_inactive.png"), 150, 40)
        self.text = text

    def handleEvents(self, event):
        if event.type == MOUSEMOTION:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.image = self.hover_image
                self.active = True
            else:
                self.image = self.inactive_image
                self.active = False

    def get_surface(self, img, width, height):
        image = pygame.image.load(img)
        image = pygame.transform.smoothscale(image, (width, height))
        self.rect.width = image.get_rect().width
        self.rect.height = image.get_rect().height

        return image

    def center(self, text):
        textRect = text.get_rect()
        textRect.centerx = self.rect.centerx
        textRect.centery = self.rect.centery

        return textRect

    def makeActive(self, text):
        """ Makes the button active """
        self.text = self.font.render(text, True, GREEN)
        self.active = True

