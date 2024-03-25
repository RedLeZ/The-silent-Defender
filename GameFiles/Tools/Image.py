import pygame

class Image:
    def __init__(self, image_path, x=0, y=0):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = x
        self.y = y

    def resize(self, width, height):
        self.image = pygame.transform.smoothscale(self.original_image, (width, height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
