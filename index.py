import time
import data
from heuristics import Heuristics
from search import Search

search = Search()

# Get data set
num_data = 28
data_set = data.get_data(num_data)

def test_search_algorithm(search_function, type):
    train_time = []
    solve_time = []
    results = {}  # Track results per test case

    trained = 0
    solved = 0

    for data in data_set.values():
        train_start = time.time()
        sol_program = search_function(data.train)

        train_duration = time.time() - train_start
        result = {'id': data.id, 'found_solution': False, 'solution': None, 
                 'train_time': train_duration}

        if sol_program is not None:
            trained += 1
            train_time.append(train_duration)

            solve_start = time.time()
            is_valid = search.validate_program(sol_program, data.test)
            solve_duration = time.time() - solve_start
            solve_time.append(solve_duration)

            result.update({
                'found_solution': True,
                'solution': str(sol_program),
                'complexity': sol_program.complexity,
                'valid': is_valid,
                'solve_time': solve_duration
            })

            if is_valid:
                print("\033[K", end="", flush=True)
                print(f"{type}: Solved {data.id} with {sol_program}")
                solved += 1
            else:
                print("\033[K", end="", flush=True)
                print(f"{type}: Failed {data.id} with {sol_program}")

        results[data.id] = result

    stats = {
        'avg_train_time': sum(train_time) / len(train_time) if train_time else 0,
        'avg_solve_time': sum(solve_time) / len(solve_time) if solve_time else 0,
        'solved': solved,
        'total': num_data,
        'success_rate': solved / num_data * 100,
        'results': results
    }

    return stats


# BFS Search
bfs_results = test_search_algorithm(search.bfs, "BFS")

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

gbfs_cell_results = test_search_algorithm(gbfs_cell_runner, "GBFS (Cell)")
gbfs_color_results = test_search_algorithm(gbfs_color_runner, "GBFS (Color)")
gbfs_meta_results = test_search_algorithm(gbfs_meta_runner, "GBFS (Meta)")

# A* with different heuristics
def astar_cell_runner(train):
    return search.a_star_search(train, cell_h.mismatch_sum)

def astar_color_runner(train):
    return search.a_star_search(train, color_h.color_dist_shape)

def astar_meta_runner(train):
    return search.a_star_search(train, meta_h.meta_heuristic)

astar_cell_results = test_search_algorithm(astar_cell_runner, "A* (Cell)")
astar_color_results = test_search_algorithm(astar_color_runner, "A* (Color)")
astar_meta_results = test_search_algorithm(astar_meta_runner, "A* (Meta)")


def format_time(time_val, unit):
    return f"{time_val:>10.0f}{unit:2}"

print(f"====================================================================")
print(f"| Algorithm    | Avg Train Time | Avg Solve Time | Num Sol | Sol % |")
print(f"====================================================================")
print(f"| BFS          |   {format_time(bfs_results['avg_train_time']*10**6, 'μs')} |   {format_time(bfs_results['avg_solve_time']*10**9, 'ns')} | {bfs_results['solved']:2.0f}/{bfs_results['total']:2.0f}   | {bfs_results['success_rate']:4.1f}% |")
print(f"|--------------|----------------|----------------|---------|-------|")
print(f"| GBFS (Cell)  |   {format_time(gbfs_cell_results['avg_train_time']*10**6, 'μs')} |   {format_time(gbfs_cell_results['avg_solve_time']*10**9, 'ns')} | {gbfs_cell_results['solved']:2.0f}/{gbfs_cell_results['total']:2.0f}   | {gbfs_cell_results['success_rate']:4.1f}% |")
print(f"| GBFS (Color) |   {format_time(gbfs_color_results['avg_train_time']*10**6, 'μs')} |   {format_time(gbfs_color_results['avg_solve_time']*10**9, 'ns')} | {gbfs_color_results['solved']:2.0f}/{gbfs_color_results['total']:2.0f}   | {gbfs_color_results['success_rate']:4.1f}% |")
print(f"| GBFS (Meta)  |   {format_time(gbfs_meta_results['avg_train_time']*10**6, 'μs')} |   {format_time(gbfs_meta_results['avg_solve_time']*10**9, 'ns')} | {gbfs_meta_results['solved']:2.0f}/{gbfs_meta_results['total']:2.0f}   | {gbfs_meta_results['success_rate']:4.1f}% |")
print(f"|--------------|----------------|----------------|---------|-------|")
print(f"| A* (Cell)    |   {format_time(astar_cell_results['avg_train_time']*10**6, 'μs')} |   {format_time(astar_cell_results['avg_solve_time']*10**9, 'ns')} | {astar_cell_results['solved']:2.0f}/{astar_cell_results['total']:2.0f}   | {astar_cell_results['success_rate']:4.1f}% |")
print(f"| A* (Color)   |   {format_time(astar_color_results['avg_train_time']*10**6, 'μs')} |   {format_time(astar_color_results['avg_solve_time']*10**9, 'ns')} | {astar_color_results['solved']:2.0f}/{astar_color_results['total']:2.0f}   | {astar_color_results['success_rate']:4.1f}% |")
print(f"| A* (Meta)    |   {format_time(astar_meta_results['avg_train_time']*10**6, 'μs')} |   {format_time(astar_meta_results['avg_solve_time']*10**9, 'ns')} | {astar_meta_results['solved']:2.0f}/{astar_meta_results['total']:2.0f}   | {astar_meta_results['success_rate']:4.1f}% |")
print(f"====================================================================")