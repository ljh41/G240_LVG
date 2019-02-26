import numpy as np
import math
import string
import os
import sys
import matplotlib.pyplot as plt

#name
errflag = 'errrms'

#rms
rms21 = 0.004
rms32 = 0.04
rms65 = 0.04
rms76 = 0.1

#define
vellist = [46,48,50,52,54,56,58,60,74,76,78,80,82,84,86,88,90]
nvel = len(vellist)

dv = 2.

#plot
m = 3 #panel per row
n = 6 #rows

fig = plt.figure()
fig.set_size_inches(12,12)
plt.axis('off')
ch=0

for i in range(nvel):
    nx = ch % m
    ny = ch / m
    ch = ch + 1
    xmin = 0.1 + nx*0.8/m
    ymin = 0.9 - (ny+1)*0.8/n
    dx = 0.8/m
    dy = 0.8/n

    vel = vellist[i]
    if vel<67.5:
        fsed = np.loadtxt('./data/LVGsolution/SED_pointdishbgaussian_'+errflag+'.txt')
    if vel>67.5:
        fsed = np.loadtxt('./data/LVGsolution/SED_pointdishrgaussian_'+errflag+'.txt')
    indv = abs(fsed[:,0]-vel)<0.1

    obs21 = fsed[:,1][indv]
    obs32 = fsed[:,2][indv]
    obs65 = fsed[:,3][indv]
    obs76 = fsed[:,4][indv]
    T10 = fsed[:,5][indv]
    T21 = fsed[:,6][indv]
    T32 = fsed[:,7][indv]
    T43 = fsed[:,8][indv]
    T54 = fsed[:,9][indv]
    T65 = fsed[:,10][indv]
    T76 = fsed[:,11][indv]
    T87 = fsed[:,12][indv]
    T98 = fsed[:,13][indv]
    chi = fsed[:,14][indv]

    #noise
    err21 = obs21*0.1
    err32 = obs32*0.15
    err65 = obs65*0.2
    err76 = obs76*0.3
    obserr21 = (err21**2+rms21**2)**0.5
    obserr32 = (err32**2+rms32**2)**0.5
    obserr65 = (err65**2+rms65**2)**0.5
    obserr76 = (err76**2+rms76**2)**0.5
    
    #dv = 2 km/s
    obs21 = dv * obs21
    obs32 = dv * obs32
    obs65 = dv * obs65
    obs76 = dv * obs76
    obserr21 = dv * obserr21
    obserr32 = dv * obserr32
    obserr65 = dv * obserr65
    obserr76 = dv * obserr76
    T10 = dv * T10
    T21 = dv * T21
    T32 = dv * T32
    T43 = dv * T43
    T54 = dv * T54
    T65 = dv * T65
    T76 = dv * T76
    T87 = dv * T87
    T98 = dv * T98

    plt.subplot(n,m,i+1)
    plt.plot([2,3,6,7],[obs21,obs32,obs65,obs76],'ko',label = 'observations')
    plt.errorbar([2,3,6,7],[obs21,obs32,obs65,obs76], yerr=[obserr21,obserr32,obserr65,obserr76],color='black',linestyle='None')
    plt.plot([1,2,3,4,5,6,7,8,9],[T10,T21,T32,T43,T54, T65,T76,T87,T98],'k',label='model')
    plt.text(6.3,T43*0.98,'$v=$'+str(int(vel))+' km s$^{-1}$')
    plt.text(6.3,T43*0.78,'$\chi^2_{\mathrm{red}}=%5.2f$'%(chi[0]))

#print nx,ny,m,n
    if ny==(n-1) and nx==0:
        plt.xlabel("$J_{\mathrm{up}}$")
        plt.ylabel("$\int T_{\mathrm{mb}}$dv (K km s$^{-1}$)")
#plt.legend()
    plt.axis([0,10,0.1,T43*1.2])

fig.canvas.draw()
fig.savefig('./fig/SED.eps')


