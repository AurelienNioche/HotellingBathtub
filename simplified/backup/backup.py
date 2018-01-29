import os
import pickle
import json
import datetime


class Backup:

    pickle_folder = "data/pickle"
    json_folder = "data/json"

    def __init__(self, parameters):

        self.parameters = parameters

    @staticmethod
    def timestamp():
        return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")

    def save(self):
        os.makedirs(self.pickle_folder, exist_ok=True)
        os.makedirs(self.json_folder, exist_ok=True)

        file_name = "{}".format(self.timestamp())

        # Save a summary of parameters in json
        with open("{}/{}.json".format(self.json_folder, file_name), "w") as f:

            param = self.parameters.dict()
            param.update({"name": file_name})

            json.dump(param, f, indent=2)

        with open("{}/{}.p".format(self.pickle_folder, file_name), "wb") as f:
            pickle.dump(self, f)

        return file_name

    @classmethod
    def load(cls, file_name, folder_name):

        if folder_name is None:
            folder_name = cls.pickle_folder

        with open("{}/{}.p".format(folder_name, file_name), "rb") as f:
            return pickle.load(f)


class RunBackup(Backup):

    def __init__(self, parameters, positions, prices, profits):
        super().__init__(parameters)

        self.positions = positions
        self.prices = prices
        self.profits = profits


class PoolBackup(Backup):

    def __init__(self, parameters, backups):
        super().__init__(parameters)

        self.backups = backups
