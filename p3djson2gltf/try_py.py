from struct import pack
from time import sleep
import json

from cl import calc_maxmin, Intersect, StaticPhysDSG, OBBox

# with open('./flandersHouse.json', 'rt') as p3djson:
# with open('./common_gens16Shape.json', 'rt') as p3djson:
# with open('./l1z2_col_chunks.json', 'rt') as p3djson:
# with open('./intersect_add_normals/l1_all_intersects_updated.json', 'rt') as p3djson:
# with open('./l1_regions__intersect_jsons__sorted_by_terrain/l1_all_intersects_2.json', 'rt') as p3djson:
with open('./obbox_/l7z6_all_spd.json', 'rt') as p3djson:
    d = json.loads(p3djson.read())

class myfloat(float):
    ''' cheap work-a-round for None that you can compare numbers to '''
    def __init__(self, *args, **kwargs):
        float.__init__(*args, **kwargs)

    def __gt__(self, comp): return False
    def __ge__(self, comp): return False
    def __lt__(self, comp): return False
    def __le__(self, comp): return False


_terrain_types = ['TT_Road','TT_Grass','TT_Sand','TT_Gravel','TT_Water','TT_Wood','TT_Metal','TT_Dirt','None']
s = []
## 9 for not-existing default to None, 8 for default as TT_Road
b = [ b'' for i in range(9) ]
mfvec3 = [ myfloat(0), myfloat(0), myfloat(0) ]
mxmn = [[ mfvec3.copy(), mfvec3.copy() ] for i in range(9) ]


def loopdict(dic):
    global b, s
    
    for key, value in dic.items():
        if key == 'OBBoxVolume':
            # print(value)
            bi = OBBox(value)
            # n += f'{i}, '
            # print(bi.gltf_node())
            s += [bi.gltf_node()]
        
        
        ## intersect stuff
        # if key == 'IntersectDSG':
        #     Int = Intersect(value)
            
        #     ## temp hack for handling when terraintypes chunk isn't present, fixed in class definition
        #     try: types = Int.types
        #     except AttributeError: types = [ 8 for _ in Int.indices3 ]

        #     for i, s in enumerate(types):
        #         t = _terrain_types.index(s)
        #         for j in Int.indices3[i]:
        #             for p in Int.positions3_oz[j]:
        #                 mxmn[t] = calc_maxmin(Int.positions3_oz[j], *mxmn[t])
        #                 b[t] += pack('f', p)
        #             # for p in Int.positions3[j]:
        #             #     mxmn[t] = calc_maxmin(Int.positions3[j], *mxmn[t])
        #             #     b[t] += pack('f', p)

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


# terrain_types  Road Grass Sand Gravel Water Wood Metal Dirt None

## for intersects
# total = 0
# for i in range(9):
#     # with open(f'./l1_regions__intersect_jsons__sorted_by_terrain/l1_terrain_2_opposite_z/{_terrain_types[i]}.bin', 'wb') as file:
#     #     file.write(b[i])

#     print(f'',
#         f'{_terrain_types[i]}',
#         f'    "count": {len(b[i])//12},',
#         f'    "byteLength": {len(b[i])},',
#         f'    "byteOffset": {total},',
#         f'    "max": {mxmn[i][0]},',
#         f'    "min": {mxmn[i][1]}',
#         sep='\n')
#
#    total += len(b[i])
#    # print(f'{mxmn[i]} = ')

# print(f'{max(ps[1])}  {min(ps[1])}')

# with open('./intersect_add_normals/l1r7_redo_intersects.bin', 'wb') as outbin:
#     outbin.write(b''.join(b))

with open('./obbox_/l7z6_all_spd__meshes.json', 'wt') as outbin:
    # outbin.write(b''.join(b))
    json.dump(s, outbin, indent=2)
