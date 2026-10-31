from circleshape import CircleShape
from constants import (
    ASTEROID_MIN_RADIUS,
    EXPLOSION_DURATION_SECONDS,
    LINE_WIDTH,
)
from logger import log_event
import pygame
import random
from explosion import Explosion

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        self.points = [
            self.radius * random.uniform(0.8, 1.2) for _ in range(10)
        ]

    def draw(self, screen) -> None:
        points = [
            self.position
            + pygame.Vector2(0, -length).rotate(index * 36)
            for index, length in enumerate(self.points)
        ]
        pygame.draw.polygon(screen, "white", points, LINE_WIDTH)

    def update(self, dt: float) -> None:
        # Update the asteroid's position based on its velocity
        self.position += self.velocity * dt
        self.wrap()

    def split(self) -> None:
        if not self.alive():
            return
        self.kill()
        Explosion(self.position.x, self.position.y, self.radius, EXPLOSION_DURATION_SECONDS)
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = self.velocity.rotate(angle) * 1.2
        asteroid2.velocity = self.velocity.rotate(-angle) * 1.2
