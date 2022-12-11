from dataclasses import dataclass
from math import sqrt
from typing import Optional, List

import pygame
from pygame.surface import Surface

fenster_breite = 1000
fenster_höhe = 1000


explosioni = pygame.image.load("explosion.png")
explosioni = pygame.transform.scale(explosioni, (50,50))



@dataclass
class Body:
    x: float
    y: float
    bild: Optional[Surface] = None
    stabilität: int = 1000
    winkel: float = 0
    masse:float = 0
    radius:float =0
    klebt_an:Optional["Body"] = None
    klebestelle_x: float = 0
    klebestelle_y: float = 0
    x_geschwi: float = 0
    y_geschwi: float = 0
    skraft: bool = True
    bildausrichtung: float = 0

    def __post_init__(self):
        self.explosion_time = None

    def explodiere(self):
        self.explosion_time = pygame.time.get_ticks()

    def ist_explodiert(self):
        return self.explosion_time is not None

    def turn(self,change):
        self.winkel = self.winkel - change
        if self.winkel > 360:
            self.winkel -= 360
        if self.winkel < 0:
            self.winkel += 350


    def draw(self,screen):
        image = self.bild
        if self.explosion_time is not None:
            delta_t = pygame.time.get_ticks() - self.explosion_time
            if delta_t > 1000:
                image = None
            else:
                image = explosioni

        if image is not None:
            image = pygame.transform.rotate(image, self.winkel - self.bildausrichtung)
            screen.blit(image, (int(self.x - image.get_width() / 2), self.y - int(image.get_height() / 2)))


    def kollision(self, other: "Body"):
        pass

    def move(self, bodies: List):#["Body"]):
        if self.klebt_an is None:
            self.freie_bewegung(bodies)
        else:
            self.angeklebte_bewegung()

    def angeklebte_bewegung(self):
        self.x = self.klebt_an.x + self.klebestelle_x
        self.y = self.klebt_an.y + self.klebestelle_y
        self.x_geschwi = self.klebt_an.x_geschwi
        self.y_geschwi = self.klebt_an.y_geschwi

    def freie_bewegung(self, bodies):
        if self.skraft:
            for body in bodies:
                if body!=self and body.masse:
                    schwerkraft(self, body)

        self.x += self.x_geschwi
        self.y += self.y_geschwi






def schwerkraft(objekt1,objekt2):
    abstand = sqrt((objekt1.x-objekt2.x)**2+(objekt1.y-objekt2.y)**2)
    beschleuigung_x = (objekt1.x-objekt2.x)/abstand**3
    beschleuigung_y = (objekt1.y-objekt2.y)/abstand**3

    objekt1.x_geschwi += -beschleuigung_x*objekt2.masse
    objekt1.y_geschwi += -beschleuigung_y*objekt2.masse


def geschwindikeits_differenz(objekt1,objekt2):
    differenz = sqrt((objekt1.x_geschwi - objekt2.x_geschwi) ** 2 + (objekt1.y_geschwi - objekt2.y_geschwi) ** 2)
    return differenz


def skaliere_vector(p: tuple, new_length:float): #[float,float]
    x, y = p
    length_p = sqrt(x**2+y**2)
    faktor = new_length/length_p
    return x*faktor, y*faktor





