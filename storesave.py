import tkinter as tk
from ctypes import*
import time
import numpy as np

salib = CDLL(".//bin//sa_api.dll")
tglib = CDLL(".//bin//tg_api.dll")

class Storedata:
    def __init__(self,master):
        self.master = master
        self.frame = tk.Frame(self.master).grid(row=1,column=3)
        self.label1 = tk.Label(self.frame,text="1st Solution ")
        self.label2 = tk.Label(self.frame,text="2nd Solution ")
        self.label3 = tk.Label(self.frame,text="3rd Solution ")
        self.button1 = tk.Button(self.frame,text='store',bd=5,command=self.store_function1)
        self.button2 = tk.Button(self.frame,text='store',bd=5,command=self.store_function2)
        self.button3 = tk.Button(self.frame,text='store',bd=5,command=self.store_function3)
        self.button = tk.Button(self.frame,text="reset store",command=self.reset,bd=2,bg="firebrick1",font=("Helvetica", 10))
        
    #Grid position 
        self.label1.grid(row=1,column=3)
        self.label2.grid(row=2,column=3)
        self.label3.grid(row=3,column=3)
        self.button1.grid(row=1,column=4)
        self.button2.grid(row=2,column=4)
        self.button3.grid(row=3,column=4)
        self.button.grid(row=5,column=4,stick='w')

    def store_function1(self):
        self.store1 = 1
        self.button1 = tk.Button(self.frame,text='store',bd=5,state='disabled').grid(row=1,column=4)
        
    
    def store_function2(self):
        self.store2 = 2
        print('store2')
        self.button2 = tk.Button(self.frame,text='store',bd=5,state='disabled').grid(row=2,column=4)

    
    def store_function3(self):
        self.store3 = 4 
        print(self.store3)
        self.button3 = tk.Button(self.frame,text='store',bd=5,state='disabled').grid(row=3,column=4)
    
    def reset(self):
        print('reset')
        self.button1 = tk.Button(self.frame,text='store',command=self.store_function1,bd=5).grid(row=1,column=4)
        self.button2 = tk.Button(self.frame,text='store',command=self.store_function2,bd=5).grid(row=2,column=4)
        self.button3 = tk.Button(self.frame,text='store',command=self.store_function3,bd=5).grid(row=3,column=4)

class Comment:
    def __init__(self,master):
        self.master = master
        self.text_comment = tk.StringVar()
        self.percentage_amine = tk.DoubleVar()
        self.frame = tk.Frame(self.master).grid(row=2,column=1)
        self.label = tk.Label(self.frame,text='Comment')
        self.label2 = tk.Label(self.frame,text="Percentage Amine(%)")
        self.entry = tk.Entry(self.frame,textvariable=self.text_comment,borderwidth=2,highlightcolor="blue",width=20,font=('Helvetica',10))
        self.entry2 = tk.Entry(self.frame,textvariable=self.percentage_amine,width=10)
        self.button = tk.Button(self.frame,text='save',command=self.save)
    
    # #Grid set up 
   
        self.label.grid(row=3,column=0)
        self.label2.grid(row=4,column=0)
        self.entry.grid(row=3,column=1)
        self.entry2.grid(row=4,column=1,stick='w')
        self.button.grid(row=3,column=2)

    def save(self):
        self.operation_comment=self.text_comment.get()
        print(self.operation_comment)
        self.percentage = self.percentage_amine.get()
        print('percentage: %.1f '%(self.percentage))
        self.entry.delete(0, 'end')
        self.entry2.delete(0, 'end')

class Comparison:
    def __init__(self,master):
        self.master = master
       
        self.frame = tk.Frame(self.master).grid(row=1,column=5)
        self.canvas1 =tk.Canvas(self.frame, width=20, height=20, borderwidth=5, highlightthickness=0, bg="green")
        self.canvas2 =tk.Canvas(self.frame, width=20, height=20, borderwidth=5, highlightthickness=0, bg="green")
        self.canvas3 =tk.Canvas(self.frame, width=20, height=20, borderwidth=5, highlightthickness=0, bg="red")
        self.canvas4 =tk.Canvas(self.frame, width=20, height=20, borderwidth=5, highlightthickness=0, bg="green")
        self.canvas5 =tk.Canvas(self.frame, width=20, height=20, borderwidth=5, highlightthickness=0, bg="green")
        self.canvas6 =tk.Canvas(self.frame, width=20, height=20, borderwidth=5, highlightthickness=0, bg="red")
        self.canvas7 =tk.Canvas(self.frame, width=20, height=20, borderwidth=5, highlightthickness=0, bg="red")
        self.canvas8 =tk.Canvas(self.frame, width=20, height=20, borderwidth=5, highlightthickness=0, bg="red")
        self.canvas9 =tk.Canvas(self.frame, width=20, height=20, borderwidth=5, highlightthickness=0, bg="red")
        
    #Grid position 
        self.canvas1.grid(row=1,column=5,padx=2)
        self.canvas2.grid(row=1,column=6,padx=2)
        self.canvas3.grid(row=1,column=7,padx=2)
        self.canvas4.grid(row=2,column=5,padx=2)
        self.canvas5.grid(row=2,column=6,padx=2)
        self.canvas6.grid(row=2,column=7,padx=2)
        self.canvas7.grid(row=3,column=5,padx=2)
        self.canvas8.grid(row=3,column=6,padx=2)
        self.canvas9.grid(row=3,column=7,padx=2)
        
        
        

    def solution_compare(self):
        self.value_store1 = Storedata.self.store1
        print('aa')
        pass
