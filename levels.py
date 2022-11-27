from dataclasses import dataclass

import pygame
from pygame.surface import Surface

from asteroid import Asteroid
from framework import fenster_breite
from mond import Mond
from rakete import Rakete

hintergrund = pygame.image.load("Universum3.jpg")
hintergrund = pygame.transform.scale(hintergrund, (1000,1000))


@dataclass
class Level:
    hintergrund: Surface = hintergrund
    def mission_erfüllt(self) -> bool:
        raise NotImplemented


@dataclass
class Level1(Level):
    mond: Mond = Mond()
    rakete: Rakete = Rakete()
    def mission_erfüllt(self) -> bool:
        return self.rakete.klebt_an == self.mond

    def __post_init__(self):
        self.bodies = [self.mond, self.rakete]


@dataclass
class Level2(Level):
    mond: Mond = Mond()
    rakete: Rakete = Rakete()
    asteroid: Asteroid = Asteroid(
        x_geschwi=0,
        y_geschwi=2,
        x= fenster_breite//4,
        y= fenster_breite//2
    )

    def mission_erfüllt(self) -> bool:
        return self.rakete.klebt_an == self.mond

    def __post_init__(self):
        self.bodies = [self.mond, self.rakete, self.asteroid]

levels = [Level1(), Level2()]

