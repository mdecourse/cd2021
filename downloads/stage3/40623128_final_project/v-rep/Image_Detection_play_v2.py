import vrep
import time

from PIL import Image as I
import array

import cv2, numpy

# function based on: 
#   https://github.com/simondlevy/OpenCV-Python-Hacks/blob/master/greenball_tracker.py
def speed(handle,speed):
    vrep.simxSetJointTargetVelocity(clientID,handle,speed,vrep.simx_opmode_oneshot_wait)
        
def track_green_object(image):
    # Blur the image to reduce noise100
    blur = cv2.GaussianBlur(image, (5,5),0)
    # Convert BGR to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    # Threshold the HSV image for only green colors
    range = 15
    lower_green = numpy.array([60-range,100,100])
    upper_green = numpy.array([60+range,255,255])
    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_green, upper_green)
    # Blur the mask
    bmask = cv2.GaussianBlur(mask, (5,5),0)
    # Take the moments to get the centroid
    moments = cv2.moments(bmask)
    m00 = moments['m00']
    centroid_x, centroid_y = None, None
    if m00 != 0:
        centroid_x = int(moments['m10']/m00)
        centroid_y = int(moments['m01']/m00)
    # Assume no centroid
    ctr = None
    # Use centroid if it exists
    if centroid_x != None and centroid_y != None:
        ctr = (centroid_x, centroid_y)
    return ctr

def track_blue_object(image):
    # Blur the image to reduce noise100
    blur = cv2.GaussianBlur(image, (5,5),0)
    # Convert BGR to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    # Threshold the HSV image for only green colors
    range = 15
    lower_red = numpy.array([0-range,100,100])
    upper_red = numpy.array([0+range,255,255])
    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_red, upper_red)
    # Blur the mask
    bmask = cv2.GaussianBlur(mask, (5,5),0)
    # Take the moments to get the centroid
    moments = cv2.moments(bmask)
    m00 = moments['m00']
    centroid_x, centroid_y = None, None
    if m00 != 0:
        centroid_x = int(moments['m10']/m00)
        centroid_y = int(moments['m01']/m00)
    # Assume no centroid
    ctr = None
    # Use centroid if it exists
    if centroid_x != None and centroid_y != None:
        ctr = (centroid_x, centroid_y)
    return ctr
    
def track_red_object(image):
    # Blur the image to reduce noise100
    blur = cv2.GaussianBlur(image, (5,5),0)
    # Convert BGR to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    # Threshold the HSV image for only green colors
    range = 15
    lower_blue = numpy.array([120-range,100,100])
    upper_blue = numpy.array([120+range,255,255])
    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # Blur the mask
    bmask = cv2.GaussianBlur(mask, (5,5),0)
    # Take the moments to get the centroid
    moments = cv2.moments(bmask)
    m00 = moments['m00']
    centroid_x, centroid_y = None, None
    if m00 != 0:
        centroid_x = int(moments['m10']/m00)
        centroid_y = int(moments['m01']/m00)
    # Assume no centroid
    ctr = None
    # Use centroid if it exists
    if centroid_x != None and centroid_y != None:
        ctr = (centroid_x, centroid_y)
    return ctr

vrep.simxFinish(-1)
clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)

if clientID!=-1:
  print('Connected to remote API server')
  # get vision sensor objects
  res, v0 = vrep.simxGetObjectHandle(clientID, 'vs1', vrep.simx_opmode_oneshot_wait)
  res, v1 = vrep.simxGetObjectHandle(clientID, 'vs2', vrep.simx_opmode_oneshot_wait)
  err, resolution, image = vrep.simxGetVisionSensorImage(clientID, v0, 0, vrep.simx_opmode_streaming)
  err,Sphere_handle=vrep.simxGetObjectHandle(clientID,'Sphere',vrep.simx_opmode_oneshot_wait)
  err,BRod_handle=vrep.simxGetObjectHandle(clientID,'BRod',vrep.simx_opmode_oneshot_wait)
  err,BRev_handle=vrep.simxGetObjectHandle(clientID,'BRev',vrep.simx_opmode_oneshot_wait)
  err,BMo_handle=vrep.simxGetObjectHandle(clientID,'BMo',vrep.simx_opmode_oneshot_wait)
  err,RRev_handle=vrep.simxGetObjectHandle(clientID,'RRev',vrep.simx_opmode_oneshot_wait)
  err,RMo_handle=vrep.simxGetObjectHandle(clientID,'RMo',vrep.simx_opmode_oneshot_wait)
  err,RRod_handle=vrep.simxGetObjectHandle(clientID,'RRod',vrep.simx_opmode_oneshot_wait)
  time.sleep(1)
  while (vrep.simxGetConnectionId(clientID) != -1):
    # get image from vision sensor 'v0'
    err, resolution, image = vrep.simxGetVisionSensorImage(clientID, v0, 0, vrep.simx_opmode_buffer)
    if err == vrep.simx_return_ok:
        image_byte_array = array.array('b', image)
        #print(image_byte_array)
        image_buffer = I.frombuffer("RGB", (resolution[0],resolution[1]), bytes(image_byte_array), "raw", "RGB", 0, 1)
        img2 = numpy.asarray(image_buffer)
      # try to find something green
        ret_green = track_green_object(img2)
        ret_red = track_red_object(img2)
        ret_blue = track_blue_object(img2)
        #print('B=',ret_blue[1],ret_blue[0])#y軸座標為0 x軸座標為1
        #print('R=',ret_red[1],ret_red[0])
        #print('G=',ret_green[1],ret_green[0])
        #'''
        if ret_green != None and ret_red != None and ret_blue != None:
            Bv = float(ret_green[0])-float(ret_blue[0])
            BBv=float(ret_green[1])-float(ret_blue[1])
            Rv = float(ret_green[0])-float(ret_red[0])
            RRv=float(ret_green[1])-float(ret_red[1])
            if Bv<0.0:
                speed(BMo_handle,Bv*-0.02)
            elif Bv>0.0:
                speed(BMo_handle,Bv*-0.02)
            else:
                pass
                
                
            if Rv<0.0:
                speed(RMo_handle,Rv*-0.02)
            elif Rv>0.0:
                speed(RMo_handle,Rv*-0.02)
            else:
                pass
                
                
            if  ret_blue[1] >=18 and ret_green[1] <= 17:
                if ret_green[0] >62.5:
                    speed(BMo_handle,2)
                    time.sleep(0.1)
                    speed(BRev_handle,20)
                    time.sleep(0.1)
                    if ret_green[1] != ret_blue[1]:
                        Bv = float(ret_green[0])-float(ret_blue[0])
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
                    if ret_green[1] != ret_blue[1]:
                        Bv = float(ret_green[0])-float(ret_blue[0])
                        if Bv<0.0:
                            speed(BMo_handle,Bv*-0.02)
                        elif Bv>0.0:
                            speed(BMo_handle,Bv*-0.02)
                        else:
                            pass
                    else:
                        speed(BRev_handle,2)
            elif ret_green[0]-ret_blue[0] >= -3 and ret_green[0]-ret_blue[0] <= 3:
                if BBv<10.0:
                    speed(BRev_handle,-2)
                elif BBv>10.0:
                    speed(BRev_handle,2)
                else:
                    pass
                    
            
            if  ret_red[1] <=236 and ret_green[1] >= 237:
                if ret_green[0] >62.5:
                    speed(RMo_handle,2)
                    time.sleep(0.1)
                    speed(RRev_handle,-20)
                    time.sleep(0.1)
                    if ret_green[1] != ret_red[1]:
                        Rv = float(ret_green[0])-float(ret_red[0])
                        if Rv<0.0:
                            speed(RMo_handle,Rv*-0.02)
                        elif Rv>0.0:
                            speed(RMo_handle,Rv*-0.02)
                        else:
                            pass
                    else:
                        speed(RRev_handle,2)
                    
                elif ret_green[0] <62.5:
                    speed(RMo_handle,-2)
                    time.sleep(0.1)
                    speed(RRev_handle,-20)
                    time.sleep(0.1)
                    if ret_green[1] != ret_red[1]:
                        Rv = float(ret_green[0])-float(ret_red[0])
                        if Rv<0.0:
                            speed(RMo_handle,Rv*-0.02)
                        elif Rv>0.0:
                            speed(RMo_handle,Rv*-0.02)
                        else:
                            pass
                    else:
                        speed(RRev_handle,2)
            elif ret_green[0]-ret_red[0] >= -3 and ret_green[0]-ret_red[0] <= 3:
                if RRv<-10.0:
                    speed(RRev_handle,-2)
                elif RRv>-10.0:
                    speed(RRev_handle,2)
                else:
                    pass
                    
            #'''
      # overlay rectangle marker if something is found by OpenCV
        if ret_green:
            cv2.rectangle(img2,(ret_green[0]-5,ret_green[1]-5), (ret_green[0]+5,ret_green[1]+5), (0x99,0xff,0x33), 1)
          # return image to sensor 'v1'
        if ret_red:
            cv2.rectangle(img2,(ret_red[0]-3,ret_red[1]-5), (ret_red[0]+3,ret_red[1]+5), (0xff,0x33,0x33), 1)
        if ret_blue:
            cv2.rectangle(img2,(ret_blue[0]-3,ret_blue[1]-5), (ret_blue[0]+3,ret_blue[1]+5), (0x33,0xcc,0xff), 1)
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