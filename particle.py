import random

import pygame  # pyright: ignore[reportMissingImports]


class Particles(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float) -> None:
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.radius = random.uniform(1, 3)
        self.lifetime = random.uniform(0.3 ,0.6)
        speed = random.uniform(60, 180)
        angle = random.uniform(0, 360)
        self.velocity = pygame.Vector2(1, 0).rotate(angle) * speed

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

    def draw(self, screen):
        pygame.draw.circle(screen, "white", (int(self.position.x), int(self.position.y)), self.radius)
