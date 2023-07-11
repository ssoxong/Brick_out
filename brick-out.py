import pygame
import random
import time

class Bar:
    def __init__(self, screenSize):
        self.width = screenSize['width'] * 0.2
        self.height = 10
        self.speed = 10
        self.rect = pygame.Rect(screenSize['width'] // 2 - self.width // 2, screenSize['height'] - self.height - 50, self.width, self.height)

class Ball:
    def __init__(self, screenSize):
        self.radius = 20
        self.speed = 6
        self.rect = pygame.Rect(random.randint(self.radius, screenSize['width'] - self.radius), screenSize['height'] * 0.7, self.radius, self.radius)
        self.dx = 1  # 추가: x 방향 이동 속도
        self.dy = -1  # 추가: y 방향 이동 속도

class Block:
    def __init__(self, rect, color):
        self.rect = rect
        self.color = color

def collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.rect.right - rect.left
    else:
        delta_x = rect.right - ball.rect.left
    
    if dy > 0:
        delta_y = ball.rect.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.rect.top
        
    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy 
    elif delta_y > delta_x:
        dx = -dx

    return dx, dy

def set_block(screenSize):
    block_list = []
    color_list = [
        (255, 191, 217),  # 분홍색
        (255, 207, 159),  # 주황색
        (255, 234, 167),  # 노란색
        (192, 235, 192),  # 연두색
        (187, 222, 251),  # 하늘색
        (214, 191, 255),  # 보라색
    ]

    margin = 7
    index = 0
    for i in range(7):
        for j in range(6):
            rect = pygame.Rect(margin + 85 * i, margin + 30 + 50 * j, screenSize['width'] // 8, screenSize['width'] // 8 // 2)
            color = color_list[(i + index) % len(color_list)]
            block = Block(rect, color)
            block_list.append(block)
            index += 1

    return block_list

def main():
    screenSize = {'width': 600, 'height': 700}
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screenSize['width'], screenSize['height']))
    pygame.display.set_caption("BoB 12 - sso's Brick Out")

    bar = Bar(screenSize)
    ball = Ball(screenSize)
    block_list = set_block(screenSize)
    fp = 50
    score = 0
    bar_color = (255,255,255)


    while True:
        screen.fill([50, 50, 85])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        for block in block_list:
            pygame.draw.rect(screen, block.color, block.rect)

        pygame.draw.rect(screen, pygame.Color(bar_color), bar.rect, 0, 10)

        pygame.draw.circle(screen, pygame.Color('black'), ball.rect.center, ball.radius)

        ball_image = pygame.image.load('ball.png')
        ball_image = pygame.transform.scale(ball_image, (ball.radius * 2, ball.radius * 2))
        ball_image_rect = ball_image.get_rect(center=ball.rect.center)
        screen.blit(ball_image, ball_image_rect)

        ball.rect.x += ball.speed * ball.dx
        ball.rect.y += ball.speed * ball.dy

        if ball.rect.centerx < ball.radius or ball.rect.centerx > screenSize['width'] - ball.radius:
            ball.dx = -ball.dx

        if ball.rect.centery < ball.radius:
            ball.dy = -ball.dy

        if ball.rect.colliderect(bar.rect) and ball.dy > 0:
            ball.dx, ball.dy = collision(ball.dx, ball.dy, ball, bar.rect)

        hit_block = ball.rect.collidelist(block_list)
        if hit_block != -1:
            score += 1
            hit_rect = block_list[hit_block].rect
            bar_color = block_list[hit_block].color

            block_list.pop(hit_block)
            ball.dx, ball.dy = collision(ball.dx, ball.dy, ball, hit_rect)
            fp += 2
            bar.speed += 0.1

        score_str = "Score: " + str(score)
        font = pygame.font.SysFont('georgia', 20)

        text = font.render(score_str, True, pygame.Color('white'))
        screen.blit(text, (screenSize['width'] - text.get_width() - 7, 7))

        font = pygame.font.SysFont('georgia', 50)

        if ball.rect.bottom > screenSize['height']:
            
            lose_text = font.render("You lose....", True, pygame.Color('white'))
            screen.blit(lose_text, (screenSize['width'] // 2 - lose_text.get_width() // 2, screenSize['height'] // 2 - lose_text.get_height() // 2))
            pygame.display.flip()
            time.sleep(2)
            pygame.quit()
            exit()

        if not block_list:
            win_text = font.render("You Win!!!", True, pygame.Color('white'))
            screen.blit(win_text, (screenSize['width'] // 2 - win_text.get_width() // 2, screenSize['height'] // 2 - win_text.get_height() // 2))
            pygame.display.flip()
            time.sleep(2)
            pygame.quit()
            exit()

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and bar.rect.left > 0:
            bar.rect.left -= bar.speed
        elif key[pygame.K_RIGHT] and bar.rect.right < screenSize['width']:
            bar.rect.right += bar.speed

        pygame.display.flip()
        clock.tick(fp)

if __name__ == '__main__':
    main()
