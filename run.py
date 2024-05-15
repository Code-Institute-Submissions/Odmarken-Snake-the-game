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
