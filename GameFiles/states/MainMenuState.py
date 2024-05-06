import pygame
from Tools.Button import Button


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
                ((self.screen_width - 150) / 2) - 100,
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
                ((self.screen_width - 150) / 2) + 100,
                self.screen_height / 2 + 80,
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
                self.screen_height / 2 + 160,
                150,
                50,
                "Shop",
                self.font,
                (31, 122, 136),
                (81, 122, 136),
                action=lambda: self.game_state_manager.change_state("Shop"),
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
    def start(self):
        pass
    def end(self):
        pass
    
    def update(self, dt):
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
