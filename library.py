import os

def ESlist():
    ES = [
            "Crop production",                              #0  
            "Fodder production",                     #1   
            "Accessibility to water ",      #2  
            "Erosion control"      #3
            ]                   
            
    return ES
    
def SIlist():
    SI = [
          "Area of agriculture",                      #0
          "Area of grassland",                #1
          "Cluster size of grassland",            #2
          "Grassland cohesion",            #3
          "Distance from buit up area to area of natural water sources",  #4
          "Cluster size of vegetation",            #5
          "Forest cohesion",     #6
          "Wetness index",  #7
          ]
    return SI

def ListA(): #List of SI that ES status's improvement depends on increase of SI's value
    SI = SIlist()
    A = [SI[18],SI[10],SI[1], SI[4], SI[12], SI[11], SI[14], SI[2], SI[5], SI[13], SI[0], SI[3]]
    return A

def ListB(): #List of SI that ES status's improvement depends on decrease of SI's value
    SI = SIlist()
    B = [SI[8],SI[15],SI[16],SI[7],SI[17],SI[20],SI[6],SI[9]]
    return B
    
def List1(): #List of SI to ES which process is : accessibility to water
    SI = SIlist()
    L1 = [SI[8]]
    return L1    

def List2(): #List of SI to ES which process is : accessibility to water
    SI = SIlist()
    L2 = [SI[18], SI[15]]
    return L2

def List3(): #List of SI to ES which process is : accessibility to timber
    SI = SIlist()
    L3 = [SI[10]]
    return L3

def List4(): #List of SI to ES which process is : production to wood from trees
    SI = SIlist()
    L4 = [SI[1], SI[4], SI[12], SI[16]]
    return L4
 
def List5(): #List of SI to ES which process is : suitable living space for wild plants and animals
    SI = SIlist()
    L5 = [SI[4], SI[10]]
    return L5

def List6(): #List of SI to ES which process is : visitors' movement
    SI = SIlist()
    L6 = [SI[7], SI[6], SI[9]]
    return L6
    
def List7(): #List of SI to ES which process is : genetic material and evolution in wild plants and animals
    SI = SIlist()
    L7 = [SI[11], SI[14], SI[17]]
    return L7

def List8(): #List of SI to ES which process is : production of edible plants for humans
    SI = SIlist()
    L8 = [SI[0], SI[3], SI[22]]
    return L8

def List9(): #List of SI to ES which process is : production of edible plants for Livestock
    SI = SIlist()
    L9 = [SI[2], SI[5], SI[13], SI[14], SI[22]]
    return L9

def List10(): #List of SI to ES which process is : runoff regulation  & river discharge
    SI = SIlist()
    L10 = [SI[18]]
    return L10

def List11(): #List of SI to ES which process is : role of vegetation root matrix and soil biota in soil retention
    SI = SIlist()
    L11 = [SI[14], SI[1], SI[23]]
    return L11

def List12(): #List of SI to ES which process is : retarditation of wind/water/mud movement
    SI = SIlist()
    L12 = [SI[4], SI[12], SI[5], SI[13], SI[20]]
    return L12
    

def List13(): #List of SI to ES which process is : influence of land cover for gravitational air movement, air purification/renewal
    SI = SIlist()
    L13 = [SI[14]]
    return L13
    
def List14(): #List of SI to ES which process is : role of nature in storage and re-cycling
    SI = SIlist()
    L14 = [SI[15], SI[17], SI[23]]
    return L14

def List15(): #List of SI to ES which process is : visual composition for observer psychology
    SI = SIlist()
    L15 = [SI[10], SI[11], SI[17], SI[16]]
    return L15
