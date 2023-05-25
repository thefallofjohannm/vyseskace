import pygame
from PIL import Image  # naimportuj knihuvnu pro praci s obrazky
import random
import numpy as np  # knihovna na praci s maticemi

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (200, 200, 100)
BLUE = (0, 0, 255)
LBLUE = (200, 200, 255)
YELLOW = (253, 218, 13)
COIN = (25, 21, 13)


def draw_tree(screen, x, y):
    pygame.draw.rect(screen, BROWN, [60 + x, 170 + y, 30, 45])
    pygame.draw.polygon(screen, GREEN, [[150 + x, 170 + y], [75 + x, 20 + y], [x, 170 + y]])
    pygame.draw.polygon(screen, GREEN, [[140 + x, 120 + y], [75 + x, y], [10 + x, 120 + y]])


def draw_sun(screen, x, y):
    pygame.draw.ellipse(screen, YELLOW, [900, 100, 50, 50])
    pygame.draw.line(screen, YELLOW, [900 - 10, 100 - 10], [1000 + 10, 150 + 10], 2)
    pygame.draw.line(screen, YELLOW, [900 - 10, 100 - 10], [1000 + 10, 150 + 10], 2)
    pygame.draw.line(screen, YELLOW, [900 - 10, 100 - 10], [1000 + 10, 150 + 10], 2)
    pygame.draw.line(screen, YELLOW, [900 - 10, 125 - 10], [1000 + 10, 125 + 10], 2)


def draw_background(screen):
    screen.fill(LBLUE)
    draw_tree(screen, 20, 450)
    draw_sun(screen, 300, 100)
    # toto je moje pozadí


def draw_ground(screen):
    pygame.draw.rect(screen, WHITE,
                     [0, screen.get_height() - 43, screen.get_width(), 43], 30)
    # toto je spodní hranice. Je tam spíš z graifckých než užitových důvodů


"""def snow(screen):
        x = random.randrange(0, screen.get_width())  # kdyz zmenim okno bude to fungoat
        y = random.randrange(0, screen.get_height())
        pygame.draw.circle(screen, COIN, [x, y], 10)
    #toto je COIN, ale funguje tak, že se mi to někde ranodm ukazuje"""


class Block:  # toto jsou moje bloky, na které chci skákat
    def __init__(self, screen, y):
        self.screen = screen
        self.width = 50
        self.height = 10
        self.color = BLUE
        self.position_x = random.randint(self.width, screen.get_width() - self.width)  # ohraničení, aby nebyly všude
        self.position_y = y

    def draw(self):
        pygame.draw.rect(self.screen,
                         self.color,
                         [self.position_x, self.position_y, self.width, self.height],
                         10)

    def shift(self):
        self.position_y += 1  # posune se blok

    def __str__(self):
        return f"x:{self.position_x}, y:{self.position_y}"
    #když se pokusíš ten objekt konvertovat na string, tak se promění ve string, obsahující informace o poloze





# player player player player player player player player
class Player:

    def __init__(self, screen, x, y):
        self.screen = screen
        self.size = 15
        self.color = RED
        self.position = np.array([x, y])
        self.movement_vector = np.array([0, 0])  # ted je to vektor
        self.gravity_acceleration = 1
        self.gravity_update_tick = 0

    def gravity(self):
        if self.gravity_update_tick >= 5:
            self.movement_vector[1] += self.gravity_acceleration  # postupně se lineárně zrychluje
            self.gravity_update_tick = 0
        else:
            self.gravity_update_tick += 1

    def update_position(self):
        self.gravity()
        self.position += self.movement_vector
        if self.position[1] == 642:
            self.movement_vector = [0, 0]
            self.gravity_acceleration = 0
        else:
            self.gravity_acceleration = 1

    def draw(self):  # aktualizuje mi, kde je zrovna Player tím, že se znovu vykreslí
        pygame.draw.rect(self.screen,
                         self.color,
                         [self.position[0], self.position[1], self.size, self.size], self.size)

    def ground_stop(self):
        self.movement_vector = [0, 0]
        self.gravity_acceleration = 0

    def jump(self):
        self.movement_vector[1] = -5

    def go_left(self):
        self.movement_vector[0] = -5

    def go_right(self):
        self.movement_vector[0] = 5



