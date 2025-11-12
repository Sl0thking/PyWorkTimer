from datetime import datetime
from tkinter import Tk, ttk, font
import subprocess

from pytimer.timer import WorkTimer

timer = WorkTimer()
screen_locked = False
curr_day = datetime.now().strftime("%d.%m.%Y")

start_btn = None
pause_btn = None
label = None
pause_label = None
root = None

def start():
    global timer
    global start_btn
    global curr_day

    timer.track_day(curr_day)
    timer.start()

    start_btn["command"] = stop
    start_btn["text"] = "Stop"

def stop():
    global timer
    global start_btn

    timer.stop()

    start_btn["command"] = start
    start_btn["text"] = "Start"

def pause():
    global timer
    global pause_btn

    timer.pause()
    pause_btn["command"] = unpause
    pause_btn["text"] = "Unpause"

def unpause():
    global timer
    global pause_btn

    timer.unpause()
    pause_btn["command"] = pause
    pause_btn["text"] = "Pause"

def is_screen_locked():
    process_name = 'LogonUI.exe'
    callall = 'TASKLIST'
    outputall = subprocess.check_output(callall)
    outputstringall = str(outputall)
    return process_name in outputstringall

def timer_process():
    global timer
    global screen_locked
    global curr_day
    global label
    global pause_label
    global root

    print(timer.to_json())

    if screen_locked and not is_screen_locked():
        unpause()
        screen_locked = False
    elif is_screen_locked():
        pause()
        screen_locked = True

    label["text"] = str(timer.worktime(curr_day)).split(".")[0]
    pause_label["text"] = str(timer.pausetime(curr_day)).split(".")[0]
    root.after(1000, timer_process)


def main():
    global pause_btn
    global start_btn
    global root
    global pause_label
    global label

    root = Tk()
    root.title("Time")

    root.geometry("200x80")

    highlightFont = font.Font(family='Helvetica', name='appHighlightFont', size=24, weight='bold')

    label = ttk.Label(root, text="0:00:00", font=highlightFont)
    label.grid(column=0, row=0)

    pause_label = ttk.Label(root, text="0:00:00")
    pause_label.grid(column=1, row=0)

    start_btn = ttk.Button(root, text="Start", command=start)
    pause_btn = ttk.Button(root, text="Pause", command=pause)

    start_btn.grid(column=0, row=2, sticky="W,E")
    pause_btn.grid(column=1, row=2, sticky="W,E")

    root.columnconfigure(0, weight=3)
    root.columnconfigure(1, weight=3)

    root.rowconfigure(0, weight=3)
    root.after(1000, timer_process)
    root.mainloop()

if __name__ == "__main__":
    main()