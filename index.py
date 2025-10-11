import time
from data import Data
from search import Search

data = Data()
search = Search()

ids = data.get_ids()
train_data = data.get_train_data()
solution_data = data.get_solution_data()

num_challenges = len(train_data)

## BFS Search
# Iterate over training data
train_solutions = []

bfs_start = time.time() # Log Start Time
num_trained = 0

for i, in_out_pair in enumerate(train_data):
    print(f"Solving {ids[i]} : {i}/{num_challenges}", end='\r')

    sol = search.bfs(in_out_pair)
    train_solutions.append(sol)

    # Count train solutions found
    if not (sol.left is None and sol.right is None):
        num_trained += 1

bfs_time_taken = time.time() - bfs_start # Calculate wall clock time
test_data = data.get_test_data()
num_solved = 0

for i, inputs in enumerate(test_data):
    solution = train_solutions[i]

    # Count correct solutions
    test_cases = [{'input': test_case['input'], 'output': output_grid} for test_case, output_grid in zip(inputs, solution_data[i])]
    if search.validate_program(solution, test_cases):
        num_solved += 1


print(f"================================")
print(f"| Alg | Time | Train % | Sol % |")
print(f"================================")
print(f"| BFS | {bfs_time_taken:3.0f}s | {(num_trained / len(train_data) * 100):6.2f}% | {(num_solved / len(train_data) * 100):4.2f}% |")
print(f"================================")