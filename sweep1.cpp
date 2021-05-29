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

    // Sweep some device at 900MHz center with 1MHz span
    saConfigCenterSpan(handle, 2.8e9, 0.8e9);
    saConfigAcquisition(handle, SA_MIN_MAX, SA_LOG_SCALE);
    saConfigLevel(handle, -10.0);
    saConfigSweepCoupling(handle, 1.0e3, 1.0e3, true);

    // Additional configuration routine
    // Configure a 100 point sweep
    // The size of the sweep is a suggestion to the API, it will attempt to
    // get near the requested size.
    // Optimized for high dynamic range and passive devices
    saConfigTgSweep(handle, 100, true, true);

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

        // Allocate memory for the sweep
        float *max = new float[sweepLen];
        float *min = new float[sweepLen];
        // sweep 10 time
        for(int j=0; j<10; j++ ){
            std::cout << "j = " << j << std::endl;
            saGetSweep_32f(handle, min, max);
            std::cout << "i = 60 " << min[60] << std::endl;
            for(int i=0; i<sweepLen; i++){
                std::cout << i+1 << " " << min[i] << std::endl;
            }
            Sleep(1000);
        }
        delete [] max;
        delete [] min;
    }

    saAbort(handle);
    saCloseDevice(handle);
}

int main(){
      trackingGeneratorSweep();

}
