import pygame
pygame.init()
pygame.mixer.init()
from random import*

dino_image = pygame.image.load('t-rex.png')
obstacle_image = pygame.image.load('Cactus.png')
ground_image = pygame.image.load('bcff74a8a6252d8.png')
jump_sound = pygame.mixer.Sound('pixel-jump-319167.mp3')
colliderrect_sound = pygame.mixer.Sound('pixel-explosion-319166.mp3')
backround_sound = pygame.mixer.Sound('retro-wave-revival_92786.mp3')


pygame.init()
screen_width = 900
screen_height = 450
screen = pygame.display.set_mode((screen_width, screen_height))
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
clock = pygame.time.Clock()
fps = 30
high_score = 0
font = pygame.font.SysFont('comicsans', 36)
dino_image=pygame.transform.scale(dino_image,(60,60))
obstacle_image=pygame.transform.scale(obstacle_image,(40,60))
ground_height = screen_height - dino_image.get_height() - 10  # 10 — отступ от низа
ground_image = pygame.transform.scale(ground_image, (screen_width, ground_height))


class Dino:
    def __init__(self):
        self.image=dino_image
        self.x = 50
        self.y = 300
        self.is_jumping = False
        self.jump_count = 10
        self.gravity = 1
        self.rect= pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())


    def draw(self, win):
        win.blit(self.image,(self.x, self.y))

    def jump(self):
        if self.is_jumping:
            if self.jump_count >=-10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.y -= (self.jump_count ** 2) *0.5 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = 10

    def displayScore(self,score):
        score_text = font.render(f"Score:{round(score)}", True, black)
        screen.blit(score_text, (10, 10))

class Obstacle:
    def __init__(self, x, y, width, height, speed):
        self.image = obstacle_image
        self.x = screen_width
        self.y = y
        self.width=width
        self.height = height
        self.speed = speed
        self.passed = False

    def reset(self):
        self.width = randint(15, 40)
        self.height = randint(40, 50)
        self.speed = randint(10, 15)
        self.x = screen_width
        self.y = 300
        self.passed=False
        if self.x<=0:
            self.passed=True

    def draw(self, win):
        win.blit(self.image,(self.x, self.y))

    def move(self):
        self.x -= self.speed
        if self.x < -self.width:
            self.reset()

class Ground:
    def __init__(self,height,y, speed):
        self.image = ground_image
        self.x1 =0
        self.x2 = self.image.get_width()
        self.y=y
        self.speed = speed
    def move(self):
        self.x1 -= self.speed
        self.x2 -= self.speed

        if self.x1 <= -self.image.get_width():
            self.x1 = self.x2 + self.image.get_width()

        if self.x2 <= -self.image.get_width():
            self.x2 = self.x1 + self.image.get_width()
    def draw(self, screen):
        screen.blit(self.image, (self.x1, self.y))
        screen.blit(self.image, (self.x2, self.y))
def game(high_score):
    waiting = True
    while waiting:
        screen.fill(white)

        title_text = font.render(" DINO GAME ", True, black)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 120))

        instruction_text = font.render("Нажмите ПРОБЕЛ, чтобы начать", True, black)
        screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

        pygame.display.update()
        clock.tick(fps)

    dino_image = Dino()
    m = randint(15, 40)
    l = 0
    b = randint(10, 15)
    obstacle = Obstacle(screen_width, 300 + l // 2, m, l, b)
    ground_y = screen_height - ground_image.get_height()
    grass=Ground(ground_image.get_height(),ground_y,obstacle.speed)
    backround_sound.play()


    collider=False
    running = True
    game_over = False


    score = 0
    a=0
    jump=0
    increase=False
    if obstacle.x<=0:
        obstacle.reset()
    if score!=a:
        a=score
        score+=score/50
    while running:
        score += 1/3

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False, high_score
        screen.fill(white)
        dino_image.draw(screen)
        grass.draw(screen)
        grass.move()
        obstacle.draw(screen)
        obstacle.move()
        dino_image.displayScore(score)
        if score>=100:
            screen.fill(green)
            dino_image.draw(screen)
            grass.draw(screen)
            obstacle.draw(screen)
            obstacle.move()
            dino_image.displayScore(score)
        if score%100==0 and score!=0 and increase==False:
            obstacle.speed+=1
            increase=True
        elif score%100==0:
            increase=False
        # Проерка на столкновение
        keys = pygame.key.get_pressed()
        if not dino_image.is_jumping and keys[pygame.K_SPACE]:
                dino_image.is_jumping = True
                jump=jump+1
                jump_sound.play()
        if obstacle.x < dino_image.x + dino_image.image.get_width() and obstacle.x + obstacle.width > dino_image.x:
            if dino_image.y + dino_image.image.get_height() > obstacle.y:
                game_over = True
                if not collider:
                    colliderrect_sound.play()
                    collider = True
        else:
            collider = False
        if not game_over and not obstacle.passed and obstacle.x + obstacle.width < dino_image.x:
            obstacle.passed = True

        if game_over:
            pygame.mixer.Sound.stop(backround_sound)
            score=0
            jump=0
            over_text=font.render("Столкновение!", True, black)
            screen.blit(over_text, (screen_width//2-150, screen_height//2-50))
            restart_text = font.render("Нажмите 'r' чтобы начать заново", True, black)
            screen.blit(restart_text, (screen_width//2-250, screen_height//2))
            if keys[pygame.K_r]:
                return True,high_score
        else:
            if round(score)>high_score:
                high_score=round(score)

        high_score_text = font.render(f"Record: {high_score}", True, black)
        screen.blit(high_score_text, (10, 50))

        jump_count_text = font.render(f"Счетчик прыжков: {jump}", True, black)
        screen.blit(jump_count_text, (screen_width-350, 10))



# Обработка событий

        dino_image.jump()
        pygame.display.update()
        clock.tick(fps)
    return True,high_score
high_score=0
running = True
while running:
    running,high_score=game(high_score)

pygame.quit()
