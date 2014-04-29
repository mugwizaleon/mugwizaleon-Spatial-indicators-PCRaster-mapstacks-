import os,  glob
from osgeo import gdal
import numpy as np
import struct
import FilesNaming

def style(filename, Mytext, dataDir ):
    directory = str(os.path.dirname(os.path.abspath(__file__)))
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
    values = []
    for index, file in enumerate(file_list):
        lc_data = gdal.Open(file)
        lc = lc_data.ReadAsArray()
        values.append(lc.max())
    Mymax = str(sorted(values)[-1])
    Myline = '    <rasterrenderer opacity="1" alphaBand="-1" classificationMax="'+Mymax+'" classificationMinMaxOrigin="User" band="1" classificationMin="1" type="singlebandpseudocolor">'

    listOfColors = ['228b22', 'ff4040','ffd700','228b22','0000ff', '00008b', '8a2be2', '8ee5ee','76ee00',
                           'ee7621', 'eead0e', 'bcee68', 'bf3eff', '1c1c1c', 'e6e6fa', 'ffaeb9',
                           'bcd2ee','8b008b','b03060', '9370db', '00fa9a', '191970', 'c0ff3e',
                           '6b8e23', 'ff4500', 'db7093', 'ffb5c5', '4169e1' ]  
                           
    with open(directory+'/MyStyle.qml', 'r') as input_file, open(os.path.join(dataDir, 'MyFile.qml') , 'w') as output_file:
        for i, line  in enumerate(input_file):
            if i == 3: 
                line = Myline
                output_file.write(line+'\n')
            elif i == 8: 
                for i, value in enumerate(values):
                    if i < len (listOfColors):
                        line = '          <item alpha="255" value="'+str(value)+'" label="'+Mytext+' '+str(value)+'" color="#'+listOfColors[i]+'"/>' 
                    output_file.write(line+'\n')
            else:
                output_file.write(line)

def eachStyle (Myfile, Mytext, file_list, dataDir):
    directory = str(os.path.dirname(os.path.abspath(__file__)))
    lc_data = gdal.Open(Myfile)
    values = []
    lc = lc_data.ReadAsArray()
    MyValue = lc.max()
    for index, file in enumerate(file_list):
        lc_data = gdal.Open(file)
        values.append(lc_data.ReadAsArray().max())        
    Myline = '    <rasterrenderer opacity="1" alphaBand="-1" classificationMax="'+str(MyValue)+'" classificationMinMaxOrigin="User" band="1" classificationMin="1" type="singlebandpseudocolor">'   
    listOfColors = ['7fffd4', 'ff4040','ffd700','228b22','0000ff', '00008b', '8a2be2', '8ee5ee','76ee00',
                           'ee7621', 'eead0e', 'bcee68', 'bf3eff', '1c1c1c', 'e6e6fa', 'ffaeb9',
                           'bcd2ee','8b008b','b03060', '9370db', '00fa9a', '191970', 'c0ff3e',
                           '6b8e23', 'ff4500', 'db7093', 'ffb5c5', '4169e1' ]  
    with open(directory+'/MyStyle.qml', 'r') as input_file, open(os.path.join(dataDir, 'MyFile.qml') , 'w') as output_file:
        for i, line  in enumerate(input_file):
            if i == 3: 
                line = Myline
                output_file.write(line+'\n')
            elif i == 8: 
                for i, value in enumerate(values):
                    if i < len (listOfColors):
                        j = values.index (MyValue)
                        line = '          <item alpha="255" value="'+str(value)+'" label="'+Mytext+' '+str(value)+'" color="#'+listOfColors[j]+'"/>' 
                        output_file.write(line+'\n')
            else:
                output_file.write(line)        

def ClusterSize (Myfile, Mytext, file_list, dataDir):
    directory = str(os.path.dirname(os.path.abspath(__file__)))
    lc_data = gdal.Open(Myfile)
    band = lc_data.GetRasterBand(1)
    xsize = band.XSize  
    ysize = band.YSize
    datatype = band.DataType
    values = band.ReadRaster( 0, 0, xsize, ysize, xsize, ysize, datatype )
    data_types ={'Byte':'B','UInt16':'H','Int16':'h','UInt32':'I','Int32':'i','Float32':'f','Float64':'d'}
    values = struct.unpack(data_types[gdal.GetDataTypeName(band.DataType)]*xsize*ysize,values)
    uniquevalues = np.unique (values)
    Myvalues = []
    for uniquevalue in uniquevalues: 
        if uniquevalue > 0:
            Myvalues.append(uniquevalue)
    lc = lc_data.ReadAsArray()
    MaxValue = lc.max()       
    Myline = '    <rasterrenderer opacity="1" alphaBand="-1" classificationMax="'+str(MaxValue)+'" classificationMinMaxOrigin="User" band="1" classificationMin="1" type="singlebandpseudocolor">'   
    listOfColors = ['40FF46', 'F50727','F5F25D']  
    with open(directory+'/MyStyle.qml', 'r') as input_file, open(os.path.join(dataDir, 'MyFile.qml') , 'w') as output_file:
        for i, line  in enumerate(input_file):
            if i == 3: 
                line = Myline
                output_file.write(line+'\n')
            elif i == 8: 
                for i, Myvalue in enumerate(Myvalues):
                    if Myvalue  > 0.32 : 
                        j = Myvalues.index (Myvalue)
                        line = '          <item alpha="255" value="'+str(Myvalue)+'" label="'+Mytext+' '+str(Myvalue)+'" color="#'+listOfColors[1]+'"/>'
                        output_file.write(line+'\n')
                    if Myvalue  == 999 : 
                        j = Myvalues.index (Myvalue)
                        line = '          <item alpha="255" value="'+str(Myvalue)+'" label="'+Mytext+' '+str(Myvalue)+'" color="#ffffff"/>'                            
                    else:
                        line = '          <item alpha="255" value="'+str(Myvalue)+'" label="'+Mytext+' '+str(Myvalue)+'" color="#'+listOfColors[0]+'"/>' 
                        output_file.write(line+'\n')
            else:
                output_file.write(line)   

def Wetness (Myfile, Mytext, file_list, dataDir):
    directory = str(os.path.dirname(os.path.abspath(__file__)))
    lc_data = gdal.Open(Myfile)
    band = lc_data.GetRasterBand(1)
    xsize = band.XSize  
    ysize = band.YSize
    datatype = band.DataType
    values = band.ReadRaster( 0, 0, xsize, ysize, xsize, ysize, datatype )
    data_types ={'Byte':'B','UInt16':'H','Int16':'h','UInt32':'I','Int32':'i','Float32':'f','Float64':'d'}
    values = struct.unpack(data_types[gdal.GetDataTypeName(band.DataType)]*xsize*ysize,values)
    uniquevalues = np.unique (values)
    Myvalues = []
    for uniquevalue in uniquevalues: 
        if uniquevalue > 0:
            Myvalues.append(uniquevalue)
    lc = lc_data.ReadAsArray()
    MaxValue = lc.max()       
    Myline = '    <rasterrenderer opacity="1" alphaBand="-1" classificationMax="'+str(MaxValue)+'" classificationMinMaxOrigin="User" band="1" classificationMin="1" type="singlebandpseudocolor">'   
    listOfColors = ['40FF46', 'F50727','ffec00']  
    with open(directory+'/MyStyle.qml', 'r') as input_file, open(os.path.join(dataDir, 'MyFile.qml') , 'w') as output_file:
        for i, line  in enumerate(input_file):
            if i == 3: 
                line = Myline
                output_file.write(line+'\n')
            elif i == 8: 
                for i, Myvalue in enumerate(Myvalues):
                    if  0 <= Myvalue <= 3 : 
                        j = Myvalues.index (Myvalue)
                        line = '          <item alpha="255" value="'+str(Myvalue)+'" label="'+Mytext+' '+str(Myvalue)+'" color="#'+listOfColors[0]+'"/>'
                        output_file.write(line+'\n')
                    if 4 < Myvalue <= 10 : 
                        j = Myvalues.index (Myvalue)
                        line = '          <item alpha="255" value="'+str(Myvalue)+'" label="'+Mytext+' '+str(Myvalue)+'" color="#'+listOfColors[2]+'"/>'    
                        output_file.write(line+'\n')
                    if 11< Myvalue<= 21 :
                        line = '          <item alpha="255" value="'+str(Myvalue)+'" label="'+Mytext+' '+str(Myvalue)+'" color="#'+listOfColors[1]+'"/>' 
                        output_file.write(line+'\n')
            else:
                output_file.write(line) 
                
def Mydistance (Myfile, Mytext, file_list, dataDir):
    directory = str(os.path.dirname(os.path.abspath(__file__)))
    lc_data = gdal.Open(Myfile)
    band = lc_data.GetRasterBand(1)
    xsize = band.XSize  
    ysize = band.YSize
    datatype = band.DataType
    values = band.ReadRaster( 0, 0, xsize, ysize, xsize, ysize, datatype )
    data_types ={'Byte':'B','UInt16':'H','Int16':'h','UInt32':'I','Int32':'i','Float32':'f','Float64':'d'}
    values = struct.unpack(data_types[gdal.GetDataTypeName(band.DataType)]*xsize*ysize,values)
    uniquevalues = np.unique (values)
    Myvalues = []
    for uniquevalue in uniquevalues: 
        if uniquevalue > 0:
            Myvalues.append(uniquevalue)
    lc = lc_data.ReadAsArray()
    MaxValue = lc.max()       
    Myline = '    <rasterrenderer opacity="1" alphaBand="-1" classificationMax="'+str(MaxValue)+'" classificationMinMaxOrigin="User" band="1" classificationMin="1" type="singlebandpseudocolor">'   
    listOfColors = ['40FF46', 'F50727','ffff00']  
    with open(directory+'/MyStyle.qml', 'r') as input_file, open(os.path.join(dataDir, 'MyFile.qml') , 'w') as output_file:
        for i, line  in enumerate(input_file):
            if i == 3: 
                line = Myline
                output_file.write(line+'\n')
            elif i == 8: 
                for i, Myvalue in enumerate(Myvalues):
                    if Myvalue  > 1 : 
                        j = Myvalues.index (Myvalue)
                        line = '          <item alpha="255" value="'+str(Myvalue)+'" label="'+Mytext+' '+str(Myvalue)+'" color="#'+listOfColors[1]+'"/>'
                        output_file.write(line+'\n')
                    if Myvalue  == 1 : 
                        j = Myvalues.index (Myvalue)
                        line = '          <item alpha="255" value="'+str(Myvalue)+'" label="'+Mytext+' '+str(Myvalue)+'" color="#'+listOfColors[2]+'"/>'                            
                    else:
                        line = '          <item alpha="255" value="'+str(Myvalue)+'" label="'+Mytext+' '+str(Myvalue)+'" color="#'+listOfColors[0]+'"/>' 
                        output_file.write(line+'\n')
            else:
                output_file.write(line)  
                
def MeanClusterSize (Myfile, Mytext, file_list, dataDir):
    directory = str(os.path.dirname(os.path.abspath(__file__)))
    lc_data = gdal.Open(Myfile)
    band = lc_data.GetRasterBand(1)
    xsize = band.XSize  
    ysize = band.YSize
    datatype = band.DataType
    values = band.ReadRaster( 0, 0, xsize, ysize, xsize, ysize, datatype )
    data_types ={'Byte':'B','UInt16':'H','Int16':'h','UInt32':'I','Int32':'i','Float32':'f','Float64':'d'}
    values = struct.unpack(data_types[gdal.GetDataTypeName(band.DataType)]*xsize*ysize,values)
    uniquevalues = np.unique (values)
    Myvalues = []
    for uniquevalue in uniquevalues: 
        if uniquevalue > 0:
            Myvalues.append(uniquevalue)
    lc = lc_data.ReadAsArray()
    MaxValue = lc.max()       
    Myline = '    <rasterrenderer opacity="1" alphaBand="-1" classificationMax="'+str(MaxValue)+'" classificationMinMaxOrigin="User" band="1" classificationMin="1" type="singlebandpseudocolor">'   
    listOfColors = ['40FF46', 'F50727','F5F25D']  

    ###########
    stripped = []
    stripper =  open("CMPSvege.tss", 'r')
    st_lines = stripper.readlines()[4:]
    stripper.close()
    for lines in st_lines:
        stripped_line = " ".join(lines.split())
        stripped.append(stripped_line)
    data = "\n".join(stripped)
    data = data.split('\n')
    MPS = []
    for row in data:
        x, y = row.split()
        MPS.append(float(y))
    print MPS
     ############   
    with open(directory+'/MyStyle.qml', 'r') as input_file, open(os.path.join(dataDir, 'MyFile.qml') , 'w') as output_file:
        for i, line  in enumerate(input_file):
            if i == 3: 
                line = Myline
                output_file.write(line+'\n')
            elif i == 8: 
                k = 0
                for i, Myvalue in enumerate(Myvalues):
                    if Myvalue  < MPS[file_list.index(Myfile)] : 
                        j = Myvalues.index (Myvalue)
                        line = '          <item alpha="255" value="'+str(Myvalue)+'" label="'+Mytext+' '+str(Myvalue)+'" color="#'+listOfColors[1]+'"/>'
                        output_file.write(line+'\n')
                    if Myvalue  == MPS[file_list.index(Myfile)] : 
                        j = Myvalues.index (Myvalue)
                        line = '          <item alpha="255" value="'+str(Myvalue)+'" label="'+Mytext+' '+str(Myvalue)+'" color="#ffffff"/>'                            
                    else:
                        line = '          <item alpha="255" value="'+str(Myvalue)+'" label="'+Mytext+' '+str(Myvalue)+'" color="#'+listOfColors[0]+'"/>' 
                        output_file.write(line+'\n')
            else:
                output_file.write(line)  


def MapstackStyle (Myfile, Mytext, file_list, dataDir):
    directory = str(os.path.dirname(os.path.abspath(__file__)))
    lc_data = gdal.Open(Myfile)
    band = lc_data.GetRasterBand(1)
    xsize = band.XSize  
    ysize = band.YSize
    datatype = band.DataType
    values = band.ReadRaster( 0, 0, xsize, ysize, xsize, ysize, datatype )
    data_types ={'Byte':'B','UInt16':'H','Int16':'h','UInt32':'I','Int32':'i','Float32':'f','Float64':'d'}
    values = struct.unpack(data_types[gdal.GetDataTypeName(band.DataType)]*xsize*ysize,values)
    uniquevalues = np.unique (values)
    Myvalues = []
    for uniquevalue in uniquevalues: 
        if uniquevalue > 0:
            Myvalues.append(uniquevalue)
    lc = lc_data.ReadAsArray()
    MaxValue = lc.max()    
    Myline = '    <rasterrenderer opacity="1" alphaBand="-1" classificationMax="'+str(MaxValue)+'" classificationMinMaxOrigin="User" band="1" classificationMin="1" type="singlebandpseudocolor">'       
    listOfColors = ['7fffd4', 'ff4040','ffd700','228b22','0000ff', '00008b', '8a2be2', '8ee5ee','76ee00',
                           'ee7621', 'eead0e', 'bcee68', 'bf3eff', '1c1c1c', 'e6e6fa', 'ffaeb9',
                           'bcd2ee','8b008b','b03060', '9370db', '00fa9a', '191970', 'c0ff3e',
                           '6b8e23', 'ff4500', 'db7093', 'ffb5c5', '4169e1' ]  
    with open(directory+'/MyStyle.qml', 'r') as input_file, open(os.path.join(dataDir, 'MyFile.qml') , 'w') as output_file:
        for i, line  in enumerate(input_file):
            if i == 3: 
                line = Myline
                output_file.write(line+'\n')
            elif i == 8: 
                for i, value in enumerate(Myvalues):
                    if i < len (listOfColors):
                       j = Myvalues.index (value)
                       line = '          <item alpha="255" value="'+str(value)+'" label="'+Mytext+' '+str(value)+'" color="#'+listOfColors[j]+'"/>' 
                       output_file.write(line+'\n')
            else:
                output_file.write(line)   
                
def style1 (filename, Mytext, dataDir, file_list ):
    directory = str(os.path.dirname(os.path.abspath(__file__)))
    values = []
    for index, file in enumerate(file_list):
        lc_data = gdal.Open(file)
    band = lc_data.GetRasterBand(1)
    xsize = band.XSize  
    ysize = band.YSize
    datatype = band.DataType
    values = band.ReadRaster( 0, 0, xsize, ysize, xsize, ysize, datatype )
    data_types ={'Byte':'B','UInt16':'H','Int16':'h','UInt32':'I','Int32':'i','Float32':'f','Float64':'d'}
    values = struct.unpack(data_types[gdal.GetDataTypeName(band.DataType)]*xsize*ysize,values)
    uniquevalues = np.unique (values)
    Myvalues = []
    for uniquevalue in uniquevalues: 
        if uniquevalue > 0:
            Myvalues.append(uniquevalue)
    lc = lc_data.ReadAsArray()
    Mymax = lc.max()   
    Myline = '    <rasterrenderer opacity="1" alphaBand="-1" classificationMax="'+str(Mymax)+'" classificationMinMaxOrigin="User" band="1" classificationMin="1" type="singlebandpseudocolor">'
    listOfColors = ['228b22', 'ff4040','ffd700','228b22','0000ff', '00008b', '8a2be2', '8ee5ee','76ee00',
                           'ee7621', 'eead0e', 'bcee68', 'bf3eff', '1c1c1c', 'e6e6fa', 'ffaeb9',
                           'bcd2ee','8b008b','b03060', '9370db', '00fa9a', '191970', 'c0ff3e',
                           '6b8e23', 'ff4500', 'db7093', 'ffb5c5', '4169e1' ]  
                           
    with open(directory+'/MyStyle.qml', 'r') as input_file, open(os.path.join(dataDir, 'MyFile.qml') , 'w') as output_file:
        for i, line  in enumerate(input_file):
            if i == 3: 
                line = Myline
                output_file.write(line+'\n')
            elif i == 8: 
                for i, value in enumerate(Myvalues):
                    if i < len (listOfColors):
                        line = '          <item alpha="255" value="'+str(value)+'" label="'+Mytext+' '+str(value)+'" color="#'+listOfColors[i]+'"/>' 
                    output_file.write(line+'\n')
            else:
                output_file.write(line)
