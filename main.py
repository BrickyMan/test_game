import pygame
import random

# Константы
WIDTH = 1000
HEIGHT = 600
TICKRATE = 60
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Инициализация библиотеки
pygame.init()

# Создание окна
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Star Wars')

# Игровые часы
clock = pygame.time.Clock()

# Базовый класс спрайта
class Sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, speed, image, cd):
        super().__init__()
        # Загрузка изображения
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (w, h))
        # Хитбокс
        self.rect = self.image.get_rect(center = (x, y))
        # Скорость
        self.speed = speed
        # КД на стрельбу
        self.cd = cd
        self.base_cd = cd

    # Отрисовка спрайта
    def draw(self):
        window.blit(self.image, self.rect.topleft)

class Player(Sprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.centerx -= self.speed
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.centerx += self.speed
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.centery -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < HEIGHT:
            self.rect.centery += self.speed
        if self.cd > 0:
            self.cd -= 1
        if keys[pygame.K_SPACE] and game.state == 'play':
            if self.cd == 0:
                self.cd = self.base_cd
                laser_sound.play()
                lasers.add(Laser(self.rect.centerx, self.rect.top, -10))

class Enemy(Sprite):
    def update(self):
        # Движение вниз
        self.rect.centery += self.speed
        # Проверка выхода из кона
        if self.rect.top > HEIGHT:
            self.kill()

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((3, 15))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center = (x, y))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT or self.rect.bottom < 0:
            self.kill()

    def draw(self):
        window.blit(self.image, self.rect.topleft)

# Игра
class GameManager():
    def __init__(self):
        self.state = 'play'
        self.score = 0
        self.score_font = pygame.font.SysFont('consolas', 30)
        self.score_text = self.score_font.render('0', True, WHITE)

    def show_score(self):
        window.blit(self.score_text, (10, 10))

    def update_score(self):
        self.score += 1
        self.score_text = self.score_font.render(str(self.score), True, WHITE)

    def restart(self):
        self.state = 'play'
        self.score = 0
        self.score_text = self.score_font.render('0', True, WHITE)
        player.rect.center = (WIDTH // 2, HEIGHT - 100)
        for e in enemies:
            e.kill()

    def update(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE and self.state == 'game_over':
                    self.restart()

game = GameManager()

# Спрайты
player = Player(WIDTH // 2, HEIGHT - 100, 100, 100, 5, 'battleship.png', TICKRATE // 3)

# Группа противников
enemies = pygame.sprite.Group()
enemy_spawn_cd = TICKRATE

# Группа лазеров
lasers = pygame.sprite.Group()

# Загрузка звуков
laser_sound = pygame.mixer.Sound('laser.mp3')
laser_sound.set_volume(0.2)

# Фон
bg = pygame.image.load('background.jpg')
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# Шрифт
my_font = pygame.font.SysFont('Arial', 70)
game_over_text = my_font.render('Game over!', True, WHITE)
my_font = pygame.font.SysFont('Arial', 45)
restart_text = my_font.render('Press SPACE to restart', True, WHITE)

# Переменная управляющая игровым циклом
run = True

# Игровой цикл
while run:
    events = pygame.event.get()
    # Перебор событий
    for e in events:
        if e.type == pygame.QUIT:
            run = False
    
    game.update(events)

    if game.state == 'play':
        # Отрисовка фона
        window.blit(bg, (0, 0))

        # Спаун противников
        if enemy_spawn_cd == 0:
            enemy_spawn_cd = TICKRATE
            enemies.add(Enemy(random.randint(100, WIDTH - 100), -100, 100, 100, 3, 'aircraft.png', TICKRATE // 2))
        else:
            enemy_spawn_cd -= 1

        # Обновление спрайтов
        player.update()
        enemies.update()
        lasers.update()

        # Отрисовка спрайтов
        player.draw()
        enemies.draw(window)
        lasers.draw(window)
        game.show_score()

        # Коллизия игрока и противников
        if pygame.sprite.spritecollideany(player, enemies):
            game.state = 'game_over'

        # Коллизия противников и лазеров
        shots = pygame.sprite.groupcollide(lasers, enemies, True, True)

        if len(shots) > 0:
            game.update_score()

    if game.state == 'game_over':
        # Отрисовка фона
        window.blit(bg, (0, 0))
        # Отрисовка надписей
        window.blit(game_over_text, ((WIDTH // 4) + 50, (HEIGHT // 2) - 50))
        window.blit(restart_text, (WIDTH // 4, (HEIGHT // 2) + 50))

    # Обновление игры
    pygame.display.flip()
    # Тикрейт
    clock.tick(TICKRATE)