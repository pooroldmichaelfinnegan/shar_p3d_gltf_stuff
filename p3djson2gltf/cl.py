
class Chunk:
    def __init__(self, chunk_body: list):
        self.chunk_body = chunk_body

        if isinstance(chunk_body, dict):
            self.data  = chunk_body
        elif isinstance(chunk_body, list):
            if len(chunk_body) == 1:
                self.child = chunk_body[0]
            elif len(chunk_body) == 2:
                self.data  = chunk_body[0]
                self.child = chunk_body[1]
            else: raise 'ERROR chunk body invalid type'



class StaticPhysDSG(Chunk):
    def __init__(self, chunk_body: list):
        Chunk.__init__(self, chunk_body)

        for i in self.child:
            child_name = list[i][0]
            match child_name:
                case 'StaticPhysDSG': StaticPhysDSG(i['StaticPhysDSG'])
                case 'CollisionObject': CollisionObject(i['CollisionObject'])
                case _: pass


class CollisionObject(Chunk):
    def __init__(self, chunk_body: list):
        Chunk.__init__(self, chunk_body)

        for i in self.child:
            child_name = list[i][0]
            match child_name:
                case 'CollisionObject': CollisionObject(i['CollisionObject'])
                case 'CollisionVolume': CollisionVolume(i['CollisionVolume'])
                case _: pass


class CollisionVolume(Chunk):
    def __init__(self, chunk_body: list):
        Chunk.__init__(self, chunk_body)

        for i in self.child:
            child_name = list[i][0]
            match child_name:
                case 'CollisionVolume': CollisionVolume(i['CollisionVolume'])
                case 'OBBoxVolume': OBBox(i['OBBoxVolume'])
                case 'CylinderVolume': Cylinder(i['CylinderVolume'])
                case _: pass
            

class OBBox(Chunk):
    def __init__(self, chunk_body: list):
        Chunk.__init__(self, chunk_body)
        self.length = self.scale = Vec3f(self.data).xyz
        self.transform = Vec3f(self.child[0]['CollisionVector']).xyoz
        self.rotation = Matrix4(
            Vec3f(self.child[1]['CollisionVector']).xyz,   # X
            Vec3f(self.child[2]['CollisionVector']).xyz,   # Y
            Vec3f(self.child[3]['CollisionVector']).xyz,   # Z
        ).lazy

    def gltf_node(self, mesh_index: int = 0):
        return {
            'mesh': mesh_index,
            'translation': self.transform,
            'rotation': self.rotation,
            'scale': self.scale
        }


class Cylinder(Chunk):
    def __init__(self, chunk_body: list):
        Chunk.__init__(self, chunk_body)
        self.postition = self.transform = Vec3f(self.child[0]['CollisionVector']).xyoz
        self.rotation = Vec3f(self.child[0]['CollisionVector']).xyz
        self.length = self.scale = Vec3f(self.data).xyz


class Intersect(Chunk):
    def __init__(self, chunk_body: list):
        Chunk.__init__(self, chunk_body)
        self.indices3     = self.data['Indices']
        self.positions3   = self.data['Positions']
        self.facenormals3 = self.data['Normals']
        self.indices      = [ i for j in self.indices3 for i in j ]
        self.positions    = [ i for j in self.positions3 for i in j ]
        self.facenormals  = [ i for j in self.facenormals3 for i in j ]

        self.indices_max,     self.indices_min     = calc_maxmin(*self.indices3)
        self.positions_max,   self.positions_min   = calc_maxmin(*self.positions3)
        self.facenormals_max, self.facenormals_min = calc_maxmin(*self.facenormals3)


        if 'TerrainType' in list(self.child[0]):
            self.types = self.child[0]['TerrainType']['Types']
            self.bsphere = BSphere(self.child[1]['BSphere'])
            self.box = BBox((self.child[2]['BBox']))
        else:
            self.types = b''
            self.bsphere = BSphere(self.child[0]['BSphere'])
            self.box = BBox((self.child[1]['BBox']))
        

class BSphere(Chunk):
    def __init__(self, chunk_body: list):
        Chunk.__init__(self, chunk_body)
        self.sphere = self.data['Sphere']

        self.x, self.y, self.z, self.radius = self.sphere[:4]
        self.oz = self.z * -1.0


class BBox(Chunk):
    def __init__(self, chunk_body: list):
        Chunk.__init__(self, chunk_body)
        self.box = self.data['Box']

        self.xyz1  = self.box[0:3]
        self.xyoz1 = self.xyz1[2]*-1.0
        self.xyz2  = self.box[3:6]
        self.xyoz2 = self.xyz2[2]*-1.0


class Vec3f(Chunk):
    def __init__(self, chunk_body: list):
        Chunk.__init__(self, chunk_body)
        self.items = list(self.data.items())
        self.xyz  = [self.items[0][1], self.items[1][1], self.items[2][1]]
        self.xyoz = [self.items[0][1], self.items[1][1], self.items[2][1]*-1.0]

    # def __call__(self) -> list[float, float, float]:
    #     return self.xyz


class Matrix4(Chunk):
    def __init__(self, X: list, Y: list, Z: list, W: list = [0.0, 0.0, 0.0, 1.0]):
        self.X, self.Y, self.Z, self.W = X, Y, Z, W
        self.matrix = [X, Y, Z, W]
        self.IDENTITY = self.I = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
        self.lazy = [self.X[0]*-1.0, self.Y[1]*-1.0, self.Z[2]*-1.0, self.W[3]]


def calc_maxmin(*args: list[float]):
    _max = list(map(max, zip(*args)))
    _min = list(map(min, zip(*args)))
    return _max, _min

