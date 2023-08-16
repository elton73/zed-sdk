import os
import csv
from UWBE_PROJECT.python.utils.inputs import choose_csv
class CsvHandler:
    def __init__(self):
        self._csv_file = None
        self._csv_writer = None
        self.path_string = r'C:\Users\ML-2\Documents\GitHub\zed-sdk\UWBE_PROJECT\csv' # Csv save directory
    def setup_csv(self, csv_name):
        if not os.path.exists(self.path_string):
            os.makedirs(self.path_string)

        counter = 1
        output_csv = os.path.join(self.path_string, f"{csv_name}_{counter}.csv")
        while os.path.exists(output_csv):
            counter += 1
            output_csv = os.path.join(self.path_string, f"{csv_name}_{counter}.csv")
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
        return choose_csv(self.path_string)

    def set_custom_path(self, new_path):
        self.path_string = new_path





