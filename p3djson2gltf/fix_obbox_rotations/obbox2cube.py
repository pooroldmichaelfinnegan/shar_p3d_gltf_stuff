from struct import pack, unpack
import json

# with open('./flandersHouse.json', 'rt') as p3djson:
# with open('./common_gens16Shape.json', 'rt') as p3djson:
with open('./l1z2_col_chunks.json', 'rt') as p3djson:
    d = json.loads(p3djson.read())

s = []


def loopdict(dic):
    for key, value in dic.items():
        if key == 'OBBoxVolume':
            return obbox(value)
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


def obbox(box):
    global s
    # print(f'{list(box[0].values()) = }\n{list(list(box[1][0].values())[0][0].values()) = }')
    sx, sy, sz = box[0].values()
    # print(f'{box[1][0] = }')
    # print(f'{box[1][0].values() = }')
    # print(f'{list(box[1][0].values()) = }')
    # print(f'{list(box[1][0].values())[0] = }')
    # print(f'{list(box[1][0].values())[0][0] = }')
    # print(f'{list(box[1][0].values())[0][0].values() = }')
    tx, ty, tz = list(box[1][0].values())[0].values()
    o0 = list(list(box[1][1].values())[0].values())
    o1 = list(list(box[1][2].values())[0].values())
    o2 = list(list(box[1][3].values())[0].values())
    s += [{ 
        "mesh": 0,
        "scale": [sy, sz, sx],
        "translation": [tx, ty, -1.0*tz],
        "rotation": [o0[0], o1[1], o2[2], 1]
        }]
    # return { 
    #     "mesh": 0,
    #     "scale": [sz, sy, sx],
    #     "translation": [tx, ty, tz],
    #     "rotation": [o0[0], -1.0*o1[1], o2[2]]
    # }

# loopdict(d)
with open('./cube.default.gltf', 'r') as readgltf:
    gltf = json.loads(readgltf.read())

# gltf["nodes"] += [loopdict(d)]
print(loopdict(d))

with open('./rot2.txt', 'wt') as outgltf:
    # outgltf.write(gltf)
    json.dump(s, outgltf, indent=2)
