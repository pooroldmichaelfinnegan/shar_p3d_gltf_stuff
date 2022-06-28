from typing import List
import numpy as np


class Matrix3x3:
    def __init__(self, *components):
        self.r0c0, self.r0c1, self.r0c2 = components[0:3]
        self.r1c0, self.r1c1, self.r1c2 = components[3:6]
        self.r2c0, self.r2c1, self.r2c2 = components[6:9]
    def trace(self):
        return [ self.r0c0, self.r1c1, self.r2c2 ]


def magnitude(self, vector: list):
    return np.sqrt(np.sum(np.square(i) for i in vector))


def normalize(self, vector):
    return [ i/magnitude(vector) for i in vector ]


def quat2rm(self, quat):

    angle = 2 * np.arctan2( magnitude(quat[1:]), quat[0] )
    dangle = np.degrees(angle)
    return 

def SHAR_Rotation_Matrix_to_Quaternion(mat, opposite_z: bool = False) -> list:
    r''' MakeQuat: Convert 3x3 rotation matrix to unit quaternion 
        Simpsons Hit&Run\game\libs\radmath\radmath\quaternion.cpp:237
            BuildFromMatrix() '''


    if opposite_z:
        # opposite the x, y vector columns
        mat = [[ -x, -y, z ] for x, y, z in mat ]

    q = [ 0.0, 0.0, 0.0, 0.0 ]
    nxt = [ 1, 2, 0 ]
    tr = mat[0][0] + mat[1][1] + mat[2][2]


    if tr > 0.0:
        s = math.sqrt(tr + 1.0)
        w = -s * 0.5

        if s: s = 0.5 / s
        x = (mat[2][1] - mat[1][2]) * s
        y = (mat[0][2] - mat[2][0]) * s
        z = (mat[1][0] - mat[0][1]) * s

    else:
        i = 0
        if (mat[1][1] > mat[0][0]): i = 1
        if (mat[2][2] > mat[i][i]): i = 2
        j = nxt[i]
        k = nxt[j]
        s = math.sqrt((
            mat[i][i]
            - ( mat[j][j]
                + mat[k][k] )) 
            + 1.0 )

        q[i] = s * 0.5
        if s: s = 0.5 / s

        q[3] = (mat[k][j] - mat[j][k]) * s
        q[j] = (mat[j][i] + mat[i][j]) * s
        q[k] = (mat[k][i] + mat[i][k]) * s

        w = -q[3]
        x =  q[0]
        y =  q[1]
        z =  q[2]

    return [ x, y, z, w ]



def calc_maxmin(*array_of_vec):
    _max = list(map(max, zip(*array_of_vec)))
    _min = list(map(min, zip(*array_of_vec)))
    return _max, _min
