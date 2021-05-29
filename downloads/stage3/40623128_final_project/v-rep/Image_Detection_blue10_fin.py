import vrep
import time
import random as rng
from PIL import Image as I
import array

import cv2, numpy

# function based on: 
#   https://github.com/simondlevy/OpenCV-Python-Hacks/blob/master/greenball_tracker.py
def speed(handle,speed):
    vrep.simxSetJointTargetVelocity(clientID,handle,speed,vrep.simx_opmode_oneshot_wait)

#影像尋找藍色物件
def track_blue_object(image):
    # Blur the image to reduce noise100
    blur = cv2.GaussianBlur(image, (3,3),0)
    # Convert BGR to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    # Threshold the HSV image for only blue colors
    ran = 20
    lower_blue = numpy.array([0-ran,100,100])
    upper_blue = numpy.array([0+ran,255,255])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # Blur the mask
    bmask = cv2.GaussianBlur(mask, (5,5),0)
    threshold = 100
    canny_output = cv2.Canny(bmask, threshold,threshold*2)
    contours, _ = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Get the moments
    mu = [None]*len(contours)
    for i in range(len(contours)):
        mu[i] = cv2.moments(contours[i])
    # Get the mass centers
    mc = [None]*len(contours)
    for i in range(len(contours)):
        mc[i] = (mu[i]['m10'] / (mu[i]['m00']), mu[i]['m01'] / (mu[i]['m00']))
    return mc
#影像尋找紅色物件
def track_red_object(image):
    # Blur the image to reduce noise100
    blur = cv2.GaussianBlur(image, (3,3),0)
    # Convert BGR to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    # Threshold the HSV image for only blue colors
    ran = 15
    lower_red = numpy.array([120-ran,100,100])
    upper_red = numpy.array([120+ran,255,255])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_red, upper_red)
    # Blur the mask
    bmask = cv2.GaussianBlur(mask, (5,5),0)
    
    threshold = 100
    canny_output = cv2.Canny(bmask, threshold,threshold*2)
    contours, _ = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Get the moments
    mu = [None]*len(contours)
    for i in range(len(contours)):
        mu[i] = cv2.moments(contours[i])
    # Get the mass centers
    mc = [None]*len(contours)
    for i in range(len(contours)):
        # add 1e-5 to avoid division by zero
        mc[i] = (mu[i]['m10'] / (mu[i]['m00'] ), mu[i]['m01'] / (mu[i]['m00']))
    return mc
#影像尋找綠色物件
def track_green_object(image):
    # Blur the image to reduce noise100
    blur = cv2.GaussianBlur(image, (3,3),0)
    # Convert BGR to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    # Threshold the HSV image for only blue colors
    ran = 20
    lower_blue = numpy.array([60-ran,100,100])
    upper_blue = numpy.array([60+ran,255,255])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # Blur the mask
    bmask = cv2.GaussianBlur(mask, (5,5),0)
    threshold = 100
    canny_output = cv2.Canny(bmask, threshold,threshold*2)
    contours, _ = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Get the moments
    mu = [None]*len(contours)
    for i in range(len(contours)):
        mu[i] = cv2.moments(contours[i])
    # Get the mass centers
    mc = [None]*len(contours)
    for i in range(len(contours)):
        mc[i] = (mu[i]['m10'] / (mu[i]['m00']), mu[i]['m01'] / (mu[i]['m00']))
    return mc
    
vrep.simxFinish(-1)
clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
blue00=blue10=blue11=blue20=blue21=blue22=blue30=blue31=blue32=None
red00=red10=red11=red20=red21=red22=red30=red31=red32=None
if clientID!=-1:
  print('Connected to remote API server')
  # get vision sensor objects
  res, v0 = vrep.simxGetObjectHandle(clientID, 'vs1', vrep.simx_opmode_oneshot_wait)
  res, v1 = vrep.simxGetObjectHandle(clientID, 'vs2', vrep.simx_opmode_oneshot_wait)
  err, resolution, image = vrep.simxGetVisionSensorImage(clientID, v0, 0, vrep.simx_opmode_streaming)
  err,BRev_handle=vrep.simxGetObjectHandle(clientID,'BRev',vrep.simx_opmode_oneshot_wait)
  err,BRev0_handle=vrep.simxGetObjectHandle(clientID,'BRev0',vrep.simx_opmode_oneshot_wait)
  err,BMo_handle=vrep.simxGetObjectHandle(clientID,'BMo',vrep.simx_opmode_oneshot_wait)
  err,BMo0_handle=vrep.simxGetObjectHandle(clientID,'BMo0',vrep.simx_opmode_oneshot_wait)
  err,RRev_handle=vrep.simxGetObjectHandle(clientID,'RRev',vrep.simx_opmode_oneshot_wait)
  err,RMo_handle=vrep.simxGetObjectHandle(clientID,'RMo',vrep.simx_opmode_oneshot_wait)
  time.sleep(1)
  while (vrep.simxGetConnectionId(clientID) != -1):
    # get image from vision sensor 'v0'
    blue00_pos=blue10_pos=blue11_pos=blue20_pos=blue21_pos=blue22_pos=blue30_pos=blue31_pos=blue32_pos=None
    err, resolution, image = vrep.simxGetVisionSensorImage(clientID, v0, 0, vrep.simx_opmode_buffer)
    if err == vrep.simx_return_ok:
        image_byte_array = array.array('b', image)
        image_buffer = I.frombuffer("RGB", (resolution[0],resolution[1]), bytes(image_byte_array), "raw", "RGB", 0, 1)
        img2 = numpy.asarray(image_buffer)
        ret_blue = track_blue_object(img2)
        ret_red = track_red_object(img2)
        ret_green = track_green_object(img2)
        
        if ret_green != None:
            #各球員座標命名
            # blue(x)(y) x = 第幾根桿子(0~3) y = 左邊數來第幾個人(0~2)
            # red(x)(y) x = 第幾根桿子(0~3) y = 左邊數來第幾個人(0~2)
            ret_red_odd = ret_red[::2]
            #刪除重複的座標
            times_of_del_ret_blue = int(len(ret_blue)/2)
            times_of_del_ret_green = int(len(ret_green)/2)
            for i in range(0,times_of_del_ret_blue):
                if ret_blue[i][1] - ret_blue[i+1][1] <= 1:
                    del ret_blue[i]
            for i in range(0,times_of_del_ret_green):
                if ret_green[i][1] - ret_green[i+1][1] <= 1:
                    del ret_green[i]
            for i in range(len(ret_blue)):
                if ret_blue[i][1] >=13 and ret_blue[i][1] <=25:
                    blue00 = (ret_blue[i][0], ret_blue[i][1])
                elif ret_blue[i][1] >= 50 and ret_blue[i][1] <=64:
                    blue10_pos = (ret_blue[i][0], ret_blue[i][1])
                    if blue11_pos== None:
                        blue11_pos= (ret_blue[i][0], ret_blue[i][1])
                elif ret_blue[i][1] >=101 and ret_blue[i][1] <=120:
                    if blue20_pos == None:
                        if blue22_pos == None:
                            blue22_pos = (ret_blue[i][0], ret_blue[i][1])
                        elif blue21_pos == None:
                            blue21_pos = (ret_blue[i][0], ret_blue[i][1])
                        elif blue20_pos == None:
                            blue20_pos = (ret_blue[i][0], ret_blue[i][1])
                elif ret_blue[i][1] >=152 and ret_blue[i][1] <=172:
                    if blue30_pos == None:
                        if blue32_pos == None:
                            blue32_pos = (ret_blue[i][0], ret_blue[i][1])
                        elif blue31_pos == None:
                            blue31_pos = (ret_blue[i][0], ret_blue[i][1])
                        elif blue30_pos == None:
                            blue30_pos = (ret_blue[i][0], ret_blue[i][1])
            #藍球員座標排列
            if blue10_pos[0] < blue11_pos[0]:
                blue10 = blue10_pos
                blue11 = blue11_pos
            elif blue10_pos[0] > blue11_pos[0]:
                blue10 = blue11_pos
                blue11 = blue10_pos
            if blue20_pos[0] > blue21_pos[0]:
                #2>0>1
                if blue22_pos[0] > blue20_pos[0]:
                    blue20 = blue21_pos
                    blue21 = blue20_pos
                    blue22 = blue22_pos
                #0>1>2
                elif blue22_pos[0] < blue21_pos[0]:
                    blue20 = blue22_pos
                    blue21 = blue21_pos
                    blue22 = blue20_pos
                #0>2>1
                elif blue22_pos[0] < blue20_pos[0] and blue22_pos[0] > blue21_pos:
                    blue20 = blue21_pos
                    blue21 = blue22_pos
                    blue22 = blue20_pos
            elif blue20_pos[0] < blue21_pos[0]:
                #2>1>0
                if blue22_pos[0] > blue21_pos[0]:
                    blue20 = blue20_pos
                    blue21 = blue21_pos
                    blue22 = blue22_pos
                #1>0>2
                elif blue22_pos[0] < blue20_pos[0]:
                    blue20 = blue22_pos
                    blue21 = blue20_pos
                    blue22 = blue21_pos
                #1>2>0
                elif blue22_pos[0] > blue20_pos[0] and blue22_pos[0] < blue21_pos[0]:
                    blue20 = blue20_pos
                    blue21 = blue22_pos
                    blue22 = blue21_pos
            #紅球員座標命名
            for i in range(len(ret_red_odd)):
                if ret_red_odd[i][1] >=230 and ret_red_odd[i][1] <=250:
                    red00 = (ret_red_odd[i][0], ret_red_odd[i][1])
                elif ret_red_odd[i][1] >= 185 and ret_red_odd[i][1] <=205:
                    red10 = (ret_red_odd[i][0], ret_red_odd[i][1])
                    if red11 == None:
                        red11 = (ret_red_odd[i][0], ret_red_odd[i][1])
                elif ret_red_odd[i][1] >=134 and ret_red_odd[i][1] <=154:
                    if red21 == None:
                        if red22 == None:
                            red22 = (ret_red_odd[i][0], ret_red_odd[i][1])
                        elif red20 == None:
                            red20 = (ret_red_odd[i][0], ret_red_odd[i][1])
                        elif red21 == None:
                            red21 = (ret_red_odd[i][0], ret_red_odd[i][1])
                elif ret_red_odd[i][1] >=80 and ret_red_odd[i][1] <=100:
                    if red30 == None:
                        if red32 == None:
                            red32 = (ret_red_odd[i][0], ret_red_odd[i][1])
                        elif red31 == None:
                            red31 = (ret_red_odd[i][0], ret_red_odd[i][1])
                        elif red30 == None:
                            red30 = (ret_red_odd[i][0], ret_red_odd[i][1])
            print('blue10 =',blue10)
            print('blue11 =',blue11)
            #對打程式開始
            Bv = ret_green[0][0] - blue00[0]
            BBv=ret_green[0][1] - blue00[1]
            Rv = ret_green[0][0] - red00[0]
            RRv=ret_green[0][1] - red00[1]
            #藍守門員移動
            if Bv<0.0:
                speed(BMo_handle,Bv*-0.02)
            elif Bv>0.0:
                speed(BMo_handle,Bv*-0.02)
            else:
                pass
            #紅守門員移動
            if Rv<0.0:
                speed(RMo_handle,Rv*-0.02)
            elif Rv>0.0:
                speed(RMo_handle,Rv*-0.02)
            else:
                pass
            #藍桿一移動
            B10v = ret_green[0][0] - blue10[0]
            B11v = ret_green[0][0] - blue11[0]
            if abs(B10v) <= abs(B11v):
                if ret_green[0][0] < 147 :
                    if B10v < 0:
                        speed(BMo0_handle,B10v*-0.02)
                    elif B10v > 0:
                        speed(BMo0_handle,B10v*-0.02)
                    else:
                        pass
                else:
                    speed(BMo0_handle,0.5)
            elif abs(B10v) > abs(B11v):
                if ret_green[0][0] >108:
                    if B11v < 0:
                        speed(BMo0_handle,B11v*-0.02)
                    elif B11v > 0:
                        speed(BMo0_handle,B11v*-0.02)
                    else:
                        pass
                else:
                    speed(BMo0_handle,-0.5)
            #藍守門員踢球
            if  blue00[1] >=18 and ret_green[0][1] <= 17:
                if ret_green[0] >62.5:
                    speed(BMo_handle,2)
                    time.sleep(0.1)
                    speed(BRev_handle,20)
                    time.sleep(0.1)
                    if ret_green[1] != blue00[1]:
                        Bv = ret_green[0]-blue00[0]
                        if Bv<0.0:
                            speed(BMo_handle,Bv*-0.02)
                        elif Bv>0.0:
                            speed(BMo_handle,Bv*-0.02)
                        else:
                            pass
                    else:
                        speed(BRev_handle,2)
                    
                elif ret_green[0] <62.5:
                    speed(BMo_handle,-2)
                    time.sleep(0.1)
                    speed(BRev_handle,20)
                    time.sleep(0.1)
                    if ret_green[1] != blue00[1]:
                        Bv = ret_green[0] - blue00[0]
                        if Bv<0.0:
                            speed(BMo_handle,Bv*-0.02)
                        elif Bv>0.0:
                            speed(BMo_handle,Bv*-0.02)
                        else:
                            pass
                    else:
                        speed(BRev_handle,2)
            elif ret_green[0][0] - blue00[0] >= -3 and ret_green[0][0] - blue00[0] <= 3:
                if BBv<10.0:
                    speed(BRev_handle,-2)
                elif BBv>10.0:
                    speed(BRev_handle,2)
                else:
                    pass
            #紅守門員踢球   
            if  red00[1] <=236 and ret_green[0][1] >= 237:
                if ret_green[0][0] >62.5:
                    speed(RMo_handle,2)
                    time.sleep(0.1)
                    speed(RRev_handle,-20)
                    time.sleep(0.1)
                    if ret_green[0][1] != ret_red[1]:
                        Rv = ret_green[0][0] - red00[0]
                        if Rv < 0.0:
                            speed(RMo_handle,Rv*-0.02)
                        elif Rv>0.0:
                            speed(RMo_handle,Rv*-0.02)
                        else:
                            pass
                    else:
                        speed(RRev_handle,2)
                    
                elif ret_green[0][0] <62.5:
                    speed(RMo_handle,-2)
                    time.sleep(0.1)
                    speed(RRev_handle,-20)
                    time.sleep(0.1)
                    if ret_green[0][1] != red00[1]:
                        Rv = ret_green[0][0] - red00[0]
                        if Rv<0.0:
                            speed(RMo_handle,Rv*-0.02)
                        elif Rv>0.0:
                            speed(RMo_handle,Rv*-0.02)
                        else:
                            pass
                    else:
                        speed(RRev_handle,2)
            elif ret_green[0][0] - red00[0] >= -3 and ret_green[0][0] - red00[0] <= 3:
                if RRv<-10.0:
                    speed(RRev_handle,-2)
                elif RRv>-10.0:
                    speed(RRev_handle,2)
                else:
                    pass
            #對打程式結束
            #影像加框處理
        if ret_blue:
            for i in range(len(ret_blue)):
                cv2.rectangle(img2,(int(ret_blue[i][0] - 2),int(ret_blue[i][1] - 5)), (int(ret_blue[i][0] + 2),int(ret_blue[i][1] + 5)), (0x33,0xcc,0xff), 1)
        if ret_red:
            for i in range(len(ret_red)):
                cv2.rectangle(img2,(int(ret_red[i][0] - 2),int(ret_red[i][1] - 5)), (int(ret_red[i][0] + 2),int(ret_red[i][1] + 5)), (0xff,0x33,0x33), 1)
        if ret_green:
            for i in range(len(ret_green)):
                cv2.rectangle(img2,(int(ret_green[i][0] - 5),int(ret_green[i][1] - 5)), (int(ret_green[i][0] + 5),int(ret_green[i][1] + 5)), (0x99,0xff,0x33), 1)
        img2 = img2.ravel()
        vrep.simxSetVisionSensorImage(clientID, v1, img2, 0, vrep.simx_opmode_oneshot)
    elif err == vrep.simx_return_novalue_flag:
      print("no image yet")
      pass
    else:
      print(err)
else:
  print("Failed to connect to remote API Server")
  vrep.simxFinish(clientID)