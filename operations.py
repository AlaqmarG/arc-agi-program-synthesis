from program import Program

class Operations:
    def get_base_operations(self, grid=None) -> list[Program]:
        operations = []

        operations += self._iterate_color_operations("ColorChange") # Color Change Operations
        operations += [Program("Mirror", right=i) for i in ['horizontal', 'vertical']] # Mirror Operations
        operations += [Program("Rotate", right=i) for i in [90, 180, 270]] # Rotate Operations

        # SwapColors Operations
        colors = self._get_colors_in_grid(grid)
        operations += [Program("SwapColors", right=[i, j]) for i in colors for j in colors if i != j]

        # Scale Operations
        operations += [Program(i) for i in ['Scale2x2', 'Scale3x3', 'Scale1x2', 'Scale2x1']]

        # Positional Shift
        operations += [Program('PositionalShift', None, right=[i, j, x, y]) for i in colors for j in range(0, 10) if i != j for x in range(-1, 2) for y in range(-1, 2)]

        return operations

    def _iterate_color_operations(self, op: str) -> list[Program]:
        operations = []

        for i in range(10):
            for j in range(10):
                if i == j:
                    continue

                operations.append(Program(op, right=[i, j]))

        return operations
    
    def _get_colors_in_grid(self, grid) -> list[int]:
        if not grid:
            return []
        unique_colors = set()
        for row in grid:
            if row is None:
                continue
            for e in row:
                unique_colors.add(e)
        return list(unique_colors)