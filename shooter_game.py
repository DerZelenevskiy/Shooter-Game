import pygame
import random
from time import sleep

width = 800
height = 600
fps = 60

pygame.init()
win = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

pygame.mixer.music.load('space.ogg')
pygame.mixer.music.play()
font = pygame.font.SysFont('Arial', 24)

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def blit(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, image, x, y):
        self.image = pygame.transform.scale(pygame.image.load(image), (100, 150))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.last = 0

    def move(self, keys):
        if keys[pygame.K_a] and self.rect.x >= 8:
            self.rect.x -= 8
        if keys[pygame.K_d] and self.rect.x <= 792-100:
            self.rect.x += 8
        if keys[pygame.K_w] and self.rect.y >= 8:
            self.rect.y -= 8
        if keys[pygame.K_s] and self.rect.y <= 592-150:
            self.rect.y += 8
        
    def fire(self, keys, frames):
        if keys[pygame.K_SPACE] and frames - 15 >= self.last:
            bullets.append(Bullet('bullet.png', self.rect.x+45, self.rect.y))
            self.last = frames

class Enemy(GameSprite):
    def __init__(self, image):
        self.image = pygame.transform.scale(pygame.image.load(image), (125, 75))
        self.rect = self.image.get_rect()
        self.rect.y = -75
        self.rect.x = random.randint(0, 675)

    def move(self):
        self.rect.y += 3

class Bullet(GameSprite):
    def __init__(self, image, x, y):
        self.image = pygame.transform.scale(pygame.image.load(image), (10, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self):
        self.rect.y -= 8


class Bg():
    def __init__(self, image):
        self.image = pygame.transform.scale(pygame.image.load(image), (800, 600))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def blit(self, win):
        if self.rect.y < 600:
            win.blit(self.image, (self.rect.x, self.rect.y))
            win.blit(self.image, (self.rect.x, self.rect.y-600))
            self.rect.y += 3
        else:
            self.rect.y = 0

player = Player('rocket.png', 350, 450)
bg = Bg('space.jpg')
enemys = list()
bullets = list()

game = True
res = None
score = 0
missed = 0
frames = 0
ticks = 45

while True:
    clock.tick(fps)

    if game == True:

        curFPS = clock.get_fps()
        curFPS = font.render(str(round(curFPS, 1)), 24, (255, 255, 255))
        curScore = font.render(f'Счёт: {str(score)}', 24, (255, 255, 255))
        curMissed = font.render(f'Пропущено: {str(missed)}', 24, (255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        keys = pygame.key.get_pressed()

        bg.blit(win)

        if ticks == 0:
            enemys.append(Enemy('ufo.png'))
            ticks = 45
        for i in enemys:
            i.move()
            if i.rect.y > 600:
                enemys.remove(i)
                missed += 1
            if i.rect.colliderect(player):
                game = False
                res = False
        
        for i in bullets:
            for enemy in enemys:
                if i.rect.colliderect(enemy):
                    score += 1
                    bullets.remove(i)
                    enemys.remove(enemy)
            i.move()
            if i.rect.y < 50 and i in bullets:
                bullets.remove(i)

        for i in enemys:
            i.blit(win)
        for i in bullets:
            i.blit(win)
        player.move(keys)
        player.fire(keys, frames)
        player.blit(win)

        win.blit(curFPS, (755, 0))
        win.blit(curScore, (0, 0))
        win.blit(curMissed, (0, 25))

        pygame.display.update()

        if score >= 50:
            game = False
            res = True

        if missed >= 5:
            game = False
            res = False

        ticks -= 1
        frames += 1
    else:
        if res == True:
            win.fill((0, 255, 0))
            win.blit(pygame.font.SysFont('Arial', 50).render('YOU WIN!', 50, (255, 255, 255)), (275, 250))

        if res == False:
            win.fill((255, 0, 0))
            win.blit(pygame.font.SysFont('Arial', 50).render('YOU LOSE!', 50, (255, 255, 255)), (275, 250))
        
        pygame.display.update()
        sleep(3)
        player.rect.x = 350
        player.rect.y = 450
        enemys.clear()
        bullets.clear()
        score = 0
        missed = 0
        res = None
        game = True