from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
import time
import json
import sys
import keyboard as pressed
from bidict import bidict
import threading

n = len(sys.argv)

if n < 3:
    exit("Takes two arguments - name of recording to play and number of times to play it")

if n > 3:
    exit("Only takes two argument - name of recording to play and number of times to play it")

if n == 3:
    name_of_recording = "data/" + str(sys.argv[1]) +'.txt'
    number_of_plays = int(sys.argv[2])

with open(name_of_recording) as json_file:
    data = json.load(json_file)

special_keys = {"Key.shift": Key.shift, "Key.tab": Key.tab, "Key.caps_lock": Key.caps_lock, "Key.ctrl": Key.ctrl, "Key.alt": Key.alt, "Key.cmd": Key.cmd, "Key.cmd_r": Key.cmd_r, "Key.alt_r": Key.alt_r, "Key.alt_l": Key.alt_r, "Key.ctrl_r": Key.ctrl_r, "Key.shift_r": Key.shift_r, "Key.enter": Key.enter, "Key.backspace": Key.backspace, "Key.f19": Key.f19, "Key.f18": Key.f18, "Key.f17": Key.f17, "Key.f16": Key.f16, "Key.f15": Key.f15, "Key.f14": Key.f14, "Key.f13": Key.f13, "Key.media_volume_up": Key.media_volume_up, "Key.media_volume_down": Key.media_volume_down, "Key.media_volume_mute": Key.media_volume_mute, "Key.media_play_pause": Key.media_play_pause, "Key.f6": Key.f6, "Key.f5": Key.f5, "Key.right": Key.right, "Key.down": Key.down, "Key.left": Key.left, "Key.up": Key.up, "Key.page_up": Key.page_up, "Key.page_down": Key.page_down, "Key.home": Key.home, "Key.end": Key.end, "Key.delete": Key.delete, "Key.space": Key.space, "Key.ctrl_l": Key.ctrl_l}

mouse = MouseController()
keyboard = KeyboardController()

program_running = True
paused = False

with open('key_mapping.json', 'r') as file:
    key_mapping_data = json.load(file)

map = bidict(key_mapping_data)

def toggle_pause():
    global paused
    paused = not paused

def return_key(key):
    if key in map.values():
        return map.inv[key]
    else:
        return key

print("Program is starting soon in 3 seconds...")
time.sleep(1)
print("Program is starting soon in 2 seconds...")
time.sleep(1)
print("Program is starting soon in 1 seconds...")
time.sleep(1)

while program_running:
    for loop in range(number_of_plays):
        for index, obj in enumerate(data):
            if pressed.is_pressed('F1'):
                    pressed.unhook_all()
                    sys.exit(0)
            if pressed.is_pressed('F2'):
                paused = True
                print(f"paused: {paused}")
            if pressed.is_pressed('F3'):
                paused = False
                print(f"resumed: {paused}")
            if not paused:
                # if index == 1:
                #     continue
                action, _time= obj['action'], obj['_time']
                try:
                    next_movement = data[index+1]['_time']
                    pause_time = next_movement - _time
                except IndexError as e:
                    pause_time = 0
                if action == "pressed_key" or action == "released_key":
                    key = special_keys[return_key(obj['key'])] if return_key(obj['key']) in special_keys else return_key(obj['key'])
                    print("action: {0}, time: {1}, key: {2}".format(action, _time, str(key)))
                    if action == "pressed_key":
                        keyboard.press(key)
                    else:
                        keyboard.release(key)
                    time.sleep(pause_time)


