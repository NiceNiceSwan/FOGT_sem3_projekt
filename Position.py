from __future__ import annotations
import math

class Position:
    x: int
    y: int

    def __init__(self, _x: int, _y: int) -> None:
        self.x = _x
        self.y = _y

    def copy(self) -> Position:
        return Position(self.x, self.y)

    def __eq__(self, value):
        if not isinstance(value, Position):
            return False
        
        if self.x == value.x and self.y == value.y:
            return True
        
        return False

    def __str__(self):
        return "X: " + str(self.x) + ", Y: " + str(self.y)
    
    def distance(self: Position, other: Position) -> float:
        """
        calculates the distance between itself and the other position
        
        :param other: another position
        :type other: Position
        :return: distance between the 2 positions
        :rtype: float
        """
        if self == other:
            return 0
        distance_x: float = self.x - other.x
        distance_y: float = self.y - other.y
        distance: float = math.sqrt(distance_x**2 + distance_y**2)
        return distance
