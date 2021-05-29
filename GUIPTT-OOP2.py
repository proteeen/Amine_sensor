import tkinter as tk
import numpy as np
from ctypes import*
from running import Setup, Vna_option
from storesave import Storedata, Comment, Comparison
salib = CDLL(".//bin//sa_api.dll")
tglib = CDLL(".//bin//tg_api.dll")

class Title:
    def __init__(self,root):
        root.title("PTT Instrument Project")
        root.columnconfigure(0,weight=1)
        root.rowconfigure(0,weight=0)
        mainframe = tk.Frame(root,bg='black')
        titleLabel = tk.Label(root,text="PTT Instrument Project",font=('Helvetica',10),bg="deep sky blue",width=40)
        titleLabel.grid(row=0,column=0,columnspan=8,padx=0,pady=0,sticky='nsew')

 #   def showserialnum(self, handle):
 #       serialNumber = c_int(0)
 #       salib.saGetSerialNumber(handle, pointer(serialNumber))
 #       print("serial number = "+str(serialNumber.value))
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
            root  = tk.Tk()
            title =Title(root)
            setup = Setup(root,handle)
            storedata = Storedata(root)
            comment = Comment(root)
            vna = Vna_option(root,handle)
            comparison = Comparison(root)
            root.mainloop()
        else:
            # Unable to find tracking generator
            print("track gen = error")
    else:
        # Handle unable to open/find device error here
        print("open device = error")

    salib.saAbort(handle)
    salib.saCloseDevice(handle)

#    root = Tk()
#    a = aaa(root)
    
if __name__=='__main__':
    main()
    

            