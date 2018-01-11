import pygame
import nn
import time
import random

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)

SPEED = 10
BALL_SPEED = 6

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
        self.initX = x
        self.y = w.y / 2
        self.w = 25
        self.h = 150
        self.y_change = 0

    def reset(self):
        self.x = self.initX
        self.y = w.y / 2

    def draw_paddle(self, w):
        pygame.draw.rect(w, white, [self.x, self.y - self.h/2, self.w, self.h])

    def tick(self):
        self.event_handling()
        self.y += self.y_change
        if self.y<self.h/2:
            self.y=self.h/2
        if (self.y+self.h/2)>w.y:
            self.y=w.y-self.h/2

    def welldone(self):
        pass
    def lost(self,dir,value):
        pass


class Human(Player):
    def __init__(self, x, keyUp, keyDown):
        Player.__init__(self, x)
        self.keyUp = keyUp
        self.keyDown = keyDown

    def event_handling(self):

        if event.type == pygame.KEYDOWN:

            if event.key == self.keyUp:
                self.y_change = -SPEED

            elif event.key == self.keyDown:
                self.y_change = SPEED

            if self.y >= 530 or self.y <= 70:
                self.y_change = 0
                self.event_handling()

        if event.type == pygame.KEYUP:
            self.y_change = 0



class SimplePC(Player):
    def __init__(self, x, ball):
        Player.__init__(self, x)
        self.count = 10
        self.y_change = SPEED
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
            self.y_change = SPEED
        if self.ball.y < self.y:
            self.y_change = -SPEED


class NeuralPlayer(Player):
    def __init__(self, x, ball):
        Player.__init__(self, x)
        self.y_change = SPEED
        self.ball = ball
        input_nodes = 5
        hidden_nodes = 5
        output_nodes = 3

        learning_rate = 0.3

        self.neural = nn.neuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

        self.data = []

    def welldone(self):
        for a in self.data[-30:]:
            self.neural.train(a[0],a[1])
        for a in self.data[-2:]:
            self.neural.train(a[0],[0,1,0])
        for a in self.data[:4]:
            self.neural.train(a[0],[0,0.3,0])
        self.data = []

    def lost(self,dir):
        print("VAL")
        #print(value)
        for a in self.data[:2]:
            self.neural.train(a[0],[0,0.3,0])
        for a in self.data[-10:]:
            x = a[0]
            y = [
                value if dir<0 else 0,
                value if dir==0 else 0,
                value if dir>0 else 0]
            self.neural.train(x,y)
        self.data = []

    def event_handling(self):

        i = [self.ball.x, self.ball.y, self.y, self.ball.velox, self.ball.veloy]
        r = self.neural.query(i)
        if r[0] > r[1] and r[0] > r[2]:
            self.y_change = -SPEED
        elif r[1] > r[0] and r[1] > r[2]:
            self.y_change = 0
        else:
            self.y_change = SPEED

        self.data.append([i,[r[0][0],r[1][0],r[2][0]]])

class NeuralPlayer2(Player):
    def __init__(self, x, ball):
        Player.__init__(self, x)
        self.y_change = SPEED
        self.ball = ball
        input_nodes = 3
        hidden_nodes = 3
        output_nodes = 1

        learning_rate = 0.3

        self.neural = nn.neuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

        self.data = []

    def welldone(self):
        for a in self.data[-30:]:
            self.neural.train(a,[1])
        self.data = []

    def lost(self,dir,value):
        for a in self.data[-10:]:
            self.neural.train(a,[0])
        self.data = []

    def currentData(self, val):
        return [self.ball.y, self.y, val*1000]
        return [self.ball.x, self.ball.y, self.y, self.ball.velox, self.ball.veloy, val*1000]

    def result(self,val):
        i = self.currentData(val)
        r = self.neural.query(i)
        print(r)
        print(i)
        return r[0]

    def event_handling(self):
        r = [self.result(-1), self.result(0), self.result(1)]
        dir = 0
        if r[0] > r[1] and r[0] > r[2]:
            dir = -1
        elif r[1] > r[0] and r[1] > r[2]:
            dir = 0
        else:
            dir = 1
            
        self.y_change = dir * SPEED

        self.data.append(self.currentData(dir))


class NeuralPlayer3(NeuralPlayer2):
    def __init__(self, x, ball):
        NeuralPlayer2.__init__(self, x, ball)
        self.ticks=0

    def event_handling(self):
        self.ticks = self.ticks+1
        if self.ticks<1500:
            print("TRAIN"+str(self.ticks))
            dir= 0
            if self.ball.y > self.y:
                dir = 1
            if self.ball.y < self.y:
                dir = -1
            self.y_change = dir * SPEED
#            self.data.append(self.currentData(dir))
            self.neural.train(self.currentData(1),[1 if dir==1 else 0])
            self.neural.train(self.currentData(0),[1 if dir==0 else 0])
            self.neural.train(self.currentData(-1),[1 if dir==-1 else 0])

        else:
            NeuralPlayer2.event_handling(self)




class Ball:

    def __init__(self):
        self.reset()

    def reset(self):
        self.x = w.x / 2
        self.y = w.y / 2
        self.w = 15
        self.h = 15
        self.velox = -BALL_SPEED
        self.veloy = random.randrange(-3,3) #-1
        self.multi = 0.03

    def draw_ball(self, w):
        pygame.draw.rect(w, white, [self.x, self.y, self.w, self.h])

    def step(self):
        self.x += self.velox
        self.y += self.veloy

b = Ball()
p = Human(0, pygame.K_w, pygame.K_s)
#p = SimplePC2(0, b)
p2 = NeuralPlayer3(775, b)
#p = SimplePC2(0, b)
#p2 = SimplePC2(775, b)

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
    done = False
    if b.x < 0:
        #message_display("Right wins")
        p.lost(1 if p.y<b.y else -1, abs(b.y-p.y)*1.0/(w.y))
        done = True
    elif b.x > w.x:
        #message_display("Left wins")
        p2.lost(1 if p2.y<b.y else -1, abs(b.y-p2.y)*1.0/(w.y))
        done = True
    if done:
        b.reset()
        p.reset()
        p2.reset()

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
