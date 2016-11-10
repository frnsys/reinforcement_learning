import math
import textwrap
from PIL import Image, ImageDraw, ImageFont

font = ImageFont.load_default()

move_to_arrow = {
    'right': '>',
    'left': '<',
    'up': '^',
    'down': 'v'
}

def cell_label(qvals, reward, show_qvals=True):
    # given the Q values for a state and the state's reward,
    # output a string describing it
    n = []
    if not all(v == 0 for v in qvals.values()):
        if show_qvals:
            for k, v in qvals.items():
                n.append('{}{:.2f}'.format(k[0].upper(), v))
        best_move = max(qvals.keys(), key=lambda k: qvals[k])
        n.append(move_to_arrow[best_move])
    else:
        n.append(str(reward) if reward is not None else 'hole')
    return '\n'.join(n)


class PolicyRenderer():
    """renders a grid with values (for the gridworld)"""
    def __init__(self, agent, env, cell_size=60):
        # generate the grid, with labels, to render
        grid = []
        for i, row in enumerate(env.grid):
            grid.append([cell_label(
                agent.Q.get((i,j), {}),
                env.value((i,j)),
                show_qvals=False) for j, col in enumerate(row)])

        self.grid = grid
        self.cell_size = cell_size

        grid_h = len(grid)
        grid_w = max(len(row) for row in grid)
        self.size = (grid_w * self.cell_size, grid_h * self.cell_size)

    def _draw_cell(self, x, y, fill, color, value, pos, text_padding=10):
        self.draw.rectangle([(x, y), (x+self.cell_size, y+self.cell_size)], fill=fill)

        # render text
        y_mid = math.floor(self.cell_size/2)
        lines = textwrap.wrap(str(value), width=15)
        _, line_height = self.draw.textsize(lines[0], font=font)
        height = len(lines) * line_height + (len(lines) - 1) * text_padding
        current_height = y_mid - height/2

        for line in lines:
            w, h = self.draw.textsize(line, font=font)
            self.draw.text((x + (self.cell_size - w)/2, y + current_height), line, font=font, fill=color)
            current_height += h + text_padding

    def render(self, pos=None):
        """renders the grid,
        highlighting the specified position if there is one"""
        self.img = Image.new('RGBA', self.size, color=(255,255,255,0))
        self.draw = ImageDraw.Draw(self.img)

        for r, row in enumerate(self.grid):
            for c, val in enumerate(row):
                if val is None:
                    continue
                fill = (220,220,220,255) if (r + c) % 2 == 0 else (225,225,225,255)

                # current position
                if pos is not None and pos == (r, c):
                    fill = (255,255,150,255)
                self._draw_cell(c * self.cell_size, r * self.cell_size, fill, (0,0,0,255), val, (r,c))

        return self.img