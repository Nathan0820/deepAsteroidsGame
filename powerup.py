import pygame

from constants import LINE_WIDTH


class PowerUp(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, kind: str) -> None:
        super().__init__(*self.containers)
        self.position = pygame.Vector2(x, y)
        self.kind = kind
        self.radius = 12
        self.velocity = pygame.Vector2(0, 25)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.position.x %= pygame.display.get_surface().get_width()
        self.position.y %= pygame.display.get_surface().get_height()

    def draw(self, screen: pygame.Surface) -> None:
        color = "cyan" if self.kind == "shield" else "lime"
        pygame.draw.circle(screen, color, self.position, self.radius, LINE_WIDTH)
        label = pygame.font.Font(None, 18).render(
            "S" if self.kind == "shield" else "V", True, color
        )
        screen.blit(label, label.get_rect(center=self.position))
