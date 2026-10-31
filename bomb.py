import pygame

from constants import LINE_WIDTH


class Bomb(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float) -> None:
        super().__init__(*self.containers)
        self.position = pygame.Vector2(x, y)
        self.timer = 1.0
        self.radius = 8

    def update(self, dt: float) -> None:
        self.timer -= dt

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "red", self.position, self.radius, LINE_WIDTH)
