import pygame
import json
from Tools.Button import Button
import os


class GameOverState:
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

        self.stats_file = "GameFiles/assets/data/private/playerstats.json"
        button_width = 250
        button_height = 50

        self.buttons = [
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
        if not os.path.exists(self.stats_file):
            data = {
                "coins": 0,
                "lastScore": 0,
                "maxScore": 0,
                "LastTimeSurvived": 0,
                "MaxTimeSurvived": 0,
            }
            with open(self.stats_file, "w") as file:
                json.dump(data, file)

    def start(self):
        # Load player stats from JSON file
        with open(self.stats_file) as file:
            self.data = json.load(file)
            self.Coingained = int(self.data["lastScore"] / 3)
            self.score = self.data["lastScore"]
            self.time = self.data["LastTimeSurvived"]
            self.maxTime = self.data["MaxTimeSurvived"]

        # Initialize text
        self.coin_text = self.font.render(
            f"Coins gained: {self.Coingained}", True, (0, 0, 0)
        )
        self.time_text = self.font.render(
            f"Time Survived: {self.time}", True, (0, 0, 0)
        )
        self.max_time_text = self.font.render(
            f"Best Time Survived: {self.maxTime}", True, (0, 0, 0)
        )
        self.score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.max_score_etxt = self.font.render(
            f"Best Score: {self.data['maxScore']}", True, (0, 0, 0)
        )

    def end(self):
        # Reset any state-specific variables if needed
        pass

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    button.click()

    def update(self, dt):
        for button in self.buttons:
            button.update(pygame.mouse.get_pos())

    def draw(self, surface):
        self.background_image.draw(surface)
        self.logo.draw(surface)
        for button in self.buttons:
            button.draw(surface)

        surface.blit(
            self.coin_text, ((self.screen_width / 3) - 120, self.screen_height / 4)
        )
        surface.blit(
            self.score_text, ((self.screen_width / 3) + 120, self.screen_height / 4)
        )
        surface.blit(
            self.time_text, ((self.screen_width / 3) + 240, self.screen_height / 4)
        )
        surface.blit(
            self.max_time_text, ((self.screen_width / 3) + 30, self.screen_height / 2)
        )
        surface.blit(
            self.max_score_etxt,
            ((self.screen_width / 3) + 30, (self.screen_height / 2) + 40),
        )

    def back_button_clicked(self):
        self.game_state_manager.change_state("Levels")
