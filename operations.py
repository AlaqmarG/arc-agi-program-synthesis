from program import Program
from random import shuffle

class Operations:
    def get_base_operations(self, grid, out_grid) -> list[Program]:
        operations = []

        # Get colors that appear in input and output
        input_colors = set(self._get_colors_in_grid(grid))
        output_colors = set(self._get_colors_in_grid(out_grid))
        all_colors = input_colors.union(output_colors)
        
        # Color Change Operations: Only from input colors to output colors
        for in_color in input_colors:
            for out_color in output_colors:
                if in_color != out_color:
                    operations.append(Program("ColorChange", right=[in_color, out_color]))

        # Mirror and Rotate (fundamental transformations)
        operations += [Program("Mirror", right=i) for i in ['horizontal', 'vertical']]
        operations += [Program("Rotate", right=i) for i in [90, 180, 270]]

        # SwapColors: Only between colors that appear in either grid
        for i in all_colors:
            for j in all_colors:
                if i < j:  # Only one direction to avoid redundancy
                    operations.append(Program("SwapColors", right=[i, j]))

        # Scale Operations (when grid dimensions change)
        if grid and out_grid and (len(grid) != len(out_grid) or len(grid[0]) != len(out_grid[0])):
            operations += [Program(i) for i in ['Scale2x2', 'Scale3x3', 'Scale1x2', 'Scale2x1']]

        # Positional Shift: Only from input colors to output colors, with minimal shifts
        for in_color in input_colors:
            for out_color in output_colors:
                if in_color != out_color:
                    # Only generate shifts if we see patterns requiring them
                    for x, y in [(0,1), (1,0), (0,-1), (-1,0)]:  # Cardinal directions only
                        operations.append(Program('PositionalShift', None, right=[in_color, out_color, x, y]))

        # Diagonal Reflection: Only when needed based on color patterns
        diag_needed = False
        if grid and out_grid:
            # Check if any color appears in different positions that could be diagonal reflections
            for color in all_colors:
                if any(grid[i][j] == color and out_grid[j][i] != color 
                      for i in range(len(grid)) 
                      for j in range(len(grid[0]))
                      if j < len(grid) and i < len(grid[0])):
                    diag_needed = True
                    break
                    
        if diag_needed:
            for in_color in input_colors:
                for out_color in output_colors:
                    if in_color != out_color:
                        operations.append(Program('DiagonalReflection', None, [in_color, out_color]))

        # Randomize the order
        shuffle(operations)
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