import tkinter

window = tkinter.Tk()

currentDirLabel = tkinter.Label(window)
currentDirLabel.grid(row=0, columnspan=2)

currentDirContentListbox = tkinter.Listbox(window, width=64, height=24)
currentDirContentListbox.grid(row=1, column=0, sticky="n", padx=10)

copiesDirContentListbox = tkinter.Listbox(window, width=64, height=24)
copiesDirContentListbox.grid(row=1, column=1, sticky="n", padx=10)

progress = tkinter.Progressbar(window)
progress.grid(row=2, columnspan=2)

# currentDirContentListbox.bind('<<ListboxSelect>>',CurSelet)
#currentDirContentListbox.bind('<<ListboxSelect>>', item_selected)

window.config(width = 640, height = 480)
window.mainloop()
