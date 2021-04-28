# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 20:22:49 2021

@author: Mustvvvics
"""

import cv2
import os
import numpy as np
# from matplotlib import pyplot as plt
from clear_screen import clear
import time

# def cameraInitialization():
CV_CAP_PROP_FRAME_WIDTH = 3
CV_CAP_PROP_FRAME_HEIGHT = 4
CV_CAP_PROP_FPS = 5
CV_CAP_PROP_FOURCC = 6


RealyHighMax = 13
CameraHighMax = 321

name = 0
cap = cv2.VideoCapture(name) #打开内置摄像头

# cap.set(CV_CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(CV_CAP_PROP_FPS, 1)

frameWidth = 640
frameHeight = 480

cap.set(cv2.CAP_PROP_FRAME_WIDTH, frameWidth) #设置窗体 1920 * 1080 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frameHeight)

ratioWindowsHeight = 1
ratioWindowsWidth = 0.6
windowsWidth = int(frameWidth * ( 0.5 - ratioWindowsWidth / 2 )), int(frameWidth * ( 0.5 + ratioWindowsWidth / 2 ))
windowsHeight = int(frameHeight * ( 0.5 - ratioWindowsHeight / 2 )), int(frameHeight * ( 0.5 + ratioWindowsHeight / 2 ))
# print(f"windowsSize {windowsHeight, windowsWidth}")

# cap.set(cv2.CAP_PROP_FRAME_WIDTH,16 * 70) #设置窗体 1920 * 1080 
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT,9 * 70)

# img : (768,1024,3)

def CalculationHigh(h):
        if h > 0 :
                high =  (RealyHighMax / CameraHighMax) * h
        else:
                high = 0
        return high

def Calculation(cnt):

        M=cv2.moments(cnt)
        # cx=int(M['m10']/M['m00'])#轮廓contour的质心的横坐标
        # cy=int(M['m01']/M['m00'])#轮廓contour的质心的纵坐标
        
        area=cv2.contourArea(cnt)#面积
        
        x, y, w, h = cv2.boundingRect(cnt)#x，y是矩阵左上点的坐标，w，h是矩阵的宽和高

        # print("质心x：",cx)
        # print("质心y：",cy)
        print("面积：",area)
        print("左上角坐标x：",x)
        print("左上角坐标y：",y)
        print("矩形宽 w：",w)
        print("矩形高 h：",h)

def ShowContours(img):
        # ret , thresh1 = cv2.threshold(img,90,255,cv2.THRESH_BINARY)
        # ret , thresh2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)    
        # ret , thresh3 = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
        # ret , thresh4 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO)
        # ret , thresh5 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO_INV)
        
        # titles = ['original image','Binary','binary-inv','trunc','tozero','tozero-inv']
        # images = [img,thresh1,thresh2,thresh3,thresh4,thresh5]
        # cv2.imshow(titles[1], images[1])
        # cv2.imshow(titles[2], images[2])
        # cv2.imshow(titles[3], images[3])
        # cv2.imshow(titles[4], images[4])
        # cv2.imshow(titles[5], images[5])


        #show contours
        imggray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # cv2.cvtColor(src, code[, dst[, dstCn]])
        # src:它是要更改其色彩空间的图像
        # code:它是色彩空间转换代码。
        # dst:它是与src图像大小和深度相同的输出图像。它是一个可选参数。
        # dstCn:它是目标图像中的频道数。如果参数为0，则通道数自动从src和代码得出。它是一个可选参数。
        # 返回值：它返回一个图像。

        ret,thresh=cv2.threshold(imggray,50,255,0)#简单阈值 黑色识别
        # ret,thresh=cv2.threshold(imggray,127,255,0)
        #第一个原图像，第二个进行分类的阈值，第三个是高于（低于）阈值时赋予的新值，第四个是一个方法选择参数，常用的有
        #cv2.THRESH_BINARY（黑白二值）
        # cv2.THRESH_BINARY_INV（黑白二值反转）
        # cv2.THRESH_TRUNC （得到的图像为多像素值）
        # cv2.THRESH_TOZERO
        # cv2.THRESH_TOZERO_INV

        imgimg,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)#用来绘制轮廓
        #cv2.findContours(image, mode, method[, contours[, hierarchy[, offset ]]])  
        #第一个参数是原始图像，第二个参数是轮廓，一个python列表，第三个参数是轮廓的索引 
        #输出：第一个是图像，第二个是我们的轮廓，第三个输出名字是hierarchy 
        # opencv2返回两个值：contours：hierarchy。注:opencv3会返回三个值,分别是img, countours, hierarchy
        # 需要直线时，找到两个端点即可。cv2.CHAIN_APPROX_SIMPLE可以实现。它会将轮廓上的冗余点去掉，压缩轮廓，从而节省内存开支。
        
        # img1 = cv2.drawContours(img,contours,-1,(0,255,0),5)  # img为三通道才能显示轮廓 RGB

        # img2 = cv2.drawContours(img,contours,0,(0,0,0),5)  # img为三通道才能显示轮廓
        # img3 = cv2.drawContours(img,contours,1,(0,255,0),5)  # img为三通道才能显示轮廓
        # img4 = cv2.drawContours(img,contours,2,(205,85,85),5)  # img为三通道才能显示轮廓
        # 第一个参数是指明在哪幅图像上绘制轮廓，第二个参数是轮廓本身，在Python中是一个list。
        #第三个参数指定绘制轮廓list中的哪条轮廓，如果是-1，则绘制其中的所有轮廓
        #第四个参数，轮廓颜色
        # 第五个参数thickness为轮廓的线宽，如果为负值或CV_FILLED表示填充轮廓内部
        # 第六个参数lineType为线型
        # 第七个参数为轮廓结构信息


        # cnt0=contours[0] 
        # cnt1=contours[1] 

        # print("the contours[0]")#
        # Calculation(cnt0)
        # print("the contours[1]")#
        # Calculation(cnt1)
        clear() #清屏

        # print("contours",len(contours))
        for cnt in contours:
                # print(cv2.contourArea(cnt))
                if (cv2.contourArea(cnt) > 3000) and (cv2.contourArea(cnt) < 50000):
                        # draw a rectangle around the items
                        x,y,w,h = cv2.boundingRect(cnt)
                        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0),3)
                        print("左上角坐标x：",x)
                        print("左上角坐标y：",y)
                        print("矩形宽 w：",w)
                        print("矩形高 h：",h)
                        print("液体高度：",'%.4f' % CalculationHigh(h),"cm")
                        # return CalculationHigh(h)

        cv2.imshow("-1", img)
        # cv2.imshow("0", img2)
        # cv2.imshow("1", img3)
        # cv2.imshow("2", img4)
        #end of show contours
        
         

# cameraInitialization()

while(1):
        ret,img = cap.read() #实时读取图像
        # print(f"img shape {img.shape}")
        # img h*w*3

        img = img[ windowsHeight[0] : windowsHeight[1], windowsWidth[0] : windowsWidth[1]]
        # print(img.shape)

        # print("img shape",img.shape)
        # print("img",img)
        # start1 = time.time()
        ShowContours(img)
        # end1 = time.time()
        # print("ShowContours time",end1-start1)


        k = cv2.waitKey(5)
        if (k == ord('q')):
                break
        elif(k == ord('s')):
                #name = input('name:')
                name += 1
                filename = '/home/pi/sheji/' + str(name) + 'test' + '.jpg'
                cv2.imwrite(filename, img)
                # print(filename)
                #break 

cap.release()
cv2.destroyAllWindows()
