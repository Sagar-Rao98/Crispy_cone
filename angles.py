#python angles.py --image images\image_1.jpeg
# import the necessary packages
import argparse
import imutils
import cv2
import matplotlib.pyplot as plt
import math as m
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())
image = cv2.imread(args["image"])
canvas = image.copy()
image[:,:,0]=0 #blue
image[:,:,1]=0 #green
im=image.copy()
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
blurred=cv2.fastNlMeansDenoising(gray)#,3,7,21)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
#contouring and approximation
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
for c in cnts:
 M = cv2.moments(c)
 cv2.drawContours(image, [c], -1, (255, 0, 0), 2)
#line fitting
rows,cols = image.shape[:2]
[vx,vy,x,y] = cv2.fitLine(c, cv2.DIST_HUBER,0,0.01,0.01)
lefty = int((-x*vy/vx) + y)
righty = int(((cols-x)*vy/vx)+y)
cv2.line(canvas,(cols-1,righty),(0,lefty),(0,0,0),2)
x1=cols-1
y1=righty
x2=0
y2=lefty
angleR = m.atan2(y2 - y1, x2 - x1)
angleD=180+m.degrees(angleR)
Full_angle=angleD*2
cv2.circle(canvas, (int((x1-y1)/2), int((x2-y2)/2)), 7, (255, 255, 255), -1)
cv2.putText(canvas,'Angle with Vertical=',(int((x1-y1)/2)+50,int((x2-y2)/2)+50), 
 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
cv2.putText(canvas,str(angleD), (int((x1-y1)/2)+80,int((x2-y2)/2)+80), 
 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
cv2.imshow('canvas', canvas)
cv2.imshow('filtered',im)
cv2.imshow('gray',gray)
cv2.imshow('binary',thresh)
print('halfangle=',angleD)
print('full_angle=',Full_angle)
cv2.waitKey(0)
