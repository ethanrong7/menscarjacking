from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
import time
import json
import sys
import keyboard as pressed
from bidict import bidict

from multiprocessing import Process
from threading import Event
import signal

import asyncio
import os

blocker = Event()
wait_until_pressed_event = Event()

async def wait_until_pressed(key):
    global is_pressed
    is_pressed = False
    wait_until_pressed_event.clear()

    def toggle():
        wait_until_pressed_event.set()
        global is_pressed
        is_pressed = True

    cb = pressed.add_hotkey(key, toggle)

    while not is_pressed and not wait_until_pressed_event.is_set():
        wait_until_pressed_event.wait(0.5)

    pressed.remove_hotkey(cb)

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

mem = {}

def keyboard_press(key):
    print(key)
    keyboard.press(key)
    mem[key] = True

def keyboard_release(key):
    keyboard.release(key)
    mem[key] = False

def close():
    for key in mem.keys():
        keyboard.release(key)
    mem.clear()

with open('key_mapping.json', 'r') as file:
    key_mapping_data = json.load(file)

map = bidict(key_mapping_data)

def return_key(key):
    if key in map.values():
        return map.inv[key]
    else:
        return key

global instruction_index
global play_count
global number_of_instructions

global is_running

instruction_index = 0

play_count = 0
number_of_instructions = len(data)

is_running = False
    
async def instance():
    global play_count
    global number_of_instructions

    global is_running
    global ii_temp

    global instruction_index

    print(instruction_index)

    print("Press '*' to start")
    print("Press '*' again to pause")
    print("Press 'Shift+Escape' to exit")
    await wait_until_pressed("*")
    print("Starting in 1...")
    blocker.wait(1)

    is_running = True

    while play_count < number_of_plays and not blocker.is_set():
        while instruction_index < number_of_instructions and not blocker.is_set():
            print(f"ii: {instruction_index}")
            obj = data[instruction_index]

            action, _time= obj['action'], obj['_time']
            try:
                next_movement = data[instruction_index+1]['_time']
                pause_time = next_movement - _time
            except IndexError as e:
                pause_time = 0
            if action == "pressed_key" or action == "released_key":
                key = special_keys[return_key(obj['key'])] if return_key(obj['key']) in special_keys else return_key(obj['key'])
                print("action: {0}, time: {1}, key: {2}".format(action, _time, str(key)))
                if action == "pressed_key":
                    keyboard_press(key)
                else:
                    keyboard_release(key)
                blocker.wait(pause_time)

            instruction_index += 1

        instruction_index = 0
        play_count += 1

def schedule_task():
    global instruction_index

    def on_esc():
        global is_running
        if is_running:
            close()
            blocker.set()
            is_running = False
            os.kill(os.getpid(), signal.SIGTERM)

    pressed.add_hotkey("*", on_esc)
    asyncio.run(instance())

p = None

def on_esc():
    global is_running
    if p != None:
        close()
        p.kill()
    os.kill(os.getpid(), signal.SIGTERM)

pressed.add_hotkey("shift+esc", on_esc)
    

if __name__ == "__main__":
    while True:
        blocker.clear()
        p = Process(target=schedule_task)
        p.start()
        p.join()