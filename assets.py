import pygame
from PIL import Image  # naimportuj knihuvnu pro praci s obrazky
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (200, 200, 100)


def draw_tree(screen, x, y):
    pygame.draw.rect(screen, BROWN, [60 + x, 170 + y, 30, 45])
    pygame.draw.polygon(screen, GREEN, [[150 + x, 170 + y], [75 + x, 20 + y], [x, 170 + y]])
    pygame.draw.polygon(screen, GREEN, [[140 + x, 120 + y], [75 + x, y], [10 + x, 120 + y]])


def get_background(w, h):
    img = Image.open("background.jpeg")
    img.resize((w, h))
    return pygame.image.frombuffer(img.tobytes(), (w, h), "RGB")


def snow(screen):
    for i in range(50):
        x = random.randrange(0, screen.get_width()) #kdyz zmenim ikni bzude to fungoat
        y = random.randrange(0, screen.get_height())
        pygame.draw.circle(screen, WHITE, [x, y], 2)


class Block:
    def __init__(self, screen, y):
        self.screen = screen
        self.width = 50
        self.height = 10
        self.color = WHITE
        self.position_x = random.randint(0,screen.get_width() - self.width)
        self.position_y = y

    def draw(self):
        pygame.draw.rect(self.screen,
                         self.color,
                         [self.position_x, self.position_y, self.width, self.height],
                         3)

    def shift(self):
        self.position_y += 1 #posune se blok o neco

    def __str__(self):
        return f"x:{self.position_x}, y:{self.position_y}"