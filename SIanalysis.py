import sys
import library
    
def TargetValues (SpatialIndicator):
    SI = (library.SIlist ())
    
    if SpatialIndicator == SI[0] :
        Actual = 273425
        TVal = (Actual *  0.14)+Actual  #ha for crop production
    if SpatialIndicator == SI[1] :
        Actual = 778175
        TVal = (Actual *  0.7)+Actual #ha for fodder production
    if SpatialIndicator == SI[2] :
        Actual = 7350
        TVal = (Actual *  0.7)+Actual #ha for fodder production
    if SpatialIndicator in [SI[3], SI[6], SI[5]]  :
        TVal = 100
    if SpatialIndicator == SI[4] :
        TVal = 1
    if SpatialIndicator == SI[7] :
        TVal = 0
    return TVal
###################################################

