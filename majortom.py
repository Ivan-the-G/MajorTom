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
    winkel: float
    beschleunigugn:float
    masse:float
    x_geschwi: float
    y_geschwi: float
    x:float
    y:float

#=======================================================================Init_Rakete
rakete = Body(
    winkel = 90,
    beschleunigugn=0.1,
    masse = 10,
    x_geschwi=0,
    y_geschwi=0,
    x= 100,
    y= 100

)

#=======================================================================mond
mondi = pygame.image.load("MondComic.png")
mondi = pygame.transform.scale(mondi, (150,150))

mond = Body(
    winkel = 00,
    beschleunigugn=0,
    masse = 1000,
    x_geschwi=0,
    y_geschwi=0,
    x= fenster_breite//2,
    y= fenster_breite//2,
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
    screen.blit(hintergrund,(0,0))
    screen.blit(mondi,(mond.x -75,mond.y -75))

    #pygame.draw.polygon(screen, GELB, ((rakete.x,rakete.y), (50 + rakete.x,rakete.y), (25 + rakete.x, 50 + rakete.y)))

    if pygame.key.get_pressed()[pygame.K_UP]:
        image = raketef
    else:
        image = raketeo


    image = pygame.transform.rotate(image, rakete.winkel-45)
    screen.blit(image, (rakete.x - int(image.get_width() / 2), rakete.y - int(image.get_height() / 2)))




    #pygame.draw.circle(screen, WEISS, (x1, x1), 10)

#----------------------------------------------------------------------------rakete_move
def rakete_move():
    schwerkraft(rakete,mond)

    rakete.x += rakete.x_geschwi
    rakete.y += rakete.y_geschwi
    #print("a",end="")
    #print(str(rakete.x_geschwi) + "   " + str(rakete.y_geschwi))

#----------------------------------------------------------------------------schwerkraft
def schwerkraft(objekt1,objekt2):
    abstand = sqrt((objekt1.x-objekt2.x)**2+(objekt1.y-objekt2.y)**2)
    beschleuigung_x = (objekt1.x-objekt2.x)/abstand**3
    beschleuigung_y = (objekt1.y-objekt2.y)/abstand**3

    objekt1.x_geschwi += -beschleuigung_x*objekt2.masse
    objekt1.y_geschwi += -beschleuigung_y*objekt2.masse



    #return beschleuigung_x,beschleuigung_y



#=============================================================================Init_algemein


hintergrund = pygame.image.load("Universum3.jpg")
hintergrund = pygame.transform.scale(hintergrund, (1000,1000))

masse_mond = 1000000

#Schleife Hauptprogramm
spielaktiv = True
clock = pygame.time.Clock()


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

    draw()
    # Spielfeld/figur(en) zeichnen (davor Spielfeld löschen)

    # Fenster aktualisieren
    pygame.display.flip()
    # Refresh-Zeiten festlegen
    clock.tick(60) # 60fps

pygame.quit()