from base import *
from i2c import Bus
import time
import sys
import random
import json


__all__ = ["JHD1802"]

class JHD1802(Display):

    def __init__(self, address = 0x3E):
        self._bus = Bus()
        self._addr = address
        if self._bus.write_byte(self._addr, 0):
            print("Check if the LCD {} inserted, then try again"
                    .format(self.name))
            sys.exit(1)
        self.textCommand(0x02)
        time.sleep(0.1)
        self.textCommand(0x08 | 0x04) # display on, no cursor
        self.textCommand(0x28)

    @property
    def name(self):

        return "JHD1802"

    def type(self):

        return TYPE_CHAR

    def size(self):

        return 2, 16

    def clear(self):
 
        self.textCommand(0x01)

    def draw(self, data, bytes):

        return False

    def home(self):

        self.textCommand(0x02)
        time.sleep(0.2)

    def setCursor(self, row, column):

        self.textCommand((0x40 * row) + (column % 0x10) + 0x80)

    def write(self, msg):

        for c in msg:
            self._bus.write_byte_data(self._addr,0x40,ord(c))

    def _cursor_on(self, enable):
        if enable:
            self.textCommand(0x0E)
        else:
            self.textCommand(0x0C)
            
            
    def textCommand(self, cmd):
        self._bus.write_byte_data(self._addr,0x80,cmd)
        
obstaclePos = [15] #lista esteistä

width = 16 #peliruudun koko
height = 2

playerPosX = 0 #pelaajan paikka, posX esteiden huomioon, posY=1 maassa posY = 0 hyppy
playerPosY = 1

score = 0

scoresDict = {} #pisteet

name = ""

#with open("savedScores.json", "r") as file: #pelipisteiden asetus
    #scoresDict = json.load(file)



def getName():
    
    lcd = JHD1802() #pelaajan nimen syöttö

    rows, columns = JHD1802.size()

    while True:
        lcd.setCursor(0, 0)
        lcd.write("Give name: ")

        name = input()

        lcd.setCursor(1, 0)
        lcd.write(name)

        time.sleep(2)

        lcd.clear()
        lcd.setCursor(0,0)
        lcd.write("Save name? y/n")

        lcd.setCursor(1, 0)
        lcd.write(name)

        saveName = str(input)

        saveName = saveName.lower()

        if saveName == "y":
            
            lcd.clear()
            break
        
        return name


def inputJump():
    #sensorin koodi
    return 0

def printGame():
    
    lcd = JHD1802()

    rows, columns = JHD1802.size()

    if width - obstaclePos[len(obstaclePos) - 1] >=6: #onko esteelle tilaa
        
        obstaclePos.append(15) # este näytön reunaan


    lcd.clear()

    for obstacle in obstaclePos: #esteiden piirto
        
        lcd.setCursor(1, obstacle)
        lcd.write("x")

    if playerPosY == 1: #pelaajan piirto

        lcd.setCursor(1, 0) #jos maassa
        lcd.write("I")
    
    elif playerPosY == 0:
        
        lcd.setCursor(0, 0) #jos hypännyt
        lcd.write("I")

    lcd.setCursor(0, columns - len(str(score))) #pisteiden piirto 
    lcd.write(score)


def collision():
    
    for obstacle in obstaclePos: # lista läpi, tarkastaa onko pelaaja esteen kanssa samassa ruudussa
        if obstacle == playerPosX and playerPosY == 1:
            return True # jos osuu
        
    return False


def gameOver():
    
    lcd = JHD1802()

    rows, columns = JHD1802.size()

    lcd.clear()

    lcd.setCursor(0,0)
    lcd.write("Game over!")

    lcd.setCursor(1, 0)
    lcd.write("Score saved.")

    obstaclePos = []

    scoresDict[name] = score #pisteiden asetus sanakirjaan

    #with open("savedScores.json", "w") as file:
        #json.dump(scoresDict, file) #sanakirjan päivitys



def main():

    name = getName() #pelaajan nimen kysyminen
    jumpTimer = 3 #kaunko pelaaja ilmassa hypyn jälkeen

    lcd = JHD1802()
    rows, columns = JHD1802.size()

    while True:

        if inputJump() and jumpTimer == 3 and playerPosY == 0: # jos pelaaja maassa ja hyppyinput saatu
            
            playerPosY = 0 # hyppy

        if playerPosY == 0:
            jumpTimer = jumpTimer - 1 # pelaajan hypyn lasku

        if jumpTimer == 0: # jos pelaaj allut kolme tickiä ilmassa palaa maahan ja hyppylaskuri nollaantuu
            playerPosY = 1
            jumpTimer = 3

        if collision():
            gameOver() # jos pelaaja osuu esteeseen
            break

        for i in obstaclePos:
            obstaclePos.remove(i) #jos este menee ruudulta pois se poistetaan
            if i >= 0: # esteen paikkaa siirretään 1 eteenpäin
                obstaclePos.append(i - 1)
            

        time.sleep(0.2)

        printGame()



        



if __name__ == "__main__":
    main()
