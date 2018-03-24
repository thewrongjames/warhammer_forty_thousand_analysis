"""
This package provides tools for analysing particular eigth edition warhammer
forty thousand model loadouts.
"""

class Model:
    """
    The model class provides a programmatic representation of the warhammer
    forty thousand rules' notion of a model.
    """
    def __init__(self, stat_line, points):
        """
        Creates a model object, with the stats in stat_line, and points cost in
        points. stat_line should be indexable, and contain m, ws, bs, s, t, w,
        a, ld, and sv.
        """
        self.stat_line = stat_line
        self.points = points
        
