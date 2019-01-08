# -*- coding: utf-8 -*-
"""
@ Author : ccy865(ccy865@gmail.com)
@ Description : Change face images to kitti images name format.
@ Preparation
    - download 

    - run 
"""
import os
import math
import string
import shutil
import sys
# IMAGE_DIR_BASE = '/home/edu/RetinaNet-tensorflow-master/cvt_face2kitti/facekitti/data_object_image_2/training/images_2/'
IMAGE_DIR_BASE = '/notebooks/choicy/kitti/data_object_image_2/training/images_2/'
# IMAGE_DIR_BASE = '/home/edu/RetinaNet-tensorflow-master/cvt_face2kitti/face/image/'  # TODO Modified your directory path
# F2K_DIR_BASE = '/notebooks/choicy/cvt_face2kitti/imgNameCvt_f2k/'	# TODO Modified your directory path
F2K_DIR_BASE = '/notebooks/choicy/imgNameCvt_f2k/'	# TODO Modified your directory path
strZero = '000000'

listImageDir = os.listdir(IMAGE_DIR_BASE)

def _main():
	for img_idx, filename in enumerate(listImageDir):
		if filename.endswith("jpg"):
			fromImgPathName = IMAGE_DIR_BASE + filename
			stImgIdx = str(img_idx)

			if not len(stImgIdx) == 6:	# Fit in kitti format
				addZero = 6 - len(stImgIdx)
				totalImgIdx = strZero[:addZero] + stImgIdx
			
			toImgPathName = F2K_DIR_BASE + filename.replace(filename[:-4], totalImgIdx)	# rename
			P = shutil.copy(fromImgPathName, toImgPathName)	# copy file

if __name__ == '__main__':
    _main()