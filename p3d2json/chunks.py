import struct

# local imports
from enums import _locator_types, _event_types, _trigger_volume_types, _terrain_types

# root
def P3D(blob): return {}
CHUNKS = { b'\x50\x33\x44\xFF': P3D }


# fence walls idk dsg
def FenceDSG(blob): return {}
def Wall(blob):
    _start = struct.unpack('<3f',blob[:0xC])
    _end = struct.unpack('<3f',blob[0xC:0x18])
    _normal = struct.unpack('<3f',blob[0x18:0x24])
    return {'Start':{'X':_start[0],'Y':_start[1],'Z':_start[2]},'End':{'X':_end[0],'Y':_end[1],'Z':_end[2]},'Normal':{'X':_normal[0],'Y':_normal[1],'Z':_normal[2]}}
# CHUNKS = { **CHUNKS, **{ b'\x07\x00\xF0\x03': FenceDSG, b'\x00\x00\x00\x03': Wall }}


def IntersectDSG(blob):
    _num_indices, = struct.unpack('<I', blob[:0x4])
    # _indices = struct.unpack(f'<{_num_indices}I', blob[0x4:0x4+_num_indices*0x4])
    _indices = [struct.unpack('<3I',blob[i:i+0xC]) for i in range(0x4,0x4+_num_indices*0x4,0xC)]
    _num_positions, = struct.unpack('<I', blob[0x4+_num_indices*0x4:0x4+_num_indices*0x4+0x4])
    # _positions = struct.unpack(f'<{_num_positions*3}f', blob[0x4+_num_indices*0x4+0x4:0x4+_num_indices*0x4+0x4+_num_positions*0xC])
    _positions = [struct.unpack(f'3f', blob[i:i+0xC]) for i in range(0x4+_num_indices*0x4+0x4,0x4+_num_indices*0x4+0x4+_num_positions*0xC,0xC)]
    _num_normals, = struct.unpack('<I', blob[0x4+_num_indices*0x4+0x4+_num_positions*0xC:0x4+_num_indices*0x4+0x4+_num_positions*0xC+0x4])
    # _normals = struct.unpack(f'{_num_normals*3}f', blob[0x4+_num_indices*0x4+0x4+_num_positions*0xC+0x4:0x4+_num_indices*0x4+0x4+_num_positions*0xC+0x4+_num_normals*0xC])
    _normals = [struct.unpack(f'3f', blob[i:i+0xC]) for i in range(0x4+_num_indices*0x4+0x4+_num_positions*0xC+0x4,0x4+_num_indices*0x4+0x4+_num_positions*0xC+0x4+_num_normals*0xC,0xC)]
    return { 'Indices': _indices, 'Positions': _positions, 'Normals': _normals }
def BBox(blob):
    _box = struct.unpack('6f' ,blob[:0x1C])
    return { 'Box': _box }
# def BSphere(blob):
#     _sphere = struct.unpack('4f', blob[:0x1C])
#     return { 'Sphere': _sphere }
def TerrainType(blob):
    _version, = struct.unpack('<I', blob[:0x4])
    _num_types, = struct.unpack('<I', blob[0x4:0x8])
    _types = [_terrain_types[i] for i in struct.unpack(f'{_num_types}B', blob[0x8:0x8+_num_types])]
    # return { 'Version': _version, 'Types': _types }
    return { 'Types': _types }
# CHUNKS = { **CHUNKS, **{ b'\x03\x00\xF0\x03': IntersectDSG, b'\x03\x00\x01\x00': BBox, b'\x04\x00\x01\x00': BSphere, b'\x0E\x00\x00\x03': TerrainType }}


def TreeDSG(blob):
    _num_nodes, = struct.unpack('<I', blob[:0x4])
    _bounds_min = struct.unpack('3f', blob[0x4:0x10])
    _bounds_max = struct.unpack('3f', blob[0x10:0x1C])
    return { 'NumNodes': _num_nodes, 'BoundsMin': _bounds_min, 'BoundsMax': _bounds_max }
def ContiguousBinNode(blob):
    _sub_tree_size, _parent_offset = struct.unpack('<2I', blob[:0x8])
    return { 'SubTreeSize': _sub_tree_size, 'ParentOffset':_parent_offset }
def SpatialNode(blob):
    _plane_axis, _plane_posn, _num_s_entities, _num_s_phys, _num_intersects, _num_d_phys, _num_fences, _num_roads, _num_paths, _num_anims = struct.unpack('<Bf8I', blob[:0x37])
    return { 'PlaneAxis': _plane_axis, 'PlanePosn': _plane_posn, 'NumSEntities': _num_s_entities, 'NumSPhys': _num_s_phys, 'NumIntersects': _num_intersects, 'NumDPhys': _num_d_phys, 'NumFences': _num_fences, 'NumRoads': _num_roads, 'NumPaths': _num_paths, 'NumAnims': _num_anims }
# CHUNKS = { **CHUNKS, **{ b'\x04\x00\xF0\x03': TreeDSG, b'\x05\x00\xF0\x03': ContiguousBinNode, b'\x06\x00\xF0\x03': SpatialNode }}


# locators
def WBLocator(blob): # add more cases
    _name_size = blob[0]
    _name = struct.unpack(f'{_name_size}s', blob[0x1:0x1+_name_size])[0].decode('ascii').strip('\x00')
    _type = _locator_types[struct.unpack(f'I', blob[_name_size+0x1:_name_size+0x5])[0]]
    _num_elements, = struct.unpack(f'I', blob[_name_size+0x5:_name_size+0x9])
    match _type:
        case 'Event': _elements = [_event_types[i] for i in struct.unpack(f'<{_num_elements}I',blob[_name_size+0x9:_name_size+0x9+(_num_elements*4)])]
        case 'Script': _elements = struct.unpack(f'{_num_elements*4}s',blob[_name_size+0x9:_name_size+0x9+(_num_elements*4)])[0].decode('utf-8', 'replace').strip('\x00')
        case 'Car Start': _elements = struct.unpack(f'{_num_elements*3}f',blob[_name_size+0x9:_name_size+0x9+(_num_elements*12)])
        case 'Dynamic Zone': _elements = struct.unpack(f'{_num_elements*4}s',blob[_name_size+0x9:_name_size+0x9+(_num_elements*4)])[0].decode('utf-8', 'replace').strip('\x00')
        case _: _elements = struct.unpack(f'{_num_elements*4}s',blob[_name_size+0x9:_name_size+0x9+(_num_elements*4)])[0].decode('utf-8', 'replace')
    _position = struct.unpack(f'3f', blob[_name_size+0x9+(_num_elements*4):_name_size+0x9+(_num_elements*4)+0xC])
    _num_triggers, = struct.unpack(f'I', blob[_name_size+0x9+(_num_elements*4)+0xC:_name_size+0x9+(_num_elements*4)+0x10])
    return {'Name': _name, 'Type': _type, 'NumDataElements': _num_elements, 'Elements': _elements, 'Position': _position, 'NumTriggers': _num_triggers }
def WBTriggerVolume(blob):
    _name_size = blob[0]
    _name = struct.unpack(f'{_name_size}s', blob[0x1:0x1+_name_size])[0].decode('ascii').strip('\x00')
    _type = _trigger_volume_types[struct.unpack(f'I', blob[_name_size+0x1:_name_size+0x5])[0]]
    _scale = struct.unpack(f'3f', blob[_name_size+0x5:_name_size+0x11])
    _matrix = struct.unpack(f'16f', blob[_name_size+0x11:_name_size+0x51])
    return { 'Name': _name, 'Type': _type, 'Scale': _scale, 'Matrix': _matrix }
# CHUNKS = { **CHUNKS, **{ b'\x05\x00\x00\x03': WBLocator, b'\x06\x00\x00\x03': WBTriggerVolume }}


# TEXTURE
# def Texture(blob): return {}
# def Image(blob): return {}
# def ImageData(blob):
#     _size, = struct.unpack(f'<I', blob[:0x4])
#     # _image_data, = struct.unpack(f'{_size}s', blob[0x4:])
#     return {}
# def ImageFileName(blob): return {}
# def VolumeImage(blob): return {}
# def Sprite(blob): return {}
# CHUNKS = { **CHUNKS, **{ b'\x00\x90\x01\x00': Texture, b'\x01\x90\x01\x00': Image, b'\x02\x90\x01\x00': ImageData, b'\x03\x90\x01\x00': ImageFileName, b'\x04\x90\x01\x00': VolumeImage, b'\x05\x90\x01\x00': Sprite }}


# collision
def StaticPhysDSG(blob):
    _name_size = blob[0]
    _name = struct.unpack(f'{_name_size}s', blob[0x1:0x1+_name_size])[0].decode('ascii').strip('\x00')
    _version, = struct.unpack(f'<I', blob[0x1+_name_size:0x1+_name_size+4])
    return { "Name": _name, "Version": _version }
def CollisionObject(blob):
    _name_size = blob[0]
    _name = struct.unpack(f'{_name_size}s', blob[0x1:0x1+_name_size])[0].decode('ascii').strip('\x00')
    _version, = struct.unpack(f'<I', blob[0x1+_name_size:0x1+_name_size+4])
    return { 'Name': _name, "Version": _version }
def CollisionObjectAttribute(blob):
    _static_attribute, _default_area, _can_roll, _can_slide, _can_spin, can_bounce, _extra_attribute_1, _extra_attribute_2, _extra_attribute_3 = struct.unpack('<HI4H3I', blob[:0x20])
    return {'StaticAttribute': _static_attribute, 'CanRoll': _default_area, 'CanSlide': _can_roll, 'CanSpin': _can_slide, 'CanBounce': can_bounce, 'ExtraAttribute1': _extra_attribute_1, 'ExtraAttribute2': _extra_attribute_2, 'ExtraAttribute3': _extra_attribute_3 }
def CollisionVolumeOwner(blob):
    _num_names, = struct.unpack(f'<I', blob[:0x4])
    return { 'NumNames': _num_names }
def CollisionVolumeOwnerName(blob):
    _name_size = blob[0]
    _name = struct.unpack(f'{_name_size}s', blob[0x1:0x1+_name_size])[0].decode('ascii').strip('\x00')
    return { 'Name': _name }
def SelfCollision(blob):
    _joint_index_1, _joint_index2, _self_only_1, _self_only_2 = struct.unpack('<2I2H', blob[:0xC])
    return { 'JointIndex1': _joint_index_1, 'JointIndex2': _joint_index2, 'SelfOnly1': _self_only_1, 'SelfOnly2': _self_only_2 }
def CollisionVolume(blob):
    _object_reference_index, _owner_index, _num_sub_volume = struct.unpack(f'IiI', blob[:0xC])
    return { "ObjectReferenceIndex": _object_reference_index, "OwnerIndex": _owner_index, "NumSubVolume": _num_sub_volume }
def BBoxVolume(blob):
    _nothing, = struct.unpack(f'<I', blob[:0x4])
    return { 'Nothing': _nothing }
def SphereVolume(blob):
    _sphere_radius, = struct.unpack(f'f', blob[:0x4])
    return { 'SphereRadius': _sphere_radius }
def CylinderVolume(blob):
    _cylinder_radius, _length, _flat_end = struct.unpack(f'<2fH', blob[:0x10])
    return { 'CylinderRadius': _cylinder_radius, 'Length': _length, 'FlatEnd': _flat_end }
def OBBoxVolume(blob):
    _length_1, _length_2, _length_3 = struct.unpack('3f', blob[:0xC])
    return { 'Length1': _length_1, 'Length2': _length_2, 'Length3': _length_3 }
def WallVolume(blob): return {}
def CollisionVector(blob):
    _x, _y, _z = struct.unpack('3f', blob[:0xC])
    return { 'X': _x, 'Y': _y, 'Z': _z }
# CHUNKS = { **CHUNKS, **{ b'\x01\x00\xF0\x03': StaticPhysDSG, b'\x00\x00\x01\x07': CollisionObject, b'\x23\x00\x01\x07': CollisionObjectAttribute, b'\x21\x00\x01\x07': CollisionVolumeOwner, b'\x22\x00\x01\x07': CollisionVolumeOwnerName, b'\x20\x00\x01\x07': SelfCollision, b'\x01\x00\x01\x07': CollisionVolume, b'\x06\x00\x01\x07': BBoxVolume, b'\x02\x00\x01\x07': SphereVolume, b'\x03\x00\x01\x07': CylinderVolume, b'\x04\x00\x01\x07': OBBoxVolume, b'\x05\x00\x01\x07': WallVolume, b'\x07\x00\x01\x07': CollisionVector }}


# world sphere
def WorldSphereDSG(blob):
    _version, = struct.unpack('I', blob[:0x4])
    _num_meshes, = struct.unpack('I', blob[0x4:0x8])
    _num_bill_board_quads, = struct.unpack('I', blob[0x8:0xC])
    return { 'Version': _version, 'NumMeshes': _num_meshes, 'NumBillBoardQuads': _num_bill_board_quads }
def MultiController(blob): return {}
def FrameController(blob): return {}
def Skeleton(blob): return {}
def Animation(blob): return {}
def CompositeDrawable(blob): return {}
def BillboardQuadGroup(blob): return {}
def LensFlareDSG(blob): return {}
def RenderStatus(blob):
    _cast_shadow, = struct.unpack('I', blob[:0x4])
    return { 'CastShadow': _cast_shadow }
# CHUNKS = { **CHUNKS, **{ b'\x01\x00\xF0\x03': WorldSphereDSG }}


# MESH
def Mesh(blob):
    ''' subchunks
            PrimGroup
            BBox
            BSphere
            RenderStatus
            ExpressionOffsets '''
    _name_size = blob[0]
    _name = struct.unpack(f'{_name_size}s', blob[0x1:0x1+_name_size])[0].decode('ascii').strip('\x00')
    _version, = struct.unpack('I', blob[0x1+_name_size:0x1+_name_size+0x4])
    _num_prime_groups, = struct.unpack('I', blob[0x1+_name_size+0x4:0x1+_name_size+0x4+0x4])
    return { 'Name': _name, 'Version': _version, 'NumPrimGroups': _num_prime_groups }
def PrimeGroup(blob): return {}


CHUNKS = {
    b'\x50\x33\x44\xFF': P3D,

    # b'\x07\x00\xF0\x03': FenceDSG,
    # b'\x00\x00\x00\x03': Wall,

    b'\x03\x00\xF0\x03': IntersectDSG,
    # b'\x03\x00\x01\x00': BBox,
    # b'\x04\x00\x01\x00': BSphere,
    b'\x0E\x00\x00\x03': TerrainType,

    # b'\x04\x00\xF0\x03': TreeDSG,
    # b'\x05\x00\xF0\x03': ContiguousBinNode,
    # b'\x06\x00\xF0\x03': SpatialNode,

    # b'\x05\x00\x00\x03': WBLocator,
    # b'\x06\x00\x00\x03': WBTriggerVolume,

    # b'\x00\x90\x01\x00': Texture,
    # b'\x01\x90\x01\x00': Image,
    # b'\x02\x90\x01\x00': ImageData,
    # b'\x03\x90\x01\x00': ImageFileName,
    # b'\x04\x90\x01\x00': VolumeImage,
    # b'\x05\x90\x01\x00': Sprite,

    # b'\x01\x00\xF0\x03': StaticPhysDSG,
    # b'\x00\x00\x01\x07': CollisionObject,
    # b'\x23\x00\x01\x07': CollisionObjectAttribute,
    # b'\x21\x00\x01\x07': CollisionVolumeOwner,
    # b'\x22\x00\x01\x07': CollisionVolumeOwnerName,
    # b'\x20\x00\x01\x07': SelfCollision,
    # b'\x01\x00\x01\x07': CollisionVolume,
    # b'\x06\x00\x01\x07': BBoxVolume,
    # b'\x02\x00\x01\x07': SphereVolume,
    # b'\x03\x00\x01\x07': CylinderVolume,
    # b'\x04\x00\x01\x07': OBBoxVolume,
    # b'\x05\x00\x01\x07': WallVolume,
    # b'\x07\x00\x01\x07': CollisionVector,

    # b'\x0B\x00\xF0\x03': WorldSphereDSG,
    # b'\x00\x00\x01\x00': Mesh,

    # b'\x02\x00\x01\x00': PrimeGroup,

}









