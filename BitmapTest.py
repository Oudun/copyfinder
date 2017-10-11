import tkinter
#import Pillow

tk = tkinter.Tk()

photo = tkinter.PhotoImage(file="resources/folder_scanned.png")
photo1 = photo.subsample(6, 6)
button = tkinter.Button(image=photo1)
#button.image = photo # keep a reference!
button.pack()

tk.mainloop()
