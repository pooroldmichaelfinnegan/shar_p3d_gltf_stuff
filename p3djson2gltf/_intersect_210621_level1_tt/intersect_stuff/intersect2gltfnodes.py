from struct import pack, unpack
import struct
import json

# local imports
import classes
from gltf_template import glTF
_glTF = glTF.copy()

with open('./test_intersect.json', 'rt') as p3djson:
    d = json.loads(p3djson.read())


def loopdict(dic):
    for key, value in dic.items():
        if key == 'IntersectDSG':
            intersect(value)
        if type(value) is dict:
            loopdict(value)
        if type(value) is list:
            looplist(value)


def looplist(lst):
    for index in lst:
        if type(index) is dict:
            loopdict(index)
        if type(index) is list:
            looplist(index)


def intersect(lst):
    global _glTF
    sumbytelen = 0
    uri = './first_pygltf_intersect.bin'
    data = lst[0]
    child_list = lst[1]
    indices3 = data['Indices']
    positions3 = data['Positions']
    facenormals = data['Normals']


# indices ...
    indices = [ i for j in indices3 for i in j ]
    rawbytes = b''.join(pack('I', i) for i in indices)
    beforelen = sumbytelen
    sumbytelen += len(rawbytes)

    with open(uri, 'w+b') as wr:
        bufoffset = len(wr.read())
        wr.write(rawbytes)
        buf_len = len(wr.read())

    buf = classes.Buffers(uri, sumbytelen)
    bv = classes.BufferViews(0, bufoffset, len(rawbytes), 34963)
    acc = classes.Accessor(0, 0, 5125, "SCALAR", len(indices), [max(indices)], [min(indices)])
    
    _glTF["buffers"] += [buf()]
    _glTF["bufferViews"] += [bv()]
    _glTF["accessors"] += [acc()]


# positions ...
    x, y, z = zip(*positions3)
    positions = [ i for j in positions3 for i in j ]
    rawbytes = b''.join(pack('f', i) for i in positions)
    byteslen = len(rawbytes)
    beforelen = sumbytelen
    sumbytelen += byteslen

    with open(uri, 'a+b') as wr:
        wr.write(rawbytes)
    
    # buf = classes.Buffers(uri, bytelen)
    bv = classes.BufferViews(0, beforelen, byteslen, 34962)
    acc = classes.Accessor(len(_glTF["bufferViews"]), 0, 5126, "VEC3", len(positions)/3, [max(i) for i in zip(*positions3)], [min(i) for i in zip(*positions3)])
    msh = classes.Meshes('a', len(_glTF["accessors"]), len(_glTF["accessors"])-1, 4)

    _glTF["bufferViews"] += [bv()]
    _glTF["accessors"] += [acc()]
    _glTF["buffers"][0]["byteLength"] = sumbytelen
    _glTF["meshes"] += [msh()]
    

loopdict(d)


with open('./first_pygltf_intersect.gltf', 'wt') as outgltf:
    # outgltf.write(gltf)
    json.dump(_glTF, outgltf, indent=2)
