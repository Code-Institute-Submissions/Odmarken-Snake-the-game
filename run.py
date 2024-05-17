import os
import random
import time
import sys
import tty
import termios
import select

# Terminal settings 
def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        if select.select([sys.stdin], [], [], 0.1)[0]:
            ch = sys.stdin.read(1)
        else:
            ch = None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# Game settings
frame_size_x = 40
frame_size_y = 20

# Variables
def init_vars():
    global head_pos, snake_body, food_pos, food_spawn, score, direction, change_to
    direction = "RIGHT"
    change_to = direction
    head_pos = [10, 5]
    snake_body = [[10, 5]]
    food_pos = [random.randrange(1, frame_size_x), random.randrange(1, frame_size_y)]
    food_spawn = True
    score = 0
    print(f'Initial food position: {food_pos}')

def draw_game():
    os.system('clear')
    print("Press W, A, S, D to move the snake. Press Q to quit.")
    print(f"Score: {score}")
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

# Game button/directions
def update_game():
    global food_spawn, score, food_pos, direction

    # Change direction
    if change_to == "UP" and direction != "DOWN":
        direction = "UP"
    if change_to == "DOWN" and direction != "UP":
        direction = "DOWN"
    if change_to == "LEFT" and direction != "RIGHT":
        direction = "LEFT"
    if change_to == "RIGHT" and direction != "LEFT":
        direction = "RIGHT"

    if direction == "UP":
        head_pos[1] -= 1
    elif direction == "DOWN":
        head_pos[1] += 1
    elif direction == "LEFT":
        head_pos[0] -= 1
    elif direction == "RIGHT":
        head_pos[0] += 1

    # Wrap around
    if head_pos[0] < 0:
        head_pos[0] = frame_size_x - 1
    elif head_pos[0] >= frame_size_x:
        head_pos[0] = 0
    if head_pos[1] < 0:
        head_pos[1] = frame_size_y - 1
    elif head_pos[1] >= frame_size_y:
        head_pos[1] = 0

    snake_body.insert(0, list(head_pos))
    if head_pos == food_pos:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = [random.randrange(1, frame_size_x), random.randrange(1, frame_size_y)]
        food_spawn = True

    for block in snake_body[1:]:
        if head_pos == block:
            return False
    return True

# Initialize variables
init_vars()

# Main game loop
while True:
    draw_game()
    key = get_key()
    if key:
        key = key.lower()
        if key == 'w':
            change_to = "UP"
        elif key == 's':
            change_to = "DOWN"
        elif key == 'a':
            change_to = "LEFT"
        elif key == 'd':
            change_to = "RIGHT"
        elif key == 'q':
            break

    if not update_game():
        print("Game Over!")
        break

    time.sleep(0.1)
