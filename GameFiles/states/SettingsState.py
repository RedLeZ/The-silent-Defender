import pygame
from Tools.Button import Button
from Tools.VolumeSlider import VolumeSlider


class SettingsState:
    def __init__(
        self,
        screen_width,
        screen_height,
        font,
        music,
        click_sound,
        btn_frame,
        game_state_manager,
        logo,
        background_image,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.music = music
        self.click_sound = click_sound
        self.btn_frame = btn_frame
        self.game_state_manager = game_state_manager
        self.logo = logo
        self.music_status = True
        self.background_image = background_image
        self.volume = pygame.mixer.music.get_volume()
        self.current_volume = self.volume
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

        def update_volume(volume):
            self.current_volume = volume

        self.sound_control = VolumeSlider(
            (self.screen_width - 400) / 2,
            self.screen_height / 3 + 26.666666666666668,
            400,
            50,
            (200, 200, 200),
            (0, 0, 255),
            update_volume,
            self.btn_frame,
        )

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    button.click()

        self.sound_control.handle_event(event)

    def start(self):
        pass

    def end(self):
        pass

    def update(self, dt):
        pygame.mixer.music.set_volume(self.current_volume)
        for button in self.buttons:
            button.update(pygame.mouse.get_pos())

        self.sound_control.update()

    def draw(self, surface):
        self.background_image.draw(surface)
        self.logo.draw(surface)
        self.sound_control.draw(surface)

        for button in self.buttons:
            button.draw(surface)

    def toggle_music(self):
        self.music_status = not self.music_status
        if self.music_status:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        for button in self.buttons:
            if button.id is not None and button.id == "Music":
                button.text = f"Music {'On' if self.music_status else 'Off'}"
