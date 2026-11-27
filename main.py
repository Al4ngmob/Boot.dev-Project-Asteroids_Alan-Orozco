import os
import random
import sys

import pygame  # pyright: ignore[reportMissingImports]

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import (
    ASTEROID_MIN_RADIUS,
    PLAYER_LIVES,
    RESPAWN_INVULNERABILITY_TIMER,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from logger import log_event, log_state
from particle import Particles
from player import Player
from powerup import Powerup
from shot import Shot


def play_game(screen, clock, font, large_font, bg_image):
    dt = 0.0
    score = 0
    time_survived = 0.0
    lives = PLAYER_LIVES

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, drawable, updatable)
    Particles.containers = (drawable, updatable)
    Powerup.containers = (powerups, updatable, drawable)

    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)
    AsteroidField()

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        #Check if bag_image exists, else fill screen black
        if bg_image is not None:
            screen.blit(bg_image, (0, 0))
        else:
            screen.fill("Black")

        updatable.update(dt)

        for sprite in drawable:
            sprite.draw(screen)

        # Check asteroid and powerup collisions with player
        for powerup in list(powerups):
            if powerup.collides_with(player):
                powerup.apply(player)
                powerup.kill()

        for asteroid in list(asteroids):
            if player.invulnerable_timer <= 0 and asteroid.collides_with(player):
                log_event("player_hit")
                if player.shield_active == True:
                    player.shield_active = False
                    player.invulnerable_timer = RESPAWN_INVULNERABILITY_TIMER
                    asteroid.kill()
                else:
                    lives -= 1

                    # --- RESPAWN PROMPT ---
                    score_lives_surface = font.render(
                        f"REMAINING LIVES: {lives}   SCORE: {score}", True, (255, 0, 0)
                    )
                    score_lives_rect = score_lives_surface.get_rect(
                        center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 15)
                    )

                    respawn_surface = font.render(
                        "Press R to Respawn", True, (255, 255, 255)
                    )
                    respawn_rect = respawn_surface.get_rect(
                        center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 25)
                    )

                    screen.blit(score_lives_surface, score_lives_rect)
                    screen.blit(respawn_surface, respawn_rect)
                    pygame.display.flip()

                    waiting_for_respawn = True
                    while waiting_for_respawn:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                return "quit"
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                                player.respawn()
                                for a in asteroids:
                                    a.kill()
                                waiting_for_respawn = False

                if lives <= 0:
                    # --- GAME OVER SCREEN ---
                    game_over_surface = large_font.render("GAME OVER", True, (255, 0, 0))
                    game_over_rect = game_over_surface.get_rect(
                        center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40)
                    )

                    final_score_surface = font.render(
                        f"FINAL SCORE: {score}", True, (255, 0, 0)
                    )
                    final_score_rect = final_score_surface.get_rect(
                        center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 10)
                    )

                    restart_surface = font.render(
                        "Press any key to Restart", True, (255, 255, 255)
                    )
                    restart_rect = restart_surface.get_rect(
                        center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)
                    )

                    screen.blit(game_over_surface, game_over_rect)
                    screen.blit(final_score_surface, final_score_rect)
                    screen.blit(restart_surface, restart_rect)
                    pygame.display.flip()

                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                return "quit"
                            elif event.type == pygame.KEYDOWN:
                                return "restart"

                break

            # Check asteroid collisions with shots
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

        # Passive score increment per second
        time_survived += dt
        if time_survived >= 1.0:
            score += 1
            time_survived -= 1.0

        # HUD (Lives and Score)
        hud_surface = font.render(
            f"Score: {score}   Lives: {lives}", True, (255, 255, 255)
        )
        screen.blit(hud_surface, (10, 10))

        pygame.display.flip()
        dt = clock.tick(60) / 1000.0


def get_random_background(folder_path: str, width: int, height: int):
    #chose an random background from assets folder
    valid_extensions = (".png", ".jpg", ".jpge")
    images = [
        f for f in os.listdir(folder_path)
        if f.lower().endswith(valid_extensions)
    ]

    if not images:
        return None

    chosen_bg = random.choice(images)
    path = os.path.join(folder_path, chosen_bg)

    img = pygame.image.load(path).convert()
    return pygame.transform.scale(img, (width, height))





def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    large_font = pygame.font.Font(None, 64)

    while True:
        bg_image = get_random_background("assets", SCREEN_WIDTH, SCREEN_HEIGHT)

        action = play_game(screen, clock, font, large_font, bg_image)
        if action == "quit":
            break

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
