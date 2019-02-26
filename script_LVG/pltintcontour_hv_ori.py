import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
import matplotlib.pyplot as plt
import aplpy
import math
import sys

flag = int(sys.argv[1])
print 'flag: ',flag

ac = 116.21673
dc = -24.128361
avbra = 116.218372999
avbdec = -24.1316178604
avrra = 116.213773588
avrdec = -24.1262727157

velocity = np.arange(21)*2+48
nch = velocity.shape[0]

#filelist=['g240_co32_sft_mb_sin_nos_bpa_sft_cutad.fits','co21_cutad_novs.fits','./intermediate/co65_ori_mask.fits','./intermediate/co76_ori_mask.fits']
#namelist = ['co32apex','co21','co65_mask','co76_mask']
filelist=['g240_co32_sft_mb_sin_nos_bpa_sft.fits','co21_cutad_novs.fits', 'co65_mb_sft_bpa_nos.fits', 'co76_mb_sft_bpa_nos.fits']
namelist = ['co32apex','co21','co65','co76']
nametitle = ['CO (3-2) HV','CO (2-1) HV','CO (6-5) HV','CO (7-6) HV']
toTlist = [1,1.89,1,1]
vbminlist = [42,42,44,46]
vrmaxlist = [94,94,92,90]
vbmin = vbminlist[flag]
vbmax = 56
vrmin = 82
vrmax = vrmaxlist[flag]

fileco = fits.open(filelist[flag])
name = namelist[flag]
line_title = nametitle[flag]
toT = toTlist[flag]
hd = fileco[0].header
da = fileco[0].data
da[np.isnan(da)] = 0
w = WCS(hd)
k = 1.38e-23
c = 2.997e8
restf = hd['RESTFREQ']
lamb = c/restf
d = 5.32 #kpc
l = 1./2/d*0.18/math.pi
print lamb


nra = hd['naxis1']
ndec = hd['naxis2']
nvel = hd['naxis3']
refpix = hd['crpix3']
refv = hd['crval3']
wid = hd['cdelt3']
radelt = abs(hd['cdelt1'])*3600
decdelt = abs(hd['cdelt2'])*3600
bmaj = hd['bmaj']*3600
bmin = hd['bmin']*3600
n = np.arange(nvel)
velo = (n + 1 - refpix)*wid + refv
velo = velo / 1000.

indexb = (velo<=vbmax+0.1)&(velo>=vbmin-0.1)
indexr = (velo<=vrmax+0.1)&(velo>=vrmin-0.1)
print velo[indexb][0],velo[indexb][-1],velo[indexr][0],velo[indexr][-1]
#print n[indexb][0],n[indexb][-1],n[indexr][0],n[indexr][-1]

hd.remove('naxis3')
hd.remove('ctype3')
hd.remove('cdelt3')
hd.remove('crpix3')
hd.remove('crval3')
hd['naxis']=2

datab = np.zeros([ndec,nra])
datar = np.zeros([ndec,nra])

for i in range(ndec):
    for j in range(nra):
        for k in range(n[indexb][0],n[indexb][-1]+1):
            datab[i,j] += da[k,i,j]
        for m in range(n[indexr][0],n[indexr][-1]+1):
            datar[i,j] += da[m,i,j]

datab = datab*wid/1e3
datar = datar*wid/1e3
#datab = datab/(n[indexb][-1]-n[indexb][0]+1)
#datar = datar/(n[indexr][-1]-n[indexr][0]+1)

newb = fits.PrimaryHDU(data=datab,header=hd)
newr = fits.PrimaryHDU(data=datar,header=hd)
newb.writeto('./intfits/'+name+'_hv_blue.fits',clobber=True)
newr.writeto('./intfits/'+name+'_hv_red.fits',clobber=True)

peakb = datab.max()
levb = (np.arange(8)/10.+0.2)*peakb
levb.tolist()
peakr = datar.max()
levr = (np.arange(8)/10.+0.2)*peakr
levr.tolist()

line = aplpy.FITSFigure(newb)
line.show_contour(colors='blue', levels=levb)
line.show_contour(newr,colors='red', levels=levr,linestyles='dashed')
    #if flag==0 or flag==1:
#line.show_regions('ds9.reg')

line.add_beam()
line.beam.set_frame(True)
line.beam.set_facecolor('black')
line.beam.set_corner('bottom left')
line.add_label(0.2,0.9,line_title,relative=True,size='x-large')
line.add_scalebar(l)
line.scalebar.set_corner('bottom right')
line.scalebar.set_label('0.5pc')
line.recenter(ac,dc,width=0.0262,height=0.0262)
line.show_markers(avbra,avbdec,marker='+',facecolor='black',edgecolor='black')
line.show_markers(avrra,avrdec,marker='+',facecolor='black',edgecolor='black')
#line.show_markers(leftra,leftdec,marker='s',facecolor='black',edgecolor='black')
#line.show_markers(rightra,rightdec,marker='s',facecolor='black',edgecolor='black')
#line.show_markers(upra,updec,marker='s',facecolor='black',edgecolor='black')
#line.show_markers(downra,downdec,marker='s',facecolor='black',edgecolor='black')
#line.show_markers(boxra,boxdec,marker='s',facecolor='black',edgecolor='back')
#line.show_circles(boxra,boxdec,boxdia/3600)
line.save('./int_map_ori/intori_hv_'+name+'.png')


