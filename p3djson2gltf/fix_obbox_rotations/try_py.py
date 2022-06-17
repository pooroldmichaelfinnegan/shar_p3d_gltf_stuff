from struct import pack, unpack
import json

from cl import OBBox

# with open('./flandersHouse.json', 'rt') as p3djson:
# with open('./common_gens16Shape.json', 'rt') as p3djson:
with open('./l1z2_col_chunks.json', 'rt') as p3djson:
    d = json.loads(p3djson.read())

# loopdict(d)

s = []

def loopdict(dic):
    global s
    for key, value in dic.items():
        if key == 'OBBoxVolume':
            # print(value)
            bi = OBBox(value)
            # print(bi.gltf_node())
            s += [bi.gltf_node()]
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




# gltf["nodes"] += [loopdict(d)]
loopdict(d)
print(len(s))


with open('./cube.default.gltf', 'rt') as readgltf:
    gltf = json.loads(readgltf.read())

gltf['nodes'] = s
g = json.dumps(gltf, indent=2)


with open(f'./l1z2_obbox_col__r_ZXY_z1000_x1400.gltf', 'wt') as writegltf:
#     writegltf.write(gltf)
    json.dump(gltf, writegltf, indent=2)
# with open('./fix_rot0.txt', 'wt') as outgltf:
    # outgltf.write(s)
    # json.dump(s, outgltf, indent=2)
