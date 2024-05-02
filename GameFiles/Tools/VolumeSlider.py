import pygame


class VolumeSlider:
    def __init__(
        self, x, y, width, height, bg_color, fg_color, volume_callback, frame_image
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.volume_callback = volume_callback
        self.frame_image = pygame.image.load(frame_image)

        self.slider_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.circle_color = (0, 0, 0)
        self.dragging = False
        self.slider_width = int(width * pygame.mixer.music.get_volume())
        self.circle_radius = 10
        self.circle_x = self.x + self.slider_width
        self.circle_y = self.y + self.height // 2
        self.frame_offset_x = 15  # Adjust this value as needed
        self.frame_offset_y = 15  # Adjust this value as needed

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.slider_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x = event.pos[0]
                self.circle_x = max(self.x, min(self.x + self.width, mouse_x))
                volume = (self.circle_x - self.x) / self.width
                self.volume_callback(volume)

    def update(self):
        if self.dragging:
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)

    def draw(self, surface):
        # Calculate slider position and frame position
        slider_x = self.x + (self.width - self.slider_width) / 2
        frame_x = self.x - self.frame_offset_x
        frame_y = self.y - self.frame_offset_y

        # Draw background
        pygame.draw.rect(
            surface, self.bg_color, (slider_x, self.y, self.slider_width, self.height)
        )

        # Draw circle
        pygame.draw.circle(
            surface,
            self.circle_color,
            (self.circle_x, self.circle_y),
            self.circle_radius,
        )

        # Draw bar
        pygame.draw.rect(
            surface,
            self.fg_color,
            (slider_x, self.y, self.circle_x - slider_x, self.height),
        )

        # Resize the frame image to match the size of the slider rectangle
        frame_image = pygame.transform.scale(
            self.frame_image, (self.width + 30, self.height + 30)
        )

        # Draw frame
        surface.blit(frame_image, (frame_x, frame_y))

        # Draw text
        volume_percentage = int(pygame.mixer.music.get_volume() * 100)
        font = pygame.font.Font(None, 24)
        text_surface = font.render(f"{volume_percentage}%", True, (0, 0, 0))
        text_rect = text_surface.get_rect(
            center=(self.x + self.width // 2, self.y + self.height // 2)
        )
        surface.blit(text_surface, text_rect)
