import pygame
import random
import os

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SpaceMax Defender")

# Cargar imágenes
current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')
img_path = os.path.join(assets_path, 'images')

# Jugador
player_img = pygame.image.load(os.path.join(img_path, 'player.png')).convert_alpha()
# Enemigos
enemy_imgs = [
    pygame.image.load(os.path.join(img_path, 'enemy1.png')).convert_alpha(),
    pygame.image.load(os.path.join(img_path, 'enemy2.png')).convert_alpha(),
    pygame.image.load(os.path.join(img_path, 'enemy3.png')).convert_alpha()
]
# Bala
bullet_img = pygame.image.load(os.path.join(img_path, 'bullet.png')).convert_alpha()
# Fondo
background = pygame.image.load(os.path.join(img_path, 'background.jpg')).convert()

# Sonidos
laser_sound = pygame.mixer.Sound(os.path.join(assets_path, 'sounds', 'laser.mp3'))
explosion_sound = pygame.mixer.Sound(os.path.join(assets_path, 'sounds', 'explosion.mp3'))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 8
        self.lives = 3
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.image = enemy_imgs[type]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.direction *= -1
            self.rect.y += 30

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

# Grupos de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Crear jugador
player = Player()
all_sprites.add(player)

# Crear enemigos
for row in range(3):
    for column in range(8):
        enemy = Enemy(100 + column * 70, 50 + row * 60, row)
        all_sprites.add(enemy)
        enemies.add(enemy)

# Bucle principal
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)
    
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top, -10)
                all_sprites.add(bullet)
                bullets.add(bullet)
                laser_sound.play()

    # Actualizar
    all_sprites.update()

    # Colisiones balas-enemigos
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        explosion_sound.play()
        player.score += 100

    # Colisiones jugador-enemigos
    if pygame.sprite.spritecollide(player, enemies, True):
        player.lives -= 1
        if player.lives <= 0:
            running = False

    # Dibujar
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    
    # Mostrar puntuación y vidas
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {player.score}  Lives: {player.lives}", True, (255, 255, 255))
    screen.blit(text, (10, 10))
    
    pygame.display.flip()

pygame.quit()