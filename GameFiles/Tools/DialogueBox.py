import pygame
import textwrap

class DialogueBox:
    def __init__(self, x, y, font_size=24, padding=10):
        self.x = x
        self.y = y
        self.font_size = font_size
        self.padding = padding
        self.dialogue_font = pygame.font.Font(None, self.font_size)
        self.dialogue_color = (0, 0, 0)
        self.current_text = ""
        self.text_index = 0
        self.typing_sound = pygame.mixer.Sound("GameFiles/assets/sounds/typing.wav")
        self.background_image = pygame.image.load(
            "GameFiles/assets/images/dialogue_box.png"
        )

    def set_text(self, text):
        self.dialogue_text = text
        self.current_text = ""
        self.text_index = 0

    def update(self):
        if self.text_index < len(self.dialogue_text):
            self.current_text += self.dialogue_text[self.text_index]
            self.text_index += 1
            self.typing_sound.play()
            words = textwrap.wrap(
                self.current_text, self.background_image.get_width() // self.dialogue_font.size(" ")[0]
            )
            self.dialogue_lines = [
                self.dialogue_font.render(line, True, self.dialogue_color)
                for line in words
            ]
            self.height = (
                len(self.dialogue_lines) * self.dialogue_font.get_height()
                + 2 * self.padding
            )
            self.width = self.background_image.get_width()

    def draw(self, screen):
        self.background_image = pygame.transform.scale(
            self.background_image, (self.width, self.height)
        )
        screen.blit(self.background_image, (self.x, self.y))
        for i, line in enumerate(self.dialogue_lines):
            screen.blit(
                line,
                (
                    self.x + self.padding,
                    self.y + self.padding + i * self.dialogue_font.get_height(),
                ),
            )
