import numpy as np
import pygame
from  platforms import Platform
from config import *


class Jumper(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.screen = screen
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.gravity = 1


    def update(self, platforms):
        self.apply_gravity()
        self.apply_movement()
        self.check_platform_collision(platforms)


    #gravitace, která nefunguje jako naše gravitace
    #ale padá konstantní rychlostí
    def apply_gravity(self):
        if self.velocity.y < 10:
            self.velocity.y += self.gravity


    def apply_movement(self):
        self.position += self.velocity
        self.rect.topleft = self.position


    #umožnění kolize
    def check_platform_collision(self, platforms: Platform):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity.y = 0
                    self.position[1] = platform.rect.y



    #funkce pro jednotlivé pohyby
    def jump(self):
        if 0 <= self.velocity.y < 10:
            self.velocity.y = -20


    def draw(self):
        self.screen.blit(self.image, self.rect)


    def stop_movement(self):
        self.velocity = pygame.Vector2(0, 0)


    def go_left(self):
        self.velocity.x = -5


    def go_right(self):
        self.velocity.x = 5


    def stop(self):
        self.velocity.x = 0