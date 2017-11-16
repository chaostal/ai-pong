import pygame

import time
import random

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)

fps = pygame.time.Clock()

class Window:

    def __init__(self, display_width=800*0.4, display_height=600*0.7):
        self.x = 800
        self.y = 600
        self.display_width = display_width
        self.display_height = display_height
        self.win = pygame.display.set_mode((800, 600))
        self.title = pygame.display.set_caption("pong")

    def show(self):
        self.win.fill(black)

    def surface(self):
        return self.win

    def net(self, w):
        pygame.draw.line(w, white, (407, 600), (407, 0), 1)

w = Window()

class Player:

    def __init__(self, x, keyUp, keyDown):
        self.x = x
        self.y = w.y / 2
        self.w = 25
        self.h = 150
        self.y_change = 0
        self.y_change2 = 0
        self.keyUp = keyUp
        self.keyDown = keyDown


    def draw_paddle(self, w):
        pygame.draw.rect(w, white, [self.x, self.y - self.h/2, self.w, self.h])

    def event_handling(self):

        if event.type == pygame.KEYDOWN:

            if event.key == self.keyUp:
                self.y_change = -5

            elif event.key == self.keyDown:
                self.y_change = 5

            '''if self.y >= 530 or self.y <= 70:
                self.y_change = 0
                self.event_handling()'''

        if event.type == pygame.KEYUP:
            self.y_change = 0

        self.y += self.y_change


p = Player(0, pygame.K_w, pygame.K_s)
p2 = Player(775, pygame.K_UP, pygame.K_DOWN)

class Ball:

    def __init__(self):
        self.x = w.x / 2
        self.y = w.y / 2
        self.w = 15
        self.h = 15
        self.velox = -6
        self.veloy = -1
        self.multi = 0.03

    def draw_ball(self, w):
        pygame.draw.rect(w, white, [self.x, self.y, self.w, self.h])

    def step(self):
        self.x += self.velox
        self.y += self.veloy

b = Ball()

def collision(r1, r2):
    if r2.x > r1.x and r2.x < r1.x + r1.w and r2.y > r1.y - r1.h/2 and r2.y < r1.y + r1.h/2:
        return True

def direction_change():
    if collision(p, b):
        b.velox = -b.velox - 1
        if b.velox != -b.velox:
            b.velox = b.velox + 1
        b.veloy = b.multi * (b.y - p.y)

    if collision(p2, b):
        b.velox = -b.velox - 1
        if b.velox != -b.velox:
            b.velox = b.velox + 1
        b.veloy = b.multi * (b.y - p2.y)

    if b.y < 0 or b.y > w.y:
        b.veloy = -b.veloy

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font("freesansbold.ttf",115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((w.x/2),(w.y/2))
    w.win.blit(TextSurf, TextRect)

    pygame.display.update()

def evaluation():
    if b.x < 0:
        message_display("Right wins")
    elif b.x > w.x:
        message_display("Left wins")

game_exit = False
while not game_exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    w.show()
    w.net(w.surface())

    evaluation()

    p.draw_paddle(w.surface())
    p2.draw_paddle(w.surface())
    p.event_handling()
    p2.event_handling()

    b.draw_ball(w.surface())
    b.step()

    direction_change()

    pygame.display.update()
    fps.tick(60)
