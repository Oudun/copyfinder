#!/usr/bin/python

import os;
from Utils import get_drives;
from Utils import get_parent_path
from Statistic import get_duplicates
from tkinter import ttk;
import tkinter as tk;


def show_duplicates(value):
    get_duplicates(value)

def set_current_dir(dir):
    currentDirLabel.config(text = dir)
    print(dir)
    items = os.listdir(os.path.join(dir))
    counter = 1
    currentDirContentListbox.delete(0,currentDirContentListbox.size()-1)
    currentDirContentListbox.insert(++counter, "..")
    print(dir)
    for item in items:
        currentDirContentListbox.insert(++counter, os.path.join(dir, item))


def item_selected(event):
    widget = event.widget
    selection=widget.curselection()
    value = widget.get(selection[0])
    if (value == '..'):
        if (currentDirLabel['text']==get_parent_path(currentDirLabel['text'])):
            reset()
        else:
            set_current_dir(get_parent_path(currentDirLabel['text']))
    else:
        if (os.path.isfile(value)):
            print(value)
            show_duplicates(value)
        else:
            set_current_dir(value)

def reset():
    currentDirLabel.config(text = '')
    currentDirContentListbox.delete(0,currentDirContentListbox.size()-1)
    counter = 1
    for drive in drives:
        currentDirContentListbox.insert(++counter, drive+":\\")



window = tk.Tk()

currentDirLabel = tk.Label(window)
currentDirLabel.grid(row=0, columnspan=2)

currentDirContentListbox = tk.Listbox(window, width=64, height=24)
currentDirContentListbox.grid(row=1, column=0, sticky="n", padx=10)

copiesDirContentListbox = tk.Listbox(window, width=64, height=24)
copiesDirContentListbox.grid(row=1, column=1, sticky="n", padx=10)

progress = ttk.Progressbar(window)
progress.grid(row=2, columnspan=2)

#currentDirContentListbox.bind('<<ListboxSelect>>',CurSelet)
currentDirContentListbox.bind('<<ListboxSelect>>',item_selected)


drives = get_drives()
counter = 1
#currentDirContentListbox.insert(++counter, '..')
for drive in drives:
    currentDirContentListbox.insert(++counter, drive+":\\")

window.config(width = 640, height = 480)
window.mainloop()

