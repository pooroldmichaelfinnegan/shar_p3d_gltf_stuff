import numpy as np
import struct

from chunk_groups.chunk_base import Chunk
from chunk_groups.chunk_types import *


class MeshChunk(Chunk):
    def __init__(self, chunk_body):
        Chunk.__init__(self, chunk_body)

        for i in self.child:
            child_name = list[i][0]
            match child_name:
                case 'PrimGroupChunk': PrimGroupChunk(i['PrimGroupChunk'])
                case _: pass


class PrimGroupChunk(Chunk):
    def __init__(self, chunk_body):
        Chunk.__init__(self, chunk_body)

        for i in self.child:
            child_name = list[i][0]
            match child_name:
                case 'PositionList': PositionList(i['PositionList'])
                case 'IndexList': IndexList(i['IndexList'])


class PositionList(Chunk):
    def __init__(self, chunk_body):
        Chunk.__init__(self, chunk_body)

        self.positions = self.data['Positions']
        self.positions_opposite_z = [[ x, y, -z ] for x, y, z in self.positions ]

    def to_bytes(self, array: list):
        return b''.join(struct.pack('f', i) for j in array for i in j)


class IndexList(Chunk):
    def __init__(self, chunk_body):
        Chunk.__init__(self, chunk_body)

        self.indices = self.data['Indices']

    def to_bytes(self, array: list):
        return b''.join(struct.pack('I', i) for i in array)
