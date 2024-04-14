import pygame


pygame.init()


class Projectile:
    def __init__(
        self,
        x,
        y,
        target_x,
        target_y,
        speed=5,
        size=10,
        color=(255, 0, 0),
        image=None,
    ):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = speed
        self.size = size
        self.color = color
        self.image = image
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.hit_n = 1

    def update(self):
        dx = (self.target_x + self.size / 2) - self.x
        dy = (self.target_y + self.size / 2) - self.y
        distance = (dx**2 + dy**2) ** 0.5
        if distance != 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
            self.rect.center = (self.x, self.y)

    def draw(self, surface):
        if self.image is None:
            pygame.draw.rect(surface, self.color, self.rect)
        else:
            surface.blit(self.image, self.rect.topleft)

    def collide_with_point(self, point):
        return self.rect.collidepoint(point)

    def check_for_mouse_hit(self):
        pos = pygame.mouse.get_pos()
        if self.collide_with_point(pos):
            return True
        else:
            return False

    def add_power_up(self, power_up, entensity):
        self.power_up = power_up
        self.entensity = entensity

        match power_up:
            case "speed":
                self.speed += self.entensity
            case "size":
                self.size += self.entensity
                self.hit_n += self.entensity * 2
