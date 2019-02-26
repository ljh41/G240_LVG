import numpy as np
import matplotlib.pyplot as plt

#data
positionblue = 'pointdishbgaussian'
positionred = 'pointdishrgaussian'
path = './data/T/'
fda21blue = np.loadtxt(path+'co21ficvlT'+positionblue+'.dat')
fda32blue = np.loadtxt(path+'co32_smcvlT'+positionblue+'.dat')
fda65blue = np.loadtxt(path+'co65_smmaskcvlT'+positionblue+'.dat')
fda76blue = np.loadtxt(path+'co76_smmaskcvlT'+positionblue+'.dat')
n21blue = fda21blue.shape[0]
n32blue = fda32blue.shape[0]
n65blue = fda65blue.shape[0]
n76blue = fda76blue.shape[0]
velblue = fda65blue[:,0]

fda21red = np.loadtxt(path+'co21ficvlT'+positionred+'.dat')
fda32red = np.loadtxt(path+'co32_smcvlT'+positionred+'.dat')
fda65red = np.loadtxt(path+'co65_smmaskcvlT'+positionred+'.dat')
fda76red = np.loadtxt(path+'co76_smmaskcvlT'+positionred+'.dat')
n21red = fda21red.shape[0]
n32red = fda32red.shape[0]
n65red = fda65red.shape[0]
n76red = fda76red.shape[0]
velred = fda65red[:,0]

#ratio
r61bluearr = []
r62bluearr = []
r75bluearr = []
vel61blue = []
vel62blue = []
vel75blue = []
for i in range(n21blue):
    r61 = 0
    r62 = 0
    r75 = 0
    obs65 = 0.
    vel = fda21blue[i,0]
    obs21 = fda21blue[i,1]
    for j in range(n65blue):
        if abs(vel-fda65blue[j,0])<0.01:
            obs65 = fda65blue[j,1]
            r61 = obs65/obs21
            r61bluearr = r61bluearr + [r61]
            vel61blue = vel61blue + [vel]
    if abs(obs65)<0.01:
        continue
    for j in range(n32blue):
        if abs(vel-fda32blue[j,0])<0.01:
            obs32 = fda32blue[j,1]
            r62 = obs65/obs32
            r62bluearr = r62bluearr + [r62]
            vel62blue = vel62blue + [vel]
    for j in range(n76blue):
        if abs(vel-fda76blue[j,0])<0.01:
            obs76 = fda76blue[j,1]
            r75 = obs76/obs65
            r75bluearr = r75bluearr + [r75]
            vel75blue = vel75blue + [vel]
#    end
r61bluearr = np.array(r61bluearr)
r62bluearr = np.array(r62bluearr)
r75bluearr = np.array(r75bluearr)
vel61blue = np.array(vel61blue)
vel62blue = np.array(vel62blue)
vel75blue = np.array(vel75blue)

r61redarr = []
r62redarr = []
r75redarr = []
vel61red = []
vel62red = []
vel75red = []
for i in range(n21red):
    r61 = 0
    r62 = 0
    r75 = 0
    obs65 = 0.
    vel = fda21red[i,0]
    obs21 = fda21red[i,1]
    for j in range(n65red):
        if abs(vel-fda65red[j,0])<0.01:
            obs65 = fda65red[j,1]
            r61 = obs65/obs21
            r61redarr = r61redarr + [r61]
            vel61red = vel61red + [vel]
    if abs(obs65)<0.01:
        continue
    for j in range(n32red):
        if abs(vel-fda32red[j,0])<0.01:
            obs32 = fda32red[j,1]
            r62 = obs65/obs32
            r62redarr = r62redarr + [r62]
            vel62red = vel62red + [vel]
    for j in range(n76red):
        if abs(vel-fda76red[j,0])<0.01:
            obs76 = fda76red[j,1]
            r75 = obs76/obs65
            r75redarr = r75redarr + [r75]
            vel75red = vel75red + [vel]
#    end
r61redarr = np.array(r61redarr)
r62redarr = np.array(r62redarr)
r75redarr = np.array(r75redarr)
vel61red = np.array(vel61red)
vel62red = np.array(vel62red)
vel75red = np.array(vel75red)

#plot

plt.figure(0)
plt.plot(67.5-vel61blue,r61bluearr,'b^',label='6-5/2-1 blue lobe',markerfacecolor='white',markeredgecolor='blue',markersize=10)
plt.plot(vel61red-67.5,r61redarr,'r^',label='6-5/2-1 red lobe',markerfacecolor='white',markeredgecolor='red',markersize=10)
plt.plot(67.5-vel62blue,r62bluearr,'bx',label='6-5/3-2 blue lobe',markerfacecolor='white',markeredgecolor='blue',markersize=10,zorder=50)
plt.plot(vel62red-67.5,r62redarr,'rx',label='6-5/3-2 red lobe',markerfacecolor='white',markeredgecolor='red',markersize=10,zorder=50)
plt.plot(67.5-vel75blue,r75bluearr,'bs',label='7-6/6-5 blue lobe',markerfacecolor='white',markeredgecolor='blue',markersize=10)
plt.plot(vel75red-67.5,r75redarr,'rs',markerfacecolor='white',markeredgecolor='red',label='7-6/6-5 red lobe',markersize=10)

#plt.legend()
#plt.plot([6,6],[0,100],'k--')
plt.plot(22.3,1.6,'b^',markeredgecolor='blue',markerfacecolor='white',markersize=10)
plt.plot(22.3,1.7,'bx',markeredgecolor='blue',markerfacecolor='white',markersize=10)
plt.plot(22.3,1.8,'bs',markersize=10,markeredgecolor='blue',markerfacecolor='white')
plt.plot(23,1.6,'r^',markersize=10,markerfacecolor='white')
plt.plot(23,1.7,'rx',markersize=10,markerfacecolor='white')
plt.plot(23,1.8,'rs',markersize=10,markerfacecolor='white')
plt.text(23.5,1.575,'6--5/2--1')
plt.text(23.5,1.675,'6--5/3--2')
plt.text(23.5,1.775,'7--6/6--5')

plt.minorticks_on()
plt.xlabel('$V_{\mathrm{outflow}}$ (km s$^{-1}$)')
plt.ylabel('Line ratios')
#    plt.legend(loc='upper left')
#plt.title(position)
plt.axis([6,26,0.3,2.0])
plt.savefig('./fig/ratio.eps')
plt.close()
