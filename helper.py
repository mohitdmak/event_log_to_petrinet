import sys
import csv
import pm4py
import subprocess
import pandas as pd 
from pathlib import Path
from pm4py.utils import EventLog

def convertXesToCsv(file_path, out_file):
    print(f"< < < File Path recieved: {file_path}")
    file = Path(file_path)
    if not file.exists():
        raise FileExistsError(f"Given File: `{file}` does not exist < < <") 
    else:
        print(f"Given File: `{file}` exists...")
        if not str(file).endswith(".xes"):
            raise TypeError(f"Given File: `{file}` is not of .xes type < < <")
        log = pm4py.read_xes(str(file))
        pd = pm4py.convert_to_dataframe(log)
        pd.to_csv(path_or_buf=out_file)

def standardizeCsv(file_path):
    print(f"< < < File Path recieved: {file_path}")
    file = Path(file_path)
    if not file.exists():
        raise FileExistsError(f"Given File: `{file}` does not exist < < <") 
    else:
        print(f"Given File: `{file}` exists...")
        if not str(file).endswith(".csv"):
            raise TypeError(f"Given File: `{file}` is not of .csv type < < <")
        # reader = csv.reader(x.replace('\0', '') for x in mycsv)
        reader = list(csv.reader(open(file, "rU", encoding='utf-16'), delimiter='|'))
        writer = csv.writer(open(file, 'w'), delimiter=',')
        writer.writerows(row for row in reader)
        
    

if __name__ == "__main__":
    print("What action do you need to do?\n    1: Convert Xes to Csv\n    2: Standardize Csv File (delimeter)")
    action = int(input())
    if action == 1:
        print("Write relative/absolute file path of xes file:")
        file_path = str(input())
        print("Write relative/absolute file path of csv file to write:")
        out_file = str(input())
        convertXesToCsv(file_path, out_file)
    elif action == 2:
        print("Write relative/absolute file path of the csv file:")
        file_path = str(input())
        standardizeCsv(file_path)
