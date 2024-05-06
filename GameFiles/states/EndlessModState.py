import pygame
import random
import json
import os
from Tools.Projectiles import Projectile
from Tools.DialogueBox import DialogueBox
from Tools.Particles import ParticlePool


class EndlessModState:
    def __init__(
        self,
        screen_width,
        screen_height,
        font,
        gsm,
    ):
        self.screen_width = screen_width
        self.game_state_manager = gsm
        self.screen_height = screen_height
        self.particle_system = ParticlePool(30)
        self.font = font
        self.hearts = 3
        self.wave = 1
        self.paused = False
        self.player_x = screen_width / 2
        self.player_y = screen_height / 2
        self.player_size = 50
        self.p_zone_size = 325
        self.p_zone_x = self.player_x - self.p_zone_size / 2
        self.p_zone_y = self.player_y - self.p_zone_size / 2
        self.dialogue_box = DialogueBox(self.screen_width, self.screen_height)
        self.dialogue_box.add_dialogue(
            "Welcome to the Endless Mod...",
            "GameFiles/assets/images/narrator.png",
            "Narrator",
        )
        self.dialogue_box.add_dialogue(
            "Try Helping That boy to survive for a bit....",
            "GameFiles/assets/images/narrator.png",
            "Narrator",
        )
        self.dialogue_box.add_dialogue(
            "Good Luck...",
            "GameFiles/assets/images/narrator.png",
            "Narrator",
        )
        self.player = pygame.Rect(
            self.player_x, self.player_y, self.player_size, self.player_size
        )

        self.p_zone = pygame.Rect(
            self.p_zone_x, self.p_zone_y, self.p_zone_size, self.p_zone_size
        )
        self.click_sound = pygame.mixer.Sound("GameFiles/assets/sounds/pop.mp3")
        self.enemy_size = 50
        self.enemy_speed = 100
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
        self.spawn_interval = 5
        self.wave_interval = 60
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
        if self.hearts == 0:
            self.end()

    def start(self):
        self.start_time = pygame.time.get_ticks()
        self.elapsed_time = 0
        self.hearts = 3
        self.score = 0
        self.enemies = []
        print("Start method called, start_time set to", self.start_time)

    def end(self):
        self.update_playerStates()
        self.game_state_manager.change_state("GameOver")

    def update(self, dt):
        if self.paused == False:
            self.elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
            print("Update method called, elapsed_time set to", self.elapsed_time)

            self.spawn_timer += dt
            self.wave_timer += dt

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

                enemy.update(dt)

    def draw(self, surface):
        self.total_seconds = int(self.elapsed_time)
        self.hours = self.total_seconds // 3600
        self.minutes = (self.total_seconds % 3600) // 60
        self.seconds = self.total_seconds % 60
        self.milliseconds = int((self.elapsed_time - self.total_seconds) * 1000)

        score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        surface.blit(score_text, (10, 10))
        wave_text = self.font.render(f"Wave: {self.wave}", True, (0, 0, 0))
        surface.blit(wave_text, (10, 50))
        time_str = f"{self.hours:02}:{self.minutes:02}:{self.seconds:02}.{self.milliseconds:03}"
        timer_text = self.font.render(time_str, True, (0, 0, 0))
        surface.blit(timer_text, ((self.screen_width / 2) - 30, 10))

        heart_x = self.screen_width - 30
        heart_y = 10
        heart_image = pygame.image.load("GameFiles/assets/images/hrt.png")
        heart_image = pygame.transform.scale(heart_image, (20, 20))
        for i in range(self.hearts):
            surface.blit(heart_image, (heart_x, heart_y))
            heart_x -= 30
        pygame.draw.rect(surface, pygame.Color(255, 255, 255, 120), self.p_zone)
        if self.hearts == 3:
            player_image = pygame.image.load("GameFiles/assets/images/Player_happy.png")
        elif self.hearts == 2:
            player_image = pygame.image.load(
                "GameFiles/assets/images/Player_neutral.png"
            )
        else:
            player_image = pygame.image.load("GameFiles/assets/images/Player_sad.png")
        player_image = pygame.transform.scale(
            player_image, (self.player_size, self.player_size)
        )
        surface.blit(player_image, (self.player_x, self.player_y))

        for enemy in self.enemies:
            enemy.draw(surface)
        self.dialogue_box.render_text(surface)
        self.particle_system.update(surface)

        if self.paused == True:
            pygame.draw.rect(
                surface,
                (0, 0, 0),
                pygame.Rect(
                    surface.get_width() // 2 - 50,
                    surface.get_height() // 2 - 25,
                    100,
                    50,
                ),
            )
            pause_font = pygame.font.Font(None, 24)
            pause_text = pause_font.render("Paused", True, (255, 255, 255))

            surface.blit(
                pause_text,
                (
                    surface.get_width() // 2 - pause_text.get_width() // 2,
                    surface.get_height() // 2 - pause_text.get_height() // 2,
                ),
            )

    def handle_events(self, event):
        self.dialogue_box.update()
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
        if (
            self.dialogue_box.check_for_mouse_hit()
            and event.type == pygame.MOUSEBUTTONUP
        ):
            self.dialogue_box.next_dialogue()
        if self.paused == False:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for enemy in self.enemies:
                    if enemy.check_for_mouse_hit():
                        enemy.hit_n -= 1
                        if enemy.hit_n == 0:
                            self.score += 1
                            pygame.mixer.Sound(self.click_sound).play()
                            for _ in range(random.randint(10, 30)):
                                self.particle_system.add_particle(enemy.x, enemy.y)

                            self.enemies.remove(enemy)

    def update_playerStates(self):
        print("update_playerStates called, elapsed_time is", self.elapsed_time)
        try:
            # Check if file is empty or doesn't exist
            if (
                not os.path.exists("GameFiles/assets/data/private/playerstats.json")
                or os.path.getsize("GameFiles/assets/data/private/playerstats.json")
                == 0
            ):
                data = {
                    "coins": 0,
                    "lastScore": 0,
                    "maxScore": 0,
                    "LastTimeSurvived": 0,
                    "MaxTimeSurvived": 0,
                }
            else:
                # Read player stats
                with open(
                    "GameFiles/assets/data/private/playerstats.json", "r"
                ) as file:
                    data = json.load(file)

            # Update player stats
            data["coins"] += int(self.score / 3)
            data["lastScore"] = self.score
            data["LastTimeSurvived"] = self.elapsed_time
            data["maxScore"] = max(self.score, data["maxScore"])
            data["MaxTimeSurvived"] = max(self.elapsed_time, data["MaxTimeSurvived"])

            # Write updated stats back to file
            with open("GameFiles/assets/data/private/playerstats.json", "w") as file:
                json.dump(data, file)
        except Exception as e:
            print(f"Error updating player stats: {e}")
