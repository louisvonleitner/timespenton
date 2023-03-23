from tkinter import ttk
import tkinter as tk


""" add time manually process

this is a set of functions to create a window wich appears when the button 'add time manually' is pressed.
this file is used by calling the add_time_manually_button function
the other functions are activated by being called in this funciton

"""

# main func creating window
def add_time_manually_button(current_project):
    global window
    global entry_field_len
    global entry_field_start_date
    global entry_field_start_time
    global entry_field_project
    window = tk.Tk()
    window.title("add time manually")

    f = ttk.Frame(master=window, width=250, height=250)
    f.pack()

    entry_field_len = ttk.Entry(master= window, width=10)
    entry_field_len.place(x=120, y=30)
    entry_field_len.focus()

    entry_label_len = ttk.Label(master= window, text="time spent: \n    (min)")
    entry_label_len.place(x=40, y=30)

    entry_field_start_date = ttk.Entry(master=window, width=10)
    entry_field_start_date.place(x=120, y=70)

    entry_label_start_date = ttk.Label(master=window, text="    start date: \n (dd.mm.yyyy)")
    entry_label_start_date.place(x=20, y=70)

    entry_field_start_time = ttk.Entry(master=window, width=10)
    entry_field_start_time.place(x=120, y=110)

    entry_label_start_time = ttk.Label(master=window, text="start time: \n (hh:mm)")
    entry_label_start_time.place(x=45, y=110)

    entry_field_project = ttk.Entry(master=window, width=30)
    entry_field_project.insert(0, current_project)
    entry_field_project.place(x=60, y=150)

    entry_label_project = ttk.Label(master=window, text="project:")
    entry_label_project.place(x=10, y=150)


    take_box_input_btn()

    window.mainloop()

# creating a button
def take_box_input_btn():
    global take_input_button
    take_input_button = ttk.Button(master=window, text="Enter", command=take_box_inputs)
    take_input_button.place(x=114, y=200)

# formatting inputs and saving to csv file
def take_box_inputs():
    minutes_spent = int(entry_field_len.get())
    start_date = entry_field_start_date.get()
    start_time = entry_field_start_time.get()
    project = entry_field_project.get()

    correct_time_format = datetime(int(start_date[-4:]), int(start_date[3:5]), int(start_date[:2]), int(start_time[:2]), int(start_time[-2:]))
    end_datetime = correct_time_format + timedelta(minutes=minutes_spent)

    f = open("time_spent_coding.csv", "a")
    f.write(f"{correct_time_format};{end_datetime};{minutes_spent * 60};{project}, \n")
    f.close()

    window.destroy()
