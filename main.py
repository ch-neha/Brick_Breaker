import math
import pygame
import tkinter as tk
from pygame import mixer

# inputs and initial states
WIDTH, HEIGHT = 1000, 600
boardX, boardY = 430, 540
ballX, ballY = 480, 520
change, xchange, ychange, score, life = 0, 0, 0, 0, 3

rectangles = 7
begin = False
first = True
start = False
brick = []
rows = []
rx = []
ry = []


# initialize the pygame, create screen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('BrickBreaker')
brd = pygame.image.load('Resources/paddle.png')
board = pygame.transform.scale(brd, (120, 50))
bl = pygame.image.load('Resources/ball.png')
ball = pygame.transform.scale(bl, (25, 25))
brick.append(pygame.image.load('Resources/blue.png'))
brick.append(pygame.image.load('Resources/yellow.png'))
brick.append(pygame.image.load('Resources/purple.png'))
col = mixer.Sound('Resources/collision.wav')
over = mixer.Sound('Resources/gameover.wav')
pb = mixer.Sound('Resources/paddleBounce.wav')


'''
for loops add positions and brickks into lists
rx holds the values of xcordinates of all bricks
ry contains ycordinates of all bricks
rows contains all bricks and their shapes 
'''

x, y = 0, 0
for i in range(3):
    row = []
    rx1 = []
    ry1 = []
    for j in range(rectangles):
        row.append(pygame.transform.scale(brick[i], (125, 50)))
        rx1.append(50+x)
        ry1.append(100+y)
        x += 130
    rows.append(row)
    rx.append(rx1)
    ry.append(ry1)
    y += 60
    x = 0


def display_gameover(result):
    # creates a tkinter window when the game is over
    global score
    window = tk.Tk()
    window.title("GameOver!")
    label = tk.Label(
        text=result+"\nYour score is : " + str(score),
        font=("Arial,100"),
        foreground="white",
        background="red",
        width=30,
        height=10
    )
    label.pack()
    window.eval('tk::PlaceWindow . center')
    window.mainloop()
    pygame.quit()


def show_score(score):
    # displays current score and number of remaining lives
    global start, life
    pygame.font.init()
    font = pygame.font.Font('freesansbold.ttf', 32)
    s = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(s, (10, 10))
    lives = font.render("lives : " + str(life), True, (255, 255, 255))
    screen.blit(lives, (850, 10))
    if(start == False):
        space = font.render("Click space bar to start!", True, (255, 255, 255))
        screen.blit(space, (300, 295))


def collision_blocks(ballX, ballY, xchange, ychange):
    # displays bricks and breaks bricks when collision occurs
    global score, first
    for i in range(3):
        for j in range(rectangles):
            distance = math.sqrt(
                math.pow((rx[i][j] + 62-ballX-12), 2) + math.pow((ry[i][j] + 25-ballY-12), 2))
            if distance < 60:
                col.play()
                rx[i][j] = 3000
                ry[i][j] = 3000
                ychange *= -1
                score += 1
            screen.blit(rows[i][j], (rx[i][j], ry[i][j]))

    # checks if all blocks are broken or not
    all = True
    for i in range(3):
        for j in range(rectangles):
            if rx[i][j] != 3000:
                all = False
                break

    # ends game if all bricks are broken
    if(all):
        win = True
        ballX = 3000
        if(first):
            first = False
            over.play()
            display_gameover('CONGRATULATIONS! YOU WIN')
    show_score(score)
    return ychange


def display_board_ball(x, y, ballX, ballY):
    # displays the board and ball on screen
    screen.fill((0, 0, 0))
    screen.blit(board, (x, y))
    screen.blit(ball, (ballX, ballY))


def collision_board(ballX, ballY, boardX, boardY):
    # checks for ball and board collision and performs reflections at the board
    global xchange, ychange
    global begin
    dis = math.sqrt(math.pow((ballX+12-boardX-60), 2) +
                    math.pow((ballY+12-boardY-25), 2))
    if dis > 32 and dis <= 47 and begin == True:
        ychange *= -1
        if(begin):
            pb.play()
        begin = False
    elif dis > 47 and dis <= 56 and begin == True and ballY > 520:
        if xchange > 0 and ballX < boardX+62:
            xchange *= -1
            ychange *= -1
        elif xchange < 0 and ballX > boardX+62:
            xchange *= -1
            ychange *= -1
        else:
            ychange *= -1
        if(begin):
            pb.play()
    else:
        if ballY < 505:
            begin = True


def checkBoundaries():
    # performs reflections at walls
    global xchange, ychange
    global start, life, first
    global ballX, ballY
    global boardX, boardY
    if ballX <= 5 or ballX >= 970:
        xchange *= -1
    if ballY <= 5:
        ychange *= -1
    if ballY > 542:
        if(first):
            first = False
            over.play()
            life -= 1
            if(life == 0):
                display_gameover('Oops! You lose')
            else:
                ballX, ballY = 480, 520
                boardX, boardY = 430, 540
                xchange, ychange = 0, 0
                start = False
                first = True


def board_boundary():
    # checks that the board doesnt go beyond the boundary limits
    global boardX
    if(boardX < 0):
        boardX = 0
    if(boardX > 880):
        boardX = 880


# driver code
if __name__ == "__main__":
    screen.fill((0, 0, 0))

    # game loop
    running = True
    while running:

        # ball and board move together until game starts
        if(start == False):
            ballX, ballY = boardX + 50, boardY - 18

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            '''
            if keystroke is pressed then it checks whether it's a left or right or space key
            board and ball are moved accordingly
            '''
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # game starts
                    start = True
                    xchange -= 1.5
                    ychange -= 1.5
                if event.key == pygame.K_LEFT:
                    change = -2
                if event.key == pygame.K_RIGHT:
                    change = 2

            # board continues to move in same direction until key is released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    change = 0

        boardX += change

        board_boundary()
        checkBoundaries()

        # update ball's coordinates
        ballX += xchange
        ballY += ychange

        collision_board(ballX, ballY, boardX, boardY)

        display_board_ball(boardX, boardY, ballX, ballY)
        ychange = collision_blocks(ballX, ballY, xchange, ychange)
        pygame.display.update()
