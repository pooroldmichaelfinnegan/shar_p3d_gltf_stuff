
import json, sys

# local imports
from chunks import *
from list_of_chunk_ids import chunk_id_list  # for hacky chunk counter

# I = sys.argv[1]
# O = sys.argv[2]

# with open('./p3ds/flandersHouse.p3d', 'rb') as file:  # modified p3ds to test on
# with open('./p3ds/l4/loadZones.p3d', 'rb') as file:   # 
# with open('./p3ds/l4/sr1_.p3d', 'rb') as file:        # 

with open('./p3ds/L1_TERRA.p3d', 'rb') as file:
# with open('./p3ds/l1z1.p3d', 'rb') as file:
# with open(I, 'rb') as file:
    p3d_file = file.read()

counter = {}

def _next(block):
    global counter
    header, chunk_id = 0xC, block[:0x4]
    data_size = int.from_bytes(block[0x4:0x8], 'little')
    chunk_size = int.from_bytes(block[0x8:0xC], 'little')
    # next_sibling = block[chunk_size:chunk_size+header]
    # child_size = int.from_bytes(block[data_size+0x8:data_size+0xC], 'little')

    child_list, _sum = [], 0
    while data_size+_sum < chunk_size:
        # print(chunk_id, data_size + _sum)
        child_size = int.from_bytes(block[data_size+_sum+0x8:data_size+_sum+0xC], 'little')
        child_list += [_next(block[data_size+_sum:])]  # append child_list
        _sum += child_size  # move to next child

    # chunk_raw_data = block[header:data_size].decode('utf-8', 'replace')

    temp_list = []
    if child_list:
        for v in child_list:
            if v: temp_list += [v]
    child_list = temp_list

    name = ''
    if chunk_id not in CHUNKS:
        chunk_data = {};return {}
        # if chunk_id in chunk_id_list: name = chunk_id.decode('ascii', 'replace')
        # else: name = chunk_id_list[chunk_id]
    else:
        name = CHUNKS[chunk_id].__name__
        print(name, chunk_id, data_size, chunk_size)
        chunk_data = CHUNKS[chunk_id](block[header:data_size])

        # print(name)
        # json.dumps(chunk_data)  # catch non json compatible types


    if chunk_data and child_list:
        return { name: [chunk_data, child_list] }
    elif not chunk_data and child_list:
        return { name: child_list }
    elif chunk_data and not child_list:
        return { name: chunk_data }
    else: return name

# I2 = I[:-4] + '.json'


if __name__ == '__main__':
    ret = _next(p3d_file)
    # print(ret)
    # with open(I2, 'wt') as dump:
    #     json.dump(ret, dump, indent=2)
    # for i in counter:
    #     if i in chunk_id_list: print(counter[i], chunk_id_list[i])
    #     else: print(counter[i], i)