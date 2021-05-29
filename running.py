import tkinter as tk
from ctypes import*
import time
import numpy as np

salib = CDLL(".//bin//sa_api.dll")
tglib = CDLL(".//bin//tg_api.dll")
sweepLen = None
runstate = False

class Setup:
    
    def __init__(self,root,handle):
        self.handle = handle
        self.start_value = None
        self.stop_value = None
        self.start_freq = tk.DoubleVar()
        self.start_freq.set(2.4)
        self.stop_freq = tk.DoubleVar()
        self.stop_freq.set(3.2)
        mainframe = tk.Frame(root)
        StartLabel = tk.Label(mainframe,text="Start Frequency(GHz)")
        StopLabel = tk.Label(mainframe,text="Stop Frequency(GHz)")
        startFreEntry = tk.Entry(mainframe,textvariable=self.start_freq,font=('Helvetica',10),width=20)
        soptFreEntry = tk.Entry(mainframe,textvariable=self.stop_freq,font=('Helvetica',10),width=20)
        SetButclick = tk.Button(mainframe,text='set',command=self.Set_click,bd=3)
    #Grid set up
        mainframe.grid(row =1,column=0)
        StartLabel.grid(row=1,column=0)
        StopLabel.grid(row=2,column=0)
        startFreEntry.grid(row=1,column=1)
        soptFreEntry.grid(row=2,column=1)
        SetButclick.grid(row=2,column=2)

    def Set_click(self):
        global runstate
        if runstate == False:
            self.start_value= self.start_freq.get()*10e9
            self.stop_value=self.stop_freq.get()*10e9
            self.ConfigFre(self.handle)
            print(self.start_value)
            print(self.stop_value)
            runstate = True
        else:
            pass

    def ConfigFre(self, handle):
        #Configure start and spand frequency
        salib.saConfigCenterSpan(handle, c_double(2.8e9), c_double(0.8e9))
        #c_int(0)=SA_MIN_MAX,c_int(0)=SA_LOG_SCALE
        salib.saConfigAcquisition(handle, c_int(0), c_int(0))
        salib.saConfigLevel(handle, c_double(-10.0))
        salib.saConfigSweepCoupling(handle, c_double(1.0e3), c_double(1.0e3), c_bool(True))
        #Configure a 401 point sweep
        salib.saConfigTgSweep(handle, c_int(401), c_bool(True), c_bool(True))

        #Initialize the device with the configuration just set c_int(4)=SA_TG_SWEEP
        salib.saInitiate(handle, c_int(4), c_int(0))
        #Get sweep characteristics
        global sweepLen
        sweepLen = c_int(0)
        startFreq = c_double(0)
        binSize = c_double(0)
        salib.saQuerySweepInfo(handle, pointer(sweepLen), pointer(startFreq), pointer(binSize))
        print("sweeplen = " + str(sweepLen.value))
        print("start frequency = " + str(startFreq.value))
        print("binsize = " + str(binSize.value))
#====================================================================        
        miin = c_float * sweepLen.value
        a1 = miin()
        maax = c_float * sweepLen.value
        a2 = maax()
        #sweep and store to a1 float C array
        salib.saGetSweep_32f(handle, pointer(a1), pointer(a2))
        #change to numpy array
        aa = np.array(a1)
        print(aa)
#==================================================================== 
class Vna_option:
    
    def __init__(self,master,handle):
        self.handle = handle
        self.master = master
        self.frame = tk.Frame(self.master).grid(row=5,column=0)
        self.label = tk.Label(self.frame,text='Option',font=('Helvetica',10)).grid(row=5,column=0,sticky='nesw')
        self.startbut = tk.Button(self.frame,text='start',command=self.start,bg='deep sky blue',bd=2,font=('Helvetica',10)).grid(row=5,column=1,stick='nesw')
        self.stopbut = tk.Button(self.frame,text='stop',command=self.stop,bg='deep sky blue',bd=2,font=('Helvetica',10),width=10).grid(row=5,column=2,stick='nesw')
        self.calbut = tk.Button(self.frame,text='Start Calibration',command=self.calibration,bd=2,bg='deep sky blue').grid(row=5,column=3,stick='nesw')

    def start(self):
        global runstate
        if runstate == False:
            salib.saInitiate(self.handle, c_int(4), c_int(0))
#====================================================================
            global sweepLen
            miin = c_float * sweepLen.value
            a1 = miin()
            maax = c_float * sweepLen.value
            a2 = maax()
            #sweep and store to a1 float C array
            salib.saGetSweep_32f(self.handle, pointer(a1), pointer(a2))
            #change to numpy array
            aa = np.array(a1)
            print(aa)
#====================================================================             
            runstate = True
        else:
            print("Now is runnig")
            
        
    def stop(self):
        global runstate
        if runstate == True:
            salib.saAbort(self.handle)
            runstate = False
        else:
            print("Now is stopping")
            
    def calibration(self):
        salib.saStoreTgThru(self.handle, c_int(1))
#====================================================================
        global sweepLen
        miin = c_float * sweepLen.value
        a1 = miin()
        maax = c_float * sweepLen.value
        a2 = maax()
        #sweep and store to a1 float C array
        salib.saGetSweep_32f(self.handle, pointer(a1), pointer(a2))
        #change to numpy array
        aa = np.array(a1)
        print(aa)
        
    
