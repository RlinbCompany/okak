from pygame import * 
from random import randint
import sys
import os

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    elif hasattr(sys, "_MEIPASS2"):
        return os.path.join(sys._MEIPASS2, relative_path)
    else:
        return os.path.join(os.path.abspath("."), relative_path)
 
image_folder = resource_path(".")

# Инициалцзация 

mixer.init()
font.init()
# Парамтеры

WIDTH = 700
HEIGHT = 500
FPS = 60
MAX_LOST = 5
MAX_SCORE = 10
life = 3

RED = (150, 0, 0)
GREEN = (0, 150, 0)
WHITE = (250, 255, 255)
GRAY = (150, 150, 150)
DARK_GRAY = (100, 100, 100)

# Параметры окна
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Shooter YoY")
clock = time.Clock()
 
# Картинки и звуки
bak_sound = os.path.join(image_folder, "space.ogg")
bak_img = os.path.join(image_folder, "galaxy.jpg")
img_hero = os.path.join(image_folder, "rocket.png")
img_ufo = os.path.join(image_folder,"ufo.png")
img_bullet = os.path.join(image_folder,'bullet.png')
snd_fire = os.path.join(image_folder,'fire.ogg')
img_asteroid = os.path.join(image_folder,'asteroid.png')

font_text = font.Font(None, 36)
font_menu = font.Font(None, 70)
font_game = font.Font(None, 80)

win_text = font_game.render('Ты победил:(', True, GREEN)
lost_text = font_game.render('Ты проиграл:)', True, RED)

score = 0
lost = 0
# Параметры звука
mixer.music.load(bak_sound)
mixer.music.play()
mixer.music.set_volume(0.1)

fire_sound = mixer.Sound(snd_fire)
fire_sound.set_volume(0.1)

background = transform.scale(image.load(bak_img), (WIDTH, HEIGHT))
 
class GameSprite(sprite.Sprite):
    def __init__(self, p_image, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(p_image), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < WIDTH - self.rect.width - 5:
            self.rect.x += self.speed
 
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, 15)
        Bullets.add(bullet)
 
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= HEIGHT:
            self.rect.x = randint(0, WIDTH - self.rect.width) 
            self.rect.y = 0
            lost += 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= HEIGHT:
            self.rect.x = randint(0, WIDTH - self.rect.width) 
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

class Button:
    def __init__( self, text, x, y, w, h,):
        self.rect = Rect(x, y, w, h)
        self.text = text
        self.color = GRAY
        self.active = False

    def draw(self):
        mouse_pos = mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.color = DARK_GRAY 
        else:
            self.color = GRAY

        draw.rect(window, self.color, self.rect)
        text = font_menu.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        window.blit(text, text_rect)

    def is_clicked(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


start_button = Button("Старт", WIDTH // 2 - 100, HEIGHT // 2 - 60, 200, 80)
exit_button = Button("Выход", WIDTH // 2 - 100, HEIGHT // 2 + 40, 200, 80)
restart_button = Button("Рестарт", WIDTH // 2 - 100, HEIGHT // 2 + 40, 200, 80)
continue_button = Button("Дальше", WIDTH // 2 - 100, HEIGHT // 2 - 60, 200, 80)

player = Player(img_hero, 5, HEIGHT - 100, 80, 100, 10)

Bullets = sprite.Group()

monsters = sprite.Group()
asteroids = sprite.Group()

for i in range(6):
    monster = Enemy(img_ufo, randint(0, WIDTH - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

for i in range(3):
    asteroid = Asteroid(img_asteroid, randint(0, WIDTH - 80), -40, 80, 50, randint(1, 5))
    asteroids.add(asteroid)

def restart_game():
    global score, lost, life, finish
    score = 0
    lost = 0
    life = 3
    finish = False
    mosters = sprite.Group()
    asteroids = sprite.Group()
    Bullets = sprite.Group()

    for i in range(6):
        monster = Enemy(img_ufo, randint(0, WIDTH - 80), -40, 80, 50, randint(1, 5))
        monsters.add(monster)

    for i in range(3):
        asteroid = Asteroid(img_asteroid, randint(0, WIDTH - 80), -40, 80, 50, randint(1, 5))
        asteroids.add(asteroid)

run = True
finish = False
menu = True
paused = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE and not menu and not finish and not paused:  
                player.fire()
                fire_sound.play()
            if e.key == K_ESCAPE and not menu and not finish:
                paused = not paused

        if menu:
            if start_button.is_clicked(e):
                menu = False
            elif exit_button.is_clicked(e):
                run = False

        elif paused:
            if restart_button.is_clicked(e):
                restert_game()
                paused = False
            elif continue_button.is_clicked(e):
                paused = False


    if menu:
        window.blit(background, (0, 0))
        start_button.draw()
        exit_button.draw()

    elif paused:
        window.blit(background, (0, 0))
        restart_button.draw()
        continue_button.draw()

    elif not finish:
        window.blit(background, (0, 0))
 
        player.reset()
        monsters.draw(window)
        Bullets.draw(window)
        asteroids.draw(window)

        player.update()
        monsters.update()
        Bullets.update()
        asteroids.update()
        
        sprite.groupcollide(asteroids, Bullets, False, True)

        collided_monsters = sprite.spritecollide(player, monsters, True)
        collided_asteroids = sprite.spritecollide(player, asteroids, True)

        if collided_monsters or collided_asteroids:
            life -= 1
            monster = Enemy(img_ufo, randint(0, WIDTH - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
            asteroid = Asteroid(img_asteroid, randint(0, WIDTH - 80), -40, 80, 50, randint(1, 5))
            asteroids.add(asteroid)

        collides = sprite.groupcollide(monsters, Bullets, True, True)
        for collide in collides:
            score += 1
            monster = Enemy(img_ufo, randint(0, WIDTH - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(player, monsters, False):
            life -= 1
            print(life)

        if lost >= MAX_LOST or life <= 0:
            finish = True
            window.blit(lost_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
            mixer.music.stop()

        if score >= MAX_SCORE:
            finish = True
            window.blit(win_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
            mixer.music.stop()

        if life == 3:
            life_color = (0, 150, 0)
        elif life == 2:
            life_color = (150, 150, 0)
        else:
            life_color = (150, 0, 0)

        text_life = font_text.render('Жизни:'  + str(life),True, life_color )
        window.blit(text_life, (WIDTH // 2 + 220, 20))

        score_text = font_text.render('счет:' + str(score), True, WHITE)
        window.blit(score_text, (10, 20))

        lost_text = font_text.render('пропущено:' + str(lost), True, WHITE)
        window.blit(lost_text, (10, 50))

    display.update()
    clock.tick(FPS)