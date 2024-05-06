import pygame


class DialogueBox:
    def __init__(self, screen_width, screen_height):
        self.is_active = True
        self.x = 400
        self.y = 500
        self.text = ""
        self.dialogue_index = 0
        self.dialogues = []
        self.background_image = pygame.image.load(
            "GameFiles/assets/images/dialogue_box.png"
        )
        self.character_image = None
        self.title = ""
        self.font = pygame.font.Font(None, 24)  # Create a font object
        self.typing_sound = pygame.mixer.Sound("GameFiles/assets/sounds/typing.wav")
        self.typing_index = 0
        self.typing_speed = 1

    def add_dialogue(self, dialogue, character_image_path, title):
        self.dialogues.append(dialogue)
        self.character_image = pygame.image.load(character_image_path)
        self.title = title

    def next_dialogue(self):
        if self.dialogue_index < len(self.dialogues):
            self.dialogue_index += 1
            self.typing_index = 0
        else:
            self.dialogue_index = 0
            self.typing_index = 0
            self.text = ""
            self.dialogues = []
            self.character_image = None
            self.title = ""

    def render_text(self, screen):
        if self.dialogue_index < len(self.dialogues):
            self.text = self.dialogues[self.dialogue_index]
            text_surface = self.font.render(
                self.text[: self.typing_index], True, (0, 0, 0)
            )
            title_surface = self.font.render(self.title, True, (0, 0, 0))
            screen.blit(self.background_image, (self.x, self.y))
            if self.character_image:
                screen.blit(self.character_image, (self.x + 420, self.y - 10))
            screen.blit(text_surface, (self.x + 10, self.y + 20))
            screen.blit(title_surface, (self.x + 10, self.y + 5))

    def update(self):
        if not self.is_active:
            return
        if self.dialogue_index >= len(self.dialogues):
            self.is_active = False
        elif self.typing_index < len(self.dialogues[self.dialogue_index]):
            self.typing_index += self.typing_speed
            if self.typing_index % 5 == 0:
                self.play_sound_effect()

    def play_sound_effect(self):
        self.typing_sound.play()

    def check_for_mouse_hit(self):
        pos = pygame.mouse.get_pos()
        if (
            pos[0] > self.x
            and pos[0] < self.x + self.background_image.get_width()
            and pos[1] > self.y
            and pos[1] < self.y + self.background_image.get_height()
        ):
            return True
