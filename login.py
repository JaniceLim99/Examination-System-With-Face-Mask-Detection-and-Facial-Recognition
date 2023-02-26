# Import required Libraries
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import db_connection
from time import strftime
import main_window


def login():
    Login = Tk()
    screen_width = Login.winfo_screenwidth()
    screen_height = Login.winfo_screenheight()
    x_coordinate = (screen_width/2)-(880/2)
    y_coordinate = (screen_height/2)-(500/2)
    Login.geometry("%dx%d+%d+%d" % (880,
                                    500, x_coordinate, y_coordinate))
    Login.overrideredirect(True)
    Login.attributes('-topmost', True)

    main_frame = Frame(Login, width=880, height=500, bg='#191d2b')
    main_frame.place(x=0, y=0)

    welcome_lbl = Label(main_frame, text='WELCOME', font=(
        "helvetica", 25, "bold"),
        fg='#b2cdbd', bg='#191d2b')
    welcome_lbl.place(x=100, y=30, width=300, height=30)

    admin_img = Image.open('images/admin.png')
    admin_img = admin_img.resize((450, 350), Image.ANTIALIAS)
    photo_img_1 = ImageTk.PhotoImage(admin_img)

    admin_lbl = Label(main_frame, image=photo_img_1, bg='#191d2b')
    admin_lbl.place(x=2, y=130)

    icon_img = Image.open('images/admin_icon.png')
    icon_img = icon_img.resize((150, 110), Image.ANTIALIAS)
    photo_img_2 = ImageTk.PhotoImage(icon_img)

    icon_lbl = Label(main_frame, image=photo_img_2, bg='#191d2b')
    icon_lbl.place(x=570, y=70)

    login_lbl = Label(main_frame, text='Login', font=(
        "helvetica", 15, "bold"),
        fg='#b2cdbd', bg='#191d2b')
    login_lbl.place(x=618, y=180)

    username_lbl = Label(main_frame, text='Username', font=(
        "helvetica", 13, "bold"),
        fg='#6c7983', bg='#191d2b')
    username_lbl.place(x=500, y=250)

    username_entry = Entry(main_frame, highlightthickness=0, relief=FLAT, font=(
        "helvetica", 13), fg='white', bg='#191d2b')
    username_entry.place(x=530, y=285, width=270)

    username_line = Canvas(main_frame, width=300, height=0.2,
                           bg="#bdb9b1", highlightthickness=0)
    username_line.place(x=500, y=309)

    username_icon = Image.open('images/username_icon.png')
    username_icon = username_icon.resize((20, 20), Image.ANTIALIAS)
    icon_img_1 = ImageTk.PhotoImage(username_icon)

    username_icon = Label(main_frame, image=icon_img_1, bg='#191d2b')
    username_icon.place(x=500, y=282)

    password_lbl = Label(main_frame, text='Password', font=(
        "helvetica", 13, "bold"),
        fg='#6c7983', bg='#191d2b')
    password_lbl.place(x=500, y=330)

    password_entry = Entry(main_frame, highlightthickness=0, relief=FLAT, font=(
        "helvetica", 13), fg='white', bg='#191d2b', show="*")
    password_entry.place(x=530, y=366, width=270)

    password_line = Canvas(main_frame, width=300, height=0.2,
                           bg="#bdb9b1", highlightthickness=0)
    password_line.place(x=500, y=390)

    password_icon = Image.open('images/password_icon.png')
    password_icon = password_icon.resize((20, 20), Image.ANTIALIAS)
    icon_img_2 = ImageTk.PhotoImage(password_icon)

    password_icon = Label(main_frame, image=icon_img_2, bg='#191d2b')
    password_icon.place(x=500, y=363)

    def time():
        string = strftime('%H:%M:%S %p')
        lbl.config(text=string)
        lbl.after(1000, time)

    lbl = Label(main_frame, font=('helvetica', 10),
                background='#191d2b', foreground='#b2cdbd')
    lbl.place(x=760, y=450)
    time()

    def login_validation():
        # getting form data and applying empty validation
        if username_entry.get() == "" or password_entry.get == "":
            messagebox.showerror(
                "Error", "Username and password cannot be empty!")
        else:
            # establishing a connection to the database
            conn = db_connection.DbCheck.connection
            my_cursor = conn.cursor()
            # check if the user exists
            my_cursor.execute(
                "Select * from admin where username=%s and password=%s", (username_entry.get(), password_entry.get()))
            row = my_cursor.fetchone()
            # if user not exists
            if row == None:
                messagebox.showerror("Error", "Invalid username and password!")
            else:
                Login.destroy()
                main_window.Main()
            conn.commit()

    login_button = Button(main_frame, text="LOGIN", cursor="hand2", font=(
        "helvetica", 10), bg="#3399CC", fg="white", command=login_validation)
    login_button.place(x=500, y=410, width=300, height=30)

    logo_img = Image.open('images\wawasan.png')
    logo_img = logo_img.resize((80, 60), Image.ANTIALIAS)
    photo_img = ImageTk.PhotoImage(logo_img)

    f_lbl = Label(main_frame, image=photo_img, bg='#191d2b')
    f_lbl.place(x=770, y=25)

    def close():
        answer = messagebox.askyesno('Confirmation',
                                     'Are you sure that you want to quit?', parent=Login)
        if answer:
            Login.destroy()

    shutdown = Image.open('images/shutdown.png')
    shutdown = shutdown.resize((20, 20), Image.ANTIALIAS)
    shutdown = ImageTk.PhotoImage(shutdown)
    # Resizing image to fit on button
    b = Button(main_frame, border=0,
               bg='#191d2b', image=shutdown, command=close, compound=RIGHT, cursor='hand2')
    b.place(x=10, y=10)

    # ----show/hide password----
    def show():
        hide_button = Button(main_frame, image=icon_img_4, bg='white',
                             activebackground='white', cursor='hand2', bd=0, command=hide)
        hide_button.place(x=810, y=363)
        password_entry.config(show='')

    def hide():
        show_button = Button(main_frame, image=icon_img_3, bg='white',
                             activebackground='white', cursor='hand2', bd=0, command=show)
        show_button.place(x=810, y=363)
        password_entry.config(show='*')

    show_button = Image.open('images/show_pass.png')
    show_button = show_button.resize((20, 20), Image.ANTIALIAS)
    icon_img_3 = ImageTk.PhotoImage(show_button)

    show_button = Button(main_frame, image=icon_img_3, bg='white',
                         activebackground='white', cursor='hand2', bd=0, command=show)
    show_button.place(x=810, y=363)

    hide_button = Image.open('images/hide_pass.png')
    hide_button = hide_button.resize((20, 20), Image.ANTIALIAS)
    icon_img_4 = ImageTk.PhotoImage(hide_button)

    Login.mainloop()
