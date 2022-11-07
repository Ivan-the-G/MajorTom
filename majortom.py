from copy import deepcopy
from typing import Optional

import pygame
import random
from dataclasses import dataclass
from math import  sin,cos,pi,sqrt


pygame.init()

ORANGE = (250,140,0)
GELB   = (255,255,0)
ROT    = (255,0,0)
GRUEN  = (0,255,0)
SCHWARZ= (0,0,0)
WEISS  = (255,255,255)
GRAU   = (150,150,150)

x1 = random.randint(10,640)
y1 = random.randint(10,480)

x = 0
y = 0

explosion_time = None

"""


"""


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
    bild: list
    stabilität: int = 1000
    winkel: float = 0
    beschleunigugn:float = 0
    masse:float = 0
    radius:float =0
    klebt_an:Optional["Body"] = None
    x_geschwi: float = 0
    y_geschwi: float = 0

    # ---------------------------------------------------------------------------BODY.turn
    def turn(self,change):
        self.winkel = self.winkel - change
        if self.winkel > 360:
            self.winkel -= 360
        if self.winkel < 0:
            self.winkel += 350


    # ---------------------------------------------------------------------------BODY.draw_self
    def draw_self(self,bild):

        image = pygame.transform.rotate(bild, self.winkel - 45)
        screen.blit(image, (int(self.x - image.get_width() / 2), self.y - int(image.get_height() / 2)))

    # ---------------------------------------------------------------------------BODY.push
    def push(self,puch):
        self.x_geschwi += cos(self.winkel * pi / 180) * self.beschleunigugn
        self.y_geschwi += -sin(self.winkel * pi / 180) * self.beschleunigugn

    # ----------------------------------------------------------------------------BODY.chek_kollison
    def chek_kollison(self, objekt2):
        geschwindikeit = None

        abstand = sqrt((self.x - objekt2.x) ** 2 + (self.y - objekt2.y) ** 2)

        if abstand < self.radius + objekt2.radius:
            geschwindikeit = geschwindikeits_differenz(self, objekt2)

        return geschwindikeit

    # ----------------------------------------------------------------------------BODY.move
    def move(self,skraft=True):
        #print("move")
        if skraft:
            schwerkraft(self, mond)

        self.x += self.x_geschwi
        self.y += self.y_geschwi




#=======================================================================Init_Rakete
raketeo = pygame.image.load("Raketeo.png")
raketeo = pygame.transform.scale(raketeo, (60,60))

raketef = pygame.image.load("RaketeF.png")
raketef = pygame.transform.scale(raketef, (60,60))

explosioni = pygame.image.load("explosion.png")
explosioni = pygame.transform.scale(explosioni, (50,50))

rakete = Body(
    winkel = 0,
    beschleunigugn=0.15,
    bild = [raketeo,raketef,explosioni],
    stabilität = 3,
    masse = 10,
    radius= 30,
    x_geschwi=2,
    y_geschwi=0,
    x= fenster_breite//2,
    y= fenster_breite//4
)

#=======================================================================Init_mond
mondi = pygame.image.load("MondComic.png")
mondi = pygame.transform.scale(mondi, (150,150))

mond = Body(
    winkel = 00,
    beschleunigugn=0,
    bild = [mondi],
    masse = 1000,
    radius= 70,
    x_geschwi=0,
    y_geschwi=0,
    x= fenster_breite//2,
    y= fenster_breite//2,
)


#---------------------------------------------------------------------------draw
def draw():
    global explosion_time
    screen.blit(hintergrund,(0,0))
    mond.draw_self(mond.bild[0])
    #screen.blit(mondi,(mond.x -75,mond.y -75))

    #pygame.draw.polygon(screen, GELB, ((rakete.x,rakete.y), (50 + rakete.x,rakete.y), (25 + rakete.x, 50 + rakete.y)))

    if pygame.key.get_pressed()[pygame.K_UP]:
        image = rakete.bild[1]
    else:
        image = rakete.bild[0]

    if explosion_time is not None:
        delta_t = pygame.time.get_ticks() - explosion_time
        if delta_t > 1000:
            image = pygame.image.load("leer.png")

        else:
            image = rakete.bild[2]

    rakete.draw_self(image)



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
def kollisionen():
    global explosion_time
    geschwie_differenz = rakete.chek_kollison(mond)

    if geschwie_differenz != None:
        #print(geschwie_differenz)
        if geschwie_differenz > rakete.stabilität:
            #print("krasch")
            rakete.klebt_an = mond
            explosion_time = pygame.time.get_ticks()

        else:
            rakete.klebt_an= mond

# ----------------------------------------------------------------------------move
def move():
    klebt = False
    # self_kopy = deepcopy(self)

    if rakete.klebt_an != None:
        if pygame.key.get_pressed()[pygame.K_UP]:
            klebt = True
            klebt_an = rakete.klebt_an
            rakete.klebt_an = None
        else:
            #print(rakete.x_geschwi)
            rakete.x_geschwi = rakete.klebt_an.x_geschwi
            rakete.y_geschwi = rakete.klebt_an.y_geschwi

            rakete.move()
            #print(rakete.x_geschwi)
    else:
        rakete.move()

    if klebt:
        x = rakete.x
        y = rakete.y

        rakete.push(-10)
        rakete.move()

        if rakete.chek_kollison(mond) == None:
            #print("a")
            rakete.x = x
            rakete.y = y
            rakete.klebt_an = klebt_an
            #print(geschwindikeits_differenz(rakete,mond))

            #rakete.x_geschwi = rakete.klebt_an.x_geschwi
            #rakete.y_geschwi = rakete.klebt_an.y_geschwi



#==============================================================================================Main_wihle
while spielaktiv:
    #Überprüfen, ob Nutzer eine Aktion durchgeführt hat
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spielaktiv = False

        elif event.type == pygame.KEYDOWN:

            # Taste für Spieler 2

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        rakete.turn(5)
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        rakete.turn(-5)
    if pygame.key.get_pressed()[pygame.K_UP]:
        rakete.push(-10)


    move()


    # Spiellogik hier integrieren

    #Spielfeld löschen
    screen.fill(SCHWARZ)

    kollisionen()

    draw()
    # Spielfeld/figur(en) zeichnen (davor Spielfeld löschen)



    # Fenster aktualisieren
    pygame.display.flip()
    # Refresh-Zeiten festlegen
    clock.tick(60) # 60fps

pygame.quit()