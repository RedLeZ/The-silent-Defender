import pygame


class Button:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        font,
        normal_color,
        hover_color,
        action=None,
        sound_click=None,
        frame_image=None,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.action = action
        self.sound_click = sound_click
        self.frame_image = (
            pygame.transform.scale(
                pygame.image.load(frame_image).convert_alpha(),
                (width + 20, height + 20),
            )
            if frame_image
            else None
        )
        self.rect = pygame.Rect(x, y, width, height)
        self.hovered = False

    def draw(self, win):
        color = self.hover_color if self.hovered else self.normal_color
        pygame.draw.rect(win, color, self.rect)

        if self.frame_image:
            frame_rect = self.frame_image.get_rect(center=self.rect.center)
            win.blit(self.frame_image, frame_rect)

        text_surface = self.font.render(self.text, True, pygame.Color("black"))
        text_rect = text_surface.get_rect(center=self.rect.center)
        win.blit(text_surface, text_rect)

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.hovered = True
        else:
            self.hovered = False

    def click(self):
        if self.action:
            self.action()
        if self.sound_click:
            pygame.mixer.Sound(self.sound_click).play()
