from config import *
import pygame

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
def draw_sun(screen, x, y):
    pygame.draw.ellipse(screen, YELLOW, [900, 100, 50, 50])
    pygame.draw.line(screen, YELLOW, [885, 85], [965, 165], 2)  # diagonalni
    pygame.draw.line(screen, YELLOW, [925, 75], [925, 175], 2)
    pygame.draw.line(screen, YELLOW, [965, 85], [885, 165], 2)  # diagonalni
    pygame.draw.line(screen, YELLOW, [975, 125], [875, 125], 2)


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

    platform1  = Platform(100, 400, 50, 10,  2)  # x,y,width, height
    platform2  = Platform(200, 100, 30, 10,  3)
    platform3  = Platform(300, 600, 50, 10,  1)
    platform4  = Platform(400, 550, 20, 10,  4)
    platform5  = Platform(500, 52,  30, 10,  1)
    platform6  = Platform(600, 420, 50, 10,  3)
    platform7  = Platform(700, 69,  50, 10,  2)
    platform8  = Platform(800, 51,  20, 10,  8)
    platform9  = Platform(900, 320, 20, 10, 1)
    platform10 = Platform(1000, 500, 50, 10, 2)

    platforms.add(platform1, platform2, platform3, platform4, platform5, platform6, platform7,
                  platform8, platform9, platform10)

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()

                elif event.key == pygame.K_RIGHT:
                    player.go_right()

                elif event.key == pygame.K_UP:
                    player.jump()


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.stop()

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
