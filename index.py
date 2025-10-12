import time
import data
from search import Search
from heuristics import Heuristics

search = Search()
heuristics = Heuristics()

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

# GBFS Search with heuristic
def gbfs_runner(train):
    return search.gbfs_search(train, heuristics)

gbfs_results = test_search_algorithm(gbfs_runner)

# A* Search with heuristic
def astar_runner(train):
    return search.a_star_search(train, heuristics)

astar_results = test_search_algorithm(astar_runner)

print(f"==============================================================")
print(f"| Alg  | Avg Train Time | Avg Solve Time | Train % |  Sol %  |")
print(f"==============================================================")
print(f"| BFS  | {bfs_results[0]*10**6:12.0f}μs | {bfs_results[1]*10**9:12.0f}ns | {bfs_results[2]:6.2f}% | {bfs_results[3]:6.2f}% |")
print(f"| GBFS | {gbfs_results[0]*10**6:12.0f}μs | {gbfs_results[1]*10**9:12.0f}ns | {gbfs_results[2]:6.2f}% | {gbfs_results[3]:6.2f}% |")
print(f"|  A*  | {astar_results[0]*10**6:12.0f}μs | {astar_results[1]*10**9:12.0f}ns | {astar_results[2]:6.2f}% | {astar_results[3]:6.2f}% |")
print(f"==============================================================")