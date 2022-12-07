import pygame as pg
import math as m
from player import Player
from map import Map
import trois_D as D

pg.init()

width_x, width_y = 1300,700
screen = pg.display.set_mode((width_x,width_y))
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
pix_size = TS * map.MAP_SIZE
print(pix_size)
diago = m.sqrt(2 * (map.MAP_SIZE * TS) ** 2)
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

    if get_pressed[pg.K_z] and Verif(player.x - plus_x, player.y - plus_y):  # Si la case n'est pas un mur
        player.x, player.y = player.x - plus_x, player.y - plus_y

    if get_pressed[pg.K_s] and Verif(player.x + plus_x, player.y + plus_y):
        player.x, player.y = player.x + plus_x, player.y + plus_y

    if get_pressed[pg.K_d] and Verif(player.x + d_x, player.y + d_y):
        player.x, player.y = player.x + d_x, player.y + d_y

    if get_pressed[pg.K_q] and Verif(player.x + g_x, player.y + g_y):
        player.x, player.y = player.x + g_x, player.y + g_y

    if get_pressed[pg.K_1]:
        player.rotation = 0
    elif get_pressed[pg.K_2]:
        player.rotation = m.radians(90)
    elif get_pressed[pg.K_3]:
        player.rotation = m.radians(180)
    elif get_pressed[pg.K_4]:
        player.rotation = m.radians(270)
    elif get_pressed[pg.K_5]:
        player.x, player.y = map.MAP_SIZE / 2 * TS, map.MAP_SIZE / 2 * TS

    if get_pressed[pg.K_e]:
        if m.degrees(player.rotation) + 360 < 10 ** (-3):  # S'assure que l'angle est au maximum 360°
            player.rotation = 0
        elif player.rotation < 10 ** (-5):  # Et la on s'assure qu'il est > 0
            player.rotation = m.radians(360) - (player.rotation - sensi)
        else:
            player.rotation = round(player.rotation - sensi, 3)

    if get_pressed[pg.K_a]:
        if m.degrees(player.rotation) > 360:  # Et la on s'assure qu'il est > 0
            player.rotation = round(player.rotation - m.radians(360) + sensi, 3)
        elif abs(m.degrees(player.rotation) - 360) < 10 ** (-3):
            player.rotation = 0
        else:
            player.rotation = round(player.rotation + sensi, 3)

    # Pour eviter d'avoir des angle >  à 360


def Verif(x_index, y_index):
    return False if map.map[int(y_index / TS)][int(x_index / TS)] != 0 else True


def UpDepth(i, depth):
    if i == 1:
        return depth + TS
    else:
        return depth - TS


def InMap(coord):
    return True if 0 < coord < pix_size else False


# Sin = x et cos = y
def Distance(a, b):
    return m.sqrt(((a ** 2) + (b ** 2)))


def Check(in_map, coord):
    if in_map:
        for x in range(-1, 2):
            for y in range(-1, 2):
                if not Verif(coord[0] + x, coord[1] + y):
                    pg.draw.circle(screen, pg.Color("dark red"), coord, 3)
                    return True
    else:
        return True


def RayCalcul(rot_ray,fov):
    wall = False
    rot_d = m.degrees(player.rotation)+rot_ray
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

    if rot_d == 0 or rot_d == 180:
        while not wall:
            y_coord = (player.x, y_depth)
            if not Verif(y_coord[0], y_coord[1]):
                return (y_coord[0], y_coord[1] + TS if rot_d == 0 else y_coord[1] - 1), rot_d
            y_depth = UpDepth(ry, y_depth)

    elif rot_d == 90 or player.rotation == 270:
        while not wall:
            x_coord = (x_depth, player.y)
            if not Verif(x_coord[0], x_coord[1]):
                return (x_coord[0] + TS if rot_d == 90 else x_coord[0] - 1, x_coord[1]), rot_d
            x_depth = UpDepth(rx, x_depth)

    else:
        while not wall:
            x_coord = (x_depth, player.y + (x_depth - player.x) * x_slope)
            y_coord = (player.x + (y_depth - player.y) * y_slope, y_depth)

            pg.draw.circle(screen, (0, 255, 255), x_coord, 3)
            pg.draw.circle(screen, (0, 255, 255), y_coord, 5)

            d_x, d_y = Distance(x_depth, x_depth * x_slope), Distance(y_depth, y_depth * y_slope)

            verif_x = Check(InMap(x_coord[1]), x_coord)
            verif_y = Check(InMap(y_coord[0]), y_coord)

            if d_x < d_y:
                x_depth = UpDepth(rx, x_depth)

                if verif_x and not verif_y:
                    y_depth = UpDepth(ry, y_depth)
                elif verif_y and not verif_x:
                    return y_coord, rot_d
                elif verif_x and verif_y:
                    return x_coord, rot_d
                else:
                    x_depth = UpDepth(rx, x_depth)

            elif d_y < d_x:
                if verif_x and not verif_y:
                    y_depth = UpDepth(ry, y_depth)
                elif verif_y and not verif_x:
                    return y_coord, rot_d
                elif verif_x and verif_y:
                    return y_coord, rot_d
                else:
                    y_depth = UpDepth(ry, y_depth)

            elif d_x == d_y:

                y_depth = UpDepth(ry, y_depth)
                x_depth = UpDepth(rx, x_depth)
                if not verif_x and verif_y:
                    return y_coord,rot_d
                elif verif_x:
                    return x_coord, rot_d


def RayCasting():
    fov = 100
    for i in range(fov):
        end_coord, rot_d = RayCalcul(i,fov)
        D.frame(player.x, player.y, end_coord, screen, width_x, width_y, TS, fov, rot_d)
    draw_minimap()
    end_coord, rot_d = RayCalcul(0, fov)
    pg.draw.line(screen, pg.Color("green"), (player.x, player.y), end_coord)


# Game Loop

while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((0, 0, 0))

    Deplacements()
    RayCasting()


    # Création du joueur
    pg.draw.circle(screen, pg.Color("red"), (player.x, player.y), 4)
    pg.draw.circle(screen, pg.Color("red"), (player.x, player.y), TS / 3, width=1)

    pg.draw.line(screen, (255, 0, 0), (player.x, player.y),
                 (player.x - m.sin(player.rotation) * TS / 2, player.y - m.cos(player.rotation) * TS / 2))

    # Update de l'image
    pg.display.flip()
    clock.tick(60)

pg.quit()
