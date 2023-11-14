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

def main(mainDisplay):

    theMain = mainCharacter(CharacterX, CharacterY, CHARACTERWIDTH, CHARACTERHEIGHT ) #creating the main character
    mainGroup = pygame.sprite.Group()
    mainGroup.add(theMain)
    
    handleEvents = Event(mainDisplay, theMain, mainGroup)

 

    while True:
        Clock.tick(FPS)
        mainDisplay.blit(bg_image, (0,0))
        
        handleEvents.listen(pygame.event.get())
                
        theMain.loop()
        theMain.theMove()
        
        #added these
        handleEvents.waves()
        handleEvents.check()
        handleEvents.handleEnemies()
        handleEvents.handle_attack()
        handleEvents.draw()




if __name__ == "__main__":      #only runs game through this file directly
    main(mainDisplay)
