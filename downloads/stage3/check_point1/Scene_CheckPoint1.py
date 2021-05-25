import sim as vrep
import time
import numpy as np

# Close all open connections (just in case)
vrep.simxFinish(-1)

# Connect to V-REP (raise exception on failure)
clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
if clientID == -1:
    raise Exception('Failed connecting to remote API server')


################### Get handles for all joints #################################
result, joint_one_handle = vrep.simxGetObjectHandle(clientID, 'UR3_joint1', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for first joint')

result, joint_one_2_handle = vrep.simxGetObjectHandle(clientID, 'UR3_joint1_2', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for first joint1_2')

result, joint_two_handle = vrep.simxGetObjectHandle(clientID, 'UR3_joint2', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for second joint')

result, joint_two_2_handle = vrep.simxGetObjectHandle(clientID, 'UR3_joint2_2', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for first joint2_2')

result, joint_three_handle = vrep.simxGetObjectHandle(clientID, 'UR3_joint3', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for third joint')

result, joint_three_2_handle = vrep.simxGetObjectHandle(clientID, 'UR3_joint3_2', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for first joint3_2')

result, joint_four_handle = vrep.simxGetObjectHandle(clientID, 'UR3_joint4', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for fourth joint')

result, joint_four_2_handle = vrep.simxGetObjectHandle(clientID, 'UR3_joint4_2', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for fourth joint4_2')

result, joint_five_handle = vrep.simxGetObjectHandle(clientID, 'UR3_joint5', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for fifth joint')

result, joint_five_2_handle = vrep.simxGetObjectHandle(clientID, 'UR3_joint5_2', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for first joint3_2')

result, joint_six_handle = vrep.simxGetObjectHandle(clientID, 'UR3_joint6', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for sixth joint')

result, joint_six_2_handle = vrep.simxGetObjectHandle(clientID, 'UR3_joint6_2', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for sixth joint6_2')
################################################################################

# Start simulation
vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)

# Wait two seconds
time.sleep(2)


############### Get the values for joint variables #############################
result1, theta1 = vrep.simxGetJointPosition(clientID, joint_one_handle, vrep.simx_opmode_blocking)
if result1 != vrep.simx_return_ok:
    raise Exception('could not get first joint variable')
print('current value of first joint variable on UR3: theta = {:f}'.format(theta1))

result1_2, theta1_2 = vrep.simxGetJointPosition(clientID, joint_one_2_handle, vrep.simx_opmode_blocking)
if result1_2 != vrep.simx_return_ok:
    raise Exception('could not get first_2 joint variable')
print('current value of first joint variable on UR3_2: theta = {:f}'.format(theta1_2))

result2, theta2 = vrep.simxGetJointPosition(clientID, joint_two_handle, vrep.simx_opmode_blocking)
if result2 != vrep.simx_return_ok:
    raise Exception('could not get second joint variable')
print('current value of second joint variable on UR3: theta = {:f}'.format(theta2))

result2_2, theta2_2 = vrep.simxGetJointPosition(clientID, joint_two_2_handle, vrep.simx_opmode_blocking)
if result2_2 != vrep.simx_return_ok:
    raise Exception('could not get second_2 joint variable')
print('current value of second joint variable on UR3_2: theta = {:f}'.format(theta2_2))

result3, theta3 = vrep.simxGetJointPosition(clientID, joint_three_handle, vrep.simx_opmode_blocking)
if result3 != vrep.simx_return_ok:
    raise Exception('could not get third joint variable')
print('current value of third joint variable on UR3: theta = {:f}'.format(theta3))

result3_2, theta3_2 = vrep.simxGetJointPosition(clientID, joint_three_2_handle, vrep.simx_opmode_blocking)
if result3_2 != vrep.simx_return_ok:
    raise Exception('could not get third_2 joint variable')
print('current value of third joint variable on UR3_2: theta = {:f}'.format(theta3_2))

result4, theta4 = vrep.simxGetJointPosition(clientID, joint_four_handle, vrep.simx_opmode_blocking)
if result4 != vrep.simx_return_ok:
    raise Exception('could not get fourth joint variable')
print('current value of fourth joint variable on UR3: theta = {:f}'.format(theta4))

result4_2, theta4_2 = vrep.simxGetJointPosition(clientID, joint_four_2_handle, vrep.simx_opmode_blocking)
if result4_2 != vrep.simx_return_ok:
    raise Exception('could not get fourth_2 joint variable')
print('current value of fourth joint variable on UR3_2: theta = {:f}'.format(theta4_2))

result5, theta5 = vrep.simxGetJointPosition(clientID, joint_five_handle, vrep.simx_opmode_blocking)
if result5 != vrep.simx_return_ok:
    raise Exception('could not get fifth joint variable')
print('current value of fifth joint variable on UR3: theta = {:f}'.format(theta5))

result5_2, theta5_2 = vrep.simxGetJointPosition(clientID, joint_five_2_handle, vrep.simx_opmode_blocking)
if result5_2 != vrep.simx_return_ok:
    raise Exception('could not get fifth_2 joint variable')
print('current value of fifth joint variable on UR3_2: theta = {:f}'.format(theta5_2))

result6, theta6 = vrep.simxGetJointPosition(clientID, joint_six_handle, vrep.simx_opmode_blocking)
if result6 != vrep.simx_return_ok:
    raise Exception('could not get sixth joint variable')
print('current value of sixth joint variable on UR3: theta = {:f}'.format(theta6))

result6_2, theta6_2 = vrep.simxGetJointPosition(clientID, joint_six_2_handle, vrep.simx_opmode_blocking)
if result6_2 != vrep.simx_return_ok:
    raise Exception('could not get sixth_2 joint variable')
print('current value of sixth joint variable on UR3_2: theta = {:f}'.format(theta6_2))
################################################################################

# Set the desired value of the joint variables
vrep.simxSetJointTargetPosition(clientID, joint_one_handle, theta1 + (-np.pi / 6), vrep.simx_opmode_oneshot)
vrep.simxSetJointTargetPosition(clientID, joint_one_2_handle, theta1_2 + (np.pi / 6), vrep.simx_opmode_oneshot)
time.sleep(1)
vrep.simxSetJointTargetPosition(clientID, joint_two_handle, theta2 + (np.pi / 6), vrep.simx_opmode_oneshot)
vrep.simxSetJointTargetPosition(clientID, joint_two_2_handle, theta2_2 + (-np.pi / 6), vrep.simx_opmode_oneshot)
time.sleep(1)
vrep.simxSetJointTargetPosition(clientID, joint_three_handle, theta3 + (-np.pi / 4), vrep.simx_opmode_oneshot)
vrep.simxSetJointTargetPosition(clientID, joint_three_2_handle, theta3_2 + (np.pi / 4), vrep.simx_opmode_oneshot)
time.sleep(1)
vrep.simxSetJointTargetPosition(clientID, joint_four_handle, theta4 + (np.pi / 4), vrep.simx_opmode_oneshot)
vrep.simxSetJointTargetPosition(clientID, joint_four_2_handle, theta4_2 + (-np.pi / 4), vrep.simx_opmode_oneshot)
time.sleep(1)
vrep.simxSetJointTargetPosition(clientID, joint_five_handle, theta5 + (np.pi / 3), vrep.simx_opmode_oneshot)
# vrep.simxSetJointTargetPosition(clientID, joint_five_2_handle, theta5_2 + (-np.pi / 3), vrep.simx_opmode_oneshot)
time.sleep(1)
vrep.simxSetJointTargetPosition(clientID, joint_six_handle, theta6 + (np.pi / 2), vrep.simx_opmode_oneshot)
vrep.simxSetJointTargetPosition(clientID, joint_six_2_handle, theta6_2 + (-np.pi / 2.5), vrep.simx_opmode_oneshot)

print("\n\n\n\n\n\n\n\n\n\n\nSay Hi!\n\n\n\n\n\n\n\n\n\n")
vrep.simxSetStringSignal(clientID,'jacoHand','true',vrep.simx_opmode_oneshot)
vrep.simxSetStringSignal(clientID,'micoHand','true',vrep.simx_opmode_oneshot)
# print('Hands should close now')
time.sleep(0.6)
vrep.simxSetStringSignal(clientID,'jacoHand','false',vrep.simx_opmode_oneshot)
vrep.simxSetStringSignal(clientID,'micoHand','false',vrep.simx_opmode_oneshot)
# print('Hands should open now')
time.sleep(0.6)
vrep.simxSetStringSignal(clientID,'jacoHand','true',vrep.simx_opmode_oneshot)
vrep.simxSetStringSignal(clientID,'micoHand','true',vrep.simx_opmode_oneshot)
# print('Hands should close now')
time.sleep(0.6)
vrep.simxSetStringSignal(clientID,'jacoHand','false',vrep.simx_opmode_oneshot)
vrep.simxSetStringSignal(clientID,'micoHand','false',vrep.simx_opmode_oneshot)
# print('Hands should open now')
time.sleep(3)

############### Get the current values for the joints to display ###############
# Get the current value of the first joint variable
result1, theta1 = vrep.simxGetJointPosition(clientID, joint_one_handle, vrep.simx_opmode_blocking)
if result1 != vrep.simx_return_ok:
    raise Exception('could not get first joint variable')
print('current value of first joint variable on UR3: theta = {:f}'.format(theta1))

result1_2, theta1_2 = vrep.simxGetJointPosition(clientID, joint_one_2_handle, vrep.simx_opmode_blocking)
if result1_2 != vrep.simx_return_ok:
    raise Exception('could not get first joint_2 variable')
print('current value of first joint_2 variable on UR3_2: theta = {:f}'.format(theta1_2))

result2, theta2 = vrep.simxGetJointPosition(clientID, joint_two_handle, vrep.simx_opmode_blocking)
if result2 != vrep.simx_return_ok:
    raise Exception('could not get second joint variable')
print('current value of second joint variable on UR3: theta = {:f}'.format(theta2))

result2_2, theta2_2 = vrep.simxGetJointPosition(clientID, joint_two_2_handle, vrep.simx_opmode_blocking)
if result2_2 != vrep.simx_return_ok:
    raise Exception('could not get second joint_2 variable')
print('current value of second joint_2 variable on UR3_2: theta = {:f}'.format(theta2_2))

result3, theta3 = vrep.simxGetJointPosition(clientID, joint_three_handle, vrep.simx_opmode_blocking)
if result3 != vrep.simx_return_ok:
    raise Exception('could not get third joint variable')
print('current value of third joint variable on UR3: theta = {:f}'.format(theta3))

result3_2, theta3_2 = vrep.simxGetJointPosition(clientID, joint_three_2_handle, vrep.simx_opmode_blocking)
if result3_2 != vrep.simx_return_ok:
    raise Exception('could not get third joint_2 variable')
print('current value of third joint_2 variable on UR3_2: theta = {:f}'.format(theta3_2))

result4, theta4 = vrep.simxGetJointPosition(clientID, joint_four_handle, vrep.simx_opmode_blocking)
if result4 != vrep.simx_return_ok:
    raise Exception('could not get fourth joint variable')
print('current value of fourth joint variable on UR3: theta = {:f}'.format(theta4))

result4_2, theta4_2 = vrep.simxGetJointPosition(clientID, joint_four_2_handle, vrep.simx_opmode_blocking)
if result4_2 != vrep.simx_return_ok:
    raise Exception('could not get fourth joint_2 variable')
print('current value of fourth joint_2 variable on UR3_2: theta = {:f}'.format(theta4_2))

result5, theta5 = vrep.simxGetJointPosition(clientID, joint_five_handle, vrep.simx_opmode_blocking)
if result5 != vrep.simx_return_ok:
    raise Exception('could not get fifth joint variable')
print('current value of fifth joint variable on UR3: theta = {:f}'.format(theta5))

result5_2, theta5_2 = vrep.simxGetJointPosition(clientID, joint_five_2_handle, vrep.simx_opmode_blocking)
if result5_2 != vrep.simx_return_ok:
    raise Exception('could not get fifth joint_2 variable')
print('current value of fifth joint_2 variable on UR3_2: theta = {:f}'.format(theta5_2))

result6, theta6 = vrep.simxGetJointPosition(clientID, joint_six_handle, vrep.simx_opmode_blocking)
if result6 != vrep.simx_return_ok:
    raise Exception('could not get sixth joint variable')
print('current value of sixth joint variable on UR3: theta = {:f}'.format(theta6))

result6_2, theta6_2 = vrep.simxGetJointPosition(clientID, joint_six_2_handle, vrep.simx_opmode_blocking)
if result6_2 != vrep.simx_return_ok:
    raise Exception('could not get sixth joint_2 variable')
print('current value of sixth joint_2 variable on UR3_2: theta = {:f}'.format(theta6_2))

################################################################################
# Stop simulation
vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)

# Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
vrep.simxGetPingTime(clientID)

# Close the connection to V-REP
vrep.simxFinish(clientID)
