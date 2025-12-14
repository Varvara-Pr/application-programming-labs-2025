import os
import csv


class ImageIterator:
    """
    Итератор по путям к файлам из CSV аннотации
    """
    
    def __init__(self, annotation_file: str):
        self.annotation_file = annotation_file
        self.data = []
        self.index = 0

    def __iter__(self):
        if os.path.exists(self.annotation_file):
            with open(self.annotation_file, 'r', encoding='utf-8-sig') as file:
                reader = csv.reader(file)
                next(reader)
                self.data = [row for row in reader]
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.data):
            result = self.data[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration