import pygame
import numpy as np
from math import *

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
caption = "Cube"
pygame.display.set_caption(caption)

# color
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

# matrix
points = []
points.append(np.matrix([-1,-1,1]))
points.append(np.matrix([1,-1,1]))
points.append(np.matrix([1,1,1]))
points.append(np.matrix([-1,1,1]))
points.append(np.matrix([-1,-1,-1]))
points.append(np.matrix([1,-1,-1]))
points.append(np.matrix([1,1,-1]))
points.append(np.matrix([-1,1,-1]))

projection_matrix = np.matrix([
    [1,0,0],
    [0,1,0]
])

scale = 100
angle = 0
circle_pos = [screen_width/2,screen_height/2]

projected_points = [
    [n, n] for n in range(len(points))
]

def connect_points(i,j,points):
    pygame.draw.line(
        screen,black,(points[i][0],points[i][1]), (points[j][0],points[j][1]))

music = pygame.mixer.music.load('music.wav')
pygame.mixer.music.play(-1)
# running
clock = pygame.time.Clock()
run = True
while run:

    clock.tick(60)
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    
    rotate_z = np.matrix([
        [cos(angle),-sin(angle),0],
        [sin(angle),cos(angle),0],
        [0,0,1]
    ])

    rotate_x = np.matrix([
        [1,0,0],
        [0,cos(angle),-sin(angle)],
        [0,sin(angle),cos(angle)]
    ])

    rotate_y = np.matrix([
        [cos(angle),0,sin(angle)],
        [0,1,0],
        [-sin(angle),0,cos(angle)]
    ])

    angle += 0.03
    
    i = 0
    for point in points:
        rotated2d = np.dot(rotate_z,point.reshape(3,1))
        rotated2d = np.dot(rotate_y,rotated2d)
        projected2d = np.dot(projection_matrix,rotated2d)
        x = int(projected2d[0][0] * scale) + circle_pos[0]
        y = int(projected2d[1][0] * scale) + circle_pos[1]

        projected_points[i] = [x, y]
        pygame.draw.circle(screen,black,(x,y),5)
        i += 1


    
    for i in range(4):
        connect_points(i,(i+1)%4,projected_points)
        connect_points(i+4,((i+1)%4)+4,projected_points)
        connect_points(i,(i+4),projected_points)



    pygame.display.update()

pygame.quit()