import numpy as np


class Matrix3:
    def __init__(self, *components):
        self.m00, self.m01, self.m02 = components[0:3]
        self.m10, self.m11, self.m12 = components[3:6]
        self.m20, self.m21, self.m22 = components[6:9]
        self.IDENTITY = self.I = np.array([[ 0 if n-m else 1 for n in range(3) ] for m in range(3) ])
        self.M = np.array([
            [ self.m00, self.m01, self.m02 ],
            [ self.m10, self.m11, self.m12 ],
            [ self.m20, self.m21, self.m22 ]
        ])

    def trace(self):
        return np.array([ self.m00, self.m11, self.m22 ])

    def __repr__(self) -> str:
        return f'''[
            [ {self.m00:.6f}, {self.m01:.6f}, {self.m02:.6f} ],
            [ {self.m10:.6f}, {self.m11:.6f}, {self.m12:.6f} ],
            [ {self.m20:.6f}, {self.m21:.6f}, {self.m22:.6f} ]
        ]'''

    def rotate(self, theta: float) -> 'Matrix3':
        r = np.array([
            [  np.cos(theta), np.sin(theta), 0 ],
            [ -np.sin(theta), np.cos(theta), 0 ],
            [ 0, 0, 1 ]
        ])
        self.M = np.dot( self.M, r )

    def rm(self) -> None: pass


class Matrix4:
    def __init__(self, *components):
        self.m00, self.m01, self.m02, self.m03 = components[0:3]
        self.m10, self.m11, self.m12, self.m13 = components[3:6]
        self.m20, self.m21, self.m22, self.m23 = components[6:9]
        self.m30, self.m31, self.m32, self.m33 = components[9:12]
        self.M = np.array([
            [ self.m00, self.m01, self.m02, self.m03 ],
            [ self.m10, self.m11, self.m12, self.m13 ],
            [ self.m20, self.m21, self.m22, self.m23 ],
            [ self.m30, self.m31, self.m32, self.m33 ]
        ])
        self.IDENTITY = self.I = np.array([[ 0 if n-m else 1 for n in range(4) ] for m in range(4) ])

    def trace(self) -> np.array:
        return np.array([ self.m00, self.m11, self.m22, self.m33 ])

    def __repr__(self) -> str:
        return f'''[
            [ {self.m00:.6f}, {self.m01:.6f}, {self.m02:.6f}, {self.m03:.6f} ],
            [ {self.m10:.6f}, {self.m11:.6f}, {self.m12:.6f}, {self.m13:.6f} ],
            [ {self.m20:.6f}, {self.m21:.6f}, {self.m22:.6f}, {self.m23:.6f} ],
            [ {self.m30:.6f}, {self.m31:.6f}, {self.m32:.6f}, {self.m33:.6f} ]
        ]'''

    def transform(self, operand: 'Matrix3') -> None:
        self.M =  np.dot(self.M, operand)

    def scale(self, xyz: Vec3) -> None:
        mat = []
        self.M = np.dot( self.M, mat )


class Vec3:
    def __init__(self, array: np.array):
        self.array =np.array(array)

        self.x, self.y, self.z = self.array



def magnitude(self, vector: list):
    return np.sqrt(np.sum(np.square(i) for i in vector))


def normalize(self, vector):
    return [ i/magnitude(vector) for i in vector ]


# def quat2rm(self, quat):
#     angle = 2 * np.arctan2( magnitude(quat[1:]), quat[0] )
#     dangle = np.degrees(angle)
#     return dangle


def SHAR_Source__Rotation_Matrix_to_Quaternion_func(mat, opposite_z: bool = False) -> list:
    r''' MakeQuat: Convert 3x3 rotation matrix to unit quaternion 
        Simpsons Hit&Run\game\libs\radmath\radmath\quaternion.cpp:237
            BuildFromMatrix() '''

    if opposite_z:  # opposite the x, y vector columns
        mat = [[ -x, -y, z ] for x, y, z in mat ]

    q = [ 0.0, 0.0, 0.0, 0.0 ]
    nxt = [ 1, 2, 0 ]
    tr = mat[0][0] + mat[1][1] + mat[2][2]


    if tr > 0.0:
        s = np.sqrt(tr + 1.0)
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
        s = np.sqrt((
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


def op_xy_components(matrix) -> np.array:
    return np.array([[ -x, -y, *z ] for x, y, *z in matrix ])

