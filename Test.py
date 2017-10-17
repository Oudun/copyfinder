import tkinter as tk
from tkinter import font


class NewListbox(tk.Listbox):

    def autowidth(self, maxwidth=100):
        autowidth(self, maxwidth)


def autowidth(list, maxwidth=100):
    f = font.Font(font=list.cget("font"))
    pixels = 0
    for item in list.get(0, "end"):
        pixels = max(pixels, f.measure(item))
    # bump listbox size until all entries fit
    pixels = pixels + 10
    width = int(list.cget("width"))
    for w in range(0, maxwidth+1, 5):
        if list.winfo_reqwidth() >= pixels:
            break
        list.config(width=width+w)


if __name__ == "__main__":

    master = tk.Tk()
    listbox = NewListbox(master, selectmode=tk.SINGLE)

    # ...
    serverDict = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}
    keys = serverDict.keys()
    for key in sorted(keys):
        listbox.insert("end", key)

    listbox.pack()

    button = tk.Button(master, text="Execute")
    button.pack()

    listbox.autowidth()

    master.mainloop()
