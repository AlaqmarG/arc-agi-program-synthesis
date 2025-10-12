class Heuristics:
    def __init__(self):
        # Performance tracking for each heuristic
        self.stats = {
            'mismatch': {'successes': 0, 'attempts': 0},
            'color_dist': {'successes': 0, 'attempts': 0}
        }
        # Cache for last successful program complexity per heuristic
        self.last_success = {}
        self.prev_values = {}  # Track previous heuristic values
    
    def __call__(self, program, train):
        return self.meta_heuristic(program, train)
        
    def meta_heuristic(self, program, train):
        # Get base scores
        h1 = self.mismatch_sum(program, train)
        h2 = self.color_dist_shape(program, train)
        
        # Get problem features from first example
        example = train[0]
        output = example['output']
        grid_size = len(output) * len(output[0]) if output and output[0] else 0
        unique_colors = len({cell for row in output for cell in row})
        
        # Compute success rates
        h1_rate = (self.stats['mismatch']['successes'] + 1) / (self.stats['mismatch']['attempts'] + 1)
        h2_rate = (self.stats['color_dist']['successes'] + 1) / (self.stats['color_dist']['attempts'] + 1)
        
        # Adjust weights based on problem features and history
        if grid_size < 16:
            w1, w2 = 0.7, 0.3  # Small grids favor direct matching
        elif unique_colors > 4:
            w1, w2 = 0.4, 0.6  # Many colors favor pattern matching
        else:
            w1, w2 = 0.5, 0.5  # Default equal weighting
            
        # Adjust weights by success rates
        w1 *= h1_rate
        w2 *= h2_rate
        total = w1 + w2
        w1 /= total
        w2 /= total
        
        # Track attempts
        self.stats['mismatch']['attempts'] += 1
        self.stats['color_dist']['attempts'] += 1
        
        # Get program key for tracking
        prog_key = str(program)
        
        # Check if this program improves on previous values
        if prog_key in self.prev_values:
            old_h1, old_h2 = self.prev_values[prog_key]
            if h1 < old_h1 and h2 < old_h2:
                # Both heuristics showing improvement
                self.stats['mismatch']['successes'] += 1
                self.stats['color_dist']['successes'] += 1
                
        # Store current values
        self.prev_values[prog_key] = (h1, h2)
        
        # Compute weighted score
        return w1 * h1 + w2 * h2

    def color_dist_shape(self, program, train):
        score = 0
        
        for ex in train:
            target = ex['output']
            try:
                pred = program.apply_program(ex['input'])
            except Exception:
                return float('inf')

            # 1. Shape analysis
            t_height, t_width = len(target), len(target[0]) if target else 0
            p_height, p_width = len(pred), len(pred[0]) if pred else 0
            
            # Penalize aspect ratio differences
            if t_width and p_width:
                t_ratio = t_height / t_width
                p_ratio = p_height / p_width
                score += abs(t_ratio - p_ratio) * 10
            
            # 2. Color distribution comparison
            t_colors = {}
            p_colors = {}
            
            # Count colors in target
            for row in target:
                for cell in row:
                    t_colors[cell] = t_colors.get(cell, 0) + 1
            
            # Count and compare colors in prediction
            for row in pred:
                for cell in row:
                    p_colors[cell] = p_colors.get(cell, 0) + 1
            
            # Compare color frequencies
            all_colors = set(t_colors.keys()) | set(p_colors.keys())
            t_total = t_height * t_width
            p_total = p_height * p_width
            
            for color in all_colors:
                t_freq = t_colors.get(color, 0) / t_total
                p_freq = p_colors.get(color, 0) / p_total
                score += abs(t_freq - p_freq) * 20
            
            # 3. Local pattern matching (2x2 windows)
            def get_patterns(grid, h, w):
                patterns = {}
                for i in range(h-1):
                    for j in range(w-1):
                        pat = (
                            grid[i][j],
                            grid[i][j+1],
                            grid[i+1][j],
                            grid[i+1][j+1]
                        )
                        patterns[pat] = patterns.get(pat, 0) + 1
                return patterns
            
            if t_height > 1 and t_width > 1 and p_height > 1 and p_width > 1:
                t_patterns = get_patterns(target, t_height, t_width)
                p_patterns = get_patterns(pred, p_height, p_width)
                
                # Compare pattern frequencies
                all_patterns = set(t_patterns.keys()) | set(p_patterns.keys())
                t_total_patterns = (t_height-1) * (t_width-1)
                p_total_patterns = (p_height-1) * (p_width-1)
                
                for pat in all_patterns:
                    t_freq = t_patterns.get(pat, 0) / t_total_patterns
                    p_freq = p_patterns.get(pat, 0) / p_total_patterns
                    score += abs(t_freq - p_freq) * 15

        return score

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
