import pygame
from Tools.Button import Button
from Tools.Image import Image

# from Tools.pyvidplayer import Video


class GameStateManager:
    def __init__(self):
        self.states = {}
        self.current_state = None

    def add_state(self, state_name, state):
        self.states[state_name] = state

    def change_state(self, state_name):
        if state_name in self.states:
            self.current_state = self.states[state_name]

    def handle_events(self, event):
        if self.current_state:
            self.current_state.handle_events(event)

    def update(self):
        if self.current_state:
            self.current_state.update()

    def draw(self, surface):
        if self.current_state:
            self.current_state.draw(surface)


pygame.init()
pygame.mixer.init()


class IntroState:
    pass


class MainMenuState:
    def __init__(self, screen_width, screen_height, font, click_sound, btn_frame):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.click_sound = click_sound
        self.btn_frame = btn_frame
        self.buttons = [
            Button(
                (self.screen_width - 150) / 2,
                self.screen_height / 2,
                150,
                50,
                "Play",
                self.font,
                (0, 255, 0),
                (0, 200, 0),
                action=lambda: print("Button clicked!"),
                sound_click=self.click_sound,
                frame_image=self.btn_frame,
            ),
            Button(
                (self.screen_width - 150) / 2,
                self.screen_height / 2 + 80,
                150,
                50,
                "Setting",
                self.font,
                (31, 122, 136),
                (81, 122, 136),
                action=lambda: print("Button clicked!"),
                sound_click=self.click_sound,
                frame_image=self.btn_frame,
            ),
        ]

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    button.click()

    def update(self):
        for button in self.buttons:
            button.update(pygame.mouse.get_pos())

    def draw(self, surface):
        surface.fill((255, 255, 255))
        for button in self.buttons:
            button.draw(surface)


def main():
    WIDTH = 1200
    HEIGHT = 600
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("The Silent defender")

    FONT = pygame.font.Font("GameFiles/assets/ponts/phont.otf", 40)
    LOGO = "GameFiles/assets/images/Logo.png"
    BGS = "GameFiles/assets/sounds/MenuMusic.mp3"
    LOGO_WIDTH = WIDTH - (WIDTH / 4)
    x = (WIDTH - LOGO_WIDTH) // 2
    y = 30
    Click_sound = "GameFiles/assets/sounds/click_sound.mp3"
    btn_frame = "GameFiles/assets/images/btn_frame.png"
    pygame.mixer.music.load(BGS)
    pygame.mixer.music.play(-1)
    main_menu_state = MainMenuState(WIDTH, HEIGHT, FONT, Click_sound, btn_frame)
    logo = Image(LOGO, x, y)
    logo.resize(LOGO_WIDTH, 200)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            main_menu_state.handle_events(event)

        main_menu_state.update()

        WIN.fill((255, 255, 255))
        main_menu_state.draw(WIN)
        logo.draw(WIN)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
