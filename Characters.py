import pygame
import os 

import math

from os import listdir
from os.path import isfile, join

# from Images import *

class Character(pygame.sprite.Sprite):
    def __init__(self,x, y, width, height,):

        #For the sprite
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, width, height)
        self.mask = None
        self.direction = "right"
        self.currentSprite = "Idle"
        self.frame = 0
        self.character = {}
        # self.offset = offset

        #For cooldown purposes
        self.attack_cooldown = 0
        self.timeUpdate = pygame.time.get_ticks()
        self.cooldown = 75

        #For movement 
        self.vel = 2
        self.x_vel = 0
        self.GRAVITY = .2 
        self.y_vel = 0
        self.jumpHeight = 0

        #For attack
        self.health = 100
        self.hit = False
        self.stunned_cooldown = 0
        self.Alive = True

        #To determine the current action of player
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

            if changeDirect:                                               #To have the sprite have options to face both directions
                self.character[image.replace(".png", "") + "_right"] = sprites
                self.character[image.replace(".png", "") + "_left"] = self.flip(sprites)
            
            else:                                                           #This would have sprite only face one direction
                self.character[image.replace(".png", "")] = sprites


    def jump(self):
        if self.stunned_cooldown == 0:
            self.jumping = True

    def attack(self, enemy_group):
        if self.attack_cooldown == 0 and self.stunned_cooldown == 0:   #This if statement prevents the player from spamming
            self.attack_cooldown = 50
            self.attacking = True
            self.check_collision(enemy_group)

    def update_sprite(self):        #this function creates the animation
        if self.health == 0:
            self.currentSprite = "Death"
        else:

            if self.stunned_cooldown > 0:
                self.attacking = False
                self.jumping = False
                self.running = False

            if self.running:        #this changes the animation to make it more smooth.
                self.currentSprite = self.change_animation(self.currentSprite, "Run")
            elif self.jumping:
                self.currentSprite = self.change_animation(self.currentSprite, "Jump")
            elif self.attacking:
                self.currentSprite = self.change_animation(self.currentSprite, "Attack")
            elif self.hit:
                self.currentSprite = self.change_animation(self.currentSprite, "Hit")
            else:
                self.currentSprite = self.change_animation(self.currentSprite, "Idle")


        image_sheet_name = "_" + self.currentSprite + "_" + self.direction
        sprites = self.character[image_sheet_name]

        
        if pygame.time.get_ticks() - self.timeUpdate > self.cooldown:       #changes frame based on a how much time has passed
            self.timeUpdate = pygame.time.get_ticks()
            self.frame += 1

        if self.attacking == True and self.frame == len(self.character[image_sheet_name]):  #this helps show the full attacking animation
            self.attacking = False
            
        if self.frame >= len(self.character[image_sheet_name]):     #once the frame goes through the last frame of the current action spritesheet, it would start again in the beginning. This to prevent the frame from going out of bounds 
            if self.health == 0:
                self.Alive = False
            self.frame = 0

        self.sprite = sprites[self.frame]


        self.rect = self.sprite.get_rect(topleft = (self.rect.x, self.rect.y))  #updates the rectangle of sprite
        self.mask = pygame.mask.from_surface(self.sprite)   #mask is for pixel collision

    def change_animation(self, current, desired):       #to change the action. If the desired action is the same as current, it would just leave since nothing needs to be done

        if current == desired:
            return current
        
        elif self.stunned_cooldown != 0:
            current = "Hit"
            self.frame = 0

        elif desired == "Jump":
            current = "Jump"
            self.frame = 0

        elif desired == "Run":
            current = "Run"
            self.frame = 0

        elif desired == "Attack":
            current = "Attack"
            self.frame = 0

        elif desired == "Idle":
            current = "Idle"
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
            self.update_sprite()    #to constantly have animation



    def draw(self, window):     #draws the sprite on screen
        if self.Alive:
            window.blit(self.sprite, (self.rect.x, self.rect.y ))

    def check_collision(self, enemy_group):
        # self.hit = False
        hits =  pygame.sprite.spritecollide(self, enemy_group, False, pygame.sprite.collide_mask)
        for element in hits:
            if element.health  != 0:
                element.health -= 10
                element.stunned_cooldown = 15
                element.hit = True
                print(f"Health: {element.health}")
            else:
                pass



class mainCharacter(Character):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        super().loadImages("MainCharacter", "Knight", width, height, True)
        

    def draw(self, window):
        super().draw(window)

    def handle_attack(self, enemy_group):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            super().attack(enemy_group)

    def theMove(self):      #this function handles the input that allows the character to move and jump
        self.x_vel = 0
        self.y_vel = 0 

        if self.stunned_cooldown == 0 and self.Alive:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                if self.jumping == False:
                    self.running = True
                self.x_vel = -self.vel
                if self.direction != "left":
                    self.direction = "left"
                    self.frame = 0
            elif keys[pygame.K_RIGHT]:
                if self.jumping == False:
                    self.running = True
                self.x_vel = self.vel
                if self.direction != "right":
                    self.direction = "right"
                    self.frame = 0

            elif keys[pygame.K_SPACE] and self.jumping == False:
                self.jumpHeight = -self.vel * 3
                self.jumping = True
            
            self.jumpHeight += self.GRAVITY
            self.y_vel += self.jumpHeight

            if self.rect.left + self.x_vel < 0:     #this is to prevent the player from going out of the screen
                self.x_vel -= self.rect.left 
            elif self.rect.right + self.x_vel > 800:
                self.x_vel = 800 - self.rect.right 

            if self.x_vel == 0: 
                self.running = False

            if self.rect.bottom + self.y_vel > 525:     #to prevent the player from going through the map
                self.jumping = False
                self.jumpHeight = 0
                self.y_vel = 525 - self.rect.bottom

            self.rect.x += self.x_vel
            self.rect.y += self.y_vel

    def check_collision(self, enemy_group):
        super().check_collision(enemy_group)

class EnemyKnight(Character):
    def __init__(self, x, y, width, height, mainC):
        super().__init__(x, y, width, height)
        super().loadImages("Enemies", "Enemy_Knight", width, height, True)
        self.mainC = mainC 
        self.direction = "left"
        self.move_cooldown = 0
        self.move_direction = "Left"
        self.vel = 2
        self.target = False
    
    
    def draw(self, window):
        super().draw(window)



    def loop(self):
        super().loop()
        if self.move_cooldown > 0:
            self.move_cooldown -= 1

    def detect(self, enemy_group):       #stack overflow. Question: How to target something in pygame

        if self.stunned_cooldown == 0 or self.mainC.health !=0:
            self.running = True
            if self.rect.x > self.mainC.rect.x and self.direction == "right":
                self.direction = "left"
            elif self.rect.x < self.mainC.rect.x and self.direction == "left":
                self.direction = "right"
            self.x_vel = self.mainC.rect.x - self.rect.x
            dist = math.hypot(self.x_vel)
            if dist > 60:
                self.x_vel = self.x_vel / dist 
                self.rect.x += self.x_vel 
            else:
                self.running = False
                self.attack(enemy_group)

    def attack(self, enemy_group):
        if self.mainC.health !=0:
            super().attack(enemy_group)

    def check_collision(self, enemy_group):
        super().check_collision(enemy_group)




    



    


