import json

with open('./flandersHouse.json', 'rt') as js:
    js = json.load(js)

print(js)

# scene index
# scene array
#     node index
# node array
#     mesh index
# mesh array
#     primitives array
#         arrt
#             posi
#     indicies
# buffers
# bufferviews
# accessors
# assert

d = {
    "scene": None,
    "scenes": [{}],
    "nodes": [{}],
    "meshes": [{}],
    "buffers": [{}],
    "bufferViews": [{}],
    "accessors": [{}],
    "asset": {}
}

# scene index
d["scene"] = 0

# scene array
#     node index
d["scenes"] = [{
    "nodes": [0]
}]

# node array
#     mesh index
d["nodes"] = [{
    "mesh": 0
}]

# mesh array
#     primitives array
#         indices
#         attributes
#             POSITION
d["meshes"] = [{
    "primitives": [{
        "attributes": {
            "POSITION": 1
        }, "indices": 0
    }]
}]

# buffers
d["buffers"] = [{
    "uri": "",
    "byteLength": 64
}]

# bufferViews
d["bufferViews"] = [{
    "buffer": 0,
    "byteOffset": 0,
    "byteLength": 6,
    "target": 34963
}, {
    "buffer": 0,
    "byteOffset": 8,
    "byteLength": 48,
    "target": 34962
}]

# accessors
d["accessors"] = [{
    "bufferView": 0,
    "byteOffset": 0,
    "componentType": 5123,
    "count": 3,
    "type": "SCALAR",
    "max": [2],
    "min": [1]
}, {
    "bufferView": 1,
    "byteOffset": 0,
    "componentType": 5126,
    "count": 4,
    "type": "VEC3",
    "max": [1.0, 1.0, 0.0],
    "min": [0.0, 0.0, 0.0]
}]

# assert
d["assert"] = {
    "version": "2.0"
}




