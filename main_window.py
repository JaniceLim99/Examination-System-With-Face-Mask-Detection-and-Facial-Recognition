# Import required Libraries
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from doctest import master
import time
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Treeview
from PIL import Image, ImageTk
from tkcalendar import *
import mysql.connector
from mark_attendance_1 import ImageRecognition
from take_picture import *


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
        self.switch_frame(StartPage)

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
               fg='white', activebackground='#191d2b', activeforeground='white', command=lambda: self.switch_frame(StartPage)).place(x=5, y=70)
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


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        main_frame = tk.Frame(self, width=1000, height=500,
                              bg='#191d2b').place(x=200, y=0)
        master.menu('#191d2b', '#262626')

        # ------main frame-----
        def columnFormat(entry, limit):
            x = entry.get()
            if not x.isdigit():
                entry.set(entry.get()[:-1])
            if len(x) > limit:
                entry.set(entry.get()[:limit])
        # ------variable--------
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_std_gender = StringVar()
        self.var_std_email = StringVar()
        self.var_std_phone = StringVar()
        self.var_std_phone.trace("w", lambda name, index, mode,
                                 phone_no=self.var_std_phone: columnFormat(phone_no, 11))
        self.var_programme = StringVar()
        self.var_course = StringVar()
        self.var_exam_hall = StringVar()
        self.var_seat_no = StringVar()
        self.var_com_search = StringVar()
        self.var_search = StringVar()

        global programme_entry, course_entry, exam_hall_entry, seat_no_entry

        # ------Student left frame-------
        Student_l_frame = LabelFrame(main_frame, bd=2, bg="#191d2b", relief=RIDGE, text="Student Details", fg='white', font=(
            "helvetica", 10, "bold"))
        Student_l_frame.place(x=210, y=15, width=490, height=255)
        # ------take photo button------
        img_left = Image.open("images/ICON.png")
        img_left = img_left.resize((180, 180), Image.ANTIALIAS)
        self.photo_img_left = ImageTk.PhotoImage(img_left)

        take_photo = Button(
            Student_l_frame, image=self.photo_img_left, cursor="hand2", command=self.generate_dataset)
        take_photo.place(x=15, y=15, width=180, height=180)

        take_photo_btn = Button(Student_l_frame, text="Take Photo", border=0, cursor="hand2", font=(
            "helvetica", 10, "bold"), bg="#48D1CC", fg="black", command=self.generate_dataset)
        take_photo_btn.place(x=15, y=190, width=180, height=30)
        # ------student_id-----
        student_id_label = Label(Student_l_frame, text="Student ID: ", font=(
            "helvetica", 10, "bold"), bg="#191d2b", fg="white")
        student_id_label.place(x=210, y=15)

        student_id_entry = Entry(Student_l_frame, textvariable=self.var_std_id, width=20, font=(
            "helvetica", 10), state='disabled')
        student_id_entry.place(x=330, y=15, height=25)
        # ------student_name-----
        student_name_label = Label(Student_l_frame, text="Student Name: ", font=(
            "helvetica", 10, "bold"), bg="#191d2b", fg="white")
        student_name_label.place(x=210, y=60)

        student_name_entry = Entry(Student_l_frame, textvariable=self.var_std_name, width=20, font=(
            "helvetica", 10))
        student_name_entry.place(x=330, y=60, height=25)
        # -----gender-----
        gender_label = Label(Student_l_frame,  text="Gender:", font=(
            "helvetica", 10, "bold"), bg="#191d2b", fg="white")
        gender_label.place(x=210, y=105)

        gender_combo = Combobox(Student_l_frame, textvariable=self.var_std_gender, font=(
            "helvetica", 10), state="readonly", width=17)
        gender_combo["values"] = (
            "Male", "Female")
        gender_combo.current(0)
        gender_combo.place(x=330, y=105, height=25)
        # ------student_phone-----
        student_phone_label = Label(Student_l_frame, text="Student Phone: ", font=(
            "helvetica", 10, "bold"), bg="#191d2b", fg="white")
        student_phone_label.place(x=210, y=150)

        student_phone_entry = Entry(Student_l_frame, textvariable=self.var_std_phone, width=20, font=(
            "helvetica", 10))
        student_phone_entry.place(x=330, y=150, height=25)
        # ------student_email-----
        student_email_label = Label(Student_l_frame, text="Student Email: ", font=(
            "helvetica", 10, "bold"), bg="#191d2b", fg="white")
        student_email_label.place(x=210, y=195)

        student_email_entry = Entry(Student_l_frame, textvariable=self.var_std_email, width=20, font=(
            "helvetica", 10))
        student_email_entry.place(x=330, y=195, height=25)

        # ------Examination frame-------
        Exam_frame = LabelFrame(main_frame, bd=2, bg="#191d2b", relief=RIDGE, text="Examination Details", fg='white', font=(
            "helvetica", 10, "bold"))
        Exam_frame.place(x=210, y=280, width=490, height=150)

        # ------programme-----
        programme_label = Label(Exam_frame, text="Programme: ", font=(
            "helvetica", 10, "bold"), bg="#191d2b", fg="white")
        programme_label.place(x=10, y=20)

        programme_entry = Combobox(Exam_frame,
                                   textvariable=self.var_programme, font=(
                                       "helvetica", 10), state="readonly", width=17)
        programme_entry["values"] = ("Select Programme", "Psychology",
                                     "Accounting", "Software Engineering", "Hospitality", "Music")
        programme_entry.current(0)
        programme_entry.place(x=94, y=20, height=25)
        # track the change event
        self.var_programme.trace('w', self.programme_course_update)

        # ------course-----
        course_label = Label(Exam_frame, text="Course: ", font=(
            "helvetica", 10, "bold"), bg="#191d2b", fg="white")
        course_label.place(x=250, y=20)

        course_entry = Combobox(Exam_frame,
                                textvariable=self.var_course, font=(
                                    "helvetica", 10), state="readonly", width=17)
        course_entry["values"] = ("Select Course", "System Security", "Computational Logic", "Social Psychology", "Biological Psychology",
                                  "Basic Accounting", "Costing", "Musicology", "Music Performance", "Hotel Management", "Intro to Tourism")
        course_entry.current(0)
        course_entry.place(x=330, y=20, height=25)

        # ------exam_hall-----
        exam_hall_label = Label(Exam_frame, text="Hall: ", font=(
            "helvetica", 10, "bold"), bg="#191d2b", fg="white")
        exam_hall_label.place(x=10, y=70)

        exam_hall_entry = Combobox(Exam_frame,
                                   textvariable=self.var_exam_hall, font=(
                                       "helvetica", 10), state="readonly", width=17)
        exam_hall_entry["values"] = (
            "Select Hall", "Hall A", "Hall B", "Hall C")
        exam_hall_entry.current(0)
        exam_hall_entry.place(x=94, y=70, height=25)
        # track the change event
        self.var_exam_hall.trace('w', self.hall_seat_update)

        # ------seat_no-----
        seat_no_label = Label(Exam_frame, text="Seat No: ", font=(
            "helvetica", 10, "bold"), bg="#191d2b", fg="white")
        seat_no_label.place(x=250, y=70)

        seat_no_entry = Combobox(Exam_frame,
                                 textvariable=self.var_seat_no, font=(
                                     "helvetica", 10), state="readonly", width=17)
        seat_no_entry["values"] = (
            "Select Seat", "A1", "A2", "A3", "A4", "A5", "A6", "B1", "B2", "B3", "B4", "B5", "C1", "C2", "C3", "C4", "C5")
        seat_no_entry.current(0)
        seat_no_entry.place(x=330, y=70, height=25)

        # ----button-----
        btn_frame = Frame(main_frame, highlightbackground="#87CEFA",
                          highlightthickness=2, bd=0, relief=RIDGE, bg="#87CEFA")
        btn_frame.place(x=210, y=450, width=115, height=30)

        save_btn = Button(btn_frame, text="S A V E",
                          width=15, bg="black", fg="#87CEFA", command=self.add_data)
        save_btn.pack()

        btn_frame_1 = Frame(main_frame, highlightbackground="#87CEFA",
                            highlightthickness=2, bd=0, relief=RIDGE, bg="#87CEFA")
        btn_frame_1.place(x=335, y=450, width=115, height=30)

        update_btn = Button(btn_frame_1, text="U P D A T E",
                            width=15, bg="black", fg="#87CEFA", command=self.update_data)
        update_btn.pack()

        btn_frame_2 = Frame(main_frame, highlightbackground="#87CEFA",
                            highlightthickness=2, bd=0, relief=RIDGE, bg="#87CEFA")
        btn_frame_2.place(x=460, y=450, width=125, height=30)

        delete_btn = Button(btn_frame_2, text="D E L E T E ",
                            width=16, bg="black", fg="#87CEFA", command=self.delete_data)
        delete_btn.pack()

        btn_frame_3 = Frame(main_frame, highlightbackground="#87CEFA",
                            highlightthickness=2, bd=0, relief=RIDGE, bg="#87CEFA")
        btn_frame_3.place(x=595, y=450, width=115, height=30)

        reset_btn = Button(btn_frame_3, text="R E S E T",
                           width=15, bg="black", fg="#87CEFA", command=self.reset_data)
        reset_btn.pack()

        # ------Student right frame-------
        Student_r_frame = LabelFrame(main_frame, bd=2, bg="#191d2b", relief=RIDGE, text="Student Details", fg="white", font=(
            "helvetica", 10, "bold"))
        Student_r_frame.place(x=710, y=15, width=480, height=415)

        img_right = Image.open("images/student_info.png")
        img_right = img_right.resize((455, 100), Image.ANTIALIAS)
        self.photo_img_right = ImageTk.PhotoImage(img_right)

        f_lbl = Label(Student_r_frame,
                      image=self.photo_img_right, bg="#191d2b")
        f_lbl.place(x=5, y=0, width=455, height=100)
        # ------search frame-------
        Search_frame = LabelFrame(Student_r_frame, bd=2, bg="#191d2b", relief=RIDGE, text="Search Details", fg="white", font=(
            "helvetica", 10, "bold"))
        Search_frame.place(x=5, y=100, width=466, height=70)

        search_label = Label(Search_frame, text="Search By:", font=(
            "helvetica", 10, "bold"), bg="#191d2b", fg="white")
        search_label.grid(row=0, column=0, padx=1, pady=10, sticky=W)

        search_combo = Combobox(Search_frame, textvariable=self.var_com_search, font=(
            "helvetica", 10), state="readonly", width=10)
        search_combo["values"] = (
            "Select", "student_id", "name", "gender", "email")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=1, pady=10, sticky=W)

        Search_entry = Entry(Search_frame, textvariable=self.var_search, width=13, font=(
            "helvetica", 10))
        Search_entry.grid(row=0, column=2, padx=2, pady=10, sticky=W)

        btn_frame_search = Frame(Search_frame, highlightbackground="#F4A460",
                                 highlightthickness=2, bd=0, relief=RIDGE, bg="#F4A460")
        btn_frame_search.place(x=275, y=4, width=80, height=30)

        search_btn = Button(btn_frame_search, text="S E A R C H",
                            width=10, bg="black", fg="#F4A460", command=self.search_data)
        search_btn.pack()

        btn_frame_show = Frame(Search_frame, highlightbackground="#F4A460",
                               highlightthickness=2, bd=0, relief=RIDGE, bg="#F4A460")
        btn_frame_show.place(x=362, y=4, width=90, height=30)

        show_btn = Button(btn_frame_show, text="S H O W  A L L",
                          width=13, bg="black", fg="#F4A460", command=self.fetch_data)
        show_btn.pack()
        # --------Table frame-----------
        Table_frame = Frame(Student_r_frame, bd=2, bg="white", relief=RIDGE)
        Table_frame.place(x=5, y=175, width=466, height=210)

        scroll_x = Scrollbar(Table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(Table_frame, orient=VERTICAL)

        self.student_table = Treeview(Table_frame, columns=("id", "name",
                                                            "gender", "phone", "email", "programme", "course", "hall", "seat_no"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("id", text="Student ID")
        self.student_table.heading("name", text="Student Name")
        self.student_table.heading("gender", text="Gender")
        self.student_table.heading("phone", text="Phone No")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("programme", text="Programme")
        self.student_table.heading("course", text="Course")
        self.student_table.heading("hall", text="Hall")
        self.student_table.heading("seat_no", text="Seat No")
        self.student_table["show"] = "headings"

        self.student_table.column("id", width=80, anchor=CENTER)
        self.student_table.column("name", width=150, anchor=CENTER)
        self.student_table.column("gender", width=50, anchor=CENTER)
        self.student_table.column("phone", width=100, anchor=CENTER)
        self.student_table.column("email", width=180, anchor=CENTER)
        self.student_table.column("programme", width=150, anchor=CENTER)
        self.student_table.column("course", width=80, anchor=CENTER)
        self.student_table.column("hall", width=50, anchor=CENTER)
        self.student_table.column("seat_no", width=50, anchor=CENTER)
        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()

        mark_attendance = Image.open("images/mark_attendance.png")
        mark_attendance = mark_attendance.resize((30, 30), Image.ANTIALIAS)
        self.photo_mark_attendance = ImageTk.PhotoImage(mark_attendance)

        mark_attendance_lbl = Label(
            main_frame, image=self.photo_mark_attendance, bg='#191d2b')
        mark_attendance_lbl.place(x=840, y=450, width=30, height=30)

        btn_frame_4 = Frame(main_frame, highlightbackground="#90EE90",
                            highlightthickness=2, bd=0, relief=RIDGE, bg="#90EE90")
        btn_frame_4.place(x=880, y=450, width=165, height=30)

        mark_attendance_btn = Button(btn_frame_4, text="M A R K   A T T E N D A N C E",
                                     width=22, bg="black", fg="#90EE90", command=ImageRecognition)
        mark_attendance_btn.pack()

        master.shutdown(main_frame, 1150, 455)

        self.pack(fill=BOTH, expand=True)

# ------Function declaration------
    def programme_course_update(self, *args):
        course_entry.set("Select Course")  # reset the option
        if programme_entry.get() == "Psychology":
            course_entry["values"] = (
                "Social Psychology", "Biological Psychology")
        elif programme_entry.get() == "Accounting":
            course_entry["values"] = (
                "Basic Accounting", "Costing")
        elif programme_entry.get() == "Software Engineering":
            course_entry["values"] = (
                "System Security", "Computational Logic")
        elif programme_entry.get() == "Hospitality":
            course_entry["values"] = (
                "Hotel Management", "Intro to Tourism")
        elif programme_entry.get() == "Music":
            course_entry["values"] = (
                "Musicology", "Music Performance")
        else:
            course_entry["values"] = ("Select Course", "System Security", "Computational Logic", "Social Psychology", "Biological Psychology",
                                      "Basic Accounting", "Costing", "Musicology", "Music Performance", "Hotel Management", "Intro to Tourism")

    def hall_seat_update(self, *args):
        seat_no_entry.set("Select Seat")  # reset the option
        if exam_hall_entry.get() == "Hall A":
            seat_no_entry["values"] = ("A1", "A2", "A3", "A4", "A5", "A6")
        elif exam_hall_entry.get() == "Hall B":
            seat_no_entry["values"] = ("B1", "B2", "B3", "B4", "B5")
        elif exam_hall_entry.get() == "Hall C":
            seat_no_entry["values"] = ("C1", "C2", "C3", "C4", "C5")
        else:
            seat_no_entry["values"] = (
                "Select Seat", "A1", "A2", "A3", "A4", "A5", "A6", "B1", "B2", "B3", "B4", "B5", "C1", "C2", "C3", "C4", "C5")

    # --------Generate data set or take photo samples ---------
    def generate_dataset(self):
        # getting from data
        sid = self.var_std_id.get()
        name = self.var_std_name.get()

        if sid == '' or name == '':
            messagebox.showwarning(
                "Recognize Error", "Please select the student that want to recognize!!")
        else:
            cam_recognize(
                sid, name, "haarcascades/haarcascade_frontalface_default.xml", "student_data", "Trainner")
            reply = messagebox.showinfo(
                "Mask is Required", "Please put on your mask.")
            if reply:
                cam_recognize(
                    sid, name, "data_classifier_2/cascade.xml", "student_mask_data", "Mask Trainner")

# ------Add student data-------
    def add_data(self):
        active = 1
        if self.var_std_name.get() == "" or self.var_std_phone.get() == "" or self.var_std_email.get() == "" or self.var_programme.get() == "Select Programme" or self.var_course.get() == "Select Course Code" or self.var_exam_hall.get() == "Select Hall" or self.var_seat_no == "Select Seat":
            messagebox.showerror(
                "Error", "All Field are required", parent=master)
        else:
            try:
                conn = mysql.connector.connect(host='localhost',
                                               database='examination_attendance',
                                               user='root',
                                               password='root')
                if conn.is_connected():
                    db_Info = conn.get_server_info()
                    print("Connected to MySQL Server version ", db_Info)
                    cursor = conn.cursor()
                    cursor.execute("Insert into student_examination_list (name,gender,phone,email,programme,course,hall,seat,available)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (self.var_std_name.get(), self.var_std_gender.get(
                    ), self.var_std_phone.get(), self.var_std_email.get(), self.var_programme.get(),  self.var_course.get(), self.var_exam_hall.get(), self.var_seat_no.get(), active))
                    conn.commit()
                    self.fetch_data()
                    conn.close()
                    messagebox.showinfo(
                        "Success", "Student details has been added successfully", parent=master)
                    self.reset_data()
            except Exception as e:
                messagebox.showerror("Error while connecting to MySQL", e)

# -------fetch data-------
    def fetch_data(self):
        conn = mysql.connector.connect(host='localhost',
                                       database='examination_attendance',
                                       user='root',
                                       password='root')
        if conn.is_connected():
            db_Info = conn.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * from student_examination_list WHERE available = 1")
            student_detail = cursor.fetchall()
        if len(student_detail) != 0:
            self.student_table.delete(*self.student_table.get_children())
            for i in student_detail:
                self.student_table.insert("", END, values=i)
                conn.commit()
            conn.close()

# -------get cursor-------
    def get_cursor(self, event=""):
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        data = content["values"]

        self.var_std_id.set(data[0])
        self.var_std_name.set(data[1])
        self.var_std_gender.set(data[2])
        self.var_std_phone.set(data[3])
        self.var_std_email.set(data[4])
        self.var_programme.set(data[5])
        self.var_course.set(data[6])
        self.var_exam_hall.set(data[7])
        self.var_seat_no.set(data[8])

# ------Update student data------
    def update_data(self):
        if self.var_std_name.get() == "" or self.var_std_phone.get() == "" or self.var_std_email.get() == "" or self.var_programme.get() == "Select Programme" or self.var_course.get() == "Select Course Code" or self.var_exam_hall.get() == "Select Hall" or self.var_seat_no == "Select Seat":
            messagebox.showerror(
                "Update Error", "Please select the record need to be change and cannot be empty. ", parent=master)
        else:
            try:
                Update = messagebox.askyesno(
                    "Update", "Are you sure you want to update the details?", parent=master)
                if Update > 0:
                    conn = mysql.connector.connect(host='localhost',
                                                   database='examination_attendance',
                                                   user='root',
                                                   password='root')
                    cursor = conn.cursor()
                    cursor.execute("Update student_examination_list set name=%s,gender=%s,phone=%s,email=%s, programme=%s, course=%s, hall =%s, seat=%s where student_id=%s", (self.var_std_name.get(), self.var_std_gender.get(
                    ), self.var_std_phone.get(), self.var_std_email.get(), self.var_programme.get(),  self.var_course.get(), self.var_exam_hall.get(), self.var_seat_no.get(), self.var_std_id.get()))
                else:
                    if not Update:
                        return
                messagebox.showinfo(
                    "Success", "Student details has been updated successfully", parent=master)
                conn.commit()
                self.fetch_data()
                conn.close()
                self.reset_data()
            except Exception as e:
                messagebox.showerror("Error while connecting to MySQL", e)

# ------Delete student data------
    def delete_data(self):
        if self.var_std_id.get() == "":
            messagebox.showerror(
                "Error", "Student id must be required", parent=master)
        else:
            try:
                delete = messagebox.askyesno(
                    "Student Delete Page", "Do you sure you want to delete this student?", parent=master)
                if delete > 0:
                    connection = mysql.connector.connect(
                        host='localhost', database='examination_attendance', user='root', password='root')
                    cursor = connection.cursor()
                    sql = "Delete from student_examination_list where student_id =%s"
                    val = (self.var_std_id.get(),)
                    cursor.execute(sql, val)
                else:
                    if not delete:
                        return
                connection.commit()
                self.fetch_data()
                connection.close()
                messagebox.showinfo(
                    "Delete", "Successfully deleted student details", parent=master)
            except Exception as e:
                messagebox.showerror("Error while connecting to MySQL", e)

# ------reset function------
    def reset_data(self):
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_std_phone.set("")
        self.var_std_gender.set("Male")
        self.var_std_email.set("")
        self.var_programme.set("Select Programme")
        self.var_course.set("Select Course Code")
        self.var_exam_hall.set("Select Hall")
        self.var_seat_no.set("Select Seat")

# -------search function------
    def search_data(self):
        if self.var_com_search.get() == '' or self.var_search.get() == '':
            messagebox.showerror('Error', 'Please select option')
        else:
            try:
                connection = mysql.connector.connect(
                    host='localhost', database='examination_attendance', user='root', password='root')
                cursor = connection.cursor()
                cursor.execute("Select * from student_examination_list where " + str(
                    self.var_com_search.get())+" LIKE'%"+str(self.var_search.get()+"%'"))
                rows = cursor.fetchall()
                if len(rows) != 0:
                    self.student_table.delete(
                        *self.student_table.get_children())
                    for i in rows:
                        self.student_table.insert("", END, values=i)
                    connection.commit()
                    connection.close()
                else:
                    messagebox.showerror('Error', 'Cannot find data')
            except Exception as e:
                messagebox.showerror("Error while connecting to MySQL", e)


class TrackAttendancePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        main_frame = tk.Frame(self, width=1000, height=500,
                              bg='#191d2b').place(x=200, y=0)
        master.menu('#262626', '#191d2b')
        # ------main frame-----
        # ------Student Attendance frame-------
        student_attendance_frame = LabelFrame(main_frame, bd=2, bg="#191d2b", relief=RIDGE, text="Student Attendance Details", fg='white', font=(
            "helvetica", 10, "bold"))
        student_attendance_frame.place(x=210, y=15, width=490, height=445)

        # Calender
        cal = Calendar(student_attendance_frame, selectmode='day',
                       date_pattern='y-mm-dd')
        cal.place(x=15, y=20)

        def update_attentance_view():
            date = cal.get_date()
            ts = time.time()
            system_data = datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            if date > system_data:
                messagebox.showinfo("Date Picker Response",
                                    "Cannot more than current date!!!")
            else:
                try:
                    execute = mysql.connector.connect(
                        host='localhost', database='examination_attendance', user='root', password='root')
                    if execute.is_connected():
                        dbcursor_attend_display = execute.cursor(buffered=True)
                        checkAttendQuery = "SELECT a.student_id, a.name, a.programme, a.course, a.hall ,a.seat, b.time, b.date, b.status FROM student_examination_list a INNER JOIN attendance_records b ON a.student_id =b.student_id WHERE b.date =%s"
                        checkAttendInfo = date,
                        dbcursor_attend_display.execute(
                            checkAttendQuery, checkAttendInfo)
                        result = dbcursor_attend_display.fetchall()
                        # print(result)
                        if len(result) != 0:
                            self.PresentTable.delete(
                                *self.PresentTable.get_children())
                            for row in result:
                                self.PresentTable.insert(
                                    '', END, values=row)
                        else:
                            self.PresentTable.delete(
                                *self.PresentTable.get_children())

                        # For absent view
                        dbcursor_attendance_display = execute.cursor(
                            buffered=True)
                        checkAttendanceQuery = "SELECT a.student_id, a.name, a.programme, a.course, a.hall, a.seat FROM student_examination_list a WHERE a.available = 1 AND NOT EXISTS (SELECT * FROM attendance_records b WHERE b.student_id = a.student_id AND b.date =%s)"
                        checkAttendanceInfo = date,
                        dbcursor_attendance_display.execute(
                            checkAttendanceQuery, checkAttendanceInfo)
                        result = dbcursor_attendance_display.fetchall()
                        # print result
                        if len(result) != 0:
                            self.AbsentTable.delete(
                                *self.AbsentTable.get_children())
                            for row in result:
                                self.AbsentTable.insert(
                                    '', END, values=row)
                        else:
                            self.AbsentTable.delete(
                                *self.AbsentTable.get_children())

                        # For total number
                        dbcursor_count_total = execute.cursor()
                        countTotalQuery = "SELECT COUNT(*) FROM student_examination_list a WHERE a.available = 1"
                        dbcursor_count_total.execute(
                            countTotalQuery)
                        countTotal = dbcursor_count_total.fetchall()
                        for countT in countTotal:
                            int(countT[0])
                        TotalNo = int(countT[0])

                        # For absent number
                        dbcursor_count_absent = execute.cursor()
                        countAbsentQuery = "SELECT COUNT(*) FROM student_examination_list a WHERE a.available = 1 AND NOT EXISTS (SELECT * FROM attendance_records b WHERE b.student_id = a.student_id AND b.date = %s)"
                        countAbsentInfo = date,
                        dbcursor_count_absent.execute(
                            countAbsentQuery, countAbsentInfo)
                        countAbsent = dbcursor_count_absent.fetchall()
                        for countAb in countAbsent:
                            int(countAb[0])
                        absentNo = int(countAb[0])

                        # For present number
                        dbcursor_count_present = execute.cursor()
                        countAttendQuery = "SELECT COUNT(*) FROM student_examination_list a WHERE a.available = 1 AND EXISTS (SELECT * FROM attendance_records b WHERE a.student_id = b.student_id AND b.date =%s )"
                        countAttendInfo = date,
                        dbcursor_count_present.execute(
                            countAttendQuery, countAttendInfo)
                        countPresent = dbcursor_count_present.fetchall()
                        for countP in countPresent:
                            int(countP[0])
                        presentNo = int(countP[0])

                        showDate.config(text="Tracking Date:" + date)
                        total_student.configure(
                            text="Total Student:" + str(TotalNo))
                        absent_student.configure(
                            text="Total Absent:" + str(absentNo))
                        present_student.configure(
                            text="Total Present:"+str(presentNo))

                        # Chart
                        Labelling = ['Present', 'Absent']
                        Values = [presentNo, absentNo]

                        fig = Figure(figsize=(3, 2), dpi=90,
                                     facecolor='grey', edgecolor='white')
                        # create a figure object
                        ax = fig.add_subplot(111)  # add an Axes to the figure
                        ax.pie(Values, radius=1, labels=Labelling,
                               autopct='%0.2f%%', textprops={'color': 'w'})

                        chart1 = FigureCanvasTkAgg(
                            fig, student_attendance_frame)
                        chart1.get_tk_widget().place(x=110, y=240)
                except mysql.connector.Error as e:
                    print("Error while connecting to MySQL", e)

        # search button
        buttonChoose = Button(student_attendance_frame, text='Search', font=(
            "helvetica", 10), width=31, height=1, border=0, fg='white', bg='#696969', command=update_attentance_view)
        buttonChoose.place(x=14, y=203)

        # Label student attendance frame
        showDate = Label(student_attendance_frame, text='Tracking Date:', fg='white', bg='#191d2b', font=(
            "helvetica", 10))
        showDate.place(x=280, y=40)

        total_student = Label(student_attendance_frame, text='Total Student:', fg='white', bg='#191d2b', font=(
            "helvetica", 10))
        total_student.place(x=280, y=90)

        absent_student = Label(student_attendance_frame, text='Total Absent:', fg='white', bg='#191d2b', font=(
            "helvetica", 10))
        absent_student.place(x=280, y=140)

        present_student = Label(student_attendance_frame, text='Total Present:', fg='white', bg='#191d2b', font=(
            "helvetica", 10))
        present_student.place(x=280, y=190)

        # Present Attendance List
        present_lbl = Label(main_frame, text='Present Attendance', fg='white', bg='#191d2b', font=(
            "helvetica", 10, "bold"))
        present_lbl.place(x=710, y=15)

        table_frame = Frame(main_frame, bd=2, relief=RIDGE, bg="#00FA9A")
        table_frame.place(x=710, y=40, width=475, height=195)

        # --------scroll bar table -------
        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)

        self.PresentTable = Treeview(table_frame, column=("sid", "name", "course", "subject", "hall",
                                     "seat_no", "time", "date", "status"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.PresentTable.xview)
        scroll_y.config(command=self.PresentTable.yview)

        self.PresentTable.heading("sid", text="Student ID")
        self.PresentTable.heading("name", text="Name")
        self.PresentTable.heading("course", text="Course")
        self.PresentTable.heading("subject", text="Subject")
        self.PresentTable.heading("hall", text="Hall")
        self.PresentTable.heading("seat_no", text="Seat No")
        self.PresentTable.heading("time", text="Time")
        self.PresentTable.heading("date", text="Date")
        self.PresentTable.heading("status", text="Attendance Status")

        self.PresentTable["show"] = "headings"

        self.PresentTable.column("sid", width=100, anchor=CENTER)
        self.PresentTable.column("name", width=100, anchor=CENTER)
        self.PresentTable.column(
            "course", width=100, anchor=CENTER)
        self.PresentTable.column("subject", width=100, anchor=CENTER)
        self.PresentTable.column("hall", width=100, anchor=CENTER)
        self.PresentTable.column("seat_no", width=100, anchor=CENTER)
        self.PresentTable.column("time", width=100, anchor=CENTER)
        self.PresentTable.column("date", width=100, anchor=CENTER)
        self.PresentTable.column("status", width=100, anchor=CENTER)

        self.PresentTable.pack(fill=BOTH, expand=1)

        self.PresentTable.bind("<ButtonRelease>")

        # Absent Attendance List
        absent_lbl = Label(main_frame, text='Absent Attendance', fg='white', bg='#191d2b', font=(
            "helvetica", 10, "bold"))
        absent_lbl.place(x=710, y=238)

        table_1_frame = Frame(main_frame, bd=2, relief=RIDGE, bg="#DC143C")
        table_1_frame.place(x=710, y=265, width=475, height=195)

        # --------scroll bar table -------
        scroll_x = Scrollbar(table_1_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_1_frame, orient=VERTICAL)

        self.AbsentTable = Treeview(table_1_frame, column=(
            "sid", "name", "course", "subject", "hall", "seat_no"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.AbsentTable.xview)
        scroll_y.config(command=self.AbsentTable.yview)

        self.AbsentTable.heading("sid", text="Student ID")
        self.AbsentTable.heading("name", text="Name")
        self.AbsentTable.heading("course", text="Course")
        self.AbsentTable.heading("subject", text="Subject")
        self.AbsentTable.heading("hall", text="Hall")
        self.AbsentTable.heading("seat_no", text="Seat No")

        self.AbsentTable["show"] = "headings"

        self.AbsentTable.column("sid", width=100, anchor=CENTER)
        self.AbsentTable.column("name", width=100, anchor=CENTER)
        self.AbsentTable.column("course", width=100, anchor=CENTER)
        self.AbsentTable.column("subject", width=100, anchor=CENTER)
        self.AbsentTable.column("hall", width=100, anchor=CENTER)
        self.AbsentTable.column("seat_no", width=100, anchor=CENTER)

        self.AbsentTable.pack(fill=BOTH, expand=1)

        self.AbsentTable.bind("<ButtonRelease>")

        master.shutdown(main_frame, 1150, 465)
        self.pack(fill=BOTH, expand=True)


if __name__ == "__main__":
    app = Main()
    app.mainloop()
