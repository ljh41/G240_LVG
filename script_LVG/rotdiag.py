import numpy as np
import math
import matplotlib.pyplot as plt
import os
import sys

#name and flag
position = sys.argv[1]
print 'name',position

#defination
velocity = 60.
Tex = 50.

#rms (K)
rms21 = 0.004
rms32 = 0.04
rms65 = 0.04
rms76 = 0.1

#constant
h = 6.626e-34
k = 1.38e-23
c = 3.0e8
mu21 = 230.53800e9
mu32 = 345.79599e9
mu65 = 691.4730e9
mu76 = 806.65180e9
A21 = -6.1605
A32 = -5.6026
A65 = -4.6701
A76 = -4.4657
E21 = 16.6013 #in K
E32 = 33.1994
E65 = 116.1745
E76 = 154.8899
g21 = 5
g32 = 7
g65 = 13
g76 = 15


Tarr = np.array([1000.,500.,300.,225.,150.,75.,37.5,18.75,9.375,5.000,2.725])
Zarr = np.array([2.5595,2.2584,2.0369,1.9123,1.7370,1.4386,1.1429,0.8526,0.5733,0.3389,0.1478])
Tarr.sort()
Zarr.sort()
zex = 10**Zarr
Z = np.log10(np.interp(Tex,Tarr,zex))

'''
fda21 = np.loadtxt('./data/T/co21ficvlT'+position+'.dat')
fda32 = np.loadtxt('./data/T/co32apex_smcvlT'+position+'.dat')
fda65 = np.loadtxt('./data/T/co65_sft_smcvlT'+position+'.dat')
fda76 = np.loadtxt('./data/T/co76_sft_smcvlT'+position+'.dat')
'''
fda21 = np.loadtxt('./data/T/co21ficvlT'+position+'.dat')
fda32 = np.loadtxt('./data/T/co32_smcvlT'+position+'.dat')
fda65 = np.loadtxt('./data/T/co65_smmaskcvlT'+position+'.dat')
fda76 = np.loadtxt('./data/T/co76_smmaskcvlT'+position+'.dat')
n21 = fda21.shape[0]
n32 = fda32.shape[0]
n65 = fda65.shape[0]
n76 = fda76.shape[0]

ft = open('./data/RTsolution/TandN_'+position+'_Tex'+str(int(Tex))+'.txt','w')
for j in range(n21):
    obs32 = 0
    obs65 = 0
    obs76 = 0
    obs21 = fda21[j,1]
    vel = fda21[j,0]
    print vel
    for k in range(n32):
        if abs(vel-fda32[k,0])<0.01:
            obs32 = fda32[k,1]
            break
    if obs32==0:
        continue
    for k in range(n65):
        if abs(vel-fda65[k,0])<0.01:
            obs65 = fda65[k,1]
            break
    if obs65==0:
        continue
    for k in range(n76):
        if abs(vel-fda76[k,0])<0.01:
            obs76 = fda76[k,1]
            break
    T21 = obs21
    T32 = obs32
    T65 = obs65

    err21 = obs21*0.1
    err32 = obs32*0.15
    err65 = obs65*0.2
    err76 = obs76*0.3

    obserr21 = (err21**2+rms21**2)**0.5
    obserr32 = (err32**2+rms32**2)**0.5
    obserr65 = (err65**2+rms65**2)**0.5
    obserr76 = (err76**2+rms76**2)**0.5

    const21 = 298207655543928.40
    const32 = 185683644420422.18
    const65 = 86732966311934.35
    const76 = 73723502632994.91
    Nu21 = const21*T21
    Nu32 = const32*T32
    Nu65 = const65*T65


    #    print vel,const21,const32,const65,const76,Nu21,Nu32,Nu65,Nu76
    y21 = math.log(Nu21/g21*10**Z)
    y32 = math.log(Nu32/g32*10**Z)
    y65 = math.log(Nu65/g65*10**Z)

    Nulow21 = const21*(T21-obserr21)
    Nulow32 = const32*(T32-obserr32)
    Nulow65 = const65*(T65-obserr65)
    Nuup21 = const21*(T21+obserr21)
    Nuup32 = const32*(T32+obserr32)
    Nuup65 = const65*(T65+obserr65)

    ylow21 = math.log(Nulow21/g21*10**Z)
    ylow32 = math.log(Nulow32/g32*10**Z)
    ylow65 = math.log(Nulow65/g65*10**Z)
    yup21 = math.log(Nuup21/g21*10**Z)
    yup32 = math.log(Nuup32/g32*10**Z)
    yup65 = math.log(Nuup65/g65*10**Z)

    x = np.array([E21,E32,E65])
    y = np.array([y21,y32,y65])

    yerr = np.array([[y21-ylow21,y32-ylow32,y65-ylow65],[yup21-y21,yup32-y32,yup65-y65]])
    if obs76!=0:
        T76 = obs76
        Nu76 = const76*T76
        y76 = math.log(Nu76/g76*10**Z)
        x = np.array([E21,E32,E65,E76])
        y = np.array([y21,y32,y65,y76])
        Nulow76 = const76*(T76-obserr76)
        Nuup76 = const76*(T76+obserr76)
        ylow76 = math.log(Nulow76/g76*10**Z)
        yup76 = math.log(Nuup76/g76*10**Z)
        yerr = np.array([[y21-ylow21,y32-ylow32,y65-ylow65,y76-ylow76], [yup21-y21, yup32-y32, yup65-y65, yup76-y76]])

    coeff = np.polyfit(x, y, 1)
    pline = np.poly1d(coeff)
    Tkin = -1./coeff[0]
    Nco = math.exp(coeff[1])
    ft.write(str(vel)+'  %5.3f  %5.3e\n'%(Tkin,Nco))

    plt.figure(j)
    plt.plot(x,y,'ko',markersize=10)
    plt.errorbar(x,y,yerr=yerr,color='black',linestyle='None')
    plt.xlabel('$E_\mathrm{up}$ (K)')
    plt.ylabel('ln($N_\mathrm{up}/g_\mathrm{up}$)')
    #plt.title('Tkin=%5.3f K, N=%5.3e'% (Tkin,Nco))
    xfit = np.arange(170)
    yfit = xfit*coeff[0]+coeff[1]
    plt.plot(xfit,yfit,'k')
    plt.savefig('fig/RD/RD_'+str(int(vel))+'.png')
    plt.close(j)
ft.close()
