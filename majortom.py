import math
from typing import Optional, List

import pygame
from dataclasses import dataclass
from math import  sin,cos,pi,sqrt

from pygame.surface import Surface

from asteroid import Asteroid
from framework import fenster_breite, fenster_höhe
from levels import Level, levels
from mond import Mond
from rakete import Rakete

pygame.init()



#Fenster öffnen

pygame.display.set_mode((fenster_breite,fenster_höhe))
screen = pygame.display.set_mode((fenster_breite, fenster_höhe))

pygame.display.set_caption("MajorTom")

spielaktiv = True
clock = pygame.time.Clock()


def draw(level: Level):
    screen.blit(level.hintergrund,(0,0))
    for body in level.bodies:
        body.draw(screen)


def chek_kollison(objekt1, objekt2) -> bool:
    abstand = sqrt((objekt1.x - objekt2.x) ** 2 + (objekt1.y - objekt2.y) ** 2)
    return abstand < objekt1.radius + objekt2.radius


def kollisionen(bodies: list):#[Body]):
    n = len(bodies)
    for i in range(n):
        for j in range(i+1,n):
            b1 = bodies[i]
            b2 = bodies[j]
            if chek_kollison(b1, b2):
                b1.kollision(b2)
                b2.kollision(b1)

# ----------------------------------------------------------------------------move
def move(level: Level):
    for body in level.bodies:
        body.move(level.bodies)


level_zähler = 0
level = levels[0]

#==============================================================================================Main_wihle
while spielaktiv:
    #Überprüfen, ob Nutzer eine Aktion durchgeführt hat
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spielaktiv = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

    move(level)
    kollisionen(level.bodies)
    if level.mission_erfüllt():
        level_zähler += 1
        level = levels[level_zähler]
    draw(level)

    # Fenster aktualisieren
    pygame.display.flip()

    # Refresh-Zeiten festlegen
    clock.tick(60) # 60fps

pygame.quit()
