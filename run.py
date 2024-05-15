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
  
