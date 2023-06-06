import pygame.display
from game import game, game_init
from config import *


def main():
    game(**game_init())


if __name__ == "__main__":
    main()
