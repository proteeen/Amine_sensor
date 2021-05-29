#include <windows.h>
#include "sa_api.h"
#include "tg_api.h"
#include <iostream>
#include <string>
#include <fstream>
using namespace std;
int main()
{
    int handle = -1;
    saStatus openStatus = saOpenDevice(&handle);
    if(openStatus != saNoError) {
        // Handle unable to open/find device error here
        std::cout << saGetErrorString(openStatus) << std::endl;
    }

    if(saAttachTg(handle) != saNoError) {
        // Unable to find tracking generator
    }

    saConfigCenterSpan(handle, 2.8e9, 0.8e9);
    saConfigAcquisition(handle, SA_MIN_MAX, SA_LOG_SCALE);
    saConfigLevel(handle, -10.0);
    saConfigSweepCoupling(handle, 1.0e3, 1.0e3, true);

    // Additional configuration routine
    // Configure a 100 point sweep
    // The size of the sweep is a suggestion to the API, it will attempt to
    // get near the requested size.
    // Optimized for high dynamic range and passive devices
    saConfigTgSweep(handle, 801, true, true);

    // Initialize the device with the configuration just set
    saInitiate(handle, SA_TG_SWEEP, 0);
    // Get sweep characteristics
    int sweepLen;
    double startFreq, binSize;
    saQuerySweepInfo(handle, &sweepLen, &startFreq, &binSize);
    cout << "sweeplen = " << sweepLen << endl;
    cout << "start frequency = " << startFreq << endl;
    cout << "binsize = " << binSize << endl;

    Sleep(10000);
    cout << "saAbort" << endl;
    saAbort(handle);
    Sleep(5000);
    cout << "saInitiate" << endl;
    saInitiate(handle, SA_TG_SWEEP, 0);
    Sleep(10000);

    cout << "saCloseDevice" << endl;
    saAbort(handle);
    saCloseDevice(handle);
    return 0;
}