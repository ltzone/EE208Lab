import cv2
import numpy as np
import os
import glob

f = open("brands.txt",'r')
brands = f.read().split()
f.close()

traning = []
note = []
MIN_MATCH_COUNT = 150

# the search image
img = "2.jpg"

detector = cv2.xfeatures2d.SIFT_create()

flannParam = dict(algorithm = 0,tree = 5)
flann = cv2.FlannBasedMatcher(flannParam,{})

QueryImgBGR=cv2.imread(img)
QueryImg=cv2.cvtColor(QueryImgBGR,cv2.COLOR_BGR2GRAY)
QueryImg = cv2.GaussianBlur(QueryImg, (3, 3), 0)
queryKP,queryDesc=detector.detectAndCompute(QueryImg,None)

scores = []

for brand in brands:
    note = []
    trainImg = []
    score = 0.0
    for filename in glob.glob('logo_images/%s/*' %brand):
        im = cv2.imread(filename,0)
        im = cv2.GaussianBlur(im, (3,3), 0)
        trainImg.append(im)
        note.append(filename)
    for num in range(len(note)):
        trainKP,trainDesc=detector.detectAndCompute(trainImg[num],None)
        h,w=trainImg[num].shape
        matches=flann.knnMatch(queryDesc,trainDesc,k=2)
        goodMatch=[]
        for m,n in matches:
            if(m.distance<0.75*n.distance):
                goodMatch.append(m)
        #print(note[num], len(goodMatch))
        score = score+ len(goodMatch)
    if len(note):
        scores.append(score/len(note))
    else:
        scores.append(0)

print(brands[scores.index(max(scores))])

