import abc from ABCMeta

class AStarBase:
    __metaclass__ = ABCMeta

    def __init__(grid):
        openSet = []
