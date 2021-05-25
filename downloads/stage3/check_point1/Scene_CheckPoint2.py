import sim as vrep
import time
import numpy as np
from numpy.linalg import multi_dot
from scipy.linalg import expm
from usefulFunctions import *
import transforms3d

'''
https://matthew-brett.github.io/transforms3d/reference/transforms3d.euler.html#transforms3d.euler.euler2mat
pip install transforms3d
'''

# Close all open connections (just in case)
vrep.simxFinish(-1)

# Connect to V-REP (raise exception on failure)
clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
if clientID == -1:
    raise Exception('Failed connecting to remote API server')

# Make a dummy
result, dummy_handle_0 = vrep.simxCreateDummy(clientID,0.1,None,vrep.simx_opmode_oneshot_wait)

# Joint:                 1   2    3     4   5   6
theta_list = np.array([0.2, 0.1, 0.5, 0.7, 0.9, 0.1])
# theta_list = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1])

# Get joint object handles
result, joint_one_handle = vrep.simxGetObjectHandle(clientID, 'UR3_joint1', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for first joint')

result, joint_two_handle = vrep.simxGetObjectHandle(clientID, 'UR3_joint2', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for second joint')

result, joint_three_handle = vrep.simxGetObjectHandle(clientID, 'UR3_joint3', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for third joint')

result, joint_four_handle = vrep.simxGetObjectHandle(clientID, 'UR3_joint4', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for fourth joint')

result, joint_five_handle = vrep.simxGetObjectHandle(clientID, 'UR3_joint5', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for fifth joint')

result, joint_six_handle = vrep.simxGetObjectHandle(clientID, 'UR3_joint6', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for sixth joint')

#Get handle for UR3
result, UR3_handle = vrep.simxGetObjectHandle(clientID, 'UR3', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for UR3')
#Get handle for UR3_connection
result, UR3_connection = vrep.simxGetObjectHandle(clientID, 'UR3_connection', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for UR3UR3_connection')

# Start simulation
vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)

# Dummy handle draw at the joint_six_handle
vrep.simxSetObjectPosition(clientID, dummy_handle_0, joint_six_handle, (0,0,0), vrep.simx_opmode_oneshot_wait)
vrep.simxSetObjectOrientation(clientID, dummy_handle_0, joint_six_handle, (0,0,0), vrep.simx_opmode_oneshot_wait)

# Get the orientation from base to  world frame
result, orientation = vrep.simxGetObjectOrientation(clientID, UR3_connection, UR3_handle, vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object orientation angles for UR3')


# Get the position from base to world frame
result, p = vrep.simxGetObjectPosition(clientID, UR3_connection, UR3_handle, vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object current position for UR3')
P_initial = np.reshape(p,(3,1))
print ("P_initial", P_initial)
R_initial = transforms3d.euler.euler2mat(orientation[0], orientation[1], orientation[2])
print ("R_itinial", R_initial)

M = np.block([
[R_initial[0,:], P_initial[0,:]],
[R_initial[1,:], P_initial[1,:]],
[R_initial[2,:], P_initial[2,:]],
[0,0,0,1] ])
print ("M", M, "\n")

# Set up scew axis with respect to base frame
result, q1 = vrep.simxGetObjectPosition(clientID,joint_one_handle, UR3_handle,vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object current position for UR3')
q1 = np.reshape(q1,(3,1))
a1 = np.array([[0],[0],[1]])
S1 = revolute(a1, q1)
# print ("q1", q1)
# print ("S1", S1)

result, q2 = vrep.simxGetObjectPosition(clientID,joint_two_handle, UR3_handle,vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object current position for UR3')
q2 = np.reshape(q2,(3,1))
a2 = np.array([[-1],[0],[0]])
S2 = revolute(a2, q2)
# print ("q2", q2)
# print ("S2", S2)

result, q3 = vrep.simxGetObjectPosition(clientID,joint_three_handle, UR3_handle,vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object current position for UR3')
q3 = np.reshape(q3,(3,1))
a3 = np.array([[-1],[0],[0]])
S3 = revolute(a3, q3)
# print ("q3", q3)
# print ("S3", S3)

result, q4 = vrep.simxGetObjectPosition(clientID,joint_four_handle, UR3_handle,vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object current position for UR3')
q4 = np.reshape(q4,(3,1))
a4 = np.array([[-1],[0],[0]])
S4 = revolute(a4, q4)
# print ("q4", q4)
# print ("S4", S4)

result, q5 = vrep.simxGetObjectPosition(clientID,joint_five_handle, UR3_handle,vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object current position for UR3')
q5 = np.reshape(q5,(3,1))
a5 = np.array([[0],[0],[1]])
S5 = revolute(a5, q5)
# print ("q5", q5)
# print ("S5", S5)

result, q6 = vrep.simxGetObjectPosition(clientID,joint_six_handle, UR3_handle,vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object current position for UR3')
q6 = np.reshape(q6,(3,1))
a6 = np.array([[-1],[0],[0]])
S6 = revolute(a6, q6)
# print ("q6", q6)
# print ("S6", S6)

#Use T = e^([s]*theta)* M_inital to get final pose
#The basic Forward kinematics equation
j1 = screwBracForm(S1) * theta_list[0]
j2 = screwBracForm(S2) * theta_list[1]
j3 = screwBracForm(S3) * theta_list[2]
j4 = screwBracForm(S4) * theta_list[3]
j5 = screwBracForm(S5) * theta_list[4]
j6 = screwBracForm(S6) * theta_list[5]

T_final = multi_dot([expm(j1), expm(j2), expm(j3), expm(j4), expm(j5), expm(j6), M])
# print("T_final", T_final)

quaternion = quaternion_from_matrix(T_final)
temp = quaternion[0]
quaternion[0] = quaternion[1]
quaternion[1] = quaternion[2]
quaternion[2] = quaternion[3]
quaternion[3] = temp

P_final = T_final[0:3,3]
# print ("P_final", P_final)

# Show predicted position
vrep.simxSetObjectPosition(clientID, dummy_handle_0, -1, P_final, vrep.simx_opmode_oneshot_wait)
vrep.simxSetObjectQuaternion(clientID, dummy_handle_0, -1, quaternion, vrep.simx_opmode_oneshot_wait)
time.sleep(1)

R_final = T_final[0:3, 0:3]
# print ("R_final", R_final)

final_a,final_b,final_g = transforms3d.euler.mat2euler(R_final)
final_euler = [final_a, final_b, final_g]
# print ("final_euler", final_euler)

# Show predicted position
result, dummy_handle_1 = vrep.simxCreateDummy(clientID,0.1,None,vrep.simx_opmode_oneshot_wait)
if result != vrep.simx_return_ok:
    raise Exception('could not get dummy_handle_1')

vrep.simxSetObjectPosition(clientID, dummy_handle_1, UR3_handle, P_final, vrep.simx_opmode_oneshot_wait)
vrep.simxSetObjectOrientation(clientID, dummy_handle_1, UR3_handle, final_euler, vrep.simx_opmode_oneshot_wait)

# Set the desired value of the first joint variable
vrep.simxSetJointTargetPosition(clientID, joint_one_handle, theta_list[0], vrep.simx_opmode_oneshot_wait)
vrep.simxSetJointTargetPosition(clientID, joint_two_handle, theta_list[1], vrep.simx_opmode_oneshot_wait)
vrep.simxSetJointTargetPosition(clientID, joint_three_handle, theta_list[2], vrep.simx_opmode_oneshot_wait)
vrep.simxSetJointTargetPosition(clientID, joint_four_handle, theta_list[3], vrep.simx_opmode_oneshot_wait)
vrep.simxSetJointTargetPosition(clientID, joint_five_handle, theta_list[4], vrep.simx_opmode_oneshot_wait)
vrep.simxSetJointTargetPosition(clientID, joint_six_handle, theta_list[5], vrep.simx_opmode_oneshot_wait)
# time.sleep(2)

vrep.simxRemoveObject(clientID,dummy_handle_0,vrep.simx_opmode_oneshot_wait)
vrep.simxRemoveObject(clientID,dummy_handle_1,vrep.simx_opmode_oneshot_wait)

# Stop simulation
vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)

# Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
vrep.simxGetPingTime(clientID)

# Close the connection to V-REP
vrep.simxFinish(clientID)
