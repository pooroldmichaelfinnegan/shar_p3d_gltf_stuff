import math

class Chunk:
    def __init__(self, chunk_body: list[dict, list]):
        self.chunk_body: list = chunk_body
        self.data: dict = chunk_body[0]
        self.child: list = chunk_body[1]


class StaticPhysDSG(Chunk):
    def __init__(self, chunk_body: list[dict, list]):
        Chunk.__init__(self, chunk_body)

        for i in self.child:
            child_name = list[i][0]
            match child_name:
                case 'StaticPhysDSG': StaticPhysDSG(i['StaticPhysDSG'])
                case 'CollisionObject': CollisionObject(i['CollisionObject'])
                case _: pass


class CollisionObject(Chunk):
    def __init__(self, chunk_body: list[dict, list]):
        Chunk.__init__(self, chunk_body)

        for i in self.child:
            child_name = list[i][0]
            match child_name:
                case 'CollisionObject': CollisionObject(i['CollisionObject'])
                case 'CollisionVolume': CollisionVolume(i['CollisionVolume'])
                case _: pass


class CollisionVolume(Chunk):
    def __init__(self, chunk_body: list[dict, list]):
        Chunk.__init__(self, chunk_body)

        for i in self.child:
            child_name = list[i][0]
            match child_name:
                case 'CollisionVolume': CollisionVolume(i['CollisionVolume'])
                case 'OBBoxVolume': OBBox(i['OBBoxVolume'])
                case 'CylinderVolume': Cylinder(i['CylinderVolume'])
                case _: pass


class OBBox(Chunk):
    def __init__(self, chunk_body: list[dict, list]):
        Chunk.__init__(self, chunk_body)
        self.length = self.scale = Vec3(self.data).xyz
        self.length_4blender_zxy = [ self.length[2], self.length[0], self.length[1] ]
        self.length_4blender_yzx = [ self.length[1], self.length[2], self.length[0] ]
        self.transform = Vec3Chunk(self.child[0]['CollisionVector']).xyoz
        self.moved = self.transform
        self.o0 = Vec3Chunk(self.child[1]['CollisionVector']).xyz  # X
        self.o1 = Vec3Chunk(self.child[2]['CollisionVector']).xyz  # Y
        self.o2 = Vec3Chunk(self.child[3]['CollisionVector']).xyz  # Z
        self.o0yzx = [ self.o0[1], self.o0[2], self.o0[0] ]
        self.o0zxy = [ self.o0[2], self.o0[0], self.o0[1] ]
        self.o2yzx = [ self.o2[1], self.o2[2], self.o2[0] ]
        self.allx = [ self.o0[0], self.o1[0], self.o2[0] ]
        self.ally = [ self.o0[1], self.o1[1], self.o2[1] ]
        self.allz = [ self.o0[2], self.o1[2], self.o2[2] ]


    def shar_obbox_optimize_axis_func(self, rot, some_length_vector) -> list[float]:
        ''' path to cpp method shar source code this method is bassed on 
            srr2\game\libs\sim\simcollision\collisionvolume.cpp
                line 954
                    void OBBoxVolume::OptimizeAxis()'''


        axes = [ 0, 0, 0 ]
        gt_fabs_1 = lambda f: not -0.9999 < f < 0.9999  # check if component in unit vector is the norm (just -1.0 or 1.0 roughly (within .0001))

        # print(f"{self.o0, self.o1, self.o2 = }")``
        self.normalize = lambda vec: [ j/((sum(i**2 for i in vec))**0.5) for j in vec ]
        self.rounding = lambda unit_vector: (1 - sum(i**2 for i in unit_vector)) ** 2
        for index, vec in enumerate([self.o0, self.o1, self.o2]):
            if not any([gt_fabs_1(q) for q in vec]):
                # self.moved[2] -= 30
                self.R = [0,1,2]
                return { 'rotation': Quat([self.o0, self.o1, self.o2]), 'scale': self.length }
            for flt_index, flt in enumerate(vec):
                if gt_fabs_1(flt):
                    axes[index] = flt_index
                    break
        
        ## fix this monte
        # self.oriented_axis_length = [some_length_vector[i-1] for i in self.axes]
        # self.axes2 = [self.axes[i-1] for i, v in enumerate(self.axes)]
        oriented_axis_length = [ some_length_vector[axes.index(i)] for i, v in enumerate(axes) ]
        axes2 = [ axes[axes.index(i)] for i, v in enumerate(axes) ]

        # axis_ = { self.o0: [ 1, 0, 0, 0 ], self.o1: [ 0, 1, 0, 0 ], self.o2: [ 0, 0, 1, 0 ] }

        # return { 'rotation': [ 1, 0, 0, 0 ] , 'scale': oriented_axis_length }
        return { 'rotation': Quat([self.o0, self.o1, self.o2]) , 'scale': self.length }


    def gltf_node(self, mesh_index: int = 0) -> dict:
        return {
            'mesh': mesh_index,
            # 'translation': self.transform,
            'translation': self.moved,
            # 'scale': self.scale,
            'scale': self.shar_obbox_optimize_axis_func(self.allx, self.length)['scale'],
            # 'rotation': self.rotation,
            # 'rotation': self.Irotation,
            'rotation': self.shar_obbox_optimize_axis_func(self.allx, self.length)['rotation'],
        }


class Cylinder(Chunk):
    def __init__(self, chunk_body: list[dict, list]):
        Chunk.__init__(self, chunk_body)
        self.postition = self.transform = Vec3Chunk(self.child[0]['CollisionVector']).xyoz
        self.rotation = Vec3Chunk(self.child[0]['CollisionVector']).xyz
        self.length = self.scale = Vec3Chunk(self.data).xyz


class Intersect(Chunk):
    ''' IntersectDSG Chunk '''
    def __init__(self, chunk_body: list[dict, list]):
        Chunk.__init__(self, chunk_body)

        self.indices3      = self.data['Indices']
        self.positions3    = self.data['Positions']
        self.facenormals3  = self.data['Normals']
        self.indices       = [ i for j in self.indices3 for i in j ]
        self.positions     = [ i for j in self.positions3 for i in j ]
        self.facenormals   = [ i for j in self.facenormals3 for i in j ]

        self.indices_max,     self.indices_min     = calc_maxmin(*self.indices3)
        self.positions_max,   self.positions_min   = calc_maxmin(*self.positions3)
        self.facenormals_max, self.facenormals_min = calc_maxmin(*self.facenormals3)

        ## oppisite z co-ord
        self.positions3_oz = [[ x, y, z*-1.0 ] for x, y, z in self.positions3 ]
        self.positions_oz  = [ i for j in self.positions3 for i in j ]
        self.positions_oz_max, self.positions_oz_min = calc_maxmin(*self.positions3_oz)


        ## temp hack
        if not self.child: self.types = [ 'TT_Road' for _ in self.indices3 ]
        else: self.types = self.child[0]['TerrainType'][0]['Types']
        ## ^^ need to update, changed from list[int] to list[str]
        # if 'TerrainType' in list(self.child[0]):
        #     self.types = self.child[0]['TerrainType']['Types']
        #     self.bsphere = BSphere(self.child[1]['BSphere'])
        #     self.box = BBox((self.child[2]['BBox']))
        # else:
        #     self.types = [ 0 for _ in self.indices3]
        #     self.bsphere = BSphere(self.child[0]['BSphere'])
        #     self.box = BBox((sel`f.child[1]['BBox']))


class BSphere(Chunk):
    def __init__(self, chunk_body: list[dict, list]):
        Chunk.__init__(self, chunk_body)
        self.sphere = self.data['Sphere']

        self.x, self.y, self.z, self.radius = self.sphere[:4]
        self.oz = self.z * -1.0


class BBox(Chunk):
    def __init__(self, chunk_body: list[dict, list]):
        Chunk.__init__(self, chunk_body)
        self.box = self.data['Box']

        self.xyz1  = self.box[0:3]
        self.xyz2  = self.box[3:6]
        self.xyoz1 = self.xyz1[2]*-1.0
        self.xyoz2 = self.xyz2[2]*-1.0


class Vec3Chunk(Chunk):
    def __init__(self, chunk_body: list[dict, list]):
        Chunk.__init__(self, chunk_body)

        self.values = list(self.data.values())
        self.xyz  = [self.values[0], self.values[1], self.values[2]]
        self.xyoz = [self.values[0], self.values[1], self.values[2]*-1.0]


class Vec3:
    def __init__(self, vec3: dict):
        self.items = list(vec3.items())
        self.xyz  = [self.items[0][1], self.items[1][1], self.items[2][1]]
        self.xyoz = [self.items[0][1], self.items[1][1], self.items[2][1]*-1.0]
    # def Normalize(self, vec3: 'Vec3') -> 'Vec3':
    
    # from math import sqrt, sqr
    # Normalize = lambda vec3: sqrt(j/sum(sqr(i) for i in vec3) for j in vec3)


def calc_maxmin(*args: Vec3) -> list[float, float]:
    _max = list(map(max, zip(*args)))
    _min = list(map(min, zip(*args)))
    return _max, _min


nxt = [ 1, 2, 0 ]

def Quat(mat):
    r''' MakeQuat: Convert 3x3 rotation matrix to unit quaternion 
        Simpsons Hit&Run\game\libs\pure3d\toollib\src\tlQuat.cpp:417 '''
        

    q = [ 0.0, 0.0, 0.0, 0.0 ]

    tr = mat[0][0] + mat[1][1] + mat[2][2]

    if tr > 0.0:
        s = math.sqrt(tr + 1.0)
        w = -s * 0.5

        if s:
            s = 0.5 / s
        x = (mat[2][1] - mat[1][2]) * s
        y = (mat[0][2] - mat[2][0]) * s
        z = (mat[1][0] - mat[0][1]) * s

    else:
        i = 0
        if (mat[1][1] > mat[0][0]): i = 1
        if (mat[2][2] > mat[i][i]): i = 2
        j = nxt[i]
        k = nxt[j]
        s = math.sqrt( (mat[i][i] - (mat[j][j]+mat[k][k])) + 1.0 );      

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


# /Users/g/_m/_shar/SRR2_/game/libs/pure3d/toollib/src/tlQuat.cpp
#   line 417
#
# // MakeQuat: Convert 3x3 rotation matrix to unit quaternion 
# tlQuat::tlQuat(const tlMatrix& mat)
# {
#     float q[4];
#     float tr,s;
#     int i,j,k;
#     tr = mat.element[0][0] + mat.element[1][1] + mat.element[2][2];
#     if (tr > 0.0)
#     {
#         s = sqrtf(tr + 1.0f);
#         w = -s * 0.5f;
#         if (s!=0.0f)
#         {
#             s = 0.5f / s;
#         }
#         x = (mat.element[2][1] - mat.element[1][2]) * s;
#         y = (mat.element[0][2] - mat.element[2][0]) * s;
#         z = (mat.element[1][0] - mat.element[0][1]) * s;
#     } 
#     else 
#     {
#         i = 0;
#         if (mat.element[1][1] > mat.element[0][0]) i = 1;
#         if (mat.element[2][2] > mat.element[i][i]) i = 2;
#         j = nxt[i];
#         k = nxt[j];
#         s = sqrtf( (mat.element[i][i] - (mat.element[j][j]+mat.element[k][k])) + 1.0f );      

#         q[i] = s * 0.5f;
#         if (s!=0.0f)
#         {
#             s = 0.5f / s;
#         }
#         q[3] = (mat.element[k][j] - mat.element[j][k]) * s;
#         q[j] = (mat.element[j][i] + mat.element[i][j]) * s;
#         q[k] = (mat.element[k][i] + mat.element[i][k]) * s;

#         w = -q[3];
#         x = q[0];
#         y = q[1];
#         z = q[2];
#     }  
# }