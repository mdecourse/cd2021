# simple_image_retranslate.py
#
# Demo of simple image retranslate from v0 to v1

import vrep
import time

import cv2
vrep.simxFinish(-1)

clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)

if clientID!=-1:
  print('Connected to remote API server')

  # get vision sensor objects
  res, vs1 = vrep.simxGetObjectHandle(clientID, 'vs1', vrep.simx_opmode_oneshot_wait)
  res, vs2 = vrep.simxGetObjectHandle(clientID, 'vs2', vrep.simx_opmode_oneshot_wait)


  err, resolution, image = vrep.simxGetVisionSensorImage(clientID, vs1, 0, vrep.simx_opmode_streaming)
  time.sleep(1)

  while (vrep.simxGetConnectionId(clientID) != -1):
    err, resolution, image = vrep.simxGetVisionSensorImage(clientID, vs1, 0, vrep.simx_opmode_buffer)
    print(image)
    if err == vrep.simx_return_ok:
      vrep.simxSetVisionSensorImage(clientID, vs2, image, 0, vrep.simx_opmode_oneshot)
    elif err == vrep.simx_return_novalue_flag:
      print("no image yet")
    else:
      print(err)
else:
  print("Failed to connect to remote API Server")
  vrep.simxFinish(clientID)