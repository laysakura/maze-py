#!/usr/bin/env python

import sys
import random

class Direction:
    RIGHT, UP, LEFT, DOWN = range(4)
    @classmethod
    def rot90(cls, direction):
        """
        @in-out:
        RIGHT => UP
        UP => LEFT
        LEFT => DOWN
        DOWN => RIGHT
        """
        assert(0 <= direction <= 3)
        return (direction + 1) % 4
    @classmethod
    def get_rand_direction(cls):
        return random.randint(0, 3)

class Maze(object):
    """
    width + 2
    <----->

    1111111  ^
    1000001  |
    1000001  | height + 2
    1000001  |
    1111111  v

    @constraints:
    - Maze is surrounded by `banpei'
    - width and height are odd-number
    - Stand on (x, y), where (2 <= x <= width - 1 && 2 <= y <= height - 1)
    """

    def __init__(self, width, height):
        assert(width % 2 == 1 and height % 2 == 1)
        assert(width >= 3 and height >= 3)
        self.width = width
        self.height = height
        self.maze_data = [0 for i in range((width + 2) * (height + 2))]
        # Put `banpei' around maze.
        for i in range(self.width + 2):
            self._set_point(x=i, y=0, val=1)
            self._set_point(x=i, y=self.height + 1, val=1)
        for i in range(self.height + 2):
            self._set_point(x=0, y=i, val=1)
            self._set_point(x=self.width + 1, y=i, val=1)

    def __str__(self):
        def get_brick_or_space(p):
            assert(p == 0 or p == 1)
            return "@" if p ==0 else " "
        s = ""
        for y in range(1, self.height + 1):
            for x in range(1, self.width + 1):
                s += get_brick_or_space(self._get_point(x, y))
            s += "\n"
        return s

    def _set_point(self, x, y, val):
        self.maze_data[(self.width + 2) * y + x] = val
    def _get_point(self, x, y):
        return self.maze_data[(self.width + 2) * y + x]

    def create(self):
        """
        Create a maze.
        Implemented by 'Anahori-hou'.
        """
        def start_point():
            # Always returns even point, except `banpei'.
            return (2 * random.randint(1, (self.width - 1) / 2),
                    2 * random.randint(1, (self.height - 1) / 2))

        def dig(x, y):
            """
            Find a good direction to dig and go straight 2 points.
            Back-track when no direction found.
            """
            assert(x % 2 == 0 and y % 2 == 0)
            assert(2 <= x <= self.width - 1 and
                   2 <= y <= self.height - 1)

            def step_forward():
                """
                @returns:
                New (x, y)
                (None, None): when no good direction found
                """
                d = Direction.get_rand_direction()
                for i in range(4):  # Consider all direcitons
                    if d == Direction.RIGHT and self._get_point(x + 2, y) == 0:
                        self._set_point(x=x + 1, y=y, val=1)
                        self._set_point(x=x + 2, y=y, val=1)
                        return (x + 2, y)
                    elif d == Direction.UP and self._get_point(x, y - 2) == 0:
                        self._set_point(x=x, y=y - 1, val=1)
                        self._set_point(x=x, y=y - 2, val=1)
                        return (x, y - 2)
                    elif d == Direction.LEFT and self._get_point(x - 2, y) == 0:
                        self._set_point(x=x - 1, y=y, val=1)
                        self._set_point(x=x - 2, y=y, val=1)
                        return (x - 2, y)
                    elif d == Direction.DOWN and self._get_point(x, y + 2) == 0:
                        self._set_point(x=x, y=y + 1, val=1)
                        self._set_point(x=x, y=y + 2, val=1)
                        return (x, y + 2)
                    d = Direction.rot90(d)
                return (None, None)

            while True:
                new_x, new_y = step_forward()
                if new_x is None:
                    return  # Back-track
                dig(new_x, new_y)

        # Choose a start point randomly
        x, y = start_point()

        # Start to dig recursively
        dig(x, y)


def parse_args():
    def args_error_exit():
        sys.stderr.write(
"""
Usage: /path/to/%s WIDTH HEIGHT

* Both WIDTH and HEIGHT must be odd *
"""
% (sys.argv[0])
)
        exit(1)

    if len(sys.argv) != 3:
        args_error_exit()
    width = int(sys.argv[1])
    height = int(sys.argv[2])
    if width % 2 == 0 or height % 2 == 0:
        args_error_exit()
    return (width, height)

def main():
    width, height = parse_args()
    maze = Maze(width, height)
    maze.create()
    print(maze)

if __name__ == '__main__':
    main()
