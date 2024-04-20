import pygame
import random
from Tools.Button import Button
from Tools.Image import Image
from Tools.Projectiles import Projectile
from Tools.SoundBar import VolumeSlider


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

    def update(self):
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
        self.game_state_manager.change_state("Endless")
        pass

    def first_stage_clicked(self):
        # Navigate to First Stage (one Day)
        pass

    def back_button_clicked(self):
        self.game_state_manager.change_state("MainMenu")


class EndlessModState:
    def __init__(self, screen_width, screen_height, font, gsm):
        self.screen_width = screen_width
        self.game_state_manager = gsm
        self.screen_height = screen_height
        self.font = font
        self.hearts = 3
        self.wave = 1
        self.player_x = screen_width / 2
        self.player_y = screen_height / 2
        self.player_size = 50
        self.p_zone_size = 325
        self.p_zone_x = self.player_x - self.p_zone_size / 2
        self.p_zone_y = self.player_y - self.p_zone_size / 2
        self.player = pygame.Rect(
            self.player_x, self.player_y, self.player_size, self.player_size
        )

        self.p_zone = pygame.Rect(
            self.p_zone_x, self.p_zone_y, self.p_zone_size, self.p_zone_size
        )
        self.click_sound = pygame.mixer.Sound("GameFiles/assets/sounds/pop.mp3")
        self.enemy_size = 50
        self.enemy_speed = 2
        self.enemy_color = (255, 0, 0)
        self.enemies = []
        self.score = 0
        self.fade_duration = 3000
        self.total_duration = 6000
        self.start_time = pygame.time.get_ticks()
        self.wave_title = self.font.render(f"Wave: {self.wave}", True, (0, 0, 0))
        self.wave_rect = self.wave_title.get_rect(
            center=(screen_width // 2, screen_height // 2)
        )
        self.spawn_timer = 0
        self.wave_timer = 0
        self.spawn_interval = 200
        self.wave_interval = 720
        self.projectiles_per_spawn = 3

    def spawn_enemy(self):
        for _ in range(self.projectiles_per_spawn):
            enemy_x = random.randint(10, self.screen_width - 10)
            enemy_y = random.randint(10, self.screen_height - 10)
            while (
                enemy_x < self.player_x + self.p_zone_size / 2
                and enemy_x > self.player_x - self.p_zone_size / 2
                and enemy_y < self.player_y + self.p_zone_size / 2
            ):
                enemy_y = random.randint(10, self.screen_height - 10)
                enemy_x = random.randint(10, self.screen_width - 10)
            enemy = Projectile(
                enemy_x,
                enemy_y,
                self.player_x,
                self.player_y,
                self.enemy_speed,
                self.enemy_size,
                self.enemy_color,
                None,
            )
            self.enemies.append(enemy)

    def mouse_hit_enemy(self):
        self.score += 1

    def on_player_hit(self):
        self.hearts -= 1
        if self.hearts <= 0:
            self.game_state_manager.change_state("MainMenu")
            self.hearts = 3
            self.score = 0

    def update(self):

        self.spawn_timer += 1
        self.wave_timer += 1

        if self.spawn_timer >= self.spawn_interval:
            self.spawn_enemy()
            self.spawn_timer = 0

        if self.wave_timer >= self.wave_interval:
            self.wave += 1

            self.wave_timer = 0
        for enemy in self.enemies:
            if self.player.collidepoint((enemy.x, enemy.y)):
                self.enemies.remove(enemy)
                self.on_player_hit()

            enemy.update()

    def draw(self, surface):
        score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        surface.blit(score_text, (10, 10))
        wave_text = self.font.render(f"Wave: {self.wave}", True, (0, 0, 0))
        surface.blit(wave_text, (10, 50))

        heart_x = self.screen_width - 30
        heart_y = 10
        heart_image = pygame.image.load("GameFiles/assets/images/hrt.png")
        heart_image = pygame.transform.scale(heart_image, (20, 20))
        for i in range(self.hearts):
            surface.blit(heart_image, (heart_x, heart_y))
            heart_x -= 30
        pygame.draw.rect(surface, pygame.Color(255, 255, 255, 120), self.p_zone)
        pygame.draw.rect(surface, (0, 255, 0), self.player)

        for enemy in self.enemies:
            enemy.draw(surface)

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for enemy in self.enemies:
                if enemy.check_for_mouse_hit():
                    enemy.hit_n -= 1
                    if enemy.hit_n == 0:
                        self.score += 1
                        pygame.mixer.Sound(self.click_sound).play()
                        self.enemies.remove(enemy)


class FirstStageState:
    def __init__(self):
        pass


def main():
    pygame.init()
    WIDTH = 1200
    HEIGHT = 700
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("The Silent Defender")

    FONT = pygame.font.Font("GameFiles/assets/fonts/font.otf", 40)
    FONT2 = pygame.font.Font("GameFiles/assets/fonts/font2.otf", 40)
    Click_sound = "GameFiles/assets/sounds/click_sound.mp3"
    btn_frame = "GameFiles/assets/images/btn_frame.png"
    LOGO = "GameFiles/assets/images/Logo.png"
    MBG = "GameFiles/assets/images/background_image.png"
    SNG = "GameFiles/assets/sounds/MenuMusic.mp3"
    pygame.mixer.music.load(SNG)
    pygame.mixer.music.play(-1)
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
        WIDTH,
        HEIGHT,
        FONT,
        SNG,
        Click_sound,
        btn_frame,
        game_state_manager,
        logo,
        mainBg,
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
    endlessmod_state = EndlessModState(
        WIDTH,
        HEIGHT,
        FONT2,
        game_state_manager,
    )

    game_state_manager.add_state("MainMenu", main_menu_state)
    game_state_manager.add_state("Settings", settings_state)
    game_state_manager.add_state("Credits", credits_state)
    game_state_manager.add_state("Levels", level_state)
    game_state_manager.add_state("Endless", endlessmod_state)
    game_state_manager.change_state("MainMenu")

    clock = pygame.time.Clock()

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
