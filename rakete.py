from dataclasses import dataclass
from math import sin, pi
from math import cos

import pygame

from framework import Body, skaliere_vector, geschwindikeits_differenz, fenster_breite

raketeo = pygame.image.load("Raketeo.png")
raketeo = pygame.transform.scale(raketeo, (60,60))

raketef = pygame.image.load("RaketeF.png")
raketef = pygame.transform.scale(raketef, (60,60))


@dataclass
class Rakete(Body):
    winkel: float = 0
    stabilität: float = 3
    masse: float = 10
    radius: float = 30
    x_geschwi: float = 2
    y_geschwi: float = 0
    x: float = fenster_breite // 2
    y: float = fenster_breite // 4
    bildausrichtung: float = 45.
    schub: float = 0.15

    def move(self, bodies: list):#[Body]):
        if not self.ist_explodiert():
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.turn(5)
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                self.turn(-5)
            if pygame.key.get_pressed()[pygame.K_UP]:
                self.klebt_an = None
                self.push()
        super().move(bodies)

    def push(self):
        self.x_geschwi += cos(self.winkel * pi / 180) * self.schub
        self.y_geschwi += -sin(self.winkel * pi / 180) * self.schub

    def draw(self,screen):
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.bild = raketef
        else:
            self.bild = raketeo
        super().draw(screen)

    def kollision(self, other: "Body"):
        from mond import Mond
        from asteroid import Asteroid
        if isinstance(other, Mond):
            self.kollision_mond(other)
        if isinstance(other, Asteroid):
            self.explodiere()

    def kollision_mond(self, mond: "Mond"):
        self.klebt_an = mond
        abstand_x = self.x - mond.x
        abstand_y = self.y - mond.y
        self.klebestelle_x, self.klebestelle_y = skaliere_vector( (abstand_x, abstand_y), mond.radius+self.radius+1)

        geschwie_differenz = geschwindikeits_differenz(self, mond)
        if geschwie_differenz > self.stabilität:
            self.explodiere()














