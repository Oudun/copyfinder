import tkinter

tk = tkinter.Tk()

photo = tkinter.PhotoImage(file="home-icon.png")
button = tkinter.Button(image=photo)
#button.image = photo # keep a reference!
button.pack()

tk.mainloop()
