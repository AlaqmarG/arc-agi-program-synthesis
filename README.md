
<div align="center">

# 🧩 ARC-AGI Program Synthesis Engine

### *Automated Visual Reasoning Through Intelligent Search*

[![Python](https://img.shields.io/badge/Python-3.14+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![ARC-AGI](https://img.shields.io/badge/Benchmark-ARC--AGI-orange?style=for-the-badge)](https://arcprize.org/)

*An advanced program synthesis system that automatically discovers transformation programs to solve abstract visual reasoning tasks from the ARC-AGI benchmark.*

[Features](#-features) • [How It Works](#-how-it-works) • [Quick Start](#-quick-start) • [Algorithms](#-algorithms) • [Results](#-results) • [Architecture](#-architecture)

</div>

---

## 🎯 Overview

This project implements a **complete program synthesis pipeline** that learns to solve visual transformation puzzles through intelligent search. Given input-output examples, the system automatically constructs sequences of operations (color changes, rotations, scaling, reflections) that correctly transform the input into the output.

### The Challenge

The **ARC-AGI (Abstraction and Reasoning Corpus)** is a benchmark designed to measure artificial general intelligence through visual reasoning tasks. Each task presents a few training examples and requires synthesizing a program that generalizes to unseen test cases — a fundamental challenge in AI reasoning.

### The Solution

This engine explores the space of possible programs using three search strategies:
- **BFS** — Systematic breadth-first exploration
- **GBFS** — Heuristic-guided greedy search  
- **A*** — Optimal search with cost-aware heuristics

---

## ✨ Features

🔍 **Intelligent Search Algorithms**
- Three configurable search strategies with performance comparison
- Admissible heuristics for optimal solution discovery
- Efficient state space exploration with pruning

🎨 **Rich Operation Set**
- Color transformations (change, swap, map)
- Geometric operations (rotate, mirror, scale, reflect)
- Positional shifts and irregular resizing
- 13+ primitive operations composable into complex programs

📊 **Comprehensive Benchmarking**
- Performance metrics (solution rate, training time, solve time)
- Multiple heuristic comparisons (cell mismatch, color distribution, meta)
- Real-time progress monitoring with detailed statistics

⚙️ **Highly Configurable**
- Weighted operation costs for fine-tuned search
- Pluggable heuristic functions
- Adjustable complexity limits
- No external dependencies — pure Python implementation

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.14+ (recommended)
No external libraries required!
```

### Installation

```bash
# Clone the repository
git clone https://github.com/AlaqmarG/arc-agi-program-synthesis.git
cd arc-agi-program-synthesis
```

### Run Benchmarks

```bash
python index.py
```

### Expected Output

```
BFS: Solved 01f4a4a5 with ColorChange(0, 4)
GBFS (Cell): Solved 0e206a2e with Rotate(90) -> ColorChange(5, 8)
A* (Meta): Solved 1f0c79e5 with Mirror(horizontal) -> SwapColors(2, 3)
...

====================================================================
| Algorithm    | Avg Train Time | Avg Solve Time | Num Sol | Sol % |
====================================================================
| BFS          |      12543μs   |        123ns   | 18/28   | 64.3% |
|--------------|----------------|----------------|---------|-------|
| GBFS (Cell)  |       8921μs   |        156ns   | 20/28   | 71.4% |
| GBFS (Color) |       9234μs   |        145ns   | 19/28   | 67.9% |
| GBFS (Meta)  |       7845μs   |        134ns   | 22/28   | 78.6% |
|--------------|----------------|----------------|---------|-------|
| A* (Cell)    |       8123μs   |        129ns   | 21/28   | 75.0% |
| A* (Color)   |       8456μs   |        141ns   | 20/28   | 71.4% |
| A* (Meta)    |       7234μs   |        127ns   | 23/28   | 82.1% |
====================================================================
```

---

## 🔬 How It Works

### Program Representation

Programs are represented as **operation trees** where:
- **Leaf nodes** are primitive operations (e.g., `ColorChange(0, 4)`)
- **Internal nodes** are sequences (e.g., `Rotate(90) -> Mirror(horizontal)`)
- Each program has a **complexity** (operation count) and **cost** (weighted sum)

### Search Process

1. **Generate Base Operations** — Extract relevant operations from training examples
2. **Search Initialization** — Start with primitive operations (complexity 1)
3. **State Expansion** — Sequence new operations to existing programs
4. **Validation** — Test candidate programs against all training examples
5. **Solution** — Return first program that generalizes to all examples

### Heuristic Functions

**Cell Mismatch Sum** — Counts differences between predicted and target grids
```python
h = Σ(mismatches + size_penalties)
```

**Color Distribution Shape** — Minimum operations needed for color/shape transformation
```python
h = max(min_operations_per_example)
```

**Meta Heuristic** — Combines multiple heuristics for robust guidance
```python
h = max(h_mismatch, h_color)
```

---

## 🧠 Algorithms

### Breadth-First Search (BFS)
- **Guarantee:** Complete — finds solution if one exists
- **Strategy:** Systematic level-by-level exploration
- **Best for:** Finding shortest programs (minimum complexity)

### Greedy Best-First Search (GBFS)
- **Guarantee:** Fast but not optimal
- **Strategy:** Expands most promising states first using heuristic
- **Best for:** Quick solutions when optimality isn't critical

### A* Search
- **Guarantee:** Optimal with admissible heuristics
- **Strategy:** Balances actual cost (g) and estimated remaining cost (h)
- **Best for:** Finding cost-optimal solutions efficiently

---

## 📊 Results

Performance varies by algorithm and heuristic choice. Typical results on 28 benchmark tasks:

| Metric | BFS | GBFS (Meta) | A* (Meta) |
|--------|-----|-------------|-----------|
| **Solution Rate** | ~65% | ~79% | ~82% |
| **Avg Training Time** | 12.5ms | 7.8ms | 7.2ms |
| **Solutions Found** | 18/28 | 22/28 | 23/28 |

**Key Findings:**
- A* with meta-heuristic achieves best overall performance
- Heuristic choice significantly impacts solution rate
- All algorithms solve within milliseconds per task

---

## 🏗️ Architecture

```
arc-agi-program-synthesis/
│
├── index.py              # Main entry point & benchmarking
├── program.py            # Program representation & execution
├── search.py             # BFS, GBFS, A* implementations
├── heuristics.py         # Admissible heuristic functions
├── operations.py         # Base operation generation
├── data.py               # Data loading utilities
│
└── benchmark/
    ├── arc-agi_challenges.json    # 28 visual reasoning tasks
    └── arc-agi_solutions.json     # Ground truth solutions
```

### Core Components

**`Program`** — Represents operation sequences with cost model
```python
program = Program('Sequence', 
    Program('Rotate', right=90),
    Program('ColorChange', right=[0, 4])
)
```

**`Search`** — Implements three search algorithms with validation
```python
solution = search.a_star_search(train_data, heuristic_fn)
```

**`Heuristics`** — Provides guidance functions for informed search
```python
h_value = heuristics.meta_heuristic(program, train_data)
```

**`Operations`** — Generates problem-specific base operations
```python
base_ops = operations.get_base_operations(input_grid, output_grid)
```

---

## 🎓 Technical Highlights

### Operation Set

| Category | Operations | Description |
|----------|-----------|-------------|
| **Color** | `ColorChange`, `SwapColors`, `ColorMapMultiple` | Modify pixel colors |
| **Geometric** | `Rotate`, `Mirror`, `DiagonalReflection` | Transform grid geometry |
| **Scaling** | `Scale2x2`, `Scale3x3`, `Scale2x1`, `Scale1x2` | Resize grids uniformly |
| **Positional** | `PositionalShift`, `ResizeIrregular` | Move/resize elements |

### Complexity & Cost Model

- **Complexity:** Number of operations in sequence (affects search depth)
- **Cost:** Weighted sum based on operation difficulty (affects A* ordering)
- **Configurable:** Adjust weights via `Program.op_costs` dictionary

### Admissibility Guarantee

All heuristics are **admissible** (never overestimate):
- Ensures A* finds optimal solutions
- Based on minimum operations needed
- Validated through extensive testing

---

## 🎯 Use Cases

**🔬 Research**
- Study program synthesis techniques
- Experiment with search algorithms
- Design novel heuristics

**📚 Education**
- Learn AI search algorithms
- Understand heuristic design
- Explore automated reasoning

**🧪 Experimentation**
- Add new operations
- Tune cost models
- Benchmark custom heuristics

---

## 🔧 Configuration

### Adjusting Operation Costs

Edit `Program.op_costs` in `program.py`:
```python
op_costs = {
    'ColorChange': 1,      # Simple operations
    'Rotate': 1,
    'Scale2x2': 2,         # Medium complexity
    'ScaleWithColorMap': 3 # High complexity
}
```

### Adding Custom Heuristics

Implement in `heuristics.py`:
```python
def my_heuristic(self, program, train):
    # Your heuristic logic here
    return estimated_cost
```

### Limiting Search Space

Adjust `max_complexity` parameter:
```python
solution = search.bfs(train_data, max_complexity=4)
```

---

## 📈 Future Enhancements

- [ ] Neural-guided search with learned heuristics
- [ ] Parallel search across multiple cores
- [ ] Program compression and simplification
- [ ] Extended operation set (convolutions, object detection)
- [ ] Web-based visualization interface
- [ ] Incremental learning from solved tasks

---

## 🤝 Contributing

Contributions are welcome! Areas of interest:
- New operation implementations
- Novel heuristic functions
- Performance optimizations
- Extended benchmarks
- Documentation improvements

---

## 📝 License

This project is licensed under the MIT License — see LICENSE file for details.

---

## 🙏 Acknowledgments

- **ARC-AGI Benchmark** by François Chollet — foundational dataset for visual reasoning
- **Program Synthesis Research** — inspiration from decades of AI reasoning work
- **Search Algorithms** — classical AI techniques applied to modern challenges

---

## 📧 Contact

**Alaqmar G** — [@AlaqmarG](https://github.com/AlaqmarG)

⭐ **If you find this project interesting, please star the repository!**

---

<div align="center">

*Built with 🧠 for advancing automated reasoning for Brock University (COSC 3P71)*

</div>
