# Deep Asteroids

A small Asteroids-style arcade game built with Python and Pygame.

## Requirements

- Python 3.13 or newer
- Pygame 2.6.1

## Run the game

Using `uv`:

```bash
uv sync
uv run python main.py
```

Or, after installing Pygame in your active Python environment:

```bash
python main.py
```

## Controls

| Key | Action |
| --- | --- |
| `W` | Accelerate forward |
| `S` | Accelerate backward |
| `A` | Rotate left |
| `D` | Rotate right |
| `Space` | Fire the selected weapon |
| `1` | Select the standard single-shot weapon |
| `2` | Select the spread weapon |
| `3` | Select the rapid-fire weapon |
| `B` | Drop a bomb |
| `R` | Restart after game over |

Close the game window to quit.

## Gameplay

- Destroy asteroids to earn points.
- Large asteroids split into two smaller, faster asteroids when hit.
- Small asteroids are destroyed without splitting further.
- The player starts with three lives.
- After losing a life, the ship respawns in the center with temporary
  invulnerability.
- The ship, asteroids, shots, and power-ups wrap around the screen edges.
- A cyan power-up grants a temporary shield.
- A green power-up grants temporary extra acceleration and top speed.
- Bombs detonate after a short delay and destroy asteroids in a large radius.
- The game ends when all lives are lost. Press `R` to start a new game.

## Project layout

- `main.py` - game setup, loop, collisions, scoring, and HUD
- `player.py` - movement, weapons, shield, and triangular hitbox
- `asteroid.py` - asteroid movement, rendering, and splitting
- `asteroidfield.py` - asteroid spawning
- `shot.py` - projectile behavior
- `bomb.py` - delayed area-of-effect bombs
- `explosion.py` - temporary explosion animation
- `powerup.py` - shield and speed power-ups
- `constants.py` - gameplay tuning values