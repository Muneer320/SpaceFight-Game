import pygame
import os
pygame.font.init()
pygame.mixer.init()


WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Fighter")

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

BULLET_HIT_SOUND = pygame.mixer.Sound("Assets\Grenade+1.mp3")
BULLET_FIRE_SOUND = pygame.mixer.Sound("Assets\Gun+Silencer.mp3")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREY = (200, 200, 200)

FPS = 60
VELOCITY = 5
BULLET_VEL = 7
MAX_BULLETS = 5

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)


HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = (55, 40)

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

pygame.display.set_icon(YELLOW_SPACESHIP)



class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False


def draw_window(yellow, red, yelllow_bullets, red_bullets, yellow_health, red_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in yelllow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()


def yellow_handle_movement(key_pressed, yellow):
    if key_pressed[pygame.K_a] and yellow.x - VELOCITY > 0:  # Left
        yellow.x -= VELOCITY
    if key_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.width < BORDER.x:  # Right
        yellow.x += VELOCITY
    if key_pressed[pygame.K_w] and yellow.y - VELOCITY > 0:  # Up
        yellow.y -= VELOCITY
    if key_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT - 15:  # Down
        yellow.y += VELOCITY


def red_handle_movement(key_pressed, red):
    if key_pressed[pygame.K_LEFT] and red.x - VELOCITY - red.height > BORDER.x - 15:  # Left
        red.x -= VELOCITY
    if key_pressed[pygame.K_RIGHT] and red.x + VELOCITY + red.width < WIDTH + 15:  # Right
        red.x += VELOCITY
    if key_pressed[pygame.K_UP] and red.y - VELOCITY > 0:  # Up
        red.y -= VELOCITY
    if key_pressed[pygame.K_DOWN] and red.y - VELOCITY < HEIGHT - 65:  # Down
        red.y += VELOCITY


def handleBullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    if text == "Yellow Wins!":
        draw_text = WINNER_FONT.render(text, 1, YELLOW)
    else:
        draw_text = WINNER_FONT.render(text, 1, RED)

    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(2000)


def display_buttons(REPLAY_BUTTON, QUIT_BUTTON):
    REPLAY_BUTTON.draw(WIN)
    QUIT_BUTTON.draw(WIN)
    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEMOTION:
                if REPLAY_BUTTON.isOver(pos):
                    REPLAY_BUTTON.color = GREY
                    REPLAY_BUTTON.draw(WIN)
                    pygame.display.update()
                else:
                    REPLAY_BUTTON.color = YELLOW
                    REPLAY_BUTTON.draw(WIN)
                    pygame.display.update()

                if QUIT_BUTTON.isOver(pos):
                    QUIT_BUTTON.color = GREY
                    QUIT_BUTTON.draw(WIN)
                    pygame.display.update()
                else:
                    QUIT_BUTTON.color = RED
                    QUIT_BUTTON.draw(WIN)


            if event.type == pygame.MOUSEBUTTONDOWN:
                    if REPLAY_BUTTON.isOver(pos):
                        main()
                        break
                        
                    if QUIT_BUTTON.isOver(pos):
                        pygame.quit()


def main():
    yellow = pygame.Rect(215, 290, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(675, 290, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    yellow_bullets = []
    red_bullets = []

    red_health = 10
    yellow_health = 10

    REPLAY_BUTTON = button(YELLOW, WIDTH/2 - 300, HEIGHT/2 + 100, 250, 50, "REPLAY")
    QUIT_BUTTON = button(RED, WIDTH/2 + 50, HEIGHT/2 + 100, 250, 50, "QUIT")

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health)
            draw_winner(winner_text)
            display_buttons(REPLAY_BUTTON, QUIT_BUTTON)
            break


        key_pressed = pygame.key.get_pressed()

        yellow_handle_movement(key_pressed, yellow)
        red_handle_movement(key_pressed, red)
        handleBullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health)


if __name__ == "__main__":
    main()
