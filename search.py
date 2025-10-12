from collections import deque
from heapq import heappush, heappop
from itertools import count
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

    def gbfs_search(self, train_data, heuristic_fn, max_complexity=3):
        # Edge case of complexity 0
        empty = Program()
        if self.validate_program(empty, train_data):
            return empty

        # Generate base operations from first input example (if available)
        first_input = train_data[0]['input'] if train_data else None
        ops_array = operations.get_base_operations(first_input)

        # Priority queue of (h, tie, program)
        heap = []
        tie_counter = count()

        # Seed heap with complexity-1 candidates
        for op in ops_array:
            h_val = heuristic_fn(op, train_data)
            heappush(heap, (h_val, next(tie_counter), op))

        while heap:
            _, _, program = heappop(heap)

            # Check for solution
            if self.validate_program(program, train_data):
                return program

            # Expand if under complexity budget
            if program.complexity < max_complexity:
                for op in ops_array:
                    child = Program('Sequence', program, op)
                    h_val = heuristic_fn(child, train_data)
                    heappush(heap, (h_val, next(tie_counter), child))

        return None

    def a_star_search(self, train_data, heuristic_fn, max_complexity=3):
        # Edge case of complexity 0
        empty = Program()
        if self.validate_program(empty, train_data):
            return empty

        # Generate base operations from first input example (if available)
        first_input = train_data[0]['input'] if train_data else None
        ops_array = operations.get_base_operations(first_input)

        # Priority queue of (f, tie, program)
        heap = []
        tie_counter = count()

        def priority(prog: Program) -> float:
            g = getattr(prog, 'complexity', 0)
            h = heuristic_fn(prog, train_data)
            return g + h

        # Seed heap with complexity-1 candidates
        for op in ops_array:
            heappush(heap, (priority(op), next(tie_counter), op))

        while heap:
            _, _, program = heappop(heap)

            if self.validate_program(program, train_data):
                return program

            if program.complexity < max_complexity:
                for op in ops_array:
                    child = Program('Sequence', program, op)
                    heappush(heap, (priority(child), next(tie_counter), child))

        return None

    def validate_program(self, program: Program, data):
        for dp in data:
            if program.apply_program(dp['input']) != dp['output']:
                return False
            
        return True