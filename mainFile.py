import pygame

from Characters import *
from EventHanlder import *

pygame.init()

mainDisplay = pygame.display.set_mode((800, 600))   #Display for game
bg_image = pygame.image.load("ex_background.jpg")
bg_image = pygame.transform.scale(bg_image, (800, 600))
BackgroundColor = (0,0,200)

Clock = pygame.time.Clock()
FPS = 60

CHARACTERWIDTH = 120         #for character class function. The current size for one sprite is 120 x 80 pixels
CHARACTERHEIGHT = 80
CharacterX = 100            #where you want to place the character at
CharacterY = 500
characterOffset = [0, 0]




# mainDisplay.fill(BackgroundColor)  


def main(mainDisplay):


    theMain = mainCharacter(CharacterX, CharacterY, CHARACTERWIDTH, CHARACTERHEIGHT ) #creating the main character
    enemy1 = EnemyKnight(CharacterX + 420 , CharacterY - 135, CHARACTERWIDTH, CHARACTERHEIGHT, theMain)    #enemy 1
    handleEvents = Event(mainDisplay, theMain, enemy1)

    mainGroup = pygame.sprite.Group()
    enemyGroup = pygame.sprite.Group()

    mainGroup.add(theMain)
    enemyGroup.add(enemy1)

    while True:
        Clock.tick(FPS)
        mainDisplay.blit(bg_image, (0,0))

        handleEvents.listen(pygame.event.get())
                
        theMain.loop()
        theMain.theMove()
        theMain.handle_attack()
        # theMain.check_collision(enemyGroup)

        enemy1.loop()
        enemy1.detect()
        # enemy1.check_collision(mainGroup)
        # enemy1.move()
        
        handleEvents.draw()



if __name__ == "__main__":      #only runs game through this file directly
    main(mainDisplay)