"""
@ Author : ccy865(ccy865@gmail.com)
@ Description : Change face data label to kitti label format.
@ Preparation
    - download 
        FDDB : Face Detection Data Set and Benchmark(http://vis-www.cs.umass.edu/fddb/)
    - run 
        'ellipsis_to_rectangle.py' to convert annotations in ellipsis to rectangle(https://github.com/JongsooKeum/RetinaNet-tensorflow.git)

@ Data directory
    - FDDB dataset : image(.jpg), label(.anno), label map(.json)
data
`-- face
    |-- FDDB-folds
    |-- annotations
    |-- images
    |-- originalPics
    |   |-- 2002
    |   `-- 2003
    |-- test
    |   |-- annotations
    |   |-- draws
    |   `-- images
    |-- tfrecords
    `-- train
        |-- annotations
        `-- images

    - kitti data : image(.png), label(.txt), label map(.pbtxt)
kitti
|-- data_object_image_2
|   `-- training
|       `-- image_2
|-- training
|   |-- image_2
|   `-- label_2
`-- val
    |-- images
    `-- labels
"""
import os
import math
import string

# Label path of face annotaions 
# LABEL_DIR_BASE = 'face/annotations' # For test
LABEL_DIR_BASE = '/notebooks/choicy/data/face/train/annotations'
# Location to be saved 
F2K_DIR_BASE = 'face2kitti'

str2ListWord = []
listTotal = list()
strAlparbet_Number_Dot = string.letters + string.digits + '.'

listLabelDir = os.listdir(LABEL_DIR_BASE)
for label_index, label_txt in enumerate(listLabelDir):   
    with open(LABEL_DIR_BASE + os.sep + label_txt, "r") as f1:  # load *.anno file one by one
        print(label_index, ': ', label_txt, ' is opened')
        del listTotal[:]    # list init
        while True:
            lines = f1.readline() # read line by line         
            for OneWord in lines :
                if OneWord in strAlparbet_Number_Dot :  # f
                    str2ListWord.append( OneWord )  # f,a,c,e
            strWord = ''.join( str2ListWord )   # face
            del str2ListWord[:] # list init
            if strWord:
                listTotal.append(strWord)   # ['face', '123.123', ... ]
            if not lines: break
        divCnt = int(math.ceil(len(listTotal)/5.0))
        # (For KITTI format)Add the label name after 1st bbox
        for l in range(divCnt):
            if l:
                listTotal.insert(l*5, listTotal[0]) 
        # Create KITTI format
        with open(F2K_DIR_BASE + os.sep + label_txt[:-4] +"txt", mode='wt') as f2:
            for k in range(len(listTotal)):
                if k % 5 == 0:      convert_line = listTotal[0] + ' 0.0 0 0.0 '
                elif k % 5 == 1:    convert_line = listTotal[1] + ' '
                elif k % 5 == 2:    convert_line = listTotal[2] + ' '
                elif k % 5 == 3:    convert_line = listTotal[3] + ' '
                elif k % 5 == 4:    convert_line = listTotal[4] + ' 0.0 0.0 0.0 0.0 0.0 0.0 0.0' + '\n'
                f2.write(convert_line)
            f2.close()
