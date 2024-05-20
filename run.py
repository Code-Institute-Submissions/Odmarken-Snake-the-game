import os
import random
import time
import sys
import tty
import termios
import select

# Constants
FRAME_SIZE_X = 40
FRAME_SIZE_Y = 20
HIGH_SCORE_FILE = "highscore.txt"
INITIAL_SPEED = 0.1

# Variables
direction = "RIGHT"
head_pos = [10, 5]
snake_body = [[10, 5]]
food_pos = [random.randrange(1, FRAME_SIZE_X), random.randrange(1, FRAME_SIZE_Y)]
food_spawn = True
score = 0
speed = INITIAL_SPEED
high_score = 0

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

# High score functions
def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read().strip())
    return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))

# Game setup functions
def init_vars():
    global head_pos, snake_body, food_pos, food_spawn, score, direction, speed, high_score
    direction = "RIGHT"
    head_pos = [10, 5]
    snake_body = [[10, 5]]
    food_pos = [random.randrange(1, FRAME_SIZE_X), random.randrange(1, FRAME_SIZE_Y)]
    food_spawn = True
    score = 0
    speed = INITIAL_SPEED
    high_score = load_high_score()
    print(f'Initial food position: {food_pos}')

# Game rendering
def draw_game():
    os.system('clear')
    print("Press W, A, S, D to move the snake. Press Q to quit.")
    print("Press P to make the game faster, O to make it slower.")
    print(f"Score: {score}  High Score: {high_score}")
    for y in range(FRAME_SIZE_Y):
        for x in range(FRAME_SIZE_X):
            if [x, y] == head_pos:
                print('O', end='')
            elif [x, y] in snake_body:
                print('o', end='')
            elif [x, y] == food_pos:
                print('*', end='')
            else:
                print(' ', end='')
        print()

# Game logic
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
        head_pos[0] = FRAME_SIZE_X - 1
    elif head_pos[0] >= FRAME_SIZE_X:
        head_pos[0] = 0
    if head_pos[1] < 0:
        head_pos[1] = FRAME_SIZE_Y - 1
    elif head_pos[1] >= FRAME_SIZE_Y:
        head_pos[1] = 0

    snake_body.insert(0, list(head_pos))
    if head_pos == food_pos:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = [random.randrange(1, FRAME_SIZE_X), random.randrange(1, FRAME_SIZE_Y)]
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

# Main execution
if __name__ == "__main__":
    init_vars()
    print("Press W, A, S, D to move the snake. Press Q to quit.")
    print("Press P to make the game faster, O to make it slower.")
    print("Press any key to start the game...")
    get_key()  # Wait for the user to press a key to start the game
    hide_cursor()
    try:
        main_game_loop()
    finally:
        show_cursor()
        print("\nCursor shown again. Exiting game.")
