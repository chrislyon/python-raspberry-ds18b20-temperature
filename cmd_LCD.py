#!/usr/bin/python

## -------------------------------
## Origine : Adafruit LCRTEst.py
## -------------------------------

from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import get_temp
import datetime
import time

# Initialize the LCD plate.  Should auto-detect correct I2C bus.  If not,
# pass '0' for early 256 MB Model B boards or '1' for all later versions
lcd = Adafruit_CharLCDPlate()

# Clear display and show greeting, pause 1 sec
lcd.clear()
lcd.message("SRA INFORMATIQUE")
sleep(1)
lcd.clear()
lcd.message("TEMPERATURE\nSALLE SERVEUR")
sleep(1)

# Cycle through backlight colors
col = (lcd.RED , lcd.YELLOW, lcd.GREEN, lcd.TEAL,
       lcd.BLUE, lcd.VIOLET, lcd.ON   , lcd.OFF)
for c in col:
    lcd.backlight(c)
    sleep(.5)

# Poll buttons, display message & set backlight accordingly
btn = ((lcd.LEFT  , 'BOUTON GAUCHE'              , lcd.RED),
       (lcd.UP    , 'BOUTON HAUT'     , lcd.BLUE),
       (lcd.DOWN  , 'BOUTON BAS'    , lcd.GREEN),
       (lcd.RIGHT , 'BOUTON DROIT', lcd.VIOLET),
       (lcd.SELECT, 'BOUTON SELECT', lcd.ON))

## ----------------------
## Affichage d'un message
## ----------------------
def affiche(msg):
    lcd.clear()
    lcd.message(msg)

## ------------------------------------------
## Affichage temperature
## change la couleur en fonction de celle ci
## ------------------------------------------
def affiche_temp(t):
    lcd.clear()
    if t < 15:
        color = lcd.BLUE
    elif t >= 15 and t < 20:
        color = lcd.GREEN
    elif t >= 20 and t < 25:
        color = lcd.VIOLET
    else:
        color = lcd.RED
    lcd.backlight(color)
    lcd.message("Temperature : \n%s degrees" % t)

## ---------------------------
## Attente de 5 secondes 
## que l'on confirme
## ---------------------------
def confirm( msg, temps ):
    lcd.clear()
    lcd.message(msg)
    exit = False
    debut = time.time()
    confirm = False
    while not exit:
        sleep(0.2)
        ## Appui sur le bouton
        b = lcd.buttons()
        if b == 1:
            exit = True
            confirm = True
        ## Temps depasse
        t = time.time()
        if int(t-debut) > temps:
            exit = True
    return confirm


## --------------------
## Boucle principale
## --------------------
while True:
    d = datetime.datetime.now()
    ts = d.strftime("%d-%m-%Y \n%X")
    affiche(ts)

    t = get_temp.read_all()
    temp = t[0]
    ## Affichage de la temperature
    affiche_temp(temp)
    sleep(1)
    for b in btn:
        if lcd.buttonPressed(b[0]):
            lcd.clear()
            affiche("%s / %s " % (b,b[1]))
            if b[1] == 'BOUTON HAUT':
                r = confirm("AUTO-DESTRUCT", 5)
                if r:
                    affiche("BOOM")
                else:
                    affiche("ARRET DE LA PROCEDURE")
            break
    ## Attente
    sleep(1)
    
#prev = -1
#while True:
#    for b in btn:
#        if lcd.buttonPressed(b[0]):
#            if b is not prev:
#                lcd.clear()
#                lcd.message(b[1])
#                lcd.backlight(b[2])
#                prev = b
#            break
