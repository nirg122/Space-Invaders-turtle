from turtle import *
import time
import random

screen = Screen()
screen.setup(500, 500)
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
        self.setpos((0, -175))
        self.vel = 15

    def Left(self):
        if self.xcor() >= -220:
            self.setx(self.xcor() - self.vel)

    def Right(self):
        if self.xcor() <= 210:
            self.setx(self.xcor() + self.vel)


class Enemy(Turtle):
    def __init__(self, row, column, color):
        super().__init__()
        self.row = row
        self.column = column
        self.shape("square")
        self.penup()
        self.shapesize(stretch_len=0.7, stretch_wid=0.7)
        self.color(color)
        self.setheading(0)


class EnemyGroup:
    def __init__(self):
        self.enemies = self.create_enemies(3, 5)

    def create_enemies(self, row, column):
        enemies_group = []
        for _row in range(row):
            for _column in range(column):
                if _row == 0:
                    enemy = Enemy(_row, _column, 'red')
                    enemy.setx(-200 + (_column * 50))
                    enemy.sety(200 - (_row * 50))
                    enemies_group.append(enemy)
                elif _row == 1:
                    enemy = Enemy(_row, _column, 'green')
                    enemy.setx(-200 + (_column * 50))
                    enemy.sety(200 - (_row * 50))
                    enemies_group.append(enemy)
                elif _row == 2:
                    enemy = Enemy(_row, _column, 'purple')
                    enemy.setx(-200 + (_column * 50))
                    enemy.sety(200 - (_row * 50))
                    enemies_group.append(enemy)
                # elif _row == 3:
                #     enemy = Enemy(_row, _column, 'brown')
                #     enemy.setx(-200 + (_column * 50))
                #     enemy.sety(400 - (_row * 50))
                #     enemies_group.append(enemy)
                # elif _row == 4:
                #     enemy = Enemy(_row, _column, 'black')
                #     enemy.setx(-200 + (_column * 50))
                #     enemy.sety(400 - (_row * 50))
                #     enemies_group.append(enemy)
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

    def fire_bullet(self, a, b):
        # self.sety(self.ycor() + self.vel)
        # self.forward(self.vel)
        global bullet_state
        if bullet_state == 'ready':
            bullet_state = 'fire'
            self.showturtle()
            y = player.ycor() + 5
            self.goto(player.xcor(), y)


def is_collision(t1, t2):
    if t1.distance(t2) < 15:
        return True


def update_score():
    score_pen.penup()
    score_pen.hideturtle()
    score_pen.setposition(-240, 230)
    score_pen.write(f'Score:{score}', False, align='Left', font=('Arial', 10, 'normal'))


enemies = EnemyGroup()
player = Player()
players_bullet = Bullet()
bullet_state = 'ready'

score = 0
score_pen = Turtle()

clock = 0
screen.listen()
screen.onkeypress(player.Left, 'a')
screen.onkeypress(player.Right, 'd')
screen.onclick(players_bullet.fire_bullet)

game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(1 / 60)
    update_score()
    clock += 1

    if clock % 30 == 0:
        for enemy in enemies.enemies:
            # Move the enemy
            enemy.fd(10)

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
            # Update Score
            score += 1
            score_pen.clear()
            update_score()
        # Check collision with player
        if is_collision(player, enemy) and enemy.isvisible():
            print('Game Over')
            game_is_on = False

    # Move Players Bullet
    if bullet_state == 'fire':
        y = players_bullet.ycor()
        y += players_bullet.vel
        players_bullet.sety(y)

    if players_bullet.ycor() >= 240:
        players_bullet.hideturtle()
        bullet_state = 'ready'
