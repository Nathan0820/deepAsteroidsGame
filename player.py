from bomb import Bomb
from circleshape import CircleShape
from constants import (
    PLAYER_ACCELERATION,
    BOMB_COOLDOWN_SECONDS,
    LINE_WIDTH,
    PLAYER_MAX_SPEED,
    PLAYER_RADIUS,
    PLAYER_RAPID_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_SPEED,
    PLAYER_TURN_SPEED,
    WEAPON_SPREAD_ANGLE,
)
from shot import Shot
import pygame


class Player(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.bomb_timer = 0
        self.weapon = 1
        self.shield_timer = 0
        self.speed_timer = 0
        self.invulnerable_timer = 0
        self.velocity = pygame.Vector2()

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        points = self.triangle()
        if self.invulnerable_timer > 0 and int(self.invulnerable_timer * 10) % 2 == 0:
            return
        color = "cyan" if self.shield_timer > 0 else "white"
        pygame.draw.polygon(screen, color, points, LINE_WIDTH)
        if self.shield_timer > 0:
            pygame.draw.circle(screen, color, self.position, self.radius + 8, LINE_WIDTH)

    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        self.shoot_timer = max(0, self.shoot_timer - dt)
        self.bomb_timer = max(0, self.bomb_timer - dt)
        self.shield_timer = max(0, self.shield_timer - dt)
        self.speed_timer = max(0, self.speed_timer - dt)
        self.invulnerable_timer = max(0, self.invulnerable_timer - dt)

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.accelerate(dt)
        if keys[pygame.K_s]:
            self.accelerate(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_1]:
            self.weapon = 1
        elif keys[pygame.K_2]:
            self.weapon = 2
        elif keys[pygame.K_3]:
            self.weapon = 3
        if keys[pygame.K_b]:
            self.drop_bomb()

    def accelerate(self, dt: float) -> None:
        direction = pygame.Vector2(0, 1).rotate(self.rotation)
        multiplier = 1.5 if self.speed_timer > 0 else 1
        self.velocity += direction * PLAYER_ACCELERATION * multiplier * dt
        if self.velocity.length() > PLAYER_MAX_SPEED * multiplier:
            self.velocity.scale_to_length(PLAYER_MAX_SPEED * multiplier)
        self.position += self.velocity * dt
        self.wrap()

    def shoot(self) -> None:
        if self.shoot_timer > 0:
            return
        angles = (
            [0]
            if self.weapon in (1, 3)
            else [-WEAPON_SPREAD_ANGLE, WEAPON_SPREAD_ANGLE]
        )
        for angle in angles:
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = (
                pygame.Vector2(0, 1).rotate(self.rotation + angle)
                * PLAYER_SHOOT_SPEED
            )
        self.shoot_timer = (
            PLAYER_RAPID_SHOOT_COOLDOWN_SECONDS
            if self.weapon == 3
            else PLAYER_SHOOT_COOLDOWN_SECONDS
        )

    def drop_bomb(self) -> None:
        if self.bomb_timer > 0:
            return
        Bomb(self.position.x, self.position.y)
        self.bomb_timer = BOMB_COOLDOWN_SECONDS

    def collides_with(self, other: "CircleShape") -> bool:
        points = self.triangle()
        if any(point.distance_to(other.position) <= other.radius for point in points):
            return True
        for start, end in zip(points, points[1:] + points[:1]):
            edge = end - start
            if edge.length_squared() == 0:
                continue
            projection = max(
                0,
                min(
                    1,
                    (other.position - start).dot(edge) / edge.length_squared(),
                ),
            )
            closest = start + edge * projection
            if closest.distance_to(other.position) <= other.radius:
                return True
        return False
