import time
from datetime import datetime
from datetime import timedelta
import tkinter as tk
from tkinter import ttk
import add_time_manually


time_spent_global = []
unit = "HH:MM:SS"
active = False
pause = False
internim_result = 0


def get_current_project():
    global current_project
    f = open("time_spent_coding.csv", "r")
    last_line = f.readlines()[-1]
    last_line = last_line[:-3]
    help_list = last_line.split(";")
    current_project = help_list[-1]


def get_from_file():
    time_spent_global.clear()
    f = open("time_spent_coding.csv", "r")
    for line in f:
        list_element = line[:-3]
        help_list = list_element.split(";")
        time_spent_global.append(help_list)

    return time_spent_global


def time_spent_list_calculation():
    time_spent = 0
    time_spent_global = get_from_file()
    for element in time_spent_global:
        time_spent += int(element[2])

    return time_spent


def time_elapsed_seconds():
    elapsed = time.time() - start_time + internim_result
    return elapsed


def time_format_from_seconds(seconds):
    t = str(timedelta(seconds=seconds))
    return t


def time_format_to_seconds(ISO8601):
   d, h, m, s = ISO8601.split(":")
   return int(d) * 86400 + int(h) * 3600 + int(m) * 60 + int(s)


def write_to_file():
    f = open("time_spent_coding.csv", "a")

    f.write(f"{start_datetime.strftime('%Y-%m-%d %H:%M:%S')};{stop_datetime.strftime('%Y-%m-%d %H:%M:%S')};{elapsed_seconds};{current_project}, \n")
    f.close()


def start_timer_button():
    global btn_start_timer
    btn_start_timer = ttk.Button(text="start timer", command=start_time_button)
    btn_start_timer.place(x=150, y=200)


def stop_timer_button():
    global btn_stop_timer
    btn_stop_timer = ttk.Button(master=root, text="Stop timer", command=stop_time_button)
    btn_stop_timer.place(x=250, y=200)


def pause_timer_button():
    global btn_pause_timer
    btn_pause_timer = ttk.Button(master=root, text="pause timer", command=pause_time_button)
    btn_pause_timer.place(x=150, y=200)


def pause_time_button():
    global pause_elapsed_label
    global pause
    global active
    global pause_start_time
    global internim_result
    pause = True
    active = False
    internim_result = time_elapsed_seconds()
    pause_start_time = time.time()
    pause_elapsed_label = ttk.Label(master=root, text="")
    pause_elapsed_label.place(x=250, y=150)
    pause_updater()
    btn_pause_timer.destroy()
    start_timer_button()


def pause_updater():
    global pause_start_time
    global pause_elapsed_label
    pause_elapsed = int(time.time() - pause_start_time)
    if pause:
        pause_elapsed_label.config(text=f"Paused for {pause_elapsed} seconds")
    else:
        pause_elapsed_label.destroy()

    root.after(1000, pause_updater)


def start_time_button():
    global active
    global start_time
    global start_datetime
    global pause
    pause = False
    active = True
    get_from_file()
    start_time = time.time()
    start_datetime = datetime.now()
    btn_start_timer.destroy()
    stop_timer_button()
    counter()
    total_time_counter()
    pause_timer_button()


def stop_time_button():
    global active
    global stop_datetime
    global time_spent
    global pause
    global internim_result
    active = False
    stop_datetime = datetime.now()
    write_to_file()
    btn_stop_timer.destroy()
    time_spent = time_spent_list_calculation()
    if pause:
        pause = False
        internim_result = 0
    else:
        btn_pause_timer.destroy()
        start_timer_button()


def counter():
    if active:
        global elapsed_seconds
        elapsed_seconds = int(time_elapsed_seconds())
        if unit == "s":
            elapsed = str(elapsed_seconds)
        else:
            elapsed = time_format_from_seconds(elapsed_seconds)
        time_display.configure(text=elapsed)
        root.after(1000, counter)


def total_time_counter():
    if active:
        total_time_spent = time_spent + int(time_elapsed_seconds())
        if unit == "s":
            pass
        else:
            total_time_spent = time_format_from_seconds(total_time_spent)
        total_time_display.configure(text=total_time_spent)
    root.after(1000, total_time_counter)

def change_time_unit_button():
    global change_unit_btn
    change_unit_btn = ttk.Button(master=root, text="show time in seconds", command=unit_changer)
    change_unit_btn.place(x=50, y=50)


def unit_changer():
    global unit
    if unit == "s":
        unit = "HH:MM:SS"
        change_unit_btn.config(text="show time in seconds")
        total_time_display.config(text=time_format_from_seconds(total_time_display.cget("text")))
        time_display_num = time_display.cget("text")
        if time_display_num != "":
            time_display.config(text=time_format_from_seconds(int(time_display_num)))
        else:
            pass
    else:
        unit = "s"
        change_unit_btn.config(text="show time in ISO 8601")
        total_time_display.config(text=time_format_to_seconds(total_time_display.cget("text")))
        time_display_num = time_display.cget("text")
        if time_display_num != "":
            time_display.config(text=str(time_format_to_seconds(time_display_num)))
        else:
            pass
    print(f"unit was changed to {unit}.")


def add_time_manually_btn():
    global add_time_manually_button
    add_time_manually_button = ttk.Button(master=root, text="add time manually", command= lambda: add_time_manually.add_time_manually_button(current_project))
    add_time_manually_button.place(x=10, y=270)



def change_project_button():
    global btn_change_project
    btn_change_project = ttk.Button(master=root, text="change project", command=change_project)
    btn_change_project.place(x=300, y=270)


def change_project_get_entry():
    global current_project
    current_project = input_field.get()
    window.destroy()
    current_project_display.config(text=f"current project: {current_project}")


def change_project():
    global input_field
    global window
    window = tk.Toplevel()
    window.title("change project")

    f = ttk.Frame(master=window, width=400, height=200)
    f.pack()

    input_field_label = ttk.Label(master=window, text="Input new project name:")
    input_field_label.place(x=10, y=75)

    input_field = ttk.Entry(master=window, width=35)   #change project fun + add project fun (nachträglich) + add project in "Write to file"
    input_field.place(x=150, y=75)
    input_field.focus()

    input_button = ttk.Button(master=window, text="Enter", command=change_project_get_entry)
    input_button.place(x=210, y=125)


    window.mainloop()


time_spent = time_spent_list_calculation()      #get previous time spent
get_current_project()


root = tk.Tk()


frame = ttk.Frame(root, width=400, height=300)
frame.pack()
root.title("Timespenton")

time_display = ttk.Label(master=root, text="")
time_display.place(x=200, y=150)

total_time_display = ttk.Label(master=root, text=time_format_from_seconds(time_spent_list_calculation()))
total_time_display.place(x=200, y=50)

current_project_display = ttk.Label(master=root, text=f"current project: {current_project}")
current_project_display.place(x=15, y=20)


#buttons
start_timer_button()
change_time_unit_button()
add_time_manually_btn()
change_project_button()


root.mainloop()
