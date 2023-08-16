from UWBE_PROJECT.python.utils.csv_handler import CsvHandler
from UWBE_PROJECT.python.utils.inputs import get_object_id
from matplotlib import pyplot as plt

if __name__ == '__main__':
    csv_handler = CsvHandler()
    datasets, indexes = csv_handler.read_csv()
    obj_id = get_object_id()

    for dataset in datasets:

        dataset.pop(0)
        time_start = float(dataset[0][10])
        timestamps = []
        velocities = []
        for data in dataset:
            if str(data[0]) == obj_id:
                velocities.append(float(data[4]))
                timestamps.append(float(data[10])-time_start)
        plt.plot(timestamps, velocities)
        plt.show()


