import pygame

from constants import EXPLOSION_DURATION_SECONDS, LINE_WIDTH


class Explosion(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, radius: float, duration: float) -> None:
        super().__init__(*self.containers)
        self.position = pygame.Vector2(x, y)
        self.radius = radius
        self.max_radius = radius * 1.8
        self.duration = duration

    def update(self, dt: float) -> None:
        self.duration -= dt
        if self.duration <= 0:
            self.kill()

    def draw(self, screen: pygame.Surface) -> None:
        progress = max(0, self.duration) / EXPLOSION_DURATION_SECONDS
        radius = max(1, int(self.max_radius * (1 - progress)))
        pygame.draw.circle(screen, "orange", self.position, radius, LINE_WIDTH)
