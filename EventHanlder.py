import pygame

import random

from Character import*

class Event:
    def __init__(self, window, boss, main):
        self.window = window
        self.active_wave = False
        self.x = self.window.get_width()
        self.flying_y = 325
        self.ground_y = 425
        self.vel = 3
        self.spawn_cooldown = 0
        self.waves = 0
        self.score = 0
        self.scroll = 0
        self.scroll_speed = 5
        self.score_cooldown = 0
        self.boss = boss
        self.boss_cooldown = 0
        self.enemies = []
        self.faster_cooldown = 1000
        self.updateTime = pygame.time.get_ticks()
        self.main = main

    def listen(self, theEvents):
        self.queueOfEvents = theEvents
        for event in self.queueOfEvents:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()



    def load_background(self):      #loads the background
        self.bg_images = []

        for i in range(0, 6):
            if i < 5:
                bg_image = pygame.image.load(f"Background/{i}.png").convert_alpha()
                bg_image = pygame.transform.scale(bg_image, (600,600))
                self.bg_images.append(bg_image)
            else:
                self.ground_image = pygame.image.load(f"Background/{i}.png")
                self.ground_image = pygame.transform.scale(self.ground_image, (800,100))

        

    def draw_background(self):      #creates the parrallox effect (scrolling)
        bg_width = self.bg_images[4].get_width()


        ground_width = self.ground_image.get_width()
        ground_height = self.ground_image.get_height()

        for x in range(4):
            speed = 1
            for i in self.bg_images:
                self.window.blit(i, ((x * bg_width + self.scroll * speed),0))
                speed +=.2

        for y in range(15):
            self.window.blit(self.ground_image, ((y * ground_width) + self.scroll * 2.5, 550))

        self.scroll -= self.scroll_speed
        if abs(self.scroll) > bg_width:
            self.scroll = 0

    
    def handleWaves(self):      #keeps track of how many waves have passed
        if self.active_wave != True:
            self.active_wave = True
            self.waves += 1

    def spawnEnemeies(self):        #creates and draws the enemies 
        if self.active_wave == False:
            return
        else:
            if len(self.enemies) < 3 and self.spawn_cooldown == 0:
                random_number = random.randrange(0,2)
                if random_number == 0:
                    self.enemies.append(flyingEnemies(self.x + random.randrange(0,250, 50), self.flying_y))
                else:
                    self.enemies.append(groundEnemies(self.x + random.randrange(0,250, 50), self.ground_y))
                self.spawn_cooldown = 125
            else: 
                return

    def check(self):        #check to see if enemies are out of the screen. If yes, then it would remove them from list
        checker = 0
        size_of_wave = len(self.enemies)
        for enemy in self.enemies:
            if enemy.rect.x < 0:
                checker += 1
        if checker == size_of_wave:
            self.active_wave = False

    def handleEnemies(self):        
        for enemy in self.enemies:  
            bottomr, _ = enemy.rect.bottomright
            if bottomr > 0:
                self.check_collision(enemy)
                # enemy.loop()
                enemy.rect.x -= self.vel * 2
                pygame.draw.rect(self.window, (255,0,0), enemy.rect)
            else:
                self.enemies.remove(enemy)

    def check_collision(self, enemy):
        if pygame.Rect.colliderect(enemy.rect, self.main.rect):
            pygame.quit()       #game would force quit if the main rect collides with enemy rect. For testing purposes
            print("Game Over")



    def scoreBoard(self):
        if self.score_cooldown == 0:
            self.score += 5
            self.score_cooldown = 25
            print(self.score)

    def handle_cooldowns(self):
        if self.spawn_cooldown > 0:
            self.spawn_cooldown -=1

        if self.score_cooldown > 0:
            self.score_cooldown -=1

        if self.boss_cooldown > 0:
            self.boss_cooldown -= 1

        if self.faster_cooldown > 0:
            self.faster_cooldown -= 10



       
'''        Ignore this for now
    def spawnBoss(self):
        pygame.draw.rect(self.window, (255,0,0), self.boss.rect)

    def handleBoss(self):

        if self.score > 50:
            self.spawnBoss()
            randomAtt = random.randrange(0,2)
            if randomAtt == 0 and self.boss_cooldown == 0:
                self.boss_cooldown = 300
                self.boss.groundAttack()

            elif randomAtt == 1 and self.boss_cooldown == 0:
                self.boss_cooldown = 300
                self.boss.highAttack()



        
    def goFaster(self):

        if self.score > 30 and self.faster_cooldown == 0:
            self.faster_cooldown = 250
            print(self.vel)
            self.vel += .2
            self.scroll_speed += .1

'''



