from UWBE_PROJECT.python.utils.csv_handler import CsvHandler
from UWBE_PROJECT.python.utils.inputs import get_object_id

if __name__ == '__main__':
    csv_handler = CsvHandler()
    datasets, indexes = csv_handler.read_csv()
    obj_id = get_object_id()

    for dataset in datasets:

        moving_time = 0.0
        idle_time = 0.0

        dataset.pop(0)
        start_time = float(dataset[0][10])

        for data in dataset:
            action_state = data[9]
            if str(data[0]) == obj_id:
                if action_state == "IDLE":
                    idle_time += (float(data[10]) - start_time)
                elif action_state == "MOVING":
                    moving_time += (float(data[10]) - start_time)
                start_time = float(data[10])

        print(f"Moving_time: {moving_time}")
        print(f"IDLE_time: {idle_time}")
        print("\n")


