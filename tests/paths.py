from pathlib import Path
import pandas as pd
import os


def save_csv(record):
    file_number = 1
    file_saved = False
    while file_saved == False:
        if os.path.exists(f"output/benchmarx_{file_number}.csv") == True:
            file_number += 1
        else:
            file_saved = True

    print(file_number)
    record.to_csv(os.path.abspath(f"output/benchmarx_{file_number}.csv"))


def main():
    record = pd.DataFrame([{"a": 1, "b": 2}, {"c": 3, "d": 4}])
    print(save_csv(record))


main()
