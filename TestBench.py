import random
import scipy
import numpy as np
import math
import matplotlib.pyplot as plt

g = 9.81# erbeschleunigung
D = 0.1# meter reaktor durchmesser innen

regimeFloodedToLoading = {#(Fl,Fr)
    "x1": 0.025,
    "y1": 0.04,
    "x2": 0.31,
    "y2": 0.5,
}
LoadDispX = {#(Fl,Fr)
    "x1": 0.002,
    "y1": 0.2,
    "x2": 0.053,
    "y2": 1,
}

floLoaX = [0.025,     0.1,    0.31    ] #Fl
floLoaY = [0.04,      0.16,   0.5     ] #Fr

loadDispX = [0.002,     0.01,   0.053   ] #Fl
loadDispY = [0.2,       0.4,    1       ] #Fr
mdisp=-0.41088854648177
ndisp=1.0217770929635
mfloo=1.6140350877193
nfloo=-0.00350877

# trenngerade in flowregime card
def getFrOfDispToTransFromFl(Fl, margin=0):
    xp = [math.log10(0.002), math.log10(0.1)]
    yp = [math.log10(0.2), math.log10(0.4)]
    if type(Fl) == float:
        return math.pow(10, np.interp(Fl, xp, yp))
    else:
        return [math.pow(10, np.interp(fl_value, xp, yp)) for fl_value in Fl]
    #fr=np.power(10,mdisp*(np.log10(Fl)-margin)+ndisp)
    #return fr #returns Fr

maximum = {
    "vs": 150,
    "rpm": 1000,
    "Fr": 2,#np.power(1000 * 60, 2) * D / g,
    "Fl": 1 #150 / (1000 * np.power(D, 3) * 60000)
}

minimum = {
    "vs": 10,
    "rpm": 100,
    "Fr": 0.04, #np.power(100*60, 2)*D/g,
    "Fl": 0.002#10/(100*np.power(D, 3)*60000)
}
maximumDisp = {
    "gas": 150,
    "rpm": 1000,
    "FrChart": 2,#np.power(1000 * 60, 2) * D / g,
    "FlChart": 0.2 ,#150 / (1000 * np.power(D, 3) * 60000)
    "FrConst": float(np.power(1000/60, 2) * D / g),
    "FlConst": float(150 / ((1000/60 * np.power(D, 3) * 60000)))
}

minimumDisp = {
    "vs": 10,
    "rpm": 100,
    "Fr": 0.2, #np.power(100*60, 2)*D/g,
    "Fl": 0.002,#10/(100*np.power(D, 3)*60000)
    "FrConst": float(np.power(100 / 60, 2) * D / g),
    "FlConst": float(10 / ((100 / 60 * np.power(D, 3) * 60000)))
}

def getRpm(Fr):
    return np.sqrt(Fr*g/D)*60 #rpm

def getGasflow(Fl,Fr):
    return Fl * np.sqrt(Fr*g/D)*D*D*D*60000 #Gasflow

def getRandomExperimentInDispersedState():
    randomFl = random.uniform(minimumDisp.get("FlConst"),maximumDisp.get("FlConst"))
    randomFr = random.uniform(getFrOfDispToTransFromFl(randomFl), maximumDisp.get("FrChart"))
    rpm=getRpm(randomFr)
    vs=getGasflow(randomFl, randomFr)
    return(rpm, vs)

def getRandomExperimentInFloodedState():
    randomFl = random.uniform(minimumDisp.get("FlConst"), maximumDisp.get("FlConst"))
    randomFr = random.uniform(getFrOfDispToTransFromFl(randomFl), maximumDisp.get("FrChart"))
    rpm = getRpm(randomFr)
    vs = getGasflow(randomFl, randomFr)
    return (rpm, vs)

def getRandomExperimentInLoadedState():
    randomFl = random.uniform(minimumDisp.get("FlConst"), maximumDisp.get("FlConst"))
    randomFr = random.uniform(getFrOfDispToTransFromFl(randomFl), maximumDisp.get("FrChart"))
    rpm = getRpm(randomFr)
    vs = getGasflow(randomFl, randomFr)
    return (rpm, vs)



experiments = [
    {'gas_flow': getRandomExperimentInDispersedState()[0], 'rpm': getRandomExperimentInDispersedState()[1]}, #loaded
  ]

#funktion zur abbildung von rpm und gasflow nach flow regime siehe Corina Kröger gleichung
# parameter dynamisch mit random faktor ändern aber so dass das flowregime stabil bleibt. Erste und letzte bilder entfernnen.
# extra perioden für übergangsregime einführen

exp_no = 0
picturesPersecond = 4
picturesTaken = 0
amountOfPicutures = 100
X= []
Y= []
while amountOfPicutures >= picturesTaken:
    X.append(getRandomExperimentInDispersedState()[0])
    Y.append(getRandomExperimentInDispersedState()[1])
    print("Experiment Dispersed: RPM: "+str(getRandomExperimentInDispersedState()[0])+" VS: "+str(getRandomExperimentInDispersedState()[1]))
    #print("Experiment Loaded: X: "+str(getRandomExperimentInLoadedState()[0])+" Y: "+str(getRandomExperimentInLoadedState()[1]))
    #print("Experiment Flooded: X: "+str(getRandomExperimentInFloodedState()[0])+" Y: "+str(getRandomExperimentInFloodedState()[1]))
    picturesTaken+=1

xRpmMin=np.linspace(minimum.get("rpm"),minimum.get("rpm"),maximum.get("vs"))                              #150 dots on lin line up to max
yRpmMin=np.linspace(minimum.get("vs"),maximum.get("vs"),maximum.get("vs")) #150 dots on min line
xRmpMax=np.linspace(maximum.get("rpm"),maximum.get("rpm"),maximum.get("vs"))                              #150 dots on lin line up to max
yRpmMax=np.linspace(minimum.get("vs"),maximum.get("vs"),maximum.get("vs")) #150 dots on min line
xVsMin=np.linspace(minimum.get("rpm"),maximum.get("rpm"),maximum.get("rpm"))#150 dots on lin line up to max
yVsMin=np.linspace(minimum.get("vs"),minimum.get("vs"),maximum.get("rpm"))#150 dots on lin line up to max
xVsMax=np.linspace(minimum.get("rpm"),maximum.get("rpm"),maximum.get("rpm"))#150 dots on lin line up to max
yVsMax=np.linspace(maximum.get("vs"),maximum.get("vs"),maximum.get("rpm"))#150 dots on lin line up to max

FrDisp=np.linspace(minimumDisp.get("FrConst"),maximumDisp.get("FrConst"))
xRpmDisp=getRpm(FrDisp)
yvsDisp=getGasflow(getFrOfDispToTransFromFl(FrDisp), FrDisp)

#rpmDispToTrans
#vsDispToTrans
#rpmTransToLoad
#vsTransToLoad
#rpmLoadToFlood
#vsLoadToFlood



plt.plot(getFrOfDispToTransFromFl(FrDisp), FrDisp,color='b')
plt.xscale('log')
plt.yscale('log')
plt.xlim([0,1])
plt.ylim([0,2])
plt.show()


exit(0)

plt.scatter(X,Y,1)
plt.plot(xRpmMin,yRpmMin,color='r')
plt.plot(xRmpMax,yRpmMax,color='r')
plt.plot(xVsMin,yVsMin,color='r')
plt.plot(xVsMax,yVsMax,color='r')
plt.plot(xRpmDisp,yvsDisp,color='g')
#plt.plot(rpmDispToTrans,vsDispToTrans,color='g')
#plt.plot(rpmTransToLoad,vsTransToLoad,color='g')
#plt.plot(rpmLoadToFlood,vsLoadToFlood,color='g')

plt.xlim([0,1100])
plt.ylim([0,160])
plt.show()