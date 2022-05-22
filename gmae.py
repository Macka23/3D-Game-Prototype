import pygame
import math
from pygame.locals import *

#initialize pygame
pygame.init()
screen_surface = pygame.display.set_mode((2000, 1000))
clock = pygame.time.Clock()
# Colors
black = 0, 0, 0
white = 255, 255, 255
green = 154, 205, 50
red = 255, 0, 0
yellow = 255, 255, 0
pink = 255, 153, 153
blue = 0, 0, 25
grey = 211, 211, 211
# Background surface
background = pygame.Surface(screen_surface.get_size())
background.fill(black)

# Surface of red ball
surf_red_ball = pygame.Surface(screen_surface.get_size())
surf_red_ball.set_colorkey((0, 0, 0))

map =  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


player_x, player_y = 300, 300

angle_of_cam = 0
delta_x = 0
delta_y = 0
pi = math.pi
FOV =  pi/3
HALF_FOV = pi / 6
casted_rays = 125
step_angle = FOV / casted_rays
max_depth = 2000
scale = 1000 / casted_rays

def ray_casting():
    start_angle = angle_of_cam - HALF_FOV

    for ray in range(casted_rays):
        for depth in range(max_depth):
            target_x = player_x + math.cos(start_angle) * depth
            target_y = player_y + math.sin(start_angle) * depth

            #convert target Y into map row
            if target_y - (math.floor(target_y ) * 100) >= 50:
                row = math.ceil(target_y / 100)
            else:
                row = math.floor(target_y / 100)

            col = math.floor(target_x / 100)


            if (row > 0 or row < 1000) and (col > 0 or col < 1000):
                if map[row][col] == 1:
                    pygame.draw.line(surf_red_ball, red, (player_x, player_y), (target_x , target_y), 1)


                    # draw 3D projection
                    color = 255 / (1 + depth * depth * 0.0001)

                    # fix visual
                    depth *= math.cos(angle_of_cam - start_angle)

                    #calculate wall height
                    wall_height = 21000 / (depth + 0.0001)




                    pygame.draw.rect(background, (color, color, color), (1000 + ray * scale, 500 - wall_height/2, scale, wall_height))

                    break


        start_angle += step_angle

def draw_map():
    posiy = 0
    for y in map:
        posix = 0
        for x in y:
            if x == 0:
                pygame.draw.rect(background, pink, (posix, posiy, 100, 100), 0)
            else:
                pygame.draw.rect(background, grey, (posix, posiy, 100, 100), 0)

            pygame.draw.rect(background, black, (posix, posiy, 100, 100), 1)
            posix += 100
        posiy += 100

draw_map()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
    key = pygame.key.get_pressed()

    #draw floor and ceiling
    pygame.draw.rect(background, green, (1000, 500, 1000, 500))
    pygame.draw.rect(background, grey, (1000, 0, 1000, 500))

    if player_y - (math.floor(player_y) * 100) >= 50:
        row = math.ceil((player_y) / 100)
    else:
        row = math.floor((player_y) / 100)

    col = math.floor((player_x) / 100)

    if key[K_z]:
        if map[row][col] == 1:
            pass
        player_y -= 5

    if key[K_s]:
        if map[row][col] == 1:
            pass
        player_y += 5


    if key[K_q]:
        if map[row][col] == 1:
            pass
        player_x -= 5

    if key[K_d]:
        if map[row][col] == 1:
            pass
        player_x += 5

    if key[K_LEFT]:
        angle_of_cam -= 0.1
        if angle_of_cam < 0:
            angle_of_cam += 2 * pi

    if key[K_RIGHT]:
        angle_of_cam += 0.1
        if angle_of_cam > 2 * pi:
            angle_of_cam -= 2 * pi


    surf_red_ball.fill((0, 0, 0, 0))

    #player
    pygame.draw.circle(surf_red_ball, red, (player_x, player_y), 25, 0)


    ray_casting()

    screen_surface.blit(background, (0, 0))
    screen_surface.blit(surf_red_ball, (0, 0))
    clock.tick(30)
    pygame.display.flip()
