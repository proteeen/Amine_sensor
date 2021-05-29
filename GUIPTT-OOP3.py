import tkinter as tk 
import numpy as np
import running2
import storesave2

from ctypes import*
salib = CDLL(".//bin//sa_api.dll")
tglib = CDLL(".//bin//tg_api.dll")

class Title:
    def __init__(self,master):
        self.master = master
        self.master.columnconfigure(0,weight=1)
        self.master.rowconfigure(0,weight=0)
        self.frame = tk.Frame(self.master,bg='black')
        self.label = tk.Label(self.master,text="PTT Instrument Project ESP plant",font=('Helvetica',10),bg="deep sky blue",width=40)
        self.label.grid(row=0,column=0,columnspan=8,padx=0,pady=0,sticky='nsew')

class Show_status:
    def __init__(self,master):
        self.isrunning = False
        self.isstorenewsave = True
        self.isstorenewevar = True
        self.master = master
        self.frame = tk.Frame(self.master)
        self.label = tk.Label(self.frame,text='Status : ',font=('Helvetica',10)).grid(row=6,column=0,sticky='nesw')
        self.label2 = tk.Label(self.frame,text=" ")
        self.label2.grid(row=6,column=1)
        self.frame.grid(row=6,column=0)

    def print_status(self,xstring):
        self.label2.config(text=xstring)

    def runningstatus(self,runningbool):
        self.isrunning = runningbool

    def storenewsavestatus(self,storebool):
        self.isstorenewsave = storebool
        
    def storenewevarstatus(self,storebool):
         self.isstorenewevar = storebool
    

def main():
    
    handle = c_int(-1)
    PT_handle = pointer(handle)
    serialNumber = c_int(0)
    if(salib.saOpenDevice(PT_handle) == 0):
        print("open device = no error")
        if(salib.saAttachTg(handle) == 0):
            print("track gen = no error")
            salib.saGetSerialNumber(handle, pointer(serialNumber))
            print("serial number = "+str(serialNumber.value))
            root=tk.Tk()
            root.title("PTT Instrument Project")
            title = Title(root)
            status = Show_status(root)
            comment = storesave2.Comment(root,handle,status)
            storedata = storesave2.Storedata(root,handle,status)
            vna = running2.Vna_option(root,handle,status)
            evaluate = storesave2.evaluate(root,handle,status)

            
            root.mainloop()
        else:
            # Unable to find tracking generator
            print("track gen = error")
    else:
        # Handle unable to open/find device error here
        print("open device = error")

    salib.saAbort(handle)
    salib.saCloseDevice(handle)
if __name__=='__main__':
    main()
    

            
