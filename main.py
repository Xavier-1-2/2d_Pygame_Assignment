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
        self.pos = pygame.math.Vector2(playerstartx, playerstarty)
        self.image = pygame.transform.rotozoom(pygame.image.load('Sprites/Player_Shotgun/move/survivor-move_shotgun_0.png').convert_alpha(), 0, playersize)
        self.base_player_image = self.image
        self.hitbox_rect = self.base_player_image.get_rect(center = self.pos) #collsion
        self.rect = self.hitbox_rect.copy() #drawing player
        self.speed = playerspeed
        self.shoot = False
        self.shoot_cooldown = 0
        self.barreloffset = pygame.math.Vector2(gox, goy)

    def player_rotation(self):
        self.mouse_coords = pygame.mouse.get_pos()
        self.x_mouse_player = (self.mouse_coords[0] - self.hitbox_rect.centerx)
        self.y_mouse_player = (self.mouse_coords[1] - self.hitbox_rect.centery)
        self.angle = math.degrees(math.atan2(self.y_mouse_player, self.x_mouse_player))
        self.image = pygame.transform.rotate(self.base_player_image, -self.angle)
        self.rect = self.image.get_rect(center = self.hitbox_rect.center)


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

        if pygame.mouse.get_pressed()== (1,0,0) or keys[pygame.K_SPACE]: #Left Mouse Key or Space
            self.shoot = True
            self.isShooting()
        else:
            self.shoot = False

    def isShooting(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = ShotCooldown
            spawn_bul_pos = self.pos + self.barreloffset.rotate(self.angle)
            self.bullet = Bullet(spawn_bul_pos[0], spawn_bul_pos[1], self.angle)
            bullet_groups.add(self.bullet)
            all_sprite_groups.add(self.bullet)

    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center

    def update(self):
        self.user_input()
        self.move()
        self.player_rotation()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.image.load("Sprites/Bullet1.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image,0,bulletsize)
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = bulletspeed
        self.x_vel = math.cos(self.angle * (2* math.pi / 360)) * self.speed
        self.y_vel = math.sin(self.angle * (2* math.pi / 360)) * self.speed
        self.bulletlife = bulletlife
        self.spawntime = pygame.time.get_ticks()

    def bullet_move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if pygame.time.get_ticks() - self.spawntime > self.bulletlife:
            self.kill()

    def update(self):
        self.bullet_move()

all_sprite_groups = pygame.sprite.Group()
bullet_groups = pygame.sprite.Group()
player = Player()
all_sprite_groups.add(player)

while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.blit(background, (0, 0))
    all_sprite_groups.draw(screen)
    all_sprite_groups.update()
    pygame.draw.rect(screen, "red", player.hitbox_rect, width=2)
    pygame.draw.rect(screen, "green", player.rect, width=2)
    pygame.display.update()
    clock.tick(60)