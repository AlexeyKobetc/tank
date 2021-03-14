import pygame
import sys
import os
import random
import math
import time
from pygame import *
from pygame import display

level_1 = ( 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
            'WGGGGG                                 W',
            'WGGGGGGG                               W',
            'WGGGGGGGGFG          F          F      W',
            'WGGGGGGGGFG          F          F      W',
            'WGGGGGGGFFF         FFF        FFF     W',
            'WGGGGGG FFF         FFF        FFF     W',
            'WGGGGG  FFF         FFF        FFF     W',
            'W GGG    F           F          F      W',
            'W  GE          E           E           W',
            'W                                      W',
            'WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF     W',
            'W                                   E  W',
            'W                                      W',
            'WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF     W',
            'W                                   E  W',
            'W                                      W',
            'W        P          F                  W',
            'W                                      W',
            'W       FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW',
            'W  E               E                   W',
            'W                                      W',
            'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW' )



NUM_BLOCK_WIDTH = 40
NUM_BLOCK_HEIGHT = 23

IMAGES_FILE_SPRITE_SIZE = 84

WALL_SPRITE_SIZE = IMAGES_FILE_SPRITE_SIZE // 2
BULLET_SPRITE_SIZE = IMAGES_FILE_SPRITE_SIZE // 3
WIN_WIDTH = WALL_SPRITE_SIZE * NUM_BLOCK_WIDTH
WIN_HEIGHT = WALL_SPRITE_SIZE * NUM_BLOCK_HEIGHT

BULLET_SPEED = 15

FPS = 30

class Block:
    def __init__(self, life, wall_image):

        #self.fontSize = 12

        #self.font = pygame.font.Font(None, self.fontSize)

        self.life = life
        self.image = wall_image
        self.bounds = self.image.get_rect()

        self.isLife = True
    
    def move(self, dx, dy):

        self.bounds.move_ip(dx, dy)

    def draw(self, surface):

        #life_text = self.font.render(str(self.life), 1, (255, 0, 255))

        surface.blit(self.image, [self.bounds.x, self.bounds.y])
        #surface.blit(life_text, (self.bounds.centerx, self.bounds.centery))

        #pygame.draw.rect(surface, Color("0x00FFF0"), self.bounds, 1)

class Tank:
    def __init__(self, life, speed, shoot_speed, images):

        #self.fontSize = 24

        #self.font = pygame.font.Font(None, self.fontSize)

        self.direction = 0
        self.animStep = random.randint(0, len(images) - 1)

        self.images_list = images[::-1]

        self.image = self.images_list[self.animStep]
        self.bounds = self.image.get_rect()

        self.bounds.height -= 10
        self.bounds.width -= 10

        self.life = life
        self.isCollision = False

        self.speed = speed
        self.shootspeed = shoot_speed
        self.shootTime = 0
        self.isShoot = False

        self.isLife = True

    def move(self, surface, dx, dy):
        
        self.original_image = self.images_list[self.animStep]

        self.animStep += 1
        if self.animStep >= len (self.images_list):
            self.animStep = 0

        self.bounds.move_ip(dx, dy)

        self.image = pygame.transform.rotate (self.images_list[self.animStep], self.direction * 90)

        surface.blit(self.image, (self.bounds.x - 5, self.bounds.y - 5))

    def rotate (self, rotate_direction):

        self.direction = rotate_direction
        self.image = pygame.transform.rotate (self.images_list[self.animStep], rotate_direction * 90)


    def draw (self, surface):

        #life_text = self.font.render(str(self.life), 1, (255, 0, 255))

        surface.blit(self.image, (self.bounds.x - 5, self.bounds.y - 5))
        #surface.blit(life_text, (self.bounds.centerx - self.fontSize, self.bounds.centery - self.fontSize // 2))
        #pygame.draw.rect(surface, Color("0x0FFF00"), self.bounds, 1)

class Bullet:
    def __init__(self, damage, images):

        self.direction = 0
        self.animStep = 0

        self.images_list = images

        self.image = self.images_list[self.animStep]
        self.bounds = self.image.get_rect()

        self.damage = damage

        self.isLife = True

    def move(self, surface, dx, dy):
        
        self.original_image = self.images_list[self.animStep]

        self.animStep += 1
        if self.animStep >= len (self.images_list):
            self.animStep = 0

        self.bounds.move_ip(dx, dy)

        self.image = pygame.transform.rotate (self.images_list[self.animStep], self.direction * 90)
        surface.blit(self.image, (self.bounds.x, self.bounds.y))

    def rotate (self, rotate_direction):

        self.direction = rotate_direction
        self.image = pygame.transform.rotate (self.images_list[self.animStep], rotate_direction * 90)

    def draw (self, surface):

        surface.blit(self.image, (self.bounds.x, self.bounds.y))
        #pygame.draw.rect(surface, Color("0x00FFF0"), self.bounds, 1)

class Explosion:
    def __init__(self, images):

        self.animStep = 0

        self.images_list = images

        self.image = self.images_list[self.animStep]
        self.bounds = self.image.get_rect()

        self.isLife = True

    def draw (self, surface):

        surface.blit(self.image, (self.bounds.x, self.bounds.y))
        #pygame.draw.rect(surface, Color("0x000FFF"), self.bounds, 1)

        self.animStep += 1
        if self.animStep >= len (self.images_list):
            self.isLife = False
        else:
            self.image = self.images_list[self.animStep]


class Game:
    def __init__(self, caption, frame_rate, back_image_file, sprites_image_file):

        pygame.init()

        self.background_image = pygame.image.load (back_image_file)
        self.background_image = pygame.transform.scale(self.background_image, (WIN_WIDTH , WIN_HEIGHT))
        self.frame_rate = frame_rate
        self.surface = pygame.display.set_mode((WIN_WIDTH , WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        pygame.display.set_caption(caption)

        #self.tanckTrackSound = pygame.mixer.Sound("D:/PROGS/Tanks/tada.wav")
        #self.tanckTrackSound.set_volume (0.5)


        self.playerTankMovement = 0
        self.isPlayerShoot = False
 
        self.sprites = pygame.image.load (sprites_image_file)
        self.green = pygame.image.load ("./green.png")

        self.walls = list()
        self.greens = list()
        self.playerTank = 0
        self.enemyTanks = list()
        self.bullets = list()
        self.explosions = list()

        self.player_images = list()
        self.enemy_images = list()
        self.bullet_images = list()
        self.wall_images = list()
        self.explosion_images = list()

        self.bullet_images.append ( pygame.transform.scale ( self.sprites.subsurface (IMAGES_FILE_SPRITE_SIZE * 4, IMAGES_FILE_SPRITE_SIZE * 2, IMAGES_FILE_SPRITE_SIZE * 1, IMAGES_FILE_SPRITE_SIZE), (BULLET_SPRITE_SIZE, BULLET_SPRITE_SIZE) ) )

        self.wall_images.append ( pygame.transform.scale ( self.sprites.subsurface (0, 0, IMAGES_FILE_SPRITE_SIZE, IMAGES_FILE_SPRITE_SIZE), (WALL_SPRITE_SIZE, WALL_SPRITE_SIZE) ) )
        self.wall_images.append ( pygame.transform.scale ( self.sprites.subsurface (IMAGES_FILE_SPRITE_SIZE * 2, IMAGES_FILE_SPRITE_SIZE * 3, IMAGES_FILE_SPRITE_SIZE, IMAGES_FILE_SPRITE_SIZE), (WALL_SPRITE_SIZE, WALL_SPRITE_SIZE) ) )
        self.wall_images.append ( pygame.transform.scale ( self.sprites.subsurface (IMAGES_FILE_SPRITE_SIZE * 4, IMAGES_FILE_SPRITE_SIZE * 3, IMAGES_FILE_SPRITE_SIZE, IMAGES_FILE_SPRITE_SIZE), (WALL_SPRITE_SIZE, WALL_SPRITE_SIZE) ) )

        for count in range (1, 8):
            self.player_images.append ( self.sprites.subsurface (count * IMAGES_FILE_SPRITE_SIZE, 0, IMAGES_FILE_SPRITE_SIZE, IMAGES_FILE_SPRITE_SIZE) )
        self.player_images.append ( self.sprites.subsurface (0, IMAGES_FILE_SPRITE_SIZE, IMAGES_FILE_SPRITE_SIZE, IMAGES_FILE_SPRITE_SIZE) )

        for count in range (1, 8):
            self.enemy_images.append ( self.sprites.subsurface (count * IMAGES_FILE_SPRITE_SIZE, IMAGES_FILE_SPRITE_SIZE, IMAGES_FILE_SPRITE_SIZE, IMAGES_FILE_SPRITE_SIZE) )
        self.enemy_images.append ( self.sprites.subsurface (0, IMAGES_FILE_SPRITE_SIZE * 2, IMAGES_FILE_SPRITE_SIZE, IMAGES_FILE_SPRITE_SIZE) )

        for count in range(1, 4):
            self.explosion_images.append ( self.sprites.subsurface (count * IMAGES_FILE_SPRITE_SIZE, IMAGES_FILE_SPRITE_SIZE * 2, IMAGES_FILE_SPRITE_SIZE, IMAGES_FILE_SPRITE_SIZE) )

        

        self.loadLevel (level_1)

    def loadLevel(self, Level):

        for row in range(len(Level)):
            for col in range(len(Level[row])):
                if Level[row][col] == "W" and (row == 0 or row == len(Level) - 1):

                    wall_block = Block(-9999, self.wall_images[2])
                    wall_block.bounds.x = col * WALL_SPRITE_SIZE
                    wall_block.bounds.y = row * WALL_SPRITE_SIZE
                    self.walls.append ( wall_block )

                elif Level[row][col] == "W" and (col == 0 or col == len(Level[row]) - 1):

                    wall_block = Block(-9999, self.wall_images[1])
                    wall_block.bounds.x = col * WALL_SPRITE_SIZE
                    wall_block.bounds.y = row * WALL_SPRITE_SIZE
                    self.walls.append ( wall_block )

                elif Level[row][col] == "W":

                    wall_block = Block(-9999, self.wall_images[2])
                    wall_block.bounds.x = col * WALL_SPRITE_SIZE
                    wall_block.bounds.y = row * WALL_SPRITE_SIZE
                    self.walls.append ( wall_block )

                elif Level[row][col] == "F":

                    fort_block = Block(500, self.wall_images[0])
                    fort_block.bounds.x = col * WALL_SPRITE_SIZE
                    fort_block.bounds.y = row * WALL_SPRITE_SIZE
                    self.walls.append ( fort_block )

                elif Level[row][col] == "G":

                    green_block = Block(100, self.green)
                    green_block.bounds.x = col * WALL_SPRITE_SIZE
                    green_block.bounds.y = row * WALL_SPRITE_SIZE
                    self.greens.append ( green_block )
                
                elif Level[row][col] == "E":

                    enemy_tank = Tank (1000, random.randint(2, 4), random.randint(3, 6) * 1000, self.enemy_images)
                    enemy_tank.move (self.surface, col * WALL_SPRITE_SIZE + 1, row * WALL_SPRITE_SIZE + 1)
                    self.enemyTanks.append ( enemy_tank )

                elif Level[row][col] == "P":

                    self.playerTank = Tank (1000, 3, 1, self.player_images)
                    self.playerTank.move (self.surface, col * WALL_SPRITE_SIZE + 1, row * WALL_SPRITE_SIZE + 1)

                    


    def playerTankMove(self):

        if self.playerTankMovement != 0:

            collision = 0

            if self.playerTankMovement == 1:

                for wall in self.walls:
                    if self.playerTank.bounds.left - self.playerTank.speed in range (wall.bounds.left, wall.bounds.right) \
                        and (self.playerTank.bounds.centery in range (wall.bounds.top, wall.bounds.bottom) \
                            or self.playerTank.bounds.top in range (wall.bounds.top, wall.bounds.bottom) \
                                or self.playerTank.bounds.bottom in range (wall.bounds.top, wall.bounds.bottom)):
                        collision = 1
                
                if collision == 0:
                    for tank in self.enemyTanks:
                        if self.playerTank.bounds.left - self.playerTank.speed in range (tank.bounds.left, tank.bounds.right) \
                            and (self.playerTank.bounds.centery in range (tank.bounds.top, tank.bounds.bottom) \
                                or self.playerTank.bounds.top in range (tank.bounds.top, tank.bounds.bottom) \
                                    or self.playerTank.bounds.bottom in range (tank.bounds.top, tank.bounds.bottom)):
                            collision = 1

                if collision == 0:
                    self.playerTank.move (self.surface, -self.playerTank.speed, 0)

            if self.playerTankMovement == 2:

                for wall in self.walls:
                    if self.playerTank.bounds.right + self.playerTank.speed in range (wall.bounds.left, wall.bounds.right) \
                        and (self.playerTank.bounds.centery in range (wall.bounds.top, wall.bounds.bottom) \
                            or self.playerTank.bounds.top in range (wall.bounds.top, wall.bounds.bottom) \
                                or self.playerTank.bounds.bottom in range (wall.bounds.top, wall.bounds.bottom)):
                        collision = 1
                
                if collision == 0:
                    for tank in self.enemyTanks:
                        if self.playerTank.bounds.right + self.playerTank.speed in range (tank.bounds.left, tank.bounds.right) \
                            and (self.playerTank.bounds.centery in range (tank.bounds.top, tank.bounds.bottom) \
                                or self.playerTank.bounds.top in range (tank.bounds.top, tank.bounds.bottom) \
                                    or self.playerTank.bounds.bottom in range (tank.bounds.top, tank.bounds.bottom)):
                            collision = 1

                if collision == 0:
                    self.playerTank.move (self.surface, self.playerTank.speed, 0)

            if self.playerTankMovement == 3:

                for wall in self.walls:
                    if self.playerTank.bounds.top - self.playerTank.speed in range (wall.bounds.top, wall.bounds.bottom) \
                        and (self.playerTank.bounds.centerx in range (wall.bounds.left, wall.bounds.right) \
                            or self.playerTank.bounds.left in range (wall.bounds.left, wall.bounds.right) \
                                or self.playerTank.bounds.right in range (wall.bounds.left, wall.bounds.right)):
                        collision = 1

                if collision == 0:
                    for tank in self.enemyTanks:
                        if self.playerTank.bounds.top - self.playerTank.speed in range (tank.bounds.top, tank.bounds.bottom) \
                            and (self.playerTank.bounds.centerx in range (tank.bounds.left, tank.bounds.right) \
                                or self.playerTank.bounds.left in range (tank.bounds.left, tank.bounds.right) \
                                    or self.playerTank.bounds.right in range (tank.bounds.left, tank.bounds.right)):
                            collision = 1

                if collision == 0:
                    self.playerTank.move (self.surface, 0, -self.playerTank.speed)

            if self.playerTankMovement == 4:

                for wall in self.walls:
                    if self.playerTank.bounds.bottom + self.playerTank.speed in range (wall.bounds.top, wall.bounds.bottom) \
                        and (self.playerTank.bounds.centerx in range (wall.bounds.left, wall.bounds.right) \
                            or self.playerTank.bounds.left in range (wall.bounds.left, wall.bounds.right) \
                                or self.playerTank.bounds.right in range (wall.bounds.left, wall.bounds.right)):
                        collision = 1

                if collision == 0:
                    for tank in self.enemyTanks:
                        if self.playerTank.bounds.bottom + self.playerTank.speed in range (tank.bounds.top, tank.bounds.bottom) \
                            and (self.playerTank.bounds.centerx in range (tank.bounds.left, tank.bounds.right) \
                                or self.playerTank.bounds.left in range (tank.bounds.left, tank.bounds.right) \
                                    or self.playerTank.bounds.right in range (tank.bounds.left, tank.bounds.right)):
                            collision = 1

                if collision == 0:
                    self.playerTank.move (self.surface, 0, self.playerTank.speed)
        
        else:

            pass

    def playerTankShoot(self):

        if self.isPlayerShoot == True:

            bullet = Bullet(100, self.bullet_images)

            if self.playerTank.direction == 0:

                bullet.bounds.x = self.playerTank.bounds.x + IMAGES_FILE_SPRITE_SIZE // 2 - BULLET_SPRITE_SIZE // 2 - 6
                bullet.bounds.y = self.playerTank.bounds.y - BULLET_SPRITE_SIZE
            
            elif self.playerTank.direction == 1:

                bullet.bounds.x = self.playerTank.bounds.x - BULLET_SPRITE_SIZE
                bullet.bounds.y = self.playerTank.bounds.y + IMAGES_FILE_SPRITE_SIZE // 2 - BULLET_SPRITE_SIZE // 2 - 6

            elif self.playerTank.direction == 2:

                bullet.bounds.x = self.playerTank.bounds.x + IMAGES_FILE_SPRITE_SIZE // 2 - BULLET_SPRITE_SIZE // 2 - 6
                bullet.bounds.y = self.playerTank.bounds.y + IMAGES_FILE_SPRITE_SIZE

            elif self.playerTank.direction == 3:

                bullet.bounds.x = self.playerTank.bounds.x + IMAGES_FILE_SPRITE_SIZE
                bullet.bounds.y = self.playerTank.bounds.y + IMAGES_FILE_SPRITE_SIZE // 2 - BULLET_SPRITE_SIZE // 2 - 6

            bullet.rotate (self.playerTank.direction)

            self.bullets.append ( bullet )

            self.isPlayerShoot = False

    def bulletMove(self):

        if len(self.bullets) > 0:

            self.bullets = [ bullet for bullet in self.bullets if not (bullet.bounds.right <= 0 or bullet.bounds.left > WIN_WIDTH or bullet.bounds.bottom <= 0 or bullet.bounds.top > WIN_HEIGHT or bullet.isLife == False) ]

            for bullet in self.bullets:

                if bullet.direction == 0 and bullet.isLife == True:

                    bullet.move (self.surface, 0, -BULLET_SPEED)

                elif bullet.direction == 1 and bullet.isLife == True:

                    bullet.move (self.surface, -BULLET_SPEED, 0)
                
                elif bullet.direction == 2 and bullet.isLife == True:

                    bullet.move (self.surface, 0, BULLET_SPEED)
                
                elif bullet.direction == 3 and bullet.isLife == True:

                    bullet.move (self.surface, BULLET_SPEED, 0)

                for wall in self.walls:

                    if bullet.bounds.centerx in range (wall.bounds.left, wall.bounds.right) and bullet.bounds.centery in range (wall.bounds.top, wall.bounds.bottom):

                        bullet.isLife = False

                        explosion = Explosion (self.explosion_images)
                        explosion.bounds.center = bullet.bounds.center
                        self.explosions.append (explosion)

                        if wall.life != -9999:
                            wall.life -= bullet.damage
                            if wall.life <= 0:
                                wall.isLife = False
                                self.walls = [ wall for wall in self.walls if wall.isLife == True ]
                
                for tank in self.enemyTanks:

                    if bullet.bounds.centerx in range (tank.bounds.left, tank.bounds.right) and bullet.bounds.centery in range (tank.bounds.top, tank.bounds.bottom):

                        bullet.isLife = False

                        explosion = Explosion (self.explosion_images)
                        explosion.bounds.center = bullet.bounds.center
                        self.explosions.append (explosion)

                        #tank.life -= bullet.damage
                        if tank.life <= 0:
                            tank.isLife = False
                            self.enemyTanks = [ tank for tank in self.enemyTanks if tank.isLife == True ]

                if bullet.bounds.centerx in range (self.playerTank.bounds.left, self.playerTank.bounds.right) and bullet.bounds.centery in range (self.playerTank.bounds.top, self.playerTank.bounds.bottom):
                    
                    bullet.isLife = False
                    explosion = Explosion (self.explosion_images)
                    explosion.bounds.center = bullet.bounds.center
                    self.explosions.append (explosion)

    def enemyTankMove(self):

        for tank in self.enemyTanks:

            if tank.isCollision == True:
                tank.rotate(random.randint(0, 3))
                tank.isCollision = False

            collision = 0

            if tank.direction == 1:

                for wall in self.walls:
                    if tank.bounds.left - tank.speed in range (wall.bounds.left, wall.bounds.right) \
                        and (tank.bounds.centery in range (wall.bounds.top, wall.bounds.bottom) \
                            or tank.bounds.top in range (wall.bounds.top, wall.bounds.bottom) \
                                or tank.bounds.bottom in range (wall.bounds.top, wall.bounds.bottom)):
                        collision = 1
                        tank.isCollision = True

                        if wall.life != -9999:
                            wall.life -= tank.life // 10
                            if wall.life <= 0:
                                wall.isLife = False
                                self.walls = [ wall for wall in self.walls if wall.isLife == True ]

                if collision == 0:
                    for other_tank in self.enemyTanks:
                        if tank.bounds.left - tank.speed in range (other_tank.bounds.left, other_tank.bounds.right) \
                            and (tank.bounds.centery in range (other_tank.bounds.top, other_tank.bounds.bottom) \
                                or tank.bounds.top in range (other_tank.bounds.top, other_tank.bounds.bottom) \
                                    or tank.bounds.bottom in range (other_tank.bounds.top, other_tank.bounds.bottom)) \
                                        and other_tank != tank:
                            collision = 1
                            tank.isCollision = True

                if collision == 0:
                    tank.move (self.surface, -tank.speed, 0)
            
            elif tank.direction == 3:

                for wall in self.walls:
                    if tank.bounds.right + tank.speed in range (wall.bounds.left, wall.bounds.right) \
                        and (tank.bounds.centery in range (wall.bounds.top, wall.bounds.bottom) \
                            or tank.bounds.top in range (wall.bounds.top, wall.bounds.bottom) \
                                or tank.bounds.bottom in range (wall.bounds.top, wall.bounds.bottom)):
                        collision = 1
                        tank.isCollision = True

                        if wall.life != -9999:
                            wall.life -= tank.life // 10
                            if wall.life <= 0:
                                wall.isLife = False
                                self.walls = [ wall for wall in self.walls if wall.isLife == True ]
                
                if collision == 0:
                    for other_tank in self.enemyTanks:
                        if tank.bounds.right + tank.speed in range (other_tank.bounds.left, other_tank.bounds.right) \
                            and (tank.bounds.centery in range (other_tank.bounds.top, other_tank.bounds.bottom) \
                                or tank.bounds.top in range (other_tank.bounds.top, other_tank.bounds.bottom) \
                                    or tank.bounds.bottom in range (other_tank.bounds.top, other_tank.bounds.bottom)) \
                                        and other_tank != tank:
                            collision = 1
                            tank.isCollision = True

                if collision == 0:
                    tank.move (self.surface, tank.speed, 0)

            elif tank.direction == 0:

                for wall in self.walls:
                    if tank.bounds.top - tank.speed in range (wall.bounds.top, wall.bounds.bottom) \
                        and (tank.bounds.centerx in range (wall.bounds.left, wall.bounds.right) \
                            or tank.bounds.left in range (wall.bounds.left, wall.bounds.right) \
                                or tank.bounds.right in range (wall.bounds.left, wall.bounds.right)):
                        collision = 1
                        tank.isCollision = True

                        if wall.life != -9999:
                            wall.life -= tank.life // 10
                            if wall.life <= 0:
                                wall.isLife = False
                                self.walls = [ wall for wall in self.walls if wall.isLife == True ]

                if collision == 0:
                    for other_tank in self.enemyTanks:
                        if tank.bounds.top - tank.speed in range (other_tank.bounds.top, other_tank.bounds.bottom) \
                            and (tank.bounds.centerx in range (other_tank.bounds.left, other_tank.bounds.right) \
                                or tank.bounds.left in range (other_tank.bounds.left, other_tank.bounds.right) \
                                    or tank.bounds.right in range (other_tank.bounds.left, other_tank.bounds.right)) \
                                        and other_tank != tank:
                            collision = 1
                            tank.isCollision = True

                if collision == 0:
                    tank.move (self.surface, 0, -tank.speed)

            elif tank.direction == 2:

                for wall in self.walls:
                    if tank.bounds.bottom + tank.speed in range (wall.bounds.top, wall.bounds.bottom) \
                        and (tank.bounds.centerx in range (wall.bounds.left, wall.bounds.right) \
                            or tank.bounds.left in range (wall.bounds.left, wall.bounds.right) \
                                or tank.bounds.right in range (wall.bounds.left, wall.bounds.right)):
                        collision = 1
                        tank.isCollision = True

                        if wall.life != -9999:
                            wall.life -= tank.life // 10
                            if wall.life <= 0:
                                wall.isLife = False
                                self.walls = [ wall for wall in self.walls if wall.isLife == True ]

                if collision == 0:
                    for other_tank in self.enemyTanks:
                        if tank.bounds.bottom + tank.speed in range (other_tank.bounds.top, other_tank.bounds.bottom) \
                            and (tank.bounds.centerx in range (other_tank.bounds.left, other_tank.bounds.right) \
                                or tank.bounds.left in range (other_tank.bounds.left, other_tank.bounds.right) \
                                    or tank.bounds.right in range (other_tank.bounds.left, other_tank.bounds.right)) \
                                        and other_tank != tank:
                            collision = 1
                            tank.isCollision = True

                if collision == 0:
                    tank.move (self.surface, 0, tank.speed)

    def enemyTankShoot(self):

        for tank in self.enemyTanks:

            if tank.isShoot == False:
                tank.shootTime = pygame.time.get_ticks()

                bullet = Bullet(100, self.bullet_images)

                if tank.direction == 0:

                    bullet.bounds.x = tank.bounds.x + IMAGES_FILE_SPRITE_SIZE // 2 - BULLET_SPRITE_SIZE // 2 - 6
                    bullet.bounds.y = tank.bounds.y - BULLET_SPRITE_SIZE
                
                elif tank.direction == 1:

                    bullet.bounds.x = tank.bounds.x - BULLET_SPRITE_SIZE
                    bullet.bounds.y = tank.bounds.y + IMAGES_FILE_SPRITE_SIZE // 2 - BULLET_SPRITE_SIZE // 2 - 6

                elif tank.direction == 2:

                    bullet.bounds.x = tank.bounds.x + IMAGES_FILE_SPRITE_SIZE // 2 - BULLET_SPRITE_SIZE // 2 - 6
                    bullet.bounds.y = tank.bounds.y + IMAGES_FILE_SPRITE_SIZE

                elif tank.direction == 3:

                    bullet.bounds.x = tank.bounds.x + IMAGES_FILE_SPRITE_SIZE
                    bullet.bounds.y = tank.bounds.y + IMAGES_FILE_SPRITE_SIZE // 2 - BULLET_SPRITE_SIZE // 2 - 6

                bullet.rotate (tank.direction)
                self.bullets.append ( bullet )
                tank.isShoot = True


            if tank.shootTime + tank.shootspeed < pygame.time.get_ticks():
                tank.isShoot = False




    def handle_events(self):
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_LEFT:
                
                self.playerTank.rotate (1)
                self.playerTankMovement = 1
                
            if event.type == KEYUP and event.key == K_LEFT:
                
                self.playerTankMovement = 0
                
            if event.type == KEYDOWN and event.key == K_RIGHT:
                
                self.playerTank.rotate (3)
                self.playerTankMovement = 2
                
            if event.type == KEYUP and event.key == K_RIGHT:
                
                self.playerTankMovement = 0

            if event.type == KEYDOWN and event.key == K_UP:
                
                self.playerTank.rotate (0)
                self.playerTankMovement = 3
                
            if event.type == KEYUP and event.key == K_UP:
                
                self.playerTankMovement = 0

            if event.type == KEYDOWN and event.key == K_DOWN:
                
                self.playerTank.rotate (2)
                self.playerTankMovement = 4
                
            if event.type == KEYUP and event.key == K_DOWN:
                
                self.playerTankMovement = 0

            if event.type == KEYDOWN and event.key == K_SPACE:
                
                if self.isPlayerShoot == False:
                    self.isPlayerShoot = True

    def draw (self):

        

        for wall in self.walls:
            if wall.isLife == True:
                wall.draw(self.surface)

        for enemy in self.enemyTanks:
            if enemy.isLife == True:
                enemy.draw(self.surface)

        self.playerTank.draw (self.surface)

        for greens in self.greens:
            if greens.isLife == True:
                greens.draw(self.surface)

        for bullet in self.bullets:
            if bullet.isLife == True:
                bullet.draw(self.surface)

        for explosion in self.explosions:
            if explosion.isLife == True:
                explosion.draw(self.surface)

    def run (self):

        while (True):

            if len( self.explosions ) > 0:
                self.explosions = [ explosion for explosion in self.explosions if explosion.isLife == True ]


            self.surface.blit(self.background_image, (0, 0))

            self.handle_events ()

            self.playerTankMove ()
            self.enemyTankMove ()
            self.bulletMove ()

            self.playerTankShoot ()
            self.enemyTankShoot ()

            self.draw ()

            pygame.display.update ()           
            self.clock.tick (self.frame_rate)

def main():

    game = Game ("Tanks !", FPS, "./back1.png", "./sprites.png")
    
    
    game.run ()

if __name__ == "__main__":

    main()