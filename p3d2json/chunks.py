import struct

# local imports
from enums import _locator_types, _event_types, _trigger_volume_types

# root
def P3D(block): return {}
CHUNKS = { b'\x50\x33\x44\xFF': P3D }


# fence walls idk dsg
def FenceDSG(block): return {}
def Wall(block):
    _start = struct.unpack('<3f',block[:0xC])
    _end = struct.unpack('<3f',block[0xC:0x18])
    _normal = struct.unpack('<3f',block[0x18:0x24])
    return {'Start':{'X':_start[0],'Y':_start[1],'Z':_start[2]},'End':{'X':_end[0],'Y':_end[1],'Z':_end[2]},'Normal':{'X':_normal[0],'Y':_normal[1],'Z':_normal[2]}}
# CHUNKS = { **CHUNKS, **{ b'\x07\x00\xF0\x03': FenceDSG, b'\x00\x00\x00\x03': Wall }}


def IntersectDSG(block):
    _num_indices, = struct.unpack('<I', block[:0x4])
    # _indices = struct.unpack(f'<{_num_indices}I', block[0x4:0x4+_num_indices*0x4])
    _indices = [struct.unpack('<3I',block[i:i+0xC]) for i in range(0x4,0x4+_num_indices*0x4,0xC)]
    _num_positions, = struct.unpack('<I', block[0x4+_num_indices*0x4:0x4+_num_indices*0x4+0x4])
    # _positions = struct.unpack(f'<{_num_positions*3}f', block[0x4+_num_indices*0x4+0x4:0x4+_num_indices*0x4+0x4+_num_positions*0xC])
    _positions = [struct.unpack(f'3f', block[i:i+0xC]) for i in range(0x4+_num_indices*0x4+0x4,0x4+_num_indices*0x4+0x4+_num_positions*0xC,0xC)]
    _num_normals, = struct.unpack('<I', block[0x4+_num_indices*0x4+0x4+_num_positions*0xC:0x4+_num_indices*0x4+0x4+_num_positions*0xC+0x4])
    # _normals = struct.unpack(f'{_num_normals*3}f', block[0x4+_num_indices*0x4+0x4+_num_positions*0xC+0x4:0x4+_num_indices*0x4+0x4+_num_positions*0xC+0x4+_num_normals*0xC])
    _normals = [struct.unpack(f'3f', block[i:i+0xC]) for i in range(0x4+_num_indices*0x4+0x4+_num_positions*0xC+0x4,0x4+_num_indices*0x4+0x4+_num_positions*0xC+0x4+_num_normals*0xC,0xC)]
    return { 'Indices': _indices, 'Positions': _positions, 'Normals': _normals }
def BBox(block):
    _box = struct.unpack('6f' ,block[:0x1C])
    return { 'Box': _box }
def BSphere(block):
    _sphere = struct.unpack('4f', block[:0x1C])
    return { 'Sphere': _sphere }
def TerrainType(block):
    _version, = struct.unpack('<I', block[:0x4])
    _num_types, = struct.unpack('<I', block[0x4:0x8])
    _types = struct.unpack(f'{_num_types}B', block[0x8:0x8+_num_types])
    return { 'Version': _version, 'Types': _types }
CHUNKS = { **CHUNKS, **{ b'\x03\x00\xF0\x03': IntersectDSG, b'\x03\x00\x01\x00': BBox, b'\x04\x00\x01\x00': BSphere, b'\x0E\x00\x00\x03': TerrainType }}


def TreeDSG(block):
    _num_nodes, = struct.unpack('<I', block[:0x4])
    _bounds_min = struct.unpack('3f', block[0x4:0x10])
    _bounds_max = struct.unpack('3f', block[0x10:0x1C])
    return { 'NumNodes': _num_nodes, 'BoundsMin': _bounds_min, 'BoundsMax': _bounds_max }
def ContiguousBinNode(block):
    _sub_tree_size, _parent_offset = struct.unpack('<2I', block[:0x8])
    return { 'SubTreeSize': _sub_tree_size, 'ParentOffset':_parent_offset }
def SpatialNode(block):
    _plane_axis, _plane_posn, _num_s_entities, _num_s_phys, _num_intersects, _num_d_phys, _num_fences, _num_roads, _num_paths, _num_anims = struct.unpack('<Bf8I', block[:0x37])
    return { 'PlaneAxis': _plane_axis, 'PlanePosn': _plane_posn, 'NumSEntities': _num_s_entities, 'NumSPhys': _num_s_phys, 'NumIntersects': _num_intersects, 'NumDPhys': _num_d_phys, 'NumFences': _num_fences, 'NumRoads': _num_roads, 'NumPaths': _num_paths, 'NumAnims': _num_anims }
# CHUNKS = { **CHUNKS, **{ b'\x04\x00\xF0\x03': TreeDSG, b'\x05\x00\xF0\x03': ContiguousBinNode, b'\x06\x00\xF0\x03': SpatialNode }}


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
# CHUNKS = { **CHUNKS, **{ b'\x05\x00\x00\x03': WBLocator, b'\x06\x00\x00\x03': WBTriggerVolume }}


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


# collision
def StaticPhysDSG(block):
    _name_size = block[0]
    _name = struct.unpack(f'{_name_size}s', block[0x1:0x1+_name_size])[0].decode('ascii').strip('\x00')
    _version, = struct.unpack(f'<I', block[0x1+_name_size:0x1+_name_size+4])
    return { "Name": _name, "Version": _version }
def CollisionObject(block):
    _name_size = block[0]
    _name = struct.unpack(f'{_name_size}s', block[0x1:0x1+_name_size])[0].decode('ascii').strip('\x00')
    _version, = struct.unpack(f'<I', block[0x1+_name_size:0x1+_name_size+4])
    return { 'Name': _name, "Version": _version }
def CollisionObjectAttribute(block):
    _static_attribute, _default_area, _can_roll, _can_slide, _can_spin, can_bounce, _extra_attribute_1, _extra_attribute_2, _extra_attribute_3 = struct.unpack('<HI4H3I', block[:0x20])
    return {'StaticAttribute': _static_attribute, 'CanRoll': _default_area, 'CanSlide': _can_roll, 'CanSpin': _can_slide, 'CanBounce': can_bounce, 'ExtraAttribute1': _extra_attribute_1, 'ExtraAttribute2': _extra_attribute_2, 'ExtraAttribute3': _extra_attribute_3 }
def CollisionVolumeOwner(block):
    _num_names, = struct.unpack(f'<I', block[:0x4])
    return { 'NumNames': _num_names }
def CollisionVolumeOwnerName(block):
    _name_size = block[0]
    _name = struct.unpack(f'{_name_size}s', block[0x1:0x1+_name_size])[0].decode('ascii').strip('\x00')
    return { 'Name': _name }
def SelfCollision(block):
    _joint_index_1, _joint_index2, _self_only_1, _self_only_2 = struct.unpack('<2I2H', block[:0xC])
    return { 'JointIndex1': _joint_index_1, 'JointIndex2': _joint_index2, 'SelfOnly1': _self_only_1, 'SelfOnly2': _self_only_2 }
def CollisionVolume(block):
    _object_reference_index, = struct.unpack(f'<I', block[:0x4])
    _owner_index, = struct.unpack(f'<I', block[0x4:0x8])
    _num_sub_volume, = struct.unpack(f'<I', block[0x8:0xC])
    return { "ObjectReferenceIndex": _object_reference_index, "OwnerIndex": _owner_index, "NumSubVolume": _num_sub_volume }
def BBoxVolume(block):
    _nothing, = struct.unpack(f'<I', block[:0x4])
    return { 'Nothing': _nothing }
def SphereVolume(block):
    _sphere_radius, = struct.unpack(f'f', block[:0x4])
    return { 'SphereRadius': _sphere_radius }
def CylinderVolume(block):
    _cylinder_radius, _length, _flat_end = struct.unpack(f'<2fH', block[:0x10])
    return { 'CylinderRadius': _cylinder_radius, 'Length': _length, 'FlatEnd': _flat_end }
def OBBoxVolume(block):
    _length_1, _length_2, _length_3 = struct.unpack('3f', block[:0xC])
    return { 'Length1': _length_1, 'Length2': _length_2, 'Length3': _length_3 }
def WallVolume(block): return {}
def CollisionVector(block):
    _x, _y, _z = struct.unpack('3f', block[:0xC])
    return { 'X': _x, 'Y': _y, 'Z': _z }
# CHUNKS = { **CHUNKS, **{ b'\x01\x00\xF0\x03': StaticPhysDSG, b'\x00\x00\x01\x07': CollisionObject, b'\x23\x00\x01\x07': CollisionObjectAttribute, b'\x21\x00\x01\x07': CollisionVolumeOwner, b'\x22\x00\x01\x07': CollisionVolumeOwnerName, b'\x20\x00\x01\x07': SelfCollision, b'\x01\x00\x01\x07': CollisionVolume, b'\x06\x00\x01\x07': BBoxVolume, b'\x02\x00\x01\x07': SphereVolume, b'\x03\x00\x01\x07': CylinderVolume, b'\x04\x00\x01\x07': OBBoxVolume, b'\x05\x00\x01\x07': WallVolume, b'\x07\x00\x01\x07': CollisionVector }}