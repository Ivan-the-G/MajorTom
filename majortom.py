import pygame
import random
from dataclasses import dataclass
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

#Fenster öffnen

fenster_breite = 640
fenster_höhe = 480

pygame.display.set_mode((fenster_breite,fenster_höhe))
screen = pygame.display.set_mode((fenster_breite, fenster_höhe))

pygame.display.set_caption("MajorTom")

#Schleife Hauptprogramm
spielaktiv = True
clock = pygame.time.Clock()

while spielaktiv:
    #Überprüfen, ob Nutzer eine Aktion durchgeführt hat
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spielaktiv = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Spieler hast Maus angeklickt")

            # Taste für Spieler 2

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        x = x + 10
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        x = x - 10
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        y = y + 10
    if pygame.key.get_pressed()[pygame.K_UP]:
        y = y - 10
    # Spiellogik hier integrieren

    #Spielfeld löschen
    screen.fill(SCHWARZ)
    pygame.draw.circle(screen,WEISS, (320, 240), 50)
    pygame.draw.polygon(screen,GELB,((100+x,100+y),(150+x,150+y),(150+x,100+y)))
    pygame.draw.circle(screen, WEISS, (x1, x1), 10)
    # Spielfeld/figur(en) zeichnen (davor Spielfeld löschen)

    # Fenster aktualisieren
    pygame.display.flip()
    # Refresh-Zeiten festlegen
    clock.tick(60) # 60fps

pygame.quit()