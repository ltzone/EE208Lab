# coding=UTF-8
import cv2
import math
import numpy as np
import urllib
import os
import stat
import glob
import sys
import json, sys

reload(sys)
sys.setdefaultencoding('utf-8')

projs = [ \
	[7, 10, 16, 21, 23, 34, 45, 48, 61, 62, 69, 77], 
	[12, 20, 23, 30, 32, 40, 57, 61, 62, 70, 78, 94], 
	[10, 14, 18, 21, 25, 33, 39, 44, 50, 67, 91, 93], 
	[13, 18, 19, 42, 52, 65, 67, 68, 71, 88, 90, 92], 
	[4, 6, 15, 23, 28, 37, 45, 46, 62, 81, 83, 93]]


def get_feature(img):
    img=cv2.imread(img,cv2.IMREAD_COLOR)

    imginfo = img.shape
    height = int(math.floor(imginfo[0]/8))
    width = int(math.floor(imginfo[1]/8))

    des = []

    for p in range(2,6):
        for q in range(2,6):
            e_b = 0.0
            e_g = 0.0
            e_r = 0.0
            h_b = 0
            h_g = 0
            h_r = 0
            for i in range(height):
                for j in range(width):
                    b,g,r = img[i+p*height,j+q*width]
                    index_b = int(b)
                    index_g = int(g)
                    index_r = int(r)
                    if index_b+index_g+index_r:
                        e_b += float(index_b)/(index_b+index_g+index_r)
                        e_g += float(index_g)/(index_b+index_g+index_r)
                        e_r += float(index_r)/(index_b+index_g+index_r)
            if e_b+e_g+e_r:
                h_b = e_b/(e_b+e_g+e_r)
                h_g = e_g/(e_b+e_g+e_r)
                h_r = e_r/(e_b+e_g+e_r)
            for i in [h_b, h_g, h_r]:
                if i < 0.31:
                    des.append(0)
                elif i > 0.355:
                    des.append(2)
                else:
                    des.append(1)

    return des

def LSHash(des,proj):
	C = 2
	length = len(des)
	projlength = len(proj)
	idx = 0
	hash_result = []
	for i in range(length):
		i_proj = []
		while (proj[idx]<=(i+1)*C):
			i_proj.append(proj[idx]-i*C-1)
			idx += 1       # 获取第i位中需要的投影数
			if (idx >= projlength):
				break
		for i_proj_elem in i_proj:  # 计算第i位投影hamming code，加入哈希结果
			if des[i] > i_proj_elem:
				hash_result.append(1)
			else:
				hash_result.append(0)
		if (idx >= projlength):  # proj已经遍历完，退出
			break
	# hamming code转二进制
	sum = 0
	multi = 1
	for x in hash_result:
		sum += multi*x
		multi*=2
	return sum

def getUrl(path,filename):
    f = open(os.path.join(path,filename), 'r')
    f = f.readlines()
    url = f[1].strip()
    imgurl = f[2].strip()
    return url,imgurl

def get_feature_Local(img):
    img=cv2.imread(img,cv2.IMREAD_COLOR)

    imginfo = img.shape
    height = int(math.floor(imginfo[0]/8))
    width = int(math.floor(imginfo[1]/8))

    des = []

    for p in range(2,6):
        for q in range(2,6):
            e_b = 0.0
            e_g = 0.0
            e_r = 0.0
            h_b = 0
            h_g = 0
            h_r = 0
            for i in range(height):
                for j in range(width):
                    b,g,r = img[i+p*height,j+q*width]
                    index_b = int(b)
                    index_g = int(g)
                    index_r = int(r)
                    if index_b+index_g+index_r:
                        e_b += float(index_b)/(index_b+index_g+index_r)
                        e_g += float(index_g)/(index_b+index_g+index_r)
                        e_r += float(index_r)/(index_b+index_g+index_r)
            if e_b+e_g+e_r:
                h_b = e_b/(e_b+e_g+e_r)
                h_g = e_g/(e_b+e_g+e_r)
                h_r = e_r/(e_b+e_g+e_r)
            for i in [h_b, h_g, h_r]:
                if i < 0.31:
                    des.append(0)
                elif i > 0.355:
                    des.append(2)
                else:
                    des.append(1)

    return des

det = get_feature_Local("static/userupload/try.jpg")
print det
for i in range(5):
	print LSHash(det,projs[i])