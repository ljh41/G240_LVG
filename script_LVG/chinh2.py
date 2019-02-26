import numpy as np
import math
import string
import os
import sys

#name and flag
position = sys.argv[1]
flag = int(sys.argv[2])
flagerr = sys.argv[3]
print 'name',position,'err',flagerr
#flagerr: 0,err;1,err+rms;2,err+wei

#rms (K)
rms21 = 0.004
rms32 = 0.04
rms65 = 0.04
rms76 = 0.1

#defination
abun = 103
NLTE = 1e17
bf = 1.0
ntemp = 101
ncd = 99
arraycd = np.arange(ncd)
fmodellist = 'modellist'

#data. spec and nh2 list
#fda21 = np.loadtxt('./data/T/co21cvlT'+position+'.dat')
#if position=='pointdishbgaussian':
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

nh2list = open('./LVGmodelnh2/'+fmodellist)
line = nh2list.readline()
nnh2 = 0
while(line):
    nnh2 += 1
    line = nh2list.readline()
nh2list = open('./LVGmodelnh2/'+fmodellist)

#calculate chi-squared
print 'calculate chi'
nh2arr = []
velarr = []
temparr = []
tempminarr = []
tempmaxarr = []
cdarr = []
cdminarr = []
cdmaxarr = []
chiminarr = []
line3arr = []
pixxarr = []
pixyarr = []
fsolinter = open('./data/LVGall/allsol_LVG_'+position+'_'+flagerr+'.txt','w')
fsolinter.write('#velocity   nh2   Tkin   Tmin   Tmax   column_density   cdmin   cdmax  3line?   chi\n')
for i in range(nnh2):
    line = nh2list.readline()
    line = line.strip('\n')
    nh2 = line.strip('models/coall')
    nh2 = nh2.strip('.dat')
    #print nh2
    nh2 = float(nh2)
    fra = np.loadtxt('./LVGmodelnh2/'+line)

    tempall = fra[:,0]
    cdall = fra[:,1]
    tempall = tempall.reshape(ntemp,ncd)
    temp = tempall[:,0]
    cdall = cdall.reshape(ntemp,ncd)
    cd = cdall[0,:]

    ncritical = arraycd[cd<NLTE][-1]

    f10 = fra[:,2].reshape(ntemp,ncd)
    f21 = fra[:,3].reshape(ntemp,ncd)
    f32 = fra[:,4].reshape(ntemp,ncd)
    f43 = fra[:,5].reshape(ntemp,ncd)
    f54 = fra[:,6].reshape(ntemp,ncd)
    f65 = fra[:,7].reshape(ntemp,ncd)
    f76 = fra[:,8].reshape(ntemp,ncd)
    f87 = fra[:,9].reshape(ntemp,ncd)
    f98 = fra[:,10].reshape(ntemp,ncd)

    nvel = 0
    for j in range(n21):
        line3 = 0
        obs32 = 0
        obs65 = 0
        obs76 = 0
        obs21 = fda21[j,1]
        obstau21 = 0
        obstau65 = 0
        vel = fda21[j,0]

        if flag%2==1 and vel>67.5:
            continue
        if flag%2==0 and vel<67.5:
            continue

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
        for k in range(n76):
            if abs(vel-fda76[k,0])<0.01:
                obs76 = fda76[k,1]
                break
        obs21 = obs21/bf
        obs32 = obs32/bf
        obs65 = obs65/bf
        obs76 = obs76/bf
        
        err21 = obs21*0.1
        err32 = obs32*0.15
        err65 = obs65*0.2
        err76 = obs76*0.3
        
        snr21 = obs21/rms21
        snr32 = obs32/rms32
        snr65 = obs65/rms65
        snr76 = obs76/rms76
        snrsum = (snr21**2+snr32**2+snr65**2+snr76**2)/4
        
        obserr21 = 0
        obserr32 = 0
        obserr65 = 0
        obserr76 = 0
        if flagerr=='err':
            obserr21 = err21
            obserr32 = err32
            obserr65 = err65
            obserr76 = err76
        if flagerr=='errrms':
            obserr21 = (err21**2+rms21**2)**0.5
            obserr32 = (err32**2+rms32**2)**0.5
            obserr65 = (err65**2+rms65**2)**0.5
            obserr76 = (err76**2+rms76**2)**0.5
        if flagerr=='errwei':
            obserr21 = err21/snr21*snrsum**0.5
            if obs32!=0:
                obserr32 = err32/snr32*snrsum**0.5
            if obs65!=0:
                obserr65 = err65/snr65*snrsum**0.5
            if obs76!=0:
                obserr76 = err76/snr76*snrsum**0.5
            if i==0:
                print vel,snr21,snr32,snr65,snr76,snrsum**0.5/snr21,snrsum**0.5/snr32,snrsum**0.5/snr65,snrsum**0.5/snr76
        chiimage = np.zeros([ntemp,ncd])

        if obs65!=0 and obs76==0:
            line3 = 1
            for l in range(ntemp):
                for m in range(ncd):
                    u21 = (obs21-f21[l,m])**2/obserr21**2
                    u32 = (obs32-f32[l,m])**2/obserr32**2
                    u65 = (obs65-f65[l,m])**2/obserr65**2
                    chiimage[l,m] = (u21 + u32 + u65)
        if obs65!=0 and obs76!=0:
            for l in range(ntemp):
                for m in range(ncd):
                    u21 = (obs21-f21[l,m])**2/obserr21**2
                    u32 = (obs32-f32[l,m])**2/obserr32**2
                    u65 = (obs65-f65[l,m])**2/obserr65**2
                    u76 = (obs76-f76[l,m])**2/obserr76**2
                    chiimage[l,m] = (u21 + u32 + u65 + u76)

        if obs65==0 and obs76==0:
            continue

        nvel += 1

        pixmin = chiimage.argmin()
        pixmdax = pixmin/ncd
        pixmday = pixmin%ncd

        pixLNmin = chiimage[:,:ncritical].argmin()
        pixLNx = pixLNmin/ncritical
        pixLNy = pixLNmin%ncritical
        chiminln = chiimage[pixLNx,pixLNy]

        chiarrTln = chiimage[:,pixLNy]
        indextln = (chiarrTln < chiminln + 1)
        templn = temp[indextln]
        tminln = templn[0]
        tmaxln = templn[-1]

        chiarrcdln = chiimage[pixLNx,:]
        indexcdln = (chiarrcdln < chiminln + 1)
        cdln = cd[indexcdln]
        cdminln = cdln[0]
        cdmaxln = cdln[-1]

        damin = chiimage.min()
        
        nh2arr = nh2arr + [nh2]
        velarr = velarr + [vel]
        temparr = temparr + [temp[pixLNx]]
        tempminarr = tempminarr + [tminln]
        tempmaxarr = tempmaxarr + [tmaxln]
        cdarr = cdarr + [cd[pixLNy]]
        cdminarr = cdminarr + [cdminln]
        cdmaxarr = cdmaxarr + [cdmaxln]
        chiminarr = chiminarr + [chiminln]
        line3arr = line3arr + [line3]
        pixxarr = pixxarr + [pixLNx]
        pixyarr = pixyarr + [pixLNy]

        fsolinter.write(str(vel)+'  '+'%5.2e'%(nh2)+'  '+str(temp[pixLNx])+'  '+str(tminln)+'  '+str(tmaxln)+'  '+str(cd[pixLNy])+'  '+str(cdminln)+'  '+str(cdmaxln)+'  '+str(line3)+'  '+'%5.3f'%(chiminln)+'\n')
fsolinter.close()

#reshape  nnh2*nvel arrays. parameter space
nh2arr = np.array(nh2arr).reshape([nnh2,nvel])
velarr = np.array(velarr).reshape([nnh2,nvel])
temparr = np.array(temparr).reshape([nnh2,nvel])
tempminarr = np.array(tempminarr).reshape([nnh2,nvel])
tempmaxarr = np.array(tempmaxarr).reshape([nnh2,nvel])
cdarr = np.array(cdarr).reshape([nnh2,nvel])
cdminarr = np.array(cdminarr).reshape([nnh2,nvel])
cdmaxarr = np.array(cdmaxarr).reshape([nnh2,nvel])
chiminarr = np.array(chiminarr).reshape([nnh2,nvel])
line3arr = np.array(line3arr).reshape([nnh2,nvel])
pixxarr = np.array(pixxarr).reshape([nnh2,nvel])
pixxarr = np.array(pixxarr).reshape([nnh2,nvel])

#get the final parameter range
print 'get parameter range'
fsol = open('./data/LVGsolution/LVG_'+position+'_'+flagerr+'.txt','w')
fsol.write('#velocity   nh2   nh2min    nh2max   Tkin   Tmin   Tmax   column_density   cdmin   cdmax  3line?   chi\n')
fsed = open('./data/LVGsolution/SED_'+position+'_'+flagerr+'.txt','w')
fsed.write('#vel   T21    T32    T65    T76   obs21   obs32   obs65   obs76   chi\n')
for i in range(nvel):
    vel = velarr[0,i]
    nh2vel = nh2arr[:,i]
    tempvel = temparr[:,i]
    tempminvel = tempminarr[:,i]
    tempmaxvel = tempmaxarr[:,i]
    cdvel = cdarr[:,i]
    cdminvel = cdminarr[:,i]
    cdmaxvel = cdmaxarr[:,i]
    line3fi = line3arr[0,i]
    chiminvel = chiminarr[:,i]
    
    pixfi = chiminvel.argmin()
    chiminfi = chiminvel[pixfi]
    nh2fi = nh2vel[pixfi]
    tempfi = tempvel[pixfi]
    cdfi = cdvel[pixfi]
    print 'vel nh2 temp cd line3 chimin'
    print vel,nh2fi,tempfi,cdfi,line3fi,chiminfi
    
    indfi = (chiminvel < chiminfi + 1)
    nh2fimin = nh2vel[indfi].min()
    nh2fimax = nh2vel[indfi].max()
    tempfimin = tempminvel[indfi].min()
    tempfimax = tempmaxvel[indfi].max()
    cdfimin = cdminvel[indfi].min()
    cdfimax = cdmaxvel[indfi].max()
    
    fsol.write(str(vel)+'  '+'%5.2e'%(nh2fi)+'  '+'%5.2e'%(nh2fimin)+'  '+'%5.2e'%(nh2fimax)+'  '+str(tempfi)+'  '+str(tempfimin)+'  '+str(tempfimax)+'  '+str(cdfi)+'  '+str(cdfimin)+'  '+str(cdfimax)+'  '+str(line3fi)+'  '+'%5.3f'%(chiminfi)+'\n')
    
    
    
    namenh2 = '%.1e'%(nh2fi)
    namenh2 = namenh2.replace('+0','')
    #print vel,namenh2
    fra = np.loadtxt('./LVGmodelnh2/models/coall'+namenh2+'.dat')
    
    tempall = fra[:,0]
    cdall = fra[:,1]
    tempall = tempall.reshape(ntemp,ncd)
    temp = tempall[:,0]
    cdall = cdall.reshape(ntemp,ncd)
    cd = cdall[0,:]
    
    f10 = fra[:,2].reshape(ntemp,ncd)
    f21 = fra[:,3].reshape(ntemp,ncd)
    f32 = fra[:,4].reshape(ntemp,ncd)
    f43 = fra[:,5].reshape(ntemp,ncd)
    f54 = fra[:,6].reshape(ntemp,ncd)
    f65 = fra[:,7].reshape(ntemp,ncd)
    f76 = fra[:,8].reshape(ntemp,ncd)
    f87 = fra[:,9].reshape(ntemp,ncd)
    f98 = fra[:,10].reshape(ntemp,ncd)
    
    pixx = np.arange(ntemp)[abs(temp-tempfi)<0.1]
    pixy = np.arange(ncd)[abs(cd-cdfi)<1e13]
    #print vel,pixx,pixy
    
    T10 = f10[pixx,pixy]
    T21 = f21[pixx,pixy]
    T32 = f32[pixx,pixy]
    T43 = f43[pixx,pixy]
    T54 = f54[pixx,pixy]
    T65 = f65[pixx,pixy]
    T76 = f76[pixx,pixy]
    T87 = f87[pixx,pixy]
    T98 = f98[pixx,pixy]
    
    obs21 = 0
    obs32 = 0
    obs65 = 0
    obs76 = 0

    for k in range(n21):
        if abs(vel-fda21[k,0])<0.01:
            obs21 = fda21[k,1]
            break
    for k in range(n32):
        if abs(vel-fda32[k,0])<0.01:
            obs32 = fda32[k,1]
            break
    for k in range(n65):
        if abs(vel-fda65[k,0])<0.01:
            obs65 = fda65[k,1]
            break
    for k in range(n76):
        if abs(vel-fda76[k,0])<0.01:
            obs76 = fda76[k,1]
            break
#print vel,T21,T32,T65,T76,obs21,obs32,obs65,obs76
    fsed.write('%5.2f  %5.2f  %5.2f  %5.2f  %5.2f  %5.2f  %5.2f  %5.2f  %5.2f  %5.2f  %5.2f  %5.2f  %5.2f  %5.2f   %5.3f\n' %(vel,obs21,obs32, obs65, obs76, T10, T21, T32, T43, T54, T65, T76, T87, T98, chiminfi))
#    fengjingchefu
fsol.close()
fsed.close()


