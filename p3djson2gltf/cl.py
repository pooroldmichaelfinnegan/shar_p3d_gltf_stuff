
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

        # scale
        self.length = Vec3(self.data).xyz

        # position
        self.position = Vec3Chunk(self.child[0]['CollisionVector']).xyz
        self.position_opposite_z = Vec3Chunk(self.child[0]['CollisionVector']).xy_opposite_z

        # rotation matrix 3x3
        self.o0 = Vec3Chunk(self.child[1]['CollisionVector']).xyz  # X
        self.o1 = Vec3Chunk(self.child[2]['CollisionVector']).xyz  # Y
        self.o2 = Vec3Chunk(self.child[3]['CollisionVector']).xyz  # Z
        self.rotation_matrix = [
            self.o0,
            self.o1,
            self.o2
        ]


    # part of gltf exporter 
    def gltf_node(self, mesh_index: int = 0) -> dict:
        return {
            'mesh': mesh_index,
            'translation': self.position_opposite_z,
            'scale': self.length,
            'rotation': Quat(self.rotation_matrix, opposite_z=True),
        }


class Cylinder(Chunk):
    def __init__(self, chunk_body: list[dict, list]):
        Chunk.__init__(self, chunk_body)
        self.radius = self.data['CylinderRadius']
        self.length = self.data['Length']

        # cylinder if flatend == 1 else capsule
        self.flatend = self.data['FlatEnd']
        self.postition = Vec3Chunk(self.child[0]['CollisionVector']).xyz
        self.postition_opposite_z = Vec3Chunk(self.child[0]['CollisionVector']).xy_opposite_z
        self.rotation = Vec3Chunk(self.child[1]['CollisionVector']).xyz
        self.quat = self.rotation + [0]

    def gltf_node(self):
        return {
            'mesh': 0,
            'translation': self.postition_opposite_z,
            'rotation': self.quat,
            'scale': [self.radius, self.length, self.radius ]
        }


class Sphere(Chunk):
    ''' Sphere '''
    def __init__(self, chunk_body: list[dict, list]):
        Chunk.__init__(self, chunk_body)

        self.radius = self.data['SphereRadius']
        self.position = Vec3Chunk(self.child[0]['CollisionVector']).xyz
        self.position_opposite_z = Vec3Chunk(self.child[0]['CollisionVector']).xy_opposite_z

    def gltf_node(self):
        return {
            'mesh': 0,
            'translation': self.position_opposite_z,
            'scale': [ self.radius, self.radius, self.radius ]
        }

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
        self.positions3_oz = [[ x, y, -z ] for x, y, z in self.positions3 ]
        self.positions_oz = [ i for j in self.positions3 for i in j ]
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

        self.x = self.sphere[0]
        self.y = self.sphere[1]
        self.z = self.sphere[2]
        self.opposite_z = -self.z

        self.radius = self.sphere[4]


class BBox(Chunk):
    def __init__(self, chunk_body: list[dict, list]):
        Chunk.__init__(self, chunk_body)
        self.box = self.data['Box']

        self.xyz1  = self.box[0:3]
        self.xyz2  = self.box[3:6]
        self.xy_opposite_z1 = -self.xyz1[2]
        self.xy_opposite_z2 = -self.xyz2[2]


class Vec3Chunk(Chunk):
    def __init__(self, chunk_body: list[dict, list]):
        Chunk.__init__(self, chunk_body)

        self.values = list(self.data.values())
        self.xyz = [self.values[0], self.values[1], self.values[2]]
        self.xy_opposite_z = [self.values[0], self.values[1], -self.values[2]]


class Vec3:
    def __init__(self, vec3: dict):
        self.values = list(vec3.values())
        self.xyz = [self.values[0], self.values[1], self.values[2]]
        self.xy_opposite_z = [self.values[0], self.values[1], -self.values[2]]


def calc_maxmin(*args: Vec3) -> list[float, float]:
    _max = list(map(max, zip(*args)))
    _min = list(map(min, zip(*args)))
    return _max, _min


def Quat(mat, opposite_z: bool = False) -> list:
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

