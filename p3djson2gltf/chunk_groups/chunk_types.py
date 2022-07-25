import numpy as np

from chunk_groups.chunk_base import Chunk

class Vec3Chunk(Chunk):
    def __init__(self, chunk_body: list[dict, list]):
        Chunk.__init__(self, chunk_body)

        self.values = np.array(self.data.values())
        self.xyz = np.array([self.values[0], self.values[1], self.values[2]])
        self.xy_opposite_z = np.array([self.values[0], self.values[1], -self.values[2]])
