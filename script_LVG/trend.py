import numpy as np
import math
import os
import sys
import matplotlib.pyplot as plt

#flagerr = sys.argv[1]
flagerr = 'errrms'

#data
fchiminblue = np.loadtxt('./data/LVGsolution/LVG_pointdishbgaussian'+'_'+flagerr+'.txt')
nchiblue = fchiminblue.shape[0]
fchiminred = np.loadtxt('./data/LVGsolution/LVG_pointdishrgaussian'+'_'+flagerr+'.txt')
nchired = fchiminred.shape[0]

line3blue = fchiminblue[:,10]
velblue = fchiminblue[:,0]
indexblue = (velblue<61.5) & (velblue>45.5)
velblue = velblue[indexblue]
nh2 = fchiminblue[:,1][indexblue]
nh2min = fchiminblue[:,2][indexblue]
nh2max = fchiminblue[:,3][indexblue]
Tkinblue = fchiminblue[:,4][indexblue]
Tminblue = fchiminblue[:,5][indexblue]
Tmaxblue = fchiminblue[:,6][indexblue]
cdblue = fchiminblue[:,7][indexblue]
cdminblue = fchiminblue[:,8][indexblue]
cdmaxblue = fchiminblue[:,9][indexblue]
chiblue = fchiminblue[:,11][indexblue]


line3red = fchiminred[:,10]
velred = fchiminred[:,0]
indexred = (velred>73.5) & (velred<90.5)
velred = velred[indexred]
nh2 = fchiminred[:,1][indexred]
nh2min = fchiminred[:,2][indexred]
nh2max = fchiminred[:,3][indexred]
Tkinred = fchiminred[:,4][indexred]
Tminred = fchiminred[:,5][indexred]
Tmaxred = fchiminred[:,6][indexred]
cdred = fchiminred[:,7][indexred]
cdminred = fchiminred[:,8][indexred]
cdmaxred = fchiminred[:,9][indexred]
chired = fchiminred[:,11][indexred]


#print indexblue
#print indexred

Terrblue = np.array([Tkinblue-Tminblue,Tmaxblue-Tkinblue])
Terrred = np.array([Tkinred-Tminred,Tmaxred-Tkinred])

cderrblue = np.array([cdblue-cdminblue,cdmaxblue-cdblue])
cderrred = np.array([cdred-cdminred,cdmaxred-cdred])

ftandnb = np.loadtxt('./data/RTsolution/TandN_pointdishbgaussian_Tex50.txt')
ntandnb = ftandnb.shape[0]
ftandnr = np.loadtxt('./data/RTsolution/TandN_pointdishrgaussian_Tex50.txt')
ntandnr = ftandnr.shape[0]

velrdblue = ftandnb[:,0]
indexrdblue = (velrdblue<61.5) & (velrdblue>45.5)
velrdblue = velrdblue[indexrdblue]
Tkinrdblue = ftandnb[:,1][indexrdblue]
cdrdblue = ftandnb[:,2][indexrdblue]

velrdred = ftandnr[:,0]
indexrdred = (velrdred>73.5) & (velrdred<90.5)
velrdred = velrdred[indexrdred]
Tkinrdred = ftandnr[:,1][indexrdred]
cdrdred = ftandnr[:,2][indexrdred]

#plot T-V
plt.figure(0)

plt.plot(67.5-velblue,Tkinblue,'bs',markersize=8,markerfacecolor='white',zorder=47,label='Blue lobe (LVG)')
#plt.errorbar(67.5-velblue[indexblue],Tkinblue[indexblue],yerr=Terrblue,color='blue',ls="None")
plt.plot(67.5-velrdblue,Tkinrdblue, 'bx',markersize=10,markerfacecolor='blue', markeredgecolor='blue', zorder=48, label='Blue lobe (RD)')
    #for i in range(velblue[indexblue].shape[0]):
#    plt.text(67.5-velblue[indexblue][i]-0.6,Tkinblue[indexblue][i]+10,'%5.1f'%(chiblue[i]))


plt.plot(velred-67.5,Tkinred,'rs',markersize=8,markerfacecolor='white',zorder=49,label='Red lobe (LVG)')
#plt.errorbar(velred[indexred]-67.5,Tkinred[indexred],yerr=Terrred,color='red',ls="None")
plt.plot(velrdred-67.5,Tkinrdred,'rx',markersize=10,markeredgecolor='red',zorder=50,label='Red lobe (RD)')
    #for i in range(velred[indexred].shape[0]):
#    plt.text(40,Tkinred[indexred][i]-10,'%5.1f'%(chired[i]))

plt.legend()
plt.xlabel('$V_{\mathrm{outflow}}$ (km s$^{-1}$)')
#plt.ylabel('$T_{\mathrm{kin}}$(K)')
plt.ylabel('$T$ (K)')
#plt.yscale('log')
plt.axis([6,24,30,80])
#plt.plot([6,6],[0,150],'k--')
plt.minorticks_on()
#plt.savefig('./fig/tv_paper'+'_'+flagerr+'.eps')
plt.savefig('./fig/tv_paper.eps')
plt.close(0)

#plot N-V
plt.figure(1)

plt.plot(67.5-velblue,cdblue,'bs',markersize=8,markerfacecolor='white',zorder=47,label='Blue lobe (LVG)')
#plt.errorbar(67.5-velblue[indexblue],cdblue[indexblue],yerr=cderrblue,color='black',ls="None")
plt.plot(67.5-velrdblue,cdrdblue,'bx',markersize=10,markerfacecolor='blue',markeredgecolor='blue', zorder=48,label='Blue lobe (RD)')
#for i in range(velblue.shape[0]):
#    plt.text(67.5-velblue[i]-0.6,cdblue[i]*0.7,'%5.2f'%(chiblue[i]))

plt.plot(velred-67.5,cdred,'rs',markersize=8,markerfacecolor='white',zorder=49,label='Red lobe (LVG)')
#plt.errorbar(velred[indexred]-67.5,cdred[indexred],yerr=cderrred,color='black',ls="None")
plt.plot(velrdred-67.5,cdrdred,'rx',markersize=10,markeredgecolor='red',zorder=50,label='Red lobe (RD)')
#for i in range(velred.shape[0]):
#    plt.text(velred[i]-67.5-0.6,cdred[i]*1.2,'%5.2f'%(chired[i]))

plt.legend()
plt.xlabel('$V_{\mathrm{outflow}}$ (km s$^{-1}$)')
#plt.ylabel('$N_\mathrm{CO}$ (cm$^{-2}$)')
plt.ylabel('$N$ (cm$^{-2}$)')
plt.axis([6,24,2e14,4e16])
plt.yscale('log')
#plt.plot([6,6],[3e14,4e16],'k--')
plt.minorticks_on()
#plt.savefig('./fig/Nv_paper'+'_'+flagerr+'.eps')
plt.savefig('./fig/Nv_paper.eps')
plt.close(1)
