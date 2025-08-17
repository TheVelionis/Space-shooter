import pygame
import random
import time

temps_passé = 1716816325
temps_actuel = time.ctime(temps_passé)

pygame.init()
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption('Space Shooter')

icone = pygame.image.load('assets/ship.png').convert_alpha()
pygame.display.set_icon(icone)

launch = True

enemy_timer = 0
enemy_spawn_delay = 200

font = pygame.font.SysFont('Arial', 20)
score = 0

score_texte = font.render('Score: ' + str(score), True, (255, 255, 255))

background = pygame.image.load('assets/background.png')
background = pygame.transform.scale(background, (600, 600))

class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/ship.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.centerx = 400 // 2         # centre horizontal
        self.rect.bottom = 600 - 10
        self.speed = 1

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def shoot(self, missiles_group):
        missile = Missile(self.rect.centerx, self.rect.top)
        missiles_group.add(missile)

class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction = -1):
        super().__init__()
        self.image = pygame.image.load('assets/missile.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (24, 24))
        self.speed = 3 * direction
        self.rect = self.image.get_rect(center = (x, y))

    def update(self):
        self.rect.y += self.speed
        if self.rect.top >= 600:
            self.kill()

class Ennemi(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.image.load('assets/ennemi.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 400 - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(1, 2)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:  # hors écran
            self.kill()


ship = Ship(100, 100)
missiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()

while launch:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            launch = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ship.shoot(missiles)

    screen.blit(background, (0, 0))

    enemy_timer += 1
    if enemy_timer >= enemy_spawn_delay:
        enemy = Ennemi(screen.get_width())
        enemies.add(enemy)
        enemy_timer = 0

    keys = pygame.key.get_pressed()
    ship.update(keys)
    missiles.update()

    enemies.update()  # bouger les ennemis
    enemies.draw(screen)

    for missile in missiles:
        hit_enemies = pygame.sprite.spritecollide(missile, enemies, True)
        if hit_enemies:
            missile.kill()
            score += 1

    for enemy in enemies:
        hit_player = pygame.sprite.spritecollide(ship, enemies, False)
        if hit_player:
            ship.kill()
            launch = False

    screen.blit(ship.image, ship.rect)
    missiles.draw(screen)

    score_text = font.render(f"Score : {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))


    pygame.display.flip()

with open('logs.txt', 'a') as log:
    log.write(f'\n {temps_actuel} : {score}')
pygame.quit()