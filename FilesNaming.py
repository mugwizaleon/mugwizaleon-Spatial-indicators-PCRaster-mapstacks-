import os
import library

SM = ['CA','MPS', 'Dist', 'PCI', 'WI', 'MPSD'] #Spatial metrics

#Spatial Units
SU = ['nondata', #0
        'Water', #1
        'settlement', #2
        'Roads', #3
        'Cropland', #4
        'Forest', #5
        'Orchard', #6
        'Wetland Non forest', #7
        'Wetland Forest', #8
        'Baresoil', #9
        'Grassland', #10
        'Subsistence'  #11
        ] 
ES = (library.ESlist ())
SI = (library.SIlist ())


def argments(input):
    if input == SI[0]:  #Area of agriculture
        classe = '4'
        Naming = SU[4]
        Metric = SM[0]
    if input == SI[1]: #Area of grassland
        classe = '10'
        Naming = SU[10]
        Metric = SM[0]
    if input == SI[2]: #Cluster size of grassland
        classe = '10'
        Naming = SU[10]
        Metric = SM[5]        
    if input == SI[3]: #Grassland cohesion
        classe = '10'
        Naming = SU[10]
        Metric = SM[3]            
    if input == SI[4]: #Distance from buit up area to area of natural water sources
        classe = '1'
        Naming = SU[1]
        Metric = SM[2]           
    if input == SI[5]: # Cluster size of vegetation cover
        classe = '5'
        Naming = 'vegetation'
        Metric = SM[1]       
    if input == SI[6]: # Forest cohesion
        classe = '5'
        Naming = SU[9]
        Metric = SM[3] 
    if input == SI[7]: # Wetness index
        classe = '99'
        Naming = SU[0]
        Metric = SM[4]       
    return (classe, Naming, Metric)
            
def FilesNames(input, Metric):
    first_four_letters = input[:4]
    Term = Metric+first_four_letters
    TiffName = '*'+Term+'*.tiff'
    RasterName = '*'+Term+'*'
    TSSName = Term+'.tss'
    FTSSName = 'F'+Term+'.tss'
    return (TiffName, RasterName, TSSName, FTSSName)
            
def GraphLabel(input):
    if input == SI[0]:  #Area of agriculture
        Title = 'Area of agriculture'
        xlabel = 'Period'
        xyabel = 'Area (ha)'
        legend1 = ' '
        legend2 = ''
    if input == SI[1]: #Area of grassland
        Title = 'Area of grassland'
        xlabel = 'Period'
        xyabel = 'Area (ha)'    
        legend1 = ' '
        legend2 = ''
    if input == SI[2]: #Cluster size of grassland
        Title = 'Clusters of grassland'
        xlabel = 'Period'
        xyabel = 'percentage (%)'
        legend1 = 'clusters fulfilling the desired state'
        legend2 = 'clusters not fulfilling the desired state'
    if input == SI[3]: #Grassland cohesion
        Title = 'Grassland cohesion'
        xlabel = 'Period'
        xyabel = 'percentage (%)'
        legend1 = ' '
        legend2 = ''
    if input == SI[4]: #Distance from buit up area to area of natural water sources
        Title = 'Location of built up areas to water resource'
        xlabel = 'Period'
        xyabel = 'percentage (%)'
        legend1 = 'Locations with dist.< 1km'
        legend2 = 'location with dis.> 1km'
    if input == SI[5]: # Cluster size of vegetation cover
        Title = 'Clusters of vegetation cover'
        xlabel = 'Period'
        xyabel = 'percentage (%)'
        legend1 = 'Vegetation cover in the landscape'
        legend2 = 'Non vegettion cover in the landscape'
    if input == SI[6]: # Forest cohesion
        Title = 'Forest cohesion'
        xlabel = 'Period'
        xyabel = 'percentage (%)'
        legend1 = ' '
        legend2 = ''
    if input == SI[7]: # Wetness index
        Title = 'Average WWI for the whole landscape'
        xlabel = 'Period'
        xyabel = 'value'
        legend1 = ' '
        legend2 = ''
    return (Title, xlabel, xyabel, legend1, legend2)            
            
