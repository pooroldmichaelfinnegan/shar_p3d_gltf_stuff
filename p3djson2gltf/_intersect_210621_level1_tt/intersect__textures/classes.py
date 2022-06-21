from dataclasses import dataclass

terrain_type = ['TT_Road','TT_Grass','TT_Sand','TT_Gravel','TT_Water','TT_Wood','TT_Metal','TT_Dirt',]


@dataclass
class Chunk:
    def __init__(self, data: dict = {}, childs: list = []):
        self.data = data
        self.childs = childs


class Intersect(Chunk):
    def __init__(self, data: dict = {}, childs: list = []):
        Chunk.__init__(self, data, childs)
        self.indices3 = self.data['Indices']
        self.positions3 = self.data['Positions']
        self.normals3 = self.data['Normals']
        if not childs: return
        self.child_names = [i for j in childs for i in list(j)]
        self.terraintype = self.childs[self.child_names.index('TerrainType')] if 'TerrainType' in self.child_names else None
        self.tttypes = self.terraintype['Types']
        self.tttypesstr = [terrain_type[i] for i in self.tttypes]


@dataclass
class I():
    indices3: list[list[int, int, int]]
    positions3: list[list[float, float, float]]
    normals3: list[list[float, float, float]]
    child_names: list[str]
    terraintyps: dict[Chunk: dict]
    tttypes: list[int]
    tttypesstr: list[str]
