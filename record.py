from pynput import mouse
from pynput import keyboard
import time
import json
from bidict import bidict
import sys

n = len(sys.argv)

if n < 2:
    exit("Takes a compulsory argument - name of recording, and optional argument - record-all")

if n > 3:
    exit("Only takes two arguments - name of recording and (optional) record-all")

if n == 2:
    name_of_recording = str(sys.argv[1])
    record_all = False
if n == 3:
    if str(sys.argv[2]) != "record-all":
        exit("The second argument given must be 'record-all', otherwise only pass the name of recording as a parameter")
    name_of_recording = str(sys.argv[1])
    record_all = True

print("To end the recording, press f4 and then a mouse left click to finish the recording macro")

storage = []
count = 0

with open('key_mapping.json', 'r') as file:
    key_mapping_data = json.load(file)

map = bidict(key_mapping_data)

start_time = time.time()

def return_key(key):
    if key in map:
        return map[key]
    else:
        return key


def on_press(key):
    try:
        json_object = {'action':'pressed_key', 'key':return_key(key.char), '_time': time.time() - start_time}
    except AttributeError:
        if key == keyboard.Key.f4:
            return False
        json_object = {'action':'pressed_key', 'key':return_key(str(key)), '_time': time.time() - start_time}
    storage.append(json_object)

def on_release(key):
    try:
        json_object = {'action':'released_key', 'key':return_key(key.char), '_time': time.time() - start_time}
    except AttributeError:
        json_object = {'action':'released_key', 'key':return_key(str(key)), '_time': time.time() - start_time}
    storage.append(json_object)
        

def on_move(x, y):
    if (record_all) == True:
        if len(storage) >= 1:
            if storage[-1]['action'] != "moved":
                json_object = {'action':'moved', 'x':x, 'y':y, '_time':time.time() - start_time}
                storage.append(json_object)
            elif storage[-1]['action'] == "moved" and time.time() - start_time - storage[-1]['_time'] > 0.02:
                json_object = {'action':'moved', 'x':x, 'y':y, '_time':time.time() - start_time}
                storage.append(json_object)
        else:
            json_object = {'action':'moved', 'x':x, 'y':y, '_time':time.time() - start_time}
            storage.append(json_object)
    else:
        if len(storage) >= 1:
            if (storage[-1]['action'] == "pressed" and storage[-1]['button'] == 'Button.left') or (storage[-1]['action'] == "moved" and time.time() - start_time - storage[-1]['_time'] > 0.02):
                json_object = {'action':'moved', 'x':x, 'y':y, '_time':time.time() - start_time}
                storage.append(json_object)

# def on_click(x, y, button, pressed):
#     json_object = {'action':'pressed' if pressed else 'released', 'button':str(button), 'x':x, 'y':y, '_time':time.time()}
#     storage.append(json_object)
#     if len(storage) > 1:
#         if storage[-1]['action'] == 'released' and storage[-1]['button'] == 'Button.left' and storage[-1]['_time'] - storage[-2]['_time'] > 2:
#             with open('data/{}.txt'.format(name_of_recording), 'w') as outfile:
#                 json.dump(storage, outfile)
#             return False

def on_click(x, y, button, pressed):
    json_object = {'action':'pressed' if pressed else 'released', 'button':str(button), 'x':x, 'y':y, '_time':time.time() - start_time}
    storage.append(json_object)
    if len(storage) > 1:
        if storage[-1]['action'] == 'released' and storage[-1]['button'] == 'Button.left':
            with open('data/{}.txt'.format(name_of_recording), 'w') as outfile:
                json.dump(storage, outfile)
            return False


def on_scroll(x, y, dx, dy):
    json_object = {'action': 'scroll', 'vertical_direction': int(dy), 'horizontal_direction': int(dx), 'x':x, 'y':y, '_time': time.time() - start_time}
    storage.append(json_object)


# Collect events from keyboard until esc
# Collect events from mouse until scroll
keyboard_listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)

mouse_listener = mouse.Listener(
        on_click=on_click)

# print("Program is starting soon in 10 seconds...")
# time.sleep(7)
print("Program is starting soon in 3 seconds...")
time.sleep(1)
print("Program is starting soon in 2 seconds...")
time.sleep(1)
print("Program is starting soon in 1 seconds...")
time.sleep(1)
print("Start typing")

keyboard_listener.start()
mouse_listener.start()
keyboard_listener.join()
mouse_listener.join()