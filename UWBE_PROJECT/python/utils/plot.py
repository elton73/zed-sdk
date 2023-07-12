from UWBE_PROJECT.python.utils.csv_handler import CsvHandler
from UWBE_PROJECT.python.utils.inputs import get_object_id

if __name__ == '__main__':
    csv_handler = CsvHandler()
    datasets, indexes = csv_handler.read_csv()
    obj_id = get_object_id()

    for dataset in datasets:

        dataset.pop(0)
        timestamps = []
        velocities = []
        for data in dataset:
            print(data)


