import random
import time
import os
import keyboard

clear = lambda: os.system('cls')

# vakiot

#spacen painaminen pitää vaihtaa etäisyysmittarin luentaan ja print komennot vaihtaa lcd näyttöön

Width = 16
Height = 2
PlayerPositionY = 0
PlayerPositionX = 1
ObstaclePos = Width - 1
score = 0
counter = 4

def print_game(PlayerPosX:int, PlayerPosY:int, ObstaclePos:int, score:int): # vaihetaan lcd näytön printiksi 
    for row in range(Height):
        if row == 0:
            if PlayerPositionY == 1: #jos pelaaja hyppää
                print('O' + ' ' * (Width - len(str(score)) - 2), str(score))
            else:
                print(' ' * (Width - len(str(score)) -1),str(score))
        else:
            if PlayerPositionY == 1: #jos pelaaja hyppää
                print(' '*ObstaclePos + 'x' + ' ' * (Width - ObstaclePos - 1))
            else:
                print('O' + ' ' * (ObstaclePos - 1) + 'x' + ' ' * (Width - ObstaclePos - 1)) 

def main():
    global PlayerPositionX, ObstaclePos, PlayerPositionY, score, counter
    while True:
    
        
        if keyboard.is_pressed('space') and counter == 4: #tähän vaihdetaan se että etäisyysmittarin lukema vaihtuu pienemmäksi
            PlayerPositionY = 1 #hyppy
            PlayerPositionX = -1
            counter = 4

        if PlayerPositionY == 1:
            counter = counter - 1 #hyppyajastin

        if counter == 0: #hyppy loppuu
            PlayerPositionY = 0
            PlayerPositionX = 1
            counter = 4
            
        clear()

        ObstaclePos -= 1
        if ObstaclePos < 0: # pisteet nousee
            ObstaclePos = Width - 1
            score += 1

        if PlayerPositionX == ObstaclePos and PlayerPositionY == 0: #collision
            print('Game over!')
            break

        print_game(PlayerPositionX, PlayerPositionY, ObstaclePos, score)
        time.sleep(0.5)


if __name__ == "__main__":
    main()

    
