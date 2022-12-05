import pygame as pg
import math as m
from player import Player
from map import Map

pg.init()

screen = pg.display.set_mode((1600, 800))
pg.display.set_caption("Raycasting")

# Appel de Fonctions

map = Map()
TS = map.TS
player = Player(MAP_SIZE=map.MAP_SIZE, TS=TS)

# Constantes
tailleX, tailleY = screen.get_size()
running = True

speed = 3
sensi = m.radians(1)
angle = m.radians(90)
fov_r = m.radians(100)
radius = 4
diago = m.sqrt((2 * (map.MAP_SIZE * TS ** 2))
print(diago)

clock = pg.time.Clock()


# Fonctions
def draw_minimap():
    for y, line in enumerate(map.map):
        for x, column in enumerate(line):
            pg.draw.rect(
                screen,
                (200, 200, 200) if map.map[y][x] == 0 else (100, 100, 100),
                (x * TS, y * TS, TS, TS))


def Deplacements():
    cos, sin = m.cos(player.rotation), m.sin(player.rotation)
    get_pressed = pg.key.get_pressed()

    # Gestion des collision:
    # Les variable équivalent aux positions suivantes si le joueur fait une action (H G B D)
    plus_x, plus_y = speed * sin, speed * cos  # Bas

    d_x, d_y = speed * m.sin(player.rotation + angle), speed * m.cos(player.rotation + angle)  # Droite
    g_x, g_y = speed * m.sin(player.rotation - angle), speed * m.cos(player.rotation - angle)  # Gauche

    if get_pressed[pg.K_z] and not Verif(player.x - plus_x, player.y - plus_y):  # Si la case n'est pas un mur
        player.x, player.y = player.x - plus_x, player.y - plus_y

    if get_pressed[pg.K_s] and not Verif(player.x + plus_x, player.y + plus_y):
        player.x, player.y = player.x + plus_x, player.y + plus_y

    if get_pressed[pg.K_d] and not Verif(player.x + d_x, player.y + d_y):
        player.x, player.y = player.x + d_x, player.y + d_y

    if get_pressed[pg.K_q] and not Verif(player.x + g_x, player.y + g_y):
        player.x, player.y = player.x + g_x, player.y + g_y

    if get_pressed[pg.K_e]:
        if abs(m.degrees(player.rotation) + 360) < 10 ** (-9):  # S'assure que l'angle est au maximum 360°
            player.rotation = 0
        elif player.rotation < 10 ** (-5):  # Et la on s'assure qu'il est > 0
            player.rotation = m.radians(360) - (player.rotation - sensi)
        else:
            player.rotation -= sensi

    if get_pressed[pg.K_a]:
        if abs(m.degrees(player.rotation) - 360) < 10 ** (-9):
            player.rotation = 0
        else:
            player.rotation += sensi

    # Pour eviter d'avoir des angle >  à 360


def Verif(x_index, y_index):
    return True if map.map[int(y_index / TS)][int(x_index / TS)] != 0 else False


def UpX(rx, x_depth):
    if rx == 1:
        return x_depth + TS
    else:
        return x_depth - TS


def UpY(ry, y_depth):
    if ry == 1:
        return y_depth + TS
    else:
        return y_depth - TS


# Sin = x et cos = y
def Distance(z):
    return m.sqrt(((z[0] ** 2) + (z[1] ** 2)))


def RayCasting():
    wall = False

    # Position dans la map
    #pg.draw.circle(screen, (100, 255, 100), (m.floor(player.x / TS) * TS, m.floor(player.y / TS) * TS), 5)
    #pg.draw.circle(screen, (100, 255, 100), (m.floor(player.x / TS) * TS, m.ceil(player.y / TS) * TS), 5)
    #pg.draw.circle(screen, (100, 255, 100), (m.ceil(player.x / TS) * TS, m.floor(player.y / TS) * TS), 5)
    #pg.draw.circle(screen, (100, 255, 100), (m.ceil(player.x / TS) * TS, m.ceil(player.y / TS) * TS), 5)

    rot_d = m.degrees(player.rotation)
    sin, cos = m.sin(player.rotation), m.cos(player.rotation)

    x_slope = cos / sin if sin != 0 else False
    y_slope = sin / cos if cos != 0 else False

    if rot_d <= 90 or rot_d == 360:
        rx, ry = -1, -1
    elif 90 < rot_d <= 180:
        rx, ry = -1, 1
    elif 180 < rot_d <= 270:
        rx, ry = 1, 1
    elif rot_d > 270 and rot_d != 360:
        rx, ry = 1, -1

    x_depth = m.floor(player.x / TS) * TS if rx == -1 else m.ceil(player.x / TS) * TS
    y_depth = m.floor(player.y / TS) * TS if ry == -1 else m.ceil(player.y / TS) * TS

    while not wall:
        if player.rotation == 0 or player.rotation == m.pi:
            target_x, target_y = player.x, y_depth
            y_depth = UpY(ry, y_depth)
            if Verif(target_x, target_y):
                wall_x, wall_y, wall = target_x, target_y + TS, True

        elif player.rotation == m.radians(90) or player.rotation == m.radians(270):
            target_x, target_y = x_depth, player.y
            x_depth = UpX(rx, x_depth)
            if Verif(target_x, target_y):
                wall_x, wall_y, wall = target_x, target_y, True

        else:
            # target_x, target_y = player.x - sin * d_x * rx, player.y + cos * d_y * ry
            pg.draw.circle(screen, (0, 0, 255), (x_depth, player.y), 3)
            pg.draw.circle(screen, (0, 0, 255), (player.x, y_depth), 5)

            x_coord = (x_depth, x_depth * x_slope)
            y_coord = (y_depth * y_slope, y_depth)

            pg.draw.circle(screen, (0, 255, 255), x_coord, 3)
            pg.draw.circle(screen, (0, 255, 255), y_coord, 5)


            d_x, d_y = Distance(x_coord), Distance(y_coord)


            if abs(x_coord[1]) > diago:
                if Verif(x_coord[0] / TS, x_coord[1] / TS):
                    wall_x, wall_y, wall = x_coord[0], x_coord[1], True

            if abs(y_coord[0]) > diago:
                if Verif(y_coord[0] / TS, y_coord[1] / TS):
                    wall_x, wall_y, wall = y_coord[0], y_coord[1], True

            if d_x < d_y:
                print("-----------------------------")
                print(x_depth)
                x_depth = UpX(rx, x_depth)
                print(x_depth)
            else:
                y_depth = UpY(ry, y_depth)
            #pg.draw.circle(screen, (255, 125, 65), tuple(target_x), 2)
            #pg.draw.circle(screen, (255, 125, 65), tuple(target_y), 2)

    # print((player.x, player.y), (wall_x, wall_y))
    pg.draw.line(screen, pg.Color("green"), (player.x, player.y), (wall_x, wall_y))


# Game Loop

while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((0, 0, 0))

    Deplacements()
    draw_minimap()
    RayCasting()

    # Création du joueur
    pg.draw.circle(screen, pg.Color("red"), (player.x, player.y), radius)
    pg.draw.line(screen, (255, 0, 0), (player.x, player.y),
                 (player.x - m.sin(player.rotation) * TS, player.y - m.cos(player.rotation) * TS))

    # Update de l'image
    pg.display.flip()
    clock.tick(60)

pg.quit()
