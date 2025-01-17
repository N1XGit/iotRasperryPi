from base import *
from i2c import Bus
import time
import sys

__all__ = ["JHD1802"]

class JHD1802(Display):

    def __init__(self, address = 0x3E):
        self._bus = Bus()
        self._addr = address
        if self._bus.write_byte(self._addr, 0):
            print("Check if LCD {} inserted, then try again".format(self.name))
            sys.exit(1)
        self.textCommand(0x02)
        time.sleep(0.1)
        self.textCommand(0x08 | 0x04)
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

def main():
    import time

    lcd = JHD1802()
    rows, cols = lcd.size()
    print("LCD model: {}".format(lcd.name))
    print("LCD type : {} x {}".format(cols, rows))

    lcd.backlight(False)
    time.sleep(1)

    lcd.backlight(True)
    lcd.setCursor(0, 0)
    lcd.write("KYS!")
    lcd.setCursor(0, cols - 1)
    lcd.write('kys')
    lcd.setCursor(rows - 1, 0)
    for i in range(cols):
        lcd.write(chr(ord('A') + i))

    time.sleep(3)
    lcd.clear()

    if __name__ == '__main__':
        main()

    
