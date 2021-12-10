import tkinter
import os
import sys
import time
import requests
import datetime
from tkinter import messagebox
import random

ip_adress = "192.168.0.0"
start_year = 2019
start_month = 1
start_day = 10
app_name = "Uzaktan Devam Ders Defteri Paneli"
is_32Bit = False
version = "Alpha 1.3"

x32 = " x32" if is_32Bit else " x64"
version_full = version + x32
app_width = 600
app_height = 540
shift_right = 0
shift_down = -100
app_description = ""

class Date_Manager(tkinter.Frame):
    today = datetime.datetime.now()
    days_of_months = {
        1 : 31,
        2 : 29,
        3 : 31,
        4 : 30,
        5 : 31,
        6 : 30,
        7 : 31,
        8 : 31,
        9 : 30,
        10 : 31,
        11 : 30,
        12 : 31
        }
    names_of_weekdays = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

    years = [x for x in range(start_year, today.year + 1)]
    months_of_this_year = [x for x in range(start_month if today.year == start_year else 1, today.month + 1)]
    days_of_this_month = [x for x in range(start_day if today.year == start_year and today.month == start_month else 1, today.day + 1)]
            
    def __init__(self, parent, start_year, start_month, start_day):
        self.parent = parent
        tkinter.Frame.__init__(self, self.parent)
        self.tracer_list = []
        
        self.start_year = start_year
        self.start_month = start_month
        self.start_day = start_day
        
        self.months_of_start_year = [x for x in range(self.start_month, (self.today.month if self.start_year == self.today.year else 12) + 1)]
        y = self.today.day if self.start_year == self.today.year and self.start_month == self.today.month else self.days_of_months[self.start_month]
        if self.start_year % 4 == 0 and self.start_month == 2: y += 1
        self.days_of_start_month = [x for x in range(self.start_day, y + 1)]

        self.year_var = tkinter.IntVar(parent, self.today.year)
        self.month_var = tkinter.IntVar(parent, self.today.month)
        self.day_var = tkinter.IntVar(parent, self.today.day)

        self.WeekdayTeller = tkinter.Label(self)
        self.WeekdayTeller.grid(row = 0, column = 0, columnspan = 3, sticky = "W")
        self.day_var.trace("w", self.DayTracer)
        self.day_var.set(self.today.day)

        self.active_days = self.days_of_this_month
        self.active_months = self.months_of_this_year
        self.active_years = self.years

        self.OptionMenu_day = tkinter.OptionMenu(self, self.day_var, *self.active_days)
        self.OptionMenu_month = tkinter.OptionMenu(self, self.month_var, *self.active_months, command = self.update_day)
        self.OptionMenu_year = tkinter.OptionMenu(self, self.year_var, *self.active_years, command = self.update_month)
        self.OptionMenu_day.grid(row = 1, column = 0)
        self.OptionMenu_month.grid(row = 1, column = 1)
        self.OptionMenu_year.grid(row = 1, column = 2)

    def update_month(self, year):
        if year == self.start_year:
            self.active_months = self.months_of_start_year
        elif year == self.today.year:
            self.active_months = self.months_of_this_year
        else:
            self.active_months = [x for x in range(1, 12 + 1)]
        self.OptionMenu_month.destroy()
        if self.month_var.get() < self.active_months[0]:
            self.month_var.set(self.active_months[0])
        elif self.month_var.get() > self.active_months[-1]:
            self.month_var.set(self.active_months[-1])
        else:
            self.month_var.set(self.month_var.get())
        self.OptionMenu_month = tkinter.OptionMenu(self, self.month_var, *self.active_months, command = self.update_day)
        self.OptionMenu_month.grid(row = 1, column = 1)
        self.update_day(self.month_var.get())

    def update_day(self, month):
        if month == self.start_month and self.year_var.get() == self.start_year:
            self.active_days = self.days_of_start_month
        elif month == self.today.month and self.year_var.get() == self.today.year:
            self.active_days = self.days_of_this_month
        else:
            self.active_days = [x for x in range(1, self.days_of_months[month] + 1)]
        self.OptionMenu_day.destroy()
        if self.day_var.get() < self.active_days[0]:
            self.day_var.set(self.active_days[0])
        elif self.day_var.get() > self.active_days[-1]:
            self.day_var.set(self.active_days[-1])
        else:
            self.day_var.set(self.day_var.get())
        if self.year_var.get() % 4 != 0 and self.month_var.get() == 2 and 29 in self.active_days:
            self.active_days = self.active_days[:-1]
        self.OptionMenu_day = tkinter.OptionMenu(self, self.day_var, *self.active_days)
        self.OptionMenu_day.grid(row = 1, column = 0)

    def DayTracer(self, a, b, c):
        self.WeekdayTeller.config(text = self.names_of_weekdays[datetime.datetime(self.year_var.get(), self.month_var.get(), self.day_var.get()).weekday()])
        date = self.get_date()
        for function in self.tracer_list:
            function(date)

    def get_date(self):
        return (str(self.day_var.get()), str(self.month_var.get()), str(self.year_var.get()))

    def set_tracer(self, function):
        self.tracer_list.append(function)
        return self.get_date()

class Change_Password(tkinter.Toplevel):
    def __init__(self, parent):
        self.parent = parent
        tkinter.Toplevel.__init__(self, self.parent)

        self.width = 300
        self.height = 80

        self.title("Şifre Değiştir")
        x = (self.winfo_screenwidth() // 2) - (self.width // 2) + shift_right + (Attandee_Editor.width // 2) - (Profile_Manager.width // 2)
        y = (self.winfo_screenheight() // 2) - (self.height // 2) + shift_down - 100
        self.geometry('{}x{}+{}+{}'.format(self.width, self.height, x, y))

        cover_frame = tkinter.Frame(self)
        top_frame = tkinter.Frame(cover_frame)
        tkinter.Label(top_frame, text = "Eski Şifre: ").pack(side = "left")
        self.old_password_entry = tkinter.Entry(top_frame, width = 7, show = "*")
        self.old_password_entry.pack(side = "left")
        tkinter.Label(top_frame, text = "Yeni Şifre: ").pack(side = "left")
        self.new_password_entry = tkinter.Entry(top_frame, width = 7, show = "*")
        self.new_password_entry.pack(side = "left")
        top_frame.pack()
        down_frame = tkinter.Frame(cover_frame)
        tkinter.Button(down_frame, text = "Gönder", command = self.change_password).pack(side = "left")
        tkinter.Label(down_frame).pack(side = "left")
        tkinter.Button(down_frame, text = "İptal", command = self.cancel).pack(side = "left")
        down_frame.pack()
        cover_frame.pack()
        self.message_display = tkinter.Label(self)
        self.message_display.pack()

    def change_password(self):
        old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()
        if not new_password or not old_password:
            self.message_display.config(text = "Şifre girdileri boş bırakılamaz.")
            return
        user = user_manager.get_active_user()
        username = user.username
        password = user.password
        if old_password != password:
            self.message_display.config(text = "Şifre hatalı.")
            return
        message = send_message("command/change_password~{}~{}~{}".replace("~", split_char).format(username, old_password, new_password)).text.split(split_char)
        successful = False
        while message:
            action = message.pop(0)
            if action == "message":
                server_message = message.pop(0)
                self.message_display.config(text = server_message)
            elif action == "success": 
                successful = True
                user.password = new_password
        if successful:
            self.parent.message_display.config(text = "Şifreniz değiştirilmiştir.")
            self.destroy()

    def cancel(self):
        self.destroy()

class Send_Message(tkinter.Toplevel):
    def __init__(self, parent):
        self.parent = parent
        tkinter.Toplevel.__init__(self, self.parent)

        self.width = 300
        self.height = 80

        self.title("Mesaj Gönder")
        x = (self.winfo_screenwidth() // 2) - (self.width // 2) + shift_right + (Attandee_Editor.width // 2) - (Profile_Manager.width // 2)
        y = (self.winfo_screenheight() // 2) - (self.height // 2) + shift_down - 100
        self.geometry('{}x{}+{}+{}'.format(self.width, self.height, x, y))

        cover_frame = tkinter.Frame(self)
        top_frame = tkinter.Frame(cover_frame)
        tkinter.Label(top_frame, text = "Mesajınız: ").pack(side = "left")
        self.message_entry = tkinter.Entry(top_frame, width = 20)
        self.message_entry.pack(side = "left")
        top_frame.pack()
        down_frame = tkinter.Frame(cover_frame)
        tkinter.Button(down_frame, text = "Gönder", command = self.send_message).pack(side = "left")
        tkinter.Label(down_frame).pack(side = "left")
        tkinter.Button(down_frame, text = "İptal", command = self.cancel).pack(side = "left")
        down_frame.pack()
        cover_frame.pack()
        self.message_display = tkinter.Label(self)
        self.message_display.pack()

    def send_message(self):
        message = self.message_entry.get()
        if not message:
            self.message_display.config(text = "Mesaj girdisi boş bırakılamaz.")
            return
        user = user_manager.get_active_user()
        username = user.username
        password = user.password
        date = "-".join(Date_Manager(self, start_year, start_month, start_day).get_date())
        message = "{}: {}&{}".format(user.teacher, message, date)
        message = send_message("command/send_message~{}~{}~{}~{}".replace("~", split_char).format(username, password, message, date)).text.split(split_char)
        successful = False
        while message:
            action = message.pop(0)
            if action == "message":
                server_message = message.pop(0)
                self.message_display.config(text = server_message)
            elif action == "success": 
                successful = True
        if successful:
            self.parent.message_display.config(text = "Mesajınız idareye gönderilmiştir.")
            self.destroy()

    def cancel(self):
        self.destroy()

class Change_Student(tkinter.Toplevel):
    def __init__(self, parent, student):
        self.parent = parent
        tkinter.Toplevel.__init__(self, self.parent)

        self.width = 340
        self.height = 80

        self.title("Öğrenci Bilgilerini Düzenle")
        x = (self.winfo_screenwidth() // 2) - (self.width // 2) + shift_right + (Attandee_Editor.width // 2) - (Profile_Manager.width // 2)
        y = (self.winfo_screenheight() // 2) - (self.height // 2) + shift_down - 100
        self.geometry('{}x{}+{}+{}'.format(self.width, self.height, x, y))

        self.student = student

        cover_frame = tkinter.Frame(self)
        top_frame = tkinter.Frame(cover_frame)
        tkinter.Label(top_frame, text = "İsim Soyisim: ").pack(side = "left")
        self.student_name_entry = tkinter.Entry(top_frame, width = 18)
        self.student_name_entry.insert(0, self.student.name)
        self.student_name_entry.pack(side = "left")
        tkinter.Label(top_frame, text = "Numara: ").pack(side = "left")
        self.student_number_entry = tkinter.Entry(top_frame, width = 5)
        self.student_number_entry.insert(0, self.student.number)
        self.student_number_entry.pack(side = "left")
        top_frame.pack()
        down_frame = tkinter.Frame(cover_frame)
        tkinter.Button(down_frame, text = "Kaydet", command = self.change_student).pack(side = "left")
        tkinter.Label(down_frame).pack(side = "left")
        tkinter.Button(down_frame, text = "İptal", command = self.cancel).pack(side = "left")
        down_frame.pack()
        cover_frame.pack()
        self.message_display = tkinter.Label(self)
        self.message_display.pack()

    def change_student(self):
        student_name = self.student_name_entry.get()
        student_number = self.student_number_entry.get()
        if not student_name or not student_number:
            self.message_display.config(text = "Öğrenci bilgileri boş bırakılamaz.")
            return
        self.student.name = student_name
        self.student.number = student_number
        self.parent.parent.master.master.refresh_student_list_selector()
        self.destroy()

    def cancel(self):
        self.destroy()

class Classes_Manager(tkinter.Frame):
    def __init__(self, parent, date_manager):
        self.parent = parent
        tkinter.Frame.__init__(self, self.parent)
        self.date_manager = date_manager
        self.user = user_manager.get_active_user()

        height = 300
        width = 460
        self.padx = 4
        self.pady = 2

        canvas_frame = tkinter.Frame(self)

        self.canvas = tkinter.Canvas(canvas_frame)

        scrollbar = tkinter.Scrollbar(canvas_frame, orient = "vertical", command = self.canvas.yview)
        self.canvas.configure(yscrollcommand = scrollbar.set)

        self.attandee_sheets_display = tkinter.Frame(self.canvas, padx = self.padx)
        self.attandee_sheets_display.bind("<Configure>", lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all"), width = max(self.attandee_sheets_display.winfo_width(), width), height = height))
        self.canvas.create_window((0, 0), window = self.attandee_sheets_display, anchor = "nw")

        self.canvas.bind_all("<MouseWheel>", self.mousewheel)

        self.canvas.pack(side="left", fill = "y")
        scrollbar.pack(side="left", fill = "y")

        canvas_frame.pack()
        
        tkinter.Label(self).pack()
        tkinter.Button(self, text = "Yeni Yoklama", command = self.create_new).pack()
        
        self.update_date(self.date_manager.set_tracer(self.update_date))

    def update_date(self, date):
        self.date = date
        self.request_attandee_sheets()
        self.update_table()

    def update_table(self):
        self.canvas.bind_all("<MouseWheel>", self.mousewheel)
        for child in self.attandee_sheets_display.winfo_children():
            child.destroy()
        attandee_sheets = user_manager.query_attandee_sheets(user = self.user, date = self.date, sort = "hour")
        text_width = 42
        if attandee_sheets:
            row = 0
            for x in range(len(attandee_sheets)):
                attandee_sheet = attandee_sheets[x]
                tkinter.Label(self.attandee_sheets_display, text = attandee_sheet.hour, padx = self.padx).grid(row = row, column = 0, sticky = "w" + "n")
                tkinter.Label(self.attandee_sheets_display, text = attandee_sheet.name, padx = self.padx).grid(row = row, column = 1, sticky = "w" + "n")
                tkinter.Label(self.attandee_sheets_display, text = attandee_sheet.classroom_name, padx = self.padx).grid(row = row, column = 2)
                row += 1
                tkinter.Label(self.attandee_sheets_display, text = "Konu: ", padx = self.padx).grid(row = row, column = 0, sticky = "w" + "n")
                cover = tkinter.Frame(self.attandee_sheets_display, pady = self.pady)
                topic_display = tkinter.Text(cover, width = text_width, height = 2, wrap = "word", bd = 0)
                topic_display.insert("insert", attandee_sheet.topic)
                topic_display.configure(font=("TkDefaultFont"), state = "disabled")
                topic_display.pack()
                cover.grid(row = row, rowspan = 2, column = 1, sticky = "w" + "n")
                cover = tkinter.Frame(self.attandee_sheets_display, padx = self.padx)
                tkinter.Button(cover, text = "Sil", command = lambda ae_id = attandee_sheet.id: self.delete_attandee_sheet(ae_id), bd = 0, fg = "red").pack(fill = "x", expand = True)
                cover.grid(row = row, column = 2, sticky = "e" + "w" + "s")
                row += 2
                tkinter.Label(self.attandee_sheets_display, text = "Gelmeyenler: ", padx = self.padx).grid(row = row, column = 0, sticky = "w" + "n")
                cover = tkinter.Frame(self.attandee_sheets_display, pady = self.pady)
                non_attandee_list_display = tkinter.Text(cover, width = text_width, height = 2, wrap = "word", bd = 0)
                non_attandee_list_display_text = ""
                for student in attandee_sheet.non_attandee_list:
                    non_attandee_list_display_text += student.number + ", "
                non_attandee_list_display.insert("insert", non_attandee_list_display_text[:-2] if non_attandee_list_display_text else "Sınıf Tam")
                non_attandee_list_display.configure(font=("TkDefaultFont"), state = "disabled")
                non_attandee_list_display.pack()
                cover.grid(row = row, rowspan = 2, column = 1, columnspan = 2, sticky = "w" + "n")
                cover = tkinter.Frame(self.attandee_sheets_display, padx = self.padx)
                tkinter.Button(cover, text = "Düzenle", command = lambda ae_id = attandee_sheet.id: self.edit_attandee_sheet(ae_id), bd = 0).pack()
                cover.grid(row = row, column = 2)
                row += 2
                tkinter.Label(self.attandee_sheets_display).grid(row = row, column = 0, sticky = "w" + "n")
                row += 1
        else:
            tkinter.Label(self.attandee_sheets_display, text = "Kayıtlı bir yoklama bulunamadı.").pack()

    def mousewheel(self, event):
        try:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except:
            pass
        
    def create_new(self):
        Attandee_Editor(self, Attandee_Sheet(self.user, self.date)).mainloop()

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def request_attandee_sheets(self):
        requested_attandee_sheet_ids = []
        requested_attandee_sheet_ids_sync_dict = dict()
        try:
            attandee_sheet_infos = self.user.attandee_sheet_info_elements[self.date]
        except KeyError:
            return
        for attandee_sheet_info in attandee_sheet_infos:
            attandee_sheet_info_id = attandee_sheet_info[0]
            attandee_sheet_info_sync = attandee_sheet_info[1]
            if attandee_sheet_info_id in user_manager.attandee_sheets and attandee_sheet_info_sync == user_manager.attandee_sheets[attandee_sheet_info_id].sync:
                continue
            else:
                requested_attandee_sheet_ids.append(attandee_sheet_info_id)
                requested_attandee_sheet_ids_sync_dict[attandee_sheet_info_id] = attandee_sheet_info_sync
        if requested_attandee_sheet_ids:
            raw_requested_attandee_sheet_ids = "-".join(requested_attandee_sheet_ids)
            message = send_message("command/get_attandee_sheets~{}~{}~{}".replace("~", split_char).format(self.user.username, self.user.password, raw_requested_attandee_sheet_ids)).text.split(split_char)
            successful = False
            while message:
                action = message.pop(0)
                if action == "attandee_sheet":
                    attandee_sheet_id = message.pop(0)
                    username = message.pop(0)
                    date = (*message.pop(0).split("-"),)
                    classroom_id = message.pop(0)
                    raw_data = message.pop(0)
                    attandee_sheet = Attandee_Sheet(self.user, date)
                    attandee_sheet.id = attandee_sheet_id
                    attandee_sheet.decode_raw_data(raw_data)
                    attandee_sheet.sync = requested_attandee_sheet_ids_sync_dict[attandee_sheet_info_id]
                    attandee_sheet.classroom_id = classroom_id
                    user_manager.attandee_sheets[attandee_sheet_id] = attandee_sheet
                elif action == "message":
                    server_message = message.pop(0)
                    self.parent.message_display.config(text = server_message)
                elif action == "success":
                    successful = True

    def edit_attandee_sheet(self, attandee_sheet_id):
        Attandee_Editor(self, user_manager.attandee_sheets[attandee_sheet_id], mode = "edit").mainloop()

    def delete_attandee_sheet(self, attandee_sheet_id):
        if not tkinter.messagebox.askokcancel(title = "Dikkat", message = "Yoklama geri döndürülemeyecek şekilde silinecektir. Silme işlemini onaylıyor musunuz ?"):
            return
        message = send_message("command/delete_attandee_sheet~{}~{}~{}".replace("~", split_char).format(self.user.username, self.user.password, attandee_sheet_id)).text.split(split_char)
        successful = False
        while message:
            action = message.pop(0)
            if action == "message":
                server_message = message.pop(0)
                self.message_display.config(text = server_message)
            elif action == "success":
                validation = message.pop(0)
                self.user.delete_from_attandee_sheet_info_dict(attandee_sheet_id)
                del user_manager.attandee_sheets[attandee_sheet_id]
                self.user.update_validation("attandee_sheet_info_dict", validation)
                successful = True
        if successful:
            self.update_table()

class Attandee_Sheet_Summary(tkinter.Frame):
    def __init__(self, parent, attandee_sheet):
        self.parent = parent
        tkinter.Frame.__init__(self, self.parent)
        self.attandee_sheet = attandee_sheet

        self.up_holder = tkinter.Frame(self)
        if self.attandee_sheet.hour:
            tkinter.Label(self.up_holder, text = "{}. Ders".format(self.attandee_sheet.hour)).pack(side = "left")
        tkinter.Label(self.up_holder, text = self.attandee_sheet.name).pack(side = "left")
        self.up_holder.grid(row = 0, column = 0, sticky = "w")
        tkinter.Label(self, text = "Sınıf: {}".format(self.attandee_sheet.classroom_name)).grid(row = 0, column = 1, sticky = "e")
        tkinter.Label(self, text = "Konu: {}".format(self.attandee_sheet.topic), anchor = "w").grid(row = 1, column = 0, sticky = "w")
        summary = ""
        for student in self.attandee_sheet.non_attandee_list:
            summary = summary + student.number + ", "
        summary = summary[:-2] if summary else "Sınıf Tam"
        tkinter.Label(self, text = "Gelmeyenler: {}".format(summary), anchor = "w").grid(row = 2, column = 0, sticky = "w")
        
class Attandee_Editor(tkinter.Toplevel):
    presentations = {"class_info" : lambda x: Attandee_Editor.ClassInfo(x),
                     "non_attandee_info" : lambda x: Attandee_Editor.Non_Attandee_Info(x)}
    width = 500
    height = 400
    class_hour_var_list = ["1. Ders", "2. Ders", "3. Ders", "4. Ders", "5. Ders", "6. Ders", "7. Ders", "8. Ders"]
    
    def __init__(self, parent, attandee_sheet, mode = ""):
        self.parent = parent
        tkinter.Toplevel.__init__(self)

        self.mode = mode
        
        self.title("Ders Defteri Editörü - " + "Yeni Yoklama" if not mode else "Görüntüle" if mode == "view" else "Düzenle")
        x = (self.winfo_screenwidth() // 2) - (app_width // 2) + shift_right - (Attandee_Editor.width // 2) - (Profile_Manager.width // 2)
        y = (self.winfo_screenheight() // 2) - (app_height // 2) + shift_down
        self.geometry('{}x{}+{}+{}'.format(self.width, self.height, x, y))

        self.attandee_sheet = attandee_sheet
        self.unsaved_non_attandee_list = self.attandee_sheet.non_attandee_list.copy()

        self.presentation = self.presentations["class_info"](self)
        self.presentation.pack()

    def changePresentation(self, prsnt):
        self.presentation.destroy()
        self.presentation = self.presentations[prsnt](self)
        self.presentation.pack()

    class ClassInfo(tkinter.Frame):
        def __init__(self, parent):
            self.parent = parent
            tkinter.Frame.__init__(self, self.parent)
            self.attandee_sheet = self.parent.attandee_sheet
            
            tkinter.Label(self).pack()
            self.table = tkinter.Frame(self)
            row = 0
            tkinter.Label(self.table, text = "Öğretmen: ").grid(row = row, column = 0, sticky = "w" + "n")
            self.teacher_entry = tkinter.Label(self.table, text = self.attandee_sheet.teacher)
            self.teacher_entry.grid(row = row, column = 1, sticky = "w")
            tkinter.Label(self.table, text = "Tarih: {}/{}/{}".format(*self.attandee_sheet.date)).grid(row = row, column = 3, sticky = "e", padx = 4)
            row += 1
            tkinter.Label(self.table).grid(row = row, column = 0)
            row += 1
            tkinter.Label(self.table, text = "Sınıf: ").grid(row = row, column = 0, sticky = "w")
            self.classroom_manager = Classroom_Manager(self.table, self.attandee_sheet.user, (self.attandee_sheet.classroom_name, self.attandee_sheet.classroom_id))
            self.classroom_manager.grid(row = row, column = 1, sticky = "w")
            row += 1
            tkinter.Label(self.table, text = "Ders Saati: ").grid(row = row, column = 0, sticky = "w")
            self.class_hour_var = tkinter.StringVar(self, self.attandee_sheet.hour)
            if self.parent.mode == "view":
                tkinter.Label(self.table, text = self.attandee_sheet.hour).grid(row = row, column = 1, sticky = "w")
            else:
                tkinter.OptionMenu(self.table, self.class_hour_var, *Attandee_Editor.class_hour_var_list).grid(row = row, column = 1, sticky = "w")
            row += 1
            tkinter.Label(self.table, text = "Ders: ").grid(row = row, column = 0, sticky = "w")
            self.class_name_var = tkinter.StringVar(self, self.attandee_sheet.name)
            if self.parent.mode == "view":
                tkinter.Label(self.table, text = self.attandee_sheet.name).grid(row = row, column = 1, sticky = "w")
            else:
                tkinter.OptionMenu(self.table, self.class_name_var, *self.attandee_sheet.user.class_names).grid(row = row, column = 1, sticky = "w")
            row += 1
            tkinter.Label(self.table, text = "Konu: ").grid(row = row, column = 0, sticky = "w")
            self.class_topic_text = tkinter.Text(self.table, width = 32, height = 4, wrap = "word")
            self.class_topic_text.configure(font=("TkDefaultFont"))
            self.class_topic_text.insert("insert", self.attandee_sheet.topic)
            self.class_topic_text.configure(state = "normal" if self.parent.mode != "view" else "disabled")
            self.class_topic_text.grid(row = row, rowspan = 2, column = 1, sticky = "w", pady = 2)
            row += 2
            tkinter.Label(self.table).grid(row = row, column = 0)
            row += 1
            tkinter.Button(self.table, text = "İlerle" if self.parent.mode != "view" else "Gelmeyenler", command = self.next_page, padx = 4).grid(row = row, column = 3)
            row += 1
            tkinter.Label(self.table).grid(row = row, column = 0)
            
            self.table.pack()
            
            self.message_display = tkinter.Label(self, text = "")
            self.message_display.pack()

        def next_page(self):
            self.message_display.config(text = "")
            
            classroom = self.classroom_manager.get_classroom()#(id, name)
            
            if self.parent.mode != "view" and not classroom and not tkinter.messagebox.askokcancel(title = "Dikkat", message = "Sınıf seçilmedi. Sınıf seçimi değiştirilemez. Devam etmek istiyor musunuz ?"):
                return
            if classroom:
                self.attandee_sheet.classroom_id = classroom[0]
                self.attandee_sheet.classroom_name = classroom[1]
            else:
                self.attandee_sheet.classroom_name = " "
            
            name = self.class_name_var.get()
            if self.parent.mode != "view" and not name and not tkinter.messagebox.askokcancel(title = "Dikkat", message = "Ders girilmedi. Devam etmek istiyor musunuz ?"):
                return
            self.attandee_sheet.name = name

            hour = self.class_hour_var.get()
            if self.parent.mode != "view" and not hour and not tkinter.messagebox.askokcancel(title = "Dikkat", message = "Ders saati seçilmedi. Devam etmek istiyor musunuz ?"):
                return
            self.attandee_sheet.hour = hour

            topic = self.class_topic_text.get("1.0",'end-1c')
            if self.parent.mode != "view" and not topic and not tkinter.messagebox.askokcancel(title = "Dikkat", message = "Konu girilmedi. Devam etmek istiyor musunuz ?"):
                return
            self.attandee_sheet.topic = topic

            self.parent.changePresentation("non_attandee_info")

    class Non_Attandee_Info(tkinter.Frame):
        def __init__(self, parent):
            self.parent = parent
            tkinter.Frame.__init__(self, self.parent)
            self.attandee_sheet = self.parent.attandee_sheet

            padx = 4
            tkinter.Label(self).pack()
            class_info_display = tkinter.Frame(self)
            tkinter.Label(class_info_display, text = self.attandee_sheet.classroom_name, padx = padx).pack(side = "left")
            tkinter.Label(class_info_display, text = self.attandee_sheet.name, padx = padx).pack(side = "left")
            tkinter.Label(class_info_display, text = self.attandee_sheet.hour, padx = padx).pack(side = "left")
            tkinter.Label(class_info_display, text = "Tarih: {}/{}/{}".format(*self.attandee_sheet.date), padx = padx).pack(side = "right")
            class_info_display.pack(expand = True, fill = "x")
            tkinter.Label(self).pack()
            self.non_attandee_list_selector = Non_Attandee_List_Manager(self)
            self.non_attandee_list_selector.pack()
            tkinter.Label(self, text = "Gelmeyen öğrencileri işaretleyiniz.").pack(anchor = "w")
            tkinter.Label(self).pack()
            buttons_frame = tkinter.Frame(self)
            if self.parent.mode != "view":
                tkinter.Button(buttons_frame, text = "Gönder", command = self.send_attandee_sheet).pack(side = "right")
            else:
                tkinter.Button(buttons_frame, text = "Çıkış", command = self.exit).pack(side = "right")
            tkinter.Button(buttons_frame, text = "Geri Dön", command = self.return_to_menu).pack(side = "left")
            buttons_frame.pack(fill = "x")
            self.message_display = tkinter.Label(self)
            self.message_display.pack()

        def send_attandee_sheet(self):
            self.message_display.config(text = "")
            
            self.attandee_sheet.non_attandee_list = self.non_attandee_list_selector.non_attandee_list
            
            attandee_sheet_message = self.attandee_sheet.prepare_message()
            if self.parent.mode != "edit":
                message = send_message("command/send_attandee_sheet~{}".replace("~", split_char).format(attandee_sheet_message)).text.split(split_char)
            else:
                message = send_message("command/replace_attandee_sheet~{}~{}".replace("~", split_char).format(attandee_sheet_message, self.attandee_sheet.id)).text.split(split_char)
            successful = False
            while message:
                action = message.pop(0)
                if action == "message":
                    server_message = message.pop(0)
                    self.message_display.config(text = server_message)
                elif action == "success":
                    if self.parent.mode != "edit": self.attandee_sheet.id = message.pop(0)
                    self.attandee_sheet.sync = "1" if self.parent.mode != "edit" else message.pop(0)
                    validation = message.pop(0)
                    if self.parent.mode != "edit": user_manager.add_attandee_sheet(self.attandee_sheet)
                    self.attandee_sheet.user.update_attandee_sheet_info_dict(self.attandee_sheet)
                    self.attandee_sheet.user.update_validation("attandee_sheet_info_dict", validation)
                    successful = True
            if successful:
                self.parent.parent.update_table()
                self.parent.destroy()

        def return_to_menu(self):
            self.parent.unsaved_non_attandee_list = self.non_attandee_list_selector.non_attandee_list
            self.parent.changePresentation("class_info")

        def exit(self):
            self.parent.parent.update_table()
            self.parent.destroy()

class Non_Attandee_List_Manager(tkinter.Frame):
    def __init__(self, parent):
        self.parent = parent
        tkinter.Frame.__init__(self, self.parent, padx = 2, pady = 2, bg = "grey")
        self.attandee_sheet = self.parent.attandee_sheet
        self.non_attandee_list = self.parent.parent.unsaved_non_attandee_list
        try:
            self.students = list(set(user_manager.classrooms[self.attandee_sheet.classroom_id].students).union(set(self.non_attandee_list)))
        except Exception as e:
            self.students = self.non_attandee_list.copy()
        self.students.sort(key = lambda e: int(e.number))
        self.non_attandee_var_list = [tkinter.BooleanVar(self, True) if student in self.non_attandee_list else tkinter.BooleanVar(self, False) for student in self.students]

        height = 210
        height_lines = 10
        self.padx = 4
        
        self.canvas = tkinter.Canvas(self)
        
        scrollbar = tkinter.Scrollbar(self, orient = "vertical", command = self.canvas.yview)
        self.canvas.configure(yscrollcommand = scrollbar.set)

        self.students_display = tkinter.Frame(self.canvas, padx = self.padx)
        self.students_display.bind("<Configure>", lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all"), width = self.students_display.winfo_width(), height = min(self.students_display.winfo_height(), height)))
        self.canvas.create_window((0, 0), window = self.students_display, anchor = "nw")

        self.canvas.bind_all("<MouseWheel>", self.mousewheel)

        self.canvas.pack(side="left", fill = "y")
        scrollbar.pack(side="left", fill = "y")

        non_attandee_list_display_frame = tkinter.Frame(self, padx = self.padx)
        tkinter.Label(non_attandee_list_display_frame, text = "Gelmeyenler", width = 15).pack()
        self.non_attandee_list_display = tkinter.Text(non_attandee_list_display_frame, width = 18, height = height_lines, wrap = "word", bd = 0)
        self.non_attandee_list_display.configure(font=("TkDefaultFont"), state = "disabled")
        self.non_attandee_list_display.pack()
        non_attandee_list_display_frame.pack(side = "left", anchor = "n", fill = "y")

        row = 0
        anchor_label = tkinter.Label(self.students_display)
        anchor_label.grid(row = row, column = 0, sticky = "n" + "s")
##        tkinter.Checkbutton(self.students_display).grid(row = row, column = 0, sticky = "w" + "e")
        tkinter.Label(self.students_display, text = "Numara", padx = self.padx).grid(row = row, column = 2, sticky = "w" + "n")
        tkinter.Label(self.students_display, text = "İsim Soyisim", padx = self.padx).grid(row = row, column = 3, sticky = "w" + "n")
        row += 1
        for ind in range(len(self.students)):
            student = self.students[ind]
            var = self.non_attandee_var_list[ind]
            tkinter.Checkbutton(self.students_display, onvalue = True, offvalue = False, variable = var, command = self.update_displays, padx = self.padx, state = "active" if self.parent.parent.mode != "view" else "disabled").grid(row = row, column = 0, sticky = "w" + "n")
            tkinter.Frame(self.students_display, bg = "grey", padx = self.padx).grid(row = row, column = 1, sticky = "n" + "s")
            tkinter.Label(self.students_display, text = student.number, padx = self.padx).grid(row = row, column = 2, sticky = "w" + "n")
            tkinter.Label(self.students_display, text = student.name, padx = self.padx).grid(row = row, column = 3, sticky = "w" + "n")
##            tkinter.Button(self.students_display, text = "Düzenle", padx = self.padx).grid(row = row, column = 4, sticky = "w" + "n")#
            row += 1

        self.update_displays()

    def update_displays(self):
        non_attandee_list_display_text = ""
        self.non_attandee_list = []
        for ind in range(len(self.non_attandee_var_list)):
            if self.non_attandee_var_list[ind].get():
                self.non_attandee_list.append(self.students[ind])
                non_attandee_list_display_text += self.students[ind].number + ", "
        self.non_attandee_list_display.configure(state = "normal")
        self.non_attandee_list_display.delete('1.0', "end")
        self.non_attandee_list_display.insert("insert", non_attandee_list_display_text[:-2] if non_attandee_list_display_text else "Sınıf Tam")
        self.non_attandee_list_display.configure(state = "disabled")

    def mousewheel(self, event):
        try:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except:
            pass
        
class Attandee_Sheet():
    def __init__(self, user, date):
        self.id = ""
        self.sync = ""
        self.user = user
        self.date = date
        self.classroom_id = ""
        self.teacher = user.teacher
        self.classroom_name = ""
        self.name = ""
        self.topic = ""
        self.non_attandee_list = []
        self.hour = ""

    def __repr__(self):
        return """\
self.id = {}
self.sync = {}
self.user = {}
self.date = {}
self.classroom_id = {}
self.teacher = {}
self.classroom_name = {}
self.name = {}
self.topic = {}
self.non_attandee_list = {}
self.hour = {}
""".format(self.id, self.sync, self.user, self.date, self.classroom_id, self.teacher, self.classroom_name, self.name, self.topic, self.non_attandee_list, self.hour)

    def prepare_message(self):
        message = ""
        message += self.user.username + split_char
        message += self.user.password + split_char
        for x in self.date:
            message += x + "-"
        message = message[:-1] + split_char
        message += self.classroom_id + split_char
        message += self.teacher + "%"
        message += self.classroom_name + "%"
        message += self.name + "%"
        message += self.topic + "%"
        for student in self.non_attandee_list:
            message += student.name + "-" + student.number + "&"
        if self.non_attandee_list:
            message = message[:-1]
        message += "%"
        message += self.hour
        return message

    def decode_raw_data(self, raw_data):
        raw_data = raw_data.split("%")
        self.teacher = raw_data.pop(0)
        self.classroom_name = raw_data.pop(0)
        self.name = raw_data.pop(0)
        self.topic = raw_data.pop(0)
        raw_non_attandee_list = raw_data.pop(0)
        if raw_non_attandee_list:
            self.non_attandee_list = [Student(*raw_student.split("-")) for raw_student in raw_non_attandee_list.split("&")]
        else:
            self.non_attandee_list = []
        self.hour = raw_data.pop(0)
            
class User_Manager():
    def __init__(self):
        self.users = dict()
        self.user_infos = list()
        self.active_user = None
        self.classrooms = dict()
        self.attandee_sheets = dict()
        self.messages = dict()

    def create_user(self, username, admin = False):
        if admin:
            self.users[username] = Admin_User(username)
        else:
            self.users[username] = User(username)
        return self.users[username]

    def set_active_user(self, username):
        self.active_user = self.users[username]

    def get_active_user(self):
        return self.active_user

    def update_messages(self, data):
        self.messages = dict()
        data = data.split("&")
        while data:
            message = data.pop(0)
            date = tuple(data.pop(0).split("-"))
            if date in self.messages:
                self.messages[date].append(message)
            else:
                self.messages[date] = [message]

    def update_classrooms(self, data):
        self.classrooms = dict()
        data = data.split("%")
        while data:
            classroom_id = data.pop(0)
            year = data.pop(0)
            name = data.pop(0)
            students_raw = data.pop(0)
            students = []
            if students_raw:
                for student_raw in students_raw.split("&"):
                    student_raw = student_raw.split("-")
                    students.append(Student(student_raw[0], student_raw[1]))
            self.classrooms[classroom_id] = Classroom(classroom_id, year, name, students)

    def update_user_infos(self, data):
        self.user_infos = list()
        data = data.split("%")
        while data:
            username = data.pop(0)
            admin = bool(int(data.pop(0)))
            teacher = data.pop(0)
            if admin:
                if username == self.get_active_user().username:
                    #continue
                    pass
                self.user_infos.append(User_Info(username, admin, teacher))
            else:
                classroom_ids = data.pop(0).split("-")
                class_names = data.pop(0).split("-")
                if username == self.get_active_user().username:
                    continue
                self.user_infos.append(User_Info(username, admin, teacher, classroom_ids, class_names))

    def save_to_file(self):
        pass
    
    def open_save_file(self, file_name): ###
        pass

    def add_attandee_sheet(self, attandee_sheet):
        self.attandee_sheets[attandee_sheet.id] = attandee_sheet

    def query_attandee_sheets(self, user = None, date = None, classroom_id = None, sort = None):   
        attandee_sheets = []
        for attandee_sheet in self.attandee_sheets.values():
            if user and attandee_sheet.user.username != user.username:
                continue
            if date and attandee_sheet.date != date:
                continue
            if classroom_id and attandee_sheet.classroom_id != classroom_id:
                continue
            attandee_sheets.append(attandee_sheet)
        sort_lambdas = {
            "hour": lambda attandee_sheet: attandee_sheet.hour
            }
        if sort:
            attandee_sheets.sort(key = sort_lambdas[sort])

        return attandee_sheets

    def logout(self):
        self.active_user = None

    def get_classroom_name_object_map(self): # {"11-B" : object}
        name_map = dict()
        for classroom_id in self.classrooms:
            name_map[self.classrooms[classroom_id].prepare_name()] = self.classrooms[classroom_id]
        return name_map

    def get_classroom_name_id_map(self): # {"11-B" : ID}
        name_map = dict()
        for classroom_id in self.classrooms:
            name_map[self.classrooms[classroom_id].prepare_name()] = classroom_id
        return name_map

    def get_teacher_username_map(self): # {"Andaç Elmaskaya" : 15685160338}
        username_map = dict()
        for user_info in self.user_infos:
            if not user_info.admin:
                username_map[user_info.teacher] = user_info.username
        return username_map

    def request_attandee_sheets(self, date, classroom_id, username, message_display):###Kork
        user = self.get_active_user()
        message = send_message("command/query_attandee_sheets~{}~{}~{}~{}~{}".replace("~", split_char).format(user.username, user.password, "-".join(date), classroom_id, username)).text.split(split_char)
        requested_attandee_sheets = []
        while message:
            action = message.pop(0)
            if action == "attandee_sheet":
                attandee_sheet_id = message.pop(0)
                username = message.pop(0)
                date = (*message.pop(0).split("-"),)
                classroom_id = message.pop(0)
                raw_data = message.pop(0)
                attandee_sheet = Attandee_Sheet(user, date)
                attandee_sheet.id = attandee_sheet_id
#                 attandee_sheet.classroom = self.user.classrooms[classroom_id]
                attandee_sheet.decode_raw_data(raw_data)
                attandee_sheet.classroom_id = classroom_id
                requested_attandee_sheets.append(attandee_sheet)
            elif action == "message":
                server_message = message.pop(0)
                message_display.config(text = server_message)
        return requested_attandee_sheets

class User_Info():
    def __init__(self, username, admin, teacher, classroom_ids = None, class_names = None):
        self.username = username
        self.admin = admin
        self.password = "********"
        self.teacher = teacher
        self.classroom_ids = classroom_ids
        self.class_names = class_names

class User():
    basic_validations = ["0", "0", "0", "0"]
    validation_keys = {
        "teacher" : 0,
        "classroom_ids" : 1,
        "attandee_sheet_info_dict" : 2,
        "class_names" : 3
        }
    def __init__(self, username):
        self.username = username
        self.password = ""
        self.validations = self.basic_validations.copy()
        self.classrooms = dict()
        self.teacher = ""
        self.class_names = []
        self.attandee_sheet_info_elements = dict()

    def set_password(self, password):
        self.password = password

    def encode_validations(self):
        return "-".join(self.validations)

    def set_classrooms(self, classroom_ids_raw):
        classroom_ids = classroom_ids_raw.split("-")
        self.classrooms = dict()
        for classroom_id in classroom_ids:
            self.classrooms[classroom_id] = user_manager.classrooms[classroom_id]
            
    def set_attandee_sheet_info_dict(self, raw_attandee_sheet_info_dict):#02-08-2020&2344252342:0-3241331241324:0-32432423424:1?03-08-2020&... -> {("02", "08", "2020") : [(2344252342, 0), ...], ...}
        raw_attandee_sheet_info_elements = raw_attandee_sheet_info_dict.split("%")
        if not raw_attandee_sheet_info_elements[0]:
            return
        for raw_attandee_sheet_info_element in raw_attandee_sheet_info_elements:
            raw_attandee_sheet_info_element = raw_attandee_sheet_info_element.split("?")
            date = (*raw_attandee_sheet_info_element.pop(0).split("-"),)
            raw_attandee_sheet_infos = raw_attandee_sheet_info_element.pop(0).split("&")
            self.attandee_sheet_info_elements[date] = [raw_attandee_sheet_info.split("-") for raw_attandee_sheet_info in raw_attandee_sheet_infos]

    def update_attandee_sheet_info_dict(self, attandee_sheet):
        try:
            for attandee_sheet_info_element in self.attandee_sheet_info_elements[attandee_sheet.date]:
                if attandee_sheet_info_element[0] == attandee_sheet.id:
                    attandee_sheet_info_element = [attandee_sheet_info_element[0], attandee_sheet.sync]
                    break
            else:
                attandee_sheet.user.attandee_sheet_info_elements[attandee_sheet.date].append([attandee_sheet.id, attandee_sheet.sync])
        except KeyError:
            attandee_sheet.user.attandee_sheet_info_elements[attandee_sheet.date] = [[attandee_sheet.id, attandee_sheet.sync]]

    def delete_from_attandee_sheet_info_dict(self, attandee_sheet_id):
        attandee_sheet_date = user_manager.attandee_sheets[attandee_sheet_id].date
        for ind in range(len(self.attandee_sheet_info_elements[attandee_sheet_date])):
            attandee_sheet_info_element = self.attandee_sheet_info_elements[attandee_sheet_date][ind]
            if attandee_sheet_info_element[0] == attandee_sheet_id:
                self.attandee_sheet_info_elements[attandee_sheet_date].pop(ind)
                break
            
    def get_classroom_name_key_map(self): # {"11-B" : ID}
        name_map = dict()
        for classroom in self.classrooms:
            name_map[self.classrooms[classroom].prepare_name()] = classroom
        return name_map
        
    def update_teacher(self, teacher):
        self.teacher = teacher

    def update_validation(self, validation_key, validation):
        self.validations[self.validation_keys[validation_key]] = validation

    def update_class_names(self, raw_class_names):
        self.class_names = raw_class_names.split("-")

class Admin_User():
    basic_validations = ["0", "0", "0", "0"]
    validation_keys = {
        "user_infos" : 0,
        "classrooms" : 1,
        "teacher" : 2,
        "messages" : 3
        }
    def __init__(self, username):
        self.username = username
        self.password = ""
        self.validations = self.basic_validations.copy()
        self.teacher = ""
        self.attandee_sheet_info_elements = dict()

    def set_password(self, password):
        self.password = password

    def encode_validations(self):
        return "-".join(self.validations)
            
    def set_attandee_sheet_info_dict(self, raw_attandee_sheet_info_dict):#02-08-2020&2344252342:0-3241331241324:0-32432423424:1?03-08-2020&... -> {("02", "08", "2020") : [(2344252342, 0), ...], ...}
        raw_attandee_sheet_info_elements = raw_attandee_sheet_info_dict.split("%")
        if not raw_attandee_sheet_info_elements[0]:
            return
        for raw_attandee_sheet_info_element in raw_attandee_sheet_info_elements:
            raw_attandee_sheet_info_element = raw_attandee_sheet_info_element.split("?")
            date = (*raw_attandee_sheet_info_element.pop(0).split("-"),)
            raw_attandee_sheet_infos = raw_attandee_sheet_info_element.pop(0).split("&")
            self.attandee_sheet_info_elements[date] = [raw_attandee_sheet_info.split("-") for raw_attandee_sheet_info in raw_attandee_sheet_infos]

    def update_attandee_sheet_info_dict(self, attandee_sheet):
        try:
            attandee_sheet.user.attandee_sheet_info_elements[attandee_sheet.date].append([attandee_sheet.id, "1"])
        except KeyError:
            attandee_sheet.user.attandee_sheet_info_elements[attandee_sheet.date] = [[attandee_sheet.id, "1"]]
            
    def get_classroom_name_key_map(self): # {"11-B" : ID}
        name_map = {"" : ""}
        for classroom in user_manager.classrooms:
            name_map[user_manager.classrooms[classroom].prepare_name()] = classroom
        return name_map
        
    def update_teacher(self, teacher):
        self.teacher = teacher

    def update_validation(self, validation_key, validation):
        self.validations[self.validation_keys[validation_key]] = validation
        
def send_message(message):
    req = requests.get("https://{}/{}".format(ip_adress, message))
    return req

class Classroom_Manager(tkinter.Frame):
    def __init__(self, parent, user, locked):
        self.parent = parent
        tkinter.Frame.__init__(self, self.parent)
        self.var = tkinter.StringVar()
        self.user = user
        self.classroom_map = self.user.get_classroom_name_key_map()
        keys = [x for x in self.classroom_map]
        keys.sort(key = lambda key: key.split("-")[1] if key else ".")
        keys.sort(key = lambda key: key.split("-")[0] if key else ".")
        if locked[0] or locked[1]:
            self.locked_name = locked[0]
            self.locked_id = locked[1]
            self.classroom_map[self.locked_name] = self.locked_id
            tkinter.Label(self, text = self.locked_name).pack()
            self.var.set(self.locked_name)
        else:
            if keys:
                self.option_menu = tkinter.OptionMenu(self, self.var, *keys)
                self.option_menu.pack()
            else:
                tkinter.Label(self, text = "Sınıf Yok").pack()

    def get_classroom(self):
        if self.var.get():
            return (self.classroom_map[self.var.get()], self.var.get())#(id, name)
        else:
            return None

class Classroom():
    years = ["Hz", "9", "10", "11", "12", "Mezun"]
    def __init__(self, ID, year, name, students):
        self.id = ID
        self.year = year
        self.name = name
        self.students = students

    def prepare_name(self):
        return "{}-{}".format(self.years[int(self.year)], self.name)

class Student():
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __repr__(self):
        return "({}, {})".format(self.name, self.number)

    def __eq__(self, other):
        return self.name == other.name and self.number == other.number

    def __hash__(self):
        return hash(self.__repr__())

class MainApp(tkinter.Frame):
    presentations = {
        "main_menu" : lambda x: MainApp.MainMenu(x),
        "teacher_login_menu" : lambda x: TeacherLoginPanel(x),
        "admin_login_menu" : lambda x: AdminLoginPanel(x),
        "daily_schedule" : lambda x: DailySchedule(x),
        "admin_panel" : lambda x: AdminPanel(x)
        }
    def __init__(self, parent):
        self.parent = parent
        tkinter.Frame.__init__(self, self.parent)
        self.presentation = self.presentations["main_menu"](self)
        self.presentation.pack()

    def changePresentation(self, prsnt):
        self.presentation.destroy()
        self.presentation = self.presentations[prsnt](self)
        self.presentation.pack()

    class MainMenu(tkinter.Frame):
        def __init__(self, parent):
            self.parent = parent
            tkinter.Frame.__init__(self, self.parent)

            row = 0

            space_frame = tkinter.Frame(self)
            for x in range(6):
                tkinter.Label(space_frame).pack()
            space_frame.grid(row = row)
            row += 1
            
            self.main_content_holder = tkinter.Frame(self)
            tkinter.Label(self.main_content_holder, text = app_description).pack(fill = "x")
            tkinter.Label(self.main_content_holder).pack()
            
            button_holder = tkinter.Frame(self.main_content_holder)
            tkinter.Button(button_holder, text = "Öğretmen Paneli Giriş", command = lambda: self.parent.changePresentation("teacher_login_menu")).pack()
            tkinter.Button(button_holder, text = "İdare Paneli Giriş", command = lambda: self.parent.changePresentation("admin_login_menu")).pack(fill = "x")
            button_holder.pack()
            
            self.main_content_holder.grid(row = row)
            row += 1
            space_frame = tkinter.Frame(self)
            tkinter.Label(space_frame).pack()
            tkinter.Label(space_frame).pack()
            space_frame.grid(row = row)
            row += 1
            
##            tkinter.Label(self, text = "version {}\nAndaç Elmaskaya".format(version), justify = "left").grid(row = row, sticky = "S" + "E")

class TeacherLoginPanel(tkinter.Frame):
    presentations = {"main_menu" : lambda x: TeacherLoginPanel.MainMenu(x)}
    
    def __init__(self, parent):
        self.parent = parent
        tkinter.Frame.__init__(self, self.parent)
        self.presentation = self.presentations["main_menu"](self)
        self.presentation.pack()

    def changePresentation(self, prsnt):
        self.presentation.destroy()
        self.presentation = self.presentations[prsnt](self)
        self.presentation.pack()

    class MainMenu(tkinter.Frame):
        def __init__(self, parent):
            self.parent = parent
            tkinter.Frame.__init__(self, self.parent)

            for x in range(6):
                tkinter.Label(self).pack()

            tkinter.Label(self, text = "Öğretmen Paneli").pack()
            tkinter.Label(self).pack()
            
            login_info = tkinter.Frame(self)
            tkinter.Label(login_info, text = "Kulanıcı Adı:  ").grid(row = 0, column = 0, sticky = "w")
            self.username_entry = tkinter.Entry(login_info)
            self.username_entry.insert(0, "")
            self.username_entry.grid(row = 0, column = 1)
            
            tkinter.Label(login_info, text = "Şifre:").grid(row = 1, column = 0, sticky = "w")
            self.password_entry = tkinter.Entry(login_info, show='*')
            self.password_entry.insert(0, "")
            self.password_entry.grid(row = 1, column = 1)
            login_info.pack(anchor = "w")

            tkinter.Label(self).pack()

            button_holder = tkinter.Frame(self)
            tkinter.Button(button_holder, command = self.login, text = "Giriş Yap").pack(side = "left")
            tkinter.Label(button_holder, text = "  ").pack(side = "left")
            tkinter.Button(button_holder, command = self.return_to_menu, text = "Geri Dön").pack(side = "left")
            button_holder.pack()

            self.message_display = tkinter.Label(self, text = "")
            self.message_display.pack()

        def return_to_menu(self):
            self.parent.parent.changePresentation("main_menu")

        def login(self):
            global user_manager
            username = self.username_entry.get()
            password = self.password_entry.get()
            if not username:
                self.message_display.config(text = "Kullanıcı Adı boş bırakılamaz.")
                return
            user = user_manager.create_user(username, admin = False)
            validations = user.encode_validations()
            message = send_message("command/login~{}~{}~{}".replace("~", split_char).format(username, password, validations)).text.split(split_char)
            successful = False
            while message:
                action = message.pop(0)
                if action == "message":
                    server_message = message.pop(0)
                    self.message_display.config(text = server_message)
                elif action == "success": 
                    user.set_password(password)
                    user_manager.set_active_user(username)
                    successful = True
                elif action == "update_classroom_ids":
                    classroom_ids_raw = message.pop(0)
                    validation = message.pop(0)
                    classrooms_raw = message.pop(0)
                    user_manager.update_classrooms(classrooms_raw)
                    user.set_classrooms(classroom_ids_raw)
                    user.update_validation("classroom_ids", validation)
                elif action == "update_attandee_sheet_info_dict":
                    raw_attandee_sheet_info_dict = message.pop(0)
                    validation = message.pop(0)
                    user.set_attandee_sheet_info_dict(raw_attandee_sheet_info_dict)
                    user.update_validation("attandee_sheet_info_dict", validation)
                elif action == "update_teacher":
                    teacher = message.pop(0)
                    validation = message.pop(0)
                    user.update_teacher(teacher)
                    user.update_validation("teacher", validation)
                elif action == "update_class_names":
                    raw_class_names = message.pop(0)
                    validation = message.pop(0)
                    user.update_class_names(raw_class_names)
                    user.update_validation("class_names", validation)
            if successful:
                self.parent.parent.changePresentation("daily_schedule")

class AdminLoginPanel(tkinter.Frame):
    presentations = {"main_menu" : lambda x: AdminLoginPanel.MainMenu(x)}
    
    def __init__(self, parent):
        self.parent = parent
        tkinter.Frame.__init__(self, self.parent)
        self.presentation = self.presentations["main_menu"](self)
        self.presentation.pack()

    def changePresentation(self, prsnt):
        self.presentation.destroy()
        self.presentation = self.presentations[prsnt](self)
        self.presentation.pack()

    class MainMenu(tkinter.Frame):
        def __init__(self, parent):
            self.parent = parent
            tkinter.Frame.__init__(self, self.parent)

            for x in range(6):
                tkinter.Label(self).pack()

            tkinter.Label(self, text = "İdare Paneli").pack()
            tkinter.Label(self).pack()
            
            login_info = tkinter.Frame(self)
            tkinter.Label(login_info, text = "Kulanıcı Adı:  ").grid(row = 0, column = 0, sticky = "w")
            self.username_entry = tkinter.Entry(login_info)
            self.username_entry.insert(0, "")
            self.username_entry.grid(row = 0, column = 1)
            
            tkinter.Label(login_info, text = "Şifre:").grid(row = 1, column = 0, sticky = "w")
            self.password_entry = tkinter.Entry(login_info, show='*')
            self.password_entry.insert(0, "")
            self.password_entry.grid(row = 1, column = 1)
            login_info.pack(anchor = "w")

            tkinter.Label(self).pack()

            button_holder = tkinter.Frame(self)
            tkinter.Button(button_holder, command = self.login, text = "Giriş Yap").pack(side = "left")
            tkinter.Label(button_holder, text = "  ").pack(side = "left")
            tkinter.Button(button_holder, command = self.return_to_menu, text = "Geri Dön").pack(side = "left")
            button_holder.pack()

            self.message_display = tkinter.Label(self, text = "")
            self.message_display.pack()

        def return_to_menu(self):
            self.parent.parent.changePresentation("main_menu")

        def login(self):
            global user_manager
            username = self.username_entry.get()
            password = self.password_entry.get()
            if not username:
                self.message_display.config(text = "Kullanıcı Adı boş bırakılamaz.")
                return
            user = user_manager.create_user(username, admin = True)
            validations = user.encode_validations()
            message = send_message("command/login_admin~{}~{}~{}".replace("~", split_char).format(username, password, validations)).text.split(split_char)
            successful = False
            while message:
                action = message.pop(0)
                if action == "message":
                    server_message = message.pop(0)
                    self.message_display.config(text = server_message)
                elif action == "success": 
                    user.set_password(password)
                    user_manager.set_active_user(username)
                    successful = True
                elif action == "update_classrooms":
                    validation = message.pop(0)
                    classrooms_raw = message.pop(0)
                    user_manager.update_classrooms(classrooms_raw)
                    user.update_validation("classrooms", validation)
                elif action == "update_messages":
                    validation = message.pop(0)
                    messages_raw = message.pop(0)
                    user_manager.update_messages(messages_raw)
                    user.update_validation("messages", validation)
                elif action == "update_teacher":
                    teacher = message.pop(0)
                    validation = message.pop(0)
                    user.update_teacher(teacher)
                    user.update_validation("teacher", validation)
                elif action == "update_user_infos":
                    validation = message.pop(0)
                    user_infos_raw = message.pop(0)
                    user_manager.update_user_infos(user_infos_raw)
                    user.update_validation("user_infos", validation)
            if successful:
                self.parent.parent.changePresentation("admin_panel")

class Profile_Manager(tkinter.Toplevel):
    presentations = {"details_screen" : lambda x: Profile_Manager.Details_Screen(x),
                     "change_password" : lambda x: Profile_Manager.Change_Password(x),
                     "send_note" : lambda x: Profile_Manager.Send_Note(x)}
    width = 250
    height = 500
    
    def __init__(self, parent):
        self.parent = parent
        tkinter.Toplevel.__init__(self)
        self.title("Profil Ayarları")
        x = (self.winfo_screenwidth() // 2) + (app_width // 2) + shift_right + (Attandee_Editor.width // 2) - (Profile_Manager.width // 2)
        y = (self.winfo_screenheight() // 2) - (app_height // 2) + shift_down
        self.geometry('{}x{}+{}+{}'.format(self.width, self.height, x, y))

        self.message_text = ""

        self.presentation = self.presentations["details_screen"](self)
        self.presentation.pack()

    def changePresentation(self, prsnt):
        self.presentation.destroy()
        self.presentation = self.presentations[prsnt](self)
        self.presentation.pack()

    class Details_Screen(tkinter.Frame):
        def __init__(self, parent):
            self.parent = parent
            tkinter.Frame.__init__(self, self.parent)
            self.user = user_manager.get_active_user()

            self.pady = 2
            text_width = 30

            row = 0
            tkinter.Label(self).grid(row = row, column = 0)
            row += 1
            tkinter.Label(self, text = "Kullanıcı: {}".format(self.user.teacher)).grid(row = row, column = 0, sticky = "w" + "n")
            row += 1
            tkinter.Label(self).grid(row = row, column = 0)
            row += 1
            tkinter.Label(self, text = "Atanan Sınıflar: ").grid(row = row, column = 0, sticky = "w" + "n")
            row += 1
            cover = tkinter.Frame(self, pady = self.pady)
            topic_display = tkinter.Text(cover, width = text_width, height = 3, wrap = "word", bd = 0)
            classrooms_list_text = [classroom.prepare_name() for classroom in self.user.classrooms.values()]
            classrooms_list_text.sort(key = lambda key: key.split("-")[1])
            classrooms_list_text.sort(key = lambda key: key.split("-")[0])
            topic_display.insert("insert", ", ".join(classrooms_list_text))
            topic_display.configure(font=("TkDefaultFont"), state = "disabled")
            topic_display.pack()
            cover.grid(row = row, column = 0, sticky = "w" + "n")
            row += 1
            tkinter.Label(self, text = "Atanan Dersler: ").grid(row = row, column = 0, sticky = "w" + "n")
            row += 1
            cover = tkinter.Frame(self, pady = self.pady)
            topic_display = tkinter.Text(cover, width = text_width, height = len(self.user.class_names), wrap = "word", bd = 0)
            classes_list_text = self.user.class_names
            classes_list_text.sort()
            topic_display.insert("insert", "\n".join(classes_list_text))
            topic_display.configure(font=("TkDefaultFont"), state = "disabled")
            topic_display.pack()
            cover.grid(row = row, column = 0, sticky = "w" + "n")
            row += 1
            tkinter.Label(self).grid(row = row, column = 0)
            row += 1
            button_holder_frame = tkinter.Frame(self)
            tkinter.Button(button_holder_frame, text = "İdareye Mesaj Gönder", command = self.send_message_to_admins_presentation, bd = 0).grid(row = 0, column = 0, sticky = "w" + "e")
            tkinter.Button(button_holder_frame, text = "Şifre Değiştir", command = self.change_password_presentation, bd = 0).grid(row = 1, column = 0, sticky = "w" + "e")
            tkinter.Button(button_holder_frame, text = "Oturumu Kapat", command = self.return_to_menu, fg = "red", bd = 0).grid(row = 2, column = 0, sticky = "w" + "e")
            button_holder_frame.grid(row = row, column = 0)
            row += 1
            tkinter.Label(self).grid(row = row, column = 0)
            row += 1
            self.message_display = tkinter.Label(self)
            self.message_display.grid(row = row, column = 0)
            row += 1
            
        def return_to_menu(self):
            if not tkinter.messagebox.askokcancel(title = "Dikkat", message = "Oturumu kapatmak istiyor musunuz ?"):
                return
            self.parent.parent.return_to_menu()
            self.parent.destroy()

        def change_password_presentation(self):
            Change_Password(self).mainloop()

        def send_message_to_admins_presentation(self):
            Send_Message(self).mainloop()

class DailySchedule(tkinter.Frame):
    presentations = {"main_menu" : lambda x: DailySchedule.MainMenu(x)}
    
    def __init__(self, parent):
        self.parent = parent
        tkinter.Frame.__init__(self, self.parent)
        self.presentation = self.presentations["main_menu"](self)
        self.presentation.pack()

    def changePresentation(self, prsnt):
        self.presentation.destroy()
        self.presentation = self.presentations[prsnt](self)
        self.presentation.pack()

    class MainMenu(tkinter.Frame):
        def __init__(self, parent):
            self.parent = parent
            tkinter.Frame.__init__(self, self.parent)

            tkinter.Label(self).pack()
            tkinter.Label(self).pack()
            up_holder_frame = tkinter.Frame(self)
            date_manager = Date_Manager(up_holder_frame, start_year, start_month, start_day)
            date_manager.pack(side = "left")
            profile_info_frame = tkinter.Frame(up_holder_frame)
            tkinter.Label(profile_info_frame, text = user_manager.get_active_user().teacher).grid(row = 0, column = 0, sticky = "n" + "w")
            tkinter.Button(profile_info_frame, text = "Profil Ayarları", command = self.open_profile_manager).grid(row = 1, column = 0, sticky = "n")
            profile_info_frame.pack(side = "right")
            up_holder_frame.pack(fill = "x")
            
            tkinter.Label(self).pack()

            self.message_display = tkinter.Label(self, text = "")
            
            classes_manager = Classes_Manager(self, date_manager)
            classes_manager.pack()
            
            self.message_display.pack()
            
        def return_to_menu(self):
            user_manager.logout()
            self.parent.parent.changePresentation("main_menu")

        def open_profile_manager(self):
            profile_manager = Profile_Manager(self)
            profile_manager.mainloop()

class Profile_Manager_Admin(tkinter.Toplevel):
    presentations = {"details_screen" : lambda x: Profile_Manager_Admin.Details_Screen(x),
                     "change_password" : lambda x: Profile_Manager_Admin.Change_Password(x)}
    width = 250
    height = 500
    
    def __init__(self, parent):
        self.parent = parent
        tkinter.Toplevel.__init__(self)
        self.title("Profil Ayarları")
        x = (self.winfo_screenwidth() // 2) + (app_width // 2) + shift_right + (Attandee_Editor.width // 2) - (Profile_Manager.width // 2)
        y = (self.winfo_screenheight() // 2) - (app_height // 2) + shift_down
        self.geometry('{}x{}+{}+{}'.format(self.width, self.height, x, y))

        self.message_text = ""

        self.presentation = self.presentations["details_screen"](self)
        self.presentation.pack()

    def changePresentation(self, prsnt):
        self.presentation.destroy()
        self.presentation = self.presentations[prsnt](self)
        self.presentation.pack()

    class Details_Screen(tkinter.Frame):
        def __init__(self, parent):
            self.parent = parent
            tkinter.Frame.__init__(self, self.parent)
            self.user = user_manager.get_active_user()

            self.pady = 2
            text_width = 30

            row = 0
            tkinter.Label(self).grid(row = row, column = 0)
            row += 1
            tkinter.Label(self, text = "Kullanıcı: {}".format(self.user.teacher)).grid(row = row, column = 0, sticky = "w" + "n")
            row += 1
            tkinter.Label(self).grid(row = row, column = 0)
            row += 1
            tkinter.Label(self).grid(row = row, column = 0)
            row += 1
            button_holder_frame = tkinter.Frame(self)
            tkinter.Button(button_holder_frame, text = "Şifre Değiştir", command = self.change_password_presentation, bd = 0).grid(row = 1, column = 0, sticky = "w" + "e")
            tkinter.Button(button_holder_frame, text = "Oturumu Kapat", command = self.return_to_menu, fg = "red", bd = 0).grid(row = 2, column = 0, sticky = "w" + "e")
            button_holder_frame.grid(row = row, column = 0)
            row += 1
            tkinter.Label(self).grid(row = row, column = 0)
            row += 1
            self.message_display = tkinter.Label(self)
            self.message_display.grid(row = row, column = 0)
            row += 1

        def return_to_menu(self):
            if not tkinter.messagebox.askokcancel(title = "Dikkat", message = "Oturumu kapatmak istiyor musunuz ?"):
                return
            self.parent.parent.return_to_menu()
            self.parent.destroy()

        def change_password_presentation(self):
            Change_Password(self).mainloop()

class AdminPanel(tkinter.Frame):
    presentations = {"main_menu" : lambda x: AdminPanel.MainMenu(x),
                     "notifications" : lambda x: AdminPanel.NotificationsMenu(x),
                     "attandee_sheet_display" : lambda x: AdminPanel.AttandeeSheetDisplay(x),
                     "school_settings" : lambda x: AdminPanel.SchoolSettings(x),
                     "classroom_settings" : lambda x: AdminPanel.ClassroomSettings(x),
                     "user_settings" : lambda x: AdminPanel.UserSettings(x)}
    
    def __init__(self, parent):
        self.parent = parent
        tkinter.Frame.__init__(self, self.parent)
        self.presentation = self.presentations["main_menu"](self)
        self.presentation.pack()

    def changePresentation(self, prsnt):
        self.presentation.destroy()
        self.presentation = self.presentations[prsnt](self)
        self.presentation.pack()

    class MainMenu(tkinter.Frame):
        def __init__(self, parent):
            self.parent = parent
            tkinter.Frame.__init__(self, self.parent)

            tkinter.Label(self).pack()
            tkinter.Label(self).pack()

            up_holder_frame = tkinter.Frame(self)
            school_info_frame = tkinter.Frame(up_holder_frame)
            tkinter.Label(school_info_frame, text = "Haydarpaşa Lisesi").pack(anchor = "w")
            notification_holder = tkinter.Frame(school_info_frame)
            tkinter.Button(notification_holder, text = "Mesajlar", command = self.open_notifications).pack(side = "left")
            notifications_len = 0
            try:
                notifications_len = len(user_manager.messages[Date_Manager(self, start_year, start_month, start_day).get_date()])
            except:
                pass
            self.notification_label = tkinter.Label(notification_holder, text = "Bugün {} Mesaj".format(notifications_len)).pack(side = "left")
            notification_holder.pack()
            school_info_frame.pack(side = "left", padx = 60)
            profile_info_frame = tkinter.Frame(up_holder_frame)
            tkinter.Label(profile_info_frame, text = user_manager.get_active_user().teacher).grid(row = 0, column = 0, sticky = "n" + "w")
            tkinter.Button(profile_info_frame, text = "Profil Ayarları", command = self.open_profile_manager).grid(row = 1, column = 0, sticky = "n")
            profile_info_frame.pack(side = "right", padx = 60)
            up_holder_frame.pack(fill = "x")

            tkinter.Label(self).pack()
            tkinter.Label(self).pack()
            tkinter.Button(self, text = "Yoklama Kağıdı Görüntüleyici", command = self.change_attandee_sheet_display_presentation).pack()
            tkinter.Label(self).pack()
##            tkinter.Button(self, text = "Okul Ayarları", command = self.change_school_settings_presentation).pack()
##            tkinter.Label(self).pack()
            tkinter.Button(self, text = "Sınıf Ayarları", command = self.change_classroom_settings_presentation).pack()
            tkinter.Label(self).pack()
            tkinter.Button(self, text = "Kullanıcı Ayarları", command = self.change_user_settings_presentation).pack()

        def open_profile_manager(self):
            profile_manager = Profile_Manager_Admin(self)
            profile_manager.mainloop()

        def open_notifications(self):
            self.parent.changePresentation("notifications")
            
        def return_to_menu(self):
            user_manager.logout()
            self.parent.parent.changePresentation("main_menu")

        def change_attandee_sheet_display_presentation(self):
            self.parent.changePresentation("attandee_sheet_display")

        def change_school_settings_presentation(self):
            self.parent.changePresentation("school_settings")

        def change_classroom_settings_presentation(self):
            self.parent.changePresentation("classroom_settings")

        def change_user_settings_presentation(self):
            self.parent.changePresentation("user_settings")

    class NotificationsMenu(tkinter.Frame):
        presentations = {"main_menu" : lambda x: AdminPanel.NotificationsMenu.MainMenu(x)}
        
        def __init__(self, parent):
            self.parent = parent
            tkinter.Frame.__init__(self, self.parent)
            self.presentation = self.presentations["main_menu"](self)
            self.presentation.pack()

        def changePresentation(self, prsnt):
            self.presentation.destroy()
            self.presentation = self.presentations[prsnt](self)
            self.presentation.pack()

        class MainMenu(tkinter.Frame):
            def __init__(self, parent):
                self.parent = parent
                tkinter.Frame.__init__(self, self.parent)

                tkinter.Label(self).pack()
                tkinter.Label(self).pack()
                up_holder_frame = tkinter.Frame(self)
                date_manager = Date_Manager(up_holder_frame, start_year, start_month, start_day)
                date_manager.pack(side = "left")
                up_holder_frame.pack(fill = "x")
                
                tkinter.Label(self).pack()

                self.message_display = tkinter.Label(self, text = "")
                
                classes_manager = AdminPanel.Notifications_Manager(self, date_manager)
                classes_manager.pack()
                
                self.message_display.pack()

                tkinter.Button(self, text = "Geri Dön", command = self.return_to_menu).pack()
                
            def return_to_menu(self):
                self.parent.parent.changePresentation("main_menu")

    class Notifications_Manager(tkinter.Frame):
        def __init__(self, parent, date_manager):
            self.parent = parent
            tkinter.Frame.__init__(self, self.parent)
            self.date_manager = date_manager
            self.user = user_manager.get_active_user()

            height = 300
            width = 460
            self.padx = 4
            self.pady = 2

            canvas_frame = tkinter.Frame(self)

            self.canvas = tkinter.Canvas(canvas_frame)

            scrollbar = tkinter.Scrollbar(canvas_frame, orient = "vertical", command = self.canvas.yview)
            self.canvas.configure(yscrollcommand = scrollbar.set)

            self.messages_display = tkinter.Frame(self.canvas, padx = self.padx)
            self.messages_display.bind("<Configure>", lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all"), width = max(self.messages_display.winfo_width(), width), height = height))
            self.canvas.create_window((0, 0), window = self.messages_display, anchor = "nw")

            self.canvas.bind_all("<MouseWheel>", self.mousewheel)

            self.canvas.pack(side="left", fill = "y")
            scrollbar.pack(side="left", fill = "y")

            canvas_frame.pack()
            
            self.update_date(self.date_manager.set_tracer(self.update_date))

        def update_date(self, date):
            self.date = date
            self.update_table()

        def update_table(self):
            self.canvas.bind_all("<MouseWheel>", self.mousewheel)
            for child in self.messages_display.winfo_children():
                child.destroy()
            if self.date in user_manager.messages:
                for message in user_manager.messages[self.date]:
                    tkinter.Label(self.messages_display, text = message).pack()
            else:
                tkinter.Label(self.messages_display, text = "Mesaj Yok.").pack()

        def mousewheel(self, event):
            try:
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass

        def onFrameConfigure(self, event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    class AttandeeSheetDisplay(tkinter.Frame):
        def __init__(self, parent):
            self.parent = parent
            tkinter.Frame.__init__(self, self.parent)
            self.classroom_id = ""
            self.username = ""
            self.attandee_sheet_dict = dict()

            self.padx = 15
            tkinter.Label(self).pack()
            tkinter.Label(self).pack()
            up_holder_frame = tkinter.Frame(self)
            self.date_manager = Date_Manager(up_holder_frame, start_year, start_month, start_day)
            self.date_manager.pack(side = "left", padx = self.padx)
            tkinter.Label(up_holder_frame, text = "Sınıf:").pack(side = "left", anchor = "s", pady = 6)
            self.classroom_manager = Classroom_Manager(up_holder_frame, user_manager.get_active_user(), (None, None))
            self.classroom_manager.pack(side = "left", anchor = "s")
            tkinter.Label(up_holder_frame, text = "Öğretmen:").pack(side = "left", anchor = "s", pady = 6)
            self.username_map = user_manager.get_teacher_username_map()
            self.username_map[""] = ""
            keys = list(self.username_map)
            keys.sort()
            self.username_var = tkinter.StringVar(self)
            if keys:
                self.username_option_menu = tkinter.OptionMenu(up_holder_frame, self.username_var, *keys)
                self.username_option_menu.pack(side = "left", anchor = "s")
            else:
                tkinter.Label(self, text = "").pack(side = "left", anchor = "s")
            tkinter.Button(up_holder_frame, text = "Getir", command = self.update_table).pack(side = "left", anchor = "s", padx = self.padx, pady = 4)
            up_holder_frame.pack(fill = "x")
            
            tkinter.Label(self).pack()

            height = 300
            width = 460
            self.padx = 4
            self.pady = 2

            canvas_frame = tkinter.Frame(self)

            self.canvas = tkinter.Canvas(canvas_frame)

            scrollbar = tkinter.Scrollbar(canvas_frame, orient = "vertical", command = self.canvas.yview)
            self.canvas.configure(yscrollcommand = scrollbar.set)

            self.attandee_sheets_display = tkinter.Frame(self.canvas, padx = self.padx)
            self.attandee_sheets_display.bind("<Configure>", lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all"), width = max(self.attandee_sheets_display.winfo_width(), width), height = height))
            self.canvas.create_window((0, 0), window = self.attandee_sheets_display, anchor = "nw")

            self.canvas.bind_all("<MouseWheel>", self.mousewheel)

            self.canvas.pack(side="left", fill = "y")
            scrollbar.pack(side="left", fill = "y")

            canvas_frame.pack()

            self.message_display = tkinter.Label(self, text = "")
            self.message_display.pack()

            tkinter.Label(self).pack()

            button_holder = tkinter.Frame(self)
            tkinter.Button(button_holder, text = "Geri Dön", command = self.return_to_menu, bd = 0, padx = self.padx).pack(side = "right")
            button_holder.pack(fill = "x")

            
            self.update_date(self.date_manager.set_tracer(self.update_date))

        def return_to_menu(self):
            self.parent.changePresentation("main_menu")

        def update_date(self, date):
            self.date = date
            self.update_table()

        def update_table(self):
            self.canvas.bind_all("<MouseWheel>", self.mousewheel)
            for child in self.attandee_sheets_display.winfo_children():
                child.destroy()

            self.username = self.username_map[self.username_var.get()]
            self.classroom_id = self.classroom_manager.get_classroom()
            if self.classroom_id:
                self.classroom_id = self.classroom_id[0]
            else:
                self.classroom_id = ""
            attandee_sheets = user_manager.request_attandee_sheets(self.date, self.classroom_id, self.username, self.message_display)
            text_width = 42
            if attandee_sheets:
                self.attandee_sheet_dict = dict()
                for attandee_sheet in attandee_sheets:
                    self.attandee_sheet_dict[attandee_sheet.id] = attandee_sheet
                row = 0
                for x in range(len(attandee_sheets)):
                    attandee_sheet = attandee_sheets[x]
                    tkinter.Label(self.attandee_sheets_display, text = attandee_sheet.hour, padx = self.padx).grid(row = row, column = 0, sticky = "w" + "n")
                    tkinter.Label(self.attandee_sheets_display, text = attandee_sheet.name, padx = self.padx).grid(row = row, column = 1, sticky = "w" + "n")
                    tkinter.Label(self.attandee_sheets_display, text = attandee_sheet.teacher, padx = self.padx).grid(row = row, column = 2, sticky = "e" + "n")
                    tkinter.Label(self.attandee_sheets_display, text = attandee_sheet.classroom_name, padx = self.padx).grid(row = row, column = 3)
                    row += 1
                    tkinter.Label(self.attandee_sheets_display, text = "Konu: ", padx = self.padx).grid(row = row, column = 0, sticky = "w" + "n")
                    cover = tkinter.Frame(self.attandee_sheets_display, pady = self.pady)
                    topic_display = tkinter.Text(cover, width = text_width, height = 2, wrap = "word", bd = 0)
                    topic_display.insert("insert", attandee_sheet.topic)
                    topic_display.configure(font=("TkDefaultFont"), state = "disabled")
                    topic_display.pack()
                    cover.grid(row = row, rowspan = 2, column = 1, columnspan = 2, sticky = "w" + "n")
                    cover = tkinter.Frame(self.attandee_sheets_display, padx = self.padx)
                    tkinter.Button(cover, text = "Sil", command = lambda ae_id = attandee_sheet.id: self.delete_attandee_sheet(ae_id), bd = 0, fg = "red").pack(fill = "x", expand = True)
                    cover.grid(row = row, column = 3, sticky = "e" + "w" + "s")
                    row += 2
                    tkinter.Label(self.attandee_sheets_display, text = "Gelmeyenler: ", padx = self.padx).grid(row = row, column = 0, sticky = "w" + "n")
                    cover = tkinter.Frame(self.attandee_sheets_display, pady = self.pady)
                    non_attandee_list_display = tkinter.Text(cover, width = text_width, height = 2, wrap = "word", bd = 0)
                    non_attandee_list_display_text = ""
                    for student in attandee_sheet.non_attandee_list:
                        non_attandee_list_display_text += student.number + ", "
                    non_attandee_list_display.insert("insert", non_attandee_list_display_text[:-2] if non_attandee_list_display_text else "Sınıf Tam")
                    non_attandee_list_display.configure(font=("TkDefaultFont"), state = "disabled")
                    non_attandee_list_display.pack()
                    cover.grid(row = row, rowspan = 2, column = 1, columnspan = 2, sticky = "w" + "n")
                    cover = tkinter.Frame(self.attandee_sheets_display, padx = self.padx)
                    tkinter.Button(cover, text = "Görüntüle", bd = 0, command = lambda ae_id = attandee_sheet.id: self.edit_attandee_sheet(ae_id)).pack()
                    cover.grid(row = row, column = 3)
                    row += 2
                    tkinter.Label(self.attandee_sheets_display).grid(row = row, column = 0, sticky = "w" + "n")
                    row += 1
            else:
                tkinter.Label(self.attandee_sheets_display, text = "Kayıtlı bir yoklama bulunamadı.").pack()

        def mousewheel(self, event):
            try:
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass

        def delete_attandee_sheet(self, attandee_sheet_id):
            if not tkinter.messagebox.askokcancel(title = "Dikkat", message = "Yoklama geri döndürülemeyecek şekilde silinecektir. Silme işlemini onaylıyor musunuz ?"):
                return
            user = user_manager.get_active_user()
            message = send_message("command/delete_attandee_sheet~{}~{}~{}".replace("~", split_char).format(user.username, user.password, attandee_sheet_id)).text.split(split_char)
            successful = False
            while message:
                action = message.pop(0)
                if action == "message":
                    server_message = message.pop(0)
                    self.message_display.config(text = server_message)
                elif action == "success":
                    validation = message.pop(0)
                    del user_manager.attandee_sheets[attandee_sheet_id]
                    successful = True
            if successful:
                self.update_table()

        def edit_attandee_sheet(self, attandee_sheet_id):
            Attandee_Editor(self, self.attandee_sheet_dict[attandee_sheet_id], mode = "view").mainloop()

    class SchoolSettings(tkinter.Frame):
        def __init__(self, parent):
            self.parent = parent
            tkinter.Frame.__init__(self, self.parent)
            tkinter.Label(self, text = "Okunmamış Bildirim Yok").pack()

            tkinter.Button(self, text = "Geri Dön", command = self.return_to_menu).pack()

        def return_to_menu(self):
            self.parent.changePresentation("main_menu")

    class ClassroomSettings(tkinter.Frame):
        def __init__(self, parent):
            self.parent = parent
            tkinter.Frame.__init__(self, self.parent)
            classroom_show_info_var_list = list()

            height = 350
            width = 460
            self.padx = 4
            self.pady = 2

            tkinter.Label(self).pack()
            
            up_button_holder_frame = tkinter.Frame(self)
##            tkinter.Button(up_button_holder_frame, text = "Sınıfları Yeni Yıla Aktar", fg = "red", bd = 0).pack(side = "left")
            up_button_holder_frame.pack(fill = "x")
            
            tkinter.Label(self).pack()

            canvas_frame = tkinter.Frame(self)

            self.canvas = tkinter.Canvas(canvas_frame)

            scrollbar = tkinter.Scrollbar(canvas_frame, orient = "vertical", command = self.canvas.yview)
            self.canvas.configure(yscrollcommand = scrollbar.set)

            self.classrooms_display = tkinter.Frame(self.canvas, padx = self.padx)
            self.classrooms_display.bind("<Configure>", lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all"), width = min(self.classrooms_display.winfo_width(), width), height = min(height, self.classrooms_display.winfo_height())))
            self.canvas.create_window((0, 0), window = self.classrooms_display, anchor = "nw")

            self.canvas.bind_all("<MouseWheel>", self.mousewheel)

            self.canvas.pack(side="left", fill = "y")
            scrollbar.pack(side="left", fill = "y")

            canvas_frame.pack()

            tkinter.Label(self).pack()
            
            button_holder = tkinter.Frame(self)
##            tkinter.Button(button_holder, text = "Yeni Sınıf", bd = 0, fg = "green", padx = self.padx).pack(side = "left")
            tkinter.Button(button_holder, text = "Geri Dön", command = self.return_to_menu, bd = 0, padx = self.padx).pack(side = "right")
            button_holder.pack(fill = "x")

            self.update_table()
            
        def update_table(self):
            self.canvas.bind_all("<MouseWheel>", self.mousewheel)
            for child in self.classrooms_display.winfo_children():
                child.destroy()
            text_width = 37
            if user_manager.user_infos:
                row = 0
                self.classroom_map = user_manager.get_classroom_name_object_map()
                classroom_keys = [x for x in self.classroom_map]
                classroom_keys.sort(key = lambda key: key.split("-")[1])
                classroom_keys.sort(key = lambda key: key.split("-")[0])
                for classroom_key in classroom_keys:
                    tkinter.Label(self.classrooms_display, text = classroom_key).grid(row = row, column = 0, sticky = "n", padx = self.padx, pady = self.pady)
                    tkinter.Button(self.classrooms_display, text = "Sınıf İsmini Değiştir", command = lambda classroom = self.classroom_map[classroom_key]: self.edit_classroom_name(classroom)).grid(row = row, column = 1, sticky = "n" + "w", padx = self.padx, pady = self.pady)
                    row += 1
                    tkinter.Label(self.classrooms_display, text = "Sınıf {} Kişi".format(len(self.classroom_map[classroom_key].students))).grid(row = row, column = 0, padx = self.padx, pady = self.pady)
                    tkinter.Button(self.classrooms_display, text = "Sınıf Listesini Düzenle", command = lambda classroom = self.classroom_map[classroom_key]: self.edit_student_list(classroom)).grid(row = row, column = 1, padx = self.padx, pady = self.pady)
                    row += 1
                    tkinter.Label(self.classrooms_display).grid(row = row, column = 0)
                    row += 1

            else:
                tkinter.Label(self.attandee_sheets_display, text = "Kayıtlı bir sınıf bulunamadı.").pack()

        def return_to_menu(self):
            self.parent.changePresentation("main_menu")

        def mousewheel(self, event):
            try:
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass
            
        def edit_classroom_name(self, classroom):
            AdminPanel.Change_Classroom_Name(self, classroom).mainloop()

        def edit_student_list(self, classroom):
            AdminPanel.Student_List_Editor(self, classroom).mainloop()

    class Change_Classroom_Name(tkinter.Toplevel):
        def __init__(self, parent, classroom):
            self.parent = parent
            tkinter.Toplevel.__init__(self, self.parent)

            self.width = 250
            self.height = 80

            self.title("")
            x = (self.winfo_screenwidth() // 2) - (self.width // 2) + shift_right + (Attandee_Editor.width // 2) - (Profile_Manager.width // 2)
            y = (self.winfo_screenheight() // 2) - (self.height // 2) + shift_down - 100
            self.geometry('{}x{}+{}+{}'.format(self.width, self.height, x, y))

            self.classroom = classroom

            cover_frame = tkinter.Frame(self)
            top_frame = tkinter.Frame(cover_frame)
            tkinter.Label(top_frame, text = "Sınıf: ").pack(side = "left")
            self.year_var = tkinter.StringVar(self)
            self.year_option = tkinter.OptionMenu(top_frame, self.year_var, *Classroom.years)
            self.year_var.set(Classroom.years[int(self.classroom.year)])
            self.year_option.pack(side = "left")
            tkinter.Label(top_frame, text = "Şube: ").pack(side = "left")
            self.name_entry = tkinter.Entry(top_frame, width = 3)
            self.name_entry.insert(0, self.classroom.name)
            self.name_entry.pack(side = "left")
            top_frame.pack()
            down_frame = tkinter.Frame(cover_frame)
            tkinter.Button(down_frame, text = "Kaydet", command = self.save_new_name, padx = 10).pack(side = "left")
            tkinter.Button(down_frame, text = "İptal", command = self.cancel, padx = 10).pack(side = "right")
            down_frame.pack(fill = "x")
            cover_frame.pack()
            self.message_display = tkinter.Label(self)
            self.message_display.pack()

        def save_new_name(self):
            year = str(Classroom.years.index(self.year_var.get()))
            name = self.name_entry.get()
            if not year or not name:
                self.message_display.config(text = "Sınıf veya şube boş bırakılamaz.")
                return

            user = user_manager.get_active_user()
            username = user.username
            password = user.password
            message = send_message("command/change_classroom_name~{}~{}~{}~{}~{}".replace("~", split_char).format(username, password, self.classroom.id, year, name)).text.split(split_char)
            successful = False
            while message:
                action = message.pop(0)
                if action == "message":
                    server_message = message.pop(0)
                    self.message_display.config(text = server_message)
                elif action == "success": 
                    successful = True
                    self.classroom.year = year
                    self.classroom.name = name
            if successful:
                self.parent.update_table()
                self.destroy()

        def cancel(self):
            self.destroy()

    class Student_List_Editor(tkinter.Toplevel):
        
        width = 500
        height = 400
        
        def __init__(self, parent, classroom, view = False):
            self.parent = parent
            tkinter.Toplevel.__init__(self)
            self.title("Sınıf Listesi Editörü - {}".format(classroom.prepare_name()))
            x = (self.winfo_screenwidth() // 2) - (app_width // 2) + shift_right - (Attandee_Editor.width // 2) - (Profile_Manager.width // 2)
            y = (self.winfo_screenheight() // 2) - (app_height // 2) + shift_down
            self.geometry('{}x{}+{}+{}'.format(self.width, self.height, x, y))

            self.classroom = classroom
            self.students = classroom.students.copy()

            padx = 4
            cover_frame = tkinter.Frame(self)
            tkinter.Label(cover_frame).pack()
            delete_button_holder = tkinter.Frame(cover_frame)
            tkinter.Button(delete_button_holder, text = "Sil", command = self.delete_students, fg = "red", bd = 0, padx = 10, pady = 4).pack(side = "left")
            delete_button_holder.pack(expand = True, fill = "x")
            self.student_list_selector_holder = tkinter.Frame(cover_frame)
            self.refresh_student_list_selector()
            self.student_list_selector_holder.pack()
            tkinter.Label(cover_frame).pack()
            buttons_frame = tkinter.Frame(cover_frame)
            tkinter.Button(buttons_frame, text = "Yeni Öğrenci", command = self.add_new_student, fg = "green", bd = 0).pack(side = "left")
            tkinter.Label(buttons_frame, text = "Numara:").pack(side = "left")
            self.number_entry = tkinter.Entry(buttons_frame, width = 4)
            self.number_entry.pack(side = "left")
            tkinter.Label(buttons_frame, text = " İsim Soyisim:").pack(side = "left")
            self.name_entry = tkinter.Entry(buttons_frame, width = 16)
            self.name_entry.pack(side = "left")
            tkinter.Button(buttons_frame, text = "Kaydet", command = self.save_student_list).pack(side = "right")
            buttons_frame.pack(expand = True, fill = "x")
            self.message_display = tkinter.Label(cover_frame)
            self.message_display.pack()
            cover_frame.pack()

        def refresh_student_list_selector(self):
            for child in self.student_list_selector_holder.winfo_children():
                child.destroy()
            self.student_list_selector = AdminPanel.Student_List_Manager(self.student_list_selector_holder, self.students)
            self.student_list_selector.pack()

        def delete_students(self):
            if not tkinter.messagebox.askokcancel(title = "Dikkat", message = "Seçilen öğrenciler silinirlerse geri döndürülemeyeceklerdir. Silme işlemine devam etmek istiyor musunuz ?"):
                return
            ind = 0
            while ind < len(self.students):
                student = self.students[ind]
                if student in self.student_list_selector.student_select_list:
                    self.students.pop(ind)
                else:
                    ind += 1
            self.refresh_student_list_selector()
        
        def add_new_student(self):
            name = self.name_entry.get()
            number = self.number_entry.get()
            if not (name or number):
                self.message_display.config(text = "Öğrencinin numarası veya isim soyisimi boş bırakılamaz.")
                return
            self.students.append(Student(name, number))
            self.name_entry.delete(0,"end")
            self.number_entry.delete(0,"end")
            self.refresh_student_list_selector()
        
        def save_student_list(self):
            students_raw = ""
            for student in self.students:
                students_raw += student.name + "-" + student.number + "&"
            students_raw = students_raw[:-1]

            user = user_manager.get_active_user()
            username = user.username
            password = user.password
            message = send_message("command/change_classroom_students~{}~{}~{}~{}".replace("~", split_char).format(username, password, self.classroom.id, students_raw)).text.split(split_char)
            successful = False
            while message:
                action = message.pop(0)
                if action == "message":
                    server_message = message.pop(0)
                    self.message_display.config(text = server_message)
                elif action == "success": 
                    successful = True
                    self.classroom.students = self.students
            if successful:
                self.parent.update_table()
                self.destroy()

    class Student_List_Manager(tkinter.Frame):
        def __init__(self, parent, students):
            self.parent = parent
            tkinter.Frame.__init__(self, self.parent, padx = 2, pady = 2, bg = "grey")
            self.students = students
            self.students.sort(key = lambda e: int(e.number))
            self.student_var_list = [tkinter.BooleanVar(self, False) for student in self.students]

            width = 430
            height = 210
            height_lines = 10
            self.padx = 4
            
            self.canvas = tkinter.Canvas(self)
            
            scrollbar = tkinter.Scrollbar(self, orient = "vertical", command = self.canvas.yview)
            self.canvas.configure(yscrollcommand = scrollbar.set)

            self.students_display = tkinter.Frame(self.canvas, padx = self.padx)
            self.students_display.bind("<Configure>", lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all"), width = width, height = height))
            self.canvas.create_window((0, 0), window = self.students_display, anchor = "nw")

            self.canvas.bind_all("<MouseWheel>", self.mousewheel)

            self.canvas.pack(side="left", fill = "y")
            scrollbar.pack(side="left", fill = "y")

            row = 0
            anchor_label = tkinter.Label(self.students_display)
            anchor_label.grid(row = row, column = 0, sticky = "n" + "s")
            self.select_all_var = tkinter.BooleanVar(self, False)
            self.select_all_button = tkinter.Checkbutton(self.students_display, var = self.select_all_var, command = self.select_all).grid(row = row, column = 0, sticky = "w" + "e")
            tkinter.Label(self.students_display, text = "Numara", padx = self.padx).grid(row = row, column = 2, sticky = "w" + "n")
            tkinter.Label(self.students_display, text = "İsim Soyisim", padx = self.padx).grid(row = row, column = 3, sticky = "w" + "n")
            row += 1
            for ind in range(len(self.students)):
                student = self.students[ind]
                var = self.student_var_list[ind]
                tkinter.Checkbutton(self.students_display, onvalue = True, offvalue = False, variable = var, command = self.update_selections, padx = self.padx, state = "active").grid(row = row, column = 0, sticky = "w" + "n")
                tkinter.Frame(self.students_display, bg = "grey", padx = self.padx).grid(row = row, column = 1, sticky = "n" + "s")
                tkinter.Label(self.students_display, text = student.number, padx = self.padx).grid(row = row, column = 2, sticky = "w" + "n")
                tkinter.Label(self.students_display, text = student.name, padx = self.padx).grid(row = row, column = 3, sticky = "w" + "n")
                tkinter.Button(self.students_display, text = "Düzenle", command = lambda student = student: Change_Student(self, student), padx = self.padx).grid(row = row, column = 4, sticky = "w" + "n")
                row += 1

            self.update_selections()

        def update_selections(self):
            all_selected = True
            self.student_select_list = []
            for ind in range(len(self.student_var_list)):
                if self.student_var_list[ind].get():
                    self.student_select_list.append(self.students[ind])
                else:
                    all_selected = False
            if all_selected:
                self.select_all_var.set(True)
            else:
                self.select_all_var.set(False)

        def select_all(self):
            all_selected = self.select_all_var.get()
            for student_var in self.student_var_list:
                student_var.set(True if all_selected else False)
            self.update_selections()

        def mousewheel(self, event):
            try:
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass

    class UserSettings(tkinter.Frame):
        def __init__(self, parent):
            self.parent = parent
            tkinter.Frame.__init__(self, self.parent)

            height = 370
            width = 460
            self.padx = 4
            self.pady = 2

            tkinter.Label(self).pack()
            tkinter.Label(self).pack()
            tkinter.Label(self).pack()

            canvas_frame = tkinter.Frame(self)

            self.canvas = tkinter.Canvas(canvas_frame)

            scrollbar = tkinter.Scrollbar(canvas_frame, orient = "vertical", command = self.canvas.yview)
            self.canvas.configure(yscrollcommand = scrollbar.set)

            self.users_display = tkinter.Frame(self.canvas, padx = self.padx)
            self.users_display.bind("<Configure>", lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all"), width = max(self.users_display.winfo_width(), width), height = min(height, self.users_display.winfo_height())))
            self.canvas.create_window((0, 0), window = self.users_display, anchor = "nw")

            self.canvas.bind_all("<MouseWheel>", self.mousewheel)

            self.canvas.pack(side="left", fill = "y")
            scrollbar.pack(side="left", fill = "y")

            canvas_frame.pack()

            tkinter.Label(self).pack()
            
            button_holder = tkinter.Frame(self)
##            tkinter.Button(button_holder, text = "Yeni Kullanıcı", bd = 0, fg = "green", padx = self.padx).pack(side = "left")
            tkinter.Button(button_holder, text = "Geri Dön", command = self.return_to_menu, bd = 0, padx = self.padx).pack(side = "right")
            button_holder.pack(fill = "x")

            self.message_display = tkinter.Label(self)
            self.message_display.pack()

            self.update_table()
            
        def update_table(self):
            for child in self.users_display.winfo_children():
                child.destroy()
            text_width = 37
            if user_manager.user_infos:
                row = 0
                for user_info in user_manager.user_infos:
                    tkinter.Label(self.users_display, text = user_info.username).grid(row = row, column = 0, sticky = "w" + "n", pady = self.pady)
                    tkinter.Label(self.users_display, text = ("Yönetici" if user_info.admin else "Öğretmen"), padx = self.padx).grid(row = row, column = 1, sticky = "w" + "n", pady = self.pady)
                    tkinter.Label(self.users_display, text = "Şifre: ", padx = self.padx).grid(row = row, column = 2, sticky = "w" + "n", pady = self.pady)
                    password_display = tkinter.Entry(self.users_display, width = 18)
                    password_display.insert(0, user_info.password)
                    password_display.config(state='disabled')
                    password_display.grid(row = row, column = 3, sticky = "n" + "s" + "w")
                    tkinter.Button(self.users_display, text = "Şifreyi Sıfırla", command = lambda user_info = user_info: self.reset_password(user_info)).grid(row = row, column = 4, sticky = "w" + "n", padx = self.padx, pady = self.pady)
                    row += 1
                    if not user_info.admin:
                        tkinter.Label(self.users_display, text = "Atanan Sınıflar: ", padx = self.padx).grid(row = row, column = 0, sticky = "w" + "n", pady = self.pady)
                        cover = tkinter.Frame(self.users_display, pady = self.pady)
                        topic_display = tkinter.Text(cover, width = text_width, height = 2, wrap = "word", bd = 0)
                        classrooms_list_text = []
                        for classroom_id in user_info.classroom_ids:
                            try:
                                classrooms_list_text.append(user_manager.classrooms[classroom_id].prepare_name())
                            except:
                                continue
                        classrooms_list_text.sort(key = lambda key: key.split("-")[1])
                        classrooms_list_text.sort(key = lambda key: key.split("-")[0])
                        topic_display.insert("insert", ", ".join(classrooms_list_text))
                        topic_display.configure(font=("TkDefaultFont"), state = "disabled")
                        topic_display.pack()
                        cover.grid(row = row, column = 1, columnspan = 3, sticky = "w" + "n", pady = self.pady)
                        tkinter.Button(self.users_display, text = "Düzenle", command = lambda user_info = user_info: self.open_classroom_assigner(user_info)).grid(row = row, column = 4, pady = self.pady, sticky = "w" + "n", padx = self.padx)
                        row += 1
                        tkinter.Label(self.users_display, text = "Atanan Dersler: ", padx = self.padx).grid(row = row, column = 0, sticky = "w" + "n", pady = self.pady)
                        cover = tkinter.Frame(self.users_display, pady = self.pady)
                        topic_display = tkinter.Text(cover, width = text_width, height = 4, wrap = "word", bd = 0)
                        classes_list_text = user_info.class_names
                        classes_list_text.sort()
                        topic_display.insert("insert", ", ".join(classes_list_text))
                        topic_display.configure(font=("TkDefaultFont"), state = "disabled")
                        topic_display.pack()
                        cover.grid(row = row, column = 1, columnspan = 3, sticky = "w" + "n", pady = self.pady)
##                        tkinter.Button(self.users_display, text = "Düzenle").grid(row = row, column = 4, pady = self.pady, sticky = "w" + "n", padx = self.padx)
                        row += 1
                    teacher_display = tkinter.Entry(self.users_display, width = 16)
                    teacher_display.insert(0, user_info.teacher)
                    teacher_display.grid(row = row, column = 0, sticky = "w" + "n" + "s" + "e", pady = self.pady)
                    tkinter.Button(self.users_display, text = "İsim Değiştir", command = lambda user_info = user_info, teacher_display = teacher_display: self.change_teacher(user_info, teacher_display)).grid(row = row, column = 1, sticky = "w" + "n", pady = self.pady)
##                    tkinter.Button(self.users_display, text = "Kullanıcıyı Sil", command = lambda user_info = user_info: self.delete_user(user_info), fg = "red", bd = 0).grid(row = row, column = 4, pady = self.pady)
                    row += 1
                    tkinter.Label(self.users_display).grid(row = row, column = 0)
                    row += 1
                    tkinter.Label(self.users_display).grid(row = row, column = 0)
                    row += 1

            else:
                tkinter.Label(self.attandee_sheets_display, text = "Kayıtlı bir kullanıcı bulunamadı.").pack()

        def return_to_menu(self):
            self.parent.changePresentation("main_menu")

        def mousewheel(self, event):
            try:
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass
            
        def reset_password(self, user_info):
            user = user_manager.get_active_user()
            username = user.username
            password = user.password
            message = send_message("command/reset_password~{}~{}~{}".replace("~", split_char).format(username, password, user_info.username)).text.split(split_char)
            successful = False
            while message:
                action = message.pop(0)
                if action == "message":
                    server_message = message.pop(0)
                    self.message_display.config(text = server_message)
                elif action == "success": 
                    successful = True
                    user_info.password = message.pop(0)
                    if user_info.username == username:
                        user.password = user_info.password
            if successful:
                self.update_table()

        def change_teacher(self, user_info, teacher_display):
            user = user_manager.get_active_user()
            username = user.username
            password = user.password
            teacher = teacher_display.get()
            if not teacher:
                self.message_display.config(text = "İsim girdisi boş bırakılamaz.")
                return
            
            message = send_message("command/change_teacher~{}~{}~{}~{}".replace("~", split_char).format(username, password, user_info.username, teacher)).text.split(split_char)
            successful = False
            while message:
                action = message.pop(0)
                if action == "message":
                    server_message = message.pop(0)
                    self.message_display.config(text = server_message)
                elif action == "success": 
                    successful = True
                    user_info.teacher = teacher
                    if user_info.username == username:
                        user.teacher = teacher
            if successful:
                self.message_display.config(text = "Kullanıcı ismi değiştirildi.")
                self.update_table()

        def delete_user(self, user_info):
            pass

        def open_classroom_assigner(self, user_info):
            AdminPanel.Classroom_Asigner(self, user_info).mainloop()

    class Classroom_Asigner(tkinter.Toplevel):
        presentations = {"main_menu" : lambda x: AdminPanel.Classroom_Asigner.MainMenu(x)}
        
        width = 500
        height = 400
        
        def __init__(self, parent, user_info):
            self.parent = parent
            tkinter.Toplevel.__init__(self)
            
            self.title("Sınıf Atayıcı - {}".format(user_info.teacher))
            x = (self.winfo_screenwidth() // 2) - (app_width // 2) + shift_right - (Attandee_Editor.width // 2) - (Profile_Manager.width // 2)
            y = (self.winfo_screenheight() // 2) - (app_height // 2) + shift_down
            self.geometry('{}x{}+{}+{}'.format(self.width, self.height, x, y))

            self.user_info = user_info

            self.presentation = self.presentations["main_menu"](self)
            self.presentation.pack()

        def changePresentation(self, prsnt):
            self.presentation.destroy()
            self.presentation = self.presentations[prsnt](self)
            self.presentation.pack()

        class MainMenu(tkinter.Frame):
            def __init__(self, parent):
                self.parent = parent
                tkinter.Frame.__init__(self, self.parent)

                self.user_info = self.parent.user_info

                padx = 4
                tkinter.Label(self).pack()
                class_info_display = tkinter.Frame(self)
                tkinter.Label(class_info_display).pack()
                class_info_display.pack(expand = True, fill = "x")
                tkinter.Label(self).pack()
                self.classroom_id_list_selector = AdminPanel.Classroom_ID_List_Manager(self)
                self.classroom_id_list_selector.pack()
                tkinter.Label(self).pack()
                tkinter.Label(self).pack()
                buttons_frame = tkinter.Frame(self)
                tkinter.Button(buttons_frame, text = "Kaydet", command = self.send_attandee_sheet).pack(side = "right")
                buttons_frame.pack(fill = "x")
                self.message_display = tkinter.Label(self)
                self.message_display.pack()

            def send_attandee_sheet(self):
                user = user_manager.get_active_user()
                username = user.username
                password = user.password
                classroom_ids_raw = "-".join(self.classroom_id_list_selector.classroom_ids)
                message = send_message("command/set_classrooms~{}~{}~{}~{}".replace("~", split_char).format(username, password, self.user_info.username, classroom_ids_raw)).text.split(split_char)
                successful = False
                while message:
                    action = message.pop(0)
                    if action == "message":
                        server_message = message.pop(0)
                        self.message_display.config(text = server_message)
                    elif action == "success":
                        self.user_info.classroom_ids = self.classroom_id_list_selector.classroom_ids
                        successful = True
                if successful:
                    self.parent.parent.update_table()
                    self.parent.destroy()

            def exit(self):
                self.parent.parent.update_table()
                self.parent.destroy()

    class Classroom_ID_List_Manager(tkinter.Frame):
        def __init__(self, parent):
            self.parent = parent
            tkinter.Frame.__init__(self, self.parent, padx = 2, pady = 2, bg = "grey")
            
            self.user_info = self.parent.user_info
            self.classroom_ids = self.user_info.classroom_ids.copy()
            self.classroom_id_map = user_manager.get_classroom_name_id_map()
            self.classroom_keys = [x for x in self.classroom_id_map]
            self.classroom_keys.sort(key = lambda key: key.split("-")[1])
            self.classroom_keys.sort(key = lambda key: key.split("-")[0])
            self.classroom_id_var_list = [tkinter.BooleanVar(self, True) if self.classroom_id_map[key] in self.classroom_ids else tkinter.BooleanVar(self, False) for key in self.classroom_keys]

            height = 210
            height_lines = 10
            self.padx = 4
            
            self.canvas = tkinter.Canvas(self)
            
            scrollbar = tkinter.Scrollbar(self, orient = "vertical", command = self.canvas.yview)
            self.canvas.configure(yscrollcommand = scrollbar.set)

            self.classrooms_display = tkinter.Frame(self.canvas, padx = self.padx)
            self.classrooms_display.bind("<Configure>", lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all"), width = self.classrooms_display.winfo_width(), height = min(self.classrooms_display.winfo_height(), height)))
            self.canvas.create_window((0, 0), window = self.classrooms_display, anchor = "nw")

            self.canvas.bind_all("<MouseWheel>", self.mousewheel)

            self.canvas.pack(side="left", fill = "y")
            scrollbar.pack(side="left", fill = "y")

            classrooms_display_frame = tkinter.Frame(self, padx = self.padx)
            tkinter.Label(classrooms_display_frame, text = "Atanan Sınıflar", width = 15).pack()
            self.classrooms_list_display = tkinter.Text(classrooms_display_frame, width = 18, height = height_lines, wrap = "word", bd = 0)
            self.classrooms_list_display.configure(font=("TkDefaultFont"), state = "disabled")
            self.classrooms_list_display.pack()
            classrooms_display_frame.pack(side = "left", anchor = "n", fill = "y")

            row = 0
            anchor_label = tkinter.Label(self.classrooms_display)
            anchor_label.grid(row = row, column = 0, sticky = "n" + "s")
            tkinter.Label(self.classrooms_display, text = "Sınıf", padx = self.padx).grid(row = row, column = 2, sticky = "w" + "n")
            row += 1
            for ind in range(len(self.classroom_keys)):
                key = self.classroom_keys[ind]
                var = self.classroom_id_var_list[ind]
                tkinter.Checkbutton(self.classrooms_display, onvalue = True, offvalue = False, variable = var, command = self.update_displays, padx = self.padx, state = "active").grid(row = row, column = 0, sticky = "w" + "n")
                tkinter.Frame(self.classrooms_display, bg = "grey", padx = self.padx).grid(row = row, column = 1, sticky = "n" + "s")
                tkinter.Label(self.classrooms_display, text = key, padx = self.padx).grid(row = row, column = 2, sticky = "w" + "n")
                row += 1

            self.update_displays()

        def update_displays(self):
            classroom_list_display_text = ""
            self.classroom_ids = []
            for ind in range(len(self.classroom_keys)):
                if self.classroom_id_var_list[ind].get():
                    self.classroom_ids.append(self.classroom_id_map[self.classroom_keys[ind]])
                    classroom_list_display_text += self.classroom_keys[ind] + ", "
            self.classrooms_list_display.configure(state = "normal")
            self.classrooms_list_display.delete('1.0', "end")
            self.classrooms_list_display.insert("insert", classroom_list_display_text[:-2])
            self.classrooms_list_display.configure(state = "disabled")

        def mousewheel(self, event):
            try:
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass
            

split_char = "~"
user_manager = User_Manager()

extension = os.path.splitext(sys.argv[0])[1]
os.rename(sys.argv[0], "{} v{}{}".format(app_name, version_full, extension))

main = tkinter.Tk()
main.title(app_name)
x = (main.winfo_screenwidth() // 2) - (app_width // 2) + shift_right + (Attandee_Editor.width // 2) - (Profile_Manager.width // 2)
y = (main.winfo_screenheight() // 2) - (app_height // 2) + shift_down
main.geometry('{}x{}+{}+{}'.format(app_width, app_height, x, y))
MainApp(main).pack()
main.mainloop()

user_manager.save_to_file()
