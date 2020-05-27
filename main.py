import pygame
import random
import math
from pygame import mixer

# Starting the game
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('images/bg.jpg')

# Sound
mixer.music.load("sounds/bgs.wav")
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space invaders")
icon = pygame.image.load('images/space_ship.png')
pygame.display.set_icon(icon)

# Score
score_value = 0
font = pygame.font.Font('fonts/freesansbold.ttf', 32)
text_x = 10
text_y = 10

# Math operation
font_math = pygame.font.Font('fonts/freesansbold.ttf', 20)
math_x = 500
math_y = 10
operator_1 = random.randint(0, 10)
operator_2 = random.randint(0, 10)
correct_answer_monster_pos = 0
next_math = True

# Game over text
game_over_font = pygame.font.Font('fonts/freesansbold.ttf', 64)

# Pause text
pause_font = pygame.font.Font('fonts/freesansbold.ttf', 64)

# Game status
pause_status = False
you_loose = False

def show_math(x,y):
    operation = font.render(str(operator_1)+ " x " + str(operator_2) + " =", True, (255, 255, 255)) 
    screen.blit(operation, (x, y))

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = game_over_font.render("GAME OVER: " + str(score_value), True, (255, 255, 255))
    restart_text = game_over_font.render("Press R to restart", True, (255, 255, 255))
    screen.blit(over_text, (150, 240))
    screen.blit(restart_text, (150, 310))


def pause_text():
    pause_text_message = pause_font.render("P A U S E ", True, (255, 255, 255))
    screen.blit(pause_text_message, (230, 250))


# Player
player_img = pygame.image.load('images/player_icon.png')
player_x = 370
player_y = 480
player_x_change = 0


def player(x, y):
    screen.blit(player_img, (x, y))


# Monster
monster_img = []
monster_x = []
monster_y = []
monster_x_change = []
monster_y_change = []
monster_resoult = []
monster_values = []
number_enemies = 21
real_time_enemies = 5
monster_value = 0

for i in range(number_enemies):
    if 1 <= i <= 5:
        monster_img.append(pygame.image.load('images/monster.png'))
    elif 5 < i <= 10:
        monster_img.append(pygame.image.load('images/monster2.png'))
    elif i > 10:
        monster_img.append(pygame.image.load('images/monster3.png'))
    monster_x.append(random.randint(0, 736))
    monster_y.append(random.randint(50, 150))
    monster_x_change.append(2)
    monster_y_change.append(50)
    monster_value = random.randint(0, 100)
    monster_values.append(monster_value)
    monster_resoult.append(font_math.render(str(monster_value), True, (153, 0, 0)))


def monster(x, y, i):
    #monster_resoult.insert(correct_answer_monster_pos, font_math.render(str(operator_1 * operator_2), True, (153, 0, 0)))
    screen.blit(monster_img[i], (x, y))
    screen.blit(monster_resoult[i], (x+20, y+40))


# Bullet
bullet_img = pygame.image.load('images/bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 9
bullet_shoot = False


def fire_bullet(x, y):
    global bullet_shoot
    bullet_shoot = True
    screen.blit(bullet_img, (x + 16, y + 10))


def is_Collision(enemy_x, enemy_y, player_x, player_y):
    # Distance between two points
    distance = math.sqrt(pow((player_x - enemy_x), 2) + pow((player_y - enemy_y), 2))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running_game = True
while running_game:
    screen.fill((0, 0, 50))
    # Background
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_game = False

        # If keystroke is pressed
        if event.type == pygame.KEYDOWN:
            if not pause_status:
                if event.key == pygame.K_LEFT:
                    player_x_change = -3.5
                if event.key == pygame.K_RIGHT:
                    player_x_change = 3.5
                if event.key == pygame.K_SPACE:
                    if not bullet_shoot:
                        bulletSound = mixer.Sound("sounds/laser.wav")
                        bulletSound.play()
                        bullet_x = player_x
                        fire_bullet(bullet_x, bullet_y)
            else:
                pause_text()

            # Pause when press p key
            if event.key == pygame.K_p:
                pause_status = not pause_status
            # Restart when press r key
            if you_loose:
                if event.key == pygame.K_r:
                    real_time_enemies = 5
                    score_value = 0
                    you_loose = False
                    for i in range(real_time_enemies):
                        monster_y[i] = random.randint(50, 150)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # MOVEMENT..........................................................................................................
    if not pause_status:
        # Player movement
        player_x += player_x_change
        if player_x <= 0:
            player_x = 0
        elif player_x >= 736:
            player_x = 736

        # Enemy movement
        for i in range(real_time_enemies):
            # Game over
            if monster_y[i] > 420:
                for j in range(real_time_enemies):
                    monster_y[j] = 2000
                game_over_text()
                you_loose = True
                break

        for i in range(real_time_enemies):
            monster_x[i] += monster_x_change[i]
            if monster_x[i] <= 0:
                monster_x_change[i] = 1
                monster_y[i] += monster_y_change[i]
            elif monster_x[i] >= 736:
                monster_x_change[i] = -1
                monster_y[i] += monster_y_change[i]
            # Collision
            collision = is_Collision(monster_x[i], monster_y[i], bullet_x, bullet_y)
            if collision:
                explosionSound = mixer.Sound("sounds/explosion.wav")
                explosionSound.set_volume(5)
                explosionSound.play()
                bullet_y = 480
                bullet_shoot = False
                score_value += 1
                if score_value == 30:
                    player_img = pygame.image.load('images/player2_icon.png')
                if score_value % 5 == 0:
                    if real_time_enemies == number_enemies - 1:
                        pass
                    else:
                        real_time_enemies += 1
                monster_x[i] = random.randint(0, 736)
                monster_y[i] = random.randint(50, 150)

                # Check if is the correct answer when collision
                if monster_values[i] == operator_1 * operator_2:
                    next_math = True
                    # update the screen
                    operator_1 = random.randint(0, 10)
                    operator_2 = random.randint(0, 10)
                    show_math(math_x, math_y)

            # Define if the resoult is correct
            if next_math:
                monster_resoult.insert(correct_answer_monster_pos, font_math.render(str(operator_1 * operator_2), True, (153, 0, 0)))
                monster_values.insert(correct_answer_monster_pos, operator_1*operator_2)

                # Increase the correct answer counter
                if correct_answer_monster_pos <= real_time_enemies:
                    correct_answer_monster_pos += 1
                else:
                    correct_answer_monster_pos = 0

                next_math = False
            monster(monster_x[i], monster_y[i], i)

        # Bullet movement
        if bullet_y <= 0:
            bullet_y = 480
            bullet_shoot = False
        if bullet_shoot:
            fire_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_y_change

        player(player_x, player_y)
        show_score(text_x, text_y)
        show_math(math_x, math_y)
    else:
        pause_text()

        # END MOVEMENT..................................................................................................
    pygame.display.update()
