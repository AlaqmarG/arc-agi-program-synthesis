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
        file = json.load(file)

        for id, data in list(file.items()) if limit == -1 else list(file.items())[:limit]:
            data_set[id] = Data(id, data['train'], data['test'], None)

    with open("./benchmark/arc-agi_solutions.json") as file:
        file = json.load(file)

        for id, data in list(file.items()) if limit == -1 else list(file.items())[:limit]:
            if data_set[id]:
                for index, value in enumerate(data_set[id].test):
                    value['output'] = data[index]
            else:
                error("Missing Solutions for available challenges")

    return data_set