from pcraster import *
from pcraster.framework import *
from osgeo import gdal, osr
from osgeo.gdalconst import *
import sys
import numpy as np  
import struct
import os,  glob
import time


gdal.AllRegister()  #Registers data formats
Table = "table1.txt"
raster_files = glob.glob('*year*.asc')
raster_files.sort()
newclassname = 'newmap'
expr = newclassname
reclas_map = 'classified'
name = " LU000000."
#name = sys.argv[1]
count = 0

def Openinginpfile (raster_file):
    dataset = gdal.Open( raster_file,  GA_ReadOnly )  
    cmd = "gdal_translate -of PCRaster -ot Int32 "+raster_file+" newmap." #I converted the input file first into PCRaster to be able to use lookup function in the next step
    os.system(cmd)
    return ()
    
def reclassMap(Table,expr, newclassname):
    expr = expr
    Table = Table
    landuseReclass = lookupnominal(Table, expr)
    report (landuseReclass,'classified' )
    return ()
    
def Myformat (reclas_map, name): 
    if count < 10:
        extension = "00" + str(count)
    else : 
        extension = "0" + str(count)
    cmd = "gdal_translate -of PCRaster -ot Int32 "+reclas_map+" "+name+extension    #This is more about writting/naming files in appropriate way
    os.system(cmd)
##    cmd = "legend -f legend2.txt "+name+extension #add a legend of land-use classes to PCRaster maps
##    os.system(cmd)
    return ()


for raster_file  in raster_files :
    Openinginpfile (raster_file)
    reclassMap(Table, expr, newclassname)
    count +=1
    Myformat(reclas_map, name)




  






