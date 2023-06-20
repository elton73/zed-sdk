import os
import csv
from UWBE_PROJECT.python.utils.inputs import choose_velocity_csv
class CsvHandler:
    def __init__(self):
        self._csv_file = None
        self._csv_writer = None
        self._path_string = r'C:\Users\ML-2\Documents\GitHub\zed-sdk\UWBE_PROJECT\csv'
    def setup_csv(self, csv_name):
        if not os.path.exists(self._path_string):
            os.makedirs(self._path_string)

        counter = 1
        output_csv = os.path.join(self._path_string, f"{csv_name}_{counter}.csv")
        while os.path.exists(output_csv):
            counter += 1
            output_csv = os.path.join(self._path_string, f"{csv_name}_{counter}.csv")
        self._csv_file = open(output_csv, 'w', newline='')
        self._csv_writer = csv.writer(self._csv_file)

    def write_csv(self, data):
        if not isinstance(data, list):
            data = [data]
        self._csv_writer.writerow(data)

    def close_csv(self):
        if self._csv_file:
            self._csv_file.close()
            self._csv_file = None

    def read_csv(self):
        return choose_velocity_csv(self._path_string)




