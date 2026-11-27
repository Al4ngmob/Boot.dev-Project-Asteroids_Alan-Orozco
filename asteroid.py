import random

import pygame  # pyright: ignore[reportMissingImports]

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
from logger import log_event
from particle import Particles
from powerup import No_cooldown, Shield, Speed_up


class Asteroid(CircleShape):

    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        num_vertices = random.randint(8, 12)
        angle_step = 360 / num_vertices
        self.offsets = []
        for i in range(num_vertices):
            angle = i * angle_step
            r = self.radius * random.uniform(0.80, 1.20)

            vertex_offset = pygame.Vector2(0, 1).rotate(angle) * r
            self.offsets.append(vertex_offset)

    def draw(self, screen: pygame.Surface) -> None:
        points = [self.position + offset for offset in self.offsets]
        pygame.draw.polygon(screen, "white", points, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += (self.velocity * dt)
        super().update(dt)

    def split(self):
        self.kill()
        num_particles = random.randint(10, 20)
        for _ in range(num_particles):
            Particles(self.position.x, self.position.y)
        if self.radius <= ASTEROID_MIN_RADIUS:
            spawn_power_up_chance = random.randint(1, 15)
            if spawn_power_up_chance == 2:
                Shield.spawn(self.position.x, self.position.y, self.velocity)
            elif spawn_power_up_chance == 7:
                No_cooldown.spawn(self.position.x, self.position.y, self.velocity)
            elif spawn_power_up_chance == 14:
                Speed_up.spawn(self.position.x, self.position.y, self.velocity)
            return
        log_event("asteroid_split")
        new_angle = random.uniform(20, 50)
        new_velocity_1 = self.velocity.rotate(new_angle)
        new_velocity_2 = self.velocity.rotate(- new_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        new_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid.velocity = new_velocity_1 * 1.2
        new_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid.velocity = new_velocity_2 * 1.2
