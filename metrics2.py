from pcraster import *
from pcraster.framework import *
from osgeo import gdal, osr
from osgeo.gdalconst import *
import string
from itertools import cycle
import sys
import numpy as np  
import struct
import struct
import os,  glob
import os.path, time

Spatialmetrics = ['CA','MPS' ]

# Rule for output files names

def classarea(landuse):
    conversionfactor = scalar(10000.0)
    landuseArea = areaarea(landuse) /   conversionfactor #conveting area units into ha from m2
    return landuseArea
    
def MeanPatchSize(landuse):
    conversionfactor = scalar(10000.0)
    landuseArea = classarea(landuse) #conveting area units into ha from m2
    Patch = clump( landuse) #Contiguous groups of cells with the same value
    Npatches = mapmaximum(scalar(Patch))
    Npatches = cellvalue(Npatches, 0, 0)
    Npatches = int(Npatches[0])
    print 'number of patches:',  Npatches
    MPS = landuseArea / scalar (Npatches)
    return MPS
    
def areaAround(expr):
    areaAround = windowdiversity(expr, 5000) #  identify places where together forest and settlemet are available within 5km square 
    return areaAround

def distance (classes):
    Result = extentofview (classes, 4) #nearest distance in meters
    ENND = Result / 4
    return ENND

class MyFirstModel(DynamicModel):
    def __init__(self):
        DynamicModel.__init__(self)
        setclone('clone.map')

    def initial(self):
        print "running the initial"
        self.classe = int(sys.argv[1])
        Naming = sys.argv[2]
        self.first_four_letters = Naming[:4]
        self.areaTss=TimeoutputTimeseries(sys.argv[3]+self.first_four_letters, self,"loc2.map",noHeader=False)
        

    def dynamic(self):
        timeStep = self.currentTimeStep ()
        landuse = self.readmap("LU")
        print 'running the dynamic for time step:',  timeStep
        SpatUnit = ifthen(landuse==self.classe, landuse) #selecting the target spatial unit from the landscape
        
        if sys.argv[3] == 'CA':
            #    here  the metrc "class area": 
            self.report (nominal(classarea(SpatUnit)), sys.argv[3]+self.first_four_letters) # Agriculture surface area
            self.report ((ifthenelse(landuse==self.classe, landuse, 0)), 'Surf'+self.first_four_letters) #Agriculture surface
            self.areaTss.sample(mapmaximum(classarea(SpatUnit))) #Maximum  agriculture surface area in Graph

        if sys.argv[3] == 'MPS':
            #    here call the metrc functions "Mean Patch Size":        
            MPS = MeanPatchSize (ifthen(landuse==self.classe, landuse)) #for Agriculture area
            self.report ((ifthenelse(landuse== self.classe, nominal(MPS), 0)), sys.argv[3]+self.first_four_letters)
            self.areaTss.sample(mapmaximum(MPS)) #MPS in Graph
            
        if sys.argv[3] == 'ENND':    
        #    here call the metrc functions "distance from buitup area to":
            map1 = ifthenelse(landuse==self.classe, landuse, 0) 
            map2 = ifthenelse(landuse==2, landuse, 0) 
            classes = scalar(map1) + scalar(map2)
            MyMaps = ifthen(classes != 0, classes)
            ENND = distance(nominal(MyMaps))
##            self.report (nominal(ENND), "classes")
            MapToview = ifthenelse(landuse==self.classe, ENND, 0)
            self.report (nominal(MapToview), sys.argv[3]+self.first_four_letters)
            self.areaTss.sample(mapmaximum(ENND)) #ENND in Graph

        if sys.argv[3] == 'AAB':  
            map1 = ifthenelse(landuse==self.classe, landuse, 0) 
            map2 = ifthenelse(landuse==2, landuse, 0) 
            classes = scalar(map1) + scalar(map2)            
###            self.report (nominal(classes), sys.argv[3]+self.first_four_letters)
            self.report (nominal(classes), "classes")
            Result = areaAround (nominal(ifthen(classes != 0, classes))) #  identify places where together forest and settlemet are available within 5km square 
            Result1 = ifthen(Result==2, Result) 
            Result2 = (Result1 * 0)+ classes  #identify  spatil units in the neighbourhood
###            self.report (nominal(Result2), "Result2")
            Result3 = nominal(ifthen(Result2==self.classe, Result2)) #stay only with the forest
            Result4 = classarea(Result3) #area of the forest in the neibhourhood
            self.areaTss.sample(mapmaximum (Result4)) # Graph
            
nrOfTimeSteps= 4
myModel = MyFirstModel()
dynamicModel = DynamicFramework(myModel,nrOfTimeSteps)
dynamicModel.run()

