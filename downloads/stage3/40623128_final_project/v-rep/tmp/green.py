import cv2
import numpy as np
global cxx,cyy,cxx_last,cyy_last
cxx=0
cyy=0
cap = cv2.VideoCapture(0)
point=100
cxx_m=np.zeros(point)
cyy_m=np.zeros(point)
count=0
 
Green = np.uint8([[[0,255,0 ]]])
hsv_Green = cv2.cvtColor(Green,cv2.COLOR_BGR2HSV)
print (hsv_Green)
 
ret = cap.set(3,640)             ##Default is 640X480
ret = cap.set(4,480)             ##change to 320X240
while(1):
    # Take each frame
    _, frame = cap.read()
    frame = cv2.flip(frame,1)  #0:inves up/down 1:mirror (right/left)  -1:inves up/down ,right/left
    # Convert BGR to HSV
    frame2=frame.copy()
    frame = cv2.GaussianBlur(frame,(77,77),0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_green = np.array([60,50,50])
    upper_green = np.array([80,255,255])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_green, upper_green)
    mask_org=mask.copy()
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    ##=================================
    img2, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cx=np.zeros(len(contours))
    cy=np.zeros(len(contours))
    global cxx,cyy,cxx_last,cyy_last,count,cxx_m,cyy_m
    if len(contours)>0:
        cxx_last=cxx
        cyy_last=cyy
        if count<point: cxx="" if="">1:
            cxx_m[count]=cxx
            cyy_m[count]=cyy
            count=count+1
        else:
            count=0
            cxx_m=np.zeros(point)
            cyy_m=np.zeros(point)
            
        cxx=0
        cyy=0
        print (len(contours))
        cnt = contours[0]
        M = cv2.moments(cnt)
        #print (M)
        if M['m00']>1:
     
            for i in range(len(contours)): 
                #global cxx,cyy
                cx[i] = int(M['m10']/M['m00'])
                cy[i] = int(M['m01']/M['m00'])
                cxx=cxx+cx[i]
                cyy=cyy+cy[i]
         
      #global cxx,cyy  
        cxx=cxx/(len(contours))
        yy=cyy/(len(contours))
     
      if cxx>1:
           print ("Center=",cxx,cyy)
           #area = cv2.contourArea(cnt)
           #print("Area",area)
           #perimeter = cv2.arcLength(cnt,True)
           #print("perimeter=",perimeter)
            if cxx_last>1:
                cv2.circle(res,(int(cxx_last),int(cyy_last)), 5, (0,0,255), -1)
                cv2.circle(frame,(int(cxx_last),int(cyy_last)), 5, (0,0,255), -1)
           if count <(point-1):
            for j in range(0,(point-1),1):
             if  int(cxx_m[j+1])>0:
              cv2.line(res,(int(cxx_m[j]),int(cyy_m[j])),(int(cxx_m[j+1]),int(cyy_m[j+1])),(255,0,255),3)
              cv2.circle(res,(int(cxx_m[j]),int(cyy_m[j])), 10, (0,255,0), 0)
              cv2.line(frame,(int(cxx_m[j]),int(cyy_m[j])),(int(cxx_m[j+1]),int(cyy_m[j+1])),(255,0,255),3)
              cv2.circle(frame,(int(cxx_m[j]),int(cyy_m[j])), 10, (0,255,0), 0)
              #print(j,cxx_m[j],cyy_m[j])
 ##=================================
 
cv2.drawContours(res, contours, -1, (255,0,0), 2)
cv2.imshow('Frame',frame)
#cv2.imshow('mask',mask_org)
cv2.imshow('contours:',res)
#cv2.imshow('res',res)
k = cv2.waitKey(5) & 0xFF
if k == 27:
    break
cv2.destroyAllWindows()</point:>