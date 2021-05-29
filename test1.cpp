#include <windows.h>
#include "sa_api.h"
#include "tg_api.h"
#include <iostream>
#include <string>
#include <fstream>
using namespace std;

void writecsv()
{
    ofstream myFile;
    myFile.open("testcsv.csv");
    for (int i=1; i<=5; i++)
    {
        myFile << i << "," << 2*i << endl;
    }
}

int main()
{
    //writecsv();
    //==================  initial spectru, ======================
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
    saConfigTgSweep(handle, 100, true, true);

    // Initialize the device with the configuration just set
    saInitiate(handle, SA_TG_SWEEP, 0);
    // Get sweep characteristics
    int sweepLen;
    double startFreq, binSize;
    saQuerySweepInfo(handle, &sweepLen, &startFreq, &binSize);
    cout << "sweeplen = " << sweepLen << endl;
    cout << "start frequency = " << startFreq << endl;
    cout << "binsize = " << binSize << endl;
    // Allocate memory for the sweep
    float *min = new float[sweepLen];
    float *max = new float[sweepLen];
    saGetSweep_32f(handle, min, max); //sweep
    //==================  initial spectru, ======================
    for(int i=0; i<sweepLen; i++){
        cout << i+1 << " " << min[i] << endl;
    }
    //write min max array out
    
    char checkcal;
    cout << "connect through to cal type (1) after connect ";
    cin >> checkcal;
    if (checkcal == '1'){
        cout << "store through" << endl;
        
        // Store baseline
        saStoreTgThru(handle, TG_THRU_0DB);
        Sleep(3000);
        // check and compare to 8
        saGetSweep_32f(handle, min, max); //sweep
        for(int i=0; i<sweepLen; i++){
            cout << i+1 << " " << min[i] << endl;
        }
        char select = 'N';
        string namefile;
        float aminepercen;
        while(select != '0'){
           // cout << "csv file name to save : ";
           // cin >> namefile;
           // cout << "% amine = ";
           // cin >> aminepercen;
            cout << "type (0) = quit, type (1) = continue ";
            cin >> select;
            if (select == '1'){
                cout << "continue" << endl;
                // 1. saGetSweep_32f(handle, min, max); sweep 10 times --> average to 1
                saGetSweep_32f(handle, min, max); //sweep
                for(int i=0; i<sweepLen; i++){
                    cout << min[i];
                }
                // 2. write to csv file 
                //cout << "write to " << namefile << endl;
            }
            else if (select == '0'){
                
                break;   
            }
            else{
                cout << "wrong key" << endl;
            }
        }
    }
    else{
        cout << "wrong key" << endl;
    }
    delete [] max;
    delete [] min;
    saAbort(handle);
    saCloseDevice(handle);
    cout << "quit" << endl;
    return 0;
}