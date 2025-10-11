import json

class Data:
    num_data_points = 100

    def __init__(self) -> None:
        self.ids = []
        self.train_data = []
        self.test_data = []
        self.solution_data = []

        with open("./benchmark/arc-agi_challenges.json") as file:
            file = json.load(file)
            
            for id, data_set in list(file.items())[:Data.num_data_points]:
                self.ids.append(id)
                self.train_data.append(data_set["train"])
                self.test_data.append(data_set["test"])

        with open("./benchmark/arc-agi_solutions.json") as file:
            file = json.load(file)

            for id, data_set in list(file.items())[:Data.num_data_points]:
                self.solution_data.append(data_set)

    def get_ids(self):
        return self.ids

    def get_train_data(self):
        return self.train_data
    
    def get_test_data(self):
        return self.test_data
    
    def get_solution_data(self):
        return self.solution_data
