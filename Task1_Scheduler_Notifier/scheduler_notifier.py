from tkinter import Tk, Button, Label, LabelFrame, E, W, Entry, END, StringVar
from tkinter import ttk
import winsound
from plyer import notification
import time
import sqlite3


class Alarm:
    db_name = 'scheduler.db'

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.frameWork()
        self.table_view()
        self.all_buttons()
        self.record_list()

    # connect to the database
    def db_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            print(conn)
            print(" You have successfully connected to the database")
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        return query_result

    # frame for inputs
    def frameWork(self):
        allFrame = LabelFrame(self.mainWindow, text="Add Task", bg='grey', font='helvetica 10')
        allFrame.grid(row=0, column=0, sticky=E, pady=10)

        Label(allFrame, text='Time(HH:MM):', bg='black', fg='white').grid(row=1, column=1, sticky='ew', pady=2, padx=15)
        self.timeField = Entry(allFrame, width=27)
        self.timeField.grid(row=1, column=2, sticky='ew', padx=5, pady=2)

        Label(allFrame, text='Day-Month(D M)', bg='black', fg='white').grid(row=2, column=1,
                                                                            sticky='ew', pady=2, padx=15)
        self.monthDay = Entry(allFrame, width=27)
        self.monthDay.grid(row=2, column=2, sticky='ew', padx=5, pady=2)

        Label(allFrame, text='Task To-Do:', bg='black', fg='white').grid(row=3, column=1, sticky='ew', pady=2, padx=15)
        self.todoField = Entry(allFrame, width=27)
        self.todoField.grid(row=3, column=2, sticky='ew', padx=5, pady=2)

        Label(allFrame, text='Choose Alarm Tone:', bg='black', fg='white').grid(row=4, column=1,
                                                                                sticky='ew', pady=2, padx=15)
        n = StringVar()
        self.choosen = ttk.Combobox(allFrame, width=27, textvariable=n)
        self.choosen["values"] = ("bleeping-alarm",
                                  "Annoying-sound1",
                                  "Creepy-clock-chiming1",
                                  "Fast-clock-ticking1",
                                  "Fast-High-Pitch",
                                  "Twin-bell")
        self.choosen.grid(row=4, column=2, sticky='ew', padx=5, pady=2)

        Button(allFrame, text="Add Task", command=self.add_task,
               bg="black", fg="white").grid(row=5, column=2, sticky=E, padx=5, pady=5)

    # all entries in a table
    def table_view(self):
        self.table = ttk.Treeview(height=10, columns=("month", "todo", "music"))
        self.table.grid(row=6, column=0, columnspan=3)
        self.table.heading('#0', text='Alarm Time')
        self.table.heading('month', text='Month & Date')
        self.table.heading('todo', text='Task To-Do')
        self.table.heading('music', text='Music')

    # modification of side buttons
    def all_buttons(self):
        button_frame = Label(mainWindow)
        button_frame.grid(row=0, column=1, sticky=W, padx=10)

        Button(button_frame, text="Delete", command=self.delete_task, bg="red",
               fg="black").grid(row=0, column=0, sticky='ew', pady=5)

        Button(button_frame, text="SET", command=self.alarm_logic,
               bg="blue", fg="black").grid(row=1, column=0, sticky='ew', pady=5)

        Button(button_frame, text="Cancel", command=mainWindow.quit,
               bg="Red", fg="black").grid(row=2, column=0, sticky='ew', pady=5)

    # add task on scheduler
    def add_task(self):
        if len(self.timeField.get()) != 0 and len(self.monthDay.get()) != 0 and len(self.todoField.get()) != 0 and len(
                self.choosen.get()):
            query = "INSERT INTO todo_list VALUES(NULL, ?,?,?,?)"
            parameters = (self.timeField.get(), self.monthDay.get(), self.todoField.get(), self.choosen.get())
            self.db_query(query, parameters)
            notification.notify(title="Alarm Set",
                                message=f"You will be notified on {self.monthDay.get()} at {self.timeField.get()}",
                                app_icon="F:\\The_Intern_Academy\\project1\\icons\\favicon.ico",
                                timeout=15)

            self.timeField.delete(0, END)
            self.monthDay.delete(0, END)
            self.todoField.delete(0, END)
            self.choosen.delete(0, END)
            self.record_list()

    # delete task from list and also from database
    def delete_task(self):
        timer = self.table.item(self.table.selection())['text']
        query = "DELETE FROM todo_list WHERE timer = ?"
        self.db_query(query, (timer,))
        self.record_list()

    # after executing all alarms, automatically delete all entries
    def delete_automatically(self):
        query = 'DELETE FROM todo_list'
        self.db_query(query)
        self.record_list()

    # show updated entries into the table
    def record_list(self):
        items = self.table.get_children()
        for item in items:
            self.table.delete(item)
        query = "SELECT * FROM todo_list ORDER BY month DESC, timer DESC"
        contact_entries = self.db_query(query)
        for row in contact_entries:
            self.table.insert('', 0, text=row[1], values=(row[2], row[3], row[4]))

    # main logic for notification and alarm
    def alarm_logic(self):
        query = "SELECT * FROM todo_list ORDER BY month, timer"
        select_entries = self.db_query(query)
        current_time = time.strftime("%H:%M")
        current_date = time.strftime("%d %B")
        for set_time in select_entries:
            print(set_time[1], set_time[2], set_time[3], set_time[4])  # todo:  remove it
            while current_time != str(set_time[1]):
                current_time = time.strftime("%H:%M")
                time.sleep(1)
            if current_time == str(set_time[1]) and current_date == str(set_time[2]):
                for _ in range(3):
                    winsound.PlaySound("F:\\The_Intern_Academy\\project1\\musics\\"+ str(set_time[4]) + ".wav", winsound.SND_ASYNC | winsound.SND_ALIAS)
                    notification.notify(title="Reminder", message=f"It's time to {str(set_time[3])}",
                                        app_icon="F:\\The_Intern_Academy\\project1\\icons\\calender-schedule-time-management.ico",
                                        timeout=15)
                    time.sleep(15)
                    winsound.PlaySound(None, winsound.SND_ASYNC)

        self.delete_automatically()


if __name__ == "__main__":
    mainWindow = Tk()
    mainWindow.title("Scheduler with Alarm")
    application = Alarm(mainWindow)
    mainWindow.mainloop()
