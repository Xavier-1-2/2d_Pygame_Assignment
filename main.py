import pygame
from sys import exit
import math
from player_data import *

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Shooter')
clock = pygame.time.Clock()

#Loads Images
background = pygame.transform.scale(pygame.image.load('Sprites/phbg.jpeg').convert(), (WIDTH, HEIGHT))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load('Sprites/Player_Shotgun/move/survivor-move_shotgun_0.png').convert_alpha(), 0, playersize)
        self.base_player_image = self.image
        self.pos = pygame.math.Vector2(playerstartx, playerstarty)
        self.hitbox_rect = self.base_player_image.get_rect(center = self.pos) #collsion
        self.rect = self.hitbox_rect.copy() #drawing player
        self.speed = playerspeed

    def user_input(self):
        self.velocity_x = 0
        self.velocity_y = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.velocity_y = -self.speed
        if keys[pygame.K_a]:
            self.velocity_x = -self.speed
        if keys[pygame.K_s]:
            self.velocity_y = self.speed
        if keys[pygame.K_d]:
            self.velocity_x = self.speed
        if self.velocity_x != 0 and self.velocity_y != 0: # diagonal movement
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)

    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)

    def update(self):
        self.user_input()
        self.move()

player = Player()

while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.blit(background, (0, 0))
    screen.blit(player.image, player.pos)
    player.update()
    pygame.display.update()
    clock.tick(60)