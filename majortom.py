import math
from typing import Optional, List

import pygame
from dataclasses import dataclass
from math import  sin,cos,pi,sqrt

from pygame.surface import Surface

pygame.init()

WEISS  = (255,255,255)

#Fenster öffnen
#======================================================================Init_Fenster
fenster_breite = 1000
fenster_höhe = 1000

pygame.display.set_mode((fenster_breite,fenster_höhe))
screen = pygame.display.set_mode((fenster_breite, fenster_höhe))

pygame.display.set_caption("MajorTom")

hintergrund = pygame.image.load("Universum3.jpg")
hintergrund = pygame.transform.scale(hintergrund, (1000,1000))

spielaktiv = True
clock = pygame.time.Clock()

#=========================================================================Init_objekt
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

    # ---------------------------------------------------------------------------BODY.turn
    def turn(self,change):
        self.winkel = self.winkel - change
        if self.winkel > 360:
            self.winkel -= 360
        if self.winkel < 0:
            self.winkel += 350


    # ---------------------------------------------------------------------------BODY.draw_self
    def draw(self):
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

    # ----------------------------------------------------------------------------BODY.move
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

@dataclass
class Level:
    hintergrund: Surface
    bodies: list#[Body]

#=======================================================================Init_Rakete
raketeo = pygame.image.load("Raketeo.png")
raketeo = pygame.transform.scale(raketeo, (60,60))

raketef = pygame.image.load("RaketeF.png")
raketef = pygame.transform.scale(raketef, (60,60))

explosioni = pygame.image.load("explosion.png")
explosioni = pygame.transform.scale(explosioni, (50,50))

@dataclass
class Rakete(Body):
    bildausrichtung: float = 45.
    beschleunigung = 0.15

    def move(self, bodies: list):#[Body]):
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.turn(5)
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.turn(-5)
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.klebt_an = None
            self.push()
        super().move(bodies)

    def push(self):
        self.x_geschwi += cos(self.winkel * pi / 180) * self.beschleunigung
        self.y_geschwi += -sin(self.winkel * pi / 180) * self.beschleunigung

    def draw(self):
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.bild = raketef
        else:
            self.bild = raketeo
        super().draw()

    def kollision(self, other: "Body"):
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


#=======================================================================Init_mond
mondi = pygame.image.load("MondComic.png")
mondi = pygame.transform.scale(mondi, (150,150))

@dataclass
class Mond(Body):
    bild: Surface = mondi
    skraft: bool = False

@dataclass
class Asteroid(Body):
    masse: float = 0.
    radius: float = 10.

    def draw(self):
        pygame.draw.circle(screen, WEISS, (self.x, self.y), self.radius)



mond = Mond(
    masse = 1000,
    radius= 70,
    x= fenster_breite//2,
    y= fenster_breite//2,
)

rakete = Rakete(
    winkel = 0,
    stabilität = 3,
    masse = 10,
    radius= 30,
    x_geschwi=2,
    y_geschwi=0,
    x= fenster_breite//2,
    y= fenster_breite//4
)

level1 = Level(
    hintergrund = hintergrund,
    bodies=[mond, rakete]
)

asteroid = Asteroid(
    x_geschwi=0,
    y_geschwi=2,
    x= fenster_breite//4,
    y= fenster_breite//2
)

level2 = Level(
    hintergrund = hintergrund,
    bodies=[mond, rakete, asteroid]
)


#---------------------------------------------------------------------------draw
def draw(level: Level):
    screen.blit(level.hintergrund,(0,0))
    for body in level.bodies:
        body.draw()



#----------------------------------------------------------------------------schwerkraft
def schwerkraft(objekt1,objekt2):
    abstand = sqrt((objekt1.x-objekt2.x)**2+(objekt1.y-objekt2.y)**2)
    beschleuigung_x = (objekt1.x-objekt2.x)/abstand**3
    beschleuigung_y = (objekt1.y-objekt2.y)/abstand**3

    objekt1.x_geschwi += -beschleuigung_x*objekt2.masse
    objekt1.y_geschwi += -beschleuigung_y*objekt2.masse


#----------------------------------------------------------------------------abstandsdifferenz
def geschwindikeits_differenz(objekt1,objekt2):
    differenz = sqrt((objekt1.x_geschwi - objekt2.x_geschwi) ** 2 + (objekt1.y_geschwi - objekt2.y_geschwi) ** 2)
    return differenz


#----------------------------------------------------------------------------kollisionen
def skaliere_vector(p: tuple, new_length:float): #[float,float]
    x, y = p
    length_p = math.sqrt(x**2+y**2)
    faktor = new_length/length_p
    return x*faktor, y*faktor


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

level = level1

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
    draw(level)

    # Fenster aktualisieren
    pygame.display.flip()

    # Refresh-Zeiten festlegen
    clock.tick(60) # 60fps

pygame.quit()
