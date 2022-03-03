import os
import sys
from pypcd import pypcd
from io import StringIO
import open3d as o3d
import numpy as np
import shutil
import struct
import pickle
import os.path
r"./txt2bin/txt/"

##root directory where raw file is stored in pcd file
pcd_raw_dirroot = r"./file/raw_pcd/"
##root for ACII pcd directory
pcd_ascii_dirroot = r"./file/ascii_pcd/"
##root directory for txt file
txt_dirroot = r"./file/txt/"
##root directory where bin file will be stored
bin_dirroot = r"./file/bin/"
##root directory where bin file will be stored
binary_reader_dirroot = r"./file/inside-.pcd.bin/"

##change pcd-binary into ASCII-format
raw_pcd_files = sorted( filter( lambda x: os.path.isfile(os.path.join(pcd_raw_dirroot, x)), os.listdir(pcd_raw_dirroot) ) )
for raw_pcd_file_name in raw_pcd_files:
     print("converting... " + raw_pcd_file_name + " from.. " + pcd_raw_dirroot)
     raw_pcd = pypcd.PointCloud.from_path(os.path.join(pcd_raw_dirroot,raw_pcd_file_name))
     raw_pcd.save(os.path.join(pcd_ascii_dirroot,raw_pcd_file_name))

#copy the ASCII-pcd file into a txt directory
ascii_pcd_files = sorted( filter( lambda x: os.path.isfile(os.path.join(pcd_ascii_dirroot , x)), os.listdir(pcd_ascii_dirroot) ) )
for ascii_pcd_file_name in ascii_pcd_files:
     # construct full file path
     source_ascii = pcd_ascii_dirroot + ascii_pcd_file_name
     destination = txt_dirroot + ascii_pcd_file_name
     shutil.copyfile(source_ascii, destination)
     print('copied', ascii_pcd_file_name)

#change extension the file in txt directory into .txt.
txt_pcd_files = sorted( filter( lambda x: os.path.isfile(os.path.join(txt_dirroot , x)), os.listdir(txt_dirroot) ) )
for txt_pcd_file_name in txt_pcd_files:
     pre, ext = os.path.splitext(txt_pcd_file_name)
     source_txt = txt_dirroot + txt_pcd_file_name
     os.rename(source_txt, txt_dirroot + pre + ".txt")
     print('renamed', txt_pcd_file_name)

#read the txt file and create a bin file with extension .pcd.bin
for txt_file_name in os.listdir(txt_dirroot):
    print ("converted to bin file: "+ txt_file_name)
    #print name of the text file
    if txt_file_name.split('.')[-1]!='txt':
        continue

    bin_file_name=txt_file_name.split('.txt')[0] +'.pcd.bin'
   
    txt_file=open(txt_dirroot + txt_file_name,'r') 
    bin_file=open(bin_dirroot + bin_file_name,'wb')

    lines=txt_file.readlines()
    for j,line in enumerate(lines):
        if j in range (0,10):
            continue
        curLine=line.split(' ')[0:3]                    
        #curLine.append(line.split(' ')[3])              
        for i in range(len(curLine)):
            #if len(curLine[i])==0:
                #continue
            if i == 3:                                                
                parsedata = struct.pack("f",float(curLine[i]))        
                # parsedata = struct.pack("i",int(curLine[i]))

                bin_file.write(parsedata)
            else:                                                     
                parsedata = struct.pack("f",float(curLine[i]))         
                bin_file.write(parsedata)

    bin_file.close()
    txt_file.close()

#-----------------------------------------------------------
#this is not necessary unless needed.
#to read what inside the binary file.
np.set_printoptions(threshold=sys.maxsize,linewidth=100,)
for bin_file_name in os.listdir(bin_dirroot):
     #print ("reading bin file.....")
     sys.stdout = open(binary_reader_dirroot + bin_file_name +".txt", "w")
     source_bin = bin_dirroot + bin_file_name
     with open(source_bin, 'rb') as f:
         data = np.fromfile(f, dtype=np.float32)
         array_size=data.size/4
         num = int(array_size)
         array = np.reshape(data, [num, 4])
         print(array)
         #print(np.frombuffer(array))
     sys.stdout.close()