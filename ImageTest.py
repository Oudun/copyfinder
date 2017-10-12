# Import Pillow:
from PIL import Image
import tkinter

# Load the original image:
img = Image.open("F:\\PROJECTS\\copyfinder\\resources\\DollyIcons.png")

#img = Image.open(".\\resources\\DollyIcons.png")
#img2 = img.crop((0, 0, 100, 100))

window = tkinter.Tk()

button = tkinter.Button(image=img)
button.pack()

window.mainloop()
