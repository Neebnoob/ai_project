#https://youtu.be/9H27CimgPsQ?si=wVoWMLouFUf7wQ6O&t=5583
#up until 1:33:00

from board import boards
import pygame
import math

pygame.init()

WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
level = boards  #FOR MULTIPLE LEVELS --> level = boards[active_level]
color = 'blue'
PI = math.pi
player_images = []

#Loads Pacman assets
player_images.append(pygame.transform.scale(pygame.image.load(f'assets/Pacman/PacmanOpen.png'), (45, 45)))
player_images.append(pygame.transform.scale(pygame.image.load(f'assets/Pacman/PacmanSlightOpen.png'), (45, 45)))
player_images.append(pygame.transform.scale(pygame.image.load(f'assets/Pacman/PacmanClosed.png'), (45, 45)))
player_images.append(pygame.transform.scale(pygame.image.load(f'assets/Pacman/PacmanSlightOpen.png'), (45, 45)))


player_x = 450
player_y = 663
direction = 0
counter = 0
flicker = False
#R, L, U, D
turns_allowed = [False, False, False, False]
direction_command = 0
#MAKE ADJUSTABLE LATER
player_speed = 2


def draw_board():
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)

    #REFERENCE pacman pierces.PNG

    #Calls upon board.py

    # 0 = empty black rectangle, 1 = dot, 2 = big dot, 3 = vertical line,
    # 4 = horizontal line, 5 = top right, 6 = top left, 7 = bot left, 8 = bot right
    # 9 = gate
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1: #x(starts at middle), y(top of tile), radius
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker: #x(starts at middle), y(top of tile), radius
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3: #x(starts at middle), y(top of tile, bottom of file), thickness
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1), 
                                (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4: #x(starts at left), y(top of tile, bottom of file), thickness
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)), 
                                (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5: #x(Moves rectange left, Moves rectange down), y(start in radians, end in radians, thickness)
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) -2, (i * num1 + (0.5 * num1)), num2, num1], 0, PI / 2, 2)
            if level[i][j] == 6: #x(Moves rectange right, Moves rectange down), y(start in radians, end in radians, thickness)
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 2)
            if level[i][j] == 7: #x(Moves rectange right, Moves rectange up), y(start in radians, end in radians, thickness)
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI, 3*PI / 2, 2)
            if level[i][j] == 8: #x(Moves rectange left, Moves rectange up), y(start in radians, end in radians, thickness)
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4) -2), (i * num1 - (0.4 * num1)), num2, num1], 3*PI / 2, 2*PI, 2)
            if level[i][j] == 9: #x(starts at left), y (top of tile, bottom of file), thickness
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)), 
                                (j * num2 + num2, i * num1 + (0.5 * num1)), 3)

def draw_player():
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))

def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15
    # check collisions based on center x and center y of player +/- fudge number
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True
    #player is already heading up (2) or down (3)
        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
    #player is already heading right (0) or left (1)                
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns

def move_player(play_x, play_y):
    # R, L, U, D
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y
    


run = True
while run:
    timer.tick(fps)
    #controls the timer for pacman
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False #Used for the big white dots to flash
    else:
        counter = 0
        flicker = True


    screen.fill('black')
    draw_board()
    draw_player()
    #sets position of plater
    center_x = player_x + 23
    center_y = player_y + 24
    turns_allowed = check_position(center_x, center_y)
    player_x, player_y = move_player(player_x, player_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction


    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3


        #offscreen mechanics
    if player_x > 900:
        player_x = -47
    elif player_x < -50:
        player_x = 897

    pygame.display.flip()
pygame.quit()