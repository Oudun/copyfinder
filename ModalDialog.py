from tkinter import *
from string import *


class ModalDialog(Tk):

    def __init__(self, parent):
        super().__init__()
        print(parent.winfo_geometry())
        self.geometry(parent.winfo_geometry())
        self.geometry('320x240')
        label_header = Label(self, text='Header')
        label_header.pack()
        label_text = Label(self, text='Some text')
        label_text.pack()
        button_close = Button(self, text='Close')
        button_close.pack()

        self.mainloop()

