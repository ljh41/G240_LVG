import numpy as np
import math
import string
import os
import sys
import matplotlib.pyplot as plt

#not finished

#name
position = sys.argv[1]
print 'name',position

path = './fig/SED/'
errflag = 'errrms'

#data
dv = 2. #km/s
fsed = np.loadtxt('./data/LVGsolution/SED_'+position+'_'+errflag+'.txt')
velarr = fsed[:,0]
obs21arr = fsed[:,1] * dv
obs32arr = fsed[:,2] * dv
obs65arr = fsed[:,3] * dv
obs76arr = fsed[:,4] * dv
T10arr = fsed[:,5] * dv
T21arr = fsed[:,6] * dv
T32arr = fsed[:,7] * dv
T43arr = fsed[:,8] * dv
T54arr = fsed[:,9] * dv
T65arr = fsed[:,10] * dv
T76arr = fsed[:,11] * dv
T87arr = fsed[:,12] * dv
T98arr = fsed[:,13] * dv
chi = fsed[:,14]

nvel = velarr.shape[0]

#noise
err21 = obs21arr*0.1
err32 = obs32arr*0.15
err65 = obs65arr*0.2
err76 = obs76arr*0.3

rms21 = 0.004
rms32 = 0.04
rms65 = 0.04
rms76 = 0.1

obserr21 = (err21**2+rms21**2)**0.5
obserr32 = (err32**2+rms32**2)**0.5
obserr65 = (err65**2+rms65**2)**0.5
obserr76 = (err76**2+rms76**2)**0.5

for i in range(nvel):
    vel = velarr[i]
    plt.figure(i)
    print vel,obs21arr[i],obs32arr[i],obs65arr[i],obs76arr[i]
    plt.plot([2,3,6,7],[obs21arr[i],obs32arr[i],obs65arr[i],obs76arr[i]],'ks',label = 'observations')
    plt.errorbar([2,3,6,7],[obs21arr[i],obs32arr[i],obs65arr[i],obs76arr[i]], yerr=[obserr21[i],obserr32[i],obserr65[i],obserr76[i]],color='black',linestyle='None')
    plt.plot([1,2,3,4,5,6,7,8,9],[T10arr[i],T21arr[i],T32arr[i],T43arr[i],T54arr[i], T65arr[i],T76arr[i],T87arr[i],T98arr[i]],'k',label='model')
    plt.text(1,T43arr[i]*1.1,str(int(vel))+' km/s')
    plt.text(1,T43arr[i],'$\chi^2 = $'+str(chi[i]))
    plt.xlabel("J$_{up}$")
    plt.ylabel("$\int$ T$_{\mathrm{mb}}$dv (K km/s)")
    plt.legend()
    plt.axis([0,10,0.1,T43arr[i]*1.2])
    plt.savefig(path+"/sed_"+str(int(vel))+".png")
    plt.close(i)
#    end



