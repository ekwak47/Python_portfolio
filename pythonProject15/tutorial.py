import curses
from curses import wrapper
import time
import random

def start(std):
    std.clear()
    std.addstr("Welcome to the type speed test!")
    std.addstr("\nPress any Key to Begin")
    std.refresh()
    std.getkey()


def display_text(std, target, curr, wpm = 0):
    std.addstr(target)
    std.addstr(1, 0, f"WPM: {wpm}")

    for i, x in enumerate(curr):
        correct_char = target[i]
        color = curses.color_pair(1)
        if x != correct_char:
            color = curses.color_pair(2)

        std.addstr(0, i, x, color)


def load_txt():
    with open('txt.txt', 'r') as f:
        lines = f.readlines()
        return random.choice(lines).strip()  #randomly chooses one element from list, and removes \n from lines


def wpm(std):
    target_text = load_txt()
    curr_text = []
    wpm = 0
    start = time.time()
    std.nodelay(True)
    while True:
        curr_time_elapsed = max(time.time() - start, 1)
        wpm = round((len(curr_text) / (curr_time_elapsed / 60)) / 5)
        std.clear()
        display_text(std, target_text, curr_text, wpm)
        std.refresh()

        if "".join(curr_text) == target_text:
            std.nodelay(False)
            break

        try:
            key = std.getkey()
        except:
            continue

        for x in curr_text:
            std.addstr(x, curses.color_pair(1))

        std.refresh()

        if ord(key) == 27:     # escape key exits program
            break

        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(curr_text) > 0:
                curr_text.pop()

        elif len(curr_text) < len(target_text):
            curr_text.append(key)




def main(std):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    start(std)
    while True:
        wpm(std)

        std.addstr(2, 0, "You complete the test, press and key to continue")

        key = std.getkey()

        if ord(key) == 27:
            break


wrapper(main)
