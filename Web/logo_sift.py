import cv2
import numpy as np
import os
import glob

def logo_recognition(img):

    brands = ["dell", "hp", "sony", "lenovo", "apple", "beats", "ibm", "jbl", "nikon", "ThinkPad", "HUAWEI", "Microsoft", "acer", "aigo", "asus", "casio", "htc", "logitec"]

    # the search image

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
        for filename in glob.glob('../logo_recognition/logo_images/%s/*' %brand):
            im = cv2.imread(filename,0)
            im = cv2.GaussianBlur(im, (3,3), 0)
            trainImg.append(im)
            note.append(filename)
        for num in range(len(note)):
            trainKP,trainDesc=detector.detectAndCompute(trainImg[num],None)
            matches=flann.knnMatch(queryDesc,trainDesc,k=2)
            goodMatch=[]
            for m,n in matches:
                if(m.distance<0.75*n.distance):
                    goodMatch.append(m)
            print(note[num], len(goodMatch))
            score = score+ len(goodMatch)
        if (len(note)!=0):
            scores.append(score/len(note))

    print(scores)
    print(brands[scores.index(max(scores))])
    return brands[scores.index(max(scores))]


