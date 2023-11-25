import pygame
import os

import math

from os import listdir
from os.path import isfile, join

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, info, spriteSheet, animation_steps):       #ignore most of these since it is for animation
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, 100, 160)                 #< -- focus here
        self.mask = None
        self.x,self.y = x, y
        self.action = 0         #0: idle, 1: run, 2: attack1, 3: jump, 4: range attack, 5: hit, 6: death
        self.frame = 0 
        self.size_width = info[0]
        self.size_height = info[1]
        self.image_scale = info[2]
        self.offset = [60, 62]
        # self.animation = self.load_images(spriteSheet, animation_steps)

        self.vel = 3.5                                      #< -- and this section here
        self.x_vel = 0
        self.GRAVITY = .5 
        self.y_vel = 0
        self.jumpHeight = 0

        self.attack_cooldown = 0
        self.timeUpdate = pygame.time.get_ticks()
        self.cooldown = 100

        self.health = 100
        self.strength = 50
        self.strength_active = 0
        self.hit = False
        self.stunned_cooldown = 0
        self.Alive = True


        self.running = False
        self.jumping = False
        self.attacking = False

'''         Whole section is for sprites animation. Dealing with rects for now
def join_images(self, dir1, dir2 ):
        path = join(dir1, dir2)
        images = [f for f in listdir(path) if isfile(join(path, f))]
    
        return images


    
    def load_images(self, sprite_sheet, animation_steps):
    #extract images from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size_width, y * self.size_height, self.size_width, self.size_height)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size_width * self.image_scale, self.size_height * self.image_scale)))
                # temp_img_list = self.flip(temp_img_list)
            animation_list.append(temp_img_list)

        # animation_list = self.flip(animation_list)
        return animation_list
    
    def flip(self, sprites):        #to flip the sheets to face both directions
        return[pygame.transform.flip(sprite, True, False) for sprite in sprites]
    
    def update_sprite(self):
        if self.stunned_cooldown > 0:
            self.attacking = False
            self.jumping = False
            self.running = False

        if self.running:
            self.action = self.change_animation(self.action, 1)
        elif self.jumping:
            self.action = self.change_animation(self.action, 3)
        elif self.attacking:
            self.action = self.change_animation(self.action, 2)
        elif self.hit:
            self.action = self.change_animation(self.action, 4)
        else:
            self.action = self.change_animation(self.action, 0)

        sprites = self.animation[self.action]

        if pygame.time.get_ticks() - self.timeUpdate > self.cooldown:       #changes frame based on a how much time has passed
            self.timeUpdate = pygame.time.get_ticks()
            self.frame += 1

        if self.attacking == True and self.frame == len(self.animation[self.action]):  #this helps show the full attacking animation
            self.attacking = False
            
        if self.frame >= len(self.animation[self.action]):     #once the frame goes through the last frame of the current action spritesheet, it would start again in the beginning. This to prevent the frame from going out of bounds 
            if self.health == 0:
                self.Alive = False
            self.frame = 0

        self.sprite = sprites[self.frame]


        # self.rect = self.sprite.get_rect(topleft = (self.rect.x, self.rect.y))  #updates the rectangle of sprite
        self.mask = pygame.mask.from_surface(self.sprite) 


    def change_animation(self, current, desired):       #to change the action. If the desired action is the same as current, it would just leave since nothing needs to be done

        if current == desired:
            return current
        
        elif self.stunned_cooldown != 0:
            current = desired
            self.frame = 0

        return current

    def loop(self):
        if self.Alive:
            if self.attack_cooldown > 0:
                self.attack_cooldown -=1  #to handle the attack_cooldown 

            if self.stunned_cooldown > 0:
                self.stunned_cooldown -=1
            elif self.stunned_cooldown == 0:
                self.hit = False

            # if self.strength_active > 0:
            #     self.strength_active -= 1
            # elif self.strength_active == 0 and self.strength/2 > 0:
            #     self.strength = self.strength/2

            
            self.update_sprite() 

    def attack(self):
        if self.attack_cooldown == 0 and self.stunned_cooldown == 0:   #This if statement prevents the player from spamming
            self.attack_cooldown = self.strength
            self.attacking = True


    
    def draw(self, window):
        window.blit(self.animation[self.action][self.frame], (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
        # window.blit(self.animation[self.action][self.frame], (self.rect.x, self.rect.y))
'''
        

    

class Necromancer(Character):
    def __init__(self, x, y):
        neo = pygame.image.load("Characters/Boss/Necromancer_creativekind-Sheet.png").convert_alpha()
        animation_steps = [8, 8, 13, 13, 17, 5, 10]
        data = [160, 128, 3]
        self.ducking = False
        self.ducking_cooldown = 0
        super().__init__(x, y, data, neo, animation_steps)
        

    def draw(self, window):
        super().draw(window)

    def jump(self):
        if self.stunned_cooldown == 0:
            self.jumping = True

    def attack(self):
        super().attack()

    def loop(self):
        self.x_vel = 0
        self.y_vel = 0 

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.jumping == False and self.ducking == False:        #for jumping
            self.jumpHeight = -self.vel * 5
            self.jumping = True
        elif keys[pygame.K_d] and self.ducking == False and self.jumping == False:         #for ducking
            self.ducking = True
            self.ducking_cooldown = 75
            self.rect.height = self.rect.height / 2     #this creates the smaller rect

            

        if self.ducking_cooldown > 0:
            self.ducking_cooldown -=1
        elif self.ducking_cooldown == 0 and self.ducking == True:
            self.rect.height = self.rect.height * 2     #reverts the rect back to orignal size, meaning ducking is finished
            self.ducking = False

        self.jumpHeight += self.GRAVITY     #to make jumping possible
        self.y_vel += self.jumpHeight

        if self.rect.bottom + self.y_vel > 575:     #to prevent the player from going through the map
            self.jumping = False
            self.jumpHeight = 0
            self.y_vel = 575 - self.rect.bottom

        if self.jumping == True:
            self.x_vel += self.vel *.1

        if self.rect.left + self.x_vel < 0:     #this is to prevent the player from going out of the screen
            self.x_vel -= self.rect.left 
        elif self.rect.right + self.x_vel > 800:
            self.x_vel = 800 - self.rect.right 

        self.rect.x += self.x_vel       #updates the rect of character
        self.rect.y += self.y_vel

        # super().loop()

class groundEnemies(Character):
    def __init__(self, x, y):
        neo = pygame.image.load("Characters/Boss/Necromancer_creativekind-Sheet.png").convert_alpha()
        animation_steps = [8, 8, 13, 13, 17, 5, 10]
        data = [160, 128, 3]
        super().__init__(x, y, data, neo, animation_steps)


class flyingEnemies(Character):
    def __init__(self, x, y):
        neo = pygame.image.load("Characters/Boss/Necromancer_creativekind-Sheet.png").convert_alpha()
        animation_steps = [8, 8, 13, 13, 17, 5, 10]
        data = [160, 128, 3]
        super().__init__(x, y, data, neo, animation_steps)

class Boss(Character):                      #ignore this class. It is not being used right now.
    def __init__(self, x, y):
        neo = pygame.image.load("Characters/Boss/Necromancer_creativekind-Sheet.png").convert_alpha()
        animation_steps = [8, 8, 13, 13, 17, 5, 10]
        data = [160, 128, 3]
        super().__init__(x, y, data, neo, animation_steps)
        self.ground_attack_cooldown = 0
        self.ground_attack_rect = pygame.Rect(0, 500, 800, 100)
        self.high_attack_cooldown = 0
        self.high_attack_rect = pygame.Rect(0, 250, 800, 100)
        self.draw_cooldown = 0
        self.warning = 0


    def groundAttack(self):
        if self.warning != 2 and self.draw_cooldown == 0:
            self.draw_cooldown = 25
            self.warning += 1

        if self.warning == 2 and self.draw_cooldown == 0:
            self.warning = 0
            if self.ground_attack_cooldown == 0:
                self.ground_attack_cooldown = 50

    def highAttack(self):
        if self.high_attack_cooldown == 0:
            self.high_attack_cooldown = 50

    def loop(self):
        if self.ground_attack_cooldown > 0:
            self.ground_attack_cooldown -= 1

        if self.high_attack_cooldown > 0:
            self.high_attack_cooldown -= 1

        if self.draw_cooldown > 0:
            self.draw_cooldown -= 1




    



    


