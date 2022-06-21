
class glTF:
    def __init__(self):
        self.asset       = { "version": "2.0" }
        self.scene       = []
        self.scenes      = []
        self.nodes       = []
        self.materials   = []
        self.meshes      = []
        self.accessors   = []
        self.bufferViews = []
        self.buffers     = []

        def __call__(self):
            return {
                "version": "2.0",
                "scene": self.scene,
                "scenes": self.scenes,
                "nodes": self.nodes,
                "materials": self.materials,
                "meshes": self.meshes,
                "accessors":self.accessors,
                "bufferViews": self.bufferViews,
                "buffers": self.buffers
            }

class Meshes(glTF):
    def __init__(self, name, position, indices, mode):
        self.name = name
        self.position = position
        # self.normals = normals
        self.indices = indices
        self.mode = mode

    def __call__(self):
        return {
            "primitives": [{
                "attributes": {
                    "POSITION": self.position,
                    # "NORMALS": self.normals
                },
                "indices": self.indices,
                "mode": self.mode
            }]
            # "materials": self.materials,
        }


class Accessor(glTF):
    def __init__( self, bufferView, byteOffset, componentType, type, count, max, min ):
        self.bufferView = bufferView
        self.byteOffset = byteOffset
        self.componentType = componentType
        self.type = type
        self.count = count
        self.max = max
        self.min = min

    def __call__(self):
        return {
            "bufferView": self.bufferView,
            "byteOffset": self.byteOffset,
            "componentType": self.componentType,
            "type": self.type,
            "count": self.count,
            "max": self.max,
            "min": self.min
        }

class BufferViews(glTF):
    def __init__(self, buffer, byteOffset, byteLength, target):
        self.buffer = buffer
        self.byteOffset = byteOffset
        self.byteLength = byteLength
        self.target = target
        # self.byteStride

    def __call__(self):
        return {
            "buffer": self.buffer,
            "byteOffset": self.byteOffset,
            "byteLength": self.byteLength,
            "target": self.target
        }

class Buffers(glTF):
    def __init__(self, uri, byteLength):
        self.uri = uri
        self.byteLength = byteLength
    
    def __call__(self):
        return {
            "uri": self.uri,
            "byteLength": self.byteLength
        }
    
    