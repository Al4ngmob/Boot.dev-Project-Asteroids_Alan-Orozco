# Asteroids

Asteroids is a 2D space shooter built with Python and Pygame. Pilot a triangular ship, shoot asteroids, and split them apart before they hit you.

## Requirements & Setup

1. Ensure you have **Python 3** installed.
2. Install **Pygame** from your terminal:
   ```bash
   pip install pygame
   ```

## How to Run

1. Clone the repository and move into the project directory.
2. Start the game from your terminal:
   ```bash
   python3 main.py
   ```

## Controls

- **W / S**: Move forward / backward
- **A / D**: Rotate left / right
- **Space**: Shoot (with a short cooldown)
- **R** *(when destroyed)*: Respawn ship (if lives remain)
- **Any Key** *(on Game Over)*: Restart the game
- **Close Window**: Quit the game

## Gameplay & Behavior

- **Asteroid Spawning & Splitting**
  - Asteroids drift in from the edges of the screen.
  - Shooting an asteroid splits it into smaller pieces.
  - Particles appear after hitting (splitting or destroying) an asteroid.
  - Asteroids spawn as jagged polygons instead of perfect circles.
- **Collision Handling**
  - The player has a triangular hitbox.
  - Shots, asteroids, and power-ups have circular hitboxes.
  - Checks handle player collisions with circular hitboxes and collisions between circular hitboxes.
- **Scoring System**
  - Earn points by surviving and destroying asteroids (displayed in the top-left HUD):
    - Small asteroids: +50 points
    - Medium asteroids: +25 points
    - Large asteroids: +10 points
    - Survival bonus: +1 point per second survived
- **Lives & Respawning**
  - You begin each run with 3 lives.
  - Taking a hit costs 1 life and prompts you to press **R** to respawn.
  - Respawning returns the ship to the center, clears nearby asteroids, and grants a 2-second invulnerability period (indicated by ship flickering).
- **Game Over & Restart**
  - Losing all lives triggers the Game Over screen displaying your final score.
  - Press any key on the Game Over screen to immediately restart a new run.
  - Shots that leave the screen are automatically removed.
- **Screen Wrapping & Background**
  - The player and asteroids wrap across the screen instead of going out of bounds.
  - A cap of 40 active asteroids prevents lag and keeps the screen from getting too crowded; adjustable in `constants.py`.
  - Added an `assets` folder where you can add background images (`.png`, `.jpg`, or `.jpeg`), randomly picking a background each time you start the game or respawn.
- **Power-Ups**
  - Destroying a small asteroid has a 20% chance to spawn 1 of 3 power-ups:
    - **Shield**: Grants a free hit and disappears on impact while giving brief invulnerability; spawns as a blue orb.
    - **No Shot Cooldown**: Lets you fire a laser-style stream for 2 seconds; spawns as a red orb.
    - **Speed Up**: Grants a 25% speed boost for 3.5 seconds; spawns as a green orb.
  - Durations can be adjusted in `constants.py`.

## Project Structure

- `main.py`: Game loop, HUD rendering, lives/respawn management, game over/restart handling, input handling, and collision checks
- `player.py`: Player ship movement, rotation, shooting, respawn state, and invulnerability blinking
- `asteroid.py`: Asteroid behavior and splitting
- `asteroidfield.py`: Spawns asteroids along the screen edges
- `shot.py`: Projectile behavior
- `circleshape.py`: Shared base class with position, radius, and collision detection
- `constants.py`: Screen size, speeds, lives count, timers, and other tuning values
- `logger.py`: Event and state logging
- `particle.py`: Particle class for asteroid hit/destruction effects
- `powerup.py`: Power-up class for randomly spawning 1 of 3 power-ups when a small asteroid is destroyed

## Future Updates

- None for the time being


[![Boot.dev Build Asteroids using Python and Pygame certificate](https://api.boot.dev/v1/static/certificate/24d46176-52b6-438b-b4c5-a1ecb0beed9e)](https://www.boot.dev/certificates/24d46176-52b6-438b-b4c5-a1ecb0beed9e)
