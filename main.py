import math

import pygame

import os
pygame.init()

all_sprites = pygame.sprite.Group()
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("brick breaker")
FPS = 60
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
BALL_RADIUS = 10
LIVES_FONT = pygame.font.SysFont("comicsans", 40)

class Paddle:
    VEL = 5

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def move(self, direction=1):
        self.x = self.x + self.VEL * direction


class Ball:
    VEL = 6

    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.x_vel = 1
        self.y_vel = -self.VEL
        # self.stop = True

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def set_vel(self, x_vel, y_vel):
        self.x_vel = x_vel
        self.y_vel = y_vel

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.width = self.rect[2]
        self.height = self.rect[3]
        self.health = health
        self.max_health = health
        # self.image = pygame.Surface((widht, height))
        # self.image.fill("green")
        self.rect.center = (x + self.width/2, y + self.height/2)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

        all_sprites.update()
        all_sprites.draw(win)

    def collide(self, ball):
        # удар справа
        if (ball.x + ball.radius >= self.rect.x) and (ball.x + ball.radius < self.rect.x + self.width) and (
                self.rect.y < ball.y < self.rect.y + self.height):
            print(" удар справа")
            self.hit()
            ball.set_vel(ball.x_vel * -1, ball.y_vel)
            return True
        if (ball.x - ball.radius <= self.rect.x + self.width) and (ball.x - ball.radius > self.rect.x) and (
                self.rect.y < ball.y < self.rect.y + self.height):
            print(" удар слева")
            self.hit()
            ball.set_vel(ball.x_vel * -1, ball.y_vel)
            return True
        if (ball.y + ball.radius >= self.rect.y) and (ball.y + ball.radius < self.rect.y + self.height) and (
                self.rect.x < ball.x < self.rect.x + self.width):
            print(" удар сверху")
            self.hit()
            ball.set_vel(ball.x_vel, ball.y_vel * -1)
            return True
        if (ball.y - ball.radius <= self.rect.y + self.height) and (ball.y - ball.radius > self.rect.y) and (
                self.rect.x < ball.x < self.rect.x + self.width):
            print(" удар снизу")
            self.hit()
            ball.set_vel(ball.x_vel, ball.y_vel * -1)
            return True

        return False

    def hit(self):
        self.health -= 1
        self.color = self.interpolate(
            *self.colors, self.health / self.max_health)


    @staticmethod
    def interpolate(color_a, color_b, t):
        # "color_a" and "color_b" are RGB tuples
        # "t" is a value betweem 0.0 and 1.0
        # this is a naive interpolation
        return tuple(int(a + (b - a) * t) for a, b in zip(color_a, color_b))

def draw(win, paddle, ball, bricks, lives):
    win.fill("white")
    paddle.draw(win)
    ball.draw(win)


    lives_text = LIVES_FONT.render(f"Lives: {lives}", 1, "black")
    win.blit(lives_text, (10, HEIGHT - lives_text.get_height() - 10))
    pygame.display.update()


def ball_collision(ball):
    # print("Сработал")
    if ball.x - BALL_RADIUS <= 0 or ball.x + BALL_RADIUS >= WIDTH:
        ball.set_vel(ball.x_vel * -1, ball.y_vel)


    if ball.y + BALL_RADIUS >= HEIGHT or ball.y - BALL_RADIUS <= 0:
        ball.set_vel(ball.x_vel, ball.y_vel * -1)


def ball_paddle_collision(ball, paddle):

    # если шарик вне положения площадки по X, то нечего не делай
    if not (ball.x <= paddle.x + paddle.width and ball.x >= paddle.x):
        return

    # если шарик вне положения площадки по Y, то нечего не делай
    if not (ball.y + ball.radius >= paddle.y):
        return

    paddle_center = paddle.x + paddle.width / 2
    distance_to_center = ball.x - paddle_center

    percent_width = distance_to_center / paddle.width
    angle = percent_width * 90
    angle_radians = math.radians(angle)
    x_vel = math.sin(angle_radians) * ball.VEL
    y_vel = math.cos(angle_radians) * ball.VEL * -1
    ball.set_vel(x_vel, y_vel)


def generate_bricks(width, height):
    # gap = 30
    # brick_width = WIDTH // cols - gap
    # brick_height = 30
    x = 0
    y = 0
    H = 0
    windowSize = pygame.display.get_window_size()
    cols = windowSize[0] // width
    gap = (windowSize[0] % width) // cols
    rows = 4

    bricks = []
    for row in range(rows):
        for col in range(cols):
            brick = Brick(x, y, 2)
            all_sprites.add(brick)
            x = col*(brick.width + gap)
            y = H +row * (brick.height + gap)
            print(x, y)

    brick = Brick(x, y, 2)
    all_sprites.add(brick)

    return all_sprites


# настройка папки ассетов

game_folder = os.path.dirname(__file__)

img_folder = os.path.join(game_folder, 'img')

player_img = pygame.image.load(os.path.join(img_folder, 'p1_jump.png'))

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("brick breaker")

FPS = 165
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
BALL_RADIUS = 10

LIVES_FONT = pygame.font.SysFont("comicsans", 40)


all_sprites = pygame.sprite.Group()




def main():
    clock = pygame.time.Clock()

    paddle_x = WIDTH / 2 - PADDLE_WIDTH / 2
    paddle_y = HEIGHT - PADDLE_HEIGHT - 5

    paddle = Paddle(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT, "black")
    ball = Ball(WIDTH / 2, paddle_y - BALL_RADIUS, BALL_RADIUS, "black")
    bricks = generate_bricks(91, 26)

    lives = 3

    def reset():
        paddle.x = paddle_x
        paddle.y = paddle_y
        ball.x = WIDTH / 2
        ball.y = paddle_y - BALL_RADIUS

    def display_text(text):
        text_render = LIVES_FONT.render(text, 1, "red")
        win.blit(text_render, (WIDTH / 2 - text_render.get_width() / 2, HEIGHT / 2 - text_render.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(3000)



    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and paddle.x - paddle.VEL >= 0:
            paddle.move(-1)
        if keys[pygame.K_RIGHT] and paddle.x + paddle.VEL + paddle.width <= WIDTH:
            paddle.move(1)

        ball.move()
        ball_collision(ball)
        ball_paddle_collision(ball, paddle)

        for brick in all_sprites:
            brick.collide(ball)

            if brick.health <= 0:
                all_sprites.remove(brick)
                brick.update()

        if ball.y + ball.radius >= HEIGHT:
            lives -= 1
            ball.x = paddle_x + paddle.width / 2
            ball.y = paddle_y
            ball.set_vel(0, ball.VEL * -1)
            paddle.x = WIDTH / 2 - paddle.width / 2

        if lives <= 0:
            bricks = generate_bricks(3, 3)
            lives = 3
            reset()
            display_text("You Lost!")

        if len(bricks) == 0:
            bricks = generate_bricks(3, 3)
            lives = 3
            reset()
            display_text("You Won!")

        draw(win, paddle, ball, all_sprites, bricks, lives)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
# if __name__ == '__main__':
#     print_hi('PyCharm')
