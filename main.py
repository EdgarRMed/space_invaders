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
mixer.music.load("sounds/sw.wav")
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space invaders")
icon = pygame.image.load('images/space_ship.png')
pygame.display.set_icon(icon)

# Score
score_value = 0
font = pygame.font.Font('fonts/freesansbold.ttf', 32)
text_x = 10
text_y = 50

# Math operation
font_math = pygame.font.Font('fonts/freesansbold.ttf', 20)
font_math_operation = pygame.font.Font('fonts/freesansbold.ttf', 60)
math_x = 620
math_y = 10
operator_1 = random.randint(1, 10)
operator_2 = random.randint(1, 10)
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
    operation = font_math_operation.render(str(operator_1)+ " x " + str(operator_2), True, (255, 255, 255)) 
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

# Lives
heart_img = pygame.image.load('images/heart.png')
lives_x = 10
lives_y = 10
number_lives = 5

def lives(x, y):
    for i in range(number_lives):
        screen.blit(heart_img, (x, y))
        x += 35



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
number_enemies = 5
monster_value = 0

for i in range(number_enemies):
    monster_img.append(pygame.image.load('images/monster.png'))
    monster_x.append(random.randint(0, 736))
    monster_y.append(random.randint(50, 150))
    monster_x_change.append(0)
    monster_y_change.append(0.2)
    monster_value = random.randint(0, 100)
    monster_values.append(monster_value)
    monster_resoult.append(font_math.render(str(monster_value), True, (153, 0, 0)))


def monster(x, y, i):
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
                    number_lives = 5
                    score_value = 0
                    you_loose = False
                    for i in range(number_enemies):
                        monster_y[i] = random.randint(50, 150)
                        monster_y_change[i] = 0.2

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
        for i in range(number_enemies):
            # Game over
            if monster_y[i] > 420 or number_lives == 0:
                for j in range(number_enemies):
                    monster_y[j] = 2000
                game_over_text()
                you_loose = True
                break

        for i in range(number_enemies):
            monster_y[i] += monster_y_change[i]
            
            # Collision
            collision = is_Collision(monster_x[i], monster_y[i], bullet_x, bullet_y)
            if collision:
                bullet_y = 480
                bullet_shoot = False
                if score_value == 30:
                    player_img = pygame.image.load('images/player2_icon.png')

                monster_x[i] = random.randint(0, 736)
                monster_y[i] = random.randint(50, 150)

                # Check if is the correct answer when collision
                if monster_values[i] == operator_1 * operator_2:
                    explosionSound = mixer.Sound("sounds/explosion.wav")
                    explosionSound.set_volume(5)
                    explosionSound.play()
                    next_math = True
                    # update the screen
                    score_value += 1
                    operator_1 = random.randint(1, 10)
                    operator_2 = random.randint(1, 10)
                    show_math(math_x, math_y)
                    monster_x = []
                    monster_y = []
                    for i in range (number_enemies):
                        monster_x.append(random.randint(0, 736))
                        monster_y.append(random.randint(50, 150))
                        monster_y_change[i] += .02
                else:
                    number_lives -= 1
                    explosionSound = mixer.Sound("sounds/incorrect.wav")
                    explosionSound.set_volume(5)
                    explosionSound.play()

            # Define if the resoult is correct
            if next_math:
                monster_resoult.insert(correct_answer_monster_pos, font_math.render(str(operator_1 * operator_2), True, (153, 0, 0)))
                monster_values.insert(correct_answer_monster_pos, operator_1*operator_2)

                # Increase the correct answer counter
                if correct_answer_monster_pos < number_enemies:
                    correct_answer_monster_pos += 1
                else:
                    correct_answer_monster_pos = 0
                    monster_resoult.insert(correct_answer_monster_pos, font_math.render(str(operator_1 * operator_2), True, (153, 0, 0)))
                    monster_values.insert(correct_answer_monster_pos, operator_1*operator_2)

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
        lives(lives_x, lives_y)
    else:
        pause_text()

        # END MOVEMENT..................................................................................................
    pygame.display.update()
