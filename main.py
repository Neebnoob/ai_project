#https://youtu.be/9H27CimgPsQ?si=eZ4mH0eMdhrtBpFT&t=2515
#up until 42:00

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




def draw_board():
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)

    #REFERENCE pacman pierces.PNG

    # 0 = empty black rectangle, 1 = dot, 2 = big dot, 3 = vertical line,
    # 4 = horizontal line, 5 = top right, 6 = top left, 7 = bot left, 8 = bot right
    # 9 = gate
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1: #x(starts at middle), y(top of tile), radius
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2: #x(starts at middle), y(top of tile), radius
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
    pass

run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    draw_board()
    draw_player()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.flip()
pygame.quit()