import sim as vrep
import time
import numpy as np
import math
from numpy.linalg import multi_dot
from scipy.linalg import expm, logm
from usefulFunctions import deg2rad, rad2deg, revolute, bracket_skew_4
from usefulFunctions import skew, euler2mat, euler_to_a,euler_to_axis, exp_s_the
from usefulFunctions import screwBracForm, rot2euler, quaternion_from_matrix, deg2rad
import transforms3d

'''
https://matthew-brett.github.io/transforms3d/reference/transforms3d.euler.html#transforms3d.euler.euler2mat
pip install transforms3d
'''
#input for user for goal pose
def createSkew(mat):
    skew = np.array([
    [0,-mat[2][0],mat[1][0]],
    [mat[2][0],0,-mat[0][0]],
    [-mat[1][0],mat[0][0],0]
    ])

    return skew

def createScrew(a):
    screw = np.array([
    [0],
    [0],
    [0],
    [a[0][0]],
    [a[1][0]],
    [a[2][0]]
    ])
    return screw

def createScrewQ(a, q):

    aq = -1 * np.dot(createSkew(a), q)

    screw = np.array([
    [a[0][0]],
    [a[1][0]],
    [a[2][0]],
    [aq[0][0]],
    [aq[1][0]],
    [aq[2][0]]
    ])

    return screw

def screwBracForm(mat) :

     brac = np.array([
     [0, -1 * mat[2][0], mat[1][0], mat[3][0]],
     [mat[2][0], 0, -1 * mat[0][0], mat[4][0]],
     [-1 * mat[1][0], mat[0][0], 0, mat[5][0]],
     [0,0,0,0]
     ])

     return brac

def createAdjoint(mat):

    R = np.array([
    [mat[0][0],mat[0][1],mat[0][2]],
    [mat[1][0],mat[1][1],mat[1][2]],
    [mat[2][0],mat[2][1],mat[2][2]]
    ])
    p = np.array([
    [mat[0][3]],
    [mat[1][3]],
    [mat[2][3]]
    ])

    bottomLeft = np.dot(createSkew(p), R)

    adj = np.array([
    [R[0][0],R[0][1],R[0][2],0,0,0],
    [R[1][0],R[1][1],R[1][2],0,0,0],
    [R[2][0],R[2][1],R[2][2],0,0,0],
    [bottomLeft[0][0],bottomLeft[0][1],bottomLeft[0][2], R[0][0],R[0][1],R[0][2]],
    [bottomLeft[1][0],bottomLeft[1][1],bottomLeft[1][2], R[1][0],R[1][1],R[1][2]],
    [bottomLeft[2][0],bottomLeft[2][1],bottomLeft[2][2], R[2][0],R[2][1],R[2][2]]
    ])


    return adj

def invScrewBrac(mat):

    twist = np.array([
    [mat[2][1]],
    [mat[0][2]],
    [mat[1][0]],
    [mat[0][3]],
    [mat[1][3]],
    [mat[2][3]]
    ])

    return twist

def getSpacialJacobian(S, theta):

    mat1 = np.array([
    [S[0][0]],
    [S[1][0]],
    [S[2][0]],
    [S[3][0]],
    [S[4][0]],
    [S[5][0]]
    ])
    brac1 = screwBracForm(mat1) * theta[0]
    mat1adj = createAdjoint(expm(brac1))

    mat2 = np.array([
    [S[0][1]],
    [S[1][1]],
    [S[2][1]],
    [S[3][1]],
    [S[4][1]],
    [S[5][1]]
    ])
    brac2 = screwBracForm(mat2) * theta[1]
    mat2adj = createAdjoint(expm(brac2))
    mat2 = np.dot(mat1adj, mat2)

    mat3 = np.array([
    [S[0][2]],
    [S[1][2]],
    [S[2][2]],
    [S[3][2]],
    [S[4][2]],
    [S[5][2]]
    ])
    brac3 = screwBracForm(mat3) * theta[2]
    mat3adj = createAdjoint(expm(brac3))
    mat3 = np.linalg.multi_dot([mat1adj, mat2adj, mat3])

    mat4 = np.array([
    [S[0][3]],
    [S[1][3]],
    [S[2][3]],
    [S[3][3]],
    [S[4][3]],
    [S[5][3]]
    ])
    brac4 = screwBracForm(mat4) * theta[3]
    mat4adj = createAdjoint(expm(brac4))
    mat4 = np.linalg.multi_dot([mat1adj, mat2adj, mat3adj, mat4])


    mat5 = np.array([
    [S[0][4]],
    [S[1][4]],
    [S[2][4]],
    [S[3][4]],
    [S[4][4]],
    [S[5][4]]
    ])
    brac5 = screwBracForm(mat5) * theta[4]
    mat5adj = createAdjoint(expm(brac5))
    mat5 = np.linalg.multi_dot([mat1adj, mat2adj, mat3adj, mat4adj, mat5])

    mat6 = np.array([
    [S[0][5]],
    [S[1][5]],
    [S[2][5]],
    [S[3][5]],
    [S[4][5]],
    [S[5][5]]
    ])
    brac6 = screwBracForm(mat6) * theta[5]
    mat6adj = createAdjoint(expm(brac6))
    mat6 = np.linalg.multi_dot([mat1adj, mat2adj, mat3adj, mat4adj, mat5adj, mat6])


    j = np.array([
    [mat1[0][0],mat2[0][0], mat3[0][0], mat4[0][0], mat5[0][0], mat6[0][0]],
    [mat1[1][0],mat2[1][0], mat3[1][0], mat4[1][0], mat5[1][0], mat6[1][0]],
    [mat1[2][0],mat2[2][0], mat3[2][0], mat4[2][0], mat5[2][0], mat6[2][0]],
    [mat1[3][0],mat2[3][0], mat3[3][0], mat4[3][0], mat5[3][0], mat6[3][0]],
    [mat1[4][0],mat2[4][0], mat3[4][0], mat4[4][0], mat5[4][0], mat6[4][0]],
    [mat1[5][0],mat2[5][0], mat3[5][0], mat4[5][0], mat5[5][0], mat6[5][0]]
    ])

    return j

def getT_1in0(M, S, theta):

    mat1 = np.array([
    [S[0][0]],
    [S[1][0]],
    [S[2][0]],
    [S[3][0]],
    [S[4][0]],
    [S[5][0]]
    ])
    brac1 = screwBracForm(mat1) * theta[0]

    mat2 = np.array([
    [S[0][1]],
    [S[1][1]],
    [S[2][1]],
    [S[3][1]],
    [S[4][1]],
    [S[5][1]]
    ])
    brac2 = screwBracForm(mat2) * theta[1]

    mat3 = np.array([
    [S[0][2]],
    [S[1][2]],
    [S[2][2]],
    [S[3][2]],
    [S[4][2]],
    [S[5][2]]
    ])
    brac3 = screwBracForm(mat3) * theta[2]

    mat4 = np.array([
    [S[0][3]],
    [S[1][3]],
    [S[2][3]],
    [S[3][3]],
    [S[4][3]],
    [S[5][3]]
    ])
    brac4 = screwBracForm(mat4) * theta[3]

    mat5 = np.array([
    [S[0][4]],
    [S[1][4]],
    [S[2][4]],
    [S[3][4]],
    [S[4][4]],
    [S[5][4]]
    ])
    brac5 = screwBracForm(mat5) * theta[4]

    mat6 = np.array([
    [S[0][5]],
    [S[1][5]],
    [S[2][5]],
    [S[3][5]],
    [S[4][5]],
    [S[5][5]]
    ])
    brac6 = screwBracForm(mat6) * theta[5]

    T = multi_dot([expm(brac1), expm(brac2), expm(brac3), expm(brac4), expm(brac5), expm(brac6), M])

    return T

def main():


    x = float(input("Enter X translation position"))
    y = float(input("Enter Y translation position"))
    z = float(input("Enter Z translation position"))
    a = float(input("Enter a rorational angle in degrees"))
    b = float(input("Enter b rorational angle in degrees"))
    c = float(input("Enter c rorational angle in degrees"))

    Goal_pose = RotationMatrixToPose(x, y, z, a, b, c)

    return Goal_pose


def RotationMatrixToPose(x, y, z, a, b, c):
    Goal_pose = np.zeros((4,4))
    Goal_pose[0,3] = x
    Goal_pose[1,3] = y
    Goal_pose[2,3] = z
    Goal_pose[3,3] = 1

    Rot_x = np.array([[1, 0, 0],
                      [0, math.cos(deg2rad(a)), -1*math.sin(deg2rad(a))],
                      [0, math.sin(deg2rad(a)), math.cos(deg2rad(a))]])

    Rot_y = np.array([[math.cos(deg2rad(b)), 0, math.sin(deg2rad(b))],
                      [0, 1, 0],
                      [-1*math.sin(deg2rad(b)), 0, math.cos(deg2rad(b))]])

    Rot_z = np.array([[math.cos(deg2rad(c)), -1*math.sin(deg2rad(c)), 0],
                      [math.sin(deg2rad(c)), math.cos(deg2rad(c)), 0],
                      [0, 0, 1]])


    R = multi_dot([Rot_x, Rot_y, Rot_z])
    Goal_pose[0:3,0:3] = R
    return Goal_pose

# Close all open connections (just in case)
vrep.simxFinish(-1)

# Connect to V-REP (raise exception on failure)
clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
if clientID == -1:
    raise Exception('Failed connecting to remote API server')



# Make a dummy
result, dummy_handle_0 = vrep.simxCreateDummy(clientID,0.1,None,vrep.simx_opmode_oneshot_wait)


# Get handles
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

#Get handel for UR3
result, UR3_handle = vrep.simxGetObjectHandle(clientID, 'UR3', vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object handle for UR3')

# Start simulation
vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)

# Dummy handle draw at the joint_six_handle
vrep.simxSetObjectPosition(clientID, dummy_handle_0, joint_six_handle, (0,0,0), vrep.simx_opmode_oneshot_wait)
vrep.simxSetObjectOrientation(clientID, dummy_handle_0, joint_six_handle, (0,0,0), vrep.simx_opmode_oneshot_wait)

result, pos = vrep.simxGetObjectPosition(clientID, joint_six_handle, -1, vrep.simx_opmode_oneshot_wait)
print("Initial end pos:", pos)


# Get the orientation from base to  world frame
result, orientation = vrep.simxGetObjectOrientation(clientID, joint_six_handle, UR3_handle, vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object orientation angles for UR3')
print ("orientation", orientation)
# Get the position from base to world frame
result, p = vrep.simxGetObjectPosition(clientID, joint_six_handle, UR3_handle, vrep.simx_opmode_blocking)
if result != vrep.simx_return_ok:
    raise Exception('could not get object current position for UR3')
P_initial = np.reshape(p,(3,1))
print ("P_initial", P_initial)
# Return matrix for rotations around z, y and x axes
R_initial = transforms3d.euler.euler2mat(orientation[0], orientation[1], orientation[2])
print ("R_itinial", R_initial)

M = np.array([[0,0,-1, -0.1940], [0,1,0,0], [1,0,0,0.6511], [0,0,0,1]])

print ("M", M, "\n")

a1 = np.array([[0],[0],[1]])
q1 = np.array([[0], [0], [0.1045]])
S1 = revolute(a1, q1)

a2 = np.array([[-1],[0],[0]])
q2 = np.array([[-0.1115], [0], [0.1089]])
S2 = revolute(a2,q2)

a3 = np.array([[-1],[0],[0]])
q3 = np.array([[-0.1115], [0], [0.3525]])
S3 = revolute(a3,q3)

a4 = np.array([[-1],[0],[0]])
q4 = np.array([[-0.1115], [0], [0.5658]])
S4 = revolute(a4,q4)

a5 = np.array([[0],[0],[1]])
q5 = np.array([[-0.1122], [0], [0.65]])
S5 = revolute(a5,q5)

a6 = np.array([[-1],[0],[0]])
q6 = np.array([[0.1115], [0], [0.6511]])
S6 = revolute(a6,q6)

pos_moved_to = 0

while pos_moved_to < 3:
    T_2in0 = main()
    # T_2in0 = RotationMatrixToPose(0.2, 0.2, 0.2, 0.1, 0.1, 0.1)
    print(T_2in0)
    S = np.array([
    [S1[0][0], S2[0][0], S3[0][0], S4[0][0], S5[0][0], S6[0][0]],
    [S1[1][0], S2[1][0], S3[1][0], S4[1][0], S5[1][0], S6[1][0]],
    [S1[2][0], S2[2][0], S3[2][0], S4[2][0], S5[2][0], S6[2][0]],
    [S1[3][0], S2[3][0], S3[3][0], S4[3][0], S5[3][0], S6[3][0]],
    [S1[4][0], S2[4][0], S3[4][0], S4[4][0], S5[4][0], S6[4][0]],
    [S1[5][0], S2[5][0], S3[5][0], S4[5][0], S5[5][0], S6[5][0]]
    ])

    ############### Get the values for joint variables #############################

    result1, theta1 = vrep.simxGetJointPosition(clientID, joint_one_handle, vrep.simx_opmode_blocking)
    if result1 != vrep.simx_return_ok:
        raise Exception('could not get first joint variable')
    print('current value of first joint variable on UR3: theta = {:f}'.format(theta1))

    result2, theta2 = vrep.simxGetJointPosition(clientID, joint_two_handle, vrep.simx_opmode_blocking)
    if result2 != vrep.simx_return_ok:
        raise Exception('could not get second joint variable')
    print('current value of second joint variable on UR3: theta = {:f}'.format(theta2))

    result3, theta3 = vrep.simxGetJointPosition(clientID, joint_three_handle, vrep.simx_opmode_blocking)
    if result3 != vrep.simx_return_ok:
        raise Exception('could not get third joint variable')
    print('current value of third joint variable on UR3: theta = {:f}'.format(theta3))

    result4, theta4 = vrep.simxGetJointPosition(clientID, joint_four_handle, vrep.simx_opmode_blocking)
    if result4 != vrep.simx_return_ok:
        raise Exception('could not get fourth joint variable')
    print('current value of fourth joint variable on UR3: theta = {:f}'.format(theta4))

    result5, theta5 = vrep.simxGetJointPosition(clientID, joint_five_handle, vrep.simx_opmode_blocking)
    if result5 != vrep.simx_return_ok:
        raise Exception('could not get fifth joint variable')
    print('current value of fifth joint variable on UR3: theta = {:f}'.format(theta5))

    result6, theta6 = vrep.simxGetJointPosition(clientID, joint_six_handle, vrep.simx_opmode_blocking)
    if result6 != vrep.simx_return_ok:
        raise Exception('could not get sixth joint variable')
    print('current value of sixth joint variable on UR3: theta = {:f}'.format(theta6))

    theta = np.array([[theta1],[theta2],[theta3],[theta4],[theta5],[theta6]])
    k = 1

    T_1in0 = getT_1in0(M, S, theta)
    screwMat = logm(np.dot(T_2in0, np.linalg.inv(T_1in0)))
    twist = invScrewBrac(screwMat)

    counter = 0
    final_pose_flag = 1

    while (np.linalg.norm(twist) > 0.01):

        if(counter >= 100):
            print("Desired Pose not reachable")
            final_pose_flag = 0
            break

        J = getSpacialJacobian(S, theta)
        thetadot = np.dot(np.linalg.inv(np.dot(np.transpose(J), J) + 0.1*np.identity(6)),
        np.dot(np.transpose(J), twist)) - np.dot(np.identity(6) - np.dot(np.linalg.pinv(J), J), theta)
        theta = theta + (thetadot * k)

        T_1in0 = getT_1in0(M, S, theta)
        screwMat = logm(np.dot(T_2in0, np.linalg.inv(T_1in0)))
        twist = invScrewBrac(screwMat)

        counter = counter + 1

    if(final_pose_flag):
        pos_moved_to = pos_moved_to + 1

        quaternion = quaternion_from_matrix(T_2in0)
        temp = quaternion[0]
        quaternion[0] = quaternion[1]
        quaternion[1] = quaternion[2]
        quaternion[2] = quaternion[3]
        quaternion[3] = temp

        P_final = T_2in0[0:3,3]
        print ("P_final", P_final)
        print("Theta:", theta)
        print("Calculated quaternion:", quaternion)

        vrep.simxSetObjectPosition(clientID, dummy_handle_0, -1, P_final, vrep.simx_opmode_oneshot_wait)
        # vrep.simxSetObjectQuaternion(clientID, dummy_handle_0, -1, quaternion, vrep.simx_opmode_oneshot_wait)
        
        # Set the desired value of the first joint variable
        vrep.simxSetJointTargetPosition(clientID, joint_one_handle, theta[0], vrep.simx_opmode_oneshot_wait)
        vrep.simxSetJointTargetPosition(clientID, joint_two_handle, theta[1], vrep.simx_opmode_oneshot_wait)
        vrep.simxSetJointTargetPosition(clientID, joint_three_handle, theta[2], vrep.simx_opmode_oneshot_wait)
        vrep.simxSetJointTargetPosition(clientID, joint_four_handle, theta[3], vrep.simx_opmode_oneshot_wait)
        vrep.simxSetJointTargetPosition(clientID, joint_five_handle, theta[4], vrep.simx_opmode_oneshot_wait)
        vrep.simxSetJointTargetPosition(clientID, joint_six_handle, theta[5], vrep.simx_opmode_oneshot_wait)
        # Wait two seconds
        time.sleep(1)

        #vrep.simxRemoveObject(clientID,dummy_handle_1,vrep.simx_opmode_oneshot_wait)
vrep.simxRemoveObject(clientID,dummy_handle_0,vrep.simx_opmode_oneshot_wait)
# Stop simulation
vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)

# Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
vrep.simxGetPingTime(clientID)

# Close the connection to V-REP
vrep.simxFinish(clientID)
