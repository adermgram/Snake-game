from turtle import Screen
from snake import Snake
import threading
from food import Food
from scoreboard import Scoreboard
from playsound import playsound
import time

# Constants
FOOD_DISTANCE_THRESHOLD = 15
TAIL_COLLISION_DISTANCE_THRESHOLD = 10
WALL_COLLISION_X = 280
WALL_COLLISION_Y = 280

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Adam's snake game")
screen.cv._rootwindow.resizable(False, False)
screen.tracer(0)

snake = Snake()
food = Food()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(fun=snake.up, key="Up")
screen.onkey(fun=snake.down, key="Down")
screen.onkey(fun=snake.left, key="Left")
screen.onkey(fun=snake.right, key="Right")


def play_sound(sound_file):
    playsound(sound_file)


def play_eat_sound():
    threading.Thread(target=play_sound, args=('eatsound.mp3',)).start()


def play_die_sound():
    threading.Thread(target=play_sound, args=('diesound.mp3',)).start()
    time.sleep(2)


def check_collision_with_food():
    if snake.head.distance(food) < FOOD_DISTANCE_THRESHOLD:
        play_eat_sound()
        food.refresh()
        snake.extend()
        scoreboard.increase_score()


def check_collision_with_wall():
    if (
        snake.head.xcor() > WALL_COLLISION_X
        or snake.head.xcor() < -WALL_COLLISION_X
        or snake.head.ycor() > WALL_COLLISION_Y
        or snake.head.ycor() < -WALL_COLLISION_Y
    ):
        play_die_sound()
        scoreboard.reset()
        snake.reset()


def check_collision_with_tail():
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < TAIL_COLLISION_DISTANCE_THRESHOLD:
            play_die_sound()
            scoreboard.reset()
            snake.reset()


def game_loop():
    game_is_on = True
    while game_is_on:
        screen.update()
        time.sleep(0.1)

        snake.move()

        check_collision_with_food()
        check_collision_with_wall()
        check_collision_with_tail()


game_loop()
screen.exitonclick()
