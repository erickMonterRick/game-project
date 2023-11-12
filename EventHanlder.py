import pygame

from Characters import*

class Event:
    def __init__(self, window,  mainC, enemy1 ):
        self.window = window
        self.mainC = mainC
        self.enemy1 = enemy1

    def listen(self, theEvents):
        self.queueOfEvents = theEvents
        for event in self.queueOfEvents:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


    def draw(self):
        self.mainC.draw(self.window)
        self.enemy1.draw(self.window)
        pygame.display.update()

