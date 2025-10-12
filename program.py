class Program:
    def __init__(self, op=None, left=None, right=None):
        self.op = op
        self.left = left
        self.right = right

        if op and left and right:
            self.complexity = left.complexity + right.complexity
        elif op:
            self.complexity = 1
        else:
            self.complexity = 0

    def _get(self, i, default=None):
        return self.right[i] if self.right and len(self.right) > i else default

    def __str__(self):
        if self.op == 'Sequence':
            left_op = self.left.op if self.left else 'None'
            right_op = self.right.op if self.right else 'None'
            return f"Sequence({left_op}, {right_op})"

        elif self.op == 'ColorChange':
            return f"ColorChange({self._get(0)}, {self._get(1)})"

        elif self.op == 'Mirror':
            return f"Mirror({self.right})"

        elif self.op == 'Rotate':
            return f"Rotate({self.right})"

        elif self.op == 'Scale2x2':
            return "Scale2x2()"

        elif self.op == 'Scale3x3':
            return "Scale3x3()"

        elif self.op == 'Scale2x1':
            return "Scale2x1()"

        elif self.op == 'Scale1x2':
            return "Scale1x2()"

        elif self.op == 'ResizeIrregular':
            return f"ResizeIrregular({self._get(0)}, {self._get(1)})"

        elif self.op == 'PositionalShift':
            return f"PositionalShift({self._get(0)}, {self._get(1)}, {self._get(2)}, {self._get(3)})"

        elif self.op == 'ColorMapMultiple':
            return f"ColorMapMultiple({dict(self.right) if self.right else {}})"

        elif self.op == 'ScaleWithColorMap':
            scale_map = self._get(1, [])
            if scale_map is None or not hasattr(scale_map, '__iter__'):
                scale_map = []
            return f"ScaleWithColorMap({self._get(0)}, {dict(scale_map)})"

        elif self.op == 'SwapColors':
            return f"SwapColors({self._get(0)}, {self._get(1)})"

        elif self.op == 'DiagonalReflection':
            return f"DiagonalReflection({self._get(0)}, {self._get(1)})"

        return ''

    def __lt__(self, other):
        return self.complexity < other.complexity

    def __eq__(self, other):
        return self.op == other.op and self.left == other.left and self.right == other.right
    
    def _resize(self, input_grid, size_w, size_h, scale_mode=False):
        new_grid = []
        
        for i in range(size_h):
            new_row = []
            
            for j in range(size_w):
                if scale_mode:
                    # Calculate scale factors, handle division by zero
                    scale_h = size_h // len(input_grid) if len(input_grid) > 0 else 1
                    scale_w = size_w // len(input_grid[0]) if len(input_grid[0]) > 0 else 1
                    
                    # Ensure scale factors are at least 1
                    scale_h = max(1, scale_h)
                    scale_w = max(1, scale_w)
                    
                    orig_i = min(i // scale_h, len(input_grid) - 1)
                    orig_j = min(j // scale_w, len(input_grid[0]) - 1)
                else:
                    # For irregular resize, use min to clamp coordinates
                    orig_i = min(i, len(input_grid) - 1)
                    orig_j = min(j, len(input_grid[0]) - 1)
                new_row.append(input_grid[orig_i][orig_j])
            
            new_grid.append(new_row)
        
        return new_grid

    def apply_program(self, input_grid):
        grid = [row[:] for row in input_grid]

        if self.op == 'Sequence':
            grid = self.left.apply_program(grid) if self.left is not None else grid
            grid = self.right.apply_program(grid) if self.right is not None else grid

        elif self.op == 'ColorChange':
            old_color, new_color = self.right if self.right else (None, None)
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    if grid[i][j] == old_color:
                        grid[i][j] = new_color

        elif self.op == 'Mirror':
            axis = self.right

            if axis == 'horizontal':
                grid = grid[::-1]
            elif axis == 'vertical':
                grid = [row[::-1] for row in grid]

        elif self.op == 'Rotate':
            degrees = self.right

            if degrees == 90:
                grid = [[grid[len(grid) - 1 - j][i] for j in range(len(grid))] for i in range(len(grid[0]))]
            elif degrees == 180:
                grid = [[grid[len(grid) - 1 - i][len(grid[0]) - 1 - j] for j in range(len(grid[0]))] for i in range(len(grid))]
            elif degrees == 270:
                grid = [[grid[j][len(grid[0]) - 1 - i] for j in range(len(grid))] for i in range(len(grid[0]))]

        elif self.op == 'SwapColors':
            color1, color2 = self.right if self.right else (None, None)

            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    if grid[i][j] == color1:
                        grid[i][j] = color2
                    elif grid[i][j] == color2:
                        grid[i][j] = color1

        elif self.op == 'Scale2x2':
            grid = self._resize(input_grid, 2 * len(input_grid[0]), 2 * len(input_grid), scale_mode=True)

        elif self.op == 'Scale3x3':
            grid = self._resize(input_grid, 3 * len(input_grid[0]), 3 * len(input_grid), scale_mode=True)

        elif self.op == "Scale2x1":
            grid = self._resize(input_grid, 2 * len(input_grid[0]), 1 * len(input_grid), scale_mode=True)

        elif self.op == "Scale1x2":
            grid = self._resize(input_grid, 1 * len(input_grid[0]), 2 * len(input_grid), scale_mode=True)

        elif self.op == 'PositionalShift':
            old_color = self._get(0)
            new_color = self._get(1)
            new_color = int(new_color) if new_color is not None else 0

            dr = self._get(2)
            dc = self._get(3)
            dr = int(dr) if dr is not None else 0
            dc = int(dc) if dc is not None else 0

            m, n = len(grid), len(grid[0]) if grid else 0
            new_grid = [[0 for _ in range(n)] for _ in range(m)]

            for r in range(m):
                for c in range(n):
                    if grid[r][c] == old_color:
                        new_c = c + dc
                        new_r = r
                        while new_c >= n:
                            new_c -= n
                            new_r += 1
                        if new_r >= m:
                            new_r -= m
                        if new_grid[new_r][new_c] == 0:
                            new_grid[new_r][new_c] = new_color
                        else:
                            new_grid[new_r][new_c] += new_color

            for r in range(m):
                for c in range(n):
                    if grid[r][c] != old_color and new_grid[r][c] == 0:
                        new_grid[r][c] = grid[r][c]

            grid = new_grid
            
        return grid