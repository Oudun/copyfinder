from tkinter import *


class SuperPane(PanedWindow):

    folderScannedImage = None
    index = 0


    def __init__(self):
        super().__init__()
        self.folderScannedImage = PhotoImage(file="icons/folder_duplicate.png").subsample(4, 4)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        print("building")


    def add_directory(self):
        iconLabel = Label(self, bg='white', image=self.folderScannedImage)
        iconLabel.grid(row=self.index, column=0)
        label = Label(self, bg='white', text='Some long text', anchor=W)
        label.grid(row=self.index, column=1, sticky=W+E)
        blueButton = Button(self, bg='white', relief=FLAT, text='+')
        blueButton.grid(row=self.index, column=2)
        ++self.index

window = Tk()
window.geometry('640x480')
window.grid_columnconfigure(0, weight=1)


pane = SuperPane()
pane.add_directory()
pane.grid(row=0, column=0, sticky=W+E+N)

window.mainloop()





