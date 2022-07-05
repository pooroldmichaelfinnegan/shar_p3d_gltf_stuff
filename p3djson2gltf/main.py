from struct import pack
from time import sleep
import json

from cl import calc_maxmin, Intersect, StaticPhysDSG, OBBox, Sphere, Cylinder

# with open('./flandersHouse.json', 'rt') as p3djson:
# with open('./common_gens16Shape.json', 'rt') as p3djson:
# with open('./l1z2_col_chunks.json', 'rt') as p3djson:
# with open('./intersect_add_normals/l1_all_intersects_updated.json', 'rt') as p3djson:
# with open('./l1_regions__intersect_jsons__sorted_by_terrain/l1_all_intersects_2.json', 'rt') as p3djson:
with open('./collision_stuff/obbox_workings/obbox_/l1r4b_col.json', 'rt') as p3djson_file:
    p3djson = json.loads(p3djson_file.read())


class myfloat(float):
    ''' hacky placeholder None type that can make comparisons against '''
    def __gt__(self, value: bool): return False
    def __ge__(self, value: bool): return False
    def __lt__(self, value: bool): return False
    def __le__(self, value: bool): return False


_terrain_types = [ 'TT_Road','TT_Grass','TT_Sand','TT_Gravel','TT_Water','TT_Wood','TT_Metal','TT_Dirt','None' ]

## 9 for not-existing default to None, 8 for default as TT_Road
terrain_type_buffers = [ b'' for i in range(9) ]
mfvec3 = [ myfloat(0), myfloat(0), myfloat(0) ]
mxmn = [[ mfvec3.copy(), mfvec3.copy() ] for i in range(9) ]

nodes = []

def loopdict(dic):
    global terrain_type_buffers, nodes
    
    for key, value in dic.items():
        ## collision stuff
        match key:
            case 'OBBoxVolume':
                nodes += [OBBox(value).gltf_node()]
            # case 'CylinderVolume': nodes += [ Cylinder(value).gltf_node() ]
            # case 'SphereVolume': nodes += [ Sphere(value).gltf_node() ]
        
            # case 'IntersectDSG':
            #     Int = Intersect(value)

            #     for i, s in enumerate(types):
            #         t = _terrain_types.index(s)
            #         for j in Int.indices3[i]:
            #             for p in Int.positions3_oz[j]:
            #                 mxmn[t] = calc_maxmin(Int.positions3_oz[j], *mxmn[t])
            #                 terrain_type_buffers[t] += pack('f', p)
            #             # for p in Int.positions3[j]:
            #             #     mxmn[t] = calc_maxmin(Int.positions3[j], *mxmn[t])
            #             #     terrain_type_buffers[t] += pack('f', p)

        if isinstance(value, dict):
            loopdict(value)
        if isinstance(value, list):
            looplist(value)


def looplist(lst):
    for index in lst:
        if isinstance(index, dict):
            loopdict(index)
        if isinstance(index, list):
            looplist(index)


loopdict(p3djson)


# with open('./intersect_add_normals/l1r7_redo_intersects.bin', 'wb') as outbin:
#     outbin.write(b''.join(terrain_type_buffers))

## obbox cube gltf
with open('./collision_stuff/obbox_workings/obbox_/cube.default.gltf') as cube:
    _gltf = json.loads(cube.read())


## cylinder©
# with open('./collision_stuff/cylinder/cylinder.default.x.gltf') as cylinder:
#     _gltf = json.loads(cylinder.read())


## sphere
# with open('./collision_stuff/sphere/sphere.default.gltf') as sphere:
#     _gltf = json.loads(sphere.read())


# nodes_index_str = ''.join(f'{i}, ' for i in range(len(nodes))).strip(', ')
nodes_index_list = [ i for i in range(len(nodes)) ]

_gltf['scenes'][0]['nodes'] = nodes_index_list
_gltf['nodes'] = nodes


outname = 'dump'
name_cache = []
if outname == '' or outname != 'dump' and outname in name_cache:
    raise 'RENAME'
else:
    name_cache += [ outname ]
    with open(f'./collision_stuff/obbox_workings/obbox_/l1r4b_obbox_col.gltf', 'wt') as out:
        # out.write(json.dumps(cube_gltf, out, indent=2))
        json.dump(_gltf, out, indent=2)


## dump nodes list to txt file for copy pasting
# with open('./obbox_/dump.json', 'wt') as outbin:
#     # outbin.write(b''.join(terrain_type_buffers))
#     json.dump(nodes, outbin, indent=2)

