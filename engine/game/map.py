

class Map():

    def __init__(self, vertices, edges, continents, continent_bonuses):
        self._vertices: dict[str, int] = vertices
        self._vertex_names: dict[int, str] = dict([(y, x) for x, y in vertices.items()])
        self._continents: dict[int, list[int]] = continents
        self._continent_bonuses: dict[int, int] = continent_bonuses
        self._edges: dict[int, list[int]] = edges

    def get_vertices(self):
        return self._vertices.values()
    
    def get_vertex_name(self, v: int):
        return self._vertex_names[v]

    def get_continents(self):
        return self._continents

    def get_adjacent_to(self, v: int):
        return self._edges[v]
    
    def is_adjacent(self, v1: int, v2: int):
        return v2 in self._edges[v1]