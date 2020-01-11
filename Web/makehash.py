# coding=UTF-8

import urllib
import cv2
import os, sys
import numpy as np

reload(sys)
sys.setdefaultencoding('utf-8')

def makeHash(imgurl):
    img = "1.jpg"
    urllib.urlretrieve(imgurl,filename="1.jpg")
    img=cv2.imread(img,0)
    os.remove("1.jpg")

    orb = cv2.ORB_create()
    kp,des = orb.detectAndCompute(img, None)
    hash_value = str(Hash2(normalize(des.tolist())))
    return hash_value,des

def makeHash_local(img):
    img=cv2.imread(img,0)
    orb = cv2.ORB_create()
    kp,des = orb.detectAndCompute(img, None)
    hash_value = str(Hash2(normalize(des.tolist())))
    return hash_value,des

def Hash(des):
    d = des.mean(axis=0)[:3]
    s = 0
    for i in range(len(d)):
        s = s + int(d[i])
    return s/3

def normalize(data):
	res = []
	for dataelem in data:
		res += dataelem
	return res

def Hash2(des):
	proj = [971, 3400, 9828, 14359, 43436, 51965, 71529, 75900, 85581]
	C = 255
	length = len(des)
	projlength = len(proj)
	idx = 0
	hash_result = []
	for i in range(length):# 原向量的第i位
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

imgurl = "http://imgservice.suning.cn/uimg1/b2c/image/py_C58jT444wTj_l9ACClg.jpg_800w_800h_4e"
print (makeHash(imgurl))
