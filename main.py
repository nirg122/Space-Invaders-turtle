from turtle import *
import time
from random import choice
import platform
import os
import pygame
try:
    if platform.system() == "Windows":
        import winsound
except:
    print('No Sound on Windows.')


class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.shapesize(stretch_len=2.5, stretch_wid=0.7)
        self.color("green")
        self.penup()
        self.setpos((0, -210))
        self.life = 3
        self.speed = 0

    def move_left(self):
        self.speed = -7

    def move_right(self):
        self.speed = 7

    def move_player(self):
        x = player.xcor()
        x += player.speed
        if x < -220:
            x = -220
        if x > 215:
            x = 215
        self.setx(x)


class Enemy(Turtle):
    def __init__(self, row, column):
        super().__init__()
        self.row = row
        self.column = column
        self.shape("images/alien.gif")
        self.penup()
        self.shapesize(stretch_len=1, stretch_wid=1)
        self.setheading(0)

    def shoot(self, x, y):
        enemy_bullet = Bullet()
        enemy_bullet.color('red')
        enemy_bullet.setposition(x, y)
        enemy_bullet_list.append(enemy_bullet)
        play_sound('sounds/shoot2.wav')


class EnemyGroup:
    def __init__(self):
        self.enemies = self.create_enemies(5, 8)

    def create_enemies(self, row, column):
        enemies_group = []
        for _row in range(row):
            for _column in range(column):
                if _row == 0:
                    enemy = Enemy(_row, _column)
                    enemy.setx(-200 + (_column * 50))
                    enemy.sety(200 - (_row * 50))
                    enemies_group.append(enemy)
                elif _row == 1:
                    enemy = Enemy(_row, _column)
                    enemy.setx(-200 + (_column * 50))
                    enemy.sety(200 - (_row * 50))
                    enemies_group.append(enemy)
                elif _row == 2:
                    enemy = Enemy(_row, _column)
                    enemy.setx(-200 + (_column * 50))
                    enemy.sety(200 - (_row * 50))
                    enemies_group.append(enemy)
                elif _row == 3:
                    enemy = Enemy(_row, _column)
                    enemy.setx(-200 + (_column * 50))
                    enemy.sety(200 - (_row * 50))
                    enemies_group.append(enemy)
                elif _row == 4:
                    enemy = Enemy(_row, _column)
                    enemy.setx(-200 + (_column * 50))
                    enemy.sety(200 - (_row * 50))
                    enemies_group.append(enemy)
        return enemies_group


class Bullet(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.shapesize(stretch_len=1, stretch_wid=0.1)
        self.penup()
        self.color("yellow")
        self.setpos(player.xcor(), player.ycor())
        self.setheading(90)
        self.vel = 20
        self.speed(0)
        self.hideturtle()

    def fire_bullet(self, a=None, b=None):
        # self.sety(self.ycor() + self.vel)
        # self.forward(self.vel)
        global bullet_state
        if bullet_state == 'ready':
            bullet_state = 'fire'
            self.showturtle()
            y = player.ycor() + 5
            self.goto(player.xcor(), y)
            play_sound('sounds/shoot.wav')


def is_collision(t1, t2):
    if t1.distance(t2) < 20:
        return True


def update_score():
    score_pen.penup()
    score_pen.hideturtle()
    score_pen.setposition(-240, 230)
    score_pen.color('red')
    score_pen.write(f'Score:{score}', False, align='Left', font=('Arial', 10, 'normal'))


def update_lives():
    life_pen.penup()
    life_pen.hideturtle()
    life_pen.setposition(170, 230)
    life_pen.color('red')
    life_pen.write(f'Lives:{"❤" * player.life}', False, align='Left', font=('Arial', 10, 'normal'))


def game_over_sequence():
    game_over = Turtle()
    game_over.hideturtle()
    game_over.penup()
    game_over.setposition(-80, 0)
    game_over.color('red')
    game_over.write(f'Game Over', False, align='Left', font=('Arial', 20, 'bold'))


def winning_sequence():
    winner = Turtle()
    winner.hideturtle()
    winner.penup()
    winner.setposition(-80, 0)
    winner.color('green')
    winner.write(f"You've Won!", False, align='Left', font=('Arial', 20, 'bold'))


def play_sound(sound_file, bg=0):
    if platform.system() == "Windows":
        winsound.PlaySound(sound_file, winsound.SND_ASYNC | winsound.SND_ALIAS)
    elif platform.system() == "Mac":
        os.system(f"afplay {sound_file}")
    elif platform.system() == "Linux":
        os.system(f"aplay -q {sound_file}")
    if bg == 1:
        pygame.mixer.init()
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()


# Screen Setup
screen = Screen()
screen.setup(500, 500)
screen.tracer(0)
screen.title('Space Invaders')
screen.register_shape("images/alien.gif")
screen.bgpic('images/background.gif')
enemies = EnemyGroup()
player = Player()
players_bullet = Bullet()
bullet_state = 'ready'
enemy_bullet_list = []
score = 0
score_pen = Turtle()
life_pen = Turtle()

# Clock setup
clock = 0
clock_now = 0

# Screen setup
screen.listen()
screen.onkeypress(player.move_left, 'a')
screen.onkeypress(player.move_right, 'd')
screen.onkeypress(player.move_left, 'Left')
screen.onkeypress(player.move_right, 'Right')
screen.onkeypress(players_bullet.fire_bullet, "space")
screen.onclick(players_bullet.fire_bullet)

# Play background music
play_sound('sounds/bgm.wav', 1)

game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(1 / 60)
    update_score()
    update_lives()
    player.move_player()
    clock += 1

    if clock % 10 == 0:
        for enemy in enemies.enemies:
            # Move the enemy
            enemy.fd(10)

    # make enemy_shoot
    visible_enemies = []
    if clock % 60 == 0:
        for enemy in enemies.enemies:
            if enemy.isvisible():
                visible_enemies.append(enemy)

        random_enemy = choice(visible_enemies)
        random_enemy.shoot(random_enemy.xcor(), random_enemy.ycor())
    visible_enemies.clear()

    for enemy in enemies.enemies:
        # Move the enemy back and down
        if enemy.xcor() >= 215 and enemy.isvisible():
            for e in enemies.enemies:
                e.seth(180)
                e.fd(10)
                e.sety(e.ycor() - 7)

        elif enemy.xcor() <= -220 and enemy.isvisible():
            for e in enemies.enemies:
                e.seth(0)
                e.fd(10)
                e.sety(e.ycor() - 7)

        # Check collision of enemy with bullet
        if is_collision(players_bullet, enemy) and enemy.isvisible():
            players_bullet.hideturtle()
            players_bullet.setposition(player.xcor(), -600)
            bullet_state = 'ready'
            enemy.setposition(-200, -250)
            enemy.hideturtle()
            play_sound('sounds/invaderkilled.wav')

            # Update Score
            score += 1
            score_pen.clear()
            update_score()
        # Check collision with player
        if is_collision(player, enemy) and enemy.isvisible():
            play_sound('sounds/shipexplosion.wav')
            game_over_sequence()
            game_is_on = False

    if enemy_bullet_list:
        for bullet in enemy_bullet_list:
            # Move enemy bullet
            bullet.showturtle()

            if clock % 2 == 0 and bullet.isvisible():
                y = bullet.ycor()
                y -= bullet.vel
                bullet.sety(y)
            # Check collision of enemy bullet with player
            if is_collision(bullet, player) and bullet.isvisible() and player.isvisible():
                bullet.hideturtle()
                player.hideturtle()
                play_sound('sounds/shipexplosion.wav')
                player.life -= 1
                life_pen.clear()
                update_lives()
                clock_now = clock
            # Check enemy bullet collision with bottom
            if bullet.ycor() <= -235:
                bullet.hideturtle()

    if clock - clock_now > 15:
        player.showturtle()

    # Move player's bullet
    if bullet_state == 'fire':
        y = players_bullet.ycor()
        y += players_bullet.vel
        players_bullet.sety(y)

    if players_bullet.ycor() >= 240:
        players_bullet.hideturtle()
        bullet_state = 'ready'

    if player.life == 0:
        game_over_sequence()
        game_is_on = False

    if score == 40:
        winning_sequence()
        game_is_on = False

screen.exitonclick()
