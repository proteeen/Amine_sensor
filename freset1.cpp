#include <iostream>
#include <windows.h>
#include "sa_api.h"
#include "tg_api.h"
using namespace std;

void trackingGeneratorSweep()
{
    int handle = -1;
    saStatus openStatus = saOpenDevice(&handle);
    if(openStatus != saNoError) {
        // Handle unable to open/find device error here
        std::cout << saGetErrorString(openStatus) << std::endl;
        return;
    }

    if(saAttachTg(handle) != saNoError) {
        // Unable to find tracking generator
        return;
    }
    // set frequency (handle, center[Hz], spand[Hz])
    saConfigCenterSpan(handle, 2.8e9, 0.8e9); 
    saConfigAcquisition(handle, SA_MIN_MAX, SA_LOG_SCALE);
    saConfigLevel(handle, -10.0);
    saConfigSweepCoupling(handle, 1.0e3, 1.0e3, true); 
     //set gen sweep (handle, sweep point [N],true,true) more sweep points --> more binsize
    saConfigTgSweep(handle, 1001, true, true);

    // Initialize the device with the configuration just set
    if(saInitiate(handle, SA_TG_SWEEP, 0) != saNoError) {
        // Handle unable to initialize
        std::cout << "error" << std::endl;
        return;
    }
    else{
        std::cout << "no error" << std::endl;
        // Get sweep characteristics
        int sweepLen;
        double startFreq, binSize;
        saQuerySweepInfo(handle, &sweepLen, &startFreq, &binSize);
        std::cout << "sweeplen = " << sweepLen << std::endl;
        std::cout << "start frequency = " << startFreq << std::endl;
        std::cout << "binsize = " << binSize << std::endl;
    }

    saAbort(handle);
    saCloseDevice(handle);
}

int main(){
      trackingGeneratorSweep();

}
