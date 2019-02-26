import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy import units as u
from astropy.coordinates import Angle
import matplotlib.pyplot as plt
import aplpy
import math
import sys

inf = '2p122'
name = 'co76'
fitsname = 'co76_ori_mask'

#coords
ac = 116.21673
dc = -24.128361
ra_chen07a = '7h44m52.04s'
dec_chen07a = '-24d07m42.2s'
ra_chen07b = '7h44m51.96s'
dec_chen07b = '-24d07m42.92s'

ra_OH03 = '7h44m51.97s'
dec_OH03 = '-24d07m42.3s'

ra_H2O15 = '7h44m51.9205s'  #IRAS 07427
dec_H2O15 = '-24d07m41.457s'

[ra_H2O15,dec_H2O15] = Angle([ra_H2O15,dec_H2O15]).degree

[ra_chen07a,dec_chen07a,ra_chen07b,dec_chen07b,ra_OH03,dec_OH03] = Angle([ra_chen07a,dec_chen07a,ra_chen07b,dec_chen07b,ra_OH03,dec_OH03]).degree

#defin
velocity = np.arange(27)*2+42
nch = velocity.shape[0]

toT = 1.89
levs = (np.arange(50)/2.0-2.0)
lev2 = (np.arange(50)-2.0)/toT
levs = levs.tolist()
lev2 = lev2.tolist()
levs.remove(0.)
lev2.remove(0.)

#fits
fco = fits.open(fitsname+'.fits')
finf = fits.open('./'+inf+'.fits')

hd = fco[0].header
da = fco[0].data
da[np.isnan(da)] = 0
w = WCS(hd)
k = 1.38e-23
c = 2.997e8
restf = hd['RESTFREQ']
lamb = c/restf
d = 5.32 #kpc
l = 1./2/d*0.18/math.pi
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


#plot
m = 4
fig = plt.figure()
fig.set_size_inches(10,15)
plt.axis('off')
ch = 0
for i in range(nch):
    n = nch / m
    if nch%m!=0:
        n+=1
    nx = ch % m
    ny = ch / m
    ch = ch + 1
    xmin = 0.1 + nx*0.8/m
    ymin = 0.9 - (ny+1)*0.8/n
    dx = 0.8/m
    dy = 0.8/n
    
    vel = velocity[i]
    print vel
    for j in range(nvel):
        if abs(velo[j]-vel)<0.1:
            break
    if abs(velo[j]-vel)>0.1:
        continue

    line = aplpy.FITSFigure(finf,figure=fig, subplot=[xmin,ymin,dx,dy])
    line.show_grayscale(invert=True)

    peakj = da[j,:,:].max()
    level1 = np.logspace(np.log10(0.5),np.log10(peakj),num=5)
    level2 = np.logspace(np.log10(1.),np.log10(peakj),num=5)

    if vel<58.5:
        line.show_contour(fco[0],slices=[j],colors='blue',levels=level1,alpha=0.4,linewidths=0.3)
    if vel>58.5 and vel<67.5:
        line.show_contour(fco[0],slices=[j],colors='blue',levels=level2,alpha=0.6,linewidths=0.5)
    if vel>67.5 and vel<77.5:
        line.show_contour(fco[0],slices=[j],colors='red',levels=level2,alpha=0.6,linewidths=0.5)
    if vel>77.5:
        line.show_contour(fco[0],slices=[j],colors='red',levels=level1,alpha=0.4,linewidths=0.3)


    line.add_scalebar(l)
    line.scalebar.set_corner('top right')
    line.scalebar.set_label('0.5pc')
#line.show_markers(ra_chen07a,dec_chen07a,marker='*',facecolor='white',edgecolor='yellow')
#line.show_markers(ra_chen07b,dec_chen07b,marker='*',facecolor='white',edgecolor='yellow')
#line.show_markers(ra_OH03,dec_OH03,marker='o',facecolor='white',edgecolor='cyan')
    line.show_markers(ra_H2O15,dec_H2O15,marker='*',facecolor='black',zorder=50,edgecolor='black')
    line.add_label(0.2,0.9, text=vel, relative=True, size='small')
    line.set_tick_labels_font(size='x-small')
    line.set_axis_labels_font(size='small')
    if nx!=0:
        line.hide_ytick_labels()
        line.hide_yaxis_label()
    if ny!=n-1 | nx!=0:
        line.hide_xtick_labels()
        line.hide_xaxis_label()
    line.recenter(ac,dc,width=0.0262,height=0.0262)
    line.savefig('./channelmap/'+name+'_'+inf+'.eps')
