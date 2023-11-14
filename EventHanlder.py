import pygame
import random

from Characters import*

class Event:
    def __init__(self, window,  mainC, mainGroup):
        self.window = window
        self.mainC = mainC
        self.x = 540        #to place the enemies on the ground
        self.y = 365
        self.active_wave = False    #to check if a wave has spawned
        self.wave_number = 1        
        self.mainGroup = mainGroup
        self.enemyGroup = pygame.sprite.Group()        #sprite groups are to check mulitple collisions of the same type, like hitting multiple enemies
        self.enemies = [] #this would hold the enemies

    def listen(self, theEvents):
        self.queueOfEvents = theEvents
        for event in self.queueOfEvents:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def waves(self):
        if self.active_wave != True:        #if there is no wave
            self.active_wave = True
            i = 0
            while i < self.wave_number:        #it creates the enemies
                self.enemies.append(EnemyKnight(self.x + random.randrange(0,50, 10), self.y, 120, 180, self.mainC))
                self.enemyGroup.add(self.enemies[i])    #adds to sprite group
                i += 1
            self.wave_number +=1    #increases wave number 

    def check(self):
        for enemy in self.enemies:    #if there is an enemy that is alive 
            if enemy.health > 0:
                return                 #it make sures that the another wave does not happen
        self.active_wave = False

    def handleEnemies(self):        #creates the interactions for enemies and draws on screen
        for enemy in self.enemies:
            enemy.loop()
            enemy.detect(self.mainGroup)
            enemy.draw(self.window)

    def handle_attack(self):        #to handle the attack of main (to avoid issues with sprite group)
        self.mainC.handle_attack(self.enemyGroup)


    def draw(self):
        self.mainC.draw(self.window)
        pygame.display.update()

