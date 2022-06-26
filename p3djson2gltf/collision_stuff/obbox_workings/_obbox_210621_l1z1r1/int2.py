from struct import pack, unpack
import json


with open('../l1z2_col_chunks.json', 'rt') as p3djson:
    d = json.loads(p3djson.read())

s = []

# print(d)

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


def intersect(box):
    

with open('./dump.txt', 'wt') as outgltf:
    # outgltf.write(gltf)
    json.dump(s, outgltf, indent=2)
