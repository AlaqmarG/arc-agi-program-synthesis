import json
from os import error

class Data:
    def __init__(self, id, train, test, solution) -> None:
        self.id = id
        self.train = train
        self.test = test

def get_data(limit=-1):
    data_set = {}

    with open("./benchmark/arc-agi_challenges.json") as file:
        challenges = json.load(file)

        for id, challenge_data in list(challenges.items()) if limit == -1 else list(challenges.items())[:limit]:
            data_set[id] = Data(id, challenge_data['train'], challenge_data['test'], None)

    with open("./benchmark/arc-agi_solutions.json") as file:
        solutions = json.load(file)

        # Then, match solutions to their test cases
        for id in data_set.keys():
            if id in solutions:
                solution_data = solutions[id]
                
                for test_case, solution in zip(data_set[id].test, solution_data):
                    test_case['output'] = solution

    return data_set