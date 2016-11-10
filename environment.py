from renderer import Renderer


class Environment():
    def __init__(self, grid):
        self.grid = grid
        self.n_rows = len(grid)
        self.n_cols = len(grid[0])
        self.positions = self._positions()
        self.starting_positions = [p for p in self.positions
                                   if not self.is_terminal_state(p)]
        self.renderer = Renderer(self.grid)

    def actions(self, pos):
        """possible actions for a state (position)"""
        r, c = pos
        actions = []
        if r > 0:
            actions.append('up')
        if r < self.n_rows - 1:
            actions.append('down')
        if c > 0:
            actions.append('left')
        if c < self.n_cols - 1:
            actions.append('right')
        return actions

    def value(self, pos):
        """retrieve the reward value for a position"""
        r, c = pos
        return self.grid[r][c]

    def _positions(self):
        """all positions"""
        positions = []
        for r, row in enumerate(self.grid):
            for c, _ in enumerate(row):
                positions.append((r,c))
        return positions

    def is_terminal_state(self, state):
        """tell us if the state ends the game"""
        val = self.value(state)
        return val is None or val > 0

    def reward(self, state):
        """the reward of a state:
        -1 if it's a hole,
        -1 if it's an empty space (to penalize each move),
        otherwise, the value of the state"""
        val = self.value(state)
        if val is None or val == 0:
            return -1
        return val

    def render(self, pos=None):
        self.renderer.render(pos)
