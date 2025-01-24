from base import *
from i2c import Bus
import time
import sys
import random
import json
from grove.gpio import GPIO

usleep = lambda x: time.sleep(x / 1000000.0)

_TIMEOUT1 = 1000
_TIMEOUT2 = 10000

class GroveUltrasonicRanger(object):
    def __init__(self, pin):
        self.dio = GPIO(pin)

    def _get_distance(self):
        self.dio.dir(GPIO.OUT)
        self.dio.write(0)
        usleep(2)
        self.dio.write(1)
        usleep(10)
        self.dio.write(0)

        self.dio.dir(GPIO.IN)

        t0 = time.time()
        count = 0
        while count < _TIMEOUT1:
            if self.dio.read():
                break
            count += 1
        if count >= _TIMEOUT1:
            return None

        t1 = time.time()
        count = 0
        while count < _TIMEOUT2:
            if not self.dio.read():
                break
            count += 1
        if count >= _TIMEOUT2:
            return None

        t2 = time.time()

        dt = int((t1 - t0) * 1000000)
        if dt > 530:
            return None

        distance = ((t2 - t1) * 1000000 / 29 / 2)    # cm

        return distance

    def get_distance(self):
        while True:
            dist = self._get_distance()
            if dist:
                return dist


Grove = GroveUltrasonicRanger

__all__ = ["JHD1802"]

class JHD1802(Display):
    def __init__(self, address = 0x3E):
        self._bus = Bus()
        self._addr = address
        if self._bus.write_byte(self._addr, 0):
            print("Check if the LCD {} inserted, then try again".format(self.name))
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
            self._bus.write_byte_data(self._addr, 0x40, ord(c))

    def _cursor_on(self, enable):
        if enable:
            self.textCommand(0x0E)
        else:
            self.textCommand(0x0C)

    def textCommand(self, cmd):
        self._bus.write_byte_data(self._addr, 0x80, cmd)


# Game variables
obstaclePos = []  # List of obstacles
width = 16  # Game screen width
height = 2  # Game screen height
playerPosX = 0  # Player's horizontal position
playerPosY = 1  # Player's vertical position, 1 for ground, 0 for jumping
score = 0  # Player's score
scoresDict = {}  # Saved scores
name = ""  # Player's name

lcd = JHD1802()
rows, columns = lcd.size()
pin = 5
sonar = GroveUltrasonicRanger(pin)

lcd.clear()
lcd.setCursor(0,0)
lcd.write(" Remove hand")
lcd.setCursor(1,0)
lcd.write(" Taking distance")
time.sleep(5)
baseDistance = sonar.get_distance()
lcd.clear()
lcd.setCursor(0,0)
lcd.write(" Done")
time.sleep(2)
lcd.clear()
    


#with open("savedScores.json", "r") as file:
         #json.load(scoresDict, file)

lcd = JHD1802()
lcd.clear()




def getName():
    lcd = JHD1802()
    while True:
        lcd.clear()
        lcd.setCursor(0, 0)
        lcd.write(" Give name: ")

        name = input()

        lcd.setCursor(1, 0)
        lcd.write(name)

        lcd.clear()
        lcd.setCursor(0, 0)
        lcd.write(" Save name? y/n")

        lcd.setCursor(1, 0)
        lcd.write(name)

        saveName = input().lower()

        if saveName == "y":
            lcd.clear()
            break
        
    return name


def inputJump():

    
    pin = 5
    sonar = GroveUltrasonicRanger(pin)
    from grove.helper import SlotHelper
    
    global baseDistance
    newDistance = sonar.get_distance()
    if newDistance <= baseDistance - 2:
        return False
    else:
        return True




    

def generate_obstacle():
    global obstaclePos
    if len(obstaclePos) == 0 or width - obstaclePos[-1] >= 8:
        obstaclePos.append(width - 1)


def move_obstacles():
    global obstaclePos
    new_obstacle_pos = []
    for obstacle in obstaclePos:
        if obstacle > 0:
            new_obstacle_pos.append(obstacle - 1)  # Move obstacle one step left
    obstaclePos = new_obstacle_pos



def printGame():
    lcd = JHD1802()

    rows, columns = lcd.size()


    lcd.clear()

    
    # Draw obstacles
    for obstacle in obstaclePos:
        
        lcd.setCursor(1,1)
        lcd.setCursor(1, obstacle)
        lcd.write("x")

    # Draw player
    if playerPosY == 1:  # Player on ground
        lcd.setCursor(1, 0)
        lcd.write("I")
    elif playerPosY == 0:  # Player jumping
        lcd.setCursor(0, 0)
        lcd.write("I")

    # Display score
    lcd.setCursor(0, columns - len(str(score)))
    lcd.write(str(score))

    closest = obstaclePos[0] + 1
    lcd.setCursor(0,3)
    lcd.write(str(closest))


def collision():
    global playerPosX, playerPosY
    if playerPosY == 1 and playerPosX==obstaclePos[0]:
        return True  # Collision detected
    return False


def gameOver():
    lcd = JHD1802()
    lcd.clear()

    lcd.setCursor(0, 0)
    lcd.write(" Game over!")

    lcd.setCursor(1, 0)
    lcd.write(" Score saved.")

    time.sleep(2)
    lcd.clear()

    scoresDict[name] = score


    # Uncomment to save scores to file
    #with open("savedScores.json", "w") as file:
         #json.dump(scoresDict, file)

    return 0


def main():

    pin = 5
    sonar = GroveUltrasonicRanger(pin)
    from grove.helper import SlotHelper
    
    
    newGame = "y"
    while newGame == "y":
        global playerPosY, playerPosX, obstaclePos, score, name
        obstaclePos = []
        name = getName()  # Ask for player's name
        jumpTimer = 3  # Timer for jump (how long the player stays in the air)
    
        while True:
            generate_obstacle()
            printGame()
            
            if inputJump() and jumpTimer == 3 and playerPosY == 1:  # Jumping condition
                playerPosY = 0  # Player jumps
    
            if playerPosY == 0:
                jumpTimer -= 1  # Countdown for jump
    
            if jumpTimer == 0:
                playerPosY = 1  # Player lands
                jumpTimer = 3  # Reset jump timer
    
            if collision():  # Check for collision with obstacles
                gameOver()# End game if collision happens
                time.sleep(2)
                break
    
            move_obstacles()  # Move obstacles to the left
    
            time.sleep(1)  # Game loop delay
              # Print the game state
        lcd.clear()
        lcd.setCursor(0,0)
        lcd.write(" New game? (y/n)")
        newGame = input()
        lcd.clear()


if __name__ == "__main__":
    main()
