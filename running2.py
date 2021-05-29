import tkinter as tk
from ctypes import*
import time
import numpy as np
import getsweep

salib = CDLL(".//bin//sa_api.dll")
tglib = CDLL(".//bin//tg_api.dll")
isset = False
running = False
calerror = 12

# class Setup:
#     def __init__(self,master,handle):
#         self.handle = handle
#         self.master = master
#         self.frame = tk.Frame(self.master).grid(row=1,column=0)
#         self.button2 = tk.Button(self.frame,text='set',command=self.Set_click,bd=3)
    
#     #Grid set up
#         self.button2.grid(row=2,column=2)



class Vna_option:
    def __init__(self,master,handle,status):
        self.handle = handle
        self.master = master
        self.status = status
        self.isset = False
        self.running = False
        self.frame = tk.Frame(self.master)
        self.setbutt = tk.Button(self.frame,text='set',command=self.Set_click,bg='deep sky blue',bd=2,font=('Helvetica',10))
        self.button1 = tk.Button(self.frame,text='run', bg='deep sky blue', bd=2,font=('Helvetica',10),state='disabled')
        self.button2 = tk.Button(self.frame,text='stop', bg='deep sky blue', bd=2,font=('Helvetica',10),state='disabled')
        self.button3 = tk.Button(self.frame,text='calibrate', bg='deep sky blue', bd=2,font=('Helvetica',10),state='disable')

        self.frame.grid(row=5,column=0)
        self.setbutt.grid(row=5,column=0)
        self.button1.grid(row=5,column=1)
        self.button2.grid(row=5,column=2)
        self.button3.grid(row=5,column=3)


    def Set_click(self):
        self.button2 = tk.Button(self.frame,text='set',command=self.Set_click,bd=3)
        if self.isset == False:
            getsweep.ConfigFre(self.handle)
            self.isset = True
            self.running = True
            self.status.runningstatus(True)
            self.status.print_status('Now is running please calibrate')
            tk.Button(self.frame,text='set',bg='deep sky blue',bd=2,font=('Helvetica',10), state='disabled').grid(row=5,column=0)
            tk.Button(self.frame,text='run', bg='green', bd=2,font=('Helvetica',10),state='disabled').grid(row=5,column=1)
            tk.Button(self.frame,text='stop',command=self.stop,bg='deep sky blue',bd=2,font=('Helvetica',10)).grid(row=5,column=2)
            tk.Button(self.frame,text='calibrate',command=self.calibration,bg='yellow',bd=2,font=('Helvetica',10)).grid(row=5,column=3)
        else:
            print('not first')

    def start(self):
        if self.isset == True:
            if self.running == False:
                salib.saInitiate(self.handle, c_int(4), c_int(0))
                self.running = True
                self.status.runningstatus(True)
#print array                getsweep.printarray(self.handle)
#print error                print(getsweep.abserrorsum(self.handle))
                self.status.print_status('Now is running please calibrate')
                tk.Button(self.frame,text='run',bg='green',bd=2,font=('Helvetica',10), state='disabled').grid(row=5,column=1)
                tk.Button(self.frame,text='stop',command=self.stop,bg='deep sky blue',bd=2,font=('Helvetica',10)).grid(row=5,column=2)
                tk.Button(self.frame,text='calibrate',command=self.calibration,bg='yellow',bd=2,font=('Helvetica',10)).grid(row=5,column=3)
            else:
                print('It is running')
        else:
            print('not set frequency')

    def stop(self):
        if self.isset == True:
            if self.running == True:
                salib.saAbort(self.handle)
                self.running = False
                self.status.runningstatus(False)
                self.status.print_status('Now is stopping')
                tk.Button(self.frame,text='run' ,command=self.start, bg='deep sky blue',bd=2,font=('Helvetica',10)).grid(row=5,column=1)
                tk.Button(self.frame,text='stop',bg='red',bd=2,font=('Helvetica',10), state='disabled').grid(row=5,column=2)
                tk.Button(self.frame,text='calibrate',command=self.calibration,bg='deep sky blue',bd=2,font=('Helvetica',10)).grid(row=5,column=3)
                tk.Button(self.frame,text='calibrate',bg='yellow',bd=2,font=('Helvetica',10), state='disabled').grid(row=5,column=3)
            else:
                print('It is stopping')
        else:
            print('not set frequency')
    
    def calibration(self):
        if self.isset == True:
            if self.running == True:
                time.sleep(1)			
                salib.saStoreTgThru(self.handle, c_int(1))
                time.sleep(1.5)
 #print array               getsweep.printarray(self.handle)
                sumerror = getsweep.abserrorsum(self.handle)
                print(sumerror)
                if sumerror < calerror:
                    self.status.print_status("calibration finished. You can measure now, Do not press stop until finished.")
                    tk.Button(self.frame,text='calibrate',bg='green',bd=2,font=('Helvetica',10), state='disabled').grid(row=5,column=3)
                else:
                    self.status.print_status("please calibrate again")
            else:
                print('It is not running')
        else:
            print('not set frequency')