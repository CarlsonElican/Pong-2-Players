import pygame
pygame.init()

WIDTH, HEIGHT, = 700, 500
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7
FONT = pygame.font.SysFont("times new roman", 30)
WINNING_SCORE = 10

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong AI Game")

class Paddle:
    PADDLECOLOR = WHITE
    MS = 4
    
    def __init__(self, x, y, width, height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def draw(self, window):
        pygame.draw.rect(window, self.PADDLECOLOR, (self.x, self.y, self.width, self.height))
        
    def move (self, up=True):
        if up:
            self.y -= self.MS
        else:
            self.y += self.MS
            
    def resetPaddles(self):
        self.x = self.original_x
        self.y = self.original_y

class Ball:
    MAX_MS = 5
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.radius = radius
        self.x_MS = self.MAX_MS
        self.y_MS = 0 
        
    def draw(self, window):
        pygame.draw.circle(window, self.COLOR, (self.x, self.y), self.radius)   
        
    def move(self):
        self.x += self.x_MS
        self.y += self.y_MS
        
    def resetBall(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_MS = 0
        self.x_MS *= -1
        

def draw(window, paddles, ball, left_score, right_score):
    window.fill(BLACK)
    left_score_text = FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = FONT.render(f"{right_score}", 1, WHITE)
    window.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    window.blit(right_score_text, (WIDTH * 3/4 - right_score_text.get_width() // 2, 20))

    
    for paddle in paddles:
        paddle.draw(window)
        
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(window, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))
    
    ball.draw(window)
    pygame.display.update()


def collision (ball, left_paddle, right_paddle):
    
    #Ceiling collision
    if ball.y + ball.radius >= HEIGHT:
        ball.y_MS *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_MS *= -1
        
    #Paddle collision    
    if ball.x_MS < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_MS *= -1
                
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_y = middle_y - ball.y
                reduction = (left_paddle.height / 2) / ball.MAX_MS
                ball.y_MS = difference_y/ reduction * -1
        
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_MS *= -1
                
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_y = middle_y - ball.y
                reduction = (right_paddle.height / 2) / ball.MAX_MS
                ball.y_MS = difference_y/ reduction * -1
                


def move_paddle(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.MS >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.MS + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)
        
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.MS >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.MS + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)
        
        
def main():
    mainLoop = True
    frameRate = pygame.time.Clock()
    
    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
    
    left_score = 0
    right_score = 0
    
    while mainLoop:    
        frameRate.tick(FPS)
        draw(WINDOW, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainLoop = False
                break
     
        keys = pygame.key.get_pressed()
        move_paddle(keys, left_paddle, right_paddle)
        
        ball.move()  
        collision(ball, left_paddle, right_paddle) 
        
        
        if ball.x < 0:
            right_score += 1
            ball.resetBall()
        elif ball.x > WIDTH:
            left_score += 1 
            ball.resetBall()    
            
         
        gameEnd = False   
        if left_score >= WINNING_SCORE:
            gameEnd = True
            winner = "LEFT WINS!"
        elif right_score >= WINNING_SCORE:
            gameEnd = True
            winner = "RIGHT WINS!"
            
        if gameEnd:
            winnerText = FONT.render(winner, 1, WHITE)
            WINDOW.blit(winnerText, (WIDTH // 2 - winnerText.get_width() // 2, HEIGHT // 2 - winnerText.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.resetBall()
            left_paddle.resetPaddles()
            right_paddle.resetPaddles()
            left_score = 0
            right_score = 0
        
            
    pygame.quit()
    
if __name__ == '__main__':
    main()
    