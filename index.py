import time
import data
from heuristics import Heuristics
from search import Search

search = Search()

# Get data set
num_data = 6
data_set = data.get_data(num_data)

def test_search_algorithm(search_function):
    train_time = []
    solve_time = []

    trained = 0
    solved = 0

    for data in data_set.values():
        train_start = time.time()
        sol_program = search_function(data.train)

        if sol_program is None:
            continue

        trained += 1
        train_time.append(time.time() - train_start)

        solve_start = time.time()

        if search.validate_program(sol_program, data.test):
            solved += 1

        solve_time.append(time.time() - solve_start)

    return sum(train_time) / len(train_time), sum(solve_time) / len(solve_time), trained / num_data * 100, solved / num_data * 100, 


# BFS Search
bfs_results = test_search_algorithm(search.bfs)

# Initialize heuristic instances (to maintain stats)
cell_h = Heuristics()
color_h = Heuristics()
meta_h = Heuristics()

# GBFS with different heuristics
def gbfs_cell_runner(train):
    return search.gbfs_search(train, cell_h.mismatch_sum)

def gbfs_color_runner(train):
    return search.gbfs_search(train, color_h.color_dist_shape)

def gbfs_meta_runner(train):
    return search.gbfs_search(train, meta_h.meta_heuristic)

gbfs_cell_results = test_search_algorithm(gbfs_cell_runner)
gbfs_color_results = test_search_algorithm(gbfs_color_runner)
gbfs_meta_results = test_search_algorithm(gbfs_meta_runner)

# A* with different heuristics
def astar_cell_runner(train):
    return search.a_star_search(train, cell_h.mismatch_sum)

def astar_color_runner(train):
    return search.a_star_search(train, color_h.color_dist_shape)

def astar_meta_runner(train):
    return search.a_star_search(train, meta_h.meta_heuristic)

astar_cell_results = test_search_algorithm(astar_cell_runner)
astar_color_results = test_search_algorithm(astar_color_runner)
astar_meta_results = test_search_algorithm(astar_meta_runner)


def format_time(time_val, unit):
    return f"{time_val:>10.0f}{unit:2}"

print(f"====================================================================")
print(f"| Algorithm    | Avg Train Time | Avg Solve Time | Train % | Sol % |")
print(f"====================================================================")
print(f"| BFS          |   {format_time(bfs_results[0]*10**6, 'μs')} |   {format_time(bfs_results[1]*10**9, 'ns')} | {bfs_results[2]:5.1f}%  | {bfs_results[3]:4.1f}% |")
print(f"|--------------|----------------|----------------|---------|-------|")
print(f"| GBFS (Cell)  |   {format_time(gbfs_cell_results[0]*10**6, 'μs')} |   {format_time(gbfs_cell_results[1]*10**9, 'ns')} | {gbfs_cell_results[2]:5.1f}%  | {gbfs_cell_results[3]:4.1f}% |")
print(f"| GBFS (Color) |   {format_time(gbfs_color_results[0]*10**6, 'μs')} |   {format_time(gbfs_color_results[1]*10**9, 'ns')} | {gbfs_color_results[2]:5.1f}%  | {gbfs_color_results[3]:4.1f}% |")
print(f"| GBFS (Meta)  |   {format_time(gbfs_meta_results[0]*10**6, 'μs')} |   {format_time(gbfs_meta_results[1]*10**9, 'ns')} | {gbfs_meta_results[2]:5.1f}%  | {gbfs_meta_results[3]:4.1f}% |")
print(f"|--------------|----------------|----------------|---------|-------|")
print(f"| A* (Cell)    |   {format_time(astar_cell_results[0]*10**6, 'μs')} |   {format_time(astar_cell_results[1]*10**9, 'ns')} | {astar_cell_results[2]:5.1f}%  | {astar_cell_results[3]:4.1f}% |")
print(f"| A* (Color)   |   {format_time(astar_color_results[0]*10**6, 'μs')} |   {format_time(astar_color_results[1]*10**9, 'ns')} | {astar_color_results[2]:5.1f}%  | {astar_color_results[3]:4.1f}% |")
print(f"| A* (Meta)    |   {format_time(astar_meta_results[0]*10**6, 'μs')} |   {format_time(astar_meta_results[1]*10**9, 'ns')} | {astar_meta_results[2]:5.1f}%  | {astar_meta_results[3]:4.1f}% |")
print(f"====================================================================")