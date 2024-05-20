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
        tty.setraw(fd)
        if select.select([sys.stdin], [], [], 0.1)[0]:
            ch = sys.stdin.read(1)
        else:
            ch = None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# Cursor visibility functions

def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

# Game settings

frame_size_x = 40
frame_size_y = 20
high_score_file = "highscore.txt"

# Variables

def init_vars():
    global head_pos, snake_body, food_pos, food_spawn, score, direction, speed, high_score
    direction = "RIGHT"
    head_pos = [10, 5]
    snake_body = [[10, 5]]
    food_pos = [random.randrange(1, frame_size_x), random.randrange(1, frame_size_y)]
    food_spawn = True
    score = 0
    speed = 0.1
    high_score = load_high_score()
    print(f'Initial food position: {food_pos}')

# High score functions

def load_high_score():
    if os.path.exists(high_score_file):
        with open(high_score_file, "r") as file:
            return int(file.read().strip())
    return 0

def save_high_score(score):
    with open(high_score_file, "w") as file:
        file.write(str(score))

# Game info 

def draw_game():
    os.system('clear')
    print("Press W, A, S, D to move the snake. Press Q to quit.")
    print("Press P to make the game faster, O to make it slower.")
    print(f"Score: {score}  High Score: {high_score}")
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
    global food_spawn, score, food_pos, direction, high_score

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

    if score > high_score:
        high_score = score
        save_high_score(high_score)

    return True

def handle_input():
    global direction, speed
    key = get_key()
    if key:
        key = key.lower()
        if key == 'w' and direction != "DOWN":
            direction = "UP"
        elif key == 's' and direction != "UP":
            direction = "DOWN"
        elif key == 'a' and direction != "RIGHT":
            direction = "LEFT"
        elif key == 'd' and direction != "LEFT":
            direction = "RIGHT"
        elif key == 'q':
            return False
        elif key == 'p':
            speed = max(0.01, speed - 0.01)  # Increase speed, minimum 0.01
        elif key == 'o':
            speed += 0.01  # Decrease speed
    return True

def main_game_loop():
    while True:
        draw_game()
        if not handle_input():
            break
        if not update_game():
            print("Game Over!")
            break
        time.sleep(speed)

# Initialize variables

init_vars()

# Print info text

print("Press W, A, S, D to move the snake. Press Q to quit.")
print("Press P to make the game faster, O to make it slower.")
print("Press any key to start the game...")
get_key()  

# Hide cursor

hide_cursor()

# Main game loop

try:
    main_game_loop()
finally:
    # Show cursor again

    show_cursor()
    print("\nCursor shown again. Exiting game.")
