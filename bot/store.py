import os
import pickle


class IntListStore:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data: list[int] = []
        self.read_data()

    def read_data(self):
        if os.path.isfile(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    self.data.append(int(line.strip()))
        return self.data

    def write_data(self):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write('\n'.join([str(group) for group in self.data]))

    def add_item(self, item: int):
        self.data.append(item)
        self.write_data()

    def del_item(self, item: int):
        if item in self.data:
            self.data.remove(item)
        self.write_data()


class DictStore:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data: dict[int, str] = {}
        self.read_data()

    def read_data(self):
        if os.path.isfile(self.file_path):
            with open(self.file_path, 'rb') as file:
                self.data = pickle.load(file)
        return self.data

    def write_data(self):
        with open(self.file_path, 'wb') as file:
            pickle.dump(self.data, file)

    def add_item(self, key, value):
        self.data[key] = value
        self.write_data()

    def del_item(self, key):
        if key in self.data:
            del self.data[key]
        self.write_data()
