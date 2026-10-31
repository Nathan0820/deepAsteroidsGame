from circleshape import CircleShape
from constants import LINE_WIDTH
import pygame

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, screen) -> None:
        # Draw the asteroid as a circle
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        # Update the asteroid's position based on its velocity
        self.position += self.velocity * dt
