import pygame
from Tools.Button import Button


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
            "Hiba-San (MC images)",
            "universfield(Buttons Click Sound)",
            "nojisuma(BackGround Music)",
            "limitype, Hello Baby(Font)",
        ]

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
        y_offset = 170
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
