import sys

import pygame  # pyright: ignore[reportMissingImports]

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import ASTEROID_MIN_RADIUS, SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from player import Player
from shot import Shot


def play_game(screen, clock, font, large_font):
    dt = 0.0
    score = 0
    time_survived = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, drawable, updatable)
    player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2)
    AsteroidField()

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        screen.fill("Black")
        updatable.update(dt)

        for sprite in drawable:
            sprite.draw(screen)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")

                game_over_surface = large_font.render("GAME OVER", True, (255, 0, 0))
                game_over_rect = game_over_surface.get_rect()
                game_over_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40)

                final_score_surface = font.render(f"FINAL SCORE: {score}", True, (255, 0, 0))
                final_score_rect = final_score_surface.get_rect()
                final_score_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 10)

                restart_surface = font.render("Press any key to Restart", True, (255, 255, 255))
                restart_rect = restart_surface.get_rect()
                restart_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)

                screen.blit(game_over_surface, game_over_rect)
                screen.blit(final_score_surface, final_score_rect)
                screen.blit(restart_surface, restart_rect)
                pygame.display.flip()

                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return "quit"
                        if event.type == pygame.KEYDOWN:
                            return "restart"

            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
                    if asteroid.radius <= ASTEROID_MIN_RADIUS:
                        score += 50
                    elif asteroid.radius < ASTEROID_MIN_RADIUS * 1.5:
                        score += 25
                    else:
                        score += 10
                    break

        time_survived += dt
        if time_survived >= 1.0:
            score += 1
            time_survived -= 1
        score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surface, (10, 10))
        pygame.display.flip()
        dt = clock.tick(60) / 1000


def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    large_font = pygame.font.Font(None, 64)

    while True:
            action = play_game(screen, clock, font, large_font)
            if action == "quit":
                break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
