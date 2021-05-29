import tkinter as tk
import csv
from ctypes import*
import time
import datetime
import numpy as np
import getsweep
import os
import pandas as pd
import percencal

salib = CDLL(".//bin//sa_api.dll")
tglib = CDLL(".//bin//tg_api.dll")

aa1 = np.array([])
aa2 = np.array([])
aa3 = np.array([])
freGHz = np.linspace(2.4,3.2, num=801, dtype=np.float)
LeanNum = 0
com12 = None
com13 = None
com23 = None
thstore = 1.5 # store threshold 
thstorEva = 2 # evaluate threshold 2

def savetocsv(savrdir, leanNum, collectDate, percentage, operation_comment):
    timestamp = str(datetime.datetime.now().minute)+str(datetime.datetime.now().second)
    savetodir = savrdir+ '\\csv'+"\\LEAN#" +str(leanNum)+ '\\' +collectDate+ '#' +str(percentage)+ '#' +operation_comment+ '#' +timestamp+ '.csv'
    amplitude = (aa1+aa2+aa3)/3
    dictowrite = {'freGHz':freGHz, 'amplitude':amplitude}
    dftowrite = pd.DataFrame.from_dict(dictowrite)
    dftowrite.to_csv(savetodir, sep=',', index=None, header=True)
    

# def WritetoCSV(DataIn):
#     with open('outcsv1.csv', select, newline='a') as new_file:
#         csv_write = csv.writer(new_file, delimiter=',')
#         csv_write.writerows(DataIn)

# def creDatatable(percentage,operation_comment):
#     datatowrite=[]
#     correctstr=[]
    
#     datenow = str(datetime.datetime.now().month)+"-"+str(datetime.datetime.now().day)+"-"+str(datetime.datetime.now().year)
#     timenow = str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)
#     averageArray = (aa1+aa2+aa3)/3
#     correctstr.append(percentage)
#     correctstr.append(datenow)
#     correctstr.append(timenow)
#     correctstr = correctstr + averageArray.tolist()
#     correctstr.append(operation_comment)

#     datatowrite.append(correctstr)
#     return datatowrite


class Storedata:
    def __init__(self,master,handle,status):
        self.handle = handle        
        self.master = master
        self.status = status
        self.frame = tk.Frame(self.master)
        self.label1 = tk.Label(self.frame,text="1st Solution ")
        self.label2 = tk.Label(self.frame,text="2nd Solution ")
        self.label3 = tk.Label(self.frame,text="3rd Solution ")
        self.button1 = tk.Button(self.frame,text='store',bd=5,command=self.store_function1)
        self.button2 = tk.Button(self.frame,text='store',bd=5, state='disabled')
        self.button3 = tk.Button(self.frame,text='store',bd=5, state='disabled')
        self.button = tk.Button(self.frame,text="reset store",command=self.reset,bd=2,bg="firebrick1",font=("Helvetica", 10))
        self.com12Lable = tk.Label(self.frame,text="error 1-2 % :")
        self.com13Lable = tk.Label(self.frame,text="error 1-3 % :")
        self.com23Lable = tk.Label(self.frame,text="error 2-3 % :")
        self.com12LableShow = tk.Label(self.frame,text='--.--')
        self.com13LableShow = tk.Label(self.frame,text='--.--')
        self.com23LableShow = tk.Label(self.frame,text='--.--')
        
    #Grid position 
        self.frame.grid(row=1,column=3)
        self.label1.grid(row=1,column=3)
        self.label2.grid(row=2,column=3)
        self.label3.grid(row=3,column=3)
        self.button1.grid(row=1,column=4)
        self.button2.grid(row=2,column=4)
        self.button3.grid(row=3,column=4)
        self.button.grid(row=4,column=4)
        self.com12Lable.grid(row=1,column=5)
        self.com13Lable.grid(row=2,column=5)
        self.com23Lable.grid(row=3,column=5)
        self.com12LableShow.grid(row=1,column=6)
        self.com13LableShow.grid(row=2,column=6)
        self.com23LableShow.grid(row=3,column=6)
        

    def store_function1(self):
        if self.status.isrunning == True:
            global aa1
            aa1 = getsweep.readSweep(self.handle)
            tk.Button(self.frame,text='store',bd=5,state='disabled').grid(row=1,column=4)
            tk.Button(self.frame,text='store',bd=5,command=self.store_function2).grid(row=2,column=4)
#           print(aa1)
        else:
            self.status.print_status("It is not running")
    
    def store_function2(self):
        global aa2
        global com12
        aa2 = getsweep.readSweep(self.handle)
        # compair 1-2
        com12 = np.mean(abs((aa2-aa1)/aa1))*100
        if com12 < thstore:
            self.com12LableShow.config(text=("%0.2f"%(com12)),bg = 'green')
        else:
            self.com12LableShow.config(text=("%0.2f"%(com12)),bg = 'red')
        
        tk.Button(self.frame,text='store',bd=5,command=self.store_function3).grid(row=3,column=4)
        self.button2 = tk.Button(self.frame,text='store',bd=5,state='disabled').grid(row=2,column=4)
#        print(aa2)
    
    def store_function3(self):
        global aa3
        global com13
        global com23
        aa3 = getsweep.readSweep(self.handle)
        #compair 1-3
        com13 = np.mean(abs((aa3-aa1)/aa1))*100
        if com13 < thstore:
            self.com13LableShow.config(text=("%0.2f"%(com13)),bg='green')
        else:
            self.com13LableShow.config(text=("%0.2f"%(com13)),bg='red')
        #compair 2-3
        com23 = np.mean(abs((aa3-aa2)/aa2))*100
        if com23 < thstore:
            self.com23LableShow.config(text=("%0.2f"%(com23)),bg='green')
        else:
            self.com23LableShow.config(text=("%0.2f"%(com23)),bg='red')

        tk.Button(self.frame,text='store',bd=5,state='disabled').grid(row=3,column=4)

#        print(aa3)
    
    def reset(self):
        if self.status.isrunning == True:
            global aa1
            global aa2
            global aa3
            aa1 = np.array([])
            aa2 = np.array([])
            aa3 = np.array([])
            com12 = None
            com13 = None
            com23 = None
            self.com12LableShow.config(text=('--.--'))
            self.com13LableShow.config(text=('--.--'))
            self.com23LableShow.config(text=('--.--'))
            self.status.storenewsavestatus(True)
            self.status.storenewevarstatus(True)
            tk.Button(self.frame,text='store',command=self.store_function1,bd=5).grid(row=1,column=4)
        else:
            self.status.print_status("It is not running")
            print('It is not running')

class Comment:
    def __init__(self,master,handle,status):
        self.handle = handle
        self.master = master
        self.status = status
        self.leanNum = tk.IntVar()
        self.leanNum.set(0)
        self.collectDate = tk.StringVar()
        self.collectDate.set('YY-MM-DD')
        self.percentage_amine = tk.DoubleVar()
        self.percentage_amine.set(0)
        self.text_comment = tk.StringVar()
        self.text_comment.set('x')
        self.frame = tk.Frame(self.master)
        self.leanNumLabel = tk.Label(self.frame,text="Train Numer")
        self.collectDateLabel = tk.Label(self.frame,text="collect date")
        self.percentageLabel = tk.Label(self.frame,text="Percentage Amine(%)")
        self.commentLabel = tk.Label(self.frame,text='Comment')
        
        self.leanNumEntry = tk.Entry(self.frame,textvariable=self.leanNum,width=5)
        self.collectDateEntry = tk.Entry(self.frame,textvariable=self.collectDate,width=20)
        self.percentageEntry = tk.Entry(self.frame,textvariable=self.percentage_amine,width=20)
        self.commentEntry = tk.Entry(self.frame,textvariable=self.text_comment,borderwidth=2,highlightcolor="blue",width=20,font=('Helvetica',10))

        self.button = tk.Button(self.frame,text='save',command=self.save)
    
    # #Grid set up 
        self.frame.grid(row=1,column=0)
        self.leanNumLabel.grid(row=1, column=0)
        self.collectDateLabel.grid(row=2, column=0)
        self.percentageLabel.grid(row=3, column=0)
        self.commentLabel.grid(row=4, column=0)

        self.leanNumEntry.grid(row=1, column=1)
        self.collectDateEntry.grid(row=2,column=1)
        self.percentageEntry.grid(row=3,column=1)
        self.commentEntry.grid(row=4,column=1)
        self.button.grid(row=4,column=2)

    def save(self):
        if self.status.isrunning == True:
            if self.status.isstorenewsave == True:
                if (len(aa1) > 0 and len(aa2) > 0 and len(aa3) > 0):
                    if (com12 < thstore and com13 < thstore and com23 < thstore):
                        leanNum = self.leanNum.get()
                        if (leanNum == 1 or leanNum == 2):
                            savrdir = os.getcwd()
                            collectDate = self.collectDate.get()
                            percentage = self.percentage_amine.get()
                            operation_comment = self.text_comment.get()
                            savetocsv(savrdir, leanNum, collectDate, percentage, operation_comment)
                            self.status.print_status("Save successfully")
                            print('Save successfully')
                            self.status.storenewsavestatus(False)
                        else:
                            self.status.print_status("Incorrect lean number. Input 1 or 2 only")
                            print('Incorrect lean number. Input 1 or 2 only')
                    else:
                        self.status.print_status("error is too high")
                        print('Measurements have too much error')
                else:
                    self.status.print_status("Pleas store measurement 3 times")
                    print('Pleas store measurement 3 times')
            else:
                self.status.print_status("Press restore first")
                print('Press restore first')
        else:
            self.status.print_status("It is not running")
            print('It is not running')

class evaluate(Comment):
    def __init__(self,master,handle,status):
        super().__init__(master,handle,status)
        self.handle = handle
        self.master = master
        self.status = status
        self.frame = tk.Frame(self.master)
        self.evaluatebut = tk.Button(self.frame,text='evaluate',command=self.evaluate,bg='deep sky blue',bd=2,font=('Helvetica',10))
        self.frame.grid(row=5,column=3)
        self.evaluatebut.grid(row=5,column=3)

    def evaluate(self):
        if self.status.isrunning == True:
            if self.status.isstorenewevar == True:
                if (len(aa1) > 0 and len(aa2) > 0 and len(aa3) > 0):
                    if (com12 < thstore and com13 < thstore and com23 < thstore):
                        leanNum = self.leanNum.get()
                        if (leanNum == 1 or leanNum == 2):
                            amplitude = (aa1+aa2+aa3)/3
                            Isemtydatabase, MinMAPE, OutAmine = percencal.evaluateamine(amplitude, leanNum)
                            if Isemtydatabase == False:
                                if MinMAPE < thstorEva:
                                    self.status.print_status("amine percentage = %d"%OutAmine)
                                    print("amine percentage = %d"%OutAmine)
                                    self.status.storenewevarstatus(False)
                                else:
                                    self.status.print_status("No any match in this database but you can save")
                                    print('No any match in this database but you can save')                           
                            else: 
                                self.status.print_status("Database is emty")
                                print('Database is emty')
                        else:
                            self.status.print_status("Incorrect lean number. Input 1 or 2 only")
                            print('Incorrect lean number. Input 1 or 2 only')
                    else:
                        self.status.print_status("error is too high")
                        print('Measurements have too much error')
                else:
                    self.status.print_status("Pleas store measurement 3 times")
                    print('Pleas store measurement 3 times')                    
            else:
                self.status.print_status("Press restore first")
                print('Press restore first')
        else:
            self.status.print_status("It is not running")
            print('It is not running')