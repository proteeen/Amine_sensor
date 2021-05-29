from ctypes import*
import time
import datetime
import numpy as np

salib = CDLL(".//bin//sa_api.dll")
tglib = CDLL(".//bin//tg_api.dll")
# Nsweep = 100 ,801
Nsweep = 801
sweepLen = None

def readSweep(handle):
    miin = c_float * sweepLen.value
    a1 = miin()
    maax = c_float * sweepLen.value
    a2 = maax()
    #sweep and store to a1 float C array
    salib.saGetSweep_32f(handle, pointer(a1), pointer(a2))
    #change to numpy array
    aa = np.array(a1)
    return aa

def printarray(handle):
    aa = readSweep(handle)
    print(aa)

def abserrorsum(handle):
    aa = readSweep(handle)
    return np.sum(np.abs(aa))

def ConfigFre(handle):    
    #Configure start and spand frequency
    salib.saConfigCenterSpan(handle, c_double(2.8e9), c_double(0.8e9))
    #c_int(0)=SA_MIN_MAX,c_int(0)=SA_LOG_SCALE
    salib.saConfigAcquisition(handle, c_int(0), c_int(0))
    salib.saConfigLevel(handle, c_double(-10.0))
    salib.saConfigSweepCoupling(handle, c_double(1.0e3), c_double(1.0e3), c_bool(True))
    #Configure a 100 point sweep
    salib.saConfigTgSweep(handle, c_int(Nsweep), c_bool(True), c_bool(True))

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
#print array    printarray(handle)
