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
        
obstaclePos = [15]

width = 16
height = 2

playerPosX = 0
playerPosY = 1

score = 0

scoresDict = {}

name = ""

with open("savedScores.json", "r") as file:
    scoresDict = json.load(file)



def getName():
    
    lcd = JHD1802()

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

        saveName = saveName.lower

        if saveName == "y":
            
            lcd.clear()
            break
        
        return name


def input():
    #sensorin koodi
    return 0

def printGame():
    
    lcd = JHD1802()

    rows, columns = JHD1802.size()

    if width - obstaclePos[len(obstaclePos) - 1] >=6:
        
        newObstacle = random.randint(6,10)
        
        if obstaclePos[len(obstaclePos) - 1] + newObstacle <= 15:
            
            obstaclePos.append(15)


    lcd.clear()

    for obstacle in obstaclePos: #obstacles
        
        lcd.setCursor(1, obstacle)
        lcd.write("x")

    if playerPosY == 1: #player

        lcd.setCursor(1, 0)
        lcd.write("I")
    
    elif playerPosY == 0:
        
        lcd.setCursor(0, 0)
        lcd.write("I")

    lcd.setCursor(0, columns - len(str(score)))
    lcd.write(score)


def collision():
    
    for obstacle in obstaclePos:
        if obstacle == playerPosX and playerPosY == 1:
            return True
        
    return False


def gameOver():
    
    lcd = JHD1802()

    rows, columns = JHD1802.size()

    lcd.clear()

    lcd.setCursor(0,0)
    lcd.write("Game over!")

    lcd.setCursor(1, 0)
    lcd.write("Score saved.")

    scoresDict[name] = score

    with open("savedScores.json", "w") as file:
        json.dump(scoresDict, file)



def main():

    name = getName()
    jumpTimer = 3

    while True:

        if input() and jumpTimer == 3:
            
            playerPosY = 0

        if playerPosY == 0:
            jumpTimer = jumpTimer - 1

        if jumpTimer == 0:
            playerPosY = 1
            jumpTimer = 3

        if collision():
            gameOver()
            break

        for i in obstaclePos:
            obstaclePos.remove(i)
            if obstaclePos > 0:
                obstaclePos.append(i - 1)
            

        time.sleep(0.2)

        printGame()



        



if __name__ == "__main__":
    main()