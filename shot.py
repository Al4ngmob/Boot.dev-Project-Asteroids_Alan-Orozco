import pygame  # pyright: ignore[reportMissingImports]

from circleshape import CircleShape
from constants import LINE_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, SHOT_RADIUS


class Shot(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen: pygame.Surface) -> None:
        radius = self.radius
        pygame.draw.circle(screen, "white", self.position, radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += (self.velocity * dt)
        if (
            self.position.x < 0
            or self.position.x > SCREEN_WIDTH
            or self.position.y < 0
            or self.position.y > SCREEN_HEIGHT
        ):
            self.kill()
