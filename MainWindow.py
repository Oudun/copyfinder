from tkinter import *
from Statistic import *
from Utils import *
from ModalDialog import *


window = Tk()


def start_scanning():
    if len(get_locations()) == 0:
        w = ModalDialog(window, 'Nothing to scan', 'No location were set for scanning', 320, 240)
    scanner = Scanner()
    try:
        scanner.start()
        print ("Starting scanner thread")
    except:
        print ("Error: unable to start thread")

    # print('Button clickedddd')
    # if is_scanning:
    #     print('Already scannindddg')
    # else:

    #scan()


def show_duplicates(value):
    print('Hi')
#    get_duplicates(value)


def set_current_dir(dir):
    currentDirLabel.config(text = dir)
    print(dir)
    try:
        items = os.listdir(os.path.join(dir))
        counter = 1
        contentListbox.delete(0,contentListbox.size()-1)
        contentListbox.insert(++counter, "..")
        #contentListbox.itemconfig(1, {})
        for item in items:
            contentListbox.insert(++counter, os.path.join(dir, item))
            if has_duplicates(os.path.join(dir, item)):
                if os.path.isfile(os.path.join(dir, item)):
                    contentListbox.itemconfig(counter, {'bg': 'red', 'padx': 10})
                else:
                    contentListbox.itemconfig(counter, {'bg': 'pink'})
    except PermissionError:
        print ("could not access")

def item_selected(event):
    widget = event.widget
    selection=widget.curselection()
    value = widget.get(selection[0])
    if value == '..':
        if currentDirLabel['text'] == get_parent_path(currentDirLabel['text']):
            reset()
        else:
            set_current_dir(get_parent_path(currentDirLabel['text']))
    else:
        if os.path.isfile(value):
            show_duplicates(value)
        else:
            set_current_dir(value)


def reset():
    currentDirLabel.config(text = '')
    contentListbox.delete(0,contentListbox.size()-1)
    counter = 1
    for drive in drives:
        contentListbox.insert(++counter, drive+":\\")


window.title(string='Dolly')
window.iconbitmap('icons/dolly_icon.ico')
print(window.winfo_screenwidth())
print(window.winfo_screenheight())
window.geometry('800x600+%d+%d' % ((window.winfo_screenwidth()-800)/2, (window.winfo_screenheight()-600)/2))

mainPanel = PanedWindow(orient=VERTICAL)
mainPanel.pack(fill=BOTH, expand=1)

buttonPanel = PanedWindow(orient=HORIZONTAL, bg='white')
buttonPanel.pack(fill=BOTH, expand=1)

mainPanel.add(buttonPanel)

scanImage=PhotoImage(file="icons/button_search.png").subsample(2, 2)
exportImage=PhotoImage(file="icons/button_export.png").subsample(2, 2)
importImage=PhotoImage(file="icons/button_import.png").subsample(2, 2)

buttonScan = Button(buttonPanel, compound=TOP, text='Scan', image=scanImage, relief=FLAT, width=72, bg='white', command=start_scanning)
buttonExport = Button(buttonPanel, compound=TOP, text='Export', image=exportImage, relief=FLAT, width=72, bg='white')
buttonImport = Button(buttonPanel, compound=TOP, text='Import', image=importImage, relief=FLAT, width=72, bg='white')
stub =  Label(buttonPanel, bg='white')


buttonPanel.add(buttonScan)
buttonPanel.add(buttonExport)
buttonPanel.add(buttonImport)
buttonPanel.add(stub)

label = Label(bg='white')

browsePane = PanedWindow(orient=HORIZONTAL)
browsePane.pack(fill=BOTH, expand=0)

#
contentListbox = Listbox(browsePane, bg='white')
duplicatesListbox = Listbox(browsePane, bg='white')
browsePane.add(contentListbox)
browsePane.add(duplicatesListbox)
contentListbox.configure()

mainPanel.add(browsePane)

currentDirLabel = Label()

buttonScan.bind('<<Button-1>>', start_scanning)
contentListbox.bind('<<ListboxSelect>>', item_selected)

drives = get_drives()
counter = 1
for drive in drives:
    contentListbox.insert(++counter, drive+":\\")

window.mainloop()
