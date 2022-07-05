import numpy as np

from chunk_base import Chunk
from chunk_types import Vec3Chunk
from mat import *

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
            'rotation': SHAR_Source__Rotation_Matrix_to_Quaternion_func(self.rotation_matrix, opposite_z=True),
        }


class Cylinder(Chunk):

    # capsule relation
    # if (mFlatEnd)
    #     mSphereRadius = Sqrt(Sqr(mLength) + Sqr(mCylinderRadius));
    # else
    #     mSphereRadius = mLength + mCylinderRadius;

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

