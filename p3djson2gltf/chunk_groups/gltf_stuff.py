from dataclasses import dataclass

# from ..mat import calc_maxmin

class gltf: pass


@dataclass
class Mesh:
    name: str
    position: int
    normals: int | None
    indices: int | None
    mode: int

    def to_mesh(self):
        mesh = { 
            'name': self.name,
            'primitives': []
        }

        if self.normals is not None: mesh['primitives'][0]['attributes'].update({ 'NORMALS': self.normals })

        return mesh


@dataclass
class MeshPrimitive:
    position_index: int
    normals: None | int
    indices: None | int
    mode: None | int

    def to_primitive(self) -> dict:
        primitives = {
                'attributes': {
                    'position': self.position
                },
                'mode': self.mode
            }
        if self.normals is not None:
            primitives['attributes'].update({ 'NORMALS': self.normals })

        if self.indices is not None:
            primitives.update({ 'indices': self.indices })


@dataclass
class Accessors:
    name: str
    bufferView: int
    byteOffset: int
    count: int
    componentType: int
    type: str
    max: list
    min: list

    def to_acc(self):
        accessor = {
            'name': self.name,
            'bufferView': self.bufferView,
            'byteOffset': self.byteOffset,
            'count': self.count,
            'componentType': self.componentType,
            'type': self.type,
            'max': self.max,
            'min': self.max
        }

        return accessor


@dataclass
class bufferViews:
    buffer: int
    byteLength: int | None
    byteStride: int | None
    byteOffset: int
    target: int

    def to_bf(self):
        bf = {
            'buffer': self.buffer,
            'byteLength': self.byteLength,
            'byteOffset': self.byteOffset,
            'byteStride': self.byteStride
        }

        return bf


class bin_file:
    def __init__(self, buffer: bytes = b'', iofile: str = './dump.bin'):
        self.buffer = buffer
        self.p: bytes = b''
        self.i: bytes = b''
        self.iofile = iofile
        self.offset = len(buffer)
        self.byteLength = len(buffer)

    def add(self, block_of_bytes: bytes, size: int) -> dict:
        self.count = block_of_bytes // size
        self.offset = len(self.buffer)

        buffer += block_of_bytes

        self.byteLength = len(block_of_bytes)

        return {
            'bytelength': self.byteLength,
            'offset': self.offset,
            'count': self.count
        }
    
    def out_write(self):
        with open(self.iofile, 'wt') as io_buffer:
            io_buffer.write(self.buffer)
    
    def out_append(self):
        with open(self.iofile, 'at') as io_buffer:
            io_buffer.write(self.buffer)
