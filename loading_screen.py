# Import required Libraries
import time
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk  # loading Python Imaging Library
from db_connection import *
from login import *


print(status)
root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width/2)-(680/2)
y_coordinate = (screen_height/2)-(400/2)
root.geometry("%dx%d+%d+%d" % (680,
                               400, x_coordinate, y_coordinate))
root.overrideredirect(True)
# Make the window jump above all
root.attributes('-topmost', True)

main_frame = Frame(root, width=680, height=395, bg='#191d2b')
main_frame.place(x=0, y=0)

s = ttk.Style()
s.theme_use('default')
s.configure("green.Horizontal.TProgressbar",
            foreground='green', background='#006633')
progress = Progressbar(root,
                       style="green.Horizontal.TProgressbar",
                       orient=HORIZONTAL,
                       length=690,
                       mode='determinate')

img = Image.open('images\wawasan.png')
img = img.resize((80, 60), Image.ANTIALIAS)
photo_img = ImageTk.PhotoImage(img)

f_lbl = Label(main_frame, image=photo_img, bg='#191d2b')
f_lbl.place(x=570, y=25)

title_lbl_01 = Label(main_frame, text='EXAMINATION ATTENDANCE', font=(
    "helvetica", 28, "bold"),
    fg='#b2cdbd', bg='#191d2b')
title_lbl_01.place(x=50, y=90)

title_lbl_02 = Label(main_frame, text='WITH FACE MASK DETECTION', font=(
    "helvetica", 28, "bold"),
    fg='#b2cdbd', bg='#191d2b')
title_lbl_02.place(x=50, y=130)

title_lbl_03 = Label(main_frame, text='AND FACIAL RECOGNITION', font=(
    "helvetica", 28, "bold"),
    fg='#b2cdbd', bg='#191d2b')
title_lbl_03.place(x=50, y=170)

creator_lbl = Label(main_frame, text='Creator: 141200014', font=(
    "helvetica", 10),
    fg='#b2cdbd', bg='#191d2b')
creator_lbl.place(x=510, y=210)

percentage_lbl = Label(main_frame, font=(
    "helvetica", 10),
    fg='#b2cdbd', bg='#191d2b')
percentage_lbl.place(x=315, y=340)


def progressbar():
    startup_button['text'] = 'Loading...'
    startup_button['state'] = 'disabled'
    startup_button['bg'] = '#8a8a8a'
    startup_button['fg'] = 'black'

    r = 0
    for i in range(101):
        progress['value'] = r
        percentage_lbl.config(text=str(i)+"%")
        root.update_idletasks()
        time.sleep(0.05)
        r = r + 1

    root.destroy()
    if r >= 100:
        if status is True:
            login()
        else:
            db_error = root
            db_error.withdraw()
            messagebox.showerror(
                'Database Connection Error', 'Failed To Connect Database, Please Contact IT Department!')
            db_error.destroy()


progress.place(x=-10, y=395)

startup_button = Button(main_frame, text="Launch", command=progressbar, cursor="hand2", font=(
    "helvetica", 10), bg="#006633", fg="white")
startup_button.place(x=220, y=280, width=220, height=40)

version_lbl = Label(main_frame, text='1.3.0v', font=(
    "helvetica", 8),
    fg='#b2cdbd', bg='#191d2b')
version_lbl.place(x=0, y=375)


def close():
    answer = messagebox.askyesno('Confirmation',
                                 'Are you sure that you want to quit?', parent=root)
    if answer:
        root.destroy()


shutdown = Image.open('images/shutdown.png')
shutdown = shutdown.resize((20, 20), Image.ANTIALIAS)
shutdown = ImageTk.PhotoImage(shutdown)
# Resizing image to fit on button
b = Button(main_frame, border=0,
           bg='#191d2b', image=shutdown, command=close, compound=RIGHT, cursor="hand2")
b.place(x=10, y=10)

root.mainloop()
