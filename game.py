"""
 Pygame base template for opening a window

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/vRB_983kUMc
"""

import pygame
import random
from assets import *



class VyseSkace:
    def __init__(self):
        self.window_width = 400
        self.window_height = 700
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Bav se")
        # self.screen.blit(get_background(self.window_width, self.window_height))
        self.screen.fill(LBLUE)
        pygame.display.flip()
        self.clock = pygame.time.Clock()
        self.clock.tick(60)
        self.snow_tick_count = 0
        self.blocks = list()
        self.number_of_blocks = 15
        self.player = Player(self.screen, 200, 642) #umístění hráče

    def game_loop(self):
        done = False

        # -------- Hlavní Program Loop -----------

        while not done:
            draw_background(self.screen)

            # --- Hlavní event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                #ovládání pomocí šipek
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.movement_vector = [-5,0]
                    elif event.key == pygame.K_RIGHT:
                        self.player.movement_vector = [5, 0]
                    elif event.key == pygame.K_UP:
                        self.player.movement_vector = [0, -15]
                    elif event.key == pygame.K_DOWN:
                        self.player.movement_vector = [0, 5]

                elif event.type == pygame.KEYUP:

                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.player.movement_vector[0] = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.player.movement_vector[1] = 0



            # --- Game logic

            self.update_blocks()

            #snow(self.screen)

            self.player.update_position()
            self.player.draw()



            self.player.position[0] = self.player.position[0] + self.player.movement_vector[0]
            self.player.position[1] = self.player.position[1] + self.player.movement_vector[1]

            #omezení na souřadnice, pohyb hráče
            if self.player.position[0] >= 385:
                self.player.position[0] = 385
            if self.player.position[0] <= 0:
                self.player.position[0] = 0

            if self.player.position[1] <= -5:
                self.player.position[1] = -5

            if self.player.position[1] <= 6000 and self.player.position[1]  >= 1200:
                self.player.ground_stop()
                self.player.position[0] = 200
                self.player.position[1] = 642







            # --- Screen-clearing code goes here

            # Here, we clear the screen to white. Don't put other drawing commands
            # above this, or they will be erased with this command.

            # If you want a background image, replace this clear with blit'ing the
            # background image.

            # --- Drawing code should go here

            # --- Go ahead and update the screen with what we've drawn.
            draw_ground(self.screen)
            pygame.display.flip()
            self.clock.tick(60)


        # Close the window and quit.
        pygame.quit()

    def update_blocks(self):
        for i in range(0, self.number_of_blocks - len(self.blocks)):
            self.blocks.append(Block(self.screen, self.get_height_of_heighest_block() - 50))

        new_blocks = list()
        for b in self.blocks:
            if b.position_y < self.screen.get_height():
                b.shift()
                b.draw()
                new_blocks.append(b)
        self.blocks = new_blocks

    def get_height_of_heighest_block(self):
        o = self.screen.get_height() - 100
        for b in self.blocks:
            if o > b.position_y:
                o = b.position_y
        return o
