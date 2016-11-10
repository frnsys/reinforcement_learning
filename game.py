import numpy as np
from blessings import Terminal


class Game():
    def __init__(self, shape=(10,10)):
        self.shape = shape
        self.height, self.width = shape
        self.last_row = self.height - 1
        self.paddle_padding = 1
        self.n_actions = 3 # left, stay, right
        self.term = Terminal()
        self.reset()

    def reset(self):
        # reset grid
        self.grid = np.zeros(self.shape)

        # can only move left or right (or stay)
        # so position is only its horizontal position (col)
        self.pos = np.random.randint(self.paddle_padding, self.width - 1 - self.paddle_padding)
        self.set_paddle(1)

        # item to catch
        self.target = (0, np.random.randint(self.width - 1))
        self.set_position(self.target, 1)

    def move(self, action):
        # clear previous paddle position
        self.set_paddle(0)

        # action is either -1, 0, 1,
        # but comes in as 0, 1, 2, so subtract 1
        action -= 1
        self.pos = min(max(self.pos + action, self.paddle_padding), self.width - 1 - self.paddle_padding)

        # set new paddle position
        self.set_paddle(1)

    def set_paddle(self, val):
        for i in range(1 + self.paddle_padding*2):
            pos = self.pos - self.paddle_padding + i
            self.set_position((self.last_row, pos), val)

    @property
    def state(self):
        return self.grid.reshape((1,-1)).copy()

    def set_position(self, pos, val):
        r, c = pos
        self.grid[r,c] = val

    def update(self):
        r, c = self.target

        self.set_position(self.target, 0)
        self.set_paddle(1) # in case the target is on the paddle
        self.target = (r+1, c)
        self.set_position(self.target, 1)

        # off the map, it's gone
        if r+1 == self.last_row:
            # reward of 1 if collided with paddle, else -1
            if abs(c - self.pos) <= self.paddle_padding:
                return 1
            else:
                return -1
        return 0

    def render(self):
        print(self.term.clear())
        for r, row in enumerate(self.grid):
            for c, on in enumerate(row):
                if on:
                    color = 235
                else:
                    color = 229

                print(self.term.move(r, c) + self.term.on_color(color) + ' ' + self.term.normal)

        # move cursor to end
        print(self.term.move(self.height, 0))
