import sim as vrep
import math
import random
import time
import math

def signal_switch(singal,enable):

    if singal==1 :
        vrep.simxSetIntegerSignal(clientID,"call_1",1,opmode) #here might have a error
    if singal==2 :
        vrep.simxSetIntegerSignal(clientID,"call_2",1,opmode)
    if singal==3 :
        vrep.simxSetIntegerSignal(clientID,"call_3",1,opmode)
    if singal==4 :
        vrep.simxSetIntegerSignal(clientID,"call_4",1,opmode)
    if singal==5 :
        vrep.simxSetIntegerSignal(clientID,"call_5",1,opmode)
    if singal==6 :
        vrep.simxSetIntegerSignal(clientID,"call_6",1,opmode)
    if singal==12:
        vrep.simxSetIntegerSignal(clientID,'call_1',0,opmode) #here might have a error
    if singal==11:
        vrep.simxSetIntegerSignal(clientID,"call_2",0,opmode)
    if singal==10:
        vrep.simxSetIntegerSignal(clientID,"call_3",0,opmode)
    if singal==9:
        vrep.simxSetIntegerSignal(clientID,"call_4",0,opmode)
    if singal==8:
        vrep.simxSetIntegerSignal(clientID,"call_5",0,opmode)
    if singal==7:
        vrep.simxSetIntegerSignal(clientID,"call_6",0,opmode)

def clean():
    vrep.simxSetIntegerSignal(clientID,"call_1",0,opmode)
    vrep.simxSetIntegerSignal(clientID,"call_2",0,opmode)
    vrep.simxSetIntegerSignal(clientID,"call_3",0,opmode)
    vrep.simxSetIntegerSignal(clientID,"call_4",0,opmode)
    vrep.simxSetIntegerSignal(clientID,"call_5",0,opmode)
    vrep.simxSetIntegerSignal(clientID,"call_6",0,opmode)

print ('Start')
 
vrep.simxFinish(-1)
 
clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
  
if clientID != -1:
    print ('Connected to remote API server')
      
    res = vrep.simxAddStatusbarMessage(
        clientID, "pad testing",
        vrep.simx_opmode_oneshot)
    if res not in (vrep.simx_return_ok, vrep.simx_return_novalue_flag):
        print("Could not add a message to the status bar.")
  
     
    opmode = vrep.simx_opmode_oneshot_wait
    STREAMING = vrep.simx_opmode_streaming
  
     
    vrep.simxStartSimulation(clientID, opmode)
    ret,joint01=vrep.simxGetObjectHandle(clientID,"X",opmode)
    ret,joint02=vrep.simxGetObjectHandle(clientID,"Y",opmode)
    ret,joint03=vrep.simxGetObjectHandle(clientID,"Z",opmode)
    ret,jointr=vrep.simxGetObjectHandle(clientID,"Rotate",opmode)
    tt=0.5
    long_t=1.5
    long_long_t=3 #time set
    rotate_deg=0 #pad rotate
    atz=0  #altitude set
    setx=0.5
    setpx=-0.5 #center pick set
    sety=-0.16
    setpy=-0.16 #center fall set
    cube=1              # set cube
    ball_pick_time=0    #total ball we pick
    ball_put_time=31     #total ball we put
    put_cont=0          # print the ball we put
    pick_high=['-0.0645','-0.135','-0.206','-0.2765'] #pick up high set
    fall_high=['-0.05','-0.12','-0.18','-0.26'] #fall high set
    high_up=['0','0','0.05','0.12']

    
    

    while True :
        clean()
        vrep.simxSetJointTargetPosition(clientID,joint01,0,opmode)
        vrep.simxSetJointTargetPosition(clientID,joint02,0,opmode)
        vrep.simxSetJointTargetPosition(clientID,joint03,0,opmode)
        vrep.simxSetJointTargetPosition(clientID,jointr,0,opmode)
        time.sleep(tt)
        for ball in range(1,7,1):
            ball_pick_time=ball_pick_time+1 #total time we pick
            i=1
            unit=0
            level=0
            while level < ball_pick_time :  #find which level and place should be of the xy coordinates
                unit=unit+1
                level=level+unit**2
            finding_XY=ball_pick_time  #this is the XY on that floor
            while i<=unit-1:
                finding_XY=finding_XY-(i**2) 
                i=i+1
            X_Pos=finding_XY%unit  #the X and Y coordinates(by balls)
            if X_Pos==0:
                X_Pos=unit
            Y_Pos=(math.ceil(finding_XY/unit)) 
            BaseX=setx-((unit-1)*0.05)#now we need to find the 0 of the xy
            BaseY=sety-((unit-1)*0.05)
            vrep.simxSetJointTargetPosition(clientID,joint01,BaseX+(0.1*(X_Pos-1)),opmode)
            time.sleep(tt)
            vrep.simxSetJointTargetPosition(clientID,joint02,BaseY+(0.1*(Y_Pos-1)),opmode)
            time.sleep(tt)
            print("Picking up the ball nember",ball_pick_time,"...")
            vrep.simxSetJointTargetPosition(clientID,joint03,float(pick_high[(unit-1)]),opmode)
            time.sleep(tt)
            signal_switch(ball,str(1))
            time.sleep(tt)
            vrep.simxSetJointTargetPosition(clientID,joint03,atz-float(high_up[(unit-1)]),opmode)
            time.sleep(tt)
            rotate_deg=rotate_deg+60
            vrep.simxSetJointTargetPosition(clientID,jointr,rotate_deg*math.pi/180,opmode)
            time.sleep(tt)
        vrep.simxSetJointTargetPosition(clientID,joint01,0,opmode)
        vrep.simxSetJointTargetPosition(clientID,joint02,0,opmode)
        vrep.simxSetJointTargetPosition(clientID,joint03,0,opmode)
        vrep.simxSetJointTargetPosition(clientID,jointr,0,opmode)
        for ball in range(1,7,1):
            ball_put_time=ball_put_time-1 #total time we put
            put_cont=put_cont+1
            i=1
            unit=0
            level=0
            while level < ball_put_time :
                unit=unit+1
                level=level+unit**2
            finding_XY=ball_put_time 
            while i<=unit-1:
                finding_XY=finding_XY-(i**2) 
                i=i+1
            X_Pos=finding_XY%unit
            if X_Pos==0:
                X_Pos=unit
            Y_Pos=(math.ceil(finding_XY/unit)) 
            BaseX=setpx-((unit-1)*0.05)#now we need to find the 0 of the xy
            BaseY=setpy-((unit-1)*0.05)
            rotate_deg=rotate_deg-60
            vrep.simxSetJointTargetPosition(clientID,jointr,rotate_deg*math.pi/180,opmode)
            time.sleep(tt)
            vrep.simxSetJointTargetPosition(clientID,joint01,BaseX+(0.1*(X_Pos-1)),opmode)
            time.sleep(tt)
            vrep.simxSetJointTargetPosition(clientID,joint02,BaseY+(0.1*(Y_Pos-1)),opmode)
            time.sleep(tt)
            print("Putting the ball nember",put_cont,"...")
            vrep.simxSetJointTargetPosition(clientID,joint03,float(fall_high[(unit-1)]),opmode)
            time.sleep(tt)
            signal_switch((ball+6),0)
            time.sleep(tt)
            vrep.simxSetJointTargetPosition(clientID,joint03,atz-float(high_up[unit-1]),opmode)
            time.sleep(tt)
        if ball_pick_time==30:
            pick_high=['-0.07','-0.138','-0.208','-0.2768']
            setx=-setx
            setpx=-setpx
            ball_pick_time=0
            ball_put_time=31
            put_cont=0