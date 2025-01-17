from base import *
from i2c import Bus
import time
import sys

# sphinx autoapi required
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
        

Width = 16
Height = 2
PlayerPositionY = 0
PlayerPositionX = 1
ObstaclePos = Width - 1
score = 0
counter = 4

def print_game(PlayerPosX:int, PlayerPosY:int, ObstaclePos:int, score:int): # vaihetaan lcd näytön printiksi 
    lcd = JHD1802
    rows, cols = lcd.size(lcd)
    
    for row in range(Height):
        if row == 0:
            lcd.setCursor(0, 0)
            if PlayerPositionY == 1: #jos pelaaja hyppää
                lcd.write('O' + ' ' * (Width - len(str(score)) - 2), str(score))
            else:
                lcd.write(' ' * (Width - len(str(score)) -1),str(score))
        else:
            lcd.setCursor(Height - 1, 0)
            if PlayerPositionY == 1: #jos pelaaja hyppää
                lcd.write(' '*(ObstaclePos - 1) + 'x' + ' ' * (Width - ObstaclePos))
            else:
                lcd.write('O' + ' ' * (ObstaclePos - 2) + 'x' + ' ' * (Width - ObstaclePos)) 

def main():
    global PlayerPositionX, ObstaclePos, PlayerPositionY, score, counter
    while True:
    
        lcd = JHD1802
        Height, Width = lcd.size()

        if counter == 4: #tähän vaihdetaan se että etäisyysmittarin lukema vaihtuu pienemmäksi
            PlayerPositionY = 1
            PlayerPositionX = -1
            counter = 4

        if PlayerPositionY == 1:
            counter = counter - 1

        if counter == 0:
            PlayerPositionY = 0
            PlayerPositionX = 1
            counter = 4
            

        ObstaclePos -= 1
        if ObstaclePos < 0:
            ObstaclePos = Width - 1
            score += 1

        if PlayerPositionX == ObstaclePos and PlayerPositionY == 0:
            lcd.clear(lcd)
            lcd.setCursor(0,0)
            lcd.write('Game over!')
            lcd.setCursor(0, Height - 1)
            lcd.write(score)
            break

        print_game(PlayerPositionX, PlayerPositionY, ObstaclePos, score)
        time.sleep(0.2)


if __name__ == "__main__":
    main()
