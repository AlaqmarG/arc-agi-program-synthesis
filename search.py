from collections import deque
from operations import Operations
from program import Program

operations = Operations()

class Search:
    def bfs(self, in_out_pair, max_complexity=3):
        # Edge case complexity 0
        if self.validate_program(Program(), in_out_pair):
            return Program()

        # Queue base operations
        queue = deque()
        ops_array = operations.get_base_operations(in_out_pair[0]['input'])

        # Add complexity 1 solutions
        for op in ops_array:
            queue.append(op)
            
        # Run operations and add sequenced program
        while len(queue) > 0:
            program: Program = queue.popleft()

            # Validate solution
            if self.validate_program(program, in_out_pair):
                return program
            
            # Sequence new programs
            if program.complexity != max_complexity:
                for op in ops_array:
                    queue.append(Program('Sequence', program, op))
        
        return Program()

    def validate_program(self, program: Program, in_out_pair):
        for data_point in in_out_pair:
            if program.apply_program(data_point['input']) != data_point['output']:
                return False
            
        return True