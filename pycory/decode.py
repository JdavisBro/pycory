import base64
import zlib

__all__ = (
    "GEO_SIZE",
    "PAINT_SIZE",
    "decode",
    "geo",
    "paint",
    "Geo",
    "Paint"
)

GEO_SIZE = (81,46)

PAINT_SIZE = (162,92)

class Geo():
    """
    get x,y value with geo[x,y]
    0 indexed, [0,0] is top left
    
    Takes list of this format:
    [ [ [v1, v2], 81 of these for each x ] 46 of these for each y ]
    """
    def __init__(self, data: list):
        self.data = data

    def _index_check(self, i):
        if (not isinstance(i, tuple)) or len(i) != 2:
            raise IndexError("Geo getter must be two values, e.g geo[x,y]")
        x, y = i
        if 0 > x >= GEO_SIZE[0]:
            raise IndexError(f"x value must be between 0 and {GEO_SIZE[0]-1}")
        if 0 > y >= GEO_SIZE[1]:
            raise IndexError(f"y value must be between 0 and {GEO_SIZE[1]-1}")

    def __getitem__(self, i):
        self._index_check(i)
        x, y = i
        return self.data[y][x]

    def __setitem__(self, i, value: list):
        if not isinstance(value,list):
            raise TypeError("Geo data must be a list of two values.")
        if len(value) != 2:
            raise ValueError("Geo data must be of length 2")
        
        self._index_check(i)
        x, y = i
        self.data[y][x] = value

    def __iter__(self):
        self.iter_pos = [0,0]
        return self

    def __next__(self):
        if self.iter_pos[1] == GEO_SIZE[1]:
            raise StopIteration

        value = self.data[iter_pos[1]][iter_pos[0]]

        self.iter_pos[0] += 1
        if self.iter_pos[0] == GEO_SIZE[0]:
            self.iter_pos[0] = 0
            self.iter_pos[1] += 1
        return value

    def enumerate(self): # i think there should be a better name for this
        for y in range(GEO_SIZE[1]):
            for x in range(GEO_SIZE[0]):
                yield x, y, self.data[y][x]

class Paint():
    def __init__(self):
        pass


def decode(data: str):
    """
    Returns a decoded list of data.
    """
    return [i for i in zlib.decompress(base64.b64decode(data)).hex()]

def geo(data: str) -> Geo:
    data = decode(data)
    if len(data) != (GEO_SIZE[0] * 2) * GEO_SIZE[1]:
        raise ValueError("Data size incorrect, possibly not geo data.")
    data_list = []
    for y in range(GEO_SIZE[1]):
        data_list.append([])
        for x in range(GEO_SIZE[0]):
            x *= 2 # There are 2 for each x value
            x + y*GEO_SIZE[0] # Offset x by how many y we are down
            data_list[-1].append( [ data[x], data[x+1] ] )
    return Geo(data_list)

def paint(data: str, palette: dict=None) -> Paint:
    pass

