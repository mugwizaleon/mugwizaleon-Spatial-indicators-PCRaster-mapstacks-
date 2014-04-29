from osgeo import gdal
import matplotlib
import matplotlib.pyplot as plt
import glob
import numpy as np
import sys


Naming = sys.argv[1]
first_four_letters = Naming[:4]
filename = sys.argv[2]+first_four_letters
file_list =  glob.glob('**'+filename+'**')
file_list.sort()
for index in file_list:
    if index.endswith(".tiff"):
        file_list.remove(index)
for index in file_list:
    if index.endswith(".xml"):
        file_list.remove(index)
for index in file_list:
    if index.endswith(".tss"):
        file_list.remove(index)
period = 2005
values = []
for index, file in enumerate(file_list):
    lc_data = gdal.Open(file)
    lc = lc_data.ReadAsArray()
    values.append(lc.max())
    masked_array=np.ma.masked_where(lc==-2147483647, lc )
    cmap = matplotlib.cm.jet
    cmap.set_bad('w',1.)
    fig = plt.figure(str(file))
    fig.suptitle('Year '+str(period), fontsize=20)
    plt.imshow (masked_array, interpolation='none', vmin=0, cmap=cmap)
    plt.colorbar(ticks=[0,lc.max()], format='%0.2f')
    plt.axis('off')
    ax = fig.add_subplot(111)
    ax.patch.set_alpha(0.5)
    plt.savefig(str(file)+'.tiff', transparent = True)
#    plt.show()
    period = period + 1
#    return values
###################################################
##i = 0
##period = 2005
##increase=[]
##decrease=[]
##stable=[]
##for value in values:
##    period = period + 1
##    if values[i+1] > values[0] : increase.append(period)
##    if values[i+1] < values[0] : decrease.append(period) 
##    if values[i+1] == values[0] : stable.append(period)
##    i = i+1
##    if i == len(values)-1: break 
##
####if len(increase)!= 0: print "during"+str(increase)+"ES are will imporove ", values.index(value) Pour memoire
##if len(increase)!= 0: print "during"+str(increase)+"ES are will imporove "
##if len(decrease)!= 0:print  "during"+str(decrease)+"ES provision will degrade "
##if len(stable)!= 0: print "during"+str(stable)+"ES provision will stay stable"
    
    
