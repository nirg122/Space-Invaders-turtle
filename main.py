from turtle import *
import time
import random

screen = Screen()
screen.setup(1000, 1000)
screen.tracer(0)
screen.bgcolor('silver')
screen.title('Space Invaders')
# COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]

# _tick2_frame = 0
# _tick2_fps = 20000000  # real raw FPS
# _tick2_t0 = time.time()
# 
# def tick(fps=60):
#     global _tick2_frame, _tick2_fps, _tick2_t0
#     n = _tick2_fps / fps
#     _tick2_frame += n
#     while n > 0:
#         n -= 1
#     if time.time() - _tick2_t0 > 1:
#         _tick2_t0 = time.time()
#         _tick2_fps = _tick2_frame
#         _tick2_frame = 0


class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.shapesize(stretch_len=2.5, stretch_wid=0.7)
        self.color("black")
        self.penup()
        self.setpos((0, -350))
        self.vel = 15

    def Left(self):
        self.setx(self.xcor() - self.vel)

    def Right(self):
        self.setx(self.xcor() + self.vel)

class Enemy(Turtle):
    def __init__(self, row, column, color):
        super().__init__()
        self.row = row
        self.column = column
        self.shape("square")
        self.penup()
        self.shapesize(stretch_len=1, stretch_wid=1)
        self.color(color)
        self.setheading(0)

class EnemyGroup:
    def __init__(self):
        self.enemies = self.create_enemies(5, 10)

    def create_enemies(self, row, column):
        enemies_group = []
        for _row in range(row):
            for _column in range(column):
                if _row == 0:
                    enemy = Enemy(_row, _column, 'red')
                    enemy.setx(-200 + (_column * 50))
                    enemy.sety(400 - (_row * 50))
                    enemies_group.append(enemy)
                elif _row == 1:
                    enemy = Enemy(_row, _column, 'green')
                    enemy.setx(-200 + (_column * 50))
                    enemy.sety(400 - (_row * 50))
                    enemies_group.append(enemy)
                elif _row == 2:
                    enemy = Enemy(_row, _column, 'purple')
                    enemy.setx(-200 + (_column * 50))
                    enemy.sety(400 - (_row * 50))
                    enemies_group.append(enemy)
                elif _row == 3:
                    enemy = Enemy(_row, _column, 'brown')
                    enemy.setx(-200 + (_column * 50))
                    enemy.sety(400 - (_row * 50))
                    enemies_group.append(enemy)
                elif _row == 4:
                    enemy = Enemy(_row, _column, 'black')
                    enemy.setx(-200 + (_column * 50))
                    enemy.sety(400 - (_row * 50))
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


    def fire_bullet(self):
        # self.sety(self.ycor() + self.vel)
        # self.forward(self.vel)
        global bullet_state
        if bullet_state == 'ready':
            bullet_state = 'fire'
            self.showturtle()
            y = player.ycor() + 5
            self.goto(player.xcor(), y)

def isCollision(t1, t2):
    if t1.distance(t2) < 15:
        return True

enemies = EnemyGroup()
player = Player()
players_bullet = Bullet()
bullet_state = 'ready'

screen.listen()
screen.onkeypress(player.Left, 'Left')
screen.onkeypress(player.Right, 'Right')
screen.onkey(players_bullet.fire_bullet, 'space')

game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(1/25)

    for enemy in enemies.enemies:
        # Move the enemy
        enemy.fd(10)

    for enemy in enemies.enemies:

        # Move the enemy back and down
        if enemy.xcor() >= 480:
            for e in enemies.enemies:
                e.seth(180)
                e.sety(e.ycor() - 7)

        elif enemy.xcor() <= -480:
            for e in enemies.enemies:
                e.seth(0)
                e.sety(e.ycor() - 7)

        # Check collision with bullet
        if isCollision(players_bullet, enemy) and enemy.isvisible():
            players_bullet.hideturtle()
            players_bullet.setposition(player.xcor(), -600)
            bullet_state = 'ready'
            enemy.setposition(-200, -250)
            enemy.hideturtle()
        # Check collision with player
        if isCollision(player, enemy) and enemy.isvisible():
            print('Game Over')
            game_is_on = False

    # Move Players Bullet
    if bullet_state == 'fire':
        y = players_bullet.ycor()
        y += players_bullet.vel
        players_bullet.sety(y)

    if players_bullet.ycor() >= 490:
        players_bullet.hideturtle()
        bullet_state = 'ready'

