from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
import time
import json
import sys
import keyboard as pressed
from bidict import bidict
import threading

keyboard = KeyboardController()

time.sleep(1)
keyboard.press(Key.ctrl)
time.sleep(1)
keyboard.release(Key.ctrl)