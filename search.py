from collections import deque
from heapq import heappush, heappop
from itertools import count
from operations import Operations
from program import Program

operations = Operations()

class Search:
    def bfs(self, data, max_complexity=3):
        programs_checked = 0
        
        # Edge case complexity 0
        if self.validate_program(Program(), data):
            return Program()

        # Queue base operations
        queue = deque()
        ops_array = operations.get_base_operations(data[0]['input'], data[0]['output'])
        num_base_ops = len(ops_array)

        # Add complexity 1 solutions
        for op in ops_array:
            queue.append(op)

        # Run operations and add sequenced program
        while len(queue) > 0:
            program: Program = queue.popleft()
            
            if programs_checked % 100000 == 0:
                print("\033[K", end="", flush=True)
                print(f"BFS: {programs_checked} programs, complexity: {program.complexity}, queue size: {len(queue)}, base ops: {num_base_ops}", end='\r')

            programs_checked += 1

            # Validate solution
            if self.validate_program(program, data):
                return program
            
            # Sequence new programs
            if program.complexity < max_complexity:  # Changed from != to <
                for op in ops_array:
                    new_program = Program('Sequence', program, op)
                    if new_program.complexity <= max_complexity:  # Added explicit check
                        queue.append(new_program)

        return None

    def gbfs_search(self, train_data, heuristic_fn, max_complexity=3):
        programs_checked = 0
        best_h = float('inf')
        
        # Edge case of complexity 0
        empty = Program()
        if self.validate_program(empty, train_data):
            return empty

        # Generate base operations from first example (if available)
        first_input = train_data[0]['input'] if train_data else None
        first_output = train_data[0]['output'] if train_data else None
        ops_array = operations.get_base_operations(first_input, first_output)
        num_base_ops = len(ops_array)

        # Priority queue of (h, tie, program)
        heap = []
        tie_counter = count()

        # Seed heap with complexity-1 candidates
        for op in ops_array:
            h_val = heuristic_fn(op, train_data)
            best_h = min(best_h, h_val)
            heappush(heap, (h_val, next(tie_counter), op))

        while heap:
            h_val, _, program = heappop(heap)
            programs_checked += 1
            
            if programs_checked % 100000 == 0:
                print("\033[K", end="", flush=True)
                print(f"GBFS: {programs_checked} programs, cur h: {h_val:.2f}, best h: {best_h:.2f}, heap size: {len(heap)}, base ops: {num_base_ops}", end='\r')

            # Check for solution
            if self.validate_program(program, train_data):
                return program

            # Expand if under complexity budget
            if program.complexity < max_complexity:
                for op in ops_array:
                    child = Program('Sequence', program, op)
                    h_val = heuristic_fn(child, train_data)
                    best_h = min(best_h, h_val)
                    heappush(heap, (h_val, next(tie_counter), child))

        return None

    def a_star_search(self, train_data, heuristic_fn, max_complexity=3):
        programs_checked = 0
        best_f = float('inf')
        debug_level = 1  # Set to higher values for more detailed logging
        
        # Edge case of complexity 0
        empty = Program()
        if self.validate_program(empty, train_data):
            return empty

        # Generate base operations from first example (if available)
        first_input = train_data[0]['input'] if train_data else None
        first_output = train_data[0]['output'] if train_data else None
        ops_array = operations.get_base_operations(first_input, first_output)
        num_base_ops = len(ops_array)

        # Priority queue of (f, tie, program)
        heap = []
        tie_counter = count()
        visited = set()  # Track visited program states

        # Seed heap with base candidates using weighted cost for g
        for op in ops_array:
            g = op.cost
            h = heuristic_fn(op, train_data)
            f = g + h
            heappush(heap, (f, g, h, next(tie_counter), op))
            visited.add(str(op))

        while heap:
            f_val, g_val, h_val, _, program = heappop(heap)
            programs_checked += 1
            
            if programs_checked % 100000 == 0:
                print("\033[K", end="", flush=True)
                print(f"A*: {programs_checked} programs, cur f: {f_val:.2f} (g={g_val}, h={h_val:.2f}), heap size: {len(heap)}, base ops: {num_base_ops}", end='\r')

            if self.validate_program(program, train_data):
                return program

            if program.complexity < max_complexity:
                for op in ops_array:
                    child = Program('Sequence', program, op)
                    if child.complexity <= max_complexity:
                        child_str = str(child)
                        if child_str not in visited:
                            g = child.cost
                            h = heuristic_fn(child, train_data)
                            f = g + h
                            heappush(heap, (f, g, h, next(tie_counter), child))
                            visited.add(child_str)

        return None

    def validate_program(self, program: Program, data):
        for dp in data:
            if program.apply_program(dp['input']) != dp['output']:
                return False
            
        return True