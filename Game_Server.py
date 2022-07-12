from functools import partial
import tkinter
from tkinter import *
from turtle import screensize
from click import command
from cv2 import rotate
import numpy as np
from pandastable import Table
from tkinter import ttk
import Module.data_process as dp
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import Module.server as ser
from _thread import *
import os
from tkcalendar import *
from datetime import date, datetime
from tkinter import messagebox 
from Module.Analyse import *


main_dir = os.path.split(os.path.abspath(__file__))[0]
load_image=lambda filename: os.path.join(main_dir, "data", filename)

class Display():
    def __init__(self):
        self.window=Tk()
        self.window.title('Game Server')
        self.window.geometry('1000x700+100+50')
        self.font=("Helvetica", 20)
        self.object= dp.User_Data()
        self.today=date.today()
        self.put_manual()
        # self.put_Menu()
        self.window.mainloop()
        self.exec=False
        self.reset=True

    def get_text(self, text_in):
        style = ttk.Style()
        style.configure("Bold.TLabel", font=("Helvetica", 12, "bold"))
        label = ttk.Label(text=text_in, style="Bold.TLabel")
        return label

    def put_manual(self):

        menubar = Menu(self.window)
        file = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label ='Home', menu = file)
        file.add_command(label ='Operate Server', command = self.Start_Server)
        file.add_separator()
        file.add_command(label ='Exit', command = self.window.destroy)

        edit = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label ='Management', menu = edit)
        edit.add_command(label ='User Management', command = self.Statis_Screen)
        edit.add_command(label ='Question Management', command = None)
        self.window.config(menu = menubar)

    def Statis_Screen(self):
        self.user_Screen = ttk.LabelFrame(self.window, labelwidget=self.get_text('User Statistic') , width=990, height=700, borderwidth=10)
        self.user_Screen.pack(padx=5, pady=1, side=tkinter.LEFT)

        self.list_button=[]
        self.prev=None

        self.Op1=Button(self.window, text="Registered Player", fg='black', font=("Helvetica", 10), command=partial(self.put_option, self.user_Screen, "Registered Player", 1))
        self.Op1.place(x=300, y=15)
        self.list_button.append(self.Op1)

        self.Op2=Button(self.window, text="Playing Player", fg='black', font=("Helvetica", 10), command=partial(self.put_option, self.user_Screen, "Playing Player", 2))
        self.Op2.place(x=420, y=15)
        self.list_button.append(self.Op2)

        self.Op3=Button(self.window, text="Get Rank", fg='black', font=("Helvetica", 10), command=partial(self.put_option, self.user_Screen, "Get Rank", 3))
        self.Op3.place(x=520, y=15)
        self.list_button.append(self.Op3)


    def put_option(self, master, text, button):

        if (self.prev!=None):
           self.prev.pack_forget()
    
        for i in range(1,4):
            if i==button:
                self.list_button[i-1].configure(bg='green')
            else:
                self.list_button[i-1].configure(bg='white')

        local_frame = ttk.LabelFrame(master, labelwidget=self.get_text(text) , width=990, height=700)
        local_frame.pack(side=tkinter.LEFT)
        self.prev=local_frame
        if button==1 or button==2:
            self.put_day_statistic(self.prev)
            self.put_big_static(self.prev)
        else:
            self.put_rank_static(self.prev)

    def put_day_statistic(self, master):

        self.frame = ttk.LabelFrame(master, labelwidget=self.get_text('Day Statistics') , width=300, height=280)
        self.frame.place(x=650, y=10)
        self.days=date.today()
        self.number=0
        format_date = f"{self.days: %d/%m/%Y}"
        self.date_picker=Button(self.frame, text="Pick date", fg='black', font=("Helvetica", 10), command=partial(self.create_calendar, self.frame))
        self.date_picker.place(x=10, y=10)
        self.tus=Label(self.frame, text='Date: Today '+format_date, font=("Helvetica", 10))
        self.tus.place(x=10, y=60)
        self.infor=Label(self.frame, text='Number of new player: 0', font=("Helvetica", 10))
        self.infor.place(x=10, y=80)

        self.solve_picker=Button(self.frame, text="Filter", fg='black', font=("Helvetica", 10), command=partial(self.show_date_statistics, self.prev))
        self.solve_picker.place(x=200, y=200)

    def show_date_statistics(self, master):
        year, month, day=str(self.days).split('-')
        data=self.object.get_statistics(3, [month, year])
        self.number=data[0][int(day)]
        self.infor.configure(text='Number of new player: {:d}'.format(self.number))

    def create_calendar(self, master):
        global cal
        self.local_frame = ttk.Frame(master, width=master.winfo_width()-20, height=master.winfo_height()-50)
        self.local_frame.place(x=10, y=10)
        cal=Calendar(self.local_frame, selectmode="day",year= self.days.year, month=self.days.month, day=self.days.day, maxdate=date.today())
        cal.place(x=10, y=5)
        Button(self.local_frame, text="Choose", fg='black', font=("Helvetica", 10), command=partial(self.get_day, self.local_frame)).place(x=10, y=200)
        
    def get_day(self, master):
        date_get=datetime.strptime(cal.get_date(), '%m/%d/%y')
        self.days=date_get.date()
        format_date = f"{self.days: %d/%m/%Y}"
        self.tus.config(text='Date: '+ format_date)
        self.local_frame.place(anchor="nw", x=0, y=0, width=0, height=0)
        
    def put_big_static(self, master):

        self.frame1 = ttk.LabelFrame(master, labelwidget=self.get_text('Time Statistics') , width=300, height=300)
        self.frame1.place(x=650, y=300)
        self.list_widget=[]
        Label(self.frame1, text='Year: ', font=("Helvetica", 10)).place(x=10, y=10)
        self.year_select = ttk.Combobox(self.frame1, width = 15)
        list_year=[i for i in range(2016, self.today.year+1)]
        self.year_select['values'] = tuple(list_year)
        self.year_select['state']='readonly'
        self.year_select.current(6)

        self.year_select.place(x=50, y=10)
        self.year_select.bind("<<ComboboxSelected>>", self.calBackyear)
 
        self.list_label=[]

        values = {"Quarter" : "1",
                  "Month" : "2"}
        
        self.quarter_select=Radiobutton(self.frame1, text = "Quarter", value = "1", command=self.check_quarter)
        self.quarter_select.place(x=50, y=40)

        self.quarter_selects = ttk.Combobox(self.frame1, width = 15)
        list_quarter=[i for i in range(0, self.today.month//3+2)]
        self.quarter_selects['values'] = tuple(list_quarter)
        self.quarter_selects['state']='readonly'
        self.quarter_selects.current(list_quarter.index(list_quarter[-1]))
        self.quarter_selects.place(x=150, y=40) 


        self.month_select=Radiobutton(self.frame1, text = "Month", value = "2", command=self.check_month)
        self.month_select.place(x=50, y=70)
        self.month_selects = ttk.Combobox(self.frame1, width = 15)
        list_month=[i for i in range(0, self.today.month+1)]
        self.month_selects['values'] = tuple(list_month)
        self.month_selects['state']='readonly'
        self.month_selects.current(list_month.index(list_month[-1]))
        self.month_selects.place(x=150, y=70) 
       
        self.month_select_check=True
        self.quarter_select_check=False


        self.infor_total=Label(self.frame1, text='', font=("Helvetica", 10))
        self.infor_total.place(x=10, y=130)

        Button(self.frame1, text="Show Statistics", fg='black', bg='green', font=("Helvetica", 10), command=partial(self.show_statis, self.frame1)).place(x=195, y=245)
    
    def show_other_detail(self,  master, list_print):
        for item in self.list_label:
            item.destroy()
        self.list_label.clear()
        start=150
        for item in list_print:
            label=Label(master, text=item , font=("Helvetica", 10))
            label.place(x=10, y=start)
            self.list_label.append(label)
            start+=20
            
    def check_month(self):
        self.month_select_check=True
        self.quarter_select_check=False
    
    def check_quarter(self):
        self.month_select_check=False
        self.quarter_select_check=True
    
    def show_statis(self, master):
        year=self.year_select.get()
        self.time_sta=Year(str(year))
        if self.month_select_check==True:
            month=self.month_selects.current()
            if month==0:
                self.time_sta.get_detail(2)
                self.cur_graph=self.time_sta.get_graph()
                self.infor_total.configure(text=self.time_sta.print)
                self.show_other_detail(master, self.time_sta.detail.print[:2])
                self.showGraph1((300, 10), self.cur_graph, ['Month', 'New player', 'Month Statistics'])
            else:
                strmonth=''
                if month<10:
                    strmonth='0'+str(month)
                else:
                    strmonth=str(month)
                self.time_sta.get_detail(2, strmonth)
                self.cur_graph=self.time_sta.get_graph()
                self.infor_total.configure(text=self.time_sta.print)
                self.show_other_detail(master, self.time_sta.detail.print)
                self.showGraph1((300, 10), self.cur_graph, ['Day', 'New player', 'Date Statistics'])
            
        else:
            quarter=self.quarter_selects.current()
            if quarter==0:
                self.time_sta.get_detail(1)
                self.cur_graph=self.time_sta.get_graph()
                self.infor_total.configure(text=self.time_sta.print)
                self.show_other_detail(master, self.time_sta.detail.print[:2])
                self.showGraph1((300, 10), self.cur_graph, ['Quarter', 'New player', 'Quarter Statistics'])
            else:
                
                self.time_sta.get_detail(1, str(quarter))
                self.cur_graph=self.time_sta.get_graph()
                self.infor_total.configure(text=self.time_sta.print)
                self.show_other_detail(master, self.time_sta.detail.print)
                self.showGraph1((300, 10), self.cur_graph, ['Month', 'New player', 'Month Statistics'])
                

    def calBackyear(self, event):

        year = event.widget.get()
        
        if int(year)!=self.today.year:
            self.quarter_selects['values'] = tuple([i for i in range(0, 5)])
            self.month_selects['values'] = tuple([i for i in range(0, 13)])

        else:
            self.quarter_selects['values']=[i for i in range(0, self.today.month//3+2)]
            self.month_selects['values']= [i for i in range(0, self.today.month+1)]


    def showTable(self, master, pos, df):

        self.clear_widget()
        f = Frame(master)
        f.place(x=pos[0], y=pos[1])
        self.table = pt = Table(f, dataframe=df, showtoolbar=True, showstatusbar=True)
        pt.show()
        self.list_widget.append(f)

            
    def clear_widget(self):
        for item in self.list_widget:
            item.destroy()
        self.list_widget.clear()


    def put_rank_static(self, master):

        self.frame2 = ttk.LabelFrame(master, labelwidget=self.get_text('Rank Option') , width=250, height=250)
        self.frame2.place(x=10, y=10)
        self.list_widget=[]
        self.mode_select = ttk.Combobox(self.frame2, width = 15)
        self.mode_select['values'] = ('Score Statistics', 'Time Statistics')
        self.mode_select['state']='readonly'
        self.mode_select.current(0)
        self.mode_select.place(x=10, y=10)
        self.all=True
        self.local_frame1=None

        Label(self.frame2, text='Choose Time Range', font=("Helvetica", 10)).place(x=10, y=40)

        self.time_select2=Radiobutton(self.frame2, text = "Time span", value = "2", command=partial(self.show_time_picker, self.frame2))
        self.time_select2.place(x=50, y=90)

        self.time_select1=Radiobutton(self.frame2, text = "All", value = "1", command=self. reset_time)
        self.time_select1.place(x=50, y=70)

        Button(self.frame2, text="Show table", fg='black', bg='yellow', font=("Helvetica", 10), command=partial(self.get_time_span, 1, master)).place(x=10, y=160)
        Button(self.frame2, text="Show graph", fg='black', bg='yellow', font=("Helvetica", 10), command=partial(self.get_time_span, 2, master)).place(x=10, y=190)

    def show_time_picker(self, master):

        self.all=False

        self.local_frame1 = ttk.Frame(master, width=master.winfo_width()-100, height=master.winfo_height()-200)
        self.local_frame1.place(x=50, y=110)

        Label(self.local_frame1, text='From: ', font=("Helvetica", 10)).place(x=10, y=10)
        self.cal1=DateEntry(self.local_frame1, selectmode="day",year= self.today.year, month=self.today.month, day=self.today.day, maxdate=date.today())
        self.cal1.place(x=50, y=10)

        Label(self.local_frame1, text='To: ', font=("Helvetica", 10)).place(x=10, y=30)
        self.cal2=DateEntry(self.local_frame1, selectmode="day",year= self.today.year, month=self.today.month, day=self.today.day, maxdate=date.today())
        self.cal2.place(x=50, y=30)

    def format(self, date):
        date_get=datetime.strptime(date, '%m/%d/%y')
        self.days=date_get.date()
        format_date = f"{self.days: %Y-%m-%d}"
        return format_date

    def reset_time(self):
        if (self.local_frame1!=None):
            self.local_frame1.place(anchor="nw", x=0, y=0, width=0, height=0)
        self.all=True

    def get_time_span(self, index, master):

        if self.all!=True:
            begin_time=self.cal1.get_date()
            end_time=self.cal2.get_date()
            if end_time<begin_time:
                messagebox.showinfo("Error","Date end must be after date begin") 
                return None
            else: 
                time_span=(str(begin_time), str(end_time))
        else:
            time_span=None
        df=None
        if self.mode_select.current()==0:
            if self.all==True:
                df=self.object.get_rank_score('all')
            else:
                df=self.object.get_rank_score('loc', time_span)
            if index==1:
                self.showTable(master, (300, 70), df)
            else:
                self.showGraph(master,(300, 70), df)

        else:
            if self.all==True:
                df=self.object.get_rank_time('all')
            else:
                df=self.object.get_rank_time('loc', time_span)
            if index==1:
                self.showTable(master, (300, 70), df)
            else:
                self.showGraph(master,(300, 70), df)


    def showGraph(self, master_in, pos, df, title=None):
        tab = ttk.Frame(master_in, width=700, height=600)
        tab.place(x=300, y=10)
        if len(df.index>10):
            df=df.iloc[:10]
        self.clear_widget()
        list_name=list(df.columns.values)
        fig = Figure()
        # list of squares
        ax = fig.add_axes([0.15,0.15,0.8,0.7])
        # plotting the graph
        ax.bar(df.iloc[:,0], df.iloc[:,1], color = ['green', 'red', 'blue'])
        ax.set_xlabel (list_name[0])
        ax.set_ylabel (list_name[1])
        ax.tick_params(axis='x', labelrotation=30)
        ax.set_title  (title)
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=tab)  
        canvas.draw()
        # placing the canvas on the Tkinter window
        graph1=canvas.get_tk_widget()
        graph1.place(x=pos[0], y=pos[1])
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas, tab)
        toolbar.update()
        # placing the toolbar on the Tkinter window
        graph=canvas.get_tk_widget()
        graph.pack()
        self.list_widget.append(tab)

    def showGraph1(self, pos, df, title=None):
        master_in=self.prev
        tab = ttk.Frame(master_in, width=700, height=600)
        tab.place(x=10, y=10)
        self.clear_widget()
        fig = Figure()
        # list of squares
        ax = fig.add_axes([0.15,0.15,0.8,0.7])
        # plotting the graph
        idx = np.asarray([i for i in df.keys()])
        ax.bar(df.keys(), df.values(), color = ['green', 'red', 'blue'])
        ax.set_xlabel (title[0])
        ax.set_xticks(idx)
        ax.set_ylabel (title[1])
        ax.tick_params(axis='x', labelrotation=30)
        ax.set_title  (title[2])
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=tab)  
        canvas.draw()
        # placing the canvas on the Tkinter window
        graph1=canvas.get_tk_widget()
        graph1.place(x=pos[0], y=pos[1])
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas, tab)
        toolbar.update()
        # placing the toolbar on the Tkinter window
        graph=canvas.get_tk_widget()
        graph.pack()
        self.list_widget.append(tab)


    def Question_Management(self):
        pass

    def Start_Server(self):
        start_new_thread(ser.Start_Server, ())

screen=Display()