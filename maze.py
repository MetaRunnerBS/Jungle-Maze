from pygame import *
font.init()
window = display.set_mode((800, 600))
display.set_caption("Jungle Maze")
BG = transform.scale(image.load("background.jpg"), (800, 600))
win_txt = font.SysFont("Comic Sans MS", 60,).render("YOU WIN", True, (0, 255, 70))
lose_txt = font.SysFont("Comic Sans MS", 60,).render("YOU LOSE", True, (220, 40, 20))
mixer.init()
win_sound = mixer.Sound("money.ogg")
lose_sound = mixer.Sound("kick.ogg")
mixer.music.load('jungles.ogg')
mixer.music.play()
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (80, 80))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.bottom < 600:
            self.rect.y += self.speed
        if keys[K_d] and self.rect.right < 800:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if sprite.spritecollide(self, walls, False):
            self.rect.x = 30
            self.rect.y = 500
class Enemy(GameSprite):
    direction = "left"
    def update(self):
        if self.rect.x < 500:
            self.direction = "right"
        elif self.rect.x > 700:
            self.direction = "left"
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Wall(sprite.Sprite):
    def __init__(self, x, y, w, h, color=(199, 200, 0)):
        super().__init__()
        self.image = Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
walls = sprite.Group()
walls.add(Wall(0, 430, 200, 15))
walls.add(Wall(100, 300, 300, 15))
walls.add(Wall(385, 300, 15, 300))
walls.add(Wall(100, 100, 10, 200))
walls.add(Wall(100, 100, 180, 10))
walls.add(Wall(385, 0, 15, 200))
walls.add(Wall(200, 200, 200, 5))
walls.add(Wall(490, 0, 15, 500))
walls.add(Wall(600, 385, 15, 220))
walls.add(Wall(600, 140, 15, 150))

player = Player("hero.png", 30, 500, 5)
cyborg = Enemy("cyborg.png", 700, 300, 3)
final = GameSprite("treasure.png", 670, 470, 0)
clock = time.Clock()
run = True
finish = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    if not finish:
        window.blit(BG, (0, 0))
        player.reset()
        player.update()
        final.update()
        final.reset()
        walls.draw(window)
        cyborg.reset()
        cyborg.update()
        if sprite.collide_rect(player, final):
            window.blit(win_txt, (250, 250))
            win_sound.play()
            finish = True
            mixer.music.stop()
    display.update()
    clock.tick(60)