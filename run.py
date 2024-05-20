import os
import random
import time
import sys
import tty
import termios
import select

# Constants for game settings
FRAME_SIZE_X = 40
FRAME_SIZE_Y = 20
HIGH_SCORE_FILE = "highscore.txt"
INITIAL_SPEED = 0.05  # Double the normal speed

# Initial variables for the game state
direction = "RIGHT"
head_pos = [10, 5]
snake_body = [[10, 5]]
food_pos = [
    random.randrange(1, FRAME_SIZE_X),
    random.randrange(1, FRAME_SIZE_Y)
]
food_spawn = True
score = 0
speed = INITIAL_SPEED
high_score = 0


def get_key():
    """
    Get a single key press from the user.
    This function sets the terminal to raw mode to capture a single key press
    without waiting for a newline.
    """
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


def hide_cursor():
    """
    Hide the cursor in the terminal.
    This function uses ANSI escape codes to hide the cursor.
    """
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()


def show_cursor():
    """
    Show the cursor in the terminal.
    This function uses ANSI escape codes to show the cursor.
    """
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()


def load_high_score():
    """
    Load the high score from local.
    This function reads the high score from the specified file if it exists.
    """
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read().strip())
    return 0


def save_high_score(score):
    """
    Save the high score to local.
    This function writes the current high score to the specified file.
    """
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))


def init_vars():
    """
    Initialize game variables.
    This function sets up the initial state of the game.
    """
    global head_pos, snake_body, food_pos, food_spawn, score, direction, speed
    global high_score
    direction = "RIGHT"
    head_pos = [10, 5]
    snake_body = [[10, 5]]
    food_pos = [
        random.randrange(1, FRAME_SIZE_X), 
        random.randrange(1, FRAME_SIZE_Y)
    ]
    food_spawn = True
    score = 0
    speed = INITIAL_SPEED
    high_score = load_high_score()
    print(f'Initial food position: {food_pos}')


def draw_game():
    """
    Render the game state in the terminal.
    This function clears the terminal and draws the current state of the game.
    """
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


def update_game():
    """
    Update the game state.
    This function moves the snake, checks for collisions, updates the score,
    and manages food spawning.
    """
    global food_spawn, score, food_pos, direction, high_score

    if direction == "UP":
        head_pos[1] -= 1
    elif direction == "DOWN":
        head_pos[1] += 1
    elif direction == "LEFT":
        head_pos[0] -= 1
    elif direction == "RIGHT":
        head_pos[0] += 1

    # Wrap around the edges of the screen
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
        food_pos = [
            random.randrange(1, FRAME_SIZE_X),
            random.randrange(1, FRAME_SIZE_Y)
        ]
        food_spawn = True

    # Check for collision with self
    for block in snake_body[1:]:
        if head_pos == block:
            return False

    # Update high score if needed
    if score > high_score:
        high_score = score
        save_high_score(high_score)

    return True


def handle_input():
    """
    Handle user input.
    This function captures user input and updates the direction and speed of
    the snake.
    """
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
    """
    Main game loop.
    This function runs the main loop of the game, handling input, updating the
    game state, and rendering the game.
    """
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
