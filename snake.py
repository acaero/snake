import pygame
import random
from typing import Optional, List, Tuple

TILE_SIZE = 20

# TODO: Spielklassen


class Item:
    def __init__(self, x: int, y: int) -> None:
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE

    def occupies(self, x: int, y: int) -> bool:
        return x == self.x and y == self.y


class Brick(Item):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(
            (60, 63, 64),
            pygame.Rect(
                self.x,
                self.y,
                TILE_SIZE,
                TILE_SIZE
            )
        )


class Cherry(Item):
    def __init__(self) -> None:
        super().__init__(0, 0)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.ellipse(
            surface,
            (191, 157, 138),
            pygame.Rect(
                self.x,
                self.y,
                TILE_SIZE,
                TILE_SIZE
            )
        )

    def move(self, forbidden_wall: list[object], snake: object, width: int, height: int) -> None:
        searching_spot = True
        while searching_spot:
            x, y = random.randint(0, width - 2), random.randint(0, height - 2)
            x, y = x * TILE_SIZE, y * TILE_SIZE
            searching_spot = False

            for brick in forbidden_wall:
                if brick.occupies(x, y):
                    searching_spot = True

            if snake.occupied(x, y):
                searching_spot = True

        self.x, self.y = x, y


class Snake:
    def __init__(self, x: int, y: int) -> None:
        self._ocupies = [(x * TILE_SIZE, y * TILE_SIZE)]
        self._direction = (1, 0)
        self._grow = 0
        self._last_direction = (1, 0)

        self.grow(3)

    def get_head(self) -> Tuple[int, int]:
        return self._ocupies[0]

    def set_direction(self, x: int, y: int) -> None:
        # if self._last_direction != (-x, -y):
        self._last_direction = self._direction
        self._direction = (x, y)

    def grow(self, n: int) -> None:
        self._grow += n

    def step(self, forbidden: List) -> bool:
        next_tile = self._ocupies[0][0] + self._direction[0] * TILE_SIZE, self._ocupies[0][1] + self._direction[1] * TILE_SIZE

        if self.occupied(next_tile[0], next_tile[1]):
            return False

        for brick in forbidden:
            if brick.occupies(next_tile[0], next_tile[1]):
                return False

        self._ocupies.insert(0, next_tile)

        if self._grow != 0:
            self._grow -= 1
        else:
            self._ocupies.pop()

        return True

    def occupied(self, x: int, y: int) -> bool:
        return (x, y) in self._ocupies

    def draw(self, surface: pygame.Surface) -> None:
        for tile in self._ocupies:
            surface.fill(
                (216, 217, 204),
                pygame.Rect(
                    tile[0],
                    tile[1],
                    TILE_SIZE,
                    TILE_SIZE
                )
            )


def main():
    width = 50
    height = 25
    speed = 7

    pygame.init()
    screen = pygame.display.set_mode((
        TILE_SIZE * width,
        TILE_SIZE * height
    ))

    clock = pygame.time.Clock()

    # TODO: Spielobjekte anlegen
    wall = [Brick(x, y)
            for x in range(width)
            for y in range(height)
            if x == 0 or x == width - 1
            or y == 0 or y == height - 1
            or (x == random.randint(1, width - 1) and y != int(height / 2))
            ]

    snake = Snake(int(width / 2), int(height / 2))

    cherry = Cherry()
    cherry.move(wall, snake, width, height)

    running = True
    while running:
        screen.fill((114, 115, 110))

        # TODO: Mauer zeichnen
        for brick in wall:
            brick.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Spiel beenden
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # TODO: Richtung aendern: nach links
                    snake.set_direction(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    # TODO: Richtung aendern: nach rechts
                    snake.set_direction(1, 0)
                elif event.key == pygame.K_UP:
                    # TODO: Richtung aendern: nach oben
                    snake.set_direction(0, -1)
                elif event.key == pygame.K_DOWN:
                    # TODO: Richtung aendern: nach unten
                    snake.set_direction(0, 1)

        if not running:
            break

        # TODO: Schlange bewegen
        if not snake.step(wall):
            running = False

        # TODO: Schlange zeichnen
        snake.draw(screen)

        # TODO: Ueberpruefen, ob die Kirsche erreicht wurde, falls ja, wachsen und Kirsche bewegen.
        x, y = snake.get_head()
        if cherry.occupies(x, y):
            snake.grow(5)
            cherry.move(wall, snake, width, height)

        # TODO: Kirsche zeichnen
        cherry.draw(screen)

        pygame.display.flip()
        clock.tick(speed)

    pygame.display.quit()
    pygame.quit()


if __name__ == '__main__':
    main()
