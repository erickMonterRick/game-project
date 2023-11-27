import pygame

import random

from Character import*

#you can insert music and sounds in this class

class Event:
    def __init__(self, window, boss, main):
        self.window = window
        self.x = self.window.get_width()

        self.scroll = 0
        self.scroll_speed = 5

        self.flying_y = 375
        self.ground_y = 425
        self.vel = 3

        self.active_wave = False
        self.waves = 0
        self.spawn_cooldown = 0
        self.enemies = []

        self.score = 0
        self.score_cooldown = 0
        self.font = pygame.font.SysFont("arial", 50, True)
        
        self.superCharge = pygame.Rect(600, self.flying_y - 100, 50, 50)
        self.powerup_cooldown = 1000
        self.powerup_active = False

        self.boss = boss
        self.boss_cooldown = 0
        self.boss_active = False

        self.faster_cooldown = 1000

        self.start = False
        self.game_over = False

        self.main = main
        self.mainGroup = pygame.sprite.Group()
        self.mainGroup.add(self.main)


        

    def listen(self, theEvents):
        self.queueOfEvents = theEvents
        for event in self.queueOfEvents:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def startScreen(self):              #insert start screen code here
        self.window.fill((0,255,0))
        keys = pygame.key.get_pressed()
        self.main.action = 5
        self.main.offset[1] = 50
        self.draw()
        self.main.update_sprite()
        if keys[pygame.K_0]:
            self.start = True
            self.main.offset[1] = 10



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
        if abs(self.scroll)  > bg_width:
            self.scroll = 0

    

    
    def handleWaves(self):      #keeps track of how many waves have passed
        if self.active_wave != True:
            self.active_wave = True
            self.waves += 1

    def spawnEnemeies(self):        #creates and draws the enemies 
        if self.active_wave == False:
            return
        elif self.boss_active != True:
            if len(self.enemies) < 4 and self.spawn_cooldown == 0:
                random_number = random.randrange(0,2)
                if random_number == 0:
                    self.enemies.append(flyingEnemies(self.x + random.randrange(0,250, 50), self.flying_y))
                else:
                    self.enemies.append(groundEnemies(self.x + random.randrange(0,250, 50), self.ground_y))
                self.spawn_cooldown = 100
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
                self.check_enemy_collision(enemy)
                # enemy.loop()
                enemy.rect.x -= self.vel * 2
                # pygame.draw.rect(self.window, (255,0,0), enemy.rect)
            else:
                self.enemies.remove(enemy)

    def check_enemy_collision(self, enemy):
        if pygame.Rect.colliderect(enemy.rect, self.main.rect):
            if pygame.sprite.spritecollide(enemy, self.mainGroup, False):
                self.game_over = True       #game would force quit if the main rect collides with enemy rect. For testing purposes
                print("Game Over")



    def scoreBoard(self):
        if self.score_cooldown == 0:
            self.score += 1
            self.score_cooldown = 10
        self.showScore()

    def showScore(self):
        if self.game_over == False:
            self.score_text = self.font.render(f"Score: {self.score} meters", True, (255,255,255), None)
        else:
            self.score_text = self.font.render(f"Final Score: {self.score} meters", True, (255,255,255), None)
        textRect = self.score_text.get_rect()
        textRect.center = (400,50)
        self.window.blit(self.score_text, textRect)

    def handle_cooldowns(self):
        if self.spawn_cooldown > 0:
            self.spawn_cooldown -=1

        if self.score_cooldown > 0:
            self.score_cooldown -=1

        if self.boss_cooldown > 0:
            self.boss_cooldown -= 1

        if self.faster_cooldown > 0:
            self.faster_cooldown -= 10

        if self.powerup_cooldown > 0:
            self.powerup_cooldown -= 5
        elif self.powerup_cooldown == 0:
            self.powerup_active = True

            



    def check_collision(self):
        if pygame.Rect.colliderect(self.superCharge, self.main.rect):
            self.powerup_active = False
            self.powerup_cooldown = 1000

    
    def draw(self):
        for enemy in self.enemies:
            enemy.update_sprite()
            enemy.draw(self.window)
        self.main.draw(self.window)
        if self.boss_active == True:
            self.boss.draw(self.window)

    def goFaster(self):

        if self.score % 20 == 0 and self.faster_cooldown == 0:
            self.faster_cooldown = 100
            self.vel += .2
            self.scroll_speed += .1

    def spawnBoss(self):
        pygame.draw.rect(self.window, (255,0,0), self.boss.rect)

    
    def handleBoss(self):            #Dont worry about this for now
        if self.score > 300:
            self.spawnBoss()
            self.boss_active = True
            self.boss.update_sprite()
            if self.boss_cooldown == 0:
                self.boss_cooldown = 300
                self.boss.chooseAttack()
            if self.boss.warning == True or self.boss.ground_fire == True:
                
                pygame.draw.rect(self.window, (255,0,0), self.boss.ground_attack_rect)



