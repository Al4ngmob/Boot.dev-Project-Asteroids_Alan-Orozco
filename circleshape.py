import pygame  # pyright: ignore[reportMissingImports]

from constants import SCREEN_HEIGHT, SCREEN_WIDTH


def distance_point_to_segment(
    p: pygame.Vector2, a: pygame.Vector2, b: pygame.Vector2
) -> float:
    ab = b - a
    ap = p - a

    segment_len_sq = ab.length_squared()
    if segment_len_sq == 0:
        return p.distance_to(a)

    # Project AP onto AB to find scalar t
    t = ap.dot(ab) / segment_len_sq
    # Clamp t to segment bounds [0.0, 1.0]
    t = max(0.0, min(1.0, t))

    closest = a + ab * t
    return p.distance_to(closest)

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, radius: float) -> None:
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()

        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen: pygame.Surface) -> None:
        # must override
        pass

    def update(self, dt: float) -> None:
        # Wrap horizontally with radius margin
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius

        # Wrap vertically
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius

    def collides_with(self, other: "CircleShape") -> bool:
        distance = self.position.distance_to(other.position)
        return distance <= self.radius + other.radius
