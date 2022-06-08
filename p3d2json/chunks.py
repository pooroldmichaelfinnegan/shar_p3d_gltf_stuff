import struct

# local imports
from enums import _locator_types, _event_types, _trigger_volume_types

# root
def P3D(block): return {}
CHUNKS = { b'\x50\x33\x44\xFF': P3D }


# fence walls
def FenceDSG(block): return {}
def Wall(block):
    _start = struct.unpack('<3f',block[:0xC])
    _end = struct.unpack('<3f',block[0xC:0x18])
    _normal = struct.unpack('<3f',block[0x18:0x24])
    return {'Start':{'X':_start[0],'Y':_start[1],'Z':_start[2]},'End':{'X':_end[0],'Y':_end[1],'Z':_end[2]},'Normal':{'X':_normal[0],'Y':_normal[1],'Z':_normal[2]}}
CHUNKS = { **CHUNKS, **{ b'\x07\x00\xF0\x03': FenceDSG , b'\x00\x00\x00\x03': Wall }}


# locators
def WBLocator(block):
    _name_size = block[0]
    _name = struct.unpack(f'{_name_size}s', block[0x1:0x1+_name_size])[0].decode('ascii').strip('\x00')
    _type = _locator_types[struct.unpack(f'I', block[_name_size+0x1:_name_size+0x5])[0]]
    _num_elements, = struct.unpack(f'I', block[_name_size+0x5:_name_size+0x9])
    match _type:
        case 'Event': _elements = [_event_types[i] for i in struct.unpack(f'<{_num_elements}I',block[_name_size+0x9:_name_size+0x9+(_num_elements*4)])]
        case 'Script': _elements = struct.unpack(f'{_num_elements*4}s',block[_name_size+0x9:_name_size+0x9+(_num_elements*4)])[0].decode('utf-8', 'replace').strip('\x00')
        case 'Car Start': _elements = struct.unpack(f'{_num_elements*3}f',block[_name_size+0x9:_name_size+0x9+(_num_elements*12)])
        case 'Dynamic Zone': _elements = struct.unpack(f'{_num_elements*4}s',block[_name_size+0x9:_name_size+0x9+(_num_elements*4)])[0].decode('utf-8', 'replace').strip('\x00')
        case _: _elements = struct.unpack(f'{_num_elements*4}s',block[_name_size+0x9:_name_size+0x9+(_num_elements*4)])[0].decode('utf-8', 'replace')
    _position = struct.unpack(f'3f', block[_name_size+0x9+(_num_elements*4):_name_size+0x9+(_num_elements*4)+0xC])
    _num_triggers, = struct.unpack(f'I', block[_name_size+0x9+(_num_elements*4)+0xC:_name_size+0x9+(_num_elements*4)+0x10])
    return {'Name': _name, 'Type': _type, 'NumDataElements': _num_elements, 'Elements': _elements, 'Position': _position, 'NumTriggers': _num_triggers }
def WBTriggerVolume(block):
    _name_size = block[0]
    _name = struct.unpack(f'{_name_size}s', block[0x1:0x1+_name_size])[0].decode('ascii').strip('\x00')
    _type = _trigger_volume_types[struct.unpack(f'I', block[_name_size+0x1:_name_size+0x5])[0]]
    _scale = struct.unpack(f'3f', block[_name_size+0x5:_name_size+0x11])
    _matrix = struct.unpack(f'16f', block[_name_size+0x11:_name_size+0x51])
    return { 'Name': _name, 'Type': _type, 'Scale': _scale, 'Matrix': _matrix }
CHUNKS = { **CHUNKS, **{ b'\x05\x00\x00\x03': WBLocator, b'\x06\x00\x00\x03': WBTriggerVolume }}


# textures & images  # todo
# def Texture(block): return {}
# def Image(block): return {}
# def ImageData(block):
#     _size, = struct.unpack(f'<I', block[:0x4])
#     # _image_data, = struct.unpack(f'{_size}s', block[0x4:])
#     return {}
# def ImageFileName(block): return {}
# def VolumeImage(block): return {}
# def Sprite(block): return {}
# CHUNKS = { **CHUNKS, **{ b'\x00\x90\x01\x00': Texture, b'\x01\x90\x01\x00': Image, b'\x02\x90\x01\x00': ImageData, b'\x03\x90\x01\x00': ImageFileName, b'\x04\x90\x01\x00': VolumeImage, b'\x05\x90\x01\x00': Sprite }}


# collision  # todo
def CollisionObject(block): return {}
def CollisionObjectAttribute(block): return {}
def CollisionVolumeOwner(block): return {}
def CollisionVolumeOwnerName(block): return {}
def SelfCollision(block): return {}
def CollisionVolume(block): return {}
def BBoxVolume(block): return {}
def SphereVolume(block): return {}
def CylinderVolume(block): return {}
def OBBoxVolume(block): return {}
def WallVolume(block): return {}
def CollisionVector(block): return {}
