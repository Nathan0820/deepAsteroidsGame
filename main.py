import random

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from bomb import Bomb
from constants import (
    ASTEROID_MIN_RADIUS,
    PLAYER_INVULNERABLE_SECONDS,
    PLAYER_LIVES,
    PLAYER_RESPAWN_SECONDS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SCORE_LARGE_ASTEROID,
    SCORE_MEDIUM_ASTEROID,
    SCORE_SMALL_ASTEROID,
    WEAPON_BOMB_RADIUS,
)
from explosion import Explosion
from logger import log_event, log_state
from player import Player
from powerup import PowerUp
from shot import Shot


def asteroid_score(radius: float) -> int:
    if radius <= ASTEROID_MIN_RADIUS:
        return SCORE_SMALL_ASTEROID
    if radius <= ASTEROID_MIN_RADIUS * 2:
        return SCORE_MEDIUM_ASTEROID
    return SCORE_LARGE_ASTEROID


def draw_background(screen: pygame.Surface, stars: list[tuple[int, int, int]]) -> None:
    screen.fill((4, 6, 18))
    for x, y, brightness in stars:
        pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), 1)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)
    stars = [
        (random.randrange(SCREEN_WIDTH), random.randrange(SCREEN_HEIGHT), random.randrange(80, 220))
        for _ in range(140)
    ]

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = updatable
    Bomb.containers = (updatable, drawable, bombs)
    Explosion.containers = (updatable, drawable, explosions)
    Player.containers = (updatable, drawable)
    PowerUp.containers = (updatable, drawable, powerups)
    Shot.containers = (updatable, drawable, shots)
    AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    lives = PLAYER_LIVES
    score = 0
    respawn_timer = 0.0
    game_over = False

    while True:
        dt = min(clock.tick(60) / 1000.0, 0.05)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        keys = pygame.key.get_pressed()
        if game_over and keys[pygame.K_r]:
            lives, score, game_over = PLAYER_LIVES, 0, False
            player.position.update(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            player.invulnerable_timer = PLAYER_INVULNERABLE_SECONDS

        log_state()
        if not game_over:
            updatable.update(dt)
            if respawn_timer > 0:
                respawn_timer -= dt
            for asteroid in list(asteroids):
                if not asteroid.alive():
                    continue
                if respawn_timer <= 0 and player.invulnerable_timer <= 0 and player.collides_with(asteroid):
                    if player.shield_timer > 0:
                        player.shield_timer = 0
                        asteroid.split()
                    else:
                        lives -= 1
                        log_event("player_hit")
                        player.position.update(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                        player.velocity.update(0, 0)
                        player.invulnerable_timer = PLAYER_INVULNERABLE_SECONDS
                        respawn_timer = PLAYER_RESPAWN_SECONDS
                        if lives <= 0:
                            game_over = True
                            log_event("game_over")
                    break
                for shot in list(shots):
                    if not asteroid.alive():
                        break
                    if not shot.alive():
                        continue
                    if shot.collides_with(asteroid):
                        shot.kill()
                        score += asteroid_score(asteroid.radius)
                        log_event("asteroid_shot", score=score)
                        if random.random() < 0.12:
                            PowerUp(asteroid.position.x, asteroid.position.y, random.choice(["shield", "speed"]))
                        asteroid.split()
                        break
            for powerup in list(powerups):
                if player.position.distance_to(powerup.position) <= player.radius + powerup.radius:
                    if powerup.kind == "shield":
                        player.shield_timer = 8
                    else:
                        player.speed_timer = 8
                    powerup.kill()
            for bomb in list(bombs):
                if bomb.timer <= 0:
                    Explosion(bomb.position.x, bomb.position.y, WEAPON_BOMB_RADIUS, 0.35)
                    for asteroid in list(asteroids):
                        if bomb.position.distance_to(asteroid.position) <= WEAPON_BOMB_RADIUS:
                            score += asteroid_score(asteroid.radius)
                            asteroid.split()
                    bomb.kill()

        draw_background(screen, stars)
        for obj in drawable:
            obj.draw(screen)
        hud = font.render(f"Score: {score}   Lives: {lives}   Weapon: {player.weapon}", True, "white")
        screen.blit(hud, (16, 16))
        if game_over:
            message = font.render("GAME OVER - press R to restart", True, "red")
            screen.blit(message, message.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))
        pygame.display.flip()


if __name__ == "__main__":
    main()
