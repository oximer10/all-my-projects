import pygame
from pygame import*
init()

font=font.SysFont('Arial',50)
screen_width = 900
screen_height = 600
screen = display.set_mode((screen_width, screen_height))
white = (254, 254, 254)
black = (5,5,5)
orange=(255,165,0)
blue = (0,0,255)
red = (255,0,0)
yellow = (255,255,0)
clock = time.Clock()
fps =30
point=0



class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width=width
        self.height = height
        self.color=color
        self.speed = 5
    def draw(self, screen):
        draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return Rect(self.x, self.y, self.width, self.height)

    def displayScore(self, text, score, x, y, color):
        text = font.render(text + str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)
        screen.blit(text, textRect)

    def move1(self, keys, other_player):
        # Вверх
        if keys[K_UP]:
            new_y = self.y - self.speed
            future_rect = Rect(self.x, new_y, self.width, self.height)
            if not future_rect.colliderect(other_player.get_rect()) and new_y >= 0:
                self.y = new_y

        # Вниз
        if keys[K_DOWN]:
            new_y = self.y + self.speed
            future_rect = Rect(self.x, new_y, self.width, self.height)
            if not future_rect.colliderect(other_player.get_rect()) and (new_y + self.height) <= screen_height:
                self.y = new_y

        # Влево
        if keys[K_LEFT]:
            new_x = self.x - self.speed
            future_rect = Rect(new_x, self.y, self.width, self.height)
            if not future_rect.colliderect(other_player.get_rect()) and new_x >= 0:
                self.x = new_x

        # Вправо
        if keys[K_RIGHT]:
            new_x = self.x + self.speed
            future_rect = Rect(new_x, self.y, self.width, self.height)
            if not future_rect.colliderect(other_player.get_rect()) and (new_x + self.width) <= screen_width:
                self.x = new_x

    def move2(self, keys, other_player):
        # Вверх
        if keys[K_w]:
            new_y = self.y - self.speed
            future_rect = Rect(self.x, new_y, self.width, self.height)
            if not future_rect.colliderect(other_player.get_rect()) and new_y >= 0:
                self.y = new_y

        # Вниз
        if keys[K_s]:
            new_y = self.y + self.speed
            future_rect = Rect(self.x, new_y, self.width, self.height)
            if not future_rect.colliderect(other_player.get_rect()) and (new_y + self.height) <= screen_height:
                self.y = new_y


        if keys[K_a]:
            new_x = self.x - self.speed
            future_rect = Rect(new_x, self.y, self.width, self.height)
            if not future_rect.colliderect(other_player.get_rect()) and new_x >= 0:
                self.x = new_x


        if keys[K_d]:
            new_x = self.x + self.speed
            future_rect = Rect(new_x, self.y, self.width, self.height)
            if not future_rect.colliderect(other_player.get_rect()) and (new_x + self.width) <= screen_width:
                self.x = new_x

    def update(self, yfac):
        self.y = self.y + self.speed * yfac
        if self.y + self.height >= screen_height:
            self.y = screen_height - self.height
        elif self.y <= 0:
            self.y = 0
        elif self.x + self.width >= screen_width:
            self.x = screen_width - self.width
        elif self.x <= 0:
            self.x = 0

class Ball:
    def __init__(self, posx, posy,color,radius,speed_x,speed_y):
        self.posx = posx
        self.posy = posy
        self.color = color
        self.radius = radius
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.xfac=-1
        self.yfac=1
        self.first=1
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)

    def get_rect(self):
        return Rect(self.posx - self.radius, self.posy - self.radius, self.radius * 2, self.radius * 2)

    def update(self):
        point=0
        self.posx += self.speed_x * self.xfac
        self.posy += self.speed_y * self.yfac

        if self.posy - self.radius <= 0 or self.posy + self.radius >= screen_height:
            self.yfac *= -1
            self.speed_x+=0.5
            self.speed_y+=0.5
        if self.posx <= 0 and self.first:
            self.first = 0
            point+= 1
            return 1
        elif self.posx >= screen_width and self.first:
            self.first = 0
            point+=1
            return -1

        return 0

    def reset(self):
        self.posx = screen_width // 2
        self.posy = screen_height // 2
        self.xfac *= -1
        self.yfac = 1
        self.first = 1

    def hit(self):
            self.xfac*=-1
            self.speed_x+=0.5
            self.speed_y+=0.5




running = True
player1 = Player (50, 225, 100, 300, red)
player2 = Player (825, 225, 100, 300, blue)
ball = Ball(screen_width//2, screen_height//2, yellow, 40, 5, 5)

player1score=0
player2score=0

player1_y=0
player2_y=0

while running:
    screen.fill(black) # Очистка экрана
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    player1.draw(screen) # Отрисовка игрока
    player2.draw(screen)
    ball.draw(screen)

    player1.update(0)
    player2.update(0)
    point=ball.update()
    if point==-1:
        player1score+=1
        ball.speed_x=5
        ball.speed_y=5
    elif point==1:
        player2score+=1
        ball.speed_x=5
        ball.speed_y=5
    if point!=0:
        ball.reset()


# Движение игрока
    keys = key.get_pressed()
    player1.move1(keys,player2)
    player2.move2(keys,player1)
    player1.displayScore('',player1score,100,30,yellow)
    player2.displayScore('',player2score,screen_width-100,30,yellow)
    display.update() # Обновление экрана
    clock.tick(fps) # Задание FPS

    # Проверка столкновений с игроками
    if ball.get_rect().colliderect(player1.get_rect()) or ball.get_rect().colliderect(player2.get_rect()):
        ball.hit()


    
quit()