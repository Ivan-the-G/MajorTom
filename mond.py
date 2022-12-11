from dataclasses import dataclass

import pygame
from pygame.surface import Surface

from framework import Body, fenster_breite

mondi = pygame.image.load("MondComic.png")
mondi = pygame.transform.scale(mondi, (150,150))

@dataclass
class Mond(Body):
    x: float = fenster_breite // 2
    y: float= fenster_breite // 2
    masse: float = 1000
    radius: float = 75
    bild: Surface = mondi
    skraft: bool = False













