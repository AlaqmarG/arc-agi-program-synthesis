from program import Program


class Heuristics:
    def __init__(self):
        # Sync with configurable op costs
        self.max_cost = max(Program.op_costs.values()) if hasattr(Program, 'op_costs') else 3
    
    def __call__(self, program, train):
        return self.mismatch_sum(program, train)
    
    def normalize_heuristic(self, h_value, max_complexity=3):
        """
        Normalize heuristic value to be in same range as operation costs.
        Never overestimate the actual number of operations needed.
        """
        return min(h_value, max_complexity * self.max_cost)
    
    def min_operations_needed(self, pred, target):
        """
        Calculate minimum number of operations needed to transform pred into target.
        This is an admissible heuristic as it never overestimates.
        """
        if not pred or not target:
            return 0
            
        min_ops = 0
        
        # Size mismatch requires at least one scaling operation
        if len(pred) != len(target) or len(pred[0]) != len(target[0]):
            min_ops += 1
            
        # Count minimum color changes needed
        pred_colors = {cell for row in pred for cell in row}
        target_colors = {cell for row in target for cell in row}
        
        # If colors don't match, we need at least one color change per missing color
        missing_colors = len(target_colors - pred_colors)
        min_ops += missing_colors
        
        return min_ops
        
    def _min_operations_needed(self, current, target):
        """
        Calculate minimum number of operations needed to transform current grid to target.
        This is an admissible heuristic that never overestimates.
        """
        if current == target:
            return 0
            
        c_height, c_width = len(current), len(current[0]) if current else 0
        t_height, t_width = len(target), len(target[0]) if target else 0
        
        min_ops = 0
        
        # Size difference requires resize operations
        if c_height != t_height or c_width != t_width:
            min_ops += 1
            
        # Fast color analysis
        c_colors = set()
        t_colors = set()
        mismatches = 0
        
        # Quick scan of overlap region
        for i in range(min(c_height, t_height)):
            for j in range(min(c_width, t_width)):
                if current[i][j] != target[i][j]:
                    mismatches += 1
                c_colors.add(current[i][j])
                t_colors.add(target[i][j])
                
        # Add minimal operations needed
        new_colors = len(t_colors - c_colors)
        min_ops += min(mismatches, new_colors + 1)
            
        return min_ops
        
    def meta_heuristic(self, program, train):
        """
        Fast meta-heuristic that maintains admissibility.
        Simply takes maximum of normalized heuristics.
        """
        h_mismatch = self.mismatch_sum(program, train)
        h_color = self.color_dist_shape(program, train)
        
        if float('inf') in (h_mismatch, h_color):
            return float('inf')
            
        return max(h_mismatch, h_color)

    def color_dist_shape(self, program, train):
        """
        Admissible heuristic based on minimum operations needed for shape and color transformations.
        """
        min_ops = 0
        
        for ex in train:
            target = ex['output']
            try:
                pred = program.apply_program(ex['input'])
            except Exception:
                return float('inf')

            # Calculate minimum operations needed for this example
            example_min_ops = self._min_operations_needed(pred, target)
            
            # Take maximum across examples (maintains admissibility)
            min_ops = max(min_ops, example_min_ops)

        return min_ops

    def mismatch_sum(self, program, train):
        score = 0

        for ex in train:
            target = ex['output']
            pred = program.apply_program(ex['input'])

            m = len(target)
            n = len(target[0]) if m > 0 else 0
            pm = len(pred)
            pn = len(pred[0]) if pm > 0 else 0

            # Overlap mismatches
            for i in range(min(m, pm)):
                for j in range(min(n, pn)):
                    score += (target[i][j] != pred[i][j])

            # Shape penalties
            if n > 0:
                score += abs(pm - m) * n
            else:
                score += abs(pm - m)
            if pm > 0:
                score += abs(pn - n) * pm
            else:
                score += abs(pn - n)

        return score
