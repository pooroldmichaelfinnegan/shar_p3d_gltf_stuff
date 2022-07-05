import struct

# local imports
from enums import locator_types, event_types, trigger_volume_types, terrain_types

# root
def P3D(blob): return {}
# CHUNKS = { b'\x50\x33\x44\xFF': P3D }


def float6(fl: float) -> float:
    ''' turn float to float of 6 decimal places, dont know why struct.unpack returns 17'''
    return float(f'{fl:.6f}')


# fence walls idk dsg
def FenceDSG(blob): return {}
def Wall(blob):
    start = struct.unpack('<3f',blob[:0xC])
    end = struct.unpack('<3f',blob[0xC:0x18])
    normal = struct.unpack('<3f',blob[0x18:0x24])
    return {'Start':{'X':start[0],'Y':start[1],'Z':start[2]},'End':{'X':end[0],'Y':end[1],'Z':end[2]},'Normal':{'X':normal[0],'Y':normal[1],'Z':normal[2]}}
# CHUNKS = { **CHUNKS, **{ b'\x07\x00\xF0\x03': FenceDSG, b'\x00\x00\x00\x03': Wall }}


def IntersectDSG(blob):
    num_indices, = struct.unpack('<I', blob[:0x4])
    # indices = struct.unpack(f'<{num_indices}I', blob[0x4:0x4+num_indices*0x4])
    indices = [struct.unpack('3I',blob[i:i+0xC]) for i in range(0x4,0x4+num_indices*0x4,0xC)]
    num_positions, = struct.unpack('<I', blob[0x4+num_indices*0x4:0x4+num_indices*0x4+0x4])
    # positions = struct.unpack(f'<{num_positions*3}f', blob[0x4+num_indices*0x4+0x4:0x4+num_indices*0x4+0x4+num_positions*0xC])
    positions = [struct.unpack(f'3f', blob[i:i+0xC]) for i in range(0x4+num_indices*0x4+0x4,0x4+num_indices*0x4+0x4+num_positions*0xC,0xC)]
    num_normals, = struct.unpack('I', blob[0x4+num_indices*0x4+0x4+num_positions*0xC:0x4+num_indices*0x4+0x4+num_positions*0xC+0x4])
    # normals = struct.unpack(f'{num_normals*3}f', blob[0x4+num_indices*0x4+0x4+num_positions*0xC+0x4:0x4+num_indices*0x4+0x4+num_positions*0xC+0x4+num_normals*0xC])
    normals = [struct.unpack(f'3f', blob[i:i+0xC]) for i in range(0x4+num_indices*0x4+0x4+num_positions*0xC+0x4,0x4+num_indices*0x4+0x4+num_positions*0xC+0x4+num_normals*0xC,0xC)]
    return { 'Indices': indices, 'Positions': positions, 'Normals': normals }
def BBox(blob):
    box = struct.unpack('6f' ,blob[:0x1C])
    return { 'Box': box }
def BSphere(blob): return {}
def TerrainType(blob):
    version, = struct.unpack('<I', blob[:0x4])
    num_types, = struct.unpack('<I', blob[0x4:0x8])
    types = [terrain_types[i] for i in struct.unpack(f'{num_types}B', blob[0x8:0x8+num_types])]
    # return { 'Version': version, 'Types': types }
    return { 'Types': types }
# CHUNKS = { **CHUNKS, **{ b'\x03\x00\xF0\x03': IntersectDSG, b'\x03\x00\x01\x00': BBox, b'\x04\x00\x01\x00': BSphere, b'\x0E\x00\x00\x03': TerrainType }}


def TreeDSG(blob):
    num_nodes, = struct.unpack('<I', blob[:0x4])
    bounds_min = struct.unpack('3f', blob[0x4:0x10])
    bounds_max = struct.unpack('3f', blob[0x10:0x1C])
    return { 'NumNodes': num_nodes, 'BoundsMin': bounds_min, 'BoundsMax': bounds_max }
def ContiguousBinNode(blob):
    sub_tree_size, parent_offset = struct.unpack('<2I', blob[:0x8])
    return { 'SubTreeSize': sub_tree_size, 'ParentOffset':parent_offset }
def SpatialNode(blob):
    plane_axis, plane_posn, num_s_entities, num_s_phys, num_intersects, num_d_phys, num_fences, num_roads, num_paths, num_anims = struct.unpack('<Bf8I', blob[:0x37])
    return { 'PlaneAxis': plane_axis, 'PlanePosn': plane_posn, 'NumSEntities': num_s_entities, 'NumSPhys': num_s_phys, 'NumIntersects': num_intersects, 'NumDPhys': num_d_phys, 'NumFences': num_fences, 'NumRoads': num_roads, 'NumPaths': num_paths, 'NumAnims': num_anims }
# CHUNKS = { **CHUNKS, **{ b'\x04\x00\xF0\x03': TreeDSG, b'\x05\x00\xF0\x03': ContiguousBinNode, b'\x06\x00\xF0\x03': SpatialNode }}


# locators
def WBLocator(blob): # add more cases
    name_size = blob[0]
    name = struct.unpack(f'{name_size}s', blob[0x1:0x1+name_size])[0].decode('ascii').strip('\x00')
    type = locator_types[struct.unpack(f'I', blob[name_size+0x1:name_size+0x5])[0]]
    num_elements, = struct.unpack(f'I', blob[name_size+0x5:name_size+0x9])
    match type:
        case 'Event': elements = [event_types[i] for i in struct.unpack(f'<{num_elements}I',blob[name_size+0x9:name_size+0x9+(num_elements*4)])]
        case 'Script': elements = struct.unpack(f'{num_elements*4}s',blob[name_size+0x9:name_size+0x9+(num_elements*4)])[0].decode('utf-8', 'replace').strip('\x00')
        case 'Car Start': elements = struct.unpack(f'{num_elements*3}f',blob[name_size+0x9:name_size+0x9+(num_elements*12)])
        case 'Dynamic Zone': elements = struct.unpack(f'{num_elements*4}s',blob[name_size+0x9:name_size+0x9+(num_elements*4)])[0].decode('utf-8', 'replace').strip('\x00')
        case _: elements = struct.unpack(f'{num_elements*4}s',blob[name_size+0x9:name_size+0x9+(num_elements*4)])[0].decode('utf-8', 'replace')
    position = struct.unpack(f'3f', blob[name_size+0x9+(num_elements*4):name_size+0x9+(num_elements*4)+0xC])
    num_triggers, = struct.unpack(f'I', blob[name_size+0x9+(num_elements*4)+0xC:name_size+0x9+(num_elements*4)+0x10])
    return {'Name': name, 'Type': type, 'NumDataElements': num_elements, 'Elements': elements, 'Position': position, 'NumTriggers': num_triggers }
def WBTriggerVolume(blob):
    name_size = blob[0]
    name = struct.unpack(f'{name_size}s', blob[0x1:0x1+name_size])[0].decode('ascii').strip('\x00')
    type = trigger_volume_types[struct.unpack(f'I', blob[name_size+0x1:name_size+0x5])[0]]
    scale = struct.unpack(f'3f', blob[name_size+0x5:name_size+0x11])
    matrix = struct.unpack(f'16f', blob[name_size+0x11:name_size+0x51])
    return { 'Name': name, 'Type': type, 'Scale': scale, 'Matrix': matrix }
# CHUNKS = { **CHUNKS, **{ b'\x05\x00\x00\x03': WBLocator, b'\x06\x00\x00\x03': WBTriggerVolume }}


# TEXTURE
def TextureChunk(blob):
    name_size = blob[0]
    name = struct.unpack(f'{name_size}s', blob[0x1:0x1+name_size])[0].decode('ascii').strip('\x00')
    version = struct.unpack(f'<I', blob[0x1+name_size:0x1+name_size+0x4])
    width = struct.unpack(f'<I', blob[0x1+name_size+0x4:0x1+name_size+0x8])
    height = struct.unpack(f'<I', blob[0x1+name_size+0x8:0x1+name_size+0xC])
    bpp = struct.unpack(f'<I', blob[0x1+name_size+0xC:0x1+name_size+0x14])
    alpha_depth = struct.unpack(f'<I', blob[0x1+name_size+0x14:0x1+name_size+0x18])
    num_mip_maps = struct.unpack(f'<I', blob[0x1+name_size+0x18:0x1+name_size+0x1C])
    texture_type = struct.unpack(f'<I', blob[0x1+name_size+0x1C:0x1+name_size+0x20])
    usage = struct.unpack(f'<I', blob[0x1+name_size+0x20:0x1+name_size+0x24])
    priority = struct.unpack(f'<I', blob[0x1+name_size+0x24:0x1+name_size+0x28])
    return { 'Name': name, 'Version': version, 'Width': width, 'Height': height, 'Bpp': bpp, 'AlphaDepth': alpha_depth, 'NumMipMaps': num_mip_maps, 'TextureType': texture_type, 'Usage': usage, 'Priority': priority }
def ImageChunk(blob):
    name_size = blob[0]
    name = struct.unpack(f'{name_size}s', blob[0x1:0x1+name_size])[0].decode('ascii').strip('\x00')
    version = struct.unpack(f'<I', blob[0x1+name_size:0x1+name_size+0x4])
    width = struct.unpack(f'<I', blob[0x1+name_size+0x4:0x1+name_size+0x8])
    height = struct.unpack(f'<I', blob[0x1+name_size+0x8:0x1+name_size+0xC])
    bpp = struct.unpack(f'<I', blob[0x1+name_size+0xC:0x1+name_size+0x14])
    palettized = struct.unpack(f'<I', blob[0x1+name_size+0x14:0x1+name_size+0x18])
    has_alpha = struct.unpack(f'<I', blob[0x1+name_size+0x18:0x1+name_size+0x1C])
    format = struct.unpack(f'<I', blob[0x1+name_size+0x1C:0x1+name_size+0x20])
    return { 'Name': name, 'Version': version, 'Width': width, 'Height': height, 'Bpp': bpp, 'Palettized': palettized, 'HasAlpha': has_alpha, 'Format': format }
def ImageDataChunk(blob):  # not str
    size, = struct.unpack(f'<I', blob[:0x4])
    image_data = struct.unpack(f'{size}s', blob[0x4:])
    return { 'Size': size, 'ImageData': image_data }
def ImageFileNameChunk(blob):
    size, = struct.unpack(f'<I', blob[:0x4])
    file_name = struct.unpack(f'{size}s', blob[0x4:])
    return { 'FileName': file_name }
def VolumeImageChunk(blob):
    name_size = blob[0]
    name = struct.unpack(f'{name_size}s', blob[0x1:0x1+name_size])[0].decode('ascii').strip('\x00')
    version = struct.unpack(f'<I', blob[0x1+name_size:0x1+name_size+0x4])
    width = struct.unpack(f'<I', blob[0x1+name_size+0x4:0x1+name_size+0x8])
    height = struct.unpack(f'<I', blob[0x1+name_size+0x8:0x1+name_size+0xC])
    bpp = struct.unpack(f'<I', blob[0x1+name_size+0xC:0x1+name_size+0x14])
    palettized = struct.unpack(f'<I', blob[0x1+name_size+0x14:0x1+name_size+0x18])
    has_alpha = struct.unpack(f'<I', blob[0x1+name_size+0x18:0x1+name_size+0x1C])
    format = struct.unpack(f'<I', blob[0x1+name_size+0x1C:0x1+name_size+0x20])
    version, width, height, bpp, palettized, has_alpha, format =  struct.unpack(f'<I', blob[0x1+name_size:0x1+name_size+0x20])
    return { 'Name': name, 'Version': version, 'Width': width, 'Height': height, 'Bpp': bpp, 'Palettized': palettized, 'HasAlpha': has_alpha, 'Format': format }
def Sprite(blob):
    name_size = blob[0x0]
    name = struct.unpack(f'{name_size}s', blob[0x1:0x1+name_size])[0].decode('ascii').strip('\x00')
    native_x = struct.unpack(f'<I', blob[0x1+name_size:0x1+name_size+0x4])
    native_y = struct.unpack(f'<I', blob[0x1+name_size+0x4:0x1+name_size+0x8])
    shader_size = blob[0x1+name_size+0x8]
    shader = struct.unpack(f'{name_size}s', blob[0x1+name_size+0x9:0x1+name_size+0x9+shader_size])[0].decode('ascii').strip('\x00')
    image_width = struct.unpack(f'<I', blob[0x1+name_size+0x9+shader_size:0x1+name_size+0x9+shader_size+0x4])
    image_height = struct.unpack(f'<I', blob[0x1+name_size+0x9+shader_size+0x4:0x1+name_size+0x9+shader_size+0x8])
    image_count = struct.unpack(f'<I', blob[0x1+name_size+0x9+shader_size+0x8:0x1+name_size+0x9+shader_size+0xC])
    blit_border = struct.unpack(f'<I', blob[0x1+name_size+0x9+shader_size+0xC:0x1+name_size+0x9+shader_size+0x10])
    return { 'Name': name, 'NativeX': native_x, 'NativeY': native_y, 'Shader': shader, 'ImageWidth': image_width, 'ImageHeight': image_height, 'ImageCount': image_count, 'BlitBorder': blit_border }
# CHUNKS = { **CHUNKS, **{ b'\x00\x90\x01\x00': Texture, b'\x01\x90\x01\x00': Image, b'\x02\x90\x01\x00': ImageData, b'\x03\x90\x01\x00': ImageFileName, b'\x04\x90\x01\x00': VolumeImage, b'\x05\x90\x01\x00': Sprite }}


# collision
def StaticPhysDSG(blob):
    name_size = blob[0]
    name = struct.unpack(f'{name_size}s', blob[0x1:0x1+name_size])[0].decode('ascii').strip('\x00')
    version, = struct.unpack(f'<I', blob[0x1+name_size:0x1+name_size+4])
    return { "Name": name, "Version": version }
def CollisionObject(blob):
    name_size = blob[0]
    name = struct.unpack(f'{name_size}s', blob[0x1:0x1+name_size])[0].decode('ascii').strip('\x00')
    version, = struct.unpack(f'<I', blob[0x1+name_size:0x1+name_size+4])
    return { 'Name': name, "Version": version }
def CollisionObjectAttribute(blob):
    static_attribute, default_area, can_roll, can_slide, can_spin, can_bounce, extra_attribute_1, extra_attribute_2, extra_attribute_3 = struct.unpack('<HI4H3I', blob[:0x20])
    return {'StaticAttribute': static_attribute, 'CanRoll': default_area, 'CanSlide': can_roll, 'CanSpin': can_slide, 'CanBounce': can_bounce, 'ExtraAttribute1': extra_attribute_1, 'ExtraAttribute2': extra_attribute_2, 'ExtraAttribute3': extra_attribute_3 }
def CollisionVolumeOwner(blob):
    num_names, = struct.unpack(f'<I', blob[:0x4])
    return { 'NumNames': num_names }
def CollisionVolumeOwnerName(blob):
    name_size = blob[0]
    name = struct.unpack(f'{name_size}s', blob[0x1:0x1+name_size])[0].decode('ascii').strip('\x00')
    return { 'Name': name }
def SelfCollision(blob):
    joint_index_1, joint_index2, self_only_1, self_only_2 = struct.unpack('<2I2H', blob[:0xC])
    return { 'JointIndex1': joint_index_1, 'JointIndex2': joint_index2, 'SelfOnly1': self_only_1, 'SelfOnly2': self_only_2 }
def CollisionVolume(blob):
    object_reference_index, owner_index, num_sub_volume = struct.unpack(f'IiI', blob[:0xC])
    return { "ObjectReferencIndex": object_reference_index, "OwnerIndex": owner_index, "NumSubVolume": num_sub_volume }
def BBoxVolume(blob):
    nothing, = struct.unpack(f'<I', blob[:0x4])
    return { 'Nothing': nothing }
def SphereVolume(blob):
    sphere_radius, = struct.unpack(f'f', blob[:0x4])
    return { 'SphereRadius': sphere_radius }
def CylinderVolume(blob):
    cylinder_radius, length, flat_end = struct.unpack(f'<2fH', blob[:0x10])
    return { 'CylinderRadius': cylinder_radius, 'Length': length, 'FlatEnd': flat_end }
def OBBoxVolume(blob):
    length_1, length_2, length_3 = struct.unpack('f', blob[:0xC])
    # length_1, length_2, length_3 = struct.unpack('3f', blob[:0xC])
    return { 'Length1': length_1, 'Length2': length_2, 'Length3': length_3 }
def WallVolume(blob): return {}
def CollisionVector(blob):
    x, y, z = struct.unpack('3f', blob[:0xC])
    return { 'X': x, 'Y': y, 'Z': z }
    # return { 'X': x, 'Y': y, 'Z': z }
# CHUNKS = { **CHUNKS, **{ b'\x01\x00\xF0\x03': StaticPhysDSG, b'\x00\x00\x01\x07': CollisionObject, b'\x23\x00\x01\x07': CollisionObjectAttribute, b'\x21\x00\x01\x07': CollisionVolumeOwner, b'\x22\x00\x01\x07': CollisionVolumeOwnerName, b'\x20\x00\x01\x07': SelfCollision, b'\x01\x00\x01\x07': CollisionVolume, b'\x06\x00\x01\x07': BBoxVolume, b'\x02\x00\x01\x07': SphereVolume, b'\x03\x00\x01\x07': CylinderVolume, b'\x04\x00\x01\x07': OBBoxVolume, b'\x05\x00\x01\x07': WallVolume, b'\x07\x00\x01\x07': CollisionVector }}


# world sphere
def WorldSphereDSG(blob):
    version, = struct.unpack('I', blob[:0x4])
    num_meshes, = struct.unpack('I', blob[0x4:0x8])
    num_bill_board_quads, = struct.unpack('I', blob[0x8:0xC])
    return { 'Version': version, 'NumMeshes': num_meshes, 'NumBillBoardQuads': num_bill_board_quads }
def MultiController(blob): return {}
def FrameController(blob): return {}
def Skeleton(blob): return {}
def Animation(blob): return {}
def CompositeDrawable(blob): return {}
def BillboardQuadGroup(blob): return {}
def LensFlareDSG(blob): return {}
def RenderStatus(blob):
    cast_shadow, = struct.unpack('I', blob[:0x4])
    return { 'CastShadow': cast_shadow }
# CHUNKS = { **CHUNKS, **{ b'\x01\x00\xF0\x03': WorldSphereDSG }}


# MESH
def Mesh(blob):
    name_size = blob[0x0]
    name = struct.unpack(f'{name_size}s', blob[0x1:0x1+name_size])[0].decode('ascii').strip('\x00')
    version, = struct.unpack('I', blob[0x1+name_size:0x1+name_size+0x4])
    num_prime_groups, = struct.unpack('I', blob[0x1+name_size+0x4:0x1+name_size+0x4+0x4])
    return { 'Name': name, 'Version': version, 'NumPrimGroups': num_prime_groups }
def PrimeGroupChunk(blob):
    version, = struct.unpack(f'I', blob[:0x4])
    string_size = blob[0x0]
    shader = struct.unpack(f'{string_size}s', blob[0x5:0x5+string_size])[0].decode('utf-8').strip('\x00')
    primitive_type, = struct.unpack(f'<I', blob[0x5+string_size:0x5+string_size+0x4])
    vertex_type, = struct.unpack(f'<I', blob[0x5+string_size+0x4:0x5+string_size+0x8])
    primitive_type, = struct.unpack(f'<I', blob[0x5+string_size+0x8:0x5+string_size+0xC])
    num_vertices, = struct.unpack(f'<I', blob[0x5+string_size+0xC:0x5+string_size+0x10])
    num_indices, = struct.unpack(f'<I', blob[0x5+string_size+0x10:0x5+string_size+0x14])
    num_matrices, = struct.unpack(f'<I', blob[0x5+string_size+0x14:0x5+string_size+0x18])
    return {'Version': version, 'Shader': shader, 'PrimitiveType': primitive_type, 'VertexType': vertex_type, 'NumVertices': num_vertices, 'NumIndices': num_indices, 'NumMatrices': num_matrices }
def VertexShader(blob):
    vertex_shader_name_size = blob[0x0]
    vertex_shader_name = struct.unpack(f'{vertex_shader_name_size}s', blob[:vertex_shader_name_size])[0].decode('ascii').strip('\x00')
    return { 'VertexShaderName': vertex_shader_name }
def PositionList(blob):
    num_positions, = struct.unpack(f'I', blob[:0x4])
    positions = [ list(struct.unpack('3f', blob[i:i+0xC])) for i in range(0x4,0x4+num_positions*0xC,0xC) ]
    return { 'NumPositions': num_positions, 'Positions': positions }
def NormalList(blob):
    num_normals, = struct.unpack(f'<I', blob[:0x4])
    normals = [ struct.unpack('f', i) for i in blob[0x4:num_normals*0x4]]
    return { 'NumNormals': num_normals, 'Normals': normals }
def PackedNormalList(blob):
    num_normals = blob[0x0]
    normals = ...
    return { 'NumNormals': num_normals, 'Normals': normals }
def ColourList(blob):
    num_colors, = struct.unpack(f'I', blob[:0x4])
    colours = ...
    return { 'NumColours': num_colors, 'Colours': colours }
def MultiColourList(blob):
    num_colours, = struct.unpack(f'<I', blob[:0x4])
    channel, = struct.unpack(f'I', blob[0x4:0x8])
    colours = ...
    return { 'NumColours': num_colours, 'Channel': channel, 'Colours': colours }
def StripList(blob):
    num_strips, = struct.unpack(f'<I', blob[:0x4])
    strips = ...
    return { 'NumStrips': num_strips, 'Strips': strips }
def IndexList(blob):
    num_indices, = struct.unpack(f'I', blob[:0x4])
    indices = [struct.unpack('I',blob[i:i+0x4])[0] for i in range(0x4,0x4+num_indices*0x4,0x4)]
    return { 'NumIndices': num_indices, 'Indices': indices }
def MatrixList(blob):
    num_matrices = struct.unpack(f'<I', blob[:0x4])
    matrices = ...  # colour type
    return { 'NumMatrices': num_matrices, 'Matrices': matrices }
def WeightList(blob):
    weight_list = struct.unpack(f'<I', blob[:0x4])
    weights = ...  # vec3
    return { 'WeightList': weight_list, "Weights": weights }
def MatrixPalette(blob):
    num_matrices = struct.unpack(f'<I', blob[:0x4])
    matrices = ...  # ulong
    return { 'NumMatrices': num_matrices, 'Matrices': matrices }
def InstanceInfo(blob):
    num_instances = struct.unpack(f'<I', blob[:0x4])
    vertex_count = struct.unpack(f'<I', blob[0x4:0x8])
    index_count = struct.unpack(f'<I', blob[0x8:0xC])
    return { 'NumInstances': num_instances, 'VertexCount': vertex_count, 'IndexCount': index_count }
def PrimGroupMemoryImageVertex(blob):
    version = struct.unpack(f'<I', blob[:0x4])
    param = struct.unpack(f'<I', blob[0x4:0x8])
    memory_image_vertex_size = struct.unpack(f'<I', blob[0x8:0xC])
    memory_image_vertex = ...  # byte
    return { 'Version': version, 'Param': param, 'MemoryImageVertexSize': memory_image_vertex_size, 'MemoryImageVertex': memory_image_vertex }
def PrimGroupMemoryImageIndex(blob):
    version = struct.unpack(f'<I', blob[:0x4])
    param = struct.unpack(f'<I', blob[0x4:0x8])
    memory_image_index_size = struct.unpack(f'<I', blob[0x8:0xC])
    memory_image_index = ...  # byte
    return { 'Version': version, 'Param': param, 'MemoryImageVertexSize': memory_image_index_size, 'MemoryImageVertex': memory_image_index }
def PrimGroupMemoryImageVertexDescription(blob):
    version = struct.unpack(f'<I', blob[:0x4])
    param = struct.unpack(f'<I', blob[0x4:0x8])
    memory_image_vertex_description_size = struct.unpack(f'<I', blob[0x8:0xC])
    memory_image_vertex_description = ...  # byte
    return { 'Version': version, 'Param': param, 'MemoryImageVertexDescriptionSize': memory_image_vertex_description_size, 'MemoryImageVertexDescription': memory_image_vertex_description }
def TangentList(blob):
    num_binormals = struct.unpack(f'<I', blob[:0x4])
    binormals = ...
    return { 'NumBinormals': num_binormals, 'Binormals': binormals }
def BinormalList(blob):
    tangent_list = struct.unpack(f'<I', blob[:0x4])
    tangents = ...
    return { 'NumTangents': tangent_list, 'Tangents': tangents }
def OffsetList(blob):
    num_offsets = struct.unpack(f'<I', blob[:0x4])
    key_index = struct.unpack(f'<I', blob[0x4:0x8])
    offsets = ...  # VtxOffset
    prim_group_index = struct.unpack(f'<I', blob[...])
    return { 'NumOffsets': num_offsets, 'KeyIndex': key_index, 'Offsets': offsets, 'PrimGroupIndex': prim_group_index }

def UVList(blob):
    num_uvs = struct.unpack(f'<I', blob[:0x4])
    channel = struct.unpack(f'<I', blob[0x4:0x8])
    uvs = ...
    return { 'NumUVs': num_uvs, 'Channel': channel, 'UVs': uvs }
def ExpressionOffsetsChunk(blob):
    num_prim_groups = struct.unpack(f'<I', blob[:0x4])
    num_offset_lists = struct.unpack(f'<I', blob[0x4:0x8])
    prim_group_indices = ...
    return { 'NumPrimGroups': num_prim_groups, 'NumOffsetLists': num_offset_lists, 'PrimGroupIndices': prim_group_indices }
def RenderStatusChunk(blob):
    cast_shadow = struct.unpack(f'<I', blob[:0x4])
    return { 'CastShadow': cast_shadow }
# def BBox(blob): return {  }  # dont know if dupe or
# def BSphere(blob): return {  }  # dont know if dupe or

CHUNKS = {
    b'\x50\x33\x44\xFF': P3D,

    # b'\x07\x00\xF0\x03': FenceDSG,
    #     b'\x00\x00\x00\x03': Wall,

    # b'\x03\x00\xF0\x03': IntersectDSG,
    #     b'\x03\x00\x01\x00': BBox,
    #     b'\x04\x00\x01\x00': BSphere,
    #     b'\x0E\x00\x00\x03': TerrainType,

    # b'\x04\x00\xF0\x03': TreeDSG,
    #     b'\x05\x00\xF0\x03': ContiguousBinNode,
    #     b'\x06\x00\xF0\x03': SpatialNode,

    # b'\x05\x00\x00\x03': WBLocator,
    #     b'\x06\x00\x00\x03': WBTriggerVolume,

    # b'\x00\x90\x01\x00': Texture,
    #     b'\x01\x90\x01\x00': Image,
    #     b'\x02\x90\x01\x00': ImageData,
    #     b'\x03\x90\x01\x00': ImageFileName,
    #     b'\x04\x90\x01\x00': VolumeImage,
    #     b'\x05\x90\x01\x00': Sprite,

    # b'\x01\x00\xF0\x03': StaticPhysDSG,
    #     b'\x00\x00\x01\x07': CollisionObject,
    #     b'\x23\x00\x01\x07': CollisionObjectAttribute,
    #     b'\x21\x00\x01\x07': CollisionVolumeOwner,
    #     b'\x22\x00\x01\x07': CollisionVolumeOwnerName,
    #     b'\x20\x00\x01\x07': SelfCollision,
    #     b'\x01\x00\x01\x07': CollisionVolume,
    #     b'\x06\x00\x01\x07': BBoxVolume,
    #     b'\x02\x00\x01\x07': SphereVolume,
    #     b'\x03\x00\x01\x07': CylinderVolume,
    #     b'\x04\x00\x01\x07': OBBoxVolume,
    #     b'\x05\x00\x01\x07': WallVolume,
    #     b'\x07\x00\x01\x07': CollisionVector,

    # b'\x0B\x00\xF0\x03': WorldSphereDSG,

    ## mesh
    b'\x00\x00\x01\x00': Mesh,
        b'\x02\x00\x01\x00': PrimeGroupChunk,
            # b'\x\x\x\x': VertexShader,
            b'\x05\x00\x01\x00': PositionList,
            # b'\x\x\x\x': NormalList,
            # b'\x\x\x\x': PackedNormalList,
            # b'\x\x\x\x': ColourList,
            # b'\x\x\x\x': MultiColourList,
            # b'\x\x\x\x': StripList,
            b'\x0A\x00\x01\x00': IndexList,
            # b'\x\x\x\x': MatrixList,
            # b'\x\x\x\x': WeightList,
            # b'\x\x\x\x': MatrixPalette,
            # b'\x\x\x\x': InstanceInfo,
            # b'\x\x\x\x': PrimGroupMemoryImageVertex,
            # b'\x\x\x\x': PrimGroupMemoryImageIndex,
            # b'\x\x\x\x': PrimGroupMemoryImageVertexDescription,
            # b'\x\x\x\x': TangentList,
            # b'\x\x\x\x': BinormalList,
            # b'\x\x\x\x': OffsetList,
        # b'\x\x\x\x': BBoxChunk,
        # b'\x\x\x\x': BSphereChunk,
    # b'\x\x\x\x': RenderStatusChunk,
    # b'\x\x\x\x': ExpressionOffsetsChunk,
}
