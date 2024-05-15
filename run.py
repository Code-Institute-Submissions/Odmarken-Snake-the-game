import os
import random
import time
import sys
import tty
import termios

# Terminal settings for the game

def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

    # Game settings
frame_size_x = 40
frame_size_y = 20
  
  # Variables
def init_vars():
    global head_pos, snake_body, food_pos, food_spawn, score, direction
    direction = "RIGHT"
    head_pos = [10, 5]
    snake_body = [[10, 5]]
     food_pos = [random.randrange(1, frame_size_x), random.randrange(1, frame_size_y)]
    food_spawn = True
    score = 0
    print(f'Initial food position: {food_pos}')  

    def draw_game():
    os.system('clear')
    for y in range(frame_size_y):
        for x in range(frame_size_x):
            if [x, y] == head_pos:
                print('O', end='')
            elif [x, y] in snake_body:
                print('o', end='')
            elif [x, y] == food_pos:
                print('*', end='')
            else:
                print(' ', end='')
        print()
    print(f'Score: {score}')

    #updates

    def update_game():
    global food_spawn, score, food_pos  

    if direction == "UP":
        head_pos[1] -= 1
    elif direction == "DON":
        head_pos[1] += 1
    elif direction == "LEFT":
        head_pos[0] -= 1
    elif direction == "RIGHT":
        head_pos[0] += 1


