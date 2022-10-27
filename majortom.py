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

#=========================================================================Init_objekt
@dataclass
class Body:
    x: float
    y: float
    winkel: float = 0
    beschleunigugn:float = 0
    masse:float = 0
    radius:float =0
    klebt_an:Optional["Body"] = None
    x_geschwi: float = 0
    y_geschwi: float = 0


#=======================================================================Init_Rakete
rakete = Body(
    winkel = 0,
    beschleunigugn=0.15,
    masse = 10,
    radius= 30,
    x_geschwi=2,
    y_geschwi=0,
    x= fenster_breite//2,
    y= fenster_breite//4
)

#=======================================================================mond
mondi = pygame.image.load("MondComic.png")
mondi = pygame.transform.scale(mondi, (150,150))

mond = Body(
    winkel = 00,
    beschleunigugn=0,
    masse = 1000,
    radius= 70,
    x_geschwi=0,
    y_geschwi=0,
    x= fenster_breite//2,
    y= fenster_breite//2,
)

#=======================================================================explosion
explosioni = pygame.image.load("explosion.png")
explosioni = pygame.transform.scale(explosioni, (50,50))
explosion = Body(
    winkel = 00,
    beschleunigugn=0,
    masse = 0,
    x_geschwi=0,
    y_geschwi=0,
    x= fenster_breite//2,
    y= fenster_breite//2
)

#---------------------------------------------------------------------------rakete_push
raketeo = pygame.image.load("Raketeo.png")
raketeo = pygame.transform.scale(raketeo, (60,60))

raketef = pygame.image.load("RaketeF.png")
raketef = pygame.transform.scale(raketef, (60,60))

def rakete_push(puch):
    rakete.x_geschwi += cos(rakete.winkel * pi / 180)*rakete.beschleunigugn
    rakete.y_geschwi += -sin(rakete.winkel * pi / 180)*rakete.beschleunigugn
    #print(rakete.x_geschwi,rakete.y_geschwi)



#x*Pi/180
#---------------------------------------------------------------------------rakete_turn
def rakete_turn(change):
    rakete.winkel = rakete.winkel -change
    if rakete.winkel > 360:
        rakete.winkel -= 360
    if rakete.winkel < 0:
        rakete.winkel += 350
    #print(rakete.winkel)



#---------------------------------------------------------------------------draw
def draw():
    global explosion_time
    screen.blit(hintergrund,(0,0))
    screen.blit(mondi,(mond.x -75,mond.y -75))

    #pygame.draw.polygon(screen, GELB, ((rakete.x,rakete.y), (50 + rakete.x,rakete.y), (25 + rakete.x, 50 + rakete.y)))

    if pygame.key.get_pressed()[pygame.K_UP]:
        image = raketef
    else:
        image = raketeo

    if pygame.key.get_pressed()[pygame.K_DOWN]:
        explosion_time = pygame.time.get_ticks()

    if explosion_time is not None:
        delta_t = pygame.time.get_ticks() - explosion_time
        if delta_t > 1000:
            image = pygame.image.load("leer.png")
        else:
            image = explosioni

    image = pygame.transform.rotate(image, rakete.winkel-45)
    screen.blit(image, (int(rakete.x - image.get_width() / 2), rakete.y - int(image.get_height() / 2)))


#----------------------------------------------------------------------------rakete_move
def rakete_move():
    global rakete
    schwerkraft(rakete,mond)
    rakete_kopy = deepcopy(rakete)


    if pygame.key.get_pressed()[pygame.K_UP]:
        rakete.klebt_an = None

    if rakete.klebt_an == None:
        rakete.x += rakete.x_geschwi
        rakete.y += rakete.y_geschwi
    else:
        rakete.x_geschwi = rakete.klebt_an.x_geschwi
        rakete.y_geschwi = rakete.klebt_an.y_geschwi
"""
    if rakete.klebt_an:
        if pygame.key.get_pressed()[pygame.K_UP]:
            rakete_kopy = deepcopy(rakete)
            rakete_kopy.klebt_an = None
            rakete_kopy.x += rakete_kopy.x_geschwi+cos(rakete_kopy.winkel * pi / 180)*rakete_kopy.beschleunigugn
            rakete_kopy.y += rakete_kopy.y_geschwi+-sin(rakete_kopy.winkel * pi / 180)*rakete_kopy.beschleunigugn
            if berührung[0](rakete_kopy,mond):
                pass
            else:
                rakete= rakete_kopy
    else:
        if rakete.klebt_an == None:
            rakete.x += rakete.x_geschwi
            rakete.y += rakete.y_geschwi
        else:
            rakete.x_geschwi = rakete.klebt_an.x_geschwi
            rakete.y_geschwi = rakete.klebt_an.y_geschwi
"""
    #print("a",end="")
    #print(str(rakete.x_geschwi) + "   " + str(rakete.y_geschwi))

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

#----------------------------------------------------------------------------chek_kollison
def chek_kollison(objekt1,objekt2):
    kontakt,krasch = berührung(objekt1,objekt2)
    if kontakt:
        if krasch:
            objekt1.x_geschwi = 0
            objekt1.y_geschwi = 0
            objekt1.x = 100
            objekt1.y = 100
        else:
            objekt1.klebt_an= objekt2









#----------------------------------------------------------------------------kolison
def berührung(objekt1,objekt2):
    kolison = False
    krash = False
    abstand = sqrt((objekt1.x - objekt2.x) ** 2 + (objekt1.y - objekt2.y) ** 2)
    if abstand < objekt1.radius+objekt2.radius:
        kolison = True
        if geschwindikeits_differenz(objekt1,objekt2) < 3:
            krash = False
        else:
            krash = True


    return kolison,krash




#=============================================================================Init_algemein


hintergrund = pygame.image.load("Universum3.jpg")
hintergrund = pygame.transform.scale(hintergrund, (1000,1000))


#Schleife Hauptprogramm
spielaktiv = True
clock = pygame.time.Clock()

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
        rakete_turn(5)
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        rakete_turn(-5)
    if pygame.key.get_pressed()[pygame.K_UP]:
        rakete_push(-10)


    rakete_move()


    # Spiellogik hier integrieren

    #Spielfeld löschen
    screen.fill(SCHWARZ)

    chek_kollison(rakete,mond)

    draw()
    # Spielfeld/figur(en) zeichnen (davor Spielfeld löschen)



    # Fenster aktualisieren
    pygame.display.flip()
    # Refresh-Zeiten festlegen
    clock.tick(60) # 60fps

pygame.quit()