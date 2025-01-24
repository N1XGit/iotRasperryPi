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

with open("savedScores.json", "r") as file:
         json.load(scoresDict, file)

lcd = JHD1802()
lcd.clear()


def getName():
    lcd = JHD1802()
    while True:
        lcd.clear()
        lcd.setCursor(0, 0)
        lcd.write("Give name: ")

        name = input()

        lcd.setCursor(1, 0)
        lcd.write(name)

        time.sleep(2)

        lcd.clear()
        lcd.setCursor(0, 1)
        lcd.write("Save name? y/n")

        lcd.setCursor(1, 0)
        lcd.write(name)

        saveName = input().lower()

        if saveName == "y":
            lcd.clear()
            break
        
    return name


def inputJump():
    # Sensor code for jump
    return 0  # Placeholder


def generate_obstacle():
    global obstaclePos
    if len(obstaclePos) == 0 or width - obstaclePos[-1] >= 6:
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

    generate_obstacle()  # Generate new obstacles

    lcd.clear()

    # Draw obstacles
    for obstacle in obstaclePos:
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


def collision():
    global playerPosX, playerPosY
    if playerPosY == 1 and playerPosX in obstaclePos:
        return True  # Collision detected
    return False


def gameOver():
    lcd = JHD1802()
    lcd.clear()

    lcd.setCursor(0, 0)
    lcd.write("Game over!")

    lcd.setCursor(1, 0)
    lcd.write("Score saved.")

    scoresDict[name] = score

    # Uncomment to save scores to file
    with open("savedScores.json", "w") as file:
         json.dump(scoresDict, file)


def main():
    global playerPosY, playerPosX, obstaclePos, score, name

    name = getName()  # Ask for player's name
    jumpTimer = 3  # Timer for jump (how long the player stays in the air)

    while True:
        if inputJump() and jumpTimer == 3 and playerPosY == 1:  # Jumping condition
            playerPosY = 0  # Player jumps

        if playerPosY == 0:
            jumpTimer -= 1  # Countdown for jump

        if jumpTimer == 0:
            playerPosY = 1  # Player lands
            jumpTimer = 3  # Reset jump timer

        if collision():  # Check for collision with obstacles
            gameOver()  # End game if collision happens
            break

        move_obstacles()  # Move obstacles to the left

        time.sleep(0.2)  # Game loop delay
        printGame()  # Print the game state


if __name__ == "__main__":
    main()
