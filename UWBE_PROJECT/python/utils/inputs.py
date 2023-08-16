import os
import csv
def choose_csv(recording_path):
    datasets = []
    indexes = []
    print("Enter s to begin or q to quit")
    while 1:
        counter = str(input("Enter a csv number: "))
        if "q" in counter:  # quit calibration
            raise SystemExit
        elif "s" in counter:  # begin calibration
            if len(datasets) > 0:
                return datasets, indexes
            else:
                print("No data!")
        elif counter.isnumeric() and counter not in indexes:
            path = os.path.join(recording_path, f'Raw_Data_{counter}.csv')
            if not os.path.exists(path):
                print(path)
                print("No such recording! Please Try Again")
            else:
                file = open(path, "r")
                data = list(csv.reader(file, delimiter=","))
                file.close()
                datasets.append(data)
                indexes.append(counter)
        else:
            print("Invalid Input. Please Try Again")

def choose_output_folder():
    user_input = str(input("Enter output directory: "))
    return user_input


def get_object_id():
    user_input = input("Enter object id: ")
    if user_input == "q":
        raise SystemExit
    return user_input

