import pygame  # pyright: ignore[reportMissingImports]

from circleshape import CircleShape, distance_point_to_segment
from constants import (
    LINE_WIDTH,
    PLAYER_RADIUS,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
    RESPAWN_INVULNERABILITY_TIMER,
)
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.spawn_x = x
        self.spawn_y = y
        self.rotation = 0
        self.shoot_timer = 0
        self.invulnerable_timer = 0
        self.no_cooldown_timer = 0
        self.speed_up_timer = 0
        self.shield_active = False

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def collides_with(self, other: CircleShape) -> bool:
            a, b, c = self.triangle()

            # Check distance from asteroid center to each of the 3 triangle edges
            dist_ab = distance_point_to_segment(other.position, a, b)
            dist_bc = distance_point_to_segment(other.position, b, c)
            dist_ca = distance_point_to_segment(other.position, c, a)

            # Collision if the asteroid touches any of the three edges
            return bool(dist_ab <= other.radius or dist_bc <= other.radius or dist_ca <= other.radius)

    def draw(self, screen):
        # Flicker while invulnerable (blink every 0.1s)
        if self.invulnerable_timer > 0 and int(self.invulnerable_timer * 10) % 2 == 0:
            return
        if self.shield_active == True:
            pygame.draw.circle(screen, "Blue", self.position, self.radius + 4, LINE_WIDTH)
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def respawn(self):
        self.position = pygame.Vector2(self.spawn_x, self.spawn_y)
        self.rotation = 0
        self.invulnerable_timer = RESPAWN_INVULNERABILITY_TIMER
        self.no_cooldown_timer = 0
        self.speed_up_timer = 0

    def update(self, dt):
        if self.invulnerable_timer > 0:
            self.invulnerable_timer = max(0, self.invulnerable_timer - dt)
        if self.no_cooldown_timer > 0:
            self.no_cooldown_timer = max(0, self.no_cooldown_timer - dt)
        if self.speed_up_timer > 0:
            self.speed_up_timer = max(0, self.speed_up_timer - dt)

        self.shoot_timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

        super().update(dt)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        if self.speed_up_timer > 0:
            self.position += forward * (PLAYER_SPEED * 1.25) * dt
        else:
            self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.no_cooldown_timer <= 0 and self.shoot_timer > 0:
            return
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN_SECONDS

        if self.no_cooldown_timer > 0:
            self.shoot_timer = 0.05
        else:
            self.shoot_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
