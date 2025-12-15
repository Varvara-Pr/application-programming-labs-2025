import os
import csv
from typing import Iterator, List


class ImageIterator:
    """
    Итератор по путям к файлам из CSV аннотации или директории с изображениями
    """

    def __init__(self, path: str) -> None:
        self.path = path
        self.data: List[str] = []
        self.index: int = 0

        if path.endswith(".csv"):
            self._load_csv(path)
        else:
            self._load_folder(path)

    def _load_folder(self, folder_path: str) -> None:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith((".png", ".jpg", ".jpeg")):
                    self.data.append(os.path.join(root, file))

    def _load_csv(self, csv_path: str) -> None:
        with open(csv_path, "r", encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row:
                    self.data.append(row[0])

    def __iter__(self) -> Iterator[str]:
        self.index = 0
        return self

    def __next__(self) -> str:
        if self.index >= len(self.data):
            raise StopIteration
        item = self.data[self.index]
        self.index += 1
        return item

    def __len__(self) -> int:
        return len(self.data)
