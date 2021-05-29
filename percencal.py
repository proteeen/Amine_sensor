import numpy as np
import pandas as pd
import os



def evaluateamine(amplitude, leanNum):
#   return variable
    isemtydatabase = None
    minMAPE = None
    Outamine = None

    usdir = os.getcwd()
    usdircsv = usdir + "\\csv"
    dicdatamain = {'percen_real' : [], 'percen_round' : [], 'date' : [], 'comment' : [], 'timestamp' :[]}
    dicAmplitude = {'freGHz' : np.linspace(2.4,3.2,num=801,dtype=np.float32)}
    index = 0

    for root, dirs, files in os. walk(usdircsv):
        if root == usdircsv+'\\'+"LEAN#"+str(leanNum):
            for i in files:
                dftmpAmplitude = pd.read_csv(root +'\\'+ i)
                splittmp = i.split('#')
                dicdatamain['percen_real'].append(float(splittmp[1])) # add %amine from file name to dicdatamain
                dicdatamain['percen_round'].append(int(round(float(splittmp[1]))))
                dicdatamain['date'].append(splittmp[0]) # add correct date from file name to dicdatamain
                dicdatamain['comment'].append(splittmp[2]) # add comment from file name to dicdatamain
                dicdatamain['timestamp'].append(splittmp[3]) # add timestamp from file name to dicdatamain
                dicAmplitude[str(index)] = dftmpAmplitude['amplitude']
                index = index + 1
    dfmain = pd.DataFrame.from_dict(dicdatamain)
    dfAmplitude = pd.DataFrame.from_dict(dicAmplitude)
    if (dfmain.shape[0] > 0):
#       AmplitudeNrow = dfAmplitude.shape[0]
        AmplitudeNcol = dfAmplitude.shape[1]
        AmplitudeNpArray = (dfAmplitude.iloc[:,1:AmplitudeNcol]).to_numpy() #[f1[a('0'),a('1'),a('3'),..],f2[a('0'),a('1'),a('3'),..],f3...] create Numpy array
        aaUse = AmplitudeNpArray.transpose() #['0'[a(f1),a(f2),a(f3),...a(fn)],'2'[a(f1),a(f2),a(f3),...a(fn)],'3'...] (transpose)
        abserror = abs((aaUse - amplitude)/amplitude)
        MAPEarray = abserror.mean(axis=1)*100
        minMAPE = MAPEarray.min()
        minMAPEindex = np.where(MAPEarray == minMAPE)[0][0] #retrun array in tuple select first
        Outamine = dfmain['percen_round'][minMAPEindex]
#        print(Outamine)
        isemtydatabase = False
    else:
        isemtydatabase = True

    return isemtydatabase, minMAPE, Outamine