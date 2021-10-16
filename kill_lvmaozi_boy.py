from pygame.time import Clock
import pygame, random
from pygame.sprite import Sprite, Group
import easygui

FloralWhite = (255, 250, 240)
GREEN = (0, 250, 0)
Peru = (205, 133, 63)
Red = (255, 0, 0)
WIDTH = 800
HEIGHT = 1000
FPS = 20

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('消灭绿帽子')
clock = Clock()

all_sprites = Group()
stone_sprites = Group()
player_sprites = Group()

running = True
bullet_sprites = False
# 被消灭绿帽子个数
lvmaozi_killed_count = 0
# 被带绿帽子个数
lvmaozi_faild_count = 0
# 绿帽子个数
lvmaozi_count = 20
# 生命数量
lives_count = 5
fileName = easygui.fileopenbox(msg='将出现在屏幕下方，可直接关闭。', title='请选择游戏者头像')

music_all = pygame.mixer.Sound('fenshoukuaile.wav')
qusiba = pygame.mixer.Sound('qusiba_boy.wav')
# 字幕打印
def text_update(screen, lvmaozi_killed_count):
    pygame.font.init()
    if lvmaozi_killed_count + lvmaozi_faild_count == lvmaozi_count:
        font = pygame.font.SysFont('华文楷体', 40)
        text = font.render('恭喜你！成功消灭了所有绿帽子。', True, Red)
        TextRect = text.get_rect()
        TextRect.center = ((WIDTH /2 ), (HEIGHT / 2))
        screen.blit(text, TextRect)
    elif lives_count <= 0:
        font = pygame.font.SysFont('华文楷体', 40)
        text = font.render('还是被带了绿帽子！你消灭了%s个绿帽子。' %(lvmaozi_killed_count), True, Red)
        TextRect = text.get_rect()
        TextRect.center = ((WIDTH /2 ), (HEIGHT / 2))
        screen.blit(text, TextRect)

    font = pygame.font.SysFont('华文楷体', 25)
    text = font.render('剩余生命：' + str(lives_count), True, Red)
    screen.blit(text, (0, 0))

    font = pygame.font.SysFont('华文楷体', 25)
    text = font.render('消灭绿帽子：' + str(lvmaozi_killed_count), True, Red)
    screen.blit(text, (WIDTH - 200, 0))

    pygame.display.update()

# 下方 单身狗属性
class Player(Sprite):
    def __init__(self, WIDTH, HEIGHT):
        super(Player, self).__init__()
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        # self.image = pygame.Surface((50, 40))
        # self.image.fill(GREEN)
        if fileName:
            self.image = pygame.image.load(fileName)
        else:
            self.image = pygame.image.load(r'danshengou.png')
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        # self.rect.x = 0
        # self.rect.y = HEIGHT / 2
        self.speed_x = 8
        self.speed_y = 8

    def update(self, *args, **kwargs):
        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed_x
        elif key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed_x
        elif key_pressed[pygame.K_UP]:
            self.rect.y -= self.speed_y
        elif key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed_y

        if self.rect.left >= self.WIDTH - 50:
            self.rect.right = self.WIDTH
        elif self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.top >= self.HEIGHT - 40:
            self.rect.top = self.HEIGHT - 40
        elif self.rect.top <= 0:
            self.rect.top = 0

    def shoot(self, all_sprites, bullet_sprites):
        if lives_count > 0:
            bullet = Bullet(self.rect.x, self.rect.y)
            all_sprites.add(bullet)
            bullet_sprites.add(bullet)
            return bullet_sprites

    def move(self, x):
        self.rect.x = x

# 绿帽子属性
class Stone(Sprite):
    def __init__(self, WIDTH, HEIGHT):
        super(Stone, self).__init__()
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        # self.image = pygame.Surface((20, 20))
        self.image = pygame.image.load(r'lvmaozi.png')
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = 0
        # self.rect.x = 0
        # self.rect.y = HEIGHT / 2
        self.speed_x = random.randrange(-3, 3)
        self.speed_y = random.randrange(15, 25)

    def update(self, *args, **kwargs):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if self.rect.y >= self.HEIGHT - self.rect.height or self.rect.x >= self.WIDTH or self.rect.x <= 0:
            self.rect.x = random.randrange(0, self.WIDTH - self.rect.width)
            self.rect.y = 0
            self.speed_x = random.randrange(-3, 3)
            self.speed_y = random.randrange(6, 10)

# 子弹属性
class Bullet(Sprite):
    def __init__(self, x, y):
        super(Bullet, self).__init__()
        self.x = x
        self.y = y
        # self.image = pygame.Surface((15, 15))
        # self.image.fill(Red)
        self.image = pygame.image.load(r'yanlei.png')
        self.image = pygame.transform.scale(self.image, (15, 40))
        self.rect = self.image.get_rect()
        self.rect.centerx = x + 25
        self.rect.bottom = y
        self.speed_y = -50

    def update(self, *args, **kwargs):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

player = Player(WIDTH, HEIGHT)
all_sprites.add(player)
player_sprites.add(player)

for i in range(lvmaozi_count):
    stone = Stone(WIDTH, HEIGHT)
    all_sprites.add(stone)
    stone_sprites.add(stone)

bullet_sprites = Group()
music_all.set_volume(40)
music_all.play(-1)
while running:
    text_update(screen, lvmaozi_killed_count)
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            bullet_sprites = player.shoot(all_sprites, bullet_sprites)
        elif event.type == pygame.MOUSEMOTION:
            x = event.pos[0] - 25
            player.move(x)

    all_sprites.update()
    if bullet_sprites:
        hits = pygame.sprite.groupcollide(stone_sprites, bullet_sprites, True, True)
        for hit in hits:
            qusiba.set_volume(0.1)
            qusiba.play()
        #     stone = Stone(WIDTH, HEIGHT)
        #     all_sprites.add(stone)
        #     stone_sprites.add(stone)
            lvmaozi_killed_count += 1

    hits_stone = pygame.sprite.groupcollide(player_sprites, stone_sprites, True, True)
    for hit_stone in hits_stone:
        lives_count -= 1
        if lives_count > 0:
            player = Player(WIDTH, HEIGHT)
            all_sprites.add(player)
            player_sprites.add(player)
            lvmaozi_faild_count += 1
            # stone = Stone(WIDTH, HEIGHT)
            # all_sprites.add(stone)
            # stone_sprites.add(stone)

    screen.fill(FloralWhite)
    all_sprites.draw(screen)
    pygame.display.update()