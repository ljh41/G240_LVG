import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy import units as u
from astropy.coordinates import Angle
from astropy.coordinates import SkyCoord
import matplotlib.pyplot as plt
import aplpy
import math

#positions
ac = 116.21673
dc = -24.128361
avbra = 116.218372999
avbdec = -24.1316178604
avrra = 116.213773588
avrdec = -24.1262727157

bluelobe = SkyCoord(ra=avbra*u.degree,dec=avbdec*u.degree)
redlobe = SkyCoord(ra=avrra*u.degree,dec=avrdec*u.degree)
print 'bluelobe',bluelobe.ra.hms, bluelobe.dec.dms
print 'redlobe',redlobe.ra.hms, redlobe.dec.dms

ra_H2O15 = '7h44m51.9205s'  #IRAS 07427
dec_H2O15 = '-24d07m41.457s'

[ra_H2O15,dec_H2O15] = Angle([ra_H2O15,dec_H2O15]).degree

#region
coeff1 = 92.09415
coeff2 = -140.336
coeff3 = 92.08186
coeff4 = -140.354

[x1,y1] = [(coeff1-coeff2)/2,(coeff1+coeff2)/2]
[x2,y2] = [(coeff3-coeff4)/2,(coeff3+coeff4)/2]
[x3,y3] = [(coeff1-coeff4)/2,(coeff1+coeff4)/2]
[x4,y4] = [(coeff3-coeff2)/2,(coeff3+coeff2)/2]
border1 = np.array([[x1,x3],[y1,y3]])
border2 = np.array([[x3,x2],[y3,y2]])
border3 = np.array([[x1,x4],[y1,y4]])
border4 = np.array([[x4,x2],[y4,y2]])
linelist = [border1,border2,border3,border4]

#list
namelist = ['co21_lv','co32apex_lv','co65_mask_lv','co76_mask_lv',\
'co21_hv','co32apex_hv','co65_mask_hv','co76_mask_hv']
    #namelist = ['co21_lv','co32apex_lv','co65_lv','co76_lv',\
#            'co21_hv','co32apex_hv','co65_hv','co76_hv']
#nametitle = ['CO J = 2-1 LV','CO J = 3-2 LV','CO J = 6-5 LV','CO J = 7-6 LV'\
#,'CO J = 2-1 HV','CO J = 3-2 HV','CO J = 6-5 HV','CO J = 7-6 HV']
nametitle = ['CO 2-1 LV','CO 3-2 LV','CO 6-5 LV','CO 7-6 LV'\
,'CO 2-1 HV','CO 3-2 HV','CO 6-5 HV','CO 7-6 HV']
linenamelist = ['co21lv','co32lv','co65lv','co76lv','co21hv','co32hv','co65hv','co76hv']
telelist = ['SMA+CSO','APEX','APEX','APEX','SMA+CSO','APEX','APEX','APEX']
labellist = ['(a)','(b)','(c)','(d)','(e)','(f)','(g)','(h)']

#figure
m = 4 #panel per row
n = 2 #rows

fig = plt.figure()
fig.set_size_inches(12,6)
plt.axis('off')
ch=0
#fpeak = open('./peak.txt','w')
#fpeak.write('#lines  peakb  peakr \n')
for i in range(8):
    nx = ch % m
    ny = ch / m
    ch = ch + 1
    xmin = 0.1 + nx*0.8/m
    ymin = 0.9 - (ny+1)*0.8/n
    dx = 0.8/m
    dy = 0.8/n
    
    filecob = fits.open('./intfits/'+namelist[i]+'_blue.fits')
    filecor = fits.open('./intfits/'+namelist[i]+'_red.fits')
    line_title = nametitle[i]
    linename = linenamelist[i]
    plabel = labellist[i]
    tele = telelist[i]
    hd = filecob[0].header
    dab = filecob[0].data
    dar = filecob[0].data
    w = WCS(hd)
    k = 1.38e-23
    c = 2.997e8
    restf = hd['RESTFREQ']
    lamb = c/restf
    d = 5.32 #kpc
    l = 1./2/d*0.18/math.pi
    
    #peak
    fpeak = open('./peak.txt')
    line = fpeak.readline()
    words = line.split()
    while (words[0] != linename):
        line  = fpeak.readline()
        words = line.split()
    print words[0]
    peakb = float(words[1])
    peakr = float(words[2])
#peakb = dab.max()
#peakr = dar.max()
    levb = (np.arange(8)/10.+0.2)*peakb
    levb.tolist()
    levb76 = (np.arange(8)/10.+0.3)*peakb
    levb76.tolist()

    levr = (np.arange(8)/10.+0.2)*peakr
    levr.tolist()
    levr76 = (np.arange(8)/10.+0.3)*peakr
    levr76.tolist()
    
    #fpeak.write(line_title+'   '+str(peakb)+'   '+str(peakr)+'\n')

    line = aplpy.FITSFigure(filecob[0], figure=fig, subplot=[xmin,ymin,dx,dy])
    if i < 6.5:
        line.show_contour(colors='blue',levels=levb,linewidths=1)
        line.show_contour(filecor[0],colors='red', levels=levr,linewidths=1)
    if i > 6.5:
        line.show_contour(colors='blue',levels=levb76,linewidths=1)
        line.show_contour(filecor[0],colors='red', levels=levr76,linewidths=1)
    line.add_beam()
    line.beam.set_frame(True)
    line.beam.set_facecolor('black')
    line.beam.set_corner('bottom right')
    if i!=0 and i!=4:
        line.add_label(0.12,0.9,tele,relative=True,size='small')
    if i==0 or i==4:
        line.add_label(0.18,0.9,tele,relative=True,size='small')
    line.add_label(0.2,0.8,line_title,relative=True,size='small')
    if i < 3.5:
        line.add_label(0.15,0.7,'[58, 64]',relative=True,size='small')
        line.add_label(0.15,0.6,'[74, 80]',relative=True,size='small')
    if i > 3.5 and i < 5.5:
        line.add_label(0.15,0.7,'[42, 56]',relative=True,size='small')
        line.add_label(0.15,0.6,'[82, 94]',relative=True,size='small')
    if i > 5.5 and i < 6.5:
        line.add_label(0.15,0.7,'[44, 56]',relative=True,size='small')
        line.add_label(0.15,0.6,'[82, 92]',relative=True,size='small')
    if i > 6.5:
        line.add_label(0.15,0.7,'[46, 56]',relative=True,size='small')
        line.add_label(0.15,0.6,'[82, 90]',relative=True,size='small')

#    if i<0.5 or (i<3.5 and i>2.5):
    line.show_markers(avbra,avbdec,marker='+',facecolor='black',edgecolor='black', s=400,zorder=50,linewidth=2)
    line.show_markers(avrra,avrdec,marker='+',facecolor='black',edgecolor='black', s=400,zorder=50,linewidth=2)
    line.show_markers(ra_H2O15,dec_H2O15,marker='*',facecolor='black',zorder=50,edgecolor='black')

#if i==7:
#line.show_lines(line_list=linelist,linewidth=1,color='black',linestyle='dashed')

    line.add_label(0.1,0.1,plabel,relative=True,size='small')
    line.add_scalebar(l)
    line.scalebar.set_corner('top right')
    line.scalebar.set_label('0.5pc')
    line.recenter(ac,dc,width=0.0262,height=0.0262)
    line.set_tick_labels_font(size='x-small')
    line.set_axis_labels_font(size='small')
    if nx!=0:
        line.hide_ytick_labels()
        line.hide_yaxis_label()
    if ny!=n-1 | nx!=0:
        line.hide_xtick_labels()
        line.hide_xaxis_label()
    line.ticks.show()
    line.ticks.set_xspacing(0.0125)
    line.ticks.set_minor_frequency(5)
    line.ticks.set_color('black')
    line.tick_labels.set_font(size='x-small', weight='medium', \
                         stretch='normal', family='sans-serif', \
                         style='normal', variant='normal')
#fpeak.close()
fig.canvas.draw()
fig.savefig('./fig_paper/ori_contourall.eps')
