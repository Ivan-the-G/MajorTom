from dataclasses import dataclass

import pygame

from framework import Body

WEISS  = (255,255,255)

@dataclass
class Asteroid(Body):
    masse: float = 0.
    radius: float = 10.

    def draw(self,screen):
        pygame.draw.circle(screen, WEISS, (self.x, self.y), self.radius)















