import pygame
import random
import pygame.font


pygame.init()

win_width = 500
win_height = 500

bg = pygame.image.load("sea.jpg")

bg = pygame.transform.scale(bg, (win_width, win_height))

clock = pygame.time.Clock()

window = pygame.display.set_mode((win_width, win_height))
window_rect = window.get_rect()

pygame.display.set_caption("Arcanoid")

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, new_image, x, y, width, height) -> None:
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(new_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed) -> None:
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill('black')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.width = width
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.x < win_width - self.width:
            self.rect.x += self.speed
    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def __init__(self, new_image, x, y, width, height) -> None:
        super().__init__(new_image, x, y, width, height)

class Ball(GameSprite):
    def __init__(self, new_image, x, y, width, height, speed) -> None:
        super().__init__(new_image, x, y, width, height)
        self.velocity = [speed, -speed]

    def update(self):
        # Проверяем столкновение мяча с платформой
        if self.rect.colliderect(platform.rect):
            # Определяем, где произошло столкновение
            relative_hit_position = self.rect.centerx - platform.rect.left
            # Нормализуем позицию относительно ширины платформы
            normalized_hit_position = relative_hit_position / platform.rect.width
            # Преобразуем в диапазон от 0 до 1
            normalized_hit_position = max(0, min(1, normalized_hit_position))
            # Вычисляем коэффициент, на который нужно изменить скорость мяча в зависимости от места удара
            inertia_factor = normalized_hit_position * 0.5 + 0.5  # от 0.5 до 1.0
            # Применяем инерцию к вертикальной скорости мяча
            self.velocity[1] = -self.velocity[1] * inertia_factor
        if pygame.sprite.spritecollideany(self, enemies, True):
            self.velocity[1] = not self.velocity[1]
        if self.rect.colliderect(window_rect.left) or self.rect.colliderect(window_rect.right):
            self.velocity[0] = not self.velocity[0]
        # Двигаем мяч
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

enemies = pygame.sprite.Group()

def spawn_enemy():
    index = 0
    y_cor = 0
    for _ in range(3):
        count_enemies = 9 - index
        x_cor = win_width / (count_enemies * 80)
        for _ in range(count_enemies):
            print(x_cor)
            enemies.add(Enemy('torpeda.png', x_cor, y_cor, 80, 80))
            x_cor += x_cor
        y_cor += 80
        index += 1



platform = Platform(win_width/2, win_height * 0.8, 100, 20, 8)

score = 0

finish = False

paused = True

game_over_text = ''

font = pygame.font.SysFont(None, 36)

exit = False
spawn_enemy()

while not exit:
    for event in pygame.event.get():   
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE and not finish:
                paused = not paused  # Toggle the paused state
            if event.key == pygame.K_r and finish:
                platform.rect.x = win_width/2
                platform.rect.y = win_height/2 + 30
                score = 0
                enemies_passed = 0
                enemies.empty()
                finish = False
    window.blit(bg, (0, 0))

    # if not enemies.sprites():

    if not finish and not paused:
        platform.update()

    # if score >= 10:
    #     game_over_text = font.render("Вітаю! Ти виграв вбивши 10 кораблів", True, (0, 255, 0))
    #     finish = True

    # if enemies_passed >= 5:
    #     game_over_text = font.render("Ти програв пропустивши 5 ворогів", True, (255, 0, 0))
    #     finish = True


    platform.show()
    enemies.draw(window)

    if finish:
        canavs_rect = window.get_rect()
        window.blit(game_over_text, (canavs_rect.centerx - 200, canavs_rect.centery))
    if paused:
        canavs_rect = window.get_rect()
        window.blit(font.render('Гру зупинено!', True, (255,255,255)), (canavs_rect.centerx - 100, canavs_rect.centery))
        window.blit(font.render('Натисніть ESC для продовження.', True, (255,255,255)), (canavs_rect.centerx - 200, canavs_rect.centery + 40))

    # window.blit(font.render(f"Вбито кораблів: {score}/10", True, (255, 255, 255)), (10, 10))
    # window.blit(font.render(f"Пропущено кораблів: {enemies_passed}/5", True, (255, 255, 255)), (10, 40))

    pygame.display.update()
    clock.tick(60)



