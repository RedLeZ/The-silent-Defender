import pygame


class DialogueBox:
    def __init__(self, screen_width, screen_height):
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

    def add_dialogue(self, dialogue, character_image_path, title):
        self.dialogues.append(dialogue)
        self.character_image = pygame.image.load(character_image_path)
        self.title = title

    def render_text(self, screen):
        print("DEBUG : strating the dialogue renderer")
        if self.dialogue_index < len(self.dialogues):
            
            self.text = self.dialogues[self.dialogue_index]
            text_surface = self.font.render(
                self.text, True, (255, 255, 255)
            )  # Render the text
            screen.blit(self.background_image, (self.x, self.y))
            screen.blit(text_surface, (self.x + 10, self.y + 10))  # Draw the text
            if self.character_image:
                screen.blit(self.character_image, (self.x + 10, self.y + 50))
            else:
                self.text = ""
                self.character_image = None
                self.title = ""
                screen.blit(self.background_image, (self.x, self.y))

    def play_sound_effect(self):
        self.typing_sound.play()

    def next_dialogue(self):
        if self.dialogue_index < len(self.dialogues) - 1:
            self.dialogue_index += 1
            self.play_sound_effect()
