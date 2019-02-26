#LVG calculation
gochi>chinh2.py: LVG. input: ./data/T/co??cvlTposition.dat. output: ./data/LVGsolution/LVG_.txt. ./data/LVGsolution/SED_.txt

#rotation diagram
gord>rotdiag.py: rotation diagram。 input同上。output：./fig/RD/RD_.eps. ./data/RTsolution/...

#plot N-V and T-V.
trend.py:  input: ./data/LVGsolution/LVG_.txt and ./data/RTsolution/... . output:./fig/Nv tv.eps

#plot line ratio.
pltratio.py:  output: ./fig/ratio.eps

#plot sed at each velocity
gosed>pltsed.py: 

#plot sed in one image
pltsedall.py: 

#calculate tau
gotau>caltau.py: calculate tau


##path
#integration map
g240

#chi distribution
chifig_paper

#other figures
fig

#LVG models by nh2
LVGmodelnh2