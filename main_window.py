# Import required Libraries
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from take_picture import *
from student_detail_page import StudentDetailPage
from track_attendance_page import TrackAttendancePage


class Main(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.title('WOU Examination Attendance System')
        self.resizable(False, False)
        screen_width_main = self.winfo_screenwidth()
        screen_height_main = self.winfo_screenheight()
        x_coordinate_login = (screen_width_main / 2) - (1200 / 2)
        y_coordinate_login = (screen_height_main / 2) - (500 / 2)
        self.geometry('%dx%d+%d+%d' %
                      (1200, 500, x_coordinate_login, y_coordinate_login))
        self.switch_frame(StudentDetailPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def menu(self, bg1, bg2):
        menu_frame = tk.Frame(self, width=200, height=500,
                              bg='#262626').place(x=0, y=0)
        # -----menu frame----
        icon = Image.open('images/wawasan.png')
        icon = icon.resize((40, 30), Image.ANTIALIAS)
        self.icon = ImageTk.PhotoImage(icon)

        icon_image = Label(menu_frame, bg='#262626',
                           image=self.icon)
        icon_image.place(x=15, y=25)

        title_lbl_1 = Label(menu_frame, text='E X A M I N A T I O N', bg='#262626',
                            fg='white', font=("helvetica", 7))
        title_lbl_1.place(x=75, y=25)
        title_lbl_2 = Label(menu_frame, text='A T T E N D A N C E', bg='#262626',
                            fg='white', font=("helvetica", 7))
        title_lbl_2.place(x=75, y=40)

        # ------menu button-----
        Button(menu_frame, width=27, height=5, text='R E G I S T E R', border=0, bg=bg1,
               fg='white', activebackground='#191d2b', activeforeground='white', command=lambda: self.switch_frame(StudentDetailPage)).place(x=5, y=70)
        Button(menu_frame, width=27, height=5, text='T R A C K', pady=4, border=0,
               bg=bg2, fg='white', activebackground='#191d2b', activeforeground='white', command=lambda: self.switch_frame(TrackAttendancePage)).place(x=5, y=155)

        # ------Date and time------
        timeTemp = time.strftime('%Y-%m-%d %H:%M:%S')
        watch = tk.Label(menu_frame, text=timeTemp, fg="white",
                         bg='#262626', font=("helvetica", 10))
        watch.pack()
        watch.place(x=40, y=450)

        def date_time():
            timeReplace = time.strftime('%Y-%m-%d %H:%M:%S')
            watch.configure(text=timeReplace)
            self.after(200, date_time)  # it'll call itself continuously
        date_time()

    def close(self):
        answer = messagebox.askyesno('Confirmation',
                                     'Are you sure that you want to quit?', parent=self)
        if answer:
            self.destroy()

    def shutdown(self, main_frame, x1, y1):
        shutdown = Image.open('images/shutdown.png')
        shutdown = shutdown.resize((20, 20), Image.ANTIALIAS)
        self.shutdown_icon = ImageTk.PhotoImage(shutdown)
        # Resizing image to fit on button
        b = Button(main_frame, border=0,
                   bg='#191d2b', image=self.shutdown_icon, command=self.close, compound=RIGHT, cursor='hand2')
        b.place(x=x1, y=y1)


if __name__ == "__main__":
    app = Main()
    app.mainloop()
