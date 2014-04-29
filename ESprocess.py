import os
import library

ES = (library.ESlist ())
SI = (library.SIlist ())

def selectprocess(input1, input2):
    A = (library.ListA()) #List of SI that ES status's improvement depends on increase of SI's value      
    B = (library.ListB()) #List of SI that ES status's improvement depends on decrease of SI's value
    L1 = (library.List1()) #List of SI to ES which process is : accessibility to water
    L2= (library.List2()) #List of ES process: production to water
    L3 = (library.List3()) #List of ES process: accessibility to timber
    L4 = (library.List4()) #List of ES process: production to wood from trees
    L5 = (library.List5()) #List of ES process: Suitable living space for wild plants and animals
    L6 = (library.List6()) #List of ES process: visitors' movement
    L7 = (library.List7()) #List of ES process: genetic material and evolution in wild plants and animals
    L8 = (library.List8()) #List of ES process: production of edible plants for humans
    L9 = (library.List9()) #List of ES process: production of edible plants for Livestock 
    L10 = (library.List10()) #List of ES process: runoff regulation  & river discharge
    L11 = (library.List11())  #List of ES process: role of vegetation root matrix and soil biota in soil retention
    L12 = (library.List12()) #List of ES process: retarditation of wind/water/mud movement
    L13 = (library.List13()) #List of ES process: influence of land cover for gravitational air movement, air purification/renewal
    L14 = (library.List14()) #List of ES process: role of nature in storage and re-cycling 
    L15 = (library.List15()) #List of ES process: visual composition for observer psychology
    if (input1 in L1) == True  and (input2 ) == ES[0] : process = 'accessibility to water'
    if (input1 in L2) == True and (input2 ) == ES[0] : process = 'production to water'
    if (input1 in L3) == True and (input2 ) == ES[1] : process ='accessibility to timber'
    if (input1 in L4) == True and (input2 ) == ES[1]: process ='production to wood from trees'
    if (input1 in L5) == True and (input2 ) == ES[2]: process ='suitable living space for wild plants and animals'
    if (input1 in L6) == True and (input2 ) == ES[2]: process ='visitors''movement'
    if (input1 in L7) == True and (input2 ) == ES[2]: process ='genetic material and evolution in wild plants and animals'
    if (input1 in L8) == True and (input2 ) == ES[3]: process ='production of edible plants for humans'
    if (input1 in L9) == True and (input2 ) == ES[4]: process ='production of edible plants for Livestock'
    if (input1 in L10) == True and (input2 ) == ES[5] : process ='runoff regulation  & river discharge'
    if (input1 in L11) == True and (input2 ) == ES[6]: process ='role of vegetation root matrix and soil biota in soil retention'
    if (input1 in L12) == True and (input2 ) == ES[7]: process ='retarditation of wind/water/mud movement'
    if (input1 in L13) == True and (input2 ) == ES[9]: process ='influence of land cover for gravitational air movement, air purification/renewal'
    if (input1 in L14) == True and (input2 ) == ES[8]: process ='role of nature in storage and re-cycling '
    if (input1 in L15) == True and (input2 ) == ES[11]: process ='visual composition for observer psychology'
    if (input1 in L15) == True and (input2 ) == ES[12]: process ='visual composition for observer psychology'
    return A, B, process
    
    
    
    
    
