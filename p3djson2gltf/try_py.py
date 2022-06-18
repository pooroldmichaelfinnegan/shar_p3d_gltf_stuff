from struct import pack, unpack
import json

from cl import Intersect, StaticPhysDSG

# with open('./flandersHouse.json', 'rt') as p3djson:
# with open('./common_gens16Shape.json', 'rt') as p3djson:
# with open('./l1z2_col_chunks.json', 'rt') as p3djson:
with open('./intersect_add_normals/l1_all_intersects.json', 'rt') as p3djson:
    d = json.loads(p3djson.read())

# loopdict(d)
_terrain_types = ['Road','Grass','Sand','Gravel','Water','Wood','Metal','Dirt']
s = []
b = [ b'', b'', b'', b'', b'', b'', b'', b'' ]


def loopdict(dic):
    global s, b
    for key, value in dic.items():
        # if key == 'OBBoxVolume':
            # print(value)
            # bi = OBBox(value)
            # n += f'{i}, '
            # print(bi.gltf_node())
            # s += [bi.gltf_node()]
        if key == 'IntersectDSG':
            Int = Intersect(value)
            for i, t in enumerate(Int.types):
                for j in Int.indices3[i]:
                    for p in Int.positions3[j]:
                        b[t] += pack('f', p)

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


loopdict(d)

# gltf["nodes"] += [loopdict(d)]
#jsonn = loopdict(d)
#text = loopdict(d)
#bin = loopdict(d)


    # for cube matrix transform 
# with open('./cube.default.gltf', 'rt') as readgltf:
#     gltf = json.loads(readgltf.read())

# gltf['nodes'] = s
# g = json.dumps(gltf, indent=2)


# with open(f'./l1z2_obbox_col__r_ZXY_z1000_x1400.gltf', 'wt') as writegltf:
#     json.dump(gltf, writegltf, indent=2)

# with open('./fix_rot0.txt', 'wt') as outjsonn:
    # json.dump(jsonn, outgltf, indent=2)

# with open('./fix_rot0.txt', 'wt') as outtext:
#     outtext.write(text)
# ['Road','Grass','Sand','Gravel','Water','Wood','Metal','Dirt',

total = 0
for i, B in enumerate(b):
    print(f'{_terrain_types[i]:8}{len(B):6}{total if len(B) else "":8}')
    total += len(B)

with open('./intersect_add_normals/l1_int_types.bin', 'wb') as outbin:
    outbin.write(b''.join(b))
