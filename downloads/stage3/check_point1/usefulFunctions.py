import numpy as np
from scipy.linalg import expm
import math
# def bracket_4x4(v):
# return np.block([ [bracket_3x3(v[0:3, :]), v[3:6, :]],[ np.zeros((1,4))] ])


#euler to scew_axis
def euler_to_a(a,b,g):
    R = euler2mat(a,b,g)
    a = np.reshape(R[:,2],(3,1))
    return a

def euler2mat(z=0, y=0, x=0):
    Ms = []
    if z:
        cosz = math.cos(z)
        sinz = math.sin(z)
        Ms.append(np.array(
                [[cosz, -sinz, 0],
                 [sinz, cosz, 0],
                 [0, 0, 1]]))
    if y:
        cosy = math.cos(y)
        siny = math.sin(y)
        Ms.append(np.array(
                [[cosy, 0, siny],
                 [0, 1, 0],
                 [-siny, 0, cosy]]))
    if x:
        cosx = math.cos(x)
        sinx = math.sin(x)
        Ms.append(np.array(
                [[1, 0, 0],
                 [0, cosx, -sinx],
                 [0, sinx, cosx]]))
    if Ms:
        return reduce(np.dot, Ms[::-1])
    return np.eye(3)

def skew(R):
	a = R[0]
	b = R[1]
	c = R[2]
	skew_a = np.array([[0 ,-c ,b] , [c ,0 ,-a], [-b, a ,0]])
	return skew_a

def bracket_skew_4(x):
    return np.array([[0,-x[2],x[1],x[3]],
                     [x[2],0,-x[0],x[4]],
                     [-x[1],x[0],0,x[5]],
                     [0,0,0,0]])

def revolute(a,q):
    aq = -np.dot(skew(a), q)
    screw = np.array([
    [a[0][0]],
    [a[1][0]],
    [a[2][0]],
    [aq[0][0]],
    [aq[1][0]],
    [aq[2][0]]
    ])
    return screw


def exp_s_the(s,theta):
	return expm(bracket_skew_4(s)*theta)

def deg2rad(deg):
	return deg * (np.pi) / 180

def rad2deg(rad):
    return rad * 180 / (np.pi)

def euler_to_axis(x):
	return euler_to_a(deg2rad(x[0]), deg2rad(x[1]), deg2rad(x[2]))

# def rot2euler(R):
#     r00 = R[0][0]
#     r01 = R[0][1]
#     r02 = R[0][2]
#     r12 = R[1][2]
#     r22 = R[2][2]
#     r10 = R[1][0]
#     r11 = R[1][1]
#
#     if r02 < 1:
#         if r02 > -1:
#             theta = np.arcsin(r02)
#             cos_theta = np.cos(theta)
#             psi = np.arctan2(r12/cos_theta, r22/cos_theta)
#             phi = np.arctan2(r01/cos_theta, r00/cos_theta)
#         else:
#             theta = -np.pi/2
#             psi = np.arctan2(-r10,-r11)
#             phi = 0
#     else:
#         theta = np.pi/2
#         psi = np.arctan2(r10,r11)
#         phi = 0
#     return phi, psi, theta

def rot2euler(R):
    '''
    From a paper by Gregory G. Slabaugh (undated),
    "Computing Euler angles from a rotation matrix
    '''
    phi = 0.0
    if np.isclose(R[2,0],-1.0):
        theta = math.pi/2.0
        psi = math.atan2(R[0,1],R[0,2])
    elif np.isclose(R[2,0],1.0):
        theta = -math.pi/2.0
        psi = math.atan2(-R[0,1],-R[0,2])
    else:
        theta = -math.asin(R[2,0])
        cos_theta = math.cos(theta)
        psi = math.atan2(R[2,1]/cos_theta, R[2,2]/cos_theta)
        phi = math.atan2(R[1,0]/cos_theta, R[0,0]/cos_theta)
    return psi, theta, phi



def screwBracForm(mat) :

     brac = np.array([
     [0, -1 * mat[2][0], mat[1][0], mat[3][0]],
     [mat[2][0], 0, -1 * mat[0][0], mat[4][0]],
     [-1 * mat[1][0], mat[0][0], 0, mat[5][0]],
     [0,0,0,0]
     ])
     return brac




def quaternion_from_matrix(matrix, isprecise=False):
    """Return quaternion from rotation matrix."""
    M = np.array(matrix, dtype=np.float64, copy=False)[:4, :4]
    if isprecise:
        q = np.empty((4, ))
        t = np.trace(M)
        if t > M[3, 3]:
            q[0] = t
            q[3] = M[1, 0] - M[0, 1]
            q[2] = M[0, 2] - M[2, 0]
            q[1] = M[2, 1] - M[1, 2]
        else:
            i, j, k = 0, 1, 2
            if M[1, 1] > M[0, 0]:
                i, j, k = 1, 2, 0
            if M[2, 2] > M[i, i]:
                i, j, k = 2, 0, 1
            t = M[i, i] - (M[j, j] + M[k, k]) + M[3, 3]
            q[i] = t
            q[j] = M[i, j] + M[j, i]
            q[k] = M[k, i] + M[i, k]
            q[3] = M[k, j] - M[j, k]
            q = q[[3, 0, 1, 2]]
        q *= 0.5 / math.sqrt(t * M[3, 3])
    else:
        m00 = M[0, 0]
        m01 = M[0, 1]
        m02 = M[0, 2]
        m10 = M[1, 0]
        m11 = M[1, 1]
        m12 = M[1, 2]
        m20 = M[2, 0]
        m21 = M[2, 1]
        m22 = M[2, 2]
        # symmetric matrix K
        K = np.array([[m00-m11-m22, 0.0,         0.0,         0.0],
                         [m01+m10,     m11-m00-m22, 0.0,         0.0],
                         [m02+m20,     m12+m21,     m22-m00-m11, 0.0],
                         [m21-m12,     m02-m20,     m10-m01,     m00+m11+m22]])
        K /= 3.0
        # quaternion is eigenvector of K that corresponds to largest eigenvalue
        w, V = np.linalg.eigh(K)
        q = V[[3, 0, 1, 2], np.argmax(w)]
    if q[0] < 0.0:
        np.negative(q, q)
    return q
