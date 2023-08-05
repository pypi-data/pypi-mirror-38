import ast


class Map:
    def has(self, key, map):
        #map = {i.split(': ')[0]: i.split(': ')[1] for i in map[1:-1].split(', ')}
        map = ast.literal_eval(map)
        key = key.strip()
        if len(key) < 1:
            return False
        return key in map
