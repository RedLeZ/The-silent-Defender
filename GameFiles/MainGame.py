import pygame
from Tools.Button import Button
from Tools.Image import Image


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


class MainMenuState:
    def __init__(
        self,
        screen_width,
        screen_height,
        font,
        click_sound,
        btn_frame,
        game_state_manager,
        logo,
        background_image,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.click_sound = click_sound
        self.btn_frame = btn_frame
        self.game_state_manager = game_state_manager
        self.logo = logo
        self.background_image = background_image

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
                action=self.play_button_clicked,
                sound_click=self.click_sound,
                frame_image=self.btn_frame,
            ),
            Button(
                (self.screen_width - 150) / 2,
                self.screen_height / 2 + 80,
                150,
                50,
                "Settings",
                self.font,
                (31, 122, 136),
                (81, 122, 136),
                action=lambda: self.game_state_manager.change_state("Settings"),
                sound_click=self.click_sound,
                frame_image=self.btn_frame,
            ),
            Button(
                (self.screen_width - 150) / 2,
                self.screen_height / 2 + 160,
                150,
                50,
                "Credits",
                self.font,
                (31, 122, 136),
                (81, 122, 136),
                action=self.credits_button_clicked,
                sound_click=self.click_sound,
                frame_image=self.btn_frame,
            ),
            Button(
                (self.screen_width - 150) / 2,
                self.screen_height / 2 + 240,
                150,
                50,
                "Quit",
                self.font,
                (255, 0, 0),
                (200, 0, 0),
                action=self.quit_button_clicked,
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
        self.background_image.draw(surface)

        self.logo.draw(surface)
        for button in self.buttons:
            button.draw(surface)

    def play_button_clicked(self):
        self.game_state_manager.change_state("Levels")

    def credits_button_clicked(self):
        self.game_state_manager.change_state("Credits")

    def quit_button_clicked(self):
        pygame.quit()
        exit()


class SettingsState:
    def __init__(
        self,
        screen_width,
        screen_height,
        font,
        click_sound,
        btn_frame,
        game_state_manager,
        logo,
        background_image,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.click_sound = click_sound
        self.btn_frame = btn_frame
        self.game_state_manager = game_state_manager
        self.logo = logo
        self.music_status = True
        self.background_image = background_image

        self.buttons = [
            Button(
                (self.screen_width - 150) / 2,
                self.screen_height / 2,
                150,
                50,
                f"Music {'On' if self.music_status else 'Off'}",
                self.font,
                (0, 255, 0),
                (0, 200, 0),
                action=self.toggle_music,
                sound_click=self.click_sound,
                frame_image=self.btn_frame,
                id="Music",
            ),
            Button(
                (self.screen_width - 150) / 2,
                self.screen_height / 2 + 80,
                150,
                50,
                "Back",
                self.font,
                (31, 122, 136),
                (81, 122, 136),
                action=lambda: self.game_state_manager.change_state("MainMenu"),
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
        self.background_image.draw(surface)
        self.logo.draw(surface)
        for button in self.buttons:
            button.draw(surface)

    def toggle_music(self):
        self.music_status = not self.music_status
        pygame.mixer.music.set_volume(1 if self.music_status else 0)
        for button in self.buttons:
            if button.id is not None and button.id == "Music":
                button.text = f"Music {'On' if self.music_status else 'Off'}"


class CreditsState:
    def __init__(
        self,
        screen_width,
        screen_height,
        font,
        click_sound,
        btn_frame,
        game_state_manager,
        logo,
        background_image,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.click_sound = click_sound
        self.btn_frame = btn_frame
        self.game_state_manager = game_state_manager
        self.logo = logo
        self.background_image = background_image

        self.buttons = [
            Button(
                (self.screen_width - 150) / 2,
                self.screen_height - 100,
                150,
                50,
                "Back",
                self.font,
                (31, 122, 136),
                (81, 122, 136),
                action=self.back_button_clicked,
                sound_click=self.click_sound,
                frame_image=self.btn_frame,
            ),
        ]

        self.credit_texts = [
            "Game developed by Redlez",
            "Thanks To :",
            "Upklyat(Buttons Frames, Dialogue Background)",
            "universfield(Buttons Click Sound)",
            "nojisuma(BackGround Music)",
            "limitype(Font)",
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
        self.background_image.draw(surface)
        self.logo.draw(surface)
        y_offset = 200
        for text in self.credit_texts:
            credit_text = self.font.render(text, True, (0, 0, 0))
            surface.blit(
                credit_text,
                ((self.screen_width - credit_text.get_width()) // 2, y_offset),
            )
            y_offset += credit_text.get_height() + 20
        for button in self.buttons:
            button.draw(surface)

    def back_button_clicked(self):
        self.game_state_manager.change_state("MainMenu")


class LevelState:
    def __init__(
        self,
        screen_width,
        screen_height,
        font,
        click_sound,
        btn_frame,
        game_state_manager,
        logo,
        background_image,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.click_sound = click_sound
        self.btn_frame = btn_frame
        self.game_state_manager = game_state_manager
        self.logo = logo
        self.background_image = background_image

        button_width = 250
        button_height = 50
        button_spacing = 40
        button_x = (self.screen_width - button_width) / 4
        button_y = (self.screen_height - button_height) - 400

        self.buttons = [
            Button(
                button_x,
                button_y,
                button_width,
                button_height,
                "Endless Mode",
                self.font,
                (31, 122, 136),
                (81, 122, 136),
                action=self.endless_mode_clicked,
                sound_click=self.click_sound,
                frame_image=self.btn_frame,
            ),
            Button(
                button_x + button_width + button_spacing,
                button_y,
                button_width,
                button_height,
                "First Stage",
                self.font,
                (31, 122, 136),
                (81, 122, 136),
                action=self.first_stage_clicked,
                sound_click=self.click_sound,
                frame_image=self.btn_frame,
            ),
            Button(
                (self.screen_width - button_width) / 2,
                self.screen_height - button_height - 40,
                button_width,
                button_height,
                "Back",
                self.font,
                (31, 122, 136),
                (81, 122, 136),
                action=self.back_button_clicked,
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
        self.background_image.draw(surface)
        self.logo.draw(surface)
        for button in self.buttons:
            button.draw(surface)

    def endless_mode_clicked(self):
        # Navigate to Endless Mode
        pass

    def first_stage_clicked(self):
        # Navigate to First Stage
        pass

    def back_button_clicked(self):
        self.game_state_manager.change_state("MainMenu")


def main():
    pygame.init()
    WIDTH = 1200
    HEIGHT = 700
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("The Silent Defender")

    FONT = pygame.font.Font("GameFiles/assets/fonts/font.otf", 40)
    Click_sound = "GameFiles/assets/sounds/click_sound.mp3"
    btn_frame = "GameFiles/assets/images/btn_frame.png"
    LOGO = "GameFiles/assets/images/Logo.png"
    MBG = "GameFiles/assets/images/background_image.png"
    LOGO_WIDTH = WIDTH - (WIDTH // 4)
    logo_x = (WIDTH - LOGO_WIDTH) // 2
    logo_y = 30

    game_state_manager = GameStateManager()
    logo = Image(LOGO, logo_x, logo_y)
    logo.resize(LOGO_WIDTH, 200)
    mainBg = Image(MBG, 0, 0)

    main_menu_state = MainMenuState(
        WIDTH, HEIGHT, FONT, Click_sound, btn_frame, game_state_manager, logo, mainBg
    )
    settings_state = SettingsState(
        WIDTH, HEIGHT, FONT, Click_sound, btn_frame, game_state_manager, logo, mainBg
    )
    credits_state = CreditsState(
        WIDTH, HEIGHT, FONT, Click_sound, btn_frame, game_state_manager, logo, mainBg
    )
    level_state = LevelState(
        WIDTH,
        HEIGHT,
        FONT,
        Click_sound,
        btn_frame,
        game_state_manager,
        logo,
        mainBg,
    )

    game_state_manager.add_state("MainMenu", main_menu_state)
    game_state_manager.add_state("Settings", settings_state)
    game_state_manager.add_state("Credits", credits_state)
    game_state_manager.add_state("Levels", level_state)
    game_state_manager.change_state("MainMenu")

    clock = pygame.time.Clock()
    pygame.mixer.music.load("GameFiles/assets/sounds/MenuMusic.mp3")
    pygame.mixer.music.play(-1)
    running = True
    while running:
        for event in pygame.event.get():
            game_state_manager.handle_events(event)

        game_state_manager.update()

        WIN.fill((255, 255, 255))
        game_state_manager.draw(WIN)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
