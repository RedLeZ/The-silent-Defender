import pygame


class DialogueBox:
    def __init__(self, screen_width, screen_height):
        self.is_active = True  # Flag to indicate if the dialogue box is active
        self.x = 400  # X-coordinate of the dialogue box position
        self.y = 500  # Y-coordinate of the dialogue box position
        self.text = ""  # Current dialogue text
        self.dialogue_index = 0  # Index of the current dialogue in the dialogues list
        self.dialogues = []  # List of dialogues
        self.typing_timer = pygame.time.get_ticks()  # Timer for typing effect
        self.typing_delay = (
            50  # Delay between each character in the typing effect (in milliseconds)
        )
        self.background_image = pygame.image.load(
            "GameFiles/assets/images/dialogue_box.png"
        ).convert_alpha()  # Background image of the dialogue box
        self.character_image = (
            None  # Image of the character associated with the dialogue
        )
        self.title = ""  # Title of the dialogue box
        self.font = pygame.font.Font(None, 24)  # Font for rendering text
        self.typing_sound = pygame.mixer.Sound(
            "GameFiles/assets/sounds/typing.wav"
        )  # Sound effect for typing
        self.typing_index = 0  # Index of the current character being typed
        self.typing_speed = 1  # Speed of the typing effect

    def add_dialogue(self, dialogue, character_image_path, title):
        # Add a new dialogue to the dialogues list
        self.dialogues.append(dialogue)
        self.character_image = pygame.image.load(
            character_image_path
        )  # Load the character image
        self.title = title  # Set the title of the dialogue box

    def next_dialogue(self):
        # Move to the next dialogue in the dialogues list
        if self.dialogue_index < len(self.dialogues):
            self.dialogue_index += 1
            self.typing_index = 0
        else:
            # If there are no more dialogues, reset the dialogue box
            self.dialogue_index = 0
            self.typing_index = 0
            self.text = ""
            self.dialogues = []
            self.character_image = None
            self.title = ""

    def render_text(self, screen):
        # Render the text on the screen
        if self.dialogue_index < len(self.dialogues):
            self.text = self.dialogues[self.dialogue_index]
            text_surface = self.font.render(
                self.text[: self.typing_index], True, (0, 0, 0)
                
            )  # Render the text with the typing effect
            
            title_surface = self.font.render(
                self.title, True, (0, 0, 0)
            )  # Render the title
            screen.blit(
                self.background_image, (self.x, self.y)
            )  # Draw the background image
            if self.character_image:
                screen.blit(
                    self.character_image, (self.x + 420, self.y - 10)
                )  # Draw the character image
            screen.blit(text_surface, (self.x + 10, self.y + 20))  # Draw the text
            screen.blit(title_surface, (self.x + 10, self.y + 5))  # Draw the title
        
        

    def update(self):
        # Update the state of the dialogue box
        if not self.is_active:
            return
        if self.dialogue_index >= len(self.dialogues):
            self.is_active = (
                False  # Deactivate the dialogue box if there are no more dialogues
            )
        elif self.typing_index < len(self.dialogues[self.dialogue_index]):
            current_time = pygame.time.get_ticks()
            if current_time - self.typing_timer > self.typing_delay:
                self.typing_index += self.typing_speed  # Increment the typing index
                self.typing_timer = current_time

    def play_sound_effect(self):
        # Play the typing sound effect
        self.typing_sound.play()

    def check_for_mouse_hit(self):
        # Check if the mouse is hovering over the dialogue box
        pos = pygame.mouse.get_pos()
        if (
            pos[0] > self.x
            and pos[0] < self.x + self.background_image.get_width()
            and pos[1] > self.y
            and pos[1] < self.y + self.background_image.get_height()
        ):
            return True
