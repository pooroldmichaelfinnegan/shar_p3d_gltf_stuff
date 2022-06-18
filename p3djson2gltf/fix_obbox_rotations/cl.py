class Chunk:
    def __init__(self, chunk_body: list):
        self.chunk_body = chunk_body

        if isinstance(chunk_body, dict):
            self.data  = chunk_body
        elif isinstance(chunk_body, list):
            if len(chunk_body) == 2:
                self.data  = chunk_body[0]
                self.child = chunk_body[1]
            elif len(chunk_body) == 1:
                self.child = chunk_body[0]
            else: raise 'ERROR chunk body invalid type'



class SP(Chunk):
    def __init__(self, chunk_body: list):
        Chunk.__init__(self, chunk_body)
        for i in self.child:
            child_name = list[i][0]
            match child_name:
                case 'StaticPhysDSG': SP(i['StaticPhysDSG'])
                case 'CollisionObject': CO(i['CollisionObject'])
                case _: pass


class CO(Chunk):
    def __init__(self, chunk_body: list):
        Chunk.__init__(self, chunk_body)
        for i in self.child:
            child_name = list[i][0]
            match child_name:
                case 'CollisionObject': CO(i['CollisionObject'])
                case 'CollisionVolume': CV(i['CollisionVolume'])
                case _: pass



class CV(Chunk):
    def __init__(self, chunk_body: list):
        Chunk.__init__(self, chunk_body)
        for i in self.child:
            child_name = list[i][0]
            match child_name:
                case 'CollisionVolume': CV(i['CollisionVolume'])
                case 'OBBoxVolume': OBBox(i['OBBoxVolume'])
                case 'CylinderVolume': OBBox(i['CylinderVolume'])
                case _: pass
            

class OBBox(Chunk):
    def __init__(self, chunk_body: list):
        Chunk.__init__(self, chunk_body)
        self.length = Vec3f(self.data).xyz
        self.transform = Vec3f(self.child[0]['CollisionVector']).xyoz
        self.transform[2] += 1000
        self.transform[0] += 1400
        self.rotation = Matrix4(
            Vec3f(self.child[3]['CollisionVector']).xyz,   # Z
            Vec3f(self.child[1]['CollisionVector']).xyz,   # X
            Vec3f(self.child[2]['CollisionVector']).xyz,   # Y
        ).lazy

    def gltf_node(self):
        return {
            'mesh': 0,
            'scale': self.length,
            'translation': self.transform,
            'rotation': self.rotation
        }


class Cylinder(Chunk):
    def __init__(self, chunk_body: list):
        Chunk.__init__(self, chunk_body)
        self.length = Vec3f(self.data).xyz
        self.transform = Vec3f(self.child[0]['CollisionVector']).xyoz
        self.rotation = Vec3f(self.child[0]['CollisionVector']).xyz


class Vec3f(Chunk):
    def __init__(self, chunk_body: list):
        Chunk.__init__(self, chunk_body)
        self.items = list(self.data.items())
        self.xyz = [self.items[0][1], self.items[1][1], self.items[2][1]]
        self.xyoz = [self.items[0][1], self.items[1][1], self.items[2][1]*-1.0]
    
    # def __call__(self) -> list[float, float, float]:
    #     return self.xyz


class Matrix4(Chunk):
    def __init__(self, X: list, Y: list, Z: list, W: list = [0.0, 0.0, 0.0, 1.0]):
        self.X, self.Y, self.Z, self.W = X, Y, Z, W
        self.matrix = [X, Y, Z, W]
        self.IDENTITY = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
        self.lazy = [self.X[0]*-1.0, self.Y[1]*-1.0, self.Z[2]*-1.0, self.W[3]]


# note yZX z800 x1200 may be YZX
