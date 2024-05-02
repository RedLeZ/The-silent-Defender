import pygame
import random
from Tools.Projectiles import Projectile
from Tools.DialogueBox import DialogueBox


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
        dialogue_text = "This is a dialogue box. Click to advance text."
        self.dialogue_box = DialogueBox(400, 100, 300, 300)
        self.dialogue_box.set_text(dialogue_text)
        self.dialogue_box.set_font(self.font)
        self.dialogue_box.set_color((255, 0, 0))
        self.dialogue_box.set_animation_speed(5)
        self.dialogue_box.start_animation()
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
        if self.hearts <= 0:
            self.game_state_manager.change_state("MainMenu")
            self.hearts = 3
            self.score = 0

    def update(self, dt):
        self.dialogue_box.update()

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
        self.dialogue_box.draw(surface)
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
