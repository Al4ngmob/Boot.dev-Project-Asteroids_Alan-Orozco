import random

import pygame  # pyright: ignore[reportMissingImports]

from circleshape import CircleShape
from constants import MAX_POWER_UPS, SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event


class Powerup(CircleShape):
    containers: tuple[pygame.sprite.Group, ...] = ()

    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        if (
            self.position.x < 0
            or self.position.x > SCREEN_WIDTH
            or self.position.y < 0
            or self.position.y > SCREEN_HEIGHT
        ):
            self.kill()


class Shield(Powerup):
    def apply(self, player):
            player.shield_active = True
            log_event("picked_up: shield")

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "blue", self.position, self.radius, 0)

    @classmethod
    def spawn(cls, x: float, y: float, velocity: pygame.Vector2):
        if len(cls.containers[0]) < MAX_POWER_UPS:
            shield = cls(x, y, 10)
            shield.velocity = velocity * 0.5
            return shield


class No_cooldown(Powerup):
    def apply(self, player):
            player.no_cooldown_timer = 2.0
            log_event("picked_up: no_cooldown")

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "red", self.position, self.radius, 0)

    @classmethod
    def spawn(cls, x: float, y: float, velocity: pygame.Vector2):
        if len(cls.containers[0]) < MAX_POWER_UPS:
            powerup = cls(x, y, 10)
            angle = random.uniform(20, 50)
            powerup.velocity = (velocity * 0.5).rotate(angle)
            return powerup

class Speed_up(Powerup):
    def apply(self, player):
            player.speed_up_timer = 3.5
            log_event("picked_up: Speed up")

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "green", self.position, self.radius, 0)

    @classmethod
    def spawn(cls, x: float, y: float, velocity: pygame.Vector2):
        if len(cls.containers[0]) < MAX_POWER_UPS:
            powerup = cls(x, y, 10)
            angle = random.uniform(20, 50)
            powerup.velocity = (velocity * 0.5).rotate(angle)
            return powerup
