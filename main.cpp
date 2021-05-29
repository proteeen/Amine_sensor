#include <iostream>
#include <windows.h>
#include "sa_api.h"
#include "tg_api.h"
using namespace std;

void openDevice()
{

    std::cout << "API Version: " << saGetAPIVersion() << std::endl;

    int handle = -1;
    saStatus openStatus = saOpenDevice(&handle);
    if(openStatus != saNoError) {
        std::cout << saGetErrorString(openStatus) << std::endl;
        return;
    }

    std::cout << "Device Found!\n";

    saDeviceType deviceType;
    saGetDeviceType(handle, &deviceType);

    std::cout << "Device Type: ";
    if(deviceType == saDeviceTypeSA44) {
        std::cout << "SA44\n";
    } else if(deviceType == saDeviceTypeSA44B) {
        std::cout << "SA44B\n";
    } else if(deviceType == saDeviceTypeSA124A) {
        std::cout << "SA124A\n";
    } else if(deviceType == saDeviceTypeSA124B) {
        std::cout << "SA124B\n";
    }

    int serialNumber = 0;
    saGetSerialNumber(handle, &serialNumber);
    std::cout << "Serial Number: " << serialNumber << std::endl;

    float temperature = 0.0;
    saQueryTemperature(handle, &temperature);
    std::cout << "Internal Temp: " << temperature << " C" << std::endl;

    float voltage = 0.0;
    saQueryDiagnostics(handle, &voltage);
    std::cout << "Voltage: " << voltage << " V" << std::endl;

    int sweepLen;
    double startFreq, binSize;
    saQuerySweepInfo(handle, &sweepLen, &startFreq, &binSize);

    std::cout << "sweeplen : " << sweepLen << " startfre : " << startFreq<< " binsize : "<< binSize <<std::endl;

    saCloseDevice(handle);
}

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
        for(int j=0; j<10; j++ ){
            std::cout << "j = " << j << std::endl;
            saGetSweep_32f(handle, min, max);
            std::cout << "i = 60 " << min[60] << std::endl;
//            for(int i=0; i<sweepLen; i++){
//                std::cout << i+1 << " " << min[i] << std::endl;
//            }
            Sleep(1000);
        }
        delete [] max;
        delete [] min;
    }

    saAbort(handle);
    saCloseDevice(handle);
}

int main(){
//    for( int a = 1; a < 5; a = a + 1 ) {
//      cout << "value of a: " << a << endl;
      trackingGeneratorSweep();
//   }

}
