#!/usr/bin/python

import os;
from Utils import get_drives;
import tkinter as tk;
from tkinter import ttk;

from ctypes import windll

#ttk.Progressbar;

def a(x):
    print ("hi")

def CurSelet(event):
    widget = event.widget
    selection=widget.curselection()
    value = widget.get(selection[0])
    values = ''
    counter = 1
    currentDirContentListbox.delete(0,currentDirContentListbox.size()-1)
    if (value == '..'):
        if (currentDirLabel['text'].rfind('\\') != -1):
            value = currentDirLabel['text'][0:currentDirLabel['text'].rfind('\\')]
            print(value)
            values = os.listdir(value)
            currentDirContentListbox.insert(++counter, "..")
            currentDirLabel.config(text = value)
            for item in values:
                currentDirContentListbox.insert(++counter, value + "\\" + item)
        else:
            values = get_drives()
            for item in values:
                currentDirContentListbox.insert(++counter, item+":")
    else:
        print(value)
        values = os.listdir(value)
        currentDirContentListbox.insert(++counter, "..")
        currentDirLabel.config(text = value)
        for item in values:
            currentDirContentListbox.insert(++counter, value + "\\" + item)

window = tk.Tk()

currentDirLabel = tk.Label(window)
currentDirLabel.grid(row=0, columnspan=2)

currentDirContentListbox = tk.Listbox(window, width=64, height=24)
currentDirContentListbox.grid(row=1, column=0, sticky="n", padx=10)

copiesDirContentListbox = tk.Listbox(window, width=64, height=24)
copiesDirContentListbox.grid(row=1, column=1, sticky="n", padx=10)

progress = ttk.Progressbar(window)
progress.grid(row=2, columnspan=2)

currentDirContentListbox.bind('<<ListboxSelect>>',CurSelet)

drives = get_drives()
counter = 1
#currentDirContentListbox.insert(++counter, '..')
for drive in drives:
    currentDirContentListbox.insert(++counter, drive+":")

window.config(width = 640, height = 480)
window.mainloop()

