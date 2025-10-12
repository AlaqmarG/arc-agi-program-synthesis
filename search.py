from collections import deque
from operations import Operations
from program import Program

operations = Operations()

class Search:
    def bfs(self, data, max_complexity=3):
        # Edge case complexity 0
        if self.validate_program(Program(), data):
            return Program()

        # Queue base operations
        queue = deque()
        ops_array = operations.get_base_operations(data[0]['input'])

        # Add complexity 1 solutions
        for op in ops_array:
            queue.append(op)
            
        # Run operations and add sequenced program
        while len(queue) > 0:
            program: Program = queue.popleft()

            # Validate solution
            if self.validate_program(program, data):
                return program
            
            # Sequence new programs
            if program.complexity != max_complexity:
                for op in ops_array:
                    queue.append(Program('Sequence', program, op))
        
        return None

    def validate_program(self, program: Program, data):
        for dp in data:
            if program.apply_program(dp['input']) != dp['output']:
                return False
            
        return True