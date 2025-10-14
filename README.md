
# ARC-AGI Program Synthesis

This repository implements program synthesis for the ARC-AGI benchmark using advanced search algorithms (BFS, GBFS, and A*). It is designed for both research and educational purposes, supporting configurable operation costs and multiple heuristics to optimize solution discovery.

## Project Overview

- **Goal:** Automatically synthesize programs that solve visual reasoning tasks from the ARC-AGI benchmark.
- **Algorithms:** Includes Breadth-First Search (BFS), Greedy Best-First Search (GBFS), and A* Search, each with tunable heuristics and cost models.
- **Configurable:** Operation costs and heuristic strategies can be easily adjusted for experimentation and benchmarking.

## How to Run

1. **Requirements**
   - Python 3.14+ (recommended)
   - No external dependencies required for core functionality.

2. **Running Benchmarks**
   - Open a terminal in the project directory.
   - Execute:
     ```
     python index.py
     ```
   - The script will run all search algorithms on the provided benchmark tasks and print solution rates and timing statistics.

## Expected Output

- Solution rates (number of tasks solved) and timing for each algorithm.
- Progress logs for each search method.
- Results are printed to the console for easy comparison.

## Configuration

- **Heuristics:** Modify or extend heuristic functions in `heuristics.py` for custom search strategies.

## File Structure

- `index.py` — Main entry point; runs benchmarks and prints results.
- `program.py` — Program representation and cost model.
- `search.py` — Search algorithm implementations.
- `heuristics.py` — Heuristic functions for search guidance.
- `benchmark/` — Contains challenge and solution data.
- `config/op_costs.json` — Operation cost configuration.

## Academic Context

This project was developed as part of an assignment on program synthesis and search algorithms. It demonstrates the use of weighted cost models, heuristic design, and benchmarking for automated reasoning tasks.

---

For questions, see code comments or contact the repository owner.
