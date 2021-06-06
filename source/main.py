import pygame
import random
import math
from pygame import mixer



# Initializing pygame
pygame.init()

# Creating screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.jpg')

# Background music
mixer.music.load('backmusic.wav')
mixer.music.play(-1)

# Title
pygame.display.set_caption("Pyramid Panic")

# Icon
icon = pygame.image.load('pyramid.png')
pygame.display.set_icon(icon)

# User
userImage = pygame.image.load('user.png')
userX = 370
userY = 480
changeUX = 0

# Enemy features
enemyImage = []
enemyX = []
enemyY = []
changeEX = []
changeEY = []
num_of_enemies = 6

# Creating multiple enemies
for i in range(num_of_enemies):
    enemyImage.append(pygame.image.load('ra2.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    changeEX.append(0.25)
    changeEY.append(30)

# Spear
spearImage = pygame.image.load('spear.png')
spearX = 0
spearY = 480
changeSX = 0
changeSY = 0.45  # spear speed
spearState = 0  # 0 -> invisible |  1 -> visible

# Score
killed = 0

# Font
font = pygame.font.Font('freesansbold.ttf', 32)

# Score Coordinates
textX = 10
textY = 10

# Final Game Over text
lastText = pygame.font.Font('freesansbold.ttf', 64)

# Display Score
def scoreShow(x, y):
    score = font.render("Score: " + str(killed), True, (0, 0, 0))
    screen.blit(score, (x, y))

# Display Final Message
def gameOver():
    text = lastText.render("GAME OVER", True, (0, 0, 0))
    screen.blit(text, (200, 250))

# Draw user to screen
def user(x, y):
    screen.blit(userImage, (x, y))


# Draw enemy to screen
def enemy(x, y, i):
    screen.blit(enemyImage[i], (x, y))


def fireSpear(x, y):
    global spearState
    spearState = 1  # visible
    screen.blit(spearImage, (x + 16, y + 10))


def isColliding(enemyX, enemyY, spearX, spearY):
    # Simple Pythagorean Theorem for calculating distance between two points
    distance = math.sqrt((math.pow(enemyX - spearX, 2)) + (math.pow(enemyY - spearY, 2)))

    # If space between spear and enemy is less than 30 pixels, collision occurs
    return True if distance < 30 else False


# Game state boolean
running = True

# Game loop
while running:

    # Background color - old
    screen.fill((245, 213, 161))

    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():

        # Quit Game
        if event.type == pygame.QUIT:
            running = False

        # Moving the player to left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                changeUX = -0.3
            if event.key == pygame.K_RIGHT:
                changeUX = 0.3

            # Throwing spear if it is available
            if event.key == pygame.K_SPACE:
                if spearState == 0:
                    spearSound = mixer.Sound('throw.wav')
                    spearSound.play()
                    # Getting user coordinate to fire spear
                    spearX = userX
                    fireSpear(spearX, spearY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                changeUX = 0

    # Updating user coordinates
    userX += changeUX

    # Drawing user boundaries
    if userX <= 0:
        userX = 0
    elif userX >= 736:
        userX = 736

    # Updating enemy coordinates
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            gameOver()
            break

        enemyX[i] += changeEX[i]

        # Drawing enemy boundaries
        if enemyX[i] <= 0:
            changeEX[i] = 0.25
            enemyY[i] += changeEY[i]
        elif enemyX[i] >= 736:
            changeEX[i] = -0.25
            enemyY[i] += changeEY[i]

        # Collision detection
        collision = isColliding(enemyX[i], enemyY[i], spearX, spearY)
        if collision:
            # Adding explosion sound effect
            explosionSound = mixer.Sound('explosion.wav')
            explosionSound.play()
            spearY = 480
            spearState = 0
            killed += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        # Drawing enemy
        enemy(enemyX[i], enemyY[i], i)

    # Spear Boundary
    if spearY <= 0:
        spearY = 480
        spearState = 0

    # Spear Movement
    if spearState == 1:
        fireSpear(spearX, spearY)
        spearY -= changeSY

    # Draw user
    user(userX, userY)
    # Display score
    scoreShow(textX, textY)
    pygame.display.update()
