import pygame


class DialogueBox:
    def __init__(self, width, height, x, y):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dialogue_text = ""
        self.dialogue_font = pygame.font.Font(None, 24)
        self.dialogue_color = (255, 255, 255)
        self.dialogue_position = (10, 10)
        self.animation_speed = 1
        self.animation_timer = 0
        self.is_animating = False

    def set_text(self, text):
        self.dialogue_text = text

    def set_font(self, font):
        self.dialogue_font = font

    def set_color(self, color):
        self.dialogue_color = color

    def set_animation_speed(self, speed):
        self.animation_speed = speed

    def start_animation(self):
        self.is_animating = True

    def stop_animation(self):
        self.is_animating = False

    def set_dialogue_position(self, x, y):
        self.dialogue_position = (x, y)

    def update(self):
        if self.is_animating:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                if len(self.dialogue_text) > 0:
                    self.dialogue_text = self.dialogue_text[:-1]
                else:
                    self.is_animating = False

    def draw(self, screen):
        dialogue_surface = self.dialogue_font.render(
            self.dialogue_text, True, self.dialogue_color
        )
        dialogue_rect = dialogue_surface.get_rect()
        dialogue_rect.topleft = self.dialogue_position
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height))
        screen.blit(dialogue_surface, dialogue_rect)
