import pygame
import nn
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

    def __init__(self, x):
        self.x = x
        self.y = w.y / 2
        self.w = 25
        self.h = 150
        self.y_change = 0

    def draw_paddle(self, w):
        pygame.draw.rect(w, white, [self.x, self.y - self.h/2, self.w, self.h])

    def tick(self):
        self.event_handling()
        self.y += self.y_change
        if self.y<self.h/2:
            self.y=self.h/2
        if self.y+self.h/2>w.display_height:
            self.y=w.display_height-self.h/2

    def welldone(self):
        pass
    def lost(self):
        pass


class Human(Player):
    def __init__(self, x, keyUp, keyDown):
        Player.__init__(self, x)
        self.keyUp = keyUp
        self.keyDown = keyDown

    def event_handling(self):

        if event.type == pygame.KEYDOWN:

            if event.key == self.keyUp:
                self.y_change = -5

            elif event.key == self.keyDown:
                self.y_change = 5

            if self.y >= 530 or self.y <= 70:
                self.y_change = 0
                self.event_handling()

        if event.type == pygame.KEYUP:
            self.y_change = 0



class SimplePC(Player):
    def __init__(self, x, ball):
        Player.__init__(self, x)
        self.count = 10
        self.y_change = 5
        self.ball = ball

    def event_handling(self):
        self.count-=1
        if self.count == 0:
            self.y_change *= -1
            self.count = 20

class SimplePC2(Player):
    def __init__(self, x, ball):
        Player.__init__(self, x)
        self.y_change = 0
        self.ball = ball

    def event_handling(self):
        if self.ball.y > self.y:
            self.y_change = 5
        if self.ball.y < self.y:
            self.y_change = -5


class neuralPlayer(Player):
    def __init__(self, x, ball):
        Player.__init__(self, x)
        self.y_change = 5
        self.ball = ball
        input_nodes = 3
        hidden_nodes = 5
        output_nodes = 3

        learning_rate = 0.3

        self.neural = nn.neuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

        self.data = []

        for a in range(0,100):
            self.neural.train([1,30,100],[1,0,0])
            self.neural.train([1,30,400],[1,0,0])
            self.neural.train([1,130,30],[0,0,1])
            self.neural.train([1,50,50],[0,1,0])
            self.neural.train([1,430,30],[0,0,1])

    def welldone(self):
        for a in self.data:
            print(a)
            self.neural.train(a[0],a[1])
        self.data = []

    def lost(self):
        for a in self.data:
            print(a)
            self.neural.train(a[0],[-a[1][0],-a[1][1],-a[1][2]])
        self.data = []

    def event_handling(self):

        i = [self.ball.x, self.ball.y, self.y]
        r = self.neural.query([self.ball.x, self.ball.y, self.y])

        if r[0] > r[1] and r[0] > r[2]:
            self.y_change = -5
        elif r[1] > r[0] and r[1] > r[2]:
            self.y_change = 0
        else:
            self.y_change = 5

        self.data.append([i,[r[0][0],r[1][0],r[2][0]]])


class Ball:

    def __init__(self):
        self.reset()

    def reset(self):
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
p = Human(0, pygame.K_w, pygame.K_s)
# p = SimplePC2(0, b)
p = neuralPlayer(0, b)
p2 = SimplePC2(775, b)

def collision(r1, r2):
    if r2.x > r1.x and r2.x < r1.x + r1.w and r2.y > r1.y - r1.h/2 and r2.y < r1.y + r1.h/2:
        return True

def direction_change():
    if collision(p, b):
        b.velox = -b.velox - 1
        if b.velox != -b.velox:
            b.velox = b.velox + 1
        b.veloy = b.multi * (b.y - p.y)
        p.welldone()

    if collision(p2, b):
        b.velox = -b.velox - 1
        if b.velox != -b.velox:
            b.velox = b.velox + 1
        b.veloy = b.multi * (b.y - p2.y)
        p2.welldone()

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
        #message_display("Right wins")
        p.lost()
        b.reset()

    elif b.x > w.x:
        #message_display("Left wins")
        p2.lost()
        b.reset()

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
    p.tick()
    p2.tick()

    b.draw_ball(w.surface())
    b.step()

    direction_change()

    pygame.display.update()
    fps.tick(60)
