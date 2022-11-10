import numpy as np
# from mat import *

class Chunk:
    def __init__(self, chunk_body: list[dict, list]):
        self.body: list = chunk_body
        self.data: dict = chunk_body[0]
        self.child: list = chunk_body[1]


class glTF:
    def node(self, name: str, mesh: int) -> dict:
        return {
            'name': name,
            'mesh': mesh
        }

    def mesh(
            self,
            name: str,
            position: int = 0,
            normals: int = None,
            indices: int = None,
            mode: int = 4
        ) -> dict:

        mesh = { 
            'name': name,
            'primitives': [{
                'attributes': {
                    'position': position
                },
                'mode': mode
            }]
        }
        if indices is not None: mesh['primitives'].update({ 'indices': indices })
        return mesh

    def accessor(
            self,
            name: str,
            bufferView: int = 0,
            byteOffset: int = 0,
            count: int = 0,
            componentType: int = 5126,
            type: str = 'VEC3',
            max_: list = [],
            min_: list = []
        ) -> dict:

        return {
            'name': name,
            'bufferView': bufferView,
            'byteOffset': byteOffset,
            'count': count,
            'componentType': componentType,
            'type': type,
            'max': max_,
            'min': max_
        }

    def bufferViews(
            self,
            buffer: int,
            byteStride: int | None,
            byteOffset: int
        ) -> dict:

        bf = {
            'buffer': buffer,
            'byteOffset': byteOffset
        }

        if byteStride is not None: bf.update({ 'byteStride': byteStride })

        return bf

    def buffer(self, uri: str, byteLength: int = None):
        if byteLength is None: raise 'no bytelength'

        return {
            'uri': uri,
            'byteLength': byteLength
        }