# Particle class
import pygame
import random


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = random.uniform(-1, 1)
        self.dy = random.uniform(-1, 1)
        self.lifetime = 60

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1

    def draw(self, window):
        color = (255, 0, 0)
        position = (int(self.x), int(self.y))
        pygame.draw.circle(window, color, position, 2)


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def add_particle(self, x, y):
        self.particles.append(Particle(x, y))

    def update(self, window):
        self.particles = [p for p in self.particles if p.lifetime > 0]
        for particle in self.particles:
            particle.update()
            particle.draw(window)


class ParticlePool:
    def __init__(self, size):
        self.size = size
        self.particles = [Particle(0, 0) for _ in range(size)]
        self.next_particle = 0

    def add_particle(self, x, y):
        self.particles[self.next_particle].x = x
        self.particles[self.next_particle].y = y
        self.particles[self.next_particle].lifetime = 60
        self.next_particle = (self.next_particle + 1) % self.size

    def update(self, window):
        for particle in self.particles:
            if particle.lifetime > 0:
                particle.update()
                particle.draw(window)
