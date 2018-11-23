import pygame
import random
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
PLAYER_STEP = 10
BULLET_SPEED = 15
MAX_ASTEROID_SIZE = SCREEN_WIDTH // 5
MIN_ASTEROID_SIZE = SCREEN_WIDTH // 20
ASTEROID_SIZE_AVERAGE = (MAX_ASTEROID_SIZE + MIN_ASTEROID_SIZE)//2
BULLET_W = SCREEN_WIDTH // 23
BULLET_H = SCREEN_HEIGHT // 23
BULLET_IMAGES = []
ASTEROID_IMAGE = []
EXPLOSION = []
BULLETS_COUNT = 1
FPS = 30


class App:
    def __init__(self):
        self._running = True
        self.gameOver = True
        self.screen = None
        self.size = self.width, self.height = SCREEN_WIDTH, SCREEN_HEIGHT
        self.background = pygame.image.load("data\\space.png")
        self.background_rect = self.background.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = FPS
        self.playtime = 0.0
        self.player = Player()
        self.explosions = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.changeX = 0
        self.changeY = 0
        self.score = None
        self.upTo100 = False
        self.upTo300 = False
        self.upTo500 = False

    def on_init(self):
        pygame.init()
        self.load_images()
        self.add_asteroids()
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    def draw_text(self, text, x, y, size=20):
        font = pygame.font.SysFont('mono', size, True, False)
        surface = font.render(text, True, (255, 255, 255))
        self.screen.blit(surface, (x, y))

    def load_images(self):
        BULLET_IMAGES.append(pygame.transform.scale(pygame.image.load("data\\bulletU.png"), (BULLET_H, BULLET_W)))
        BULLET_IMAGES.append(pygame.transform.scale(pygame.image.load("data\\bulletR.png"), (BULLET_W, BULLET_H)))
        BULLET_IMAGES.append(pygame.transform.scale(pygame.image.load("data\\bulletD.png"), (BULLET_H, BULLET_W)))
        BULLET_IMAGES.append(pygame.transform.scale(pygame.image.load("data\\bulletL.png"), (BULLET_W, BULLET_H)))
        ASTEROID_IMAGE.append(pygame.image.load("data\\asteroid1.png"))
        EXPLOSION.append(pygame.image.load("data\\explosion0.png"))
        EXPLOSION.append(pygame.image.load("data\\explosion1.png"))
        EXPLOSION.append(pygame.image.load("data\\explosion2.png"))
        EXPLOSION.append(pygame.image.load("data\\explosion3.png"))

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.player.set_current_image(1)
                self.changeX = PLAYER_STEP
                self.changeY = 0
            if event.key == pygame.K_LEFT:
                self.player.set_current_image(3)
                self.changeX = -PLAYER_STEP
                self.changeY = 0
            if event.key == pygame.K_UP:
                self.player.set_current_image(0)
                self.changeY = -PLAYER_STEP
                self.changeX = 0
            if event.key == pygame.K_DOWN:
                self.player.set_current_image(2)
                self.changeY = PLAYER_STEP
                self.changeX = 0
            if event.key == pygame.K_SPACE:
                if len(self.player.bullets) < BULLETS_COUNT:
                    self.player.bullets.add(Bullet(self.player.currentDirection, self.player.rect.x, self.player.rect.y))

        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_UP) | (event.key == pygame.K_DOWN):
                self.changeY = 0
            if (event.key == pygame.K_LEFT) | (event.key == pygame.K_RIGHT):
                self.changeX = 0

    def on_loop(self, milliseconds):

        self.game_updates()

        for bullet in self.player.bullets:
            for asteroid in self.asteroids:
                if pygame.sprite.collide_mask(bullet, asteroid):
                    self.score += asteroid.value
                    self.explosions.add(Explosion(asteroid.rect.center, asteroid.rect.size))
                    asteroid.kill()
                    bullet.kill()
                    self.asteroids.add(Asteroid())

        if self.player.check_collision(self.asteroids):
            self.gameOver = True

        self.asteroids.update()
        self.asteroids.draw(self.screen)

        self.explosions.update()
        self.explosions.draw(self.screen)

        self.player.bullets.update()
        self.player.bullets.draw(self.screen)

        self.player.update(self.changeX, self.changeY)
        self.screen.blit(self.player.image, (self.player.rect.x, self.player.rect.y))

        self.playtime += milliseconds / 1000.0
        self.draw_text("  BULLETS: {}   SCORE: {}   PLAYTIME:{} SECONDS".format(
            BULLETS_COUNT, self.score, math.floor(self.playtime)), 0, 0)

        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))

    def add_asteroids(self, number=10):
        for x in range(number):
            self.asteroids.add(Asteroid())

    def new_game(self):
        self.score = 0
        self.asteroids.empty()
        self.add_asteroids()
        self.player.reset()
        self.delete_upgrades()
        self.changeY = 0
        self.changeX = 0

    def delete_upgrades(self):
        self.upTo100 = False
        self.upTo300 = False
        self.upTo500 = False

    def on_game_over(self):
        self.show_menu()
        self.new_game()
        self.gameOver = False

    def show_menu(self):
        self.screen.blit(self.background, self.background_rect)

        self.draw_text("SPACE ADVENTURE", SCREEN_WIDTH / 7, SCREEN_HEIGHT / 6, 64)

        if self.score != None:
            self.draw_text("GAME OVER", SCREEN_WIDTH / 7, SCREEN_HEIGHT * 3/6, 40)
            self.draw_text("Your score: {}".format(self.score), SCREEN_WIDTH / 7, SCREEN_HEIGHT * 3.5/6)

        self.draw_text("Arrow keys move, Space to fire", SCREEN_WIDTH / 7, SCREEN_HEIGHT * 4/6)
        self.draw_text("Press ENTER to start the game", SCREEN_WIDTH / 7, SCREEN_HEIGHT * 4.25/6)
        pygame.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                     waiting = False

    def game_updates(self):
        global BULLETS_COUNT

        if self.score > 100:
            if self.upTo100 != True:
                BULLETS_COUNT = 2
                self.upTo100 = True

        if self.score > 300:
            if self.upTo300 != True:
                BULLETS_COUNT = 3
                self.add_asteroids(5)
                self.upTo300 = True

        if self.score > 500:
            if self.upTo500 != True:
                self.add_asteroids(5)
                self.upTo500 = True


    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):

            if self.gameOver:
                self.on_game_over()

            for event in pygame.event.get():
                self.on_event(event)

            milliseconds = self.clock.tick(self.fps)
            self.on_loop(milliseconds)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.playerW = SCREEN_WIDTH//10
        self.playerH = SCREEN_HEIGHT//10
        self.currentDirection = 0
        self.bullets = pygame.sprite.Group()
        self.playerImages = []
        self.load_images()
        self.image = None
        self.rect = None
        self.reset()

    def reset(self):
        global BULLETS_COUNT
        BULLETS_COUNT = 1
        self.bullets.empty()
        self.set_current_image(0)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH / 2
        self.rect.y = SCREEN_HEIGHT / 2

    def check_collision(self, asteroids):
        for asteroid in asteroids:
            collision = pygame.sprite.collide_mask(self, asteroid)
            if collision != None:
                return collision
        return None

    def load_images(self):
        self.playerImages.append(pygame.transform.scale(pygame.image.load("data\spacecraftU.png"), (self.playerH, self.playerW)))
        self.playerImages.append(pygame.transform.scale(pygame.image.load("data\spacecraftR.png"), (self.playerW, self.playerH)))
        self.playerImages.append(pygame.transform.scale(pygame.image.load("data\spacecraftD.png"), (self.playerH, self.playerW)))
        self.playerImages.append(pygame.transform.scale(pygame.image.load("data\spacecraftL.png"), (self.playerW, self.playerH)))

    def set_current_image(self, direction):
        self.currentDirection = direction
        self.image = self.playerImages[direction]

    def update(self, x, y):
        newX = self.rect.x + x
        newY = self.rect.y + y
        if (newX > 0) & (newX < SCREEN_WIDTH - self.playerW):
            self.rect.x = newX
        if (newY > 0) & (newY < SCREEN_HEIGHT - self.playerH):
            self.rect.y = newY

class Bullet(pygame.sprite.Sprite):
    def __init__(self, direction, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.firedDirection = direction
        self.image = BULLET_IMAGES[self.firedDirection]
        self.rect = self.image.get_rect()
        self.rect.x = x + BULLET_W / 2
        self.rect.y = y + BULLET_H / 2
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.firedDirection == 0:
            self.rect.y -= BULLET_SPEED
        if self.firedDirection == 1:
            self.rect.x += BULLET_SPEED
        if self.firedDirection == 2:
            self.rect.y += BULLET_SPEED
        if self.firedDirection == 3:
            self.rect.x -= BULLET_SPEED

        if (self.rect.x < -BULLET_W) | (self.rect.x > SCREEN_WIDTH + BULLET_W) \
                | (self.rect.y < -BULLET_H) | (self.rect.y > SCREEN_HEIGHT + BULLET_H):
            self.kill()


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ASTEROID_IMAGE[0]
        self.rect = self.image.get_rect()
        self.set_asteroid_image()
        self.speed = (0, 0)
        self.mask = None
        self.value = 0
        self.set_values()
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def is_collided_with(self, bullet):
        return self.rect.colliderect(bullet)

    def set_asteroid_image(self):
        self.image = (pygame.transform.scale(ASTEROID_IMAGE[0], (self.rect.width, self.rect.height)))

    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        if self.rect.top > SCREEN_HEIGHT + self.rect.height:
            self.set_values()

    def set_values(self):
        size = random.randrange(MIN_ASTEROID_SIZE, MAX_ASTEROID_SIZE)
        self.rect.width = size
        self.rect.height = size
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed = (random.randrange(-3, 3), random.randrange(1, 8))
        self.set_asteroid_image()
        self.mask = pygame.mask.from_surface(self.image)
        self.compute_asteroid_value(size)

    def compute_asteroid_value(self, size):
        self.value = self.speed[1] \
                     + (ASTEROID_SIZE_AVERAGE
                        - (size % ASTEROID_SIZE_AVERAGE)) // 12

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = None
        self.size =  size
        self.center = center
        self.frame = 0

    def update(self):
        if self.frame < len(EXPLOSION):
            self.image = pygame.transform.scale(EXPLOSION[self.frame], self.size)
            self.rect = self.image.get_rect()
            self.rect.center = self.center
            self.frame += 1
        else:
            self.kill()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()

