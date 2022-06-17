from audioop import maxpp
import struct, json, time
import sys

# local imports
import classes
from gltf_template import glTF
_glTF = glTF.copy()


dotjson = sys.argv[1]
out = dotjson.split('.')[0]

# bin_uri = './n3_pygltf_intersect.bin'
bin_uri = out+'.bin'
# with open(bin_uri, 'wb') as wr:
#     wr.write(b'')

with open(dotjson, 'rt') as p3djson_file:
    p3djson = json.loads(p3djson_file.read())


ind_buffer = b''
pos_buffer = b''
pos_vector_count = 0
ind_count = 0
ind_max_min, pos_max_min = [None,None], [[None,None,None],[None,None,None]]
global_pos = []


def intersect(lst):
    global _glTF, ind_buffer, pos_buffer, pos_vector_count, ind_count, global_pos
    time.sleep(0.01)
    
    data = lst[0]
    child_list = lst[1]
    ind3 = indices3 = data['Indices']
    pos3 = positions3 = data['Positions']
    face_normals = data['Normals']

# indices ...
    # ind = [ i for j in in3 for i in j ]
    ind = [ pos_vector_count + i for j in ind3 for i in j ]
    ind_count += len(ind)
    ind_rawbytes = b''.join(struct.pack('I', i) for i in ind)
    ind_buffer += ind_rawbytes

    if ind_max_min[0] is None: ind_max_min[0] = max(ind)
    if ind_max_min[1] is None: ind_max_min[1] = min(ind)
    if max(ind) > ind_max_min[0]: ind_max_min[0] = max(ind)
    if min(ind) < ind_max_min[1]: ind_max_min[1] = min(ind)

# positions ...
    x, y, z = zip(*pos3)
    oz = [ -1.0*i for i in z ]
    # oz = z
    
    pos = [ i for j in zip(x, y, oz) for i in j ]
    global_pos += pos
    # pos = [ i for j in pos3 for i in j ]
    pos_vector_count += len(pos3)
    pos_rawbytes = b''.join(struct.pack('f', i) for i in pos)
    pos_buffer += pos_rawbytes

    # [pos_max_min[0], max(x)][pos_max_min[0] < max(x)]
    if pos_max_min[0][0] is None or pos_max_min[0][0] < max(x):  
        pos_max_min[0][0] = max(x)
        # print(pos_max_min[0][0], max(x))
    if pos_max_min[0][1] is None or pos_max_min[0][1] < max(y):  
        pos_max_min[0][1] = max(y)
        # print(pos_max_min[0][1], max(y))
    if pos_max_min[0][2] is None or pos_max_min[0][2] < max(oz): 
        pos_max_min[0][2] = max(oz)
        # print(pos_max_min[0][2], max(oz))
    if pos_max_min[1][0] is None or pos_max_min[1][0] > min(x):  
        pos_max_min[1][0] = min(x)
        # print(pos_max_min[1][0], min(x))
    if pos_max_min[1][1] is None or pos_max_min[1][1] > min(y):  
        pos_max_min[1][1] = min(y)
        # print(pos_max_min[1][1], min(y))
    if pos_max_min[1][2] is None or pos_max_min[1][2] > min(oz): 
        pos_max_min[1][2] = min(oz)
        # print(pos_max_min[1][2], min(oz))


    # _glTF["bufferViews"] += [bv()]
    # _glTF["accessors"] += [acc()]
    # _glTF["buffers"][0]["uri"] = './n2_pygltf_intersect.bin'
    # _glTF["buffers"][0]["byteLength"] = sumbytelen
    # _glTF["meshes"] += [msh()]



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


loopdict(p3djson)


# print(global_pos)
# X =  [i for i in global_pos[::3]]
# Y =  [i for i in global_pos[1::3]]
# OZ = [i for i in global_pos[2::3]]
# hundo_x = {}
# hundo_z = {}
# for i in Y:
#     mx = i//1
#     if mx not in hundo_x: hundo_x[mx] = 1
#     hundo_x[mx] += 1
# print(hundo_x)
# print(hundo_z)


print(out+'.bin')
with open(out+'.bin', 'wb') as binary:
    binary.write(pos_buffer + ind_buffer)

# buf = classes.Buffers(bin_uri, len(pos_buffer+ind_buffer))
bv_pos = classes.BufferViews(0, 0, len(pos_buffer), 34962)
bv_ind = classes.BufferViews(0, len(pos_buffer), len(ind_buffer), 34963)
acc_pos = classes.Accessor(0, 0, 5126, "VEC3", pos_vector_count, pos_max_min[0], pos_max_min[1])
acc_ind = classes.Accessor(1, 0, 5125, "SCALAR", ind_count, [ind_max_min[0]], [ind_max_min[1]])
msh = classes.Meshes('a', 0, 1, 4)


_glTF["bufferViews"] += [bv_pos()]
_glTF["bufferViews"] += [bv_ind()]
_glTF["accessors"] += [acc_pos()]
_glTF["accessors"] += [acc_ind()]   
# _glTF["buffers"] += [buf()]
_glTF["buffers"][0]["uri"] = out[6:]+'.bin'
_glTF["buffers"][0]["byteLength"] = len(pos_buffer+ind_buffer)
_glTF["meshes"] += [msh()]


print(out+'.gltf')
with open(out+'.gltf', 'wt') as outgltf:
    # outgltf.write(gltf)
    json.dump(_glTF, outgltf, indent=2)
