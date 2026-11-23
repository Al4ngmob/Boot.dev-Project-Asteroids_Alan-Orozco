## Asteroids

Asteroids is a 2D space shooter built with Python and Pygame. Pilot a triangular ship, shoot asteroids, and split them apart before they hit you.

### Requirements & Setup

1. Ensure you have **Python 3** installed.
2. Install **Pygame** from your terminal:
   ```bash
   pip install pygame
   ```

### How to Run

1. Clone the repository and move into the project directory.
2. Start the game from your terminal:
   ```bash
   python3 main.py
   ```

### Controls

- **W / S:** Move forward / backward
- **A / D:** Rotate left / right
- **Space:** Shoot (with a short cooldown)
- **Any Key (on Game Over):** Restart the game
- **Close Window:** Quit the game

### Gameplay & Behavior

- **Asteroid Spawning & Splitting**
  - Asteroids drift in from the edges of the screen.
  - Shooting an asteroid splits it into smaller pieces.
- **Scoring System**
  - Earn points by surviving and destroying asteroids (displayed in the top-left corner):
    - **Small asteroids:** `+50` points
    - **Medium asteroids:** `+25` points
    - **Large asteroids:** `+10` points
    - **Survival bonus:** `+1` point per second survived
- **Collision, Game Over & Restart**
  - Colliding with an asteroid triggers a **Game Over** screen displaying your final score.
  - Press any key on the Game Over screen to immediately restart a new run.
  - Shots that leave the screen are automatically removed.

### Project Structure

- `main.py`: Game loop, scoring, game over/restart handling, input handling, and collision checks
- `player.py`: Player ship movement, rotation, and shooting
- `asteroid.py`: Asteroid behavior and splitting
- `asteroidfield.py`: Spawns asteroids along the screen edges
- `shot.py`: Projectile behavior
- `circleshape.py`: Shared base class with position, radius, and collision detection
- `constants.py`: Screen size, speeds, and other tuning values
- `logger.py`: Event and state logging

### Future Updates

- Implement multiple lives and respawning
- Add an explosion effect for asteroids
- Add acceleration to player movement
- Wrap objects around the screen instead of removing them at the edges
- Add a background image
- Create different weapon types
- Make asteroids lumpy instead of perfectly round
- Give the ship a triangular hitbox instead of a circular one
- Add a shield power-up
- Add a speed power-up
- Add bombs that can be dropped
