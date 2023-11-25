import pygame

from Character import *
from EventHandler import *



pygame.init()



mainDisplay = pygame.display.set_mode((800, 600))





Clock = pygame.time.Clock()


def main(mainDisplay):

    fps = 60

   
   

    Neo = Necromancer(0, 500)                       #suppose to be main character. Lazy to rename
    boss = Boss(700, 200)

    handleEvents = Event(mainDisplay, boss, Neo)
    handleEvents.load_background()

     
    while True:
        handleEvents.draw_background()
        Clock.tick(fps)


        handleEvents.listen(pygame.event.get())


        pygame.draw.rect(mainDisplay, (0,0,255), Neo.rect)



        handleEvents.handleWaves()
        handleEvents.spawnEnemeies()
        handleEvents.scoreBoard()
        handleEvents.check()
        handleEvents.handleEnemies()

        handleEvents.handle_cooldowns()

        # handleEvents.handleBoss()
        # handleEvents.goFaster()

        
        

        Neo.loop()      #to get user input. Space for jump, d for ducking

        pygame.display.update()

if __name__ == "__main__":      #only runs game through this file directly
    main(mainDisplay)

