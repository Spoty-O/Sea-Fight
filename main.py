import pygame
import time
import random
import pygame.font


pygame.init()
pygame.mouse.set_visible(0)

win_width = 1000
win_height = 600

bg_sea = pygame.image.load("sea.jpg")

bg_binocle = pygame.image.load("binocle.png")

bg_sea = pygame.transform.scale(bg_sea, (win_width, win_height))

bg_binocle = pygame.transform.scale(bg_binocle, (win_width, win_height))

pygame.mixer.music.load('main_theme.mp3')
pygame.mixer.music.play()


clock = pygame.time.Clock()


# CREATING CANVAS
canvas = pygame.display.set_mode((win_width, win_height))

# TITLE OF CANVAS
pygame.display.set_caption("Sea shooter")

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, new_image, x, y, width, height) -> None:
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(new_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def show(self):
        canvas.blit(self.image, (self.rect.x, self.rect.y))

class Scope(GameSprite):
    def __init__(self, new_image, x, y, width, height, delay) -> None:
        super().__init__(new_image, x, y, width, height)
        self.shoot_time = time.time()
        self.delay = delay

    def update(self):
        coordinate_x = pygame.mouse.get_pos()[0]
        if coordinate_x <= win_width - 80 and coordinate_x >= 0:
            self.rect.x = coordinate_x
        mouse = pygame.mouse.get_pressed()[0]
        if mouse and (time.time() - self.shoot_time > self.delay):
            self.shoot_time = time.time()
            bullets.add(Bullet('torpeda.png', self.rect.centerx, self.rect.bottom, 15, 50, 5))

class Bullet(GameSprite):
    def __init__(self, new_image, x, y, width, height, speed) -> None:
        super().__init__(new_image, x, y, width, height)
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= win_height/2 + 50:
            self.kill()  # Remove the bullet when it goes off the screen

class Enemy(GameSprite):
    def __init__(self, x, y, width, height, speed) -> None:
        new_image = 'small_enemy_ship.png'
        if x == 10:
            self.speed = speed
            new_image = 'small_enemy_ship_reversed.png'
        else:
            self.speed = -speed
        super().__init__(new_image, x, y, width, height)

    def update(self):
        global enemies_passed
        self.rect.x += self.speed
        if self.rect.x >= win_width or self.rect.x <= 0:
            enemies_passed += 1
            self.kill()


def spawn_enemy():
    for _ in range(5):
        enemies.add(Enemy(random.choice([10, win_width - 10]), random.randint(int(win_height/2), win_height - 200), 80, 80, 2))

enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Scope('scope.png', win_width/2, win_height/2 + 30, 150, 170, 0.6)

previous_time = pygame.time.get_ticks()

score = 0

finish = False

paused = True

enemies_passed = 0  # Variable to keep track of enemies passing the last coordinate

game_over_text = ''

font = pygame.font.SysFont(None, 36)

exit = False

while not exit:
    for event in pygame.event.get():   
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE and not finish:
                paused = not paused  # Toggle the paused state
            if event.key == pygame.K_r and finish:
                player.rect.x = win_width/2
                player.rect.y = win_height/2 + 30
                score = 0
                enemies_passed = 0
                enemies.empty()
                bullets.empty()
                finish = False
    canvas.blit(bg_sea, (0, 0))

    if not enemies.sprites():
        spawn_enemy()

    if not finish and not paused:
        player.update()
        enemies.update()
        bullets.update()

    if pygame.sprite.groupcollide(bullets, enemies, True, True):
        score += 1

    if score >= 10:
        game_over_text = font.render("Вітаю! Ти виграв вбивши 10 кораблів", True, (0, 255, 0))
        finish = True

    if enemies_passed >= 5:
        game_over_text = font.render("Ти програв пропустивши 5 ворогів", True, (255, 0, 0))
        finish = True


    player.show()
    enemies.draw(canvas)
    bullets.draw(canvas)

    if finish:
        canavs_rect = canvas.get_rect()
        canvas.blit(game_over_text, (canavs_rect.centerx - 200, canavs_rect.centery))
    if paused:
        canavs_rect = canvas.get_rect()
        canvas.blit(font.render('Гру зупинено!', True, (255,255,255)), (canavs_rect.centerx - 100, canavs_rect.centery))
        canvas.blit(font.render('Натисніть ESC для продовження.', True, (255,255,255)), (canavs_rect.centerx - 200, canavs_rect.centery + 40))
    
    canvas.blit(bg_binocle, (0, 0))
    canvas.blit(font.render(f"Вбито кораблів: {score}/10", True, (255, 255, 255)), (10, 10))
    canvas.blit(font.render(f"Пропущено кораблів: {enemies_passed}/5", True, (255, 255, 255)), (10, 40))

    pygame.display.update()
    clock.tick(60)



