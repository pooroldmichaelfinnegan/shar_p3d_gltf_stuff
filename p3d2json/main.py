
import json, sys

from chunks import *
from list_of_chunk_ids import chunk_id_list

# I = sys.argv[1]
# O = sys.argv[2]
region = 'z6'

# with open('./p3ds/flandersHouse.p3d', 'rb') as file:  # modified p3ds to test on
# with open('./p3ds/l4/loadZones.p3d', 'rb') as file:   # 
# with open('./p3ds/l4/sr1_.p3d', 'rb') as file:        # 

# with open('./p3ds/L1_TERRA.p3d', 'rb') as file:
with open(f'./p3ds/l1z1.p3d', 'rb') as file:
# with open(I, 'rb') as file:
    p3d_file = file.read()

counter = {}
uid = {}


def out_chunk_ids(chunk_id, data_size):
    chunk_id_decoded = chunk_id.decode('utf-8', 'replace')
    if chunk_id not in chunk_id_list:
        name = chunk_id_decoded
        chunk_data = CHUNKS[chunk_id](blob[8:data_size])
    else:
        # name = CHUNKS[chunk_id].__name__
        name = f'{chunk_id_decoded}    {chunk_id_list[chunk_id]}'
        chunk_data = {}


def filter(child_list: dict) -> dict:
    temp_list = []
    # if child_list:
    for v in child_list:
        if v: temp_list += [v]
    child_list = temp_list


def out():
    return {  }

class Chunk:
    def __init__(self, blob):
        self.chunk_id = blob[:0x4]
        self.header_size = 0xC
        self.child_list = []
        self.data_size = int.from_bytes(blob[0x4:0x8], 'little')
        self.chunk_size = int.from_bytes(blob[0x8:0xC], 'little')
        # self.next_sibling = blob[self.chunk_size:self.chunk_size+self.header_size]
        # self.child_size = int.from_bytes(blob[self.data_size+0x8:self.data_size+0xC], 'little')
    def decoded(self, raw: bytes) -> bytes:
        return raw.decode('utf-8', 'replace')
    def filter_child_list(self):
        temp_list = []
        for v in self.child_list:
            if v:
                temp_list += [v]
        self.child_list = temp_list


def _next(blob):
    chunk = Chunk(blob)

    _sum = 0
    while chunk.data_size+_sum < chunk.chunk_size:
        chunk.child_size = int.from_bytes(blob[chunk.data_size+_sum+0x8:chunk.data_size+_sum+0xC], 'little')
        chunk.child_list += [ _next(blob[chunk.data_size+_sum:]) ]
        _sum += chunk.child_size

    ## chunk counter
    global uid
    counter_item = chunk_id_list[chunk.chunk_id]
    if counter_item not in uid: uid[counter_item] = 1
    else: uid[counter_item] += 1

        # print(name)
        # json.dumps(chunk_data)  # catch non-json compatible types
    # if chunk.chunk_id not in CHUNKS:
    #     return chunk_id_list[chunk.chunk_id]

    chunk.filter_child_list()

    if chunk.chunk_id in CHUNKS:
        name = CHUNKS[chunk.chunk_id].__name__
        chunk_data = CHUNKS[chunk.chunk_id](blob[0xC:chunk.data_size])
        return { name: [chunk_data, chunk.child_list] }


    ## output readable chunk id tree hierarchy
    # if chunk_id not in chunk_id_list: name = chunk_id.decode('ascii', 'replace')
    # else: name = chunk_id_list[chunk_id].lower()


    # return { f'{name}_{uid[name]}': child_list }


    ## for filtering out empty lists and dicts, removed because traversing the jsons after is a pain
    # if chunk_data and child_list:
        # return { name: [chunk_data, child_list] }
    # elif not chunk_data and child_list:
    #     return { name: child_list }
    # elif chunk_data and not child_list:
    #     return { name: chunk_data }
    # else: return name


# I2 = I[:-4] + '.json'

print(uid)

if __name__ == '__main__':
    ret = _next(p3d_file)
    print(ret)
    with open(f'./dump.json', 'wt') as dump:
        json.dump(ret, dump, indent=2)
    with open('./dump.txt', 'wt') as dump:
        for key, value in uid.items():
            dump.write(f'{value:5} {key.lower()}\n')
