from chunk_base import Chunk
from chunk_types import *

class Intersect(Chunk):
    ''' IntersectDSG Chunk '''
    def __init__(self, chunk_body: list[dict, list]):
        Chunk.__init__(self, chunk_body)

        self.indices3     = self.data['Indices']
        self.positions3   = self.data['Positions']
        self.facenormals3 = self.data['Normals']
        self.indices     = [ i for j in self.indices3 for i in j ]
        self.positions   = [ i for j in self.positions3 for i in j ]
        self.facenormals = [ i for j in self.facenormals3 for i in j ]

        # self.indices_max,     self.indices_min     = calc_maxmin(*self.indices3)
        # self.positions_max,   self.positions_min   = calc_maxmin(*self.positions3)
        # self.facenormals_max, self.facenormals_min = calc_maxmin(*self.facenormals3)

        ## oppisite z co-ord
        self.positions3_opposite_z = [[ x, y, -z ] for x, y, z in self.positions3 ]
        self.positions_opposite_z = [ i for j in self.positions3_opposite_z for i in j ]
        # self.positions_opposite_z_max, self.positions_opposite_z_min = calc_maxmin(*self.positions3_opposite_z)


        ## 
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
