
class Chunk:
    def __init__(self, chunk_body: list[dict, list]):
        self.chunk_body: list = chunk_body
        print(f'{self}{self.chunk_body = }')
        self.data: dict = chunk_body[0]
        self.child: list = chunk_body[1]

        ## for when data and/or children sections were filtered out if empty
        # if isinstance(chunk_body, dict):
        #     self.data  = chunk_body
        # elif isinstance(chunk_body, list):
        #     if len(chunk_body) == 1:
        #         self.child = chunk_body[0]
        #     elif len(chunk_body) == 2:
        #         self.data  = chunk_body[0]
        #         self.child = chunk_body[1]
        #     else: raise 'ERROR chunk body invalid type'


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
        self.length = self.scale = Vec3f(self.data).xyz
        self.length_swap_around = [ self.length[2], self.length[0], self.length[1] ]
        self.transform = Vec3fChunk(self.child[0]['CollisionVector']).xyoz
        self.rotation = Matrix4(
            Vec3fChunk(self.child[1]['CollisionVector']).xyz,  # X
            Vec3fChunk(self.child[2]['CollisionVector']).xyz,  # Y
            Vec3fChunk(self.child[3]['CollisionVector']).xyz,  # Z
        ).lazy_broke

    def gltf_node(self, mesh_index: int = 0) -> dict:
        return {
            'mesh': mesh_index,
            'translation': self.transform,
            'rotation': self.rotation,
            # 'scale': self.scale
            'scale': self.length_swap_around
        }


class Cylinder(Chunk):
    def __init__(self, chunk_body: list[dict, list]):
        Chunk.__init__(self, chunk_body)
        self.postition = self.transform = Vec3fChunk(self.child[0]['CollisionVector']).xyoz
        self.rotation = Vec3fChunk(self.child[0]['CollisionVector']).xyz
        self.length = self.scale = Vec3fChunk(self.data).xyz


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

        ## need to update, changed from list[int] to list[str]
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


class Vec3fChunk(Chunk):
    def __init__(self, chunk_body: list[dict, list]):
        Chunk.__init__(self, chunk_body)

        self.items = list(self.data.items())
        self.xyz  = [self.items[0][1], self.items[1][1], self.items[2][1]]
        self.xyoz = [self.items[0][1], self.items[1][1], self.items[2][1]*-1.0]


class Vec3f:
    def __init__(self, Vec3: dict):
        self.items = list(Vec3.items())
        self.xyz  = [self.items[0][1], self.items[1][1], self.items[2][1]]
        self.xyoz = [self.items[0][1], self.items[1][1], self.items[2][1]*-1.0]



class Matrix4(Chunk):
    def __init__(self, X: list, Y: list, Z: list, W: list = [0.0, 0.0, 0.0, 1.0]):
        self.X, self.Y, self.Z, self.W = X, Y, Z, W
        self.matrix = [X, Y, Z, W]
        self.IDENTITY = self.I = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
        self.lazy = [self.X[0], self.Y[1], self.Z[2], self.W[3]]
        self.lazy_broke = [ self.lazy[0], self.lazy[2], self.lazy[1]*-1.0, self.lazy[3],  ]


def calc_maxmin(*args: list[float, float, float]):
    _max = list(map(max, zip(*args)))
    _min = list(map(min, zip(*args)))
    return _max, _min

