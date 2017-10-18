from tkinter import *
from string import *


class ModalDialog(Tk):

    def __init__(self, parent, headerText, detailsText, width, height):

        super().__init__()

        parent_width = int(parent.winfo_geometry().split('+')[0].split('x')[0])
        parent_height = int(parent.winfo_geometry().split('+')[0].split('x')[1])
        parent_offx = int(parent.winfo_geometry().split('+')[1])
        parent_offy = int(parent.winfo_geometry().split('+')[2])
        self.geometry('%dx%d+%d+%d' % (width, height, parent_offx +
                               (parent_width-width)/2, parent_offy + (parent_height-height)/2))

        label_header = Label(self, text=headerText)
        label_header.grid(column=0, row=0, sticky=E+W, pady=5, padx=5)
        label_text = Label(self, text=detailsText)
        label_text.grid(column=0, row=1, sticky=E+W+N+S, pady=5, padx=5)
        button_close = Button(self, text='Close', command=self.destroy)
        button_close.grid(column=0, row=2, pady=5, padx=5)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.grab_set_global()

        self.mainloop()

