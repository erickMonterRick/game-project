import pygame
import os

import random

import math

from os import listdir
from os.path import isfile, join

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, info):       #ignore most of these since it is for animation
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, 100, 160)                 #< -- focus here
        self.mask = None
        self.x,self.y = x, y
        self.action = 0         #0: idle, 1: run, 2: attack1, 3: jump, 4: range attack, 5: hit, 6: death
        self.frame = 0 
        self.size_width = info[0]
        self.size_height = info[1]
        self.image_scale = info[2]
        # self.offset = [60, 62]
        self.character = {}
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
        self.hit = False
        self.stunned_cooldown = 0
        self.Alive = True


        self.running = False
        self.jumping = False
        self.attacking = False


    def flip(self, sprites):        #to flip the sheets to face both directions
        return[pygame.transform.flip(sprite, True, False) for sprite in sprites]
    
    def loadImages(self, dir1, dir2, width, height, changeDirect):          #This function loads the images of the characters from spritesheet
        
        path = join(dir1, dir2)
        images = [f for f in listdir(path) if isfile(join(path, f))]
    
        for image in images:
            sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

            sprites = []

            for i in range(sprite_sheet.get_width()// width):
                surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
                rect =  pygame.Rect(i * width, 0, width, height)
                surface.blit(sprite_sheet, (0,0), rect)
                sprites.append(pygame.transform.scale2x(surface))
                # sprites.append((surface))

            if changeDirect:                                               #To have the sprite have options to face both directions
                self.character[image.replace(".png", "") + "_right"] = sprites
                self.character[image.replace(".png", "") + "_left"] = self.flip(sprites)
            
            else:                                                           #This would have sprite only face one direction
                self.character[image.replace(".png", "")] = sprites


    
    def load_sheet(self, sprite_sheet, animation_steps, flip = False):
    #extract images from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size_width, y * self.size_height, self.size_width, self.size_height)
                if flip:
                    temp_img = pygame.transform.flip(temp_img, True, False)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size_width * self.image_scale, self.size_height * self.image_scale)))
                # temp_img_list = self.flip(temp_img_list)
            animation_list.append(temp_img_list)

        # animation_list = self.flip(animation_list)
        return animation_list

    def loadImages(self, dir1, dir2, width, height, changeDirect):          #This function loads the images of the characters from spritesheet
        
        path = join(dir1, dir2)
        images = [f for f in listdir(path) if isfile(join(path, f))]
    
        for image in images:
            sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

            sprites = []

            for i in range(sprite_sheet.get_width()// width):
                surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
                rect =  pygame.Rect(i * width, 0, width, height)
                surface.blit(sprite_sheet, (0,0), rect)
                sprites.append(pygame.transform.scale_by(surface, 3))
                # sprites.append((surface))

            if changeDirect:                                               #To have the sprite have options to face both directions
                # self.character[image.replace(".png", "") + "_right"] = sprites
                self.character[image.replace(".png", "") + "_left"] = self.flip(sprites)
            
            else:                                                           #This would have sprite only face one direction
                self.character[image.replace(".png", "")] = sprites



    
    def draw(self, window, sprite):
        window.blit(sprite, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
        # window.blit(self.animation[self.action][self.frame], (self.rect.x, self.rect.y))

        

    

class theMain(Character):
    def __init__(self, x, y):
        main = pygame.image.load("Characters\Main\spritesheet.png").convert_alpha()
        animation_steps = [8,8,7,7,6,4,4,2]
        data = [64, 64, 3]
        self.ducking = False
        self.ducking_cooldown = 0
        self.offset = [50, 10]
        # self.currentSprite = "Run"
        super().__init__(x, y, data)
        self.animation = super().load_sheet(main, animation_steps)
        self.rect = pygame.Rect(x, y, 110, 135)
        

    def draw(self, window):
        super().draw(window)

    def jump(self):
        if self.stunned_cooldown == 0:
            self.jumping = True

    # def attack(self):
    #     super().attack()

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
            self.offset[1] = 70

         

        if self.ducking_cooldown > 0:
            self.ducking_cooldown -=1
        elif self.ducking_cooldown == 0 and self.ducking == True:
            self.rect.height = self.rect.height * 2     #reverts the rect back to orignal size, meaning ducking is finished
            self.offset[1] = 10
            self.ducking = False
            self.running = True

        self.jumpHeight += self.GRAVITY     #to make jumping possible
        self.y_vel += self.jumpHeight

        if self.rect.bottom + self.y_vel > 575:     #to prevent the player from going through the map
            self.jumping = False
            self.running = True
            self.jumpHeight = 0
            self.y_vel = 575 - self.rect.bottom


        if self.jumping == True:
            self.x_vel += self.vel *.1

        if self.rect.left + self.x_vel < 50:     #this is to prevent the player from going out of the screen
            self.x_vel -= self.rect.left 
        elif self.rect.right + self.x_vel > 800:
            self.x_vel = 800 - self.rect.right 

        self.rect.x += self.x_vel       #updates the rect of character
        self.rect.y += self.y_vel

        # super().loop()


    def update_sprite(self):
        if self.ducking == True or self.jumping == True:
            self.running = False

        if self.running:
            self.action = self.change_animation(self.action, 0)
        elif self.jumping:
            self.action = self.change_animation(self.action, 6)
        elif self.attacking:
            self.action = self.change_animation(self.action, 3)
        elif self.ducking:
            self.action = self.change_animation(self.action, 2)

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
        
        elif self.stunned_cooldown == 0:
            current = desired
            self.frame = 0

        return current


    def draw(self, window):
        
        window.blit(self.animation[self.action][self.frame], (self.rect.x - self.offset[0], self.rect.y - self.offset[1]))
        # window.blit(self.animation[self.action][self.frame], (self.rect.x, self.rect.y))

    

class groundEnemies(Character):
    def __init__(self, x, y):
        self.currentSprite = "Walk"
        self.direction = "left"
        data = [160, 128, 3]
        super().__init__(x, y, data)
        super().loadImages("Characters", "Ground_Enemy", 150, 150, True)
        self.rect = pygame.Rect(x, y, 90, 150)


    
    def update_sprite(self):
        if self.health > 0:
            self.running = True

        image_sheet_name =  self.currentSprite + "_" + self.direction
        sprites = self.character[image_sheet_name]

        
        if pygame.time.get_ticks() - self.timeUpdate > self.cooldown:       #changes frame based on a how much time has passed
            self.timeUpdate = pygame.time.get_ticks()
            self.frame += 1
        
        if self.frame >= len(self.character[image_sheet_name]):     #once the frame goes through the last frame of the current action spritesheet, it would start again in the beginning. This to prevent the frame from going out of bounds 
            if self.health == 0:
                self.Alive = False
            self.frame = 0

        self.sprite = sprites[self.frame]


    def draw(self, window):
        window.blit(self.sprite, (self.rect.x - 155, self.rect.y - 155))
        # window.blit(self.animation[self.action][self.frame], (self.rect.x, self.rect.y))

class flyingEnemies(Character):
    def __init__(self, x, y):
        self.currentSprite = "Flight"
        self.direction = "left"
        data = [160, 128, 3]
        super().__init__(x, y, data)
        super().loadImages("Characters", "Flying_Enemy", 150, 150, True)
        self.rect = pygame.Rect(x, y, 100, 100)

    def update_sprite(self):
        if self.health > 0:
            self.running = True

        image_sheet_name = self.currentSprite + "_" + self.direction
        sprites = self.character[image_sheet_name]

        
        if pygame.time.get_ticks() - self.timeUpdate > self.cooldown:       #changes frame based on a how much time has passed
            self.timeUpdate = pygame.time.get_ticks()
            self.frame += 1
        
        if self.frame >= len(self.character[image_sheet_name]):     #once the frame goes through the last frame of the current action spritesheet, it would start again in the beginning. This to prevent the frame from going out of bounds 
            if self.health == 0:
                self.Alive = False
            self.frame = 0

        self.sprite = sprites[self.frame]

    def draw(self, window):
        window.blit(self.sprite, (self.rect.x - 160, self.rect.y - 175))
        # window.blit(self.animation[self.action][self.frame], (self.rect.x, self.rect.y))





class Boss(Character):                      #ignore this class. It is not being used right now.
    def __init__(self, x, y):
        neo = pygame.image.load("Characters/Boss/Necromancer_creativekind-Sheet.png").convert_alpha()
        animation_steps = [8, 8, 13, 13, 17, 5, 10]
        data = [160, 128, 3]
        super().__init__(x, y, data)
        self.animation = super().load_sheet(neo, animation_steps, True)
        self.ground_attack_cooldown = 0
        self.ground_attack_rect = pygame.Rect(0, 500, 800, 100)
        self.high_attack_cooldown = 0
        self.high_attack_rect = pygame.Rect(0, 250, 800, 100)
        self.draw_cooldown = 0
        self.warning = False
        self.warning_shots = 0
        self.warning_cooldown = 0
        self.ground_fire = False

    def chooseAttack(self):
        randomAtt = random.randrange(0,2)
        if randomAtt == 0:
            self.groundAttack()
            

        elif randomAtt == 1:
            self.highAttack()


    def groundAttack(self):
        pass

    def highAttack(self):
        pass

    def loop(self):
        if self.ground_attack_cooldown > 0:
            self.ground_attack_cooldown -= 1

        if self.high_attack_cooldown > 0:
            self.high_attack_cooldown -= 1

        if self.draw_cooldown > 0:
            self.draw_cooldown -= 1

    def update_sprite(self):

        if self.running:
            self.action = self.change_animation(self.action, 1)
        elif self.jumping:
            self.action = self.change_animation(self.action, 6)
        elif self.attacking:
            self.action = self.change_animation(self.action, 3)
        else:
            self.action = self.change_animation(self.action, 1)

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
        
        elif self.stunned_cooldown == 0:
            current = desired
            self.frame = 0

        return current
    
    def draw(self, window):
        
        window.blit(self.animation[self.action][self.frame], (self.rect.x-180, self.rect.y - 200))
        # window.blit(self.animation[self.action][self.frame], (self.rect.x, self.rect.y))




    



    


