from ctypes import*
import numpy as np
salib = CDLL("sa_api.dll")
tglib = CDLL("tg_api.dll")
apiversion = c_char_p(salib.saGetAPIVersion())
productid = c_char_p(salib.saGetProductID())

handle = c_int(-1)
PT_handle = pointer(handle)
serialNumber = c_int(0)
PT_serialNumber = pointer(serialNumber)

if(salib.saOpenDevice(PT_handle) == 0):
    print("open device = no error")
else:
    # Handle unable to open/find device error here
    print("open device = error")

if(salib.saAttachTg(handle) == 0):
    print("track gen = no error")
else:
    # Unable to find tracking generator
    print("track gen = error")

salib.saGetSerialNumber(handle, PT_serialNumber)
print("serial number = "+str(serialNumber.value))

#Configure start and spand frequency
salib.saConfigCenterSpan(handle, c_double(2.8e9), c_double(0.8e9))
#c_int(0)=SA_MIN_MAX,c_int(0)=SA_LOG_SCALE
salib.saConfigAcquisition(handle, c_int(0), c_int(0))
salib.saConfigLevel(handle, c_double(-10.0))
salib.saConfigSweepCoupling(handle, c_double(1.0e3), c_double(1.0e3), c_bool(True))
#Configure a 100 point sweep
salib.saConfigTgSweep(handle, c_int(100), c_bool(True), c_bool(True))

#Initialize the device with the configuration just set c_int(4)=SA_TG_SWEEP
salib.saInitiate(handle, c_int(4), c_int(0))
#Get sweep characteristics
sweepLen = c_int(0)
startFreq = c_double(0)
binSize = c_double(0)
salib.saQuerySweepInfo(handle, pointer(sweepLen), pointer(startFreq), pointer(binSize))
print("sweeplen = " + str(sweepLen.value))
print("start frequency = " + str(startFreq.value))
print("binsize = " + str(binSize.value))
#Allocate memory for the sweep
miin = c_float * sweepLen.value
a1 = miin()
maax = c_float * sweepLen.value
a2 = maax()
#sweep and store to a1 float C array
salib.saGetSweep_32f(handle, pointer(a1), pointer(a2))
#change to numpy array
aa = np.array(a1)

salib.saAbort(handle)
salib.saCloseDevice(handle)