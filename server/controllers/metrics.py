import csv
import os

def get_data():
    current_dir = os.path.dirname(__file__) 
    data_file_path = os.path.join(current_dir, "../data/mock_ga.csv") 

    with open(data_file_path) as csv_file:
        reader = csv.DictReader(csv_file)
        data = [row for row in reader]

    return data