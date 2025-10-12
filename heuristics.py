class Heuristics:
    def __call__(self, program, train):
        return self.mismatch_sum(program, train)

    def mismatch_sum(self, program, train):
        score = 0
        try:
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
        except Exception:
            # Bad programs get a high score
            return 10**9

        return score
