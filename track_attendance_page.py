# Import required Libraries
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from doctest import master
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox, Treeview
from tkcalendar import *
import mysql.connector
from take_picture import *

class TrackAttendancePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        main_frame = tk.Frame(self, width=1000, height=500,
                              bg='#191d2b').place(x=200, y=0)
        master.menu('#262626', '#191d2b')
        # ------main frame-----
        self.var_com_search = StringVar()
        self.var_search = StringVar()
        # ------Student Attendance frame-------
        student_attendance_frame = LabelFrame(main_frame, bd=2, bg="#191d2b", relief=RIDGE, text="Student Attendance Details", fg='white', font=(
            "helvetica", 10, "bold"))
        student_attendance_frame.place(x=210, y=15, width=980, height=445)

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
                        dbcursor_attend_display = execute.cursor(
                            buffered=True)
                        checkAttendQuery = "SELECT a.student_id, a.name, a.programme, a.course, a.hall ,a.seat, b.time, b.date FROM student_examination_list a INNER JOIN attendance_records b ON a.student_id =b.student_id WHERE b.date =%s"
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

                        showDate.config(text="Tracking Date: " + date)
                        total_student.configure(
                            text="Total Student: " + str(TotalNo))
                        absent_student.configure(
                            text="Absent: " + str(absentNo))
                        present_student.configure(
                            text="Present: "+str(presentNo))

                        # Chart
                        Labelling = ['Present', 'Absent']
                        Values = [presentNo, absentNo]

                        fig = Figure(figsize=(2.8, 2), dpi=80,
                                     facecolor='grey', edgecolor='white')
                        # add a title to the figure
                        fig.suptitle('Based on tracking date',
                                     fontsize=10)
                        # add an Axes to the figure
                        ax = fig.add_subplot(111)
                        ax.pie(Values, radius=1, labels=Labelling,
                               autopct='%0.2f%%', textprops={'color': 'w'})

                        chart1 = FigureCanvasTkAgg(
                            fig, student_attendance_frame)
                        chart1.get_tk_widget().place(x=15, y=240)
                except mysql.connector.Error as e:
                    print("Error while connecting to MySQL", e)

        def filter_present_attendance():
            date = cal.get_date()
            search_item = self.var_com_search.get()
            search_value = self.var_search.get()
            if search_item == '' or search_value == '':
                messagebox.showerror('Error', 'Please select filter option')
            else:
                try:
                    execute = mysql.connector.connect(
                        host='localhost', database='examination_attendance', user='root', password='root')
                    if execute.is_connected():
                        dbcursor_attend_display = execute.cursor(
                            buffered=True)
                        checkAttendQuery = "SELECT a.student_id, a.name, a.programme, a.course, a.hall ,a.seat, b.time, b.date FROM student_examination_list a INNER JOIN attendance_records b ON a.student_id =b.student_id WHERE " + str(
                            search_item)+" LIKE'%"+str(search_value + "%' AND b.date =%s")
                        checkAttendInfo = date,
                        dbcursor_attend_display.execute(
                            checkAttendQuery, checkAttendInfo)
                        result = dbcursor_attend_display.fetchall()
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
                        checkAttendanceQuery = "SELECT a.student_id, a.name, a.programme, a.course, a.hall, a.seat FROM student_examination_list a WHERE " + str(search_item) + " LIKE '%" + str(
                            search_value)+"%' AND a.available = 1 AND NOT EXISTS (SELECT * FROM attendance_records b WHERE b.student_id = a.student_id AND b.date =%s)"
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
                        countTotalQuery = "SELECT COUNT(*) FROM student_examination_list a WHERE  " + str(search_item) + " LIKE '%" + str(
                            search_value)+"%' AND a.available = 1"
                        dbcursor_count_total.execute(
                            countTotalQuery)
                        countTotal = dbcursor_count_total.fetchall()
                        for countT in countTotal:
                            int(countT[0])
                        TotalNo = int(countT[0])

                        # For absent number
                        dbcursor_count_absent = execute.cursor()
                        countAbsentQuery = "SELECT COUNT(*) FROM student_examination_list a WHERE " + str(search_item) + " LIKE '%" + str(
                            search_value)+"%' AND a.available = 1 AND NOT EXISTS (SELECT * FROM attendance_records b WHERE b.student_id = a.student_id AND b.date = %s)"
                        countAbsentInfo = date,
                        dbcursor_count_absent.execute(
                            countAbsentQuery, countAbsentInfo)
                        countAbsent = dbcursor_count_absent.fetchall()
                        for countAb in countAbsent:
                            int(countAb[0])
                        absentNo = int(countAb[0])

                        # For present number
                        dbcursor_count_present = execute.cursor()
                        countAttendQuery = "SELECT COUNT(*) FROM student_examination_list a WHERE " + str(search_item) + " LIKE '%" + str(
                            search_value)+"%' AND a.available = 1 AND EXISTS (SELECT * FROM attendance_records b WHERE a.student_id = b.student_id AND b.date =%s )"
                        countAttendInfo = date,
                        dbcursor_count_present.execute(
                            countAttendQuery, countAttendInfo)
                        countPresent = dbcursor_count_present.fetchall()
                        for countP in countPresent:
                            int(countP[0])
                        presentNo = int(countP[0])

                        # -------filter frame-------
                        Filter_frame = LabelFrame(student_attendance_frame, bd=2, bg="#191d2b", relief=RIDGE, text="Filter Options", fg="white", font=(
                            "helvetica", 10, "bold"))
                        Filter_frame.place(x=270, y=145, width=175, height=80)

                        filter_total = Label(Filter_frame, text='Total Student:', fg='white', bg='#191d2b', font=(
                            "helvetica", 10))
                        filter_total.place(x=0, y=5)

                        filter_present = Label(Filter_frame, text='Present:', fg='white', bg='#191d2b', font=(
                            "helvetica", 10))
                        filter_present.place(x=0, y=25)

                        filter_absent = Label(Filter_frame, text='Absent:', fg='white', bg='#191d2b', font=(
                            "helvetica", 10))
                        filter_absent.place(x=90, y=25)

                        filter_total.configure(
                            text="Total Student: " + str(TotalNo))
                        filter_absent.configure(
                            text="Absent: " + str(absentNo))
                        filter_present.configure(
                            text="Present: "+str(presentNo))

                        # Chart
                        Labelling = ['Present', 'Absent']
                        Values = [presentNo, absentNo]

                        fig = Figure(figsize=(2.8, 2), dpi=80,
                                     facecolor='grey', edgecolor='white')
                        # add title to the figure
                        fig.suptitle('Based on filter option', fontsize=10)
                        # add an Axes to the figure
                        ax = fig.add_subplot(111)
                        ax.pie(Values, radius=1, labels=Labelling,
                               autopct='%0.2f%%', textprops={'color': 'w'})

                        chart1 = FigureCanvasTkAgg(
                            fig, student_attendance_frame)
                        chart1.get_tk_widget().place(x=220, y=240)
                    else:
                        messagebox.showerror('Error', 'Cannot find data')
                except Exception as e:
                    messagebox.showerror("Error while connecting to MySQL", e)

        # check button
        buttonChoose = Button(student_attendance_frame, text='Check', font=(
            "helvetica", 10), width=31, height=1, border=0, fg='white', bg='#696969', command=update_attentance_view)
        buttonChoose.place(x=14, y=203)

        # Label student attendance frame
        showDate = Label(student_attendance_frame, text='Tracking Date:', fg='white', bg='#191d2b', font=(
            "helvetica", 10))
        showDate.place(x=280, y=45)

        total_student = Label(student_attendance_frame, text='Total Student:', fg='white', bg='#191d2b', font=(
            "helvetica", 10))
        total_student.place(x=280, y=85)

        present_student = Label(student_attendance_frame, text='Present:', fg='white', bg='#191d2b', font=(
            "helvetica", 10))
        present_student.place(x=280, y=105)

        absent_student = Label(student_attendance_frame, text='Absent:', fg='white', bg='#191d2b', font=(
            "helvetica", 10))
        absent_student.place(x=370, y=105)

        # ------search frame-------
        Search_frame = LabelFrame(student_attendance_frame, bd=2, bg="#191d2b", relief=RIDGE, text="Filter Attendance", fg="white", font=(
            "helvetica", 10, "bold"))
        Search_frame.place(x=450, y=0, width=521, height=418)

        search_label = Label(Search_frame, text="Filter Option:", font=(
            "helvetica", 10, "bold"), bg="#191d2b", fg="white")
        search_label.place(x=6, y=10)

        search_combo = Combobox(Search_frame, textvariable=self.var_com_search, font=(
            "helvetica", 10), state="readonly")
        search_combo["values"] = (
            "Select", "programme", "course", "hall")
        search_combo.current(0)
        search_combo.place(x=100, y=10, width=150, height=25)

        Search_entry = Entry(Search_frame, textvariable=self.var_search, font=(
            "helvetica", 10))
        Search_entry.place(x=260, y=10, width=120, height=25)

        btn_frame_search = Frame(Search_frame, highlightbackground="#F4A460",
                                 highlightthickness=2, bd=0, relief=RIDGE, bg="#F4A460")
        btn_frame_search.place(x=390, y=8, width=110, height=30)

        search_btn = Button(btn_frame_search, text="F I L T E R",
                            width=15, bg="black", fg="#F4A460", command=filter_present_attendance)
        search_btn.pack()

        # Present Attendance List
        present_lbl = Label(Search_frame, text='Present Attendance', fg='white', bg='#191d2b', font=(
            "helvetica", 10, "bold"))
        present_lbl.place(x=6, y=35)

        table_frame = Frame(Search_frame, bd=2,
                            relief=RIDGE, bg="#00FA9A")
        table_frame.place(x=10, y=55, width=495, height=160)

        # --------scroll bar table -------
        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)

        self.PresentTable = Treeview(table_frame, column=("sid", "name", "programme", "course", "hall",
                                     "seat_no", "time", "date", "status"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.PresentTable.xview)
        scroll_y.config(command=self.PresentTable.yview)

        self.PresentTable.heading("sid", text="Student ID")
        self.PresentTable.heading("name", text="Name")
        self.PresentTable.heading("programme", text="Programme")
        self.PresentTable.heading("course", text="Course")
        self.PresentTable.heading("hall", text="Hall")
        self.PresentTable.heading("seat_no", text="Seat No")
        self.PresentTable.heading("time", text="Time")
        self.PresentTable.heading("date", text="Date")

        self.PresentTable["show"] = "headings"

        self.PresentTable.column("sid", width=100, anchor=CENTER)
        self.PresentTable.column("name", width=100, anchor=CENTER)
        self.PresentTable.column(
            "programme", width=100, anchor=CENTER)
        self.PresentTable.column("course", width=100, anchor=CENTER)
        self.PresentTable.column("hall", width=100, anchor=CENTER)
        self.PresentTable.column("seat_no", width=100, anchor=CENTER)
        self.PresentTable.column("time", width=100, anchor=CENTER)
        self.PresentTable.column("date", width=100, anchor=CENTER)

        self.PresentTable.pack(fill=BOTH, expand=1)

        self.PresentTable.bind("<ButtonRelease>")

        # Absent Attendance List
        absent_lbl = Label(Search_frame, text='Absent Attendance', fg='white', bg='#191d2b', font=(
            "helvetica", 10, "bold"))
        absent_lbl.place(x=6, y=215)

        table_1_frame = Frame(Search_frame,
                              bd=2, relief=RIDGE, bg="#DC143C")
        table_1_frame.place(x=10, y=235, width=495, height=160)

        # --------scroll bar table -------
        scroll_x = Scrollbar(table_1_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_1_frame, orient=VERTICAL)

        self.AbsentTable = Treeview(table_1_frame, column=(
            "sid", "name", "programme", "course", "hall", "seat_no"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.AbsentTable.xview)
        scroll_y.config(command=self.AbsentTable.yview)

        self.AbsentTable.heading("sid", text="Student ID")
        self.AbsentTable.heading("name", text="Name")
        self.AbsentTable.heading("programme", text="Programme")
        self.AbsentTable.heading("course", text="Course")
        self.AbsentTable.heading("hall", text="Hall")
        self.AbsentTable.heading("seat_no", text="Seat No")

        self.AbsentTable["show"] = "headings"

        self.AbsentTable.column("sid", width=100, anchor=CENTER)
        self.AbsentTable.column("name", width=100, anchor=CENTER)
        self.AbsentTable.column("programme", width=100, anchor=CENTER)
        self.AbsentTable.column("course", width=100, anchor=CENTER)
        self.AbsentTable.column("hall", width=100, anchor=CENTER)
        self.AbsentTable.column("seat_no", width=100, anchor=CENTER)

        self.AbsentTable.pack(fill=BOTH, expand=1)

        self.AbsentTable.bind("<ButtonRelease>")

        master.shutdown(main_frame, 1150, 465)
        self.pack(fill=BOTH, expand=True)