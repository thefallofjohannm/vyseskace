from config import *
import pygame
import math
from Block import Block
from jumper import Jumper
from platforms import *
from coin import *
from io import BytesIO



#stromeček na pozadí
def draw_tree(screen, x, y):
    pygame.draw.rect(screen, BROWN, [60 + x, 170 + y, 30, 45])
    pygame.draw.polygon(screen, GREEN2, [[150 + x, 170 + y], [75 + x, 20 + y], [x, 170 + y]])
    pygame.draw.polygon(screen, GREEN2, [[140 + x, 120 + y], [75 + x, y], [10 + x, 120 + y]])


#slunko na pozadí
def draw_sun(screen, *_):
    X, Y, r, rr, N = 900, 100, 80, 80, 7
    pygame.draw.ellipse(screen, YELLOW, [X-rr//2, Y-rr//2, rr, rr])

    for angle in [math.pi*i/N for i in range(N)]:
        start = [900+r*math.cos(angle), 100 + r*math.sin(angle)]
        end = [900+r*math.cos(angle+math.pi), 100 + r*math.sin(angle+math.pi)]
        pygame.draw.line(screen, YELLOW, start, end, width=5)
    # pygame.draw.line(screen, YELLOW, [885, 85], [965, 165], 2)  # diagonalni
    # pygame.draw.line(screen, YELLOW, [925, 75], [925, 175], 2)
    # pygame.draw.line(screen, YELLOW, [965, 85], [885, 165], 2)  # diagonalni
    # pygame.draw.line(screen, YELLOW, [975, 125], [875, 125], 2)


def draw_background(screen):
    screen.fill(LBLUE)
    draw_tree(screen, 20, 450)
    draw_sun(screen, 300, 100)


#spodek, aby to mělo nějakou pěknou hranici
def draw_ground(screen):
    pygame.draw.rect(screen, WHITE,
                     [0, screen.get_height() - 43, screen.get_width(), 43], 30)


#funkce pro fake bloky, které mají zmást hráče, aby měly
#limitaci pro to, kde se objeví
def get_height_of_heighest_block(screen, blocks):
    o = screen.get_height() - 100
    for b in blocks:
        if o > b.position_y:
            o = b.position_y
    return o


#aby se random zobrazovaly bloky
def update_blocks(screen, blocks, number_of_blocks):
    # dopln pocet bloku do number_of_blocks
    for i in range(0, number_of_blocks - len(blocks)):
        # vyrob novy blok
        blocks.append(Block(screen, get_height_of_heighest_block(screen, blocks) - 50))

    
    new_blocks = list()
    for b in blocks:
        if b.position_y < screen.get_height():
            b.shift()
            b.draw()
            new_blocks.append(b)
    return new_blocks


#toto mi ukazuje skore na obrazovce
def draw_score(screen, score):
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(text,(900,10))



def game_init():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("You jump and have fun")
    screen.fill(LBLUE)
    pygame.display.flip()
    clock = pygame.time.Clock()
    clock.tick(60)
    player = Jumper(screen, 200, 10)

    #soundtrack
    with open('OfGodsAndPhilosophers(loop)(120).wav', 'rb') as wav_file:
        wav_data = wav_file.read()

    wav_file = BytesIO(wav_data)
    soundtrack = pygame.mixer.Sound(wav_file)

    soundtrack.play(-1) # hraj dokola

        #soundefects

    with open('Stinger_Fail4.wav', 'rb') as wav_file_2:
        wav_data_2 = wav_file_2.read()

    wav_file_2 = BytesIO(wav_data_2)
    fail_sound = pygame.mixer.Sound(wav_file_2)

    with open('Stinger_Success6.wav', 'rb') as wav_file_3:
        wav_data_3 = wav_file_3.read()

    wav_file_3 = BytesIO(wav_data_3)
    five_times_collect_sound = pygame.mixer.Sound(wav_file_3)



    blocks = list()
    number_of_blocks = 5

    #platformy, na které se dá skákat
    platforms = pygame.sprite.Group()
    platforms.add(
        Platform(100, 400, 50, 10,  2),  # x,y,width, height
        Platform(200, 100, 30, 10,  3),
        Platform(300, 600, 50, 10,  1),
        Platform(400, 550, 20, 10,  4),
        Platform(500, 52,  30, 10,  1),
        Platform(600, 420, 50, 10,  3),
        Platform(700, 69,  50, 10,  2),
        Platform(800, 51,  20, 10,  8),
        Platform(900, 320, 20, 10, 1),
        Platform(1000, 500, 50, 10, 2),
    )


    #toto je předmět, který mohu sbírat
    coin_group = pygame.sprite.Group()
    coin = Coin(screen)
    coin_group.add(coin)

    return dict(clock=clock, screen=screen,
                number_of_blocks=number_of_blocks, player=player, blocks=blocks,
                platforms=platforms, coin_group=coin_group, fail_sound=fail_sound,
                five_times_collect_sound  = five_times_collect_sound )



def game(clock, screen, number_of_blocks, player, blocks, platforms, coin_group, fail_sound, five_times_collect_sound):
    done = False
    score = 0


    #hlavní game loop
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            #ovládání šipkami
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()

                elif event.key == pygame.K_RIGHT:
                    player.go_right()

                elif event.key == pygame.K_UP:
                    player.jump(platforms)

                # elif event.key == pygame.K_ESCAPE:
                #     self.__init__()


            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.stop()

            # elif event.type == USEREVENT+1:
            #     draw()
        player.update(platforms)

        draw_background(screen)

        blocks = update_blocks(screen, blocks, number_of_blocks)

        player.draw()

        platforms.update()

        platforms.draw(screen)

        draw_ground(screen)

        coin_group.draw(screen)



        #toto je srážecí podmínka pro sběr té mince/nebo předmětu
        for coin in coin_group:
            if player.rect.colliderect(coin.rect):
                coin.spawn()
                score += 936

                five_times_collect_sound.play()
                #původně mělo být 5x ale ono je celkem uspech i jednou

     # omezení pohybu v rámci hrací plochy
        if player.position[0] >= 1085:
            player.position[0] = 1085
        if player.position[0] <= 0:
            player.position[0] = 0

        if player.position[1] <= -5:
            player.position[1] = -5

        # respawn
        if 6000 >= player.position[1] >= 700:
            player.stop_movement()
            player.position[0] = 200
            player.position[1] = 10
            score = 0
            fail_sound.play()


        draw_score(screen, score)


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
