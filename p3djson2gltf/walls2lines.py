from struct import pack, unpack
import json

# with open('./flandersHouse.json', 'rt') as p3djson:
with open('./l1_fences.json', 'rt') as p3djson:
    d = json.loads(p3djson.read())
    # print(d)
# with open('./gltftemp.json', 'rt') as gltftemp:
#     gltf = json.loads(gltftemp.read())


# m = 'w'; fhb = open('./flandersHouse.bin', f'{m}b')
b, N, l = b'', b'', []
ss = []

for chunk in d['P3D']:
    # print(list(chunk)[0])
    if list(chunk)[0] == 'FenceDSG':
        # ss += [chunk['FenceDSG'][0]['Wall']['Start']['Z']]
        *sxy, sz = chunk['FenceDSG'][0]['Wall']['Start'].values()
        sz *= -1; s = pack('3f', *sxy, sz)

        *exy, ez = chunk['FenceDSG'][0]['Wall']['End'].values()
        ez *= -1; e = pack('3f', *exy, ez)

        *nxy, nz = chunk['FenceDSG'][0]['Wall']['Normal'].values()
        nz *= -1; n = pack('3f', *nxy, nz)
        # print(n)

        b += s + e
        N += n

print(n)

with open('./L1_l_sen_opposite_z.bin', 'wb') as fhb:
    fhb.write(b+N)

fhb.close()    
# print(ss)
# print(min(ss), max(ss))
