import pygame

from Character import *
from EventHandler import *



pygame.init()



mainDisplay = pygame.display.set_mode((800, 600))
   

Clock = pygame.time.Clock()


def main(mainDisplay):

    fps = 60
    
   
   

    Neo = theMain(50, 500)                   
    boss = Boss(700, 200)

    handleEvents = Event(mainDisplay, boss, Neo)
    handleEvents.load_background()

     
    while True:
        handleEvents.listen(pygame.event.get())
        if handleEvents.start == False and handleEvents.game_over == False:
            handleEvents.startScreen()

        elif handleEvents.game_over == False and handleEvents.start == True:
            handleEvents.draw_background()  
            Clock.tick(fps)

            

            # pygame.draw.rect(mainDisplay, (0,0,255), Neo.rect)

            handleEvents.handleWaves()
            handleEvents.spawnEnemeies()    
            
            handleEvents.check()
            handleEvents.handleEnemies()
        
            handleEvents.handle_cooldowns()
            # handleEvents.movePowerup()
            handleEvents.check_collision()
            

            handleEvents.scoreBoard()

            # handleEvents.handleBoss()
            handleEvents.draw()
            handleEvents.goFaster()

            
            

            Neo.loop()      #to get user input. Space for jump, d for ducking
            Neo.update_sprite()

        else:           #here is where the game ends, so insert end screen here
            mainDisplay.fill((0,255,0))
            handleEvents.showScore()
      

        pygame.display.update()

if __name__ == "__main__":      #only runs game through this file directly
    main(mainDisplay)


