import time
import data
from search import Search

search = Search()

# Get data set
num_data = 6
data_set = data.get_data(num_data)

def test_search_algorithm(search_function):
    start_time = time.time()
    trained = 0
    solved = 0

    for data in data_set.values():
        sol_program = search_function(data.train)

        if sol_program is None:
            continue

        trained += 1

        print(data.test)

        if search.validate_program(sol_program, data.test):
            solved += 1

    return time.time() - start_time, trained / num_data * 100, solved / num_data * 100, 

# BFS Search
bfs_results = test_search_algorithm(search.bfs)

print(f"==================================")
print(f"| Alg | Time | Train % |  Sol %  |")
print(f"==================================")
print(f"| BFS | {bfs_results[0]:3.0f}s | {bfs_results[1]:6.2f}% | {bfs_results[2]:6.2f}% |")
print(f"==================================")