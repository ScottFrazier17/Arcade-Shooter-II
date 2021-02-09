import pygame
import random
import math
from pygame import mixer
import time

# Initialize the game
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((1100, 550))

# Clock/FPS
clock = pygame.time.Clock()

# Background
background = pygame.image.load('Space Background Mark II.png').convert()

# Background Music
mixer.music.load('Orbital_Colossus.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption('Space Invaders Mark II')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Animated Text
def text_animation(string, x, y):
    text = ''
    text_font = pygame.font.Font('freesansbold.ttf', 72)
    for letter in range(len(string)):
        text += string[letter]
        text_surface = text_font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (x, y))

# Score Board
score_value = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)
scoreX = 10
scoreY = 10
def score_board(x, y):
    score_text = score_font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score_text, (x, y))

# Game Over
game_over_font = pygame.font.Font('freesansbold.ttf', 64)
def game_over(x, y):
    game_over_text = game_over_font.render('GAME OVER', True, (0, 0, 0))
    screen.blit(game_over_text, (x, y))

# Player
playerIMG = pygame.image.load('PlayerShip.png')
playerX = 500
playerY = 460
playerX_change = 0
def player(x,y):
    screen.blit(playerIMG, (x, y))

# Laser
laserIMG = pygame.image.load('Laser.png')
laserX = 0
laserY = 480
laserX_change = 0
laserY_change = 15
laser_state = 'Loaded'
def fire_laser(x,y):
    global laser_state
    laser_state = 'Fired'
    screen.blit(laserIMG, (x, y - 25))

# Enemy
enemyIMG = []
enemy_rect = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyIMG.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(10, 130))
    enemyX_change.append(5)
    enemyY_change.append(50)
def enemy(x, y, i):
    screen.blit(enemyIMG[i], (x, y))

# Boss
bossIMG = pygame.image.load('monster (1).png')
bossX = 500
bossY = 25
bossX_change = 5
bossY_change = 35
boss_hp = 5
boss_current_hp = 5
end_game = False
end_game1 = False
def boss(x, y):
    screen.blit(bossIMG, (x,y))

# Collision Function
def isCollision(enemyX, enemyY, laserX, laserY):
    global dis_death
    dis_death = 50
    distance = math.sqrt((math.pow(enemyX - laserX, 2))) + (math.pow(enemyY - laserY, 2))
    if distance <= dis_death:
        return True

# Game Loop
running = True
while running:
    screen.blit(background, (0, 0))

    # Event
    for event in pygame.event.get():

        # Quit Mechanic
        if event.type == pygame.QUIT:
            running = False

        # Player Controls
        # Movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -7
            if event.key == pygame.K_RIGHT:
                playerX_change = 7

            # Shooting
            if event.key == pygame.K_SPACE:
                if laser_state =='Loaded':
                    laserX = playerX
                    laser_sound = mixer.Sound('laser.wav')
                    laser_sound.play()
                    fire_laser(laserX, laserY)
        # Stop Moving
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Boundaries
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 1034:
        playerX = 1036

    # Enemy Movement
    for i in range(num_of_enemies):
        enemyX[i]+=enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 1036:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]

        # Game Over
        if enemyY[i] >= 420:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over(350, 225)
            break

        # Collision Detection
        collision = isCollision(enemyX[i], enemyY[i], laserX, laserY)
        if collision:
            laserY = 480
            laser_state = 'Loaded'
            score_value += 100
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(10, 130)
        enemy(enemyX[i], enemyY[i], i)

    # Laser Mechanic
    if laser_state == 'Fired':
        fire_laser(laserX, laserY)
        laserY -= laserY_change
    if laserY <= 0:
        laserY = 480
        laser_state = 'Loaded'

    # Boss Stage
    if 1509 >= score_value >= 1500:
        global score
        end_game = True
        score_value += 100

# Stage Setup
    if end_game:
        for i in range(num_of_enemies):
            enemyY[i]=-100
            enemyY_change[i]=-50
        text_animation('PREPARE TO DIE', 250, 200)
        pygame.display.update()
        time.sleep(3)
        end_game = False
        end_game1 = True

# Boss
    if end_game1:
        # Boss Mechanic
        boss(bossX, bossY)
        bossX += bossX_change
        if bossX <= 0:
            bossX_change = 10
            bossY += bossY_change
        elif bossX >= 1036:
            bossX_change = -10
            bossY += bossY_change

        # Collision with Boss
        dis_death = 128
        collision1 = isCollision(bossX, bossY, laserX, laserY)
        if collision1:
            laserY=480
            laser_state='Loaded'
            explosion_sound=mixer.Sound('explosion.wav')
            explosion_sound.play()
            boss_current_hp -= 1

    # End Game
    if boss_current_hp <= 0:
        text_animation('YOU SAVED THE WORLD', 100, 200)
        bossX = -2000
        bossX_change -= .01
    elif bossY >= 350:
        game_over(350, 225)
        boss_current_hp = 5


    score_board(scoreX, scoreY)
    player(playerX, playerY)
    pygame.display.update()
    clock.tick(60)


